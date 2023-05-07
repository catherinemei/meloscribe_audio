import sounddevice as sd
import librosa
import numpy as np
from scipy.io.wavfile import write
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askokcancel
from PIL import ImageTk, Image
import time
import threading
import os


# heavily based on https://www.thepythoncode.com/article/make-a-gui-voice-recorder-python


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

        def get_scale_notes(key):
            """
            Given the letter denoting the major or minor key
            Return the notes in the scale for that major or minor key

            :param key: string representing the key
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
            minor = key.islower()
            scale = major_keys[key] if not minor else minor_keys[key[0].upper() + key[1:]]
            scale = scale + [key[0].upper() + key[1:]]  # add tonic

            return scale


        def get_scale_notes_with_octave(key, starting_note):
            """
            Given the user inputted key and starting note
            Return numpy array representing the scale including the starting note (at correct octave)
            :param key: string, major or minor key that user intends to sing in
            :param starting_note: string, tone of the starting note
            :return: list of strings representing notes in scale
            """
            distance_from_c = {'A': 6, 'B': 7, 'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G': 5}
            scale = get_scale_notes(key)

            # figure out what octave to play
            start_tone, octave = starting_note[:-1], int(starting_note[-1])

            tonic_dist_from_c = distance_from_c[key[0].upper()]
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
                progress_label.config(text="Start Recording in: " + str(time_left_before_start))

            sd.wait()
            recording = sd.playrec(metronome_while_recording, samplerate=freq, channels=1)
            counter = 0
            while counter < duration:
                window.update()
                time.sleep(1)
                counter += 1
                progress_label.config(text="Recording Timer: " + str(counter))
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
    POPUP_WIDTH = 400
    LOGO_WIDTH = 250
    LOGO_HEIGHT = 85

    window = Tk()
    window.protocol('WM_DELETE_WINDOW', close_window)
    window.title('Voice Recorder')
    window.geometry(f'{POPUP_WIDTH}x{POPUP_HEIGHT}+440+180')
    window.resizable(height=TRUE, width=TRUE)

    # Add styling for all elements
    label_style = ttk.Style()
    label_style.configure('TLabel', foreground='#000000', font=('OCR A Extended', 18))
    entry_style = ttk.Style()
    entry_style.configure('TEntry', font=('Dotum', 15))
    button_style = ttk.Style()
    button_style.configure('TButton', foreground='#000000', font='DotumChe')

    # Creating picture for recording widget
    canvas = Canvas(window, width=POPUP_WIDTH, height=POPUP_HEIGHT)
    canvas.pack()
    logo = Image.open(os.path.dirname(os.path.realpath(__file__)) + "/record.png")
    logo = logo.resize((LOGO_WIDTH, LOGO_HEIGHT))  # width, height
    logo = ImageTk.PhotoImage(logo)
    canvas.create_image(POPUP_WIDTH // 2, 100, image=logo)

    # Create box to enter recording duration
    duration_label = ttk.Label(window, text='Duration (in sec)')
    duration_entry = ttk.Entry(window, width=14, style='TEntry')
    canvas.create_window(POPUP_WIDTH // 2, 200, window=duration_label)
    canvas.create_window(POPUP_WIDTH // 2, 225, window=duration_entry)

    # Create input for metronome
    metronome_label = ttk.Label(window, text='Metronome Tempo')
    metronome_entry = ttk.Entry(window, width=14, style='TEntry')
    canvas.create_window(POPUP_WIDTH // 2, 300, window=metronome_label)
    canvas.create_window(POPUP_WIDTH // 2, 325, window=metronome_entry)

    # Create a box to enter note for starting tone
    tone_label = ttk.Label(window, text='Starting Note')
    tone_entry = ttk.Entry(window, width=14, style='TEntry')
    canvas.create_window(POPUP_WIDTH // 2, 400, window=tone_label)
    canvas.create_window(POPUP_WIDTH // 2, 425, window=tone_entry)

    # Create a checkbox for entering scale / key
    choices = ['C', 'D', 'E', 'F', 'G', 'A', 'B',
               'c', 'd', 'e', 'f', 'g', 'a', 'b']
    key_entry = StringVar(window, "C")  # Create a variable for strings, and initialize the variable
    buttons = []
    for choice in choices:
        button = ttk.Radiobutton(window, text=choice, variable=key_entry, value=choice)
        buttons.append(button)

    key_label = ttk.Label(window, text='Select a key signature')
    canvas.create_window(POPUP_WIDTH // 2, 500, window=key_label)

    num_key_letters = len(choices) // 2  # number of key letters
    starting_loc = POPUP_WIDTH // 2 - (num_key_letters // 2) * 40
    for i in range(len(buttons)):
        if i // num_key_letters == 0:
            # first row items
            canvas.create_window(starting_loc + i * 40, 525, window=buttons[i])
        elif i // num_key_letters == 1:
            # second row items
            canvas.create_window(starting_loc + (i % num_key_letters) * 40, 550, window=buttons[i])

    # Create progress bar and recording button
    progress_label = ttk.Label(window, text="Press Record to Start!")
    record_button = ttk.Button(window, text='Record', style='TButton', command=recording_thread)
    canvas.create_window(POPUP_WIDTH // 2, 600, window=progress_label)
    canvas.create_window(POPUP_WIDTH // 2, 650, window=record_button)

    window.mainloop()


launch_voice_recorder()
