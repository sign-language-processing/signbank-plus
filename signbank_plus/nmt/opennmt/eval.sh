#!/bin/bash

#SBATCH --job-name=eval-opennmt
#SBATCH --time=0-1:00:00
#SBATCH --mem=16G
#SBATCH --output=eval.out

#SBATCH --ntasks=1
#SBATCH --gres gpu:1
#SBATCH --constraint=GPUMEM32GB

set -e # exit on error
set -x # echo commands

module load anaconda3
source activate opennmt

# best model is 10 validations before the last one
best_model=$(ls $2/model/ | awk -F'_' '{ print $3 " " $0 }' | sort -k1,1n | awk '{ print $2 }' | tail -n 11 | head -n 1)

[ ! -f $2/test.translations.bpe ] &&
onmt_translate --model $2/model/$best_model \
  --src $1/test.source.unique.tokenized \
  --output $2/test.translations.bpe \
  --gpu 0 --replace_unk --beam_size 5

sed -re 's/(@@ |@@$)//g' < $2/test.translations.bpe > $2/test.translations

sacrebleu $(find $1 -type f -name "test.target*") -i $2/test.translations -m bleu chrf --width 2 > $2/sacrebleu.txt