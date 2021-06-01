from random import randint, choice
from typing import Tuple

import numpy as np

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
        gesture_length = len(self.slc.data) * repeats

        fade_in_length = int(self.fades[0] * gesture_length)
        fade_out_length = int(self.fades[1] * gesture_length)

        fade_in_env = np.linspace(start=0, stop=1, num=fade_in_length)
        fade_in_env = np.append(fade_in_env, np.ones(gesture_length - fade_in_length))

        fade_out_env = np.linspace(start=1, stop=0, num=fade_out_length)
        fade_out_env = np.insert(np.ones(gesture_length - fade_out_length), gesture_length - fade_out_length,
                                 fade_out_env)

        self.data = np.tile(self.slc.data, repeats) * fade_in_env * fade_out_env
