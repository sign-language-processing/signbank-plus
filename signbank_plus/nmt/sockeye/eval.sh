#!/bin/bash

#SBATCH --job-name=eval-sockeye
#SBATCH --time=0-0:30:00
#SBATCH --mem=16G
#SBATCH --output=eval.out

#SBATCH --ntasks=1
#SBATCH --gres gpu:1
#SBATCH --constraint=GPUMEM32GB|GPUMEM80GB

set -e # exit on error

#module load anaconda3
#source activate sockeye

cd sockeye

[ ! -f $2/test.translations.bpe ] && python3 -m sockeye.translate -m $2/model \
                        --input $1/test.source.unique.tokenized \
                        --output $2/test.translations.bpe

sed -re 's/(@@ |@@$)//g' < $2/test.translations.bpe > $2/test.translations

sacrebleu $(find $1 -type f -name "test.target*") -i $2/test.translations -m bleu chrf --width 2 > $2/sacrebleu.txt
