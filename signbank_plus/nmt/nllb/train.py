import argparse
from datasets import load_dataset
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, DataCollatorForSeq2Seq, Seq2SeqTrainingArguments, \
    Seq2SeqTrainer
from torch.utils.data import Dataset

# Load model and tokenizer
model_name = "facebook/nllb-200-1.3B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name)


# Custom Dataset
class TranslationDataset(Dataset):
    def __init__(self, tokenizer, file_path, max_length=512):
        self.dataset = load_dataset("csv", data_files=file_path)["train"]
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.dataset)

    def __getitem__(self, idx):
        source_text = self.dataset[idx]["source"]
        target_text = self.dataset[idx]["target"]
        if source_text == "" or source_text is None:
            source_text = "."
        if target_text == "" or target_text is None:
            target_text = "."

        source_encoding = tokenizer(text=source_text,
                                    return_tensors="pt",
                                    max_length=self.max_length,
                                    padding="max_length",
                                    truncation=True)
        target_encoding = tokenizer(text=target_text,
                                    return_tensors="pt",
                                    max_length=self.max_length,
                                    padding="max_length",
                                    truncation=True)

        labels = target_encoding.input_ids
        labels[labels == tokenizer.pad_token_id] = -100

        return {
            "input_ids": source_encoding.input_ids.flatten(),
            "attention_mask": source_encoding.attention_mask.flatten(),
            "labels": labels.flatten()
        }


def main(train_file, validation_file, output_dir):
    train_dataset = TranslationDataset(tokenizer, train_file)
    validation_dataset = TranslationDataset(tokenizer, validation_file)

    training_args = Seq2SeqTrainingArguments(
        output_dir=output_dir,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        predict_with_generate=True,
        evaluation_strategy="steps",
        eval_steps=500,
        save_total_limit=3,
        num_train_epochs=3,
        logging_steps=100,
        learning_rate=3e-5,
        load_best_model_at_end=True,
    )

    data_collator = DataCollatorForSeq2Seq(tokenizer, model=model)

    trainer = Seq2SeqTrainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=validation_dataset,
        tokenizer=tokenizer,
        data_collator=data_collator,
    )

    trainer.train()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--train-file", type=str, required=True)
    parser.add_argument("--validation-file", type=str, required=True)
    parser.add_argument("--output-dir", type=str, required=True)
    args = parser.parse_args()

    main(args.train_file, args.validation_file, args.output_dir)
