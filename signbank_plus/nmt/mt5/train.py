import argparse
import os
from pathlib import Path

from datasets import load_dataset, Features, Value
from tqdm import tqdm

from transformers import TFMT5ForConditionalGeneration, MT5Tokenizer, DataCollatorForSeq2Seq

import tensorflow as tf
from tensorflow.keras.optimizers import Adam

tokenizer = MT5Tokenizer.from_pretrained("google/mt5-small")
model = TFMT5ForConditionalGeneration.from_pretrained("google/mt5-small")


def preprocess_function(examples):
    padding = "max_length"
    max_length = 512

    inputs = [str(ex) for ex in examples["source"]]
    targets = [str(ex) for ex in examples["target"]]
    model_inputs = tokenizer(inputs, max_length=max_length, padding=padding, truncation=True)
    model_targets = tokenizer(targets, max_length=max_length, padding=padding, truncation=True)

    model_inputs["labels"] = model_targets["input_ids"]
    return model_inputs


def get_dataset(csv_path: str):
    # na_values is a set of strings that should be recognized as NA/NaN.
    dataset = load_dataset("csv", data_files=csv_path, na_values=set())
    dataset = dataset["train"].shuffle(seed=42)

    train_dataset = dataset.map(preprocess_function, batched=True, desc="Running tokenizer")

    data_collator = DataCollatorForSeq2Seq(
        tokenizer,
        model=model,
        label_pad_token_id=tokenizer.pad_token_id,
        pad_to_multiple_of=64,
        return_tensors="np",
    )
    return model.prepare_tf_dataset(
        train_dataset,
        collate_fn=data_collator,
        batch_size=8,
        shuffle=True,
    )


def fit_model(train_dataset, validation_dataset, checkpoints_dir: Path):
    # Model training
    model.compile(optimizer=Adam(3e-5))
    callbacks = [
        tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=1),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=os.path.join(checkpoints_dir, "cp-{epoch:04d}.ckpt"),
            verbose=1,
            save_freq=10000)  # 10k batches
    ]

    existing_checkpoints = sorted(Path(checkpoints_dir).glob("*.ckpt"))
    if len(existing_checkpoints) > 0:
        last_checkpoint = existing_checkpoints[-1]
        print("Loading checkpoint", last_checkpoint)
        model.load_weights(last_checkpoint)

    model.fit(train_dataset,
              validation_data=validation_dataset,
              epochs=20, callbacks=callbacks)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-csv", type=str, required=True)
    parser.add_argument("--validation-csv", type=str, required=True)
    parser.add_argument("--checkpoints", type=str, required=True)
    args = parser.parse_args()

    train_dataset = get_dataset(args.train_csv)
    validation_dataset = get_dataset(args.train_csv)
    fit_model(train_dataset, validation_dataset, args.checkpoints)
