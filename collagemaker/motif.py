from random import randint, choice

import numpy as np
from typing import List, Tuple

from collagemaker.audio import fade
from collagemaker.gesture import Gesture


class Motif:

    def __init__(self, sample_pool: List[Tuple[np.ndarray]], counts: range = range(2, 10), fades: Tuple[float] = (0, 0)):
        self.data = []

        self.sample_pool = sample_pool
        self.counts = counts
        self.fades = fades

        self.gestures = []

        self.compose()

    def compose(self):
        self.data = []

        count = choice(self.counts)

        # create gestures
        self.gestures = [Gesture(choice(self.sample_pool)) for _ in range(count)]

        for ch in range(2):
            gesture_data = [fade(g.data[ch], self.fades) for g in self.gestures]
            self.data.append(np.concatenate(gesture_data))
