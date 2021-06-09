from random import choice
from typing import List

import numpy as np


from collagemaker.section import Section
from collagemaker.settings import Settings
from collagemaker.utility import load_wav_paths, build_sample_pool, export


class Collage:

    def __init__(self):
        self.settings = Settings()

        self.sections = {}  # section label/name as key and section object as val
        self.structure = self.settings.collage.structure  # list of section labels in order for piece

        self.paths = load_wav_paths(
            parent_dir=self.settings.collage.parent_dir,
            sub_dirs=self.settings.collage.sub_dirs
        )
        self.sample_pool = build_sample_pool(self.paths, self.settings.collage.main_pool_size)

        for section_name in self.settings.collage.sections:
            print('Building section \"' + section_name + '\"...', end="")
            self.create_section(section_name)
            print('done')

    def create_section(self, name: str):

        pool_size = choice(self.settings.section.pool_size)

        data_pool = [choice(self.sample_pool) for _ in range(pool_size)]

        section = Section(data_pool, self.settings)

        self.sections[name] = section

    def build(self):
        print('building collage...')

        full_length = sum([len(self.sections[section].data[0]) for section in self.structure])  # not counting overlap
        output_data = np.zeros(shape=(2, full_length))
        used_sections = []

        overlap = self.settings.collage.overlap
        start = 0

        for section_name in self.structure:
            if section_name in used_sections:
                print('building new section "' + section_name + '"...')
                self.sections[section_name].compose()  # redo the section (currently overlays on existing)
                print('done')
            else:
                used_sections.append(section_name)

            d = self.sections[section_name].data
            # *** fixme
            d = np.pad(d, pad_width=((0, 0), (start, full_length - (start + len(d[0])))))
            output_data += d

            start += int(len(self.sections[section_name].data[0]) * (1 - overlap))

        export(output_data)

