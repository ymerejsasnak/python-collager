import numpy as np
import pydub
import scipy.io.wavfile
import io

from pydub import AudioSegment
from pydub.effects import normalize

from pathlib import Path
from random import choice
from datetime import datetime

from collagemaker.section import Section

import matplotlib.pyplot as plt


class Collage:
    SAMPLES_PER_MS = 44.1

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

    def build_sample_pool(self, sample_pool_size=20):

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

    def create_section(self, name, sample_pool_size=5, length=10):

        data_to_use = [choice(self.sample_pool) for _ in range(sample_pool_size)]

        section = Section(data_to_use, length)

        self.sections[name] = section

    def build(self, *section_list):
        self.structure = section_list

        output_data = np.empty(0)

        for section in self.structure:
            output_data = np.append(output_data, self.sections[section].data)

        '''
        plot below shows that it seems to work
        just need to normalize to 1 (and convert back to 16/32 bit?)
        then figure out how to get it to export to wav (prob just with scipy, no need for pydub?)
        '''

        output_data /= max(output_data.max(), abs(output_data.min()))

        #plt.xlim((0, len(output_data)))
        #plt.plot(output_data)
        #plt.show()

        filename = 'd:\\CODING\\Python\\Audio\\Collager\\%m-%d-%Y %H.%M.%S.wav'
        scipy.io.wavfile.write(datetime.now().strftime(filename), 44100, output_data)

        # wav_io = io.BytesIO()
        #
        # wav_io.seek(0)
        #
        # out = pydub.AudioSegment.from_wav(wav_io)
        # out = normalize(out)
        #
        # out.export(, format='wav')
