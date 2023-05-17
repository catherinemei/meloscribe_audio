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
* **`audio_files/recording_info.txt`:** File containing the key and tempo of the user recording. Used in processing the
recorded audio.

* **WAV files in `audio_files` folder:** the WAV files in the `audio_files` folder are sample audio files that the 
  `audio_processing.py` script can can process. In particular, the `recording.wav` file is the recorded audio from the user.
  The other WAV files (e.g. `birthday.wav`) are example recordings that can be used to test the `audio_processing.py` script.

* **`audio_processing.py`:** Main script for our tool that reads in the recorded audio file from the `audio_files` folder and
performs pitch segmentation, rhythm segmentation, and note smoothing to in-scale values. The segmented audio information is
  outputted to CSV files stored in the `notes_summary_csv` folder.

* **`audio_recording.py`:** Script that generates the recording GUI for our tool. Creates input fields (consisting of text input, radiobuttons, 
  and more). Script records user audio and outputs recording to the `audio_files` folder. User specified tempo and key are 
  stored into the `audio_files/recording_info.txt` file.

* **`insert_notes.qml`:** GRACE

* **CSV files in `notes_summary_csv` folder:** The CSVs in this folder contain the results of the `audio_processing.py` script.
In particular, the CSVs contain information about the start and end times of a note (relative to the beginning of the recording, 
  measured in seconds), the frequency of the detected note,
  the note name (string), the corresponding MIDI number for the note, and the frequencies included in the
  window from the start to end time frame (included for quality control). CSV files are named according to their corresponding
  audio file (e.g. the CSV output for `recording.wav` is `recording.csv`).

* **`record.png`:** Image of the recording icon on the recording GUI.

* **WAV files in `regenerated_wav` folder:** The WAV files in the `regenerated_wav` folder are audio representations of the 
CSV files in the `notes_summary_csv` folder. In particular, our tool reads CSV files in the `notes_summary_csv` folder and
  regenerates the identified notes into a playable WAV file. Having these regenerated audio files allow users without MuseScore
  access to examine the processed recording output.

* **`requirements.txt`:** File containing the requirements for this project. Run `pip install -r requirements.txt`
to install the packages listed in this file.

* **`run_script.sh`:** GRACE

* **`script.js`:** GRACE

* **`tooltip.py`:** File that contains the Tooltip class used to generate recording GUI. This tooltip implementation is based on
the Hovertip implementation from `idlelib.tooltip`. However, we mutated the styling of the tooltip. The code for the original tooltip
  implementation can be found here: https://github.com/python/cpython/blob/main/Lib/idlelib/tooltip.py
  
# Installation & Setup Instructions

### 1. Clone the repository & install requirements

Clone the repository into your local working directory. It is recommended that you make a Python 3.7 virtual environment 
for running this project. Then, install the requirements for this project by running the command:

```
pip install -r requirements.txt
```

### 2. Install MuseScore & Plugin Setup

Install MuseScore 3 here: [https://ftp.osuosl.org/pub/musescore/releases/MuseScore-3.2/](https://ftp.osuosl.org/pub/musescore/releases/MuseScore-3.2/).

Then, navigate to the `Plugin Creator` option under `Plugins`. 

Open the `insert_notes.qml` file and replace the `pathToMeloscribe` variable with the absolute path to your meloscribe folder.

If you would like to (attempt to) run the bash script (`run_script.sh`), you should also change the relevant paths there to match with your system.

For more information on MuseScore plugins, see [https://musescore.org/en/handbook/3/plugins](https://musescore.org/en/handbook/3/plugins).

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

### 4. Run MuseScore Plugin & Paste Transcribed Output

Once the system has finished processing the recorded input (signalled by the command-line interface finishing its execution), you can run the MuseScore plugin. In order to alter where the recorded output will be placed, move the cursor to a specific beat. Note here that selecting the entire measure will not update the cursor position correctly.

Running the plugin repeatedly will take the latest audio processing information, so results can be inserted multiple times into a score.


## FAQ: What if I don't have MuseScore installed on my computer?
If MuseScore installation is not possible, our system can still be used to transcribe and playback recorded audio. After recording audio from the user, the system processes the audio and writes the parsed results to `notes_summary_csv/recording.csv`.
Additionally, the processed audio information from the CSV is regenerated into a playable WAV file. This WAV file is
written to `regenerated_wav/recording_regenerated.wav`. Therefore, even without installing MuseScore, it is still possible
to assess the output of our system using the regenerated WAV file.

With that being said, MuseScore is available on a variety of different operating systems and should be able to be installed correctly across platforms. Our code is tested using Apple MacOS. 
