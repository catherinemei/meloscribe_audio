import sounddevice as sd
from scipy.io.wavfile import write
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror, askokcancel
from PIL import ImageTk, Image
import time
import threading

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
            recording = sd.rec(duration * freq, samplerate=freq, channels=2)
            counter = 0
            while counter < duration:
                window.update()
                time.sleep(1)
                counter += 1
                progress_label.config(text=str(counter))
            sd.wait()
            file_name = 'recording.wav'
            write(file_name, freq, recording)
            showinfo('Recording complete', 'Your recording is complete')
        except:
            showerror(title='Error', message='An error occurred' \
                                             '\nThe following could ' \
                                             'be the causes:\n->Bad duration value\n->An empty entry field\n' \
                                             'Do not leave the entry empty and make sure to enter a valid duration '
                                             'value')

    ####### CREATE WIDGET #######
    POPUP_HEIGHT = 400
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
    logo = Image.open("record.png")
    logo = logo.resize((LOGO_WIDTH, LOGO_HEIGHT))  # width, height
    logo = ImageTk.PhotoImage(logo)
    canvas.create_image(POPUP_WIDTH // 2, 100, image=logo)

    # Create box to enter recording duration
    duration_label = ttk.Label(window, text='Duration (in sec)')
    duration_entry = ttk.Entry(window, width=14, style='TEntry')
    canvas.create_window(POPUP_WIDTH // 2, 200, window=duration_label)
    canvas.create_window(POPUP_WIDTH // 2, 250, window=duration_entry)

    # Create progress bar and recording button
    progress_label = ttk.Label(window, text='')
    record_button = ttk.Button(window, text='Record', style='TButton', command=recording_thread)
    canvas.create_window(POPUP_WIDTH // 2, 300, window=progress_label)
    canvas.create_window(POPUP_WIDTH // 2, 350, window=record_button)

    window.mainloop()


launch_voice_recorder()
