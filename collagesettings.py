from pathlib import Path


class CollageSettings:

    def __init__(self):
        self.paths = []

        self.sample_count = 2
        self.output_length = 1000

        # slice length range
        self.length_min = 50
        self.length_max = 100

        self.fade_in = .1  # 0..1  no fade to full length fade
        self.fade_out = .1  # 0..1  no fade to full length fade  (these will overlap if in+out > 1)

        # number of times to repeat slice
        self.repeat_min = 1
        self.repeat_max = 1

        self.iterations = 10

    def load_wav_paths(self, parent_dir='D:/Samples', sub_dirs=None):
        """
        Get all potentially usable *.wav paths in given directory, or specified sub-directories
        
        Arguments:
        parent_dir -- the base directory from which to search (recursively), defaults to D:/Samples (my sample dir)
        sub_dirs -- optionally specify a list of sub directories of parent dir to restrict search to those sub directories (and their children)
        
        Returns:
        all *.wav paths found, as a list of strings
        """

        # if no sub dirs, just use parent path
        if sub_dirs is None:
            sub_dirs = []
        if not sub_dirs:
            p = Path(parent_dir)
            self.paths.extend(list(p.glob('**/*.wav')))

        # otherwise only use add each sub dir
        else:
            for sub in sub_dirs:
                p = Path(parent_dir + '/' + sub)
                self.paths.extend(list(p.glob('**/*.wav')))

    def update_settings(self, settings):
        # get values from dictionary - can omit and will default to already set values   **ideally should check for
        # validity/range
        self.sample_count = settings.get('sample_count', self.sample_count)
        self.output_length = settings.get('output_length', self.output_length)

        self.length_min = settings.get('length_min', self.length_min)
        self.length_max = settings.get('length_max', self.length_max)

        self.fade_in = settings.get('fade_in', self.fade_in)
        self.fade_out = settings.get('fade_out', self.fade_out)

        self.repeat_min = settings.get('repeat_min', self.repeat_min)
        self.repeat_max = settings.get('repeat_max', self.repeat_max)

        self.iterations = settings.get('iterations', self.iterations)
