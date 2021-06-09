from random import choices, randint, choice
from typing import List

import numpy as np

from collagemaker.settings import Settings
from collagemaker.utility import SAMPLES_PER_MS, normalize, offset_mix
from collagemaker.motif import Motif


class Section:

    def __init__(self, samples: List[np.ndarray], settings: Settings):
        self.sample_pool = samples
        self.settings = settings

        self.motifs = []

        length = choice(self.settings.section.length)
        self.data = np.zeros(shape=(2, int(length * 1000 * SAMPLES_PER_MS)))

        self.compose()

    def compose(self):

        samples_per_motif = choice(self.settings.section.samples_per_motif)
        motif_count = choice(self.settings.section.motif_count)

        self.motifs = [Motif(choices(self.sample_pool, k=samples_per_motif), self.settings)
                       for _ in range(motif_count)]

        for motif in self.motifs:

            motif_occurrences = choice(self.settings.section.motif_occurrences)

            for i in range(motif_occurrences):
                start = randint(0, len(self.data[0]) - len(motif.data[0]))
                self.data = offset_mix(self.data, motif.data, start)

        # do texture last because won't be certain about length until then
        self.data = offset_mix(self.data, self.generate_texture(self.data), 0)

    def generate_texture(self, data: np.ndarray):

        # currently same section generates new texture...ok??
        texture_volume = choice(self.settings.section.texture_volume) / 100
        texture_depth = choice(self.settings.section.texture_depth)

        texture = (np.zeros(shape=np.shape(data)))
        texture_length = len(texture[0])

        for i in range(texture_depth):
            sample = choice(self.sample_pool)
            sample_length = len(sample[0])

            # do each channel separately
            for ch in range(2):
                if sample_length > texture_length:
                    offset = randint(0, sample_length - texture_length)
                    data = sample[:, offset: offset + texture_length]
                    data[ch] = np.zeros(len(data[ch]))
                    texture = offset_mix(texture, data, offset)
                else:
                    position = randint(0, texture_length - sample_length)
                    data[ch] = np.zeros(len(data[ch]))
                    texture = offset_mix(texture, data, position)

        return normalize(texture) * texture_volume
