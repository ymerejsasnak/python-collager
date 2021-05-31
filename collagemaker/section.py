class Section:

    def __init__(self, samples, length):

        self.sample_pool = samples

        self.length = length    # in seconds
        self.fade_in = 0        # 0..1 of length
        self.fade_out = 0       # 0..1 of length

        # build these similarly to collage building sections?
        self.motifs = []        # collections of gestures
        self.gestures = []      # free gestures not part of a motif




    def create_section(self, name, sample_pool_size=5, length=1):
        samples = []

        for i in range(sample_pool_size):
            samples.append(choice(self.sample_pool))

        section = Section(samples, length)
        self.sections[name] = section

