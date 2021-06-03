from random import choice
from typing import List

import numpy as np


from collagemaker.section import Section
from collagemaker.utility import load_wav_paths, build_sample_pool, export


class Collage:

    def __init__(self, parent_dir: str = 'D:/Samples', sub_dirs: List[str] = None):
        self.sections = {}  # section label/name as key and section object as val
        self.structure = []  # list of section labels in order for piece

        self.paths = load_wav_paths(parent_dir=parent_dir, sub_dirs=sub_dirs)
        self.sample_pool = build_sample_pool(self.paths)

    def create_section(self, name: str, sample_pool_size: int = 10, length: int = 20):

        data_to_use = [choice(self.sample_pool) for _ in range(sample_pool_size)]

        section = Section(data_to_use, length)

        self.sections[name] = section

    def build(self, *section_list):

        self.structure = section_list

        full_length = sum([len(self.sections[section].data) for section in self.structure]) # subtract overlap though
        output_data = np.zeros(shape=(full_length, 2))
        used_sections = []

        overlap = .1
        start = 0

        for section_name in self.structure:

            if section_name in used_sections:
                self.sections[section_name].compose()  # redo the section (currently overlays on existing)
            else:
                used_sections.append(section_name)

            d = self.sections[section_name].data
            d = np.pad(d, pad_width=((start, full_length - (start + len(d))), (0, 0)))
            output_data += d

            start += int(len(self.sections[section_name].data) * (1 - overlap))

        export(output_data)

