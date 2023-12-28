FROM nvidia/cuda:11.5.2-devel-ubuntu18.04

RUN apt-get update; apt-get update
# git is needed for cloning the repository
# nano is needed for debugging files
# curl is needed for "download_mono" in the `make test` script
RUN apt-get install git nano curl -y

RUN git clone https://github.com/sign-language-processing/firefox-translations-training.git
WORKDIR firefox-translations-training

RUN chmod +x pipeline/setup/install-deps.sh
RUN ./pipeline/setup/install-deps.sh

RUN make conda
RUN make snakemake
RUN make git-modules
RUN make dry-run

# Marian/NCCL is expecting nvcc in specific location
RUN if [ ! -f "/usr/local/cuda/bin/nvcc" ]; then  mkdir /usr/local/cuda/bin/ && ln -s /usr/bin/nvcc /usr/local/cuda/bin/nvcc; fi
# NCCL: unsupported GNU version! gcc versions later than 6 are not supported!
RUN apt-get install gcc-6 g++-6 -y
RUN update-alternatives --install /usr/bin/gcc gcc /usr/bin/gcc-6 60 --slave /usr/bin/g++ g++ /usr/bin/g++-6

# For building purposes, we assume the user has 4 gpus, not 8
RUN sed -i 's/^resources:\ gpu=8/resources:\ gpu=4/' profiles/local/config.yaml
RUN sed -i 's/numgpus=8/numgpus=4/' profiles/local/config.yaml
RUN sed -i 's/workspace=12000/workspace=4000/' profiles/local/config.yaml

# disable the Shared Memory (SHM) transports if not shm is available, to prevent multi-gpu issues.
#ENV NCCL_SHM_DISABLE=1

# Downloads and compiles additional packages. It is good to install the dependencies in advance.
RUN make test TARGET=train_vocab; exit 0