#!/bin/bash

#SBATCH --job-name=bergamot
#SBATCH --time=168:00:00
#SBATCH --cpus-per-task=4
#SBATCH --ntasks=1
#SBATCH --mem=16G
#SBATCH --output=job.out

set -e # exit on error
set -x # echo commands

#mkdir -p /data/amoryo/bergamot
#cd /data/amoryo/bergamot

[ ! -d firefox-translations-training ] && git clone https://github.com/sign-language-processing/firefox-translations-training.git
cd firefox-translations-training

# Install Mamba - fast Conda package manager
make conda
conda install -n base -c conda-forge mamba -y

# Install Snakemake
make snakemake
# Update git submodules
make git-modules

# Check that everything works
#make dry-run

# (Optional) Install Singularity if running with containerization
module load singularityce

# (Optional) Prepare a container image if using Singularity (Either pull the prebuilt image)
make pull

# srun --pty -n 1 -c 4 --time=10:00:00 --mem=8G bash -l
