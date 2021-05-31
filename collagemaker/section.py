from random import choices, randint
from typing import List

import numpy as np

from collagemaker.collage import Collage
from collagemaker.motif import Motif


class Section:

    def __init__(self, samples: List[np.ndarray], name: str, length: int = 10):
        self.sample_pool = samples
        self.name = name
        self.length = length  # in seconds

        self.motifs = []

        self.data = np.zeros(int(length * 1000 * Collage.SAMPLES_PER_MS))

        self.compose()
    # section maybe handles creation of each lower level for more control of each in a less hierarchical way?

    def compose(self):
        # motif count, paste count

        samples = []

        motif_count = 10
        samples_per_motif = 3
        motif_occurrences = 3

        self.motifs = [Motif(choices(self.sample_pool, k=samples_per_motif)) for _ in range(motif_count)]

        for motif in self.motifs:
            for i in range(motif_occurrences):
                start = randint(0, len(self.data) - len(motif.data))
                new_data = np.pad(motif.data, (start, len(self.data) - (len(motif.data) + start)))

                self.data = np.add(self.data, new_data)
