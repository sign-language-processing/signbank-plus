#!/bin/bash

#SBATCH --job-name=train-opennmt
#SBATCH --time=6-23:00:00
#SBATCH --mem=16G
#SBATCH --output=train.out

#SBATCH --ntasks=1
#SBATCH --gres gpu:1
#SBATCH --constraint=GPUMEM32GB|GPUMEM80GB

set -e # exit on error
set -x # echo commands

module load anaconda3
source activate opennmt

mkdir -p $2
mkdir -p $2/data
mkdir -p $2/model


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


pip install OpenNMT-py==1.2.0

[ ! -f $2/processed.vocab.pt ] && onmt_preprocess \
  --save_data $2/processed \
  --shard_size 2000000 \
  --train_src $2/data/train.source --train_tgt $2/data/train.target \
  --valid_src $2/data/dev.source --valid_tgt $2/data/dev.target \
  --src_seq_length 512 \
  --tgt_seq_length 512 \
  --log_file_level DEBUG

onmt_train --data $2/processed --save_model $2/model/checkpoint --layers 2 --rnn_size 512 --word_vec_size 512 --heads 8 \
  --encoder_type transformer --decoder_type transformer --position_encoding --transformer_ff 2048 --dropout 0.1 \
  --early_stopping 10 --early_stopping_criteria accuracy ppl --batch_size 2048 --accum_count 3 --batch_type tokens \
  --max_generator_batches 2 --normalization tokens --optim adam --adam_beta2 0.998 --decay_method noam \
  --warmup_steps 3000 --learning_rate 0.5 --max_grad_norm 0 --param_init 0 --param_init_glorot --label_smoothing 0.1 \
  --valid_steps 500 --save_checkpoint_steps 500 --world_size 1 --gpu_ranks 0


