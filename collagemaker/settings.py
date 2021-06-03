from collections import namedtuple


class Settings:

    def __init__(self):
        self.text = namedtuple('val', 'val2')

        Collage = namedtuple('Collage',
                             ('parent_dir', 'sub_dirs', 'main_pool_size', 'sections', 'structure', 'overlap'))

        self.collage = Collage(
            parent_dir='D:/Samples',
            sub_dirs=[],
            main_pool_size=30,  # size of sample pool for entire collage
            sections=('a', 'b', 'c'),
            structure=('a', 'b', 'c', 'b', 'a'),
            overlap=0.1,  # percentage of section length that overlaps with next (or was it previous?) section
        )

        Section = namedtuple('Section',
                             ('length', 'pool_size', 'motif_count', 'samples_per_motif', 'motif_occurrences'))

        self.section = Section(
            length=range(30, 50),  # seconds
            pool_size=range(5, 20),  # size of sample pool for this section
            motif_count=range(5, 20),  # number of unique motifs to generate for this section
            samples_per_motif=range(1, 10),
            motif_occurrences=range(1, 5),  # number of times a motif is reused per section
        )

        Motif = namedtuple('Motif',
                           ('gesture_count', 'fades'))

        self.motif = Motif(
            gesture_count=range(2, 10),
            fades=(range(0, 50), range(0, 50)),  # fades as percent values since range requires ints
        )

        Gesture = namedtuple('Gesture',
                             ('repeats', 'fades'))

        self.gesture = Gesture(
            repeats=range(1, 10),
            fades=(range(0, 50), range(0, 50)),
        )

        Slice = namedtuple('Slice',
                           ('length', 'fades'))

        self.slice = Slice(
            length=range(50, 500),
            fades=(range(1, 50), range(1, 50)),
        )
