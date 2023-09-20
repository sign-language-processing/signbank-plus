#!/bin/bash

#SBATCH --job-name=eval-fairseq
#SBATCH --time=0-1:00:00
#SBATCH --mem=16G
#SBATCH --output=eval.out

#SBATCH --ntasks=1
#SBATCH --gres gpu:1
#SBATCH --constraint=GPUMEM32GB

set -e # exit on error
set -x # echo commands

module load anaconda3
source activate fairseq

# There is an issue in fairseq, have to downgrade torch: https://github.com/facebookresearch/fairseq/issues/4899
pip install torch==1.12.1+cu113 torchvision==0.13.1+cu113 torchaudio==0.12.1 --extra-index-url https://download.pytorch.org/whl/cu113
pip install fairseq==0.12.2

[ ! -f $2/test.translations.out ] && \
fairseq-interactive $2/preprocessed \
    --path $2/checkpoints/checkpoint_best.pt \
    --source-lang source \
    --target-lang target \
    --buffer-size 128 \
    --batch-size 128 \
    --beam 5 \
    --input $1/test.source.unique.tokenized \
    > $2/test.translations.out

# Output includes more things, not only translation https://github.com/facebookresearch/fairseq/issues/771
cat $2/test.translations.out | grep -P '^H-' | sed 's/H-//' | cut -f3- > $2/test.translations.bpe

sed -re 's/(@@ |@@$)//g' < $2/test.translations.bpe > $2/test.translations

sacrebleu $(find $1 -type f -name "test.target*") -i $2/test.translations -m bleu chrf --width 2 > $2/sacrebleu.txt

#  sbatch eval.sh /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test /shares/volk.cl.uzh/amoryo/checkpoints/sockeye/original
#  sbatch eval.sh /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test /shares/volk.cl.uzh/amoryo/checkpoints/sockeye/cleaned

# TODO check if ppl is correct
# original 25.52035803169066 BLEU 0.2043 chrF2 9.8421
# cleaned 27.961570090855236 BLEU 28.1635 chrF2 27.3069

# wc -l /shares/volk.cl.uzh/amoryo/checkpoints/sockeye/original/test.translations