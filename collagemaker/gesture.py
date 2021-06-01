from random import randint

import numpy as np

from collagemaker.slice import Slice


class Gesture:

    def __init__(self, sample_data: np.ndarray, repeat_min: int = 1, repeat_max: int = 10, fade_in: float = 0,
                 fade_out: float = 0):

        self.data = None

        self.slc = Slice(sample_data)

        self.repeat_min = repeat_min
        self.repeat_max = repeat_max
        self.fade_in = fade_in
        self.fade_out = fade_out

        self.compose()

    def compose(self):
        repeats = randint(self.repeat_min, self.repeat_max)
        gesture_length = len(self.slc.data) * repeats

        fade_in_length = int(self.fade_in * gesture_length)
        fade_out_length = int(self.fade_out * gesture_length)

        fade_in_env = np.linspace(start=0, stop=1, num=fade_in_length)
        fade_in_env = np.append(fade_in_env, np.ones(gesture_length - fade_in_length))

        fade_out_env = np.linspace(start=1, stop=0, num=fade_out_length)
        fade_out_env = np.insert(np.ones(gesture_length - fade_out_length), gesture_length - fade_out_length,
                                 fade_out_env)

        self.data = np.tile(self.slc.data, repeats) * fade_in_env * fade_out_env
