#!/bin/bash

#SBATCH --job-name=train-nllb
#SBATCH --time=168:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=128G
#SBATCH --output=nllb-job.out

#SBATCH --ntasks=1
#SBATCH --gres gpu:1
#SBATCH --constraint=GPUMEM80GB

set -e # exit on error
set -x # echo commands

module load gpu
module load cuda

module load anaconda3
source activate huggingface-nllb

# Install Huggingface
pip install transformers datasets

# Verify GPU with PyTorch
python3 -c "import torch; print(torch.cuda.is_available())"

python train.py --train-file="$1/train.csv" --validation-file="$1/dev.csv" --output-dir=$2
#  sbatch train.sh /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/original /shares/volk.cl.uzh/amoryo/checkpoints/nllb/original

# srun --pty -n 1 -c 2 --time=01:00:00 --gres=gpu:1 --constraint=GPUMEM80GB --mem=128G bash -l
# cd /home/amoryo/sign-language/signbank-annotation/signbank-plus/signbank_plus/nmt/nllb