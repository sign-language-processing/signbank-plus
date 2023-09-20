import os
from pathlib import Path
import requests
from tqdm import tqdm
from signwriting.signwriting_tokenizer import SignWritingTokenizer


def get_translation(fsw, spoken_language, country_code):
    # url = "https://pub.cl.uzh.ch/demo/signwriting/sign2spoken"
    url = "http://172.23.144.112:3030/api/translate/sign2spoken"
    body = {
        "text": fsw,
        "n_best": 1,
        "country_code": country_code,
        "language_code": spoken_language,
    }
    response = requests.post(url, json=body)

    return response.json()["translations"][0]


def main():
    tokenizer = SignWritingTokenizer()

    test_path = Path(__file__).parent.parent / "data" / "parallel" / "test" / "test.source.unique.country"
    with open(test_path, "r") as f:
        test_lines = [l.strip() for l in f.readlines()]

    pred_path = Path(__file__).parent.parent / "data" / "parallel" / "test" / "test.jiang_etal_2023.pred"
    # check how many lines done
    if os.path.exists(pred_path):
        with open(pred_path, "r") as f:
            pred_lines = [l.strip() for l in f.readlines()]
        print(f"Already done: {len(pred_lines)}")
        test_lines = test_lines[len(pred_lines):]

    with open(pred_path, "a") as f:
        for line in tqdm(test_lines):
            spoken_language, country_code, *signs = line.split(" ")
            spoken_language = spoken_language[1:]
            country_code = country_code[1:]
            # tokenizer removes "A" prefix
            fsw = tokenizer.tokens_to_text(tokenizer.text_to_tokens(" ".join(signs)))
            print(spoken_language, country_code, fsw, '->', end=' ')

            # make request to get translation
            translation = get_translation(fsw, spoken_language, country_code)
            print(translation)
            f.write(translation)
            f.write("\n")


if __name__ == "__main__":
    main()
    # sacrebleu $(find data/parallel/test/ -type f -name "test.target*") -i data/parallel/test/test.jiang_etal_2023.pred -m bleu chrf --width 2
