from random import choice

import numpy as np
from typing import List, Tuple

from collagemaker.settings import Settings
from collagemaker.utility import apply_fades
from collagemaker.gesture import Gesture


class Motif:

    def __init__(self, sample_pool: List[np.ndarray], settings: Settings):
        self.data = None
        self.settings = settings
        self.sample_pool = sample_pool

        self.gestures = []

        self.compose()

    def compose(self):

        count = choice(self.settings.motif.gesture_count)

        # create gestures
        self.gestures = [Gesture(choice(self.sample_pool), self.settings) for _ in range(count)]

        self.data = [apply_fades(g.data, self.settings.motif.fades) for g in self.gestures]
        self.data = np.concatenate(self.data)
