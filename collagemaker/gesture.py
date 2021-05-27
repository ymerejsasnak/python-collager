class Gesture:

    def __init__(self):
        self.sample_count = 1
        self.output_length = 1000

        # slice length range
        self.length_min = 100
        self.length_max = 100

        self.fade_in = 0  # 0..1  no fade to full length fade
        self.fade_out = 0  # 0..1  no fade to full length fade  (these will overlap if in+out > 1)

        # number of times to repeat slice
        self.repeat_min = 1
        self.repeat_max = 1

        self.iterations = 1