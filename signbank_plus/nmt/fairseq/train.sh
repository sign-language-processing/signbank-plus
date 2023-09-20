#!/bin/bash

#SBATCH --job-name=train-fairseq
#SBATCH --time=6-23:00:00
#SBATCH --mem=16G
#SBATCH --output=train.out

#SBATCH --ntasks=1
#SBATCH --gres gpu:1
#SBATCH --constraint=GPUMEM32GB|GPUMEM80GB

set -e # exit on error
set -x # echo commands

module load anaconda3
source activate fairseq

mkdir -p $2
mkdir -p $2/data


# If $3 is not empty, use it as bpe dictionary directory
if [ -n "$3" ]; then
  cp $3/bpe.codes.target $2/bpe.codes.target
fi

# Perform BPE
pip install subword-nmt
# Target BPE
[ ! -f $2/bpe.codes.target ] && subword-nmt learn-bpe -s 3000 < $1.train.target > $2/bpe.codes.target
[ ! -f $2/data/train.target ] && subword-nmt apply-bpe -c $2/bpe.codes.target < $1.train.target > $2/data/train.target
[ ! -f $2/data/dev.target ] && subword-nmt apply-bpe -c $2/bpe.codes.target < $1.dev.target > $2/data/dev.target
# Copy source
[ ! -f $2/data/train.source ] && cp $1.train.source.tokenized $2/data/train.source
[ ! -f $2/data/dev.source ] && cp $1.dev.source.tokenized $2/data/dev.source

# Install fairseq
pip install fairseq

# Prepare data
#python -m sockeye.prepare_data --max-seq-len 512 -s $2/source.bpe -t $2/target.bpe -o $2/train_data
[ ! -d $2/preprocessed ] && fairseq-preprocess --source-lang source --target-lang target \
    --trainpref $2/data/train --validpref $2/data/dev \
    --destdir $2/preprocessed


# Train
mkdir -p $2/checkpoints

fairseq-train $2/preprocessed \
  --source-lang source --target-lang target \
  --save-dir $2/checkpoints \
  --arch transformer_tiny \
  --optimizer adam --adam-betas '(0.9, 0.98)' --clip-norm 0.0 \
  --lr 5e-4 --lr-scheduler inverse_sqrt --warmup-updates 4000 \
  --dropout 0.3 --weight-decay 0.0001 \
  --criterion label_smoothed_cross_entropy --label-smoothing 0.1 \
  --max-tokens 8192 \
  --update-freq 2 \
  --max-epoch 200 \
  --patience 10 \
  --eval-bleu \
  --eval-bleu-args '{"beam": 5}' \
  --eval-bleu-remove-bpe \
  --eval-bleu-print-samples \
  --best-checkpoint-metric bleu --maximize-best-checkpoint-metric

