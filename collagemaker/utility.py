from typing import List, Tuple

import numpy as np
import scipy.io.wavfile

from pydub import AudioSegment

from pathlib import Path
from random import choice
from datetime import datetime

SAMPLES_PER_MS = 44.1


def apply_fades(data: np.ndarray, fades: Tuple[range]):
    length = len(data[0])

    fade_in_length = int(choice(fades[0])/100 * length)
    fade_out_length = int(choice(fades[1])/100 * length)

    fade_in_env = np.linspace(start=(0, 0), stop=(1, 1), num=fade_in_length, axis=1)
    fade_in_env = np.append(fade_in_env, np.ones((2, length - fade_in_length)), axis=1)

    fade_out_env = np.linspace(start=(1, 1), stop=(0, 0), num=fade_out_length, axis=1)
    fade_out_env = np.append(np.ones((2, length - fade_out_length)), fade_out_env, axis=1)

    return data * fade_in_env * fade_out_env


def load_wav_paths(parent_dir: str, sub_dirs: List[str]):
    paths = []

    # if no sub dirs, just use parent path
    if sub_dirs is None:
        sub_dirs = []
    if not sub_dirs:
        p = Path(parent_dir)
        paths.extend(list(p.glob('**/*.wav')))

    # otherwise only use  each sub dir
    else:
        for sub in sub_dirs:
            p = Path(parent_dir + '/' + sub)
            paths.extend(list(p.glob('**/*.wav')))

    return paths


def build_sample_pool(paths: List[str], sample_pool_size: int = 20):
    sample_pool = []

    while len(sample_pool) < sample_pool_size:

        path_attempt = str(choice(paths))
        seg = None

        try:
            seg = AudioSegment.from_file(path_attempt, format='wav')  # could just load w/ scipy

        except IOError:
            print("cannot load " + path_attempt)

        if seg is not None:
            seg.set_frame_rate(44100)
            # can do with audioop.ratecv (thats what pydub uses) -- just need to figure out 'fragment'
            if seg.channels == 1:
                seg = seg.set_channels(2)
            segs = seg.split_to_mono()
            samples = [s.get_array_of_samples() for s in segs]
            data = np.array(samples).astype(np.float32)
            data /= np.iinfo(samples[0].typecode).max
            sample_pool.append(data)

            print("loaded " + path_attempt)

    return sample_pool


def normalize(data: np.ndarray):
    mx = max(data.max(initial=0), abs(data.min(initial=0)))
    if mx != 0:
        data /= mx
    return data


def export(data: np.ndarray, filename: str = '%m-%d-%Y %H.%M.%S.wav'):
    path = 'd:\\CODING\\Python\\Audio\\Collager\\' + filename

    data = normalize(data)

    scipy.io.wavfile.write(datetime.now().strftime(path), 44100, data.T)


def offset_mix(first: np.ndarray, second: np.ndarray, offset: int):
    """
    Given two arrays, add the second to the first at the given index, padding/extending as necessary.
    Ex:  two arrays of [1, 1, 1, 1] with an offset of 2 = [1, 1, 2, 2, 1, 1]
            [1, 1, 1, 1]
                  [1, 1, 1, 1]

    ***this assumes simple usage to np w/ (x, 2)-shaped arrays***

    :param first:  base array
    :param second:  new array to add to base array
    :param offset:  index at which to begin adding arrays
    :return:
    """

    new_length = max(len(first[0]), len(second[0]) + offset)

    if len(first[0]) < new_length:
        padding = new_length - len(first[0])
        first = np.pad(first, pad_width=((0, 0), (0, padding)))

    pad_before = offset
    pad_after = new_length - (len(second[0]) + offset)
    second = np.pad(second, pad_width=((0, 0), (pad_before, pad_after)))

    return first + second
