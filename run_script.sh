#!/bin/sh
# Runs the audio_processing script; ideally for use in the musescore plugin

# Replace with your absolute path to the meloscribe_audio folder 
cd /Users/20gracehuang/Downloads/Documents/MIT\ Files/2023-spring-classes/6.8510/meloscribe_audio

printf '\nSetting Up Virtual Environment\n'

# setup virtual environment: Change this path if your venv is in a different folder
source venv/bin/activate

# runs audio_processing script
python3 audio_processing.py

