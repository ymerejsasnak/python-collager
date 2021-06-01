from random import randint, choice

import numpy as np
from typing import List, Tuple

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

        motif_length = sum([len(g.data[0]) for g in self.gestures])

        fade_in_length = int(self.fades[0] * motif_length)
        fade_out_length = int(self.fades[1] * motif_length)

        fade_in_env = np.linspace(start=0, stop=1, num=fade_in_length)
        fade_in_env = np.append(fade_in_env, np.ones(motif_length - fade_in_length))

        fade_out_env = np.linspace(start=1, stop=0, num=fade_out_length)
        fade_out_env = np.insert(np.ones(motif_length - fade_out_length), motif_length - fade_out_length,
                                 fade_out_env)

        for ch in range(2):
            gesture_data = [g.data[ch] for g in self.gestures]
            self.data.append(np.concatenate(gesture_data) * fade_in_env * fade_out_env)
