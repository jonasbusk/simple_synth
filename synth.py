import pyaudio
import numpy as np


class Synth(object):

    def __init__(self, rate=44100, master_volume=.5):
        self.rate = rate
        self.master_volume = master_volume

        freq0 = 8.175799
        ratio = 2**(1.0/12)
        self.midi_table = {i: freq0 * ratio**i for i in range(128)}

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1,
                        rate=self.rate, output=1)

    def terminate(self):
        self.stream.close()
        self.p.terminate()

    def sinewave(self, frequency):
        length = int(1/frequency * self.rate) # one period
        factor = frequency * (np.pi * 2) / self.rate
        return np.sin(np.arange(length) * factor)

    def play_note(self, note=60):
        frequency = self.midi_table[note]
        chunk = self.sinewave(frequency) * self.master_volume
        self.stream.write(chunk.astype(np.float32).tostring())
