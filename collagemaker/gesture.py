from random import choice
from typing import Tuple

import numpy as np
from scipy.signal import resample

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

        spacing = choice(self.settings.gesture.spacing) / 100

        # per-slice rate change
        slice_rates = [choice(self.settings.gesture.slice_rate) for _ in range(repeats)]
        slice_data = [resample(self.slice.data, int(len(self.slice.data) * slice_rates[i])) for i in range(repeats)]

        # calculate total output length...
        data_length = int(sum([len(slice_data[i]) * (1 + spacing) for i in range(repeats)]))

        self.data = np.zeros((data_length, 2))

        # then just add padded slices
        position = 0
        for r in range(repeats):
            data = slice_data[r]
            start = position
            end = len(self.data) - len(data) - position
            position += int(len(data) * (1 + spacing))
            data = np.pad(data, ((start, end), (0, 0)))

            self.data += data


        self.data = apply_fades(self.data, self.settings.gesture.fades)

        # per-gesture rate change
        self.data = resample(self.data, int(len(self.data) * choice(self.settings.gesture.gesture_rate)))
