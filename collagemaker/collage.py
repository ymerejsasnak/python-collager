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

        self.data = None

    def create_section(self, name: str, sample_pool_size: int = 10, length: int = 20):

        data_to_use = [choice(self.audio.sample_pool) for _ in range(sample_pool_size)]

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
        self.audio.output_data = output_data

