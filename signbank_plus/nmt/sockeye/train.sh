#!/bin/bash

#SBATCH --job-name=train-sockeye
#SBATCH --time=6-23:00:00
#SBATCH --mem=16G
#SBATCH --output=train.out

#SBATCH --ntasks=1
#SBATCH --gres gpu:1
#SBATCH --constraint=GPUMEM32GB|GPUMEM80GB

set -e # exit on error
set -x # echo commands

module load anaconda3
source activate sockeye

mkdir -p $2

# Initialize variables
optional_prepare_data_args=""
optional_training_args=""

# If $3 is not empty, use it as bpe dictionary directory
if [ -n "$3" ]; then
  cp $3/bpe.codes.target $2/bpe.codes.target
  optional_prepare_data_args="--source-vocab $3/train_data/vocab.src.0.json --target-vocab $3/train_data/vocab.trg.0.json"
  optional_training_args="--params $3/model/params.best"
fi

# Perform BPE
pip install subword-nmt
## Source BPE
#[ ! -f $2/bpe.codes.source ] && subword-nmt learn-bpe -s 3000 < $1.train.source > $2/bpe.codes.source
#[ ! -f $2/source.bpe ] && subword-nmt apply-bpe -c $2/bpe.codes.source < $1.train.source > $2/source.bpe
# Target BPE
[ ! -f $2/bpe.codes.target ] && subword-nmt learn-bpe -s 3000 < $1.train.target > $2/bpe.codes.target
[ ! -f $2/train.target.bpe ] && subword-nmt apply-bpe -c $2/bpe.codes.target < $1.train.target > $2/train.target.bpe
[ ! -f $2/dev.target.bpe ] && subword-nmt apply-bpe -c $2/bpe.codes.target < $1.dev.target > $2/dev.target.bpe

# Clone sockeye if doesn't exist
[ ! -d sockeye ] && git clone https://github.com/awslabs/sockeye.git
cd sockeye

pip install -r requirements/requirements.txt

# Prepare data
#python -m sockeye.prepare_data --max-seq-len 512 -s $2/source.bpe -t $2/target.bpe -o $2/train_data
[ ! -d $2/train_data ] && \
python -m sockeye.prepare_data --max-seq-len 512:128 \
                               -s $1.train.source.tokenized \
                               -t $2/train.target.bpe \
                               -o $2/train_data \
                               $optional_prepare_data_args


# batch size refers to number of target tokens, 768 sometimes does not fit in 32GB GPU memory
python -m sockeye.train -d $2/train_data \
                        --weight-tying-type none \
                        --batch-size 512 \
                        --max-seq-len 512:128 \
                        --decode-and-evaluate 500 \
                        --validation-source $1.dev.source.tokenized \
                        --validation-target $2/dev.target.bpe \
                        --optimized-metric chrf \
                        --max-num-checkpoint-not-improved 10 \
                        --output $2/model \
                        $optional_training_args

# conda activate
# cd sign-language/signbank-annotation/signbank-plus/signbank_plus/nmt/sockeye/
# ./train.sh /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/original /shares/volk.cl.uzh/amoryo/checkpoints/sockeye/original
#  watch tail train.out

# srun --pty -n 1 -c 2 --time=01:00:00 --gres=gpu:1 --constraint=GPUMEM32GB --mem=8G bash -l
# srun --pty -n 1 -c 2 --time=01:00:00 --mem=8G bash -l
# python -c "import torch; print([(i, torch.cuda.get_device_properties(i)) for i in range(torch.cuda.device_count())])"
# python -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"

#  Best validation chrf: 19.155629
#  sbatch train.sh /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/original /shares/volk.cl.uzh/amoryo/checkpoints/sockeye/original
#  Best validation chrf: 28.054069
#  sbatch train.sh /home/amoryo/sign-language/signbank-annotation/signbank-plus/data/parallel/cleaned /shares/volk.cl.uzh/amoryo/checkpoints/sockeye/cleaned