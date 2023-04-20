import librosa

y, sr = librosa.load("audio_files/trumpet.wav")

beats = librosa.onset.onset_detect(y=y, sr=sr, units='time')