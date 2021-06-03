class Settings:

    def __init__(self):

        self.collage = {
            'parent_dir': 'D:/Samples',
            'sub_dirs': [],
            'main_pool_size': 30,
            'sections': ('a', 'b'),
            'structure': ('a', 'b', 'a', 'b', 'a'),
            'overlap': 0.1,  # % of section length
        }

        self.section = {
            'length': 30,  # seconds
            'motif_count': 10,
            'samples_per_motif': 4,
            'motif_occurrences': 3,
        }

        self.motif = {
            'gesture_count': range(2, 10),
            'fades': (0, 0),
        }

        self.gesture = {
            'repeats': range(1, 10),
            'fades': (0.1, 0.1),
        }

        self.slice = {
            'length': range(100, 300),
            'fades': (0.01, 0.01),
        }

