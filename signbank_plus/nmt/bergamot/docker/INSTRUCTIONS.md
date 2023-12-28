# Building the image:

- run `nvidia-smi`
  - edit `Dockerfile`:
      - change "FROM" according to your CUDA version (must be ubuntu18.04)
      - change "gpu=4" and "numgpus=4" according to your GPU count
  - edit `profile.yaml`:
      - change "gpu=4" and "numgpus=4" according to your GPU count
- build the image:
    - run `nvidia-docker build . -t bergamot`
    - or `nvidia-docker build . --no-cache -t bergamot`

cd /home/nlp/amit/sign-language/signbank-annotation/signbank-plus/signbank_plus/nmt/bergamot/docker && nvidia-docker build . --no-cache -t bergamot

# Running the image:

Edit `config.spoken-to-signed.yml` to point to the datasets you want to use, then:

```bash
# Create a directory `bergamot_models` where the training data will be stored.
ROOT_DIR="/home/nlp/amit/bergamot_models"
mkdir -p $ROOT_DIR

# Point to the data directory
DATA_DIR="/home/nlp/amit/sign-language/signbank-annotation/signbank-plus/data"

# Run the image, 
# mounting the data and training directories, 
# and copying the config file
# shm-size is needed for multi-gpu training (otherwise, set --env NCCL_SHM_DISABLE=1)
nvidia-docker run -it  \
    --shm-size=12gb \
    --gpus '"device=1,2,3"' \
	--mount type=bind,source="$(pwd)/config.spoken-to-signed.yml",target=/firefox-translations-training/configs/config.spoken-to-signed.yml \
	--mount type=bind,source="$(pwd)/profile.yaml",target=/firefox-translations-training/profiles/local/config.yaml \
	--mount type=bind,source="$DATA_DIR",target=/corpora \
	--mount type=bind,source="$ROOT_DIR",target=/data \
	--publish 6006:6006 \
	bergamot
```

Once in the container, you can test it by using the test script (should take a few hours to a day)

```bash
make test
```

To run the pipeline on your own data, specify paths to config files

```bash
make run CONFIG=configs/config.spoken-to-signed.yml
```

To view for example the validation results for the first experiment, run

```bash
cat ~/bergamot_models/models/spoken-signed/spoken_to_signed/teacher-base0/valid.log  | grep 'chrf'
watch "cat ~/bergamot_models/models/spoken-signed/spoken_to_signed_bpe3/teacher-base0/valid.log  | grep 'chrf'"
```

To view training logs using tensorboard, run

```bash
make tensorboard
```


To reset the training for all experiments, just delete the training directory from within the container

```bash
rm -r /data/*
```


# Notes!

## GPUs

Updating from 1 to 4 2080Ti GPUs increases throughput from `26,318.99 words/s` to `44,707.07 words/s`.