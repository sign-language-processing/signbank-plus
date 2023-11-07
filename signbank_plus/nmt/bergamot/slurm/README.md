## Setup

This does not yet work.

```bash
# Clone the repository
[ ! -d firefox-translations-training ] && git clone https://github.com/sign-language-processing/firefox-translations-training.git
cd firefox-translations-training

# Install Snakemake
make snakemake
# Update git submodules
make git-modules
# (Optional) Install Singularity if running with containerization
module load singularityce
# (Optional) Prepare a container image if using Singularity (Either pull the prebuilt image)
make pull
```

In `firefox-translations-training/profiles/slurm-s3it/config.yaml`, you might need to change paths in `config`.

To test the setup, train the test config:

```bash
# Get a machine with a GPU
srun --pty -n 1 -c 2 --time=01:00:00 --gres=gpu:1 --mem=8G bash -l
cd /home/amoryo/sign-language/signbank-annotation/signbank-plus/signbank_plus/nmt/bergamot/firefox-translations-training

# Load modules
module load singularityce
module load gpu
module load cuda/11.8.0

# Run the test config
make run PROFILE=slurm-s3it CONFIG=configs/config.test.yml
```
