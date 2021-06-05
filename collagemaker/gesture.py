from random import choice
from typing import Tuple

import numpy as np

from collagemaker.settings import Settings
from collagemaker.utility import apply_fades
from collagemaker.slice import Slice


class Gesture:

    def __init__(self, sample_data: np.ndarray, settings: Settings):

        self.data = None
        self.settings = settings
        self.slice = Slice(sample_data, settings)

        self.compose()

    def compose(self):

        repeats = choice(self.settings.gesture.repeats)

        spacing = int(len(self.slice.data) * choice(self.settings.gesture.spacing)/100)

        # calculate total output length...
        data_length = len(self.slice.data) * repeats + spacing * (repeats - 1)

        self.data = np.zeros((data_length, 2))

        # then just add padded slices
        position = 0
        for r in range(repeats):
            data = np.pad(self.slice.data, ((position, len(self.data) - len(self.slice.data) - position), (0, 0)))
            self.data += data
            position += len(self.slice.data) + spacing

        self.data = apply_fades(self.data, self.settings.gesture.fades)
