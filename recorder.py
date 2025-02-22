import pyautogui
import cv2
import numpy as np
import sounddevice as sd
from scipy.io.wavfile import write
import wavio as wv
import threading
import time

class ScreenRecorder:
    def __init__(self):
        self.recording = False
        self.paused = False
        self.output_video = "recorded_video.avi"
        self.output_audio = "recorded_audio.wav"
        self.audio_data = []
        self.freq = 44100

    def start(self):
        self.recording = True
        threading.Thread(target=self.record_screen).start()
        threading.Thread(target=self.record_audio).start()

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.recording = False
        return self.output_video

    def record_screen(self):
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        out = cv2.VideoWriter(self.output_video, fourcc, 20.0, screen_size)

        while self.recording:
            if not self.paused:
                img = pyautogui.screenshot()
                frame = np.array(img)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                out.write(frame)

        out.release()

    def record_audio(self):
        self.audio_data.clear()

        def callback(indata, frames, time, status):
            if self.recording and not self.paused:
                self.audio_data.append(indata.copy())

        with sd.InputStream(samplerate=self.freq, channels=2, callback=callback):
            while self.recording:
                sd.sleep(100)

        audio_array = np.concatenate(self.audio_data, axis=0)
        write(self.output_audio, self.freq, audio_array)
        wv.write(self.output_audio, audio_array, self.freq, sampwidth=2)
