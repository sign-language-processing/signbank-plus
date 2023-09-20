import argparse
from itertools import islice
from pathlib import Path
from typing import List

from tqdm import tqdm
from transformers import TFMT5ForConditionalGeneration, MT5Tokenizer, DataCollatorForSeq2Seq


def translate_single(sentence: str, model, tokenizer):
    print("Translating", sentence)
    tokenized_input = tokenizer(sentence, return_tensors="tf").input_ids
    out = model.generate(
        input_ids=tokenized_input,
        max_length=100,
        num_beams=5,
        num_return_sequences=1,
        no_repeat_ngram_size=3,
        repetition_penalty=2.5,
        remove_invalid_values=True,
    )
    return tokenizer.decode(out[0], skip_special_tokens=True)


def load_model(checkpoints: str):
    print("Loading mode...")
    tokenizer = MT5Tokenizer.from_pretrained("google/mt5-small")
    model = TFMT5ForConditionalGeneration.from_pretrained("google/mt5-small")
    last_checkpoint = sorted(Path(checkpoints).glob("*.ckpt"))[-1]
    print("Loading checkpoint", last_checkpoint)
    model.load_weights(last_checkpoint)
    return model, tokenizer


def get_sentences(file_path: str):
    with open(file_path, "r") as f:
        return [s.strip() for s in f.readlines()]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test-source", type=str, required=True)
    parser.add_argument("--test-target", type=str, required=True)
    parser.add_argument("--checkpoints", type=str, required=True)
    args = parser.parse_args()

    sentences = get_sentences(args.test_source)
    print("Loaded", len(sentences), "sentences")

    model, tokenizer = load_model(args.checkpoints)

    with open(args.test_target, "w") as f:
        for sentence in sentences:
            translation = translate_single(sentence, model, tokenizer)
            print("translation", translation)
            no_new_lines = translation.replace(r"\n", "\\\\n")
            f.write(no_new_lines + "\n")
