from random import randint, choice
from typing import Tuple

import numpy as np

from collagemaker.utility import SAMPLES_PER_MS
from collagemaker.utility import apply_fades


class Slice:

    def __init__(self, source_data: np.ndarray, lengths: range = range(100, 300), fades: Tuple[float] = (0.01, 0.01)):

        self.source_data = source_data
        self.lengths = lengths
        self.fades = fades
        self.data = None

        self.compose()

    def compose(self):
        # decide length in samples
        length = int(choice(self.lengths) * SAMPLES_PER_MS)

        # decide portion of sample to use (if smaller than 'length' just uses entire sample)
        offset = 0
        if len(self.source_data) > length:
            offset = randint(0, len(self.source_data) - length)
        else:
            length = len(self.source_data)

        self.data = apply_fades(self.source_data[offset: offset + length], self.fades)
