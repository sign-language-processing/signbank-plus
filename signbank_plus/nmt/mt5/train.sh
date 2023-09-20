#!/bin/bash

#SBATCH --job-name=train-mt5
#SBATCH --time=168:00:00
#SBATCH --cpus-per-task=8
#SBATCH --mem=64G   # 16G ends with "killed" https://github.com/tensorflow/models/issues/3497
#SBATCH --output=job-expanded.out

#SBATCH --ntasks=1
#SBATCH --gres gpu:1
#SBATCH --constraint=GPUMEM80GB

set -e # exit on error
set -x # echo commands

module load gpu
module load cuda

module load anaconda3
source activate huggingface-mt5

# Install Huggingface
pip install transformers datasets sentencepiece tqdm

# Install Tensorflow
conda install -c conda-forge cudatoolkit=11.8.0 -y
pip install nvidia-cudnn-cu11==8.6.0.163 tensorflow==2.13.*
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
echo 'CUDNN_PATH=$(dirname $(python -c "import nvidia.cudnn;print(nvidia.cudnn.__file__)"))' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
echo 'export LD_LIBRARY_PATH=$CUDNN_PATH/lib:$CONDA_PREFIX/lib/:$LD_LIBRARY_PATH' >> $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
source $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
# Verify install:
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

python train.py --train-csv="$1.train.csv" --validation-csv="$1.dev.csv" --checkpoints=$2

#  sbatch train.sh /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/original /shares/volk.cl.uzh/amoryo/checkpoints/mt5/original
