# Bergamot

This NMT implementation is targeting production use, and is based on the [Bergamot](https://browser.mt/) project.

Therefore, data is prepared differently than in our other NMT implementations.

## Tokenization

### Signed Languages

SignWriting is tokenized using our SignWriting tokenizer. For example:

```
M526x565S30004482x483S20710484x522S15d52499x546
```

Becomes:

```
M p526 p565 S300 c0 r4 p482 p483 S207 c1 r0 p484 p522 S15d c5 r2 p499 p546
```

This tokenization saves about 60% of the tokens over character-level, and is already split to minimal units.

### Spoken Languages

Spoken language text is tokenized using a character-level tokenizer.
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
