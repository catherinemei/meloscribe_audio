#!/bin/sh
# Runs the audio_processing script; ideally for use in the musescore plugin

cd /Users/20gracehuang/Downloads/Documents/MIT\ Files/2023-spring-classes/6.8510/meloscribe_audio

printf '\nSetting Up Virtual Environment\n'

# setup virtual environment
source venv/bin/activate

python3 audio_processing.py

