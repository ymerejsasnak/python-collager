from random import choices, randint
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
        self.data = np.zeros(shape=(int(self.settings.section.length * 1000 * SAMPLES_PER_MS), 2))

        self.compose()

    # section maybe handles creation of each lower level for more control of each in a less hierarchical way?

    def compose(self):

        self.motifs = [Motif(choices(self.sample_pool, k=self.settings.section.samples_per_motif), self.settings)
                       for _ in range(self.settings.section.motif_count)]

        for motif in self.motifs:
            for i in range(self.settings.section.motif_occurrences):

                start = randint(0, len(self.data) - len(motif.data))

                data = np.pad(motif.data, pad_width=((start, len(self.data) - (len(motif.data) + start)), (0, 0)))
                self.data += data
