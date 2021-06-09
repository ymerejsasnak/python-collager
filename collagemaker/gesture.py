from random import choice
from typing import Tuple

import numpy as np
from scipy.signal import resample

from collagemaker.settings import Settings
from collagemaker.utility import apply_fades, offset_mix
from collagemaker.slice import Slice


class Gesture:

    def __init__(self, sample_data: np.ndarray, settings: Settings):

        self.data = None
        self.settings = settings
        self.slice = Slice(sample_data, settings)

        self.compose()

    def compose(self):

        self.data = np.zeros((2, 1))

        repeats = choice(self.settings.gesture.repeats)
        spacing_hold = choice(self.settings.gesture.spacing_hold)

        if spacing_hold:
            space = choice(self.settings.gesture.spacing) / 100
            spacings = [space for _ in range(repeats)]
        else:
            spacings = [choice(self.settings.gesture.spacing) / 100 for _ in range(repeats)]

        # then just add padded slices
        position = 0
        for i in range(repeats):
            rate = choice(self.settings.gesture.slice_rate)
            data = resample(self.slice.data, int(len(self.slice.data[0]) * rate), axis=1)
            self.data = offset_mix(self.data, data, position)
            position += int(len(data[0]) * (1 + spacings[i]))

        self.data = apply_fades(self.data, self.settings.gesture.fades)

        # per-gesture rate change
        self.data = resample(self.data, int(len(self.data[0]) * choice(self.settings.gesture.gesture_rate)), axis=1)
