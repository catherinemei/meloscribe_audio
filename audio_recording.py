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
        try:
            freq = 44100

            
            duration = int(duration_entry.get())

            # make click track
            # click_track_duration = 8
            amp = 2
            metronome_tempo = int(metronome_entry.get())
            interval_between_beats = 60 / metronome_tempo
            # num_beats = int(click_track_duration / interval_between_beats) + 1
            num_beats = 8
            click_track_duration = int(interval_between_beats * num_beats)
            click_times = [i * interval_between_beats for i in range(num_beats)]
            click_track = librosa.clicks(times=click_times, sr=freq)
            click_track = click_track * amp

            # make starting tone
            tone = tone_entry.get()
            note_freq = librosa.note_to_hz(tone)
            starting_tone = librosa.tone(note_freq, sr=freq, length=len(click_track))

            # combine click track and starting tone
            stacked = click_track + starting_tone
            sd.play(stacked, freq)

            # Indicate how many seconds left before recording starts
            time_left_before_start = click_track_duration
            while time_left_before_start > 0:
                window.update()
                time.sleep(1)
                time_left_before_start -= 1
                progress_label.config(text="Start Recording in: " + str(time_left_before_start))

            sd.wait()
            recording = sd.rec(duration * freq, samplerate=freq, channels=1)
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
    POPUP_HEIGHT = 600
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

    # Create progress bar and recording button
    progress_label = ttk.Label(window, text="Press Record to Start!")
    record_button = ttk.Button(window, text='Record', style='TButton', command=recording_thread)
    canvas.create_window(POPUP_WIDTH // 2, 500, window=progress_label)
    canvas.create_window(POPUP_WIDTH // 2, 550, window=record_button)

    window.mainloop()

launch_voice_recorder()