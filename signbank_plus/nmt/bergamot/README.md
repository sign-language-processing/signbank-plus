# Bergamot

This NMT implementation is targeting production use, and is based on the [Bergamot](https://browser.mt/) project.

Therefore, data is prepared differently than in our other NMT implementations.

## Data

Upload the data to the server
```bash
rsync -avz --progress data/ nlp:/home/nlp/amit/sign-language/signbank-annotation/signbank-plus/data/
```

## Tokenization

### Spoken Languages

Currently spoken languages are tokenized using a BPE tokenizer.

Spoken language text might need to be tokenized using a character-level tokenizer.
This is due to having fingerspelling in the data, which is otherwise not split into minimal units.
This approach might not be ideal for longer texts, but BPE or other approaches may hurt fingerspelling, and
morphologically rich languages.

## Data

Both the source and the target are flagged with special control tokens.
This is due to bergamot also training reverse models in its pipeline.
All flags begin with a $ sign.

The flags are:

- spoken language ISO code (e.g. `$en`)
- signed language ISO code (e.g. `$ase`)
- `$extra` is added to all automatically generated data that is out-of-distribution

Fingerspelling data (`fingerspelling.csv`):

- Using `faker`, we generate names, addresses, emails, and numbers for every language.
- fixed phrases like "My name is ____" are added when available.


Our dev set is `benchmark.csv`

### For training:

- **cleaned**: we use `gpt-3.5-cleaned.csv`, `bible.csv` and `manually-cleaned.csv`. 
- **more**: we use `sign2mint.csv`, `signsuisse.csv` and `fingerspelling.csv`.
- **expanded**: we use `gpt-3.5-expanded.csv` and `gpt-3.5-expanded.en.csv` for extra data with the `$extra` flag.


## Model

We share a bergamot model trained on the above data, and using the above tokenization. in the `exported` directory.

```bash
# To download a local copy
scp -r "nlp:/home/nlp/amit/bergamot_models/models/spoken-signed/spoken_to_signed/exported" .
scp -r "nlp:/home/nlp/amit/bergamot_models/models/spoken-signed/spoken_to_signed_bpe4/exported" .

# Extract all .gz files to $EXPORTED_DIR/extracted
gunzip -r exported

# To upload a new model to production
gsutil -m cp -r exported/* gs://sign-mt-assets/models/browsermt/spoken-to-signed/spoken-signed
```