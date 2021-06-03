from random import choices, randint, choice
from typing import List

import numpy as np

from collagemaker.settings import Settings
from collagemaker.utility import SAMPLES_PER_MS
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

                start = randint(0, len(self.data) - len(motif.data))

                data = np.pad(motif.data, pad_width=((start, len(self.data) - (len(motif.data) + start)), (0, 0)))
                self.data += data
