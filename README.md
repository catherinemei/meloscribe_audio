# Project Directory Structure & File Explanation
The structure of our project directory is as follows:

```
📦 
├─ audio_files
│  ├─ a440.wav
│  ├─ birthday.wav
│  ├─ click_track.wav
│  ├─ recording.wav
│  ├─ recording_info.txt
│  ├─ starting_tone.wav
│  ├─ trumpet.wav
│  └─ twinkle.wav
├─ audio_processing.py
├─ audio_recording.py
├─ insert_notes.qml
├─ notes_summary_csv
│  ├─ birthday.csv
│  ├─ recording.csv
│  └─ twinkle.csv
├─ package.json
├─ record.png
├─ regenerated_wav
│  ├─ birthday_regenerated.wav
│  ├─ recording_regenerated.wav
│  └─ twinkle_regenerated.wav
├─ requirements.txt
├─ run_script.sh
├─ script.js
└─ tooltip.py
```
* **`audio_files/recording_info.txt`:**

* WAV files in `audio_files` folder: the WAV files in the `audio_files` folder are sample audio files that the 
  `audio_processing.py` script can can process. In particular, the `recording.wav` file is the recorded audio from the user.
  The other WAV files (e.g. `birthday.wav`) are example recordings that can be used to test the `audio_processing.py` script.

* `audio_processing.py`:

* `audio_recording.py`:

* `insert_notes.qml`:

* CSV files in `notes_summary_csv` folder:

* `record.png`:

* WAV files in `regenerated_wav` folder:

* `requirements.txt`:

* `run_script.sh`:

* `script.js`:

* `tooltip.py`:



# Installation & Setup Instructions

### 1. Clone the repository & install requirements

Clone the repository into your local working directory. It is recommended that you make a Python 3.7 virtual environment 
for running this project. Then, install the requirements for this project by running the command:

```
pip install -r requirements.txt
```

### 2. Install MuseScore & Plugin Setup (GRACE)

### 3. Record Audio
Next, launch the recording interface by running the command:

```
python audio_processing.py
```

After the recording GUI appears, fill in the number of measures you wish to record for, the metronome tempo you wish to
record at, the starting note of your recording, and the key you wish to record in. Press the record button to start recording.
You will be given the scale of the key that you've indicated followed by an 8-beat click track at the indicated tempo. Then,
the system will start recording your singing.

When you are finished, close the recording interface, and the system will begin processing the recorded input.

### 4. Run MuseScore Plugin & Paste Transcribed Output (GRACE)


## FAQ: What if I don't have MuseScore installed on my computer?
If MuseScore installation is not possible, our system can still be used to transcribe and playback recorded audio. After recording 
audio from the user, the system processes the audio and writes the parsed results to `notes_summary_csv/recording.csv`.
Additionally, the processed audio information from the CSV is regenerated into a playable WAV file. This WAV file is
written to `regenerated_wav/recording_regenerated.wav`. Therefore, even without installing MuseScore, it is still possible
to assess the output of our system using the regenerated WAV file.
