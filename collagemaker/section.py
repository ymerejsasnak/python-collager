from random import choices, randint, choice
from typing import List

import numpy as np

from collagemaker.settings import Settings
from collagemaker.utility import normalize, offset_mix
from collagemaker.motif import Motif


class Section:

    def __init__(self, samples: List[np.ndarray], settings: Settings):
        self.sample_pool = samples
        self.settings = settings

        self.motifs = []

        self.data = np.zeros(shape=(2, 1))

        self.compose()

    def compose(self):

        samples_per_motif = choice(self.settings.section.samples_per_motif)
        motif_count = choice(self.settings.section.motif_count)

        self.motifs = [Motif(choices(self.sample_pool, k=samples_per_motif), self.settings)
                       for _ in range(motif_count)]

        for motif in self.motifs:

            motif_occurrences = choice(self.settings.section.motif_occurrences)

            for i in range(motif_occurrences):
                start = randint(0, max(0, len(self.data[0]) - len(motif.data[0])))  # sections are front-heavy because of the way this works right here (slowly grows in size, so becomes more sparse)
                self.data = offset_mix(self.data, motif.data, start)

        # do texture last because won't be certain about length until then
        self.data += self.generate_texture(len(self.data[0]))

    def generate_texture(self, length: int):

        # currently same section generates new texture...ok??
        texture_volume = choice(self.settings.section.texture_volume) / 100
        texture_depth = choice(self.settings.section.texture_depth)

        texture = np.zeros(shape=(2, length))

        for i in range(texture_depth):
            sample = choice(self.sample_pool)
            sample_length = len(sample[0])

            if sample_length > length:
                sample = sample[:, :length]
                sample_length = length

            # shift channels separately
            for ch in range(2):
                temp_data = sample[ch]  # store the opposite channels data
                sample = np.roll(sample, randint(0, sample_length), axis=1)  # shift the samples, wrapping back to beginning
                sample[ch] = temp_data

            offset = randint(0, length - sample_length)

            texture = offset_mix(texture, sample, offset)

        return normalize(texture) * texture_volume
