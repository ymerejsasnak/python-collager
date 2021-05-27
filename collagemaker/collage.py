from pydub import AudioSegment
from pydub.effects import normalize

from pathlib import Path
from random import choice, randint
from math import log
from datetime import datetime

from collagemaker.section import Section


class Collage:

    def __init__(self):
        self.paths = []  # all potentially valid wav paths
        self.sample_pool = []
        self.sections = {}  # section label/name as key and section object as val
        self.structure = []  # list of section labels in order for piece

    def load_wav_paths(self, parent_dir='D:/Samples', sub_dirs=None):

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

    def build_sample_pool(self, sample_pool_size=5):

        while len(self.sample_pool) < sample_pool_size:

            path_attempt = str(choice(self.paths))

            try:
                sample = AudioSegment.from_file(path_attempt, format='wav')
                self.sample_pool.append(sample)
                print("loaded " + path_attempt)

            except Exception:
                print("cannot load " + path_attempt)

    def create_section(self, name, sample_pool_size=5, length=1):

        samples = []

        for i in range(sample_pool_size):
            samples.append(choice(self.sample_pool))

        section = Section(samples, length)
        self.sections[name] = section

    def build_structure(self, structure):
        self.structure = structure
