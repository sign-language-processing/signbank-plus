import argparse
import csv
import hashlib
from csv import DictReader

from multiprocessing import Pool
from pathlib import Path

from tqdm import tqdm

from signwriting.visualizer.visualize import signwriting_to_image


def process_fsw(args):
    fsw, output = args
    signwriting_to_image(fsw).save(output)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-path", type=str, required=True)
    parser.add_argument("--output-path", type=str, required=True)
    args = parser.parse_args()

    input_path = Path(args.input_path)
    output_path = Path(args.output_path)

    output_path.mkdir(parents=True, exist_ok=True)
    existing_files = set(output_path.glob('*.png'))
    print(f"Found {len(existing_files)} existing files.")

    with open(input_path, 'r', encoding="utf-8") as f:
        csv.field_size_limit(2 ** 20)  # Increase limit to 1MB (2^20 characters)
        reader = DictReader(f)
        unique_fsw = set(row["sign_writing"] for row in reader)

    missing = []
    for fsw in unique_fsw:
        fsw_md5 = hashlib.md5(fsw.encode('utf-8')).hexdigest()
        output_file = output_path / f"{fsw_md5}.png"
        if output_file not in existing_files:
            missing.append((fsw, str(output_file)))

    # Create images in parallel
    pool = Pool(40)
    for _ in tqdm(pool.imap_unordered(process_fsw, missing), total=len(missing)):
        pass
