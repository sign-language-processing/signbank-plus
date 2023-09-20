# SignBank+ - Cleaning and Extending the SignBank Dataset

[Paper (Coming Soon)]()

The [SignBank](https://www.signbank.org/signpuddle/) dataset is a collection of SignWriting examples, contributed by the community.
It is a great resource for SignWriting, but it is not immediately fit for machine translation.
It includes SignWriting entries with text that is not parallel, or multiple terms where only some of them are parallel.
For example, it includes a chapter and page number for a book, but not the text, or a word and its definition.

## Data

### Files

This repository includes the `data` directory, which includes:

- [`raw.csv`](data/raw.csv) - The raw SignBank dataset (until June 2023).
- [`manually-cleaned.csv`](data/manually-cleaned.csv) - A manually cleaned subset of the raw dataset.
- [`bible.csv`](data/bible.csv) - Automatically aligned data from the Bible for puddles 151 and 152.
- [`gpt-3.5-cleaned.csv`](data/gpt-3.5-cleaned.csv) - A cleaned subset of the raw dataset, using GPT-3.5 Turbo (June 13).
- [`gpt-3.5-expanded.csv`](data/gpt-3.5-expanded.csv) - Expansion of the cleaned dataset, filtered to the source language.
- [`gpt-3.5-expanded.en.csv`](data/gpt-3.5-expanded.csv) - Expansion of the cleaned dataset, with English terms.
- [`benchmark.csv`](data/benchmark.csv) - Small subset of data manually annotated and automatically cleaned in various ways.

### Notes:

- To separate between terms, we use the `᛫` (`U+16EB`) character.
- `\n` characters are escaped as `\\n`.

## Machine Translation
Using the [signbank_plus/prep_nmt.py](signbank_plus/prep_nmt.py) script, we can prepare the data for 
machine translation training, in the [data/parallel](data/parallel) directory.

The [signbank_plus/nmt](signbank_plus/nmt) directory includes scripts for training and evaluating 
machine translation systems, like [Fairseq](signbank_plus/nmt/fairseq),
[Sockeye](signbank_plus/nmt/sockeye), [OpenNMT](signbank_plus/nmt/opennmt), and [mT5](signbank_plus/nmt/mt5).

## Benchmarking Cleaning

Using the [`benchmark.csv`](data/benchmark.csv) file, 
we benchmark with [signbank_plus/score_benchmark.py](signbank_plus/score_benchmark.py),
to get a measure of how good various automatically cleaning methods are.

The results at the moment are:

| Method                            |IoU|Average Tokens|
|-----------------------------------|---|---|
| E0: texts                         |0.497|0.0|
| E1: pred_rules                    |0.533|0.0|
| E2: pred_general                  |0.627|541.4|
| E3: pred_specific_5               |0.712|521.4|
| E4: pred_general_specific_5       |0.735|714.6|
| E5: pred_general_specific_5_gpt_4 |0.801|713.2|

GPT-4 is better than GPT-3.5 Turbo, but is also much more expensive.

There are possible improvements to the cleaning, such as using a better model, or better prompt.