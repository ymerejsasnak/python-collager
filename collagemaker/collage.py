from random import choice
from typing import List

import numpy as np

from collagemaker.section import Section
from collagemaker.audio import Audio


class Collage:

    def __init__(self, parent_dir: str = 'D:/Samples', sub_dirs: List[str] = None):
        self.sections = {}  # section label/name as key and section object as val
        self.structure = []  # list of section labels in order for piece

        self.audio = Audio()
        self.audio.load_wav_paths(parent_dir=parent_dir, sub_dirs=sub_dirs)
        self.audio.build_sample_pool()

    def create_section(self, name: str, sample_pool_size: int = 10, length: int = 20):

        data_to_use = [choice(self.audio.sample_pool) for _ in range(sample_pool_size)]

        section = Section(data_to_use, length)

        self.sections[name] = section

    def build(self, *section_list):

        self.structure = section_list

        full_length = sum([len(self.sections[section].data[0]) for section in self.structure])
        output_data = [np.zeros(full_length), np.zeros(full_length)]
        used_sections = []

        overlap = .1
        start = 0

        for section in self.structure:

            if section in used_sections:
                self.sections[section].compose()  # redo the section
            else:
                used_sections.append(section)

            for ch in range(2):
                d = self.sections[section].data[ch]
                d = np.pad(d, (start, full_length - (start + len(d))))
                output_data[ch] += d

            start += int(len(self.sections[section].data[0]) * (1 - overlap))

        self.audio.output_data = output_data

