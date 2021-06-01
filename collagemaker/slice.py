from random import randint, choice
from typing import Tuple

import numpy as np

from collagemaker.audio import Audio


class Slice:

    def __init__(self, source_data: np.ndarray, lengths: range = range(100, 300), fades: Tuple[float] = (0.01, 0.01)):

        self.source_data = source_data
        self.lengths = lengths
        self.fades = fades
        self.data = None

        self.compose()

    def compose(self):

        # decide length in samples
        length = int(choice(self.lengths) * Audio.SAMPLES_PER_MS)

        # decide portion of sample to use (if smaller than 'length' just uses entire sample)
        offset = 0
        if len(self.source_data) > length:
            offset = randint(0, len(self.source_data) - length)
        else:
            length = len(self.source_data)

        fade_in_length = int(self.fades[0] * length)
        fade_out_length = int(self.fades[1] * length)

        fade_in_env = np.linspace(start=0, stop=1, num=fade_in_length)
        fade_in_env = np.append(fade_in_env, np.ones(length - fade_in_length))

        fade_out_env = np.linspace(start=1, stop=0, num=fade_out_length)
        fade_out_env = np.insert(np.ones(length - fade_out_length), length - fade_out_length, fade_out_env)

        self.data = self.source_data[offset: offset + length] * fade_in_env * fade_out_env
