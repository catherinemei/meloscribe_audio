import sounddevice as sd
import librosa
import numpy as np
from scipy.io.wavfile import write
from tkinter import *
from tkinter.messagebox import showinfo, showerror, askokcancel
from PIL import ImageTk, Image
import time
import threading
import os
from idlelib.tooltip import Hovertip
import customtkinter
from tooltip import Hovertip

# heavily based on https://www.thepythoncode.com/article/make-a-gui-voice-recorder-python

def get_scale_notes(key_str):
    """
    Given the letter denoting the major or minor key
    Return the notes in the scale for that major or minor key

    :param key_str: string representing the key
    :return: list of notes within the key
    """
    minor_keys = {'A': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
                  'A#': ['A#', 'B#', 'C#', 'D#', 'E#', 'F#', 'G#'],
                  'Ab': ['Ab', 'Bb', 'Cb', 'Db', 'Eb', 'Fb', 'Gb'],
                  'B': ['B', 'C#', 'D', 'E', 'F#', 'G', 'A'],
                  'B#': ['B#', 'C##', 'D#', 'E#', 'F##', 'G#', 'A#'],
                  'Bb': ['Bb', 'C', 'Db', 'Eb', 'F', 'Gb', 'Ab'],
                  'C': ['C', 'D', 'Eb', 'F', 'G', 'Ab', 'Bb'],
                  'C#': ['C#', 'D#', 'E', 'F#', 'G#', 'A', 'B'],
                  'C##': ['C##', 'D##', 'E#', 'F##', 'G##', 'A#', 'B#'],
                  'D': ['D', 'E', 'F', 'G', 'A', 'Bb', 'C'],
                  'D#': ['D#', 'E#', 'F#', 'G#', 'A#', 'B', 'C#'],
                  'Db': ['Db', 'Eb', 'Fb', 'Gb', 'Ab', 'Bbb', 'Cb'],
                  'E': ['E', 'F#', 'G', 'A', 'B', 'C', 'D'],
                  'E#': ['E#', 'F##', 'G#', 'A#', 'B#', 'C#', 'D#'],
                  'Eb': ['Eb', 'F', 'Gb', 'Ab', 'Bb', 'Cb', 'Db'],
                  'F': ['F', 'G', 'Ab', 'Bb', 'C', 'Db', 'Eb'],
                  'F#': ['F#', 'G#', 'A', 'B', 'C#', 'D', 'E'],
                  'F##': ['F##', 'G##', 'A#', 'B#', 'C##', 'D#', 'E#'],
                  'G': ['G', 'A', 'Bb', 'C', 'D', 'Eb', 'F'],
                  'G#': ['G#', 'A#', 'B', 'C#', 'D#', 'E', 'F#'],
                  'G##': ['G##', 'A##', 'B#', 'C##', 'D##', 'E#', 'F##']}
    major_keys = {'A': ['A', 'B', 'C#', 'D', 'E', 'F#', 'G#'],
                  'A#': ['A#', 'B#', 'C##', 'D#', 'E#', 'F##', 'G##'],
                  'Ab': ['Ab', 'Bb', 'C', 'Db', 'Eb', 'F', 'G'],
                  'B': ['B', 'C#', 'D#', 'E', 'F#', 'G#', 'A#'],
                  'B#': ['B#', 'C##', 'D##', 'E#', 'F##', 'G##', 'A##'],
                  'Bb': ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A'],
                  'C': ['C', 'D', 'E', 'F', 'G', 'A', 'B'],
                  'C#': ['C#', 'D#', 'E#', 'F#', 'G#', 'A#', 'B#'],
                  'Cb': ['Cb', 'Db', 'Eb', 'Fb', 'Gb', 'Ab', 'Bb'],
                  'D': ['D', 'E', 'F#', 'G', 'A', 'B', 'C#'],
                  'D#': ['D#', 'E#', 'F##', 'G#', 'A#', 'B#', 'C##'],
                  'Db': ['Db', 'Eb', 'F', 'Gb', 'Ab', 'Bb', 'C'],
                  'E': ['E', 'F#', 'G#', 'A', 'B', 'C#', 'D#'],
                  'E#': ['E#', 'F##', 'G##', 'A#', 'B#', 'C##', 'D##'],
                  'Eb': ['Eb', 'F', 'G', 'Ab', 'Bb', 'C', 'D'],
                  'F': ['F', 'G', 'A', 'Bb', 'C', 'D', 'E'],
                  'F#': ['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'E#'],
                  'Fb': ['Fb', 'Gb', 'Ab', 'Bbb', 'Cb', 'Db', 'Eb'],
                  'G': ['G', 'A', 'B', 'C', 'D', 'E', 'F#'],
                  'G#': ['G#', 'A#', 'B#', 'C#', 'D#', 'E#', 'F##'],
                  'Gb': ['Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'F']}

    # get the appropriate scale
    minor = key_str.islower()
    scale = major_keys[key_str] if not minor else minor_keys[key_str[0].upper() + key_str[1:]]
    scale = scale + [key_str[0].upper() + key_str[1:]]  # add tonic

    return scale


def get_scale_notes_with_octave(key_str, starting_note):
    """
    Given the user inputted key and starting note
    Return numpy array representing the scale including the starting note (at correct octave)
    :param key_str: string, major or minor key that user intends to sing in
    :param starting_note: string, tone of the starting note
    :return: list of strings representing notes in scale
    """
    distance_from_c = {'A': 6, 'B': 7, 'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G': 5}
    scale = get_scale_notes(key_str)

    # figure out what octave to play
    start_tone, octave = starting_note[:-1], int(starting_note[-1])

    tonic_dist_from_c = distance_from_c[key_str[0].upper()]
    start_tone_dist_from_c = distance_from_c[start_tone[0].upper()]

    new_scale = []

    start_octave = octave if tonic_dist_from_c <= start_tone_dist_from_c else octave - 1

    for i in range(len(scale)):
        if scale[i][0] == 'C' and i != 0:
            start_octave += 1
        new_scale.append(scale[i] + str(start_octave))

    return new_scale


def generate_scale_tones(notes, frequency, bpm):
    """
    Given the notes, the sampling frequency, and the tempo
    Generate an array representing the audio of the notes in the scale
    :param notes: strings (ex: A4) representing notes in scale
    :param frequency: sampling frequency
    :param bpm: tempo in beats per minute
    :return: array
    """
    interval_between_beats = 60 / bpm
    scale_sound = np.array([])

    for note in notes:
        note_freq = librosa.note_to_hz(note)
        tone_audio = librosa.tone(note_freq, sr=frequency, duration=interval_between_beats)
        scale_sound = np.concatenate((scale_sound, tone_audio), axis=None)

    return scale_sound, interval_between_beats * len(notes)


def launch_voice_recorder():
    """
    Launches widget that records voice and generates wav file called recording.wav
    """

    def close_window():
        """
        Closes recording window
        """
        if askokcancel(title='Close Voice Recorder', message='Are you sure you want to close the Voice Recorder?'):
            window.destroy()

    def recording_thread():
        """
        Function that triggers recording (activated on button click)
        :return:
        """
        t1 = threading.Thread(target=record_voice)
        t1.start()

    def record_voice():
        """
        Function that records and generates wav file
        """

        def generate_click_tone_track(amp, tempo, starting_tone, frequency):
            """
            Given the level of amplification, the mentronome tempo, and the starting tone
            Generate the click track with the metronome overlaid
            :param amp: int, the amplification factor on the click trackk (sometimes tone is too loud)
            :param tempo: the metronome tempo in beats per minute
            :param starting_tone: the starting tone (ex: A4)
            :param frequency: the frequency to generate click track and tone at
            :return: np array representing the combination of the click track and starting tone;
            also returns duration of the click track
            """
            interval_between_beats = 60 / tempo
            num_beats = 8
            click_track_duration = int(interval_between_beats * num_beats)
            click_times = [i * interval_between_beats for i in range(num_beats)]
            click_track = librosa.clicks(times=click_times, sr=frequency)
            click_track = click_track * amp

            # make starting tone
            note_freq = librosa.note_to_hz(starting_tone)
            starting_tone = librosa.tone(note_freq, sr=frequency, length=len(click_track))

            # combine click track and starting tone
            combined_sound = click_track + starting_tone

            return combined_sound, click_track_duration

        def generate_click_track(amplifier, tempo, frequency, seconds):
            """
            Similar to previous helper function, except only generates click track with no tones
            :param seconds: duration of the click track in seconds
            :param amplifier: int, the amplification factor on the click trackk (sometimes tone is too loud)
            :param tempo: the metronome tempo in beats per minute
            :param frequency: the frequency to generate click track and tone at
            :return: numpy array representing the audio of the click track
            """
            interval_between_beats = 60 / tempo
            num_beats = int(seconds / interval_between_beats)
            click_times = [i * interval_between_beats for i in range(num_beats)]
            click_track = librosa.clicks(times=click_times, sr=frequency)
            click_track = click_track * amplifier

            return click_track

        #####################################################################################

        try:
            freq = 44100

            duration = int(duration_entry.get())
            key = key_entry.get()
            metronome_tempo = int(metronome_entry.get())
            tone = tone_entry.get()
            amp = 2

            stacked, click_track_duration = generate_click_tone_track(amp, metronome_tempo, tone, freq)
            notes_scale = get_scale_notes_with_octave(key, tone)
            scale_audio, scale_duration = generate_scale_tones(notes_scale, freq, metronome_tempo)

            # write key to text file
            with open('audio_files/recording_key.txt', 'w') as f:
                f.write(key)
                f.close()

            final_audio = np.concatenate((scale_audio, stacked))
            metronome_while_recording = generate_click_track(2, metronome_tempo, freq, duration)
            sd.play(final_audio, freq)

            # Indicate how many seconds left before recording starts
            time_left_before_start = int(click_track_duration + scale_duration)
            while time_left_before_start > 0:
                window.update()
                time.sleep(1)
                time_left_before_start -= 1
                progress_label.configure(text="Start Recording in: " + str(time_left_before_start))

            sd.wait()
            recording = sd.playrec(metronome_while_recording, samplerate=freq, channels=1)
            counter = 0
            while counter < duration:
                window.update()
                time.sleep(1)
                counter += 1
                progress_label.configure(text="Recording Timer: " + str(counter))
            sd.wait()
            file_name = 'audio_files/recording.wav'
            write(file_name, freq, recording)
            showinfo('Recording complete', 'Your recording is complete')
        except:
            showerror(title='Error', message='An error occurred' \
                                             '\nThe following could ' \
                                             'be the causes:\n->Bad duration value\n->An empty entry field\n' \
                                             'Do not leave the entry empty and make sure to enter a valid duration '
                                             'value')

    ####### CREATE WIDGET #######
    POPUP_HEIGHT = 700
    POPUP_WIDTH = 500
    LOGO_WIDTH = 300
    LOGO_HEIGHT = 300

    customtkinter.set_appearance_mode('light')
    customtkinter.set_default_color_theme('blue')
    window = customtkinter.CTk()
    window.protocol('WM_DELETE_WINDOW', close_window)
    window.title('Voice Recorder')
    window.geometry(f'{POPUP_WIDTH}x{POPUP_HEIGHT}+440+180')
    window.resizable(height=TRUE, width=TRUE)

    # Creating picture for recording widget
    logo = Image.open(os.path.dirname(os.path.realpath(__file__)) + "/record.png")
    logo = logo.resize((LOGO_WIDTH, LOGO_HEIGHT))  # width, height
    record_img = customtkinter.CTkImage(logo, size=(LOGO_WIDTH, LOGO_HEIGHT))
    record_img_label = customtkinter.CTkLabel(window, text="", image=record_img)
    record_img_label.place(relx=0.5, rely=0.1, anchor=CENTER)

    # Create box to enter recording duration
    duration_label = customtkinter.CTkLabel(window, text='Number of Measures', font=("Helvetica", 24))
    duration_entry = customtkinter.CTkEntry(window, width=60)
    Hovertip(duration_entry,'Enter the number of 4-beat \nmeasures you wish to record', hover_delay=0)
    duration_label.place(relx=0.5, rely=0.25, anchor=CENTER)
    duration_entry.place(relx=0.5, rely=0.30, anchor=CENTER)

    # Create input for metronome
    metronome_label = customtkinter.CTkLabel(window, text='Metronome Tempo', font=("Helvetica", 24))
    metronome_entry = customtkinter.CTkEntry(window, width=60)
    Hovertip(metronome_entry, 'Enter the tempo you wish to \nrecord at in beats per minute', hover_delay=0)
    metronome_label.place(relx=0.5, rely=0.37, anchor=CENTER)
    metronome_entry.place(relx=0.5, rely=0.42, anchor=CENTER)

    # Create a box to enter note for starting tone
    tone_label = customtkinter.CTkLabel(window, text='Starting Note', font=("Helvetica", 24))
    tone_entry = customtkinter.CTkEntry(window, width=60)
    Hovertip(tone_entry, 'Enter the starting note in the format:\n[Note Name][Octave] e.g. A4', hover_delay=0)
    tone_label.place(relx=0.5, rely=0.50, anchor=CENTER)
    tone_entry.place(relx=0.5, rely=0.55, anchor=CENTER)

    # Create a checkbox for entering scale / key
    choices = ['C', 'D', 'E', 'F', 'G', 'A', 'B',
               'c', 'd', 'e', 'f', 'g', 'a', 'b']
    key_entry = StringVar(window, "C")  # Create a variable for strings, and initialize the variable
    buttons = []
    for choice in choices:
        button = customtkinter.CTkRadioButton(window, text=choice, variable=key_entry, value=choice, font=("Helvetica", 16))
        buttons.append(button)

    key_label = customtkinter.CTkLabel(window, text='Select a key signature', font=("Helvetica", 24))
    key_label.place(relx=0.5, rely=0.65, anchor=CENTER)

    num_key_letters = len(choices) // 2  # number of key letters
    for i in range(len(buttons)):
        if i // num_key_letters == 0:
            # first row items
            buttons[i].place(relx=0.25 + (0.6 / (num_key_letters - 1)) * i, rely=0.70, anchor=CENTER)
        elif i // num_key_letters == 1:
            # second row items
            buttons[i].place(relx=0.25 + (0.6 / (num_key_letters - 1)) * (i % num_key_letters), rely=0.75, anchor=CENTER)

    # Create progress bar and recording button
    progress_label = customtkinter.CTkLabel(window, text="Press Record to Start!", font=("Helvetica", 24))
    record_button = customtkinter.CTkButton(window, text='Record', command=recording_thread)
    progress_label.place(relx=0.5, rely=0.85, anchor=CENTER)
    record_button.place(relx=0.5, rely=0.90, anchor=CENTER)

    window.mainloop()


# launch_voice_recorder()
