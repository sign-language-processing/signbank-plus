#!/bin/bash

#SBATCH --job-name=eval-mt5
#SBATCH --time=0-4:00:00
#SBATCH --mem=32G
#SBATCH --output=eval.out
#SBATCH --cpus-per-task=4
#SBATCH --ntasks=1
#SBATCH --gres gpu:1
#SBATCH --constraint=GPUMEM32GB|GPUMEM80GB

set -e # exit on error

module load anaconda3
source activate huggingface-mt5

mkdir -p $2

[ ! -f $2/test.translations ] && srun python3 inference.py \
                        --test-source $1/test.source.unique \
                        --test-target $2/test.translations \
                        --checkpoints $2


sacrebleu $(find $1 -type f -name "test.target*") -i $2/test.translations -m bleu chrf --width 2 > $2/sacrebleu.txt

#  sbatch eval.sh /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test /shares/volk.cl.uzh/amoryo/checkpoints/mt5/original
# ./eval.sh /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/test /shares/volk.cl.uzh/amoryo/checkpoints/mt5/original

# srun --pty --jobid 4633268 bash
# srun --pty --jobid 4633268 htop -u amoryo


