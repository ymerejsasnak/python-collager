from random import randint

import numpy as np

from collagemaker.collage import Collage


class Slice:

    def __init__(self, source_data, length_min=100, length_max=100, fade_in=0, fade_out=0.5):

        self.source_data = source_data
        self.len_min = length_min
        self.len_max = length_max
        self.fade_in = fade_in
        self.fade_out = fade_out

        self.data = None

        self.calculate()

    def calculate(self):

        # decide length in samples
        length = int(randint(self.len_min, self.len_max) * Collage.SAMPLES_PER_MS)

        # decide portion of sample to use (if smaller than 'length' just uses entire sample)
        offset = 0
        if len(self.source_data) > length:
            offset = randint(0, len(self.source_data) - length)
        else:
            length = len(self.source_data)

        fade_in_length = int(self.fade_in * length)
        fade_out_length = int(self.fade_out * length)

        fade_in_env = np.linspace(start=0, stop=1, num=fade_in_length)
        fade_in_env = np.append(fade_in_env, np.ones(length - fade_in_length))

        fade_out_env = np.linspace(start=1, stop=0, num=fade_out_length)
        fade_out_env = np.insert(np.ones(length - fade_out_length), length - fade_out_length, fade_out_env)

        self.data = self.source_data[offset: offset + length] * fade_in_env * fade_out_env
