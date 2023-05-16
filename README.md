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
