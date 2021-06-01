import numpy as np
import scipy.io.wavfile

from pydub import AudioSegment

from pathlib import Path
from random import choice
from datetime import datetime

from collagemaker.section import Section


class Collage:
    SAMPLES_PER_MS = 44.1

    def __init__(self):
        self.paths = []  # all potentially valid wav paths
        self.sample_pool = []
        self.sections = {}  # section label/name as key and section object as val
        self.structure = []  # list of section labels in order for piece

        self.data = None

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

    def build_sample_pool(self, sample_pool_size=30):

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

    def create_section(self, name, sample_pool_size=10, length=20):

        data_to_use = [choice(self.sample_pool) for _ in range(sample_pool_size)]

        section = Section(data_to_use, length)

        self.sections[name] = section

    def build(self, *section_list):
        self.structure = section_list

        output_data = np.empty(0)
        used_sections = []

        for section in self.structure:
            if section in used_sections:
                self.sections[section].compose()  # redo the section
            else:
                used_sections.append(section)
            output_data = np.append(output_data, self.sections[section].data)

        output_data /= max(output_data.max(initial=0), abs(output_data.min(initial=0)))
        self.data = output_data

    def export(self):
        filename = 'd:\\CODING\\Python\\Audio\\Collager\\%m-%d-%Y %H.%M.%S.wav'
        scipy.io.wavfile.write(datetime.now().strftime(filename), 44100, self.data)
