from random import choices, randint
from typing import List, Tuple

import numpy as np

from collagemaker.audio import Audio
from collagemaker.motif import Motif


class Section:

    def __init__(self, samples: List[Tuple[np.ndarray]], length: int = 30):
        self.sample_pool = samples
        self.length = length  # in seconds

        self.motifs = []

        self.data = [np.zeros(int(length * 1000 * Audio.SAMPLES_PER_MS)) for _ in range(2)]

        self.compose()
    # section maybe handles creation of each lower level for more control of each in a less hierarchical way?

    def compose(self):

        motif_count = 10
        samples_per_motif = 4
        motif_occurrences = 2

        self.motifs = [Motif(choices(self.sample_pool, k=samples_per_motif)) for _ in range(motif_count)]

        for motif in self.motifs:
            for i in range(motif_occurrences):
                start = randint(0, len(self.data[0]) - len(motif.data[0])) #this was the line that split the stereo
                for ch in range(2):
                    data = np.pad(motif.data[ch], (start, len(self.data[ch]) - (len(motif.data[ch]) + start)))
                    self.data[ch] += data
