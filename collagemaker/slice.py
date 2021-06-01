from random import randint, choice
from typing import Tuple

import numpy as np

from collagemaker.audio import Audio
from collagemaker.audio import fade


class Slice:

    def __init__(self, source_data: Tuple[np.ndarray], lengths: range = range(100, 300), fades: Tuple[float] = (0.01, 0.01)):

        self.source_data = source_data
        self.lengths = lengths
        self.fades = fades
        self.data = []

        self.compose()

    def compose(self):
        self.data = []

        # decide length in samples
        length = int(choice(self.lengths) * Audio.SAMPLES_PER_MS)

        # decide portion of sample to use (if smaller than 'length' just uses entire sample)
        offset = 0
        if len(self.source_data[0]) > length:
            offset = randint(0, len(self.source_data[0]) - length)
        else:
            length = len(self.source_data[0])

        for ch in range(2):
            self.data.append(fade(self.source_data[ch][offset: offset + length], self.fades))
