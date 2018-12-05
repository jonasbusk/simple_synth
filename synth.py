import pyaudio
import numpy as np


class Synth(object):

    def __init__(self, keyboard, rate=44100, master_volume=.8):
        self.keyboard = keyboard
        self.rate = rate # sample rate
        self.chunk_size = 1024
        self.master_volume = master_volume

        self.octave = 5
        self.octave_min = 2
        self.octave_max = 9
        self.last_key = None
        self.t = 0 # time

        # create midi table
        freq0 = 8.175799
        ratio = 2**(1.0/12)
        self.midi_table = {i: freq0 * ratio**i for i in range(128)}

        # init audio
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1,
                        rate=self.rate, output=1)

    def start(self):
        while True:
            self.keyboard.update()
            if self.keyboard.quit:
                break # exit loop
            if self.keyboard.octave_up:
                self.octave = min(self.octave_max, self.octave + 1)
            if self.keyboard.octave_down:
                self.octave = max(self.octave_min, self.octave - 1)
            self.play_note(self.keyboard.key)
        self.terminate()

    def terminate(self):
        self.stream.close()
        self.p.terminate()
        self.keyboard.terminate()

    def sinewave(self, frames, frequency, t):
        p = 2 * np.pi * frequency
        factor = p / self.rate
        offset = p * t
        x = np.arange(frames) * factor + offset
        y = np.sin(x)
        return y

    def play_note(self, key):
        if key is not None:
            frequency = self.midi_table[self.octave * 12 + key]
            y = self.sinewave(self.chunk_size, frequency, self.t)
            self.t += self.chunk_size/self.rate
        elif key is None and self.last_key is not None:
            # release: fade one chunk to avoid click
            frequency = self.midi_table[self.octave * 12 + self.last_key]
            y = self.sinewave(self.chunk_size, frequency, self.t)
            y = y * np.linspace(1,0,self.chunk_size)
        else:
            y = np.zeros(self.chunk_size)
            self.t = 0
        y = y * self.master_volume
        self.stream.write(y.astype(np.float32).tobytes())
        self.last_key = key
