from random import choices, randint, choice
from typing import List

import numpy as np

from collagemaker.settings import Settings
from collagemaker.utility import SAMPLES_PER_MS, normalize
from collagemaker.motif import Motif


class Section:

    def __init__(self, samples: List[np.ndarray], settings: Settings):
        self.sample_pool = samples
        self.settings = settings

        self.motifs = []

        length = choice(self.settings.section.length)
        self.data = np.zeros(shape=(int(length * 1000 * SAMPLES_PER_MS), 2))

        self.compose()

    # section maybe handles creation of each lower level for more control of each in a less hierarchical way?

    def compose(self):

        # this would be where to choose to clear existing data first (from same section made previously)

        samples_per_motif = choice(self.settings.section.samples_per_motif)
        motif_count = choice(self.settings.section.motif_count)

        self.motifs = [Motif(choices(self.sample_pool, k=samples_per_motif), self.settings)
                       for _ in range(motif_count)]

        for motif in self.motifs:

            motif_occurrences = choice(self.settings.section.motif_occurrences)

            for i in range(motif_occurrences):

                # increase data size if new motif is longer than existing data (due to gesture repeats/spacing/etc)
                if len(motif.data) > len(self.data):
                    self.data = np.pad(self.data, ((0, len(motif.data) - len(self.data)), (0, 0)))

                start = randint(0, len(self.data) - len(motif.data))

                data = np.pad(motif.data, pad_width=((start, len(self.data) - (len(motif.data) + start)), (0, 0)))
                self.data += data

        # do texture last because won't be certain about length until then
        self.data += self.generate_texture(self.data)

    def generate_texture(self, data: np.ndarray):

        # currently same section generates new texture...ok??
        texture_volume = choice(self.settings.section.texture_volume) / 100
        texture_depth = choice(self.settings.section.texture_depth)

        texture = (np.zeros(shape=np.shape(data)))

        for i in range(texture_depth):
            sample = choice(self.sample_pool)

            for ch in range(2):
                if len(sample) > len(texture):
                    offset = randint(0, len(sample) - len(texture))
                    data = sample[offset: offset + len(texture)]
                    data = data.T
                    data[ch] = np.zeros(len(data[ch]))
                    data = data.T
                    texture += data
                else:
                    position = randint(0, len(texture) - len(sample))
                    data = np.pad(sample, pad_width=((position, len(texture) - (len(sample) + position)), (0, 0)))
                    data = data.T
                    data[ch] = np.zeros(len(data[ch]))
                    data = data.T
                    texture += data

        return normalize(texture) * texture_volume
