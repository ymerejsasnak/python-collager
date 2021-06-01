from random import randint, choice
from typing import Tuple

import numpy as np

from collagemaker.audio import fade
from collagemaker.slice import Slice


class Gesture:

    def __init__(self, sample_data: Tuple[np.ndarray], repeats: range = range(1, 10), fades: Tuple[float] = (0.1, 0.1)):

        self.data = []

        self.slc = Slice(sample_data)

        self.repeats = repeats
        self.fades = fades

        self.compose()

    def compose(self):
        self.data = []

        repeats = choice(self.repeats)

        for ch in range(2):
            self.data.append(fade(np.tile(self.slc.data[ch], repeats), self.fades))
