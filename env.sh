# Copyright (c) 2023 Amphion.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

# Install ffmpeg in Linux
conda install -c conda-forge ffmpeg

# Pip packages
pip install setuptools ruamel.yaml tqdm colorama easydict tabulate loguru json5 Cython unidecode inflect argparse g2p_en tgt librosa matplotlib typeguard einops omegaconf hydra-core humanfriendly pandas

pip install tensorboard tensorboardX torch==2.0.1 torchaudio==2.0.2 torchvision==0.15.2 transformers diffusers accelerate praat-parselmouth audiomentations pedalboard ffmpeg-python==0.2.0 pyworld diffsptk nnAudio unidecode inflect ptwt

pip install torchmetrics pymcd openai-whisper frechet_audio_distance asteroid

pip install https://github.com/vBaiCai/python-pesq/archive/master.zip

pip install fairseq

pip install git+https://github.com/lhotse-speech/lhotse

pip install -U encodec

pip install phonemizer==3.2.1 pypinyin==0.48.0

# Uninstall nvidia-cublas-cu11 if there exist some bugs about CUDA version
# pip uninstall nvidia-cublas-cu11
