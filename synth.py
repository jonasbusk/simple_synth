import pyaudio
import numpy as np


class Synth(object):

    def __init__(self, keyboard, rate=44100, master_volume=.8):
        self.keyboard = keyboard
        self.rate = rate # sample rate
        self.chunk_size = 256
        self.master_volume = master_volume

        self.octave = 5
        self.octave_min = 2
        self.octave_max = 9
        self.last_note = None
        self.t = 0 # time

        # create midi table
        freq0 = 8.175799
        ratio = 2**(1.0/12)
        self.midi_table = {i: freq0 * ratio**i for i in range(128)}

        # chunks
        self.chunk_zeros = np.zeros(self.chunk_size)
        self.chunk_fade_in = np.linspace(0,1,self.chunk_size)
        self.chunk_fade_out = np.ones(self.chunk_size) - self.chunk_fade_in

        # init audio
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1,
                        rate=self.rate, output=1)

    def start(self):
        while True: # main loop
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

    def sinewave(self, frequency):
        p = 2 * np.pi * frequency
        factor = p / self.rate
        offset = p * self.t
        x = np.arange(self.chunk_size) * factor + offset
        y = np.sin(x)
        return y

    def play_note(self, key):
        # compute note
        if key is not None:
            note = 12 * self.octave + key
        else:
            note = None
        # compute y
        y = np.zeros(self.chunk_size)
        if note != self.last_note and note is not None:
            # fade in new note
            y += self.sinewave(self.midi_table[note]) * self.chunk_fade_in
        if note != self.last_note and self.last_note is not None:
            # fade out last note
            y += self.sinewave(self.midi_table[self.last_note]) * self.chunk_fade_out
        if note == self.last_note and note is not None:
            # sustain note
            y += self.sinewave(self.midi_table[note])
        # output
        y = y * self.master_volume
        self.stream.write(y.astype(np.float32).tobytes())
        # update
        self.last_note = note
        self.t += self.chunk_size/self.rate
