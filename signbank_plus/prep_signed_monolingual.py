import csv
import gzip
from collections import Counter
from pathlib import Path

from tqdm import tqdm
from signwriting.tokenizer import normalize_signwriting


def save_mono_single_signs(path: Path):
    # Saves single signs, in any language
    path.mkdir(parents=True, exist_ok=True)

    flags_counter = Counter()

    all_signs = set()
    original_signs = set()

    data_path = Path(__file__).parent.parent / "data"
    for file in tqdm(list(data_path.glob("*.csv"))):
        if file.stem == "fingerspelling":
            continue

        print(file.stem)

        csv.field_size_limit(2 ** 20)  # Increase limit to 1MB (2^20 characters)
        with open(file, 'r', encoding="utf-8") as f:
            data = csv.DictReader(f)
            for row in data:
                if "spoken_language" not in row or "sign_language" not in row or "sign_writing" not in row:
                    break
                flag = f"${row['spoken_language']} ${row['sign_language']}"
                flags_counter[flag] += 1

                single_signs = normalize_signwriting(row["sign_writing"]).split(" ")
                for sign in single_signs:
                    all_signs.add(sign)
                    original_signs.add(f"{flag} {sign}")


    f_gzip = gzip.open(path.joinpath(f'mono.signed.gz'), 'wt')

    # Add signs and their original flags
    for sign in tqdm(original_signs, unit="write"):
        f_gzip.write(f"{sign}\n")

    # Add all signs for the highest resource languages
    most_common_flags = [lang_code for lang_code, _ in flags_counter.most_common(5)]
    for flag in tqdm(most_common_flags, unit="language pair"):
        for sign in all_signs:
            flagged_sign = f"{flag} {sign}"
            if flagged_sign not in original_signs:
                f_gzip.write(f"{flagged_sign}\n")
    f_gzip.close()


if __name__ == "__main__":
    mono_path = Path(__file__).parent.parent / "data" / "mono"
    save_mono_single_signs(mono_path / "signs")
