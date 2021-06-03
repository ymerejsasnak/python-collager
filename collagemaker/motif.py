from random import choice

import numpy as np
from typing import List, Tuple

from collagemaker.utility import apply_fades
from collagemaker.gesture import Gesture


class Motif:

    def __init__(self, sample_pool: List[np.ndarray], counts: range = range(2, 10), fades: Tuple[float] = (0, 0)):
        self.data = None

        self.sample_pool = sample_pool
        self.counts = counts
        self.fades = fades

        self.gestures = []

        self.compose()

    def compose(self):

        count = choice(self.counts)

        # create gestures
        self.gestures = [Gesture(choice(self.sample_pool)) for _ in range(count)]

        self.data = [apply_fades(g.data, self.fades) for g in self.gestures]
        self.data = np.concatenate(self.data)
