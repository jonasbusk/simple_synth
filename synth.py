import pyaudio
import numpy as np


class Synth(object):

    def __init__(self, keyboard, rate=44100, master_volume=.8):
        self.keyboard = keyboard
        self.rate = rate # sample rate
        self.chunk_size = 1024
        self.master_volume = master_volume

        self.octave = 5
        self.last_key = None
        self.t = 0 # time

        # create midi table
        freq0 = 8.175799
        ratio = 2**(1.0/12)
        self.midi_table = {i: freq0 * ratio**i for i in range(128)}

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1,
                        rate=self.rate, output=1)

    def start(self):
        while True:
            key = self.keyboard.get_key()
            self.play_note(key)
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
