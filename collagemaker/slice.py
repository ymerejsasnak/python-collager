from random import randint, choice, random

import numpy as np

from collagemaker.settings import Settings
from collagemaker.utility import SAMPLES_PER_MS
from collagemaker.utility import apply_fades
from collagemaker.utility import normalize


class Slice:

    def __init__(self, source_data: np.ndarray, settings: Settings):

        self.source_data = source_data
        self.data = None

        self.settings = settings

        self.compose()

    def compose(self):
        # decide length in samples
        length = int(choice(self.settings.slice.length) * SAMPLES_PER_MS)

        # decide portion of sample to use
        offset = 0
        source_length = len(self.source_data[0])
        if source_length > length:
            offset = randint(0, source_length - length)
        # (if smaller than 'length' just uses entire sample)
        else:
            length = source_length

        # slice the data
        self.data = self.source_data[:, offset: offset + length]

        # fade
        self.data = apply_fades(self.data, self.settings.slice.fades)

        # channel volumes
        self.data[0] *= random() / 2 + 0.5
        self.data[1] *= random() / 2 + 0.5

        # normalize
        self.data = normalize(self.data)
