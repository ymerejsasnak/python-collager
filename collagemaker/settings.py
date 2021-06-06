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
            main_pool_size=20,  # size of sample pool for entire collage
            sections=('a', 'b', 'c'),
            structure=('a', 'b', 'c', 'b', 'a'),
            overlap=0.1,  # percentage of section length that overlaps with next (or was it previous?) section
        )

        Section = namedtuple('Section',
                             ('length', 'pool_size', 'motif_count', 'samples_per_motif', 'motif_occurrences'))

        self.section = Section(
            length=range(30, 45),  # seconds (target time, may be longer if motifs end up longer)
            pool_size=range(5, 10),  # size of sample pool for this section
            motif_count=range(4, 8),  # number of unique motifs to generate for this section
            samples_per_motif=range(2, 6),
            motif_occurrences=range(1, 3),  # number of times a motif is reused per section
        )

        Motif = namedtuple('Motif',
                           ('gesture_count', 'fades'))

        self.motif = Motif(
            gesture_count=range(1, 7),
            fades=(range(0, 5), range(0, 5)),  # fades as percent values since range requires ints
        )

        Gesture = namedtuple('Gesture',
                             ('repeats', 'spacing', 'fades'))

        self.gesture = Gesture(
            repeats=range(2, 9),
            spacing=[randint(-80, 180) for _ in range(5)],  # % of slice length to add as spacing before next repeat
            fades=(range(1, 50), range(1, 50)),

            # fade hold/rand?
            # spacing hold/change (between individual slices)
            # shift % (amount slice changes position/offset each iteration)
        )

        Slice = namedtuple('Slice',
                           ('length', 'fades'))

        self.slice = Slice(
            length=[randint(200, 500) for _ in range(5)],
            fades=(range(1, 50), range(1, 50)),

            # vol (per channel)
            # pan (or part of voluemsnsGA)G
            # pitch

        )


