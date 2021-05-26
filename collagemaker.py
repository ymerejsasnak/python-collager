from pydub import AudioSegment
from pydub.effects import normalize

from random import choice, randint
from math import log
from datetime import datetime

from collagesettings import CollageSettings


class CollageMaker:

    def __init__(self):
        self.settings = CollageSettings()
        self.samples = []

    def choose_samples(self):

        while len(self.samples) < self.settings.sample_count:

            path_choice = str(choice(self.settings.paths))

            try:
                sample = AudioSegment.from_file(path_choice, format='wav')
                self.samples.append(sample)
                print("loaded " + path_choice)

            except Exception:
                print("cannot load " + path_choice)

    def create_collage(self):

        self.collage = AudioSegment.silent(self.settings.output_length, frame_rate=44100)

        db_adjust = 20 * log(1 / self.settings.iterations, 10)
        # really don't need to reduce gain by this much...maybe base more on rms of each sample?????

        for i in range(self.settings.iterations):

            if i % (self.settings.iterations // 10) == 0:
                print("{} of {} done".format(i, self.settings.iterations)),

            sample = choice(self.samples)
            slice_length = randint(self.settings.length_min, self.settings.length_max)

            if len(sample) > slice_length:  # if sample is smaller than slice length, it just uses entire sample
                start = randint(0, len(sample) - slice_length)
                sample = sample[start: start + slice_length]

            sample = sample.apply_gain(db_adjust)

            if self.settings.fade_in > 0:
                sample = sample.fade_in(int(self.settings.fade_in * slice_length))

            if self.settings.fade_out > 0:
                sample = sample.fade_out(int(self.settings.fade_out * slice_length))

            position = randint(0, self.settings.output_length - slice_length)
            repeats = randint(self.settings.repeat_min, self.settings.repeat_max)
            counter = 0
            while counter < repeats and position + slice_length < self.settings.output_length:
                self.collage = self.collage.overlay(sample, position=position)
                position += slice_length
                counter += 1

        self.collage = normalize(self.collage)

    def export_collage(self, str_prefix=''):
        self.collage.export(datetime.now().strftime(str_prefix + '%m-%d-%Y %H.%M.%S.wav'), format='wav')
