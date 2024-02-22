#!/usr/bin/env python

import argparse
import json
import os
import re
import subprocess
import tempfile

import pympi
from huggingface_hub import snapshot_download
from signwriting.tokenizer import SignWritingTokenizer


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--elan', required=True, type=str, help='path to elan file')
    return parser.parse_args()


def main():
    args = get_args()

    print('Downloading model...')
    path_to_model = snapshot_download(repo_id="sign/sockeye-signwriting-to-text")

    print('Loading ELAN file...')
    eaf = pympi.Elan.Eaf(file_path=args.elan, author="sign-language-processing/signbank-plus")
    sign_annotations = eaf.get_annotation_data_for_tier('SIGN')

    if len(sign_annotations) == 0:
        print('No signs available to translate')
        return

    sign_language_code = dict(eaf.get_properties()).get('language', None)
    if sign_language_code is None:
        print('No language code available')
        return

    tokenizer = SignWritingTokenizer()

    sentence_to_translate = {}
    for tier in eaf.get_tier_names():
        if tier.startswith('SENTENCE_'):
            spoken_language_code = tier.split('_')[1]
            sentence_boundaries = eaf.get_annotation_data_for_tier(tier)
            for (sentence_start, sentence_end, _) in sentence_boundaries:
                signs_in_sentence = [sign for sign_start, sign_end, sign in sign_annotations
                                     if sentence_start <= sign_end and sentence_end >= sign_start]
                if len(signs_in_sentence) == 0:
                    continue

                signs_tokens = " ".join(tokenizer.text_to_tokens(' '.join(signs_in_sentence), box_position=False))
                input_sentence = f"${spoken_language_code} ${sign_language_code} {signs_tokens}"
                sentence_to_translate[(tier, sentence_start, sentence_end)] = input_sentence

    print(f"Translating {len(sentence_to_translate)} sentences...")

    # Write sentences to a temporary file
    temp_input_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    for sentence in sentence_to_translate.values():
        temp_input_file.write(sentence + "\n")
    temp_input_file.close()

    temp_output_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    temp_output_file.close()

    # Call the translation script
    cmd = ['python', '-m', 'sockeye.translate', '-m', path_to_model,
           '--input', temp_input_file.name, '--output', temp_output_file.name, '--nbest-size=5']
    print(' '.join(cmd))
    subprocess.run(cmd)

    # Read the output file
    with open(temp_output_file.name, 'r') as f:
        lines = f.readlines()
        # Remove BPE tokenization
        lines = [re.sub('(@@ |@@$)', '', line.strip()) for line in lines]
        translations = [" / ".join(json.loads(line)["translations"]) for line in lines]

    print('Adding translations to ELAN file...')
    for (tier, sentence_start, sentence_end), translation in zip(sentence_to_translate.keys(), translations):
        eaf.remove_annotation(tier, sentence_start, sentence_end)
        print(f"{tier} {sentence_start} {sentence_end} {translation}")
        eaf.add_annotation(tier, sentence_start, sentence_end, translation)

    eaf.to_file(args.elan)

    print('Cleaning up...')
    os.unlink(temp_input_file.name)
    os.unlink(temp_output_file.name)


if __name__ == '__main__':
    main()
