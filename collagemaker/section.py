class Section:

    def __init__(self):
        self.length = 1  # in seconds
        self.fade_in = 0  # 0..1
        self.fade_out = 0  # 0..1

        self.motifs = []  # collections of gestures
        self.gestures = []  # free gestures not part of a motif
