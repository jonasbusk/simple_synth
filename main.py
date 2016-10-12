import pyaudio
import numpy as np


class Synth(object):

    def __init__(self, rate=44100, master_volume=.5):
        self.rate = rate
        self.master_volume = master_volume

        freq0 = 8.175799
        ratio = 2**(1.0/12)
        self.midi_table = {i: freq0 * ratio**i for i in range(128)}
        print self.midi_table[69]

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1,
                        rate=self.rate, output=1)

    def stop(self):
        self.stream.close()
        self.p.terminate()

    def sine(self, frequency, length):
        length = int(length * self.rate)
        factor = float(frequency) * (np.pi * 2) / self.rate
        return np.sin(np.arange(length) * factor)

    def play_note(self, note=69, length=1):
        frequency = self.midi_table[note]
        chunks = []
        chunks.append(self.sine(frequency, length))
        chunk = np.concatenate(chunks) * self.master_volume
        self.stream.write(chunk.astype(np.float32).tostring())

def main():
    s = Synth()
    s.play_note(60, .5)
    s.play_note(64, .5)
    s.play_note(67, 1)
    s.stop()

if __name__ == '__main__':
    main()
