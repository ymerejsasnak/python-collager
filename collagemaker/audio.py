from typing import List

import numpy as np
import scipy.io.wavfile

from pydub import AudioSegment

from pathlib import Path
from random import choice
from datetime import datetime


class Audio:
    SAMPLES_PER_MS = 44.1

    def __init__(self):
        self.paths = []  # all potentially valid wav paths
        self.sample_pool = []

        self.output_data = None

    def load_wav_paths(self, parent_dir: str, sub_dirs: List[str]):

        # if no sub dirs, just use parent path
        if sub_dirs is None:
            sub_dirs = []
        if not sub_dirs:
            p = Path(parent_dir)
            self.paths.extend(list(p.glob('**/*.wav')))

        # otherwise only use  each sub dir
        else:
            for sub in sub_dirs:
                p = Path(parent_dir + '/' + sub)
                self.paths.extend(list(p.glob('**/*.wav')))

    def build_sample_pool(self, sample_pool_size: int = 30):

        while len(self.sample_pool) < sample_pool_size:

            path_attempt = str(choice(self.paths))

            try:
                seg = AudioSegment.from_file(path_attempt, format='wav')  # could just load w/ scipy
                seg.set_frame_rate(
                    44100)  # can do with audioop.ratecv (thats what pydub uses) -- just need to figure out 'fragment'
                segs = seg.split_to_mono()
                samples = [s.get_array_of_samples() for s in segs]
                data = np.array(samples[0]).T.astype(np.float32)  # just doing left channel for now (samples[0])
                data /= np.iinfo(samples[0].typecode).max
                self.sample_pool.append(data)

                print("loaded " + path_attempt)

            except IOError:
                print("cannot load " + path_attempt)

    def export(self, filename: str = '%m-%d-%Y %H.%M.%S.wav'):
        path = 'd:\\CODING\\Python\\Audio\\Collager\\' + filename
        scipy.io.wavfile.write(datetime.now().strftime(path), 44100, self.output_data)
