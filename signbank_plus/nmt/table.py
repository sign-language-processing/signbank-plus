import json
import os

CHECKPONTS_DIR = "/shares/volk.cl.uzh/amoryo/checkpoints/"
DATA_DIR = "/home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/"

frameworks = ["sockeye", "fairseq", "opennmt", "mt5"]
variants = ["original", "cleaned", "expanded"]

for variant in variants:
    print(variant.capitalize(), end=" & ")

    num_samples = 0
    for split in ["train", "dev"]:
        with open(os.path.join(DATA_DIR, f"{variant}.{split}.csv"), 'r') as f:
            num_samples += len(f.readlines())
    print(f"${num_samples:,}$ & ", end="")

    with open(os.path.join(CHECKPONTS_DIR, "sockeye", variant, "train_data", "vocab.trg.0.json"), 'r') as f:
        vocabulary_size = len(json.load(f))
    print(f"${vocabulary_size:,}$ ", end="")

    for framework in frameworks:
        file_path = os.path.join(CHECKPONTS_DIR, framework, variant, "sacrebleu.txt")

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                scores_data = json.load(f)
            print("& " + " & ".join([f"${score['score']}$" for score in scores_data]), end=" ")
        else:
            print("& \\fix{@@} & \\fix{@@} ", end="")
    print(" \\\\")