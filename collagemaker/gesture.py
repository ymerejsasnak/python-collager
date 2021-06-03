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
        self.slc = Slice(sample_data, settings)

        self.compose()

    def compose(self):

        repeats = choice(self.settings.gesture.repeats)

        self.data = np.tile(self.slc.data, (repeats, 1))
        self.data = apply_fades(self.data, self.settings.gesture.fades)
