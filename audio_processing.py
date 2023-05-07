import librosa
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import wavio
from audio_recording import launch_voice_recorder
from audio_recording import get_scale_notes


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


def process_fundamental_freqs(f0_freq, f0_time):
    """
    Given the fundamental frequencies and corresponding times, remove all nans from list
    :param f0_freq: list of fundamental frequencies
    :param f0_time: list of times corresponding to the fundamental frequencies
    :return: f0s and f0_times with nan values filtered out; raw note information list
    Writes js file with JSON object of the notes
    """
    new_f0s = []
    new_times = []

    for i in range(len(f0_freq)):
        if str(f0_freq[i]) != 'nan':
            new_f0s.append(f0_freq[i])
            new_times.append(f0_time[i])

    return new_f0s, new_times


def segment_notes(note_onsets, f0s_freq, f0_time, file_name):
    """
    Given a list of onsets and all of the fundamental frequencies and timestamps of those frequencies,
    generate a CSV with the start and end timestamps of a note as well as the note frequency and letter
    :param note_onsets: estimated beat event locations in time (seconds)
    :param f0s_freq: fundamental frequencies
    :param f0_time: times that the fundamental frequences occur
    :param file_name: file name of output json for notes
    :return: pandas Dataframe and raw note_info list
    """

    # load notes in key + find notes in key
    with open('audio_files/recording_key.txt', 'r') as f:
        line_input = f.read()
        lines = line_input.split("\n")

    key = lines[0]
    scale = get_scale_notes(key)

    # (timestamp start, timestamp end, note frequency, note letter, frequencies included)
    note_info = []
    freq_pt = 0
    json_obj_str = "var notes = ["

    for t in range(len(note_onsets) - 1):
        window_start = note_onsets[t]
        window_end = note_onsets[t + 1]
        window_freqs = []
        window_times = []

        # note is after this window, then skip
        if freq_pt < len(f0_time) and f0_time[freq_pt] > window_end:
            continue

        # note is before this window started, then fast forward
        while freq_pt < len(f0_time) and f0_time[freq_pt] < window_start:
            freq_pt += 1

        # add notes in window
        while freq_pt < len(f0_time) and f0_time[freq_pt] < window_end:
            window_freqs.append(f0s_freq[freq_pt])
            window_times.append(f0_time[freq_pt])
            freq_pt += 1

        # window is too short, doesn't contain any notes
        if len(window_freqs) < 2:
            continue

        note, note_freq, note_midi = match_correct_note(window_freqs, scale)
        note_info.append((window_times[0], window_times[-1], note_freq, note, note_midi, window_freqs))
        note_obj = "{ start_sec: " + str(window_times[0]) + ", end_sec: " + str(
            window_times[-1]) + ", note_freq_hz: " + str(note_freq) + ", note_midi: " + str(
            note_midi) + ", note_name: '" + note + "' }, "
        json_obj_str += note_obj

    # take care of last note
    if freq_pt < len(f0_time):
        window_freqs = f0s_freq[freq_pt:]
        window_times = f0_time[freq_pt:]

        if len(window_freqs) >= 2:
            note, note_freq, note_midi = match_correct_note(window_freqs, scale)
            note_info.append((window_times[0], window_times[-1], note_freq, note, note_midi, window_freqs))
            note_obj = "{ start_sec: " + str(window_times[0]) + ", end_sec: " + str(
                window_times[-1]) + ", note_freq_hz: " + str(note_freq) + ", note_midi: " + str(
                note_midi) + ", note_name: '" + note + "' }]; "
            json_obj_str += note_obj
        else:
            json_obj_str += "];"

    f = open(f'js_files_notes/{file_name}', "w")
    f.write(json_obj_str)
    f.close()

    # make dataframe and CSV of information
    df_notes = pd.DataFrame(note_info, columns=['start_sec', 'end_sec', 'note_freq_hz', 'note_name', 'midi_note',
                                                'included_freqs'])

    return df_notes, note_info


def match_correct_note(window_freqs, notes_in_key):
    """
    Given the frequencies in the window current window and the notes in the current key
    Return the in-key note that is closest in frequency value to the average frequency of the window
    :param window_freqs: list of frequency values
    :param notes_in_key: list of notes in the key
    :return: string representing the note within the window (note name + octave)
    the frequency of the note, and the midi number for the note
    """
    average_freq = np.average(window_freqs)

    closest_note_name = ""
    closest_note_freq = 0
    min_freq_diff = float("inf")

    # check notes from C1 to C7
    # loop through all the options and find note in key that is closest to current
    for note in notes_in_key:
        for octave in range(1, 8):
            note_with_octave = note + str(octave)
            note_with_octave_freq = librosa.note_to_hz(note_with_octave)

            if abs(note_with_octave_freq - average_freq) < min_freq_diff:
                min_freq_diff = abs(note_with_octave_freq - average_freq)
                closest_note_freq = note_with_octave_freq
                closest_note_name = note_with_octave

    note_midi = librosa.note_to_midi(closest_note_name)

    return closest_note_name, closest_note_freq, note_midi


def combine_onset_times(onset_detect, beat_track):
    """
    Given onset times found using onset.onset_detect and beat.beat_track,
    combine the two sets of information so that beat_track has the last onset time
    :param onset_detect: list of onset times as outputted by onset.onset_detect
    :param beat_track: list of onset times as outputted by beat.beat_track
    :return: combined onset times
    """
    last_beat = beat_track[-1]
    pt = 0

    while pt < len(onset_detect) and onset_detect[pt] < last_beat:
        pt += 1

    beat_onsets = list(beat_track) + list(onset_detect[pt:])

    return beat_onsets


def generate_wav(notes_list, sample_rate, file_name):
    """
    Given the notes, sample rate, and output filename, generate WAV file of processed notes
    :param notes_list: list of tuples representing note information (including onset time, offset time,
    note frequency in hz, note name as a string, and list of frequencies included in interval)
    :param sample_rate: sample rate of audio file
    :param file_name: string representing name of output wav file
    """

    audio_end_time = int(notes_list[-1][1] * sample_rate) + 1
    frames = [0 for _ in range(audio_end_time + 1)]

    for note in notes_list:
        start_time, end_time, note_freq = note[0], note[1], note[2]

        T = end_time - start_time
        n = int(sample_rate * T)  # number of samples
        t = np.arange(n) / sample_rate  # grid of time values
        x = np.sin(2 * np.pi * note_freq * t)

        for f in range(len(x)):
            frames[int(start_time * sample_rate) + f] = x[f]

    wavio.write(f'regenerated_wav/{file_name}', frames, sample_rate, sampwidth=3)


###################### MAIN ######################
launch_voice_recorder()

# y, sr = librosa.load("audio_files/birthday.wav")
# y, sr = librosa.load("audio_files/twinkle.wav")

y, sr = librosa.load("audio_files/recording.wav")

# Identify fundamental frequency
f0, voiced_flag, voiced_probs = librosa.pyin(y, fmin=librosa.note_to_hz('C2'), fmax=librosa.note_to_hz('C7'), sr=sr)
times = librosa.times_like(f0)
f0s, f0_times = process_fundamental_freqs(f0, times)
# plot_fundamental_freqs(y, f0)

# Rhythm detection - onset.onset_detect
onsets = librosa.onset.onset_detect(y=y, sr=sr, units='time')
# plot_beats(y, onsets)

# Rhythm detection - beat.beat_track
tempo, beats = librosa.beat.beat_track(y=y, sr=sr, units='time')
# plot_beats(y, beats)

# librosa.beat.beat_track misses last onset, get that information from onsets and combine the two
final_beats = combine_onset_times(onsets, beats)
# plot_beats(y, final_beats)

notes_df, notes_info = segment_notes(final_beats, f0s, f0_times, 'recording.js')

notes_df.to_csv('notes_summary_csv/recording.csv')
# notes_df.to_csv('birthday.csv')

# generate_wav(notes_info, sr, 'birthday_regenerated.wav')
# generate_wav(notes_info, sr, 'twinkle_regenerated.wav')
generate_wav(notes_info, sr, 'recording_regenerated.wav')
