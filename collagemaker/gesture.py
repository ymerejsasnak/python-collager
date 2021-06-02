from random import choice
from typing import Tuple

import numpy as np

from collagemaker.audio import fade
from collagemaker.slice import Slice


class Gesture:

    def __init__(self, sample_data: np.ndarray, repeats: range = range(1, 10), fades: Tuple[float] = (0.1, 0.1)):

        self.data = None

        self.slc = Slice(sample_data)

        self.repeats = repeats
        self.fades = fades

        self.compose()

    def compose(self):

        repeats = choice(self.repeats)

        self.data = np.tile(self.slc.data, (repeats, 1))
        self.data = fade(self.data, self.fades)
