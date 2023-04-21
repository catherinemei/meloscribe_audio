import librosa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_beats(sound_y, beats):
    """
    Plots spectrogram of sound with onset detection overlaid; displays plot
    :param sound_y: audio time series; result of librosa.load
    :param beats: estimated beat event locations in time (seconds)
    """
    D = np.abs(librosa.stft(sound_y))
    fig, ax = plt.subplots()
    librosa.display.specshow(librosa.amplitude_to_db(D, ref=np.max), x_axis='time', y_axis='log', ax=ax)
    ax.set(title='Power spectrogram')
    ax.label_outer()
    ax.vlines(beats, 0, 8192, color='w', alpha=0.9,
              linestyle='--', label='Onsets')
    plt.show()


def plot_fundamental_freqs(sound_y, f0s):
    """
    Plots spectrogram of sound with detected fundamental frequencies overlaid; displays plot
    :param sound_y: audio time series; result of librosa.load
    :param f0s: fundamental frequencies
    """
    times = librosa.times_like(f0s)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(sound_y)), ref=np.max)
    fig, ax = plt.subplots()
    img = librosa.display.specshow(D, x_axis='time', y_axis='log', ax=ax)
    ax.set(title='pYIN fundamental frequency estimation')
    fig.colorbar(img, ax=ax, format="%+2.f dB")
    ax.plot(times, f0, label='f0', color='cyan', linewidth=3)
    ax.legend(loc='upper right')
    plt.show()


def process_fundamental_freqs(f0s, f0_times):
    """
    Given the fundamental frequencies and corresponding times, remove all nans from list
    :param f0s: list of fundamental frequencies
    :param f0_times: list of times corresponding to the fundamental frequencies
    :return: f0s and f0_times with nan values filtered out
    """
    new_f0s = []
    new_times = []

    for i in range(len(f0s)):
        if str(f0s[i]) != 'nan':
            new_f0s.append(f0s[i])
            new_times.append(f0_times[i])

    return new_f0s, new_times


def segment_notes(note_onsets, f0s, f0_times):
    """
    Given a list of onsets and all of the fundamental frequencies and timestamps of those frequencies,
    generate a CSV with the start and end timestamps of a note as well as the note frequency and letter
    :param note_onsets: estimated beat event locations in time (seconds)
    :param f0s: fundamental frequencies
    :param f0_times: times that the fundamental frequences occur
    :return: pandas Dataframe
    """

    # (timestamp start, timestamp end, note frequency, note letter, frequencies included)
    note_info = []
    freq_pt = 0

    for t in range(len(note_onsets) - 1):
        window_start = note_onsets[t]
        window_end = note_onsets[t + 1]
        window_freqs = []
        window_times = []

        # note is after this window, then skip
        if freq_pt < len(f0_times) and f0_times[freq_pt] > window_end:
            continue

        # note is before this window started, then fast forward
        while freq_pt < len(f0_times) and f0_times[freq_pt] < window_start:
            freq_pt += 1

        # add notes in window
        while freq_pt < len(f0_times) and f0_times[freq_pt] < window_end:
            window_freqs.append(f0s[freq_pt])
            window_times.append(f0_times[freq_pt])
            freq_pt += 1

        # window is too short, doesn't contain any notes
        if len(window_freqs) < 2:
            continue

        average_freq = np.average(window_freqs)
        note = librosa.hz_to_note(average_freq)
        note_freq = librosa.note_to_hz(note)

        note_info.append((window_times[0], window_times[-1], note_freq, note, window_freqs))

    # take care of last note
    if freq_pt < len(f0_times):
        window_freqs = f0s[freq_pt:]
        window_times = f0_times[freq_pt:]

        if len(window_freqs) >= 2:
            average_freq = np.average(window_freqs)
            note = librosa.hz_to_note(average_freq)
            note_freq = librosa.note_to_hz(note)
            note_info.append((window_times[0], window_times[-1], note_freq, note, window_freqs))

    # make dataframe and CSV of information
    df_notes = pd.DataFrame(note_info, columns=['start_sec', 'end_sec', 'note_freq_hz', 'note_name', 'included_freqs'])
    return df_notes


if __name__ == "__main__":

    y, sr = librosa.load("audio_files/birthday.wav")

    # Identify fundamental frequency
    f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr=sr)
    times = librosa.times_like(f0)

    f0s, f0_times = process_fundamental_freqs(f0, times)
    plot_fundamental_freqs(y, f0)

    # Rhythm detection - onset.onset_detect
    onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')
    # plot_beats(y, onsets)

    # Rhythm detection - beat.beat_track
    tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')
    # plot_beats(y, beats)

    # librosa.beat.beat_track misses last onset, get that information from onsets and combine the two
    last_beat = beats[-1]
    pt = 0

    while pt < len(onsets) and onsets[pt] < last_beat:
        pt += 1

    beat_onsets = list(beats) + list(onsets[pt:])
    plot_beats(y, beat_onsets)

    notes_df = segment_notes(beat_onsets, f0s, f0_times)

    # notes_df.to_csv('twinkle.csv')
    notes_df.to_csv('birthday.csv')
