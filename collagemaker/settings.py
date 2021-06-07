from collections import namedtuple
from random import randint


class Settings:

    def __init__(self):
        self.text = namedtuple('val', 'val2')

        Collage = namedtuple('Collage',
                             ('parent_dir', 'sub_dirs', 'main_pool_size', 'sections', 'structure', 'overlap'))

        self.collage = Collage(
            parent_dir='D:/Samples',
            sub_dirs=['Surreal Collage Layers'],
            main_pool_size=30,  # size of sample pool for entire collage
            sections=('a', 'b', 'c'),
            structure=('a', 'b', 'c', 'b', 'a'),
            overlap=0.1,  # percentage of section length that overlaps with next (or was it previous?) section
        )

        Section = namedtuple('Section',
                             ('length', 'pool_size', 'motif_count', 'samples_per_motif', 'motif_occurrences',
                              'texture_volume', 'texture_depth'))

        self.section = Section(
            length=range(30, 40),  # seconds (target time, may be longer if motifs end up longer)
            pool_size=range(5, 15),  # size of sample pool for this section
            motif_count=range(5, 15),  # number of unique motifs to generate for this section
            samples_per_motif=range(2, 10),
            motif_occurrences=range(2, 6),  # number of times a motif is reused per section
            texture_volume=range(15, 25),  # int represents %
            texture_depth=range(20, 200),  # number of iterations of sample mixing for texture
        )

        Motif = namedtuple('Motif',
                           ('gesture_count', 'fades'))

        self.motif = Motif(
            gesture_count=range(1, 7),
            fades=(range(0, 50), range(0, 50)),  # fades as percent values since range requires ints
        )

        Gesture = namedtuple('Gesture',
                             ('repeats', 'spacing', 'fades'))

        self.gesture = Gesture(
            repeats=range(1, 20),
            spacing=[randint(-90, 300) for _ in range(5)],  # % of slice length to add as spacing before next repeat
            fades=(range(1, 50), range(1, 50)),

            # fade hold/rand?
            # spacing hold/change (between individual slices)
            # shift % (amount slice changes position/offset each iteration)
        )

        Slice = namedtuple('Slice',
                           ('length', 'fades'))

        self.slice = Slice(
            length=[randint(100, 500) for _ in range(5)],
            fades=(range(1, 75), range(1, 75)),

            # vol (per channel)
            # pan (or part of voluemsnsGA)G
            # pitch

        )


