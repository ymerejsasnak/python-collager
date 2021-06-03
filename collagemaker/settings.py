from collections import namedtuple


class Settings:

    def __init__(self):
        self.text = namedtuple('val', 'val2')

        Collage = namedtuple('Collage',
                             ('parent_dir', 'sub_dirs', 'main_pool_size', 'sections', 'structure', 'overlap'))

        self.collage = Collage(
            parent_dir='D:/Samples',
            sub_dirs=[],
            main_pool_size=30,
            sections=('a', 'b'),
            structure=('a', 'b', 'a', 'b', 'a'),
            overlap=0.1,
        )

        Section = namedtuple('Section',
                             ('length', 'motif_count', 'samples_per_motif', 'motif_occurrences'))

        self.section = Section(
            length=30,  # seconds
            motif_count=10,
            samples_per_motif=4,
            motif_occurrences=3,
        )

        Motif = namedtuple('Motif',
                           ('gesture_count', 'fades'))

        self.motif = Motif(
            gesture_count=range(2, 10),
            fades=(0, 0),
        )

        Gesture = namedtuple('Gesture',
                             ('repeats', 'fades'))

        self.gesture = Gesture(
            repeats=range(1, 10),
            fades=(0.1, 0.1),
        )

        Slice = namedtuple('Slice',
                           ('length', 'fades'))

        self.slice = Slice(
            length=range(100, 300),
            fades=(0.01, 0.01),
        )
