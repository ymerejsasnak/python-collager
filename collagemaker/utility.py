from typing import List, Tuple

import numpy as np
import scipy.io.wavfile

from pydub import AudioSegment

from pathlib import Path
from random import choice
from datetime import datetime

SAMPLES_PER_MS = 44.1


def apply_fades(data: np.ndarray, fades: Tuple[float]):
    length = len(data)

    fade_in_length = int(fades[0] * length)
    fade_out_length = int(fades[1] * length)

    fade_in_env = np.linspace(start=(0, 0), stop=(1, 1), num=fade_in_length)
    fade_in_env = np.append(fade_in_env, np.ones((length - fade_in_length, 2)), axis=0)

    fade_out_env = np.linspace(start=(1, 1), stop=(0, 0), num=fade_out_length)
    fade_out_env = np.insert(np.ones((length - fade_out_length, 2)), length - fade_out_length, fade_out_env, axis=0)

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
            data = np.array(samples).T.astype(np.float32)
            data /= np.iinfo(samples[0].typecode).max
            sample_pool.append(data)

            print("loaded " + path_attempt)

    return sample_pool


def export(data: np.ndarray, filename: str = '%m-%d-%Y %H.%M.%S.wav'):
    path = 'd:\\CODING\\Python\\Audio\\Collager\\' + filename

    # normalize
    mx = max(data.max(initial=0), abs(data.min(initial=0)))
    if mx != 0:
        data /= mx

    scipy.io.wavfile.write(datetime.now().strftime(path), 44100, np.array(data))
