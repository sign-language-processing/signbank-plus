import csv
import itertools
import random
from collections import defaultdict
from pathlib import Path

from tqdm import tqdm

from load_data import load_data, load_file
from signwriting.signwriting_tokenizer import SignWritingTokenizer


def get_source_target(data, field="annotated_texts"):
    random.Random(42).shuffle(data)  # Shuffle data consistently
    for instance in data:
        if field in instance:
            for text in instance[field]:
                if len(text.strip()) > 0 and len(instance["sign_writing"].strip()) > 0:
                    yield {
                        "puddle_id": instance["puddle_id"],
                        "example_id": instance["example_id"],
                        "flags": [instance["spoken_language"], instance["sign_language"]],
                        "source": instance["sign_writing"].strip(),
                        "target": text.strip(),
                    }


def get_source_target_no_test(data, field="annotated_texts"):
    test_instances = load_data("benchmark")
    test_instances = {(instance['puddle_id'], instance['example_id']) for instance in test_instances}
    for instance in get_source_target(data, field):
        if (instance['puddle_id'], instance['example_id']) not in test_instances:
            yield instance


# Model 1: Original data
def get_original_data():
    data = load_data("raw")
    yield from get_source_target_no_test(data, field="texts")


# Model 2: Cleaned data
def get_cleaned_data():
    data = load_data("raw", "gpt-3.5-cleaned", "manually-cleaned", "bible")
    yield from get_source_target_no_test(data, field="annotated_texts")


# Model 3: Expanded data
def get_expanded_data():
    data = load_data("raw", "gpt-3.5-cleaned", "gpt-3.5-expanded", "manually-cleaned", "bible")
    yield from get_source_target_no_test(data, field="annotated_texts")


def get_expanded_data_en():
    data = load_data("gpt-3.5-expanded.en")
    yield from get_source_target_no_test(data, field="annotated_texts")


def test_set():
    data = load_file("benchmark", array_fields=["gold_texts"])
    yield from get_source_target(data, field="gold_texts")


def save_parallel_csv(path: Path, data: iter, split="train"):
    f_source = open(f"{path}.{split}.source", "w", encoding="utf-8")
    f_source_tokenized = open(f"{path}.{split}.source.tokenized", "w", encoding="utf-8")
    f_target = open(f"{path}.{split}.target", "w", encoding="utf-8")
    f_csv = open(f"{path}.{split}.csv", "w", encoding="utf-8")

    tokenizer = SignWritingTokenizer()

    writer = csv.DictWriter(f_csv, fieldnames=["source", "target"])
    writer.writeheader()
    for instance in tqdm(data):
        if 0 < len(instance["target"]) < 512 and 0 < len(instance["source"]) < 1024:
            flags = [f"${flag}" for flag in instance["flags"]]
            source = " ".join(flags) + " " + instance["source"]
            writer.writerow({
                "source": source,
                "target": instance["target"],
            })
            f_source.write(source + "\n")
            f_target.write(instance["target"] + "\n")

            tokenized_source = " ".join(tokenizer.text_to_tokens(instance["source"]))
            tokenized_source = " ".join(flags) + " " + tokenized_source
            f_source_tokenized.write(tokenized_source + "\n")

    f_source.close()
    f_target.close()
    f_csv.close()


def save_splits(path: Path, data: iter):
    save_parallel_csv(path, itertools.islice(data, 3000), split="dev")
    save_parallel_csv(path, data, split="train")


def save_test(path: Path, data: iter):
    save_parallel_csv(path, data, split="all")

    # Read source file and target file
    with open(f"{path}.all.source", 'r') as f:
        source_lines = [l.strip() for l in f.readlines()]
    with open(f"{path}.all.source.tokenized", 'r') as f:
        source_lines_tokenized = [l.strip() for l in f.readlines()]
    with open(f"{path}.all.target", 'r') as f:
        target_lines = [l.strip() for l in f.readlines()]

    source_map = {source_tokenized: source for source_tokenized, source in zip(source_lines_tokenized, source_lines)}

    source_target_map = defaultdict(list)
    for source, target in zip(source_lines_tokenized, target_lines):
        source_target_map[source].append(target)

    max_references = max(len(references) for references in source_target_map.values())
    print(f"Max test references: {max_references}")

    path.mkdir(parents=True, exist_ok=True)

    with open(f"{path}/test.source.unique", 'w') as f1:
        with open(f"{path}/test.source.unique.tokenized", 'w') as f2:
            for source, references in source_target_map.items():
                f1.write(source_map[source])
                f1.write("\n")
                f2.write(source)
                f2.write("\n")

    for i in range(max_references):
        with open(f"{path}/test.target.{i}", 'w') as f:
            for source, references in source_target_map.items():
                if len(references) > i:
                    f.write(references[i])
                f.write("\n")


if __name__ == "__main__":
    parallel_path = Path(__file__).parent.parent / "data" / "parallel"

    save_test(parallel_path / "test", test_set())

    save_splits(parallel_path / "original", get_original_data())
    save_splits(parallel_path / "cleaned", get_cleaned_data())
    save_splits(parallel_path / "expanded", itertools.chain.from_iterable([
        get_expanded_data(),
        get_expanded_data_en()
    ]))
