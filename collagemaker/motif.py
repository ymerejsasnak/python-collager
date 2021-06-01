from random import randint, choice

import numpy as np
from typing import List

from collagemaker.gesture import Gesture


class Motif:

    def __init__(self, sample_pool: List[np.ndarray], gestures_min: int = 2, gestures_max: int = 10, fade_in: float = 0,
                 fade_out: float = 0):
        self.data = None

        self.sample_pool = sample_pool
        self.gestures_min = gestures_min
        self.gestures_max = gestures_max
        self.fade_in = fade_in
        self.fade_out = fade_out

        self.gestures = []

        self.compose()

    def compose(self):
        gesture_count = randint(self.gestures_min, self.gestures_max)

        # create gestures
        self.gestures = [Gesture(choice(self.sample_pool)) for _ in range(gesture_count)]

        motif_length = sum([len(g.data) for g in self.gestures])

        fade_in_length = int(self.fade_in * motif_length)
        fade_out_length = int(self.fade_out * motif_length)

        fade_in_env = np.linspace(start=0, stop=1, num=fade_in_length)
        fade_in_env = np.append(fade_in_env, np.ones(motif_length - fade_in_length))

        fade_out_env = np.linspace(start=1, stop=0, num=fade_out_length)
        fade_out_env = np.insert(np.ones(motif_length - fade_out_length), motif_length - fade_out_length,
                                 fade_out_env)

        gesture_data = [g.data for g in self.gestures]
        self.data = np.concatenate(gesture_data) * fade_in_env * fade_out_env
