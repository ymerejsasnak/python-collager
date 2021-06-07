from collections import namedtuple
from random import randint

from numpy.random import uniform


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
            pool_size=range(10, 20),  # size of sample pool for this section
            motif_count=range(4, 15),  # number of unique motifs to generate for this section
            samples_per_motif=range(2, 10),
            motif_occurrences=range(1, 5),  # number of times a motif is reused per section
            texture_volume=range(15, 25),  # int represents %
            texture_depth=range(50, 200),  # number of iterations of sample mixing for texture
        )

        Motif = namedtuple('Motif',
                           ('gesture_count', 'fades'))

        self.motif = Motif(
            gesture_count=range(2, 10),
            fades=(range(0, 50), range(0, 50)),  # fades as percent values since range requires ints
        )

        Gesture = namedtuple('Gesture',
                             ('repeats', 'spacing', 'fades', 'slice_rate', 'gesture_rate'))

        self.gesture = Gesture(
            repeats=range(1, 20),
            spacing=[randint(-90, 300) for _ in range(5)],  # % of slice length to add as spacing before next repeat
            fades=(range(1, 50), range(1, 50)),


            gesture_rate=[uniform(0.6, 1.75) for _ in range(5)],
            slice_rate=[uniform(0.9, 1.1) for _ in range(5)],

            # fade hold/rand?
            # spacing hold/change (between individual slices)
            # shift % (amount slice changes position/offset each iteration)
        )

        Slice = namedtuple('Slice',
                           ('length', 'fades',))

        self.slice = Slice(
            length=[randint(100, 900) for _ in range(5)],
            fades=(range(10, 75), range(10, 75)),

        )


