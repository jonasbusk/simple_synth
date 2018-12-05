import pyaudio
import numpy as np


class Synth(object):

    def __init__(self, keyboard, sample_rate=44100, buffer_size=128, master_volume=.8):
        self.keyboard = keyboard
        self.sample_rate = sample_rate
        self.buffer_size = buffer_size
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

        # buffers
        self.tmp = np.zeros(self.buffer_size) # tmp buffer
        self.out = np.zeros(self.buffer_size) # output buffer

        # fixed buffers
        self.range = np.arange(self.buffer_size)
        self.fade_in = np.linspace(0, 1, self.buffer_size)
        self.fade_out = np.ones(self.buffer_size) - self.fade_in

        # init audio
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=pyaudio.paFloat32, channels=1,
                        rate=self.sample_rate, output=1)

    def start(self):
        while True: # main loop
            self.keyboard.update()
            if self.keyboard.quit:
                break # exit loop
            if self.keyboard.octave_up:
                self.octave = min(self.octave_max, self.octave + 1)
            if self.keyboard.octave_down:
                self.octave = max(self.octave_min, self.octave - 1)
            self.play(self.keyboard.key)
        self.terminate()

    def terminate(self):
        self.stream.close()
        self.p.terminate()
        self.keyboard.terminate()

    def sinewave(self, frequency, out):
        p = 2 * np.pi * frequency
        factor = p / self.sample_rate
        offset = p * self.t
        np.multiply(self.range, factor, out=out) # x
        np.add(out, offset, out=out) # x
        np.sin(out, out=out) # y

    def play(self, key):
        # compute note
        if key is not None:
            note = 12 * self.octave + key
        else:
            note = None
        # compute output
        self.out.fill(0) # clear output buffer
        if note != self.last_note and note is not None:
            # fade in new note
            self.sinewave(self.midi_table[note], out=self.tmp)
            np.multiply(self.tmp, self.fade_in, out=self.tmp)
            np.add(self.out, self.tmp, out=self.out)
        if note != self.last_note and self.last_note is not None:
            # fade out last note
            self.sinewave(self.midi_table[self.last_note], out=self.tmp)
            np.multiply(self.tmp, self.fade_out, out=self.tmp)
            np.add(self.out, self.tmp, out=self.out)
        if note == self.last_note and note is not None:
            # sustain note
            self.sinewave(self.midi_table[note], out=self.tmp)
            np.add(self.out, self.tmp, out=self.out)
        # output
        np.multiply(self.out, self.master_volume, out=self.out)
        self.stream.write(self.out.astype(np.float32).tobytes())
        # update
        self.last_note = note
        self.t += self.buffer_size / self.sample_rate
