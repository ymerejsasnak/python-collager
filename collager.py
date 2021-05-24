from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import normalize

from pathlib import Path
from random import choice, randint
from math import log
from datetime import datetime



def get_wav_paths(parent_dir='D:/Samples', sub_dirs=[]):
    """
    Get all potentially usable *.wav paths in given directory, or specified sub-directories
    
    Arguments:
    parent_dir -- the base directory from which to search (recursively), defaults to D:/Samples (my sample dir)
    sub_dirs -- optionally specify a list of sub directories of parent dir to restrict search to those sub directories (and their children)
    
    Returns:
    all *.wav paths found, as a list of strings
    """

    wav_paths = []

    # no sub dirs, just use parent path
    if sub_dirs == []:
        p = Path(parent_dir)
        wav_paths.extend(list(p.glob('**/*.wav')))

    # otherwise use each sub dir
    else:
        for sub in sub_dirs:
            p = Path(parent_dir + '/' + sub)
            wav_paths.extend(list(p.glob('**/*.wav')))
    
    return wav_paths





  






class CollageMaker:
       
    def __init__(self):
        self.sample_count = 2
        self.output_length = 1000
        
        self.slice_length_min = 50
        self.slice_length_max = 100
        
        self.slice_fade_in = .1  # 0..1  no fade to full length fade
        self.slice_fade_out = .1  # 0..1  no fade to full length fade  (these will overlap if in+out > 1)
        
        self.iterations = 10
    
    
    def update_settings(self, settings):
        #get values from dictionary - can omit and will default to already set values   **ideally should check for validity/range
        self.sample_count = settings.get('sample_count', self.sample_count)
        self.output_length = settings.get('output_length', self.output_length)
        
        self.slice_length_min = settings.get('slice_length_min', self.slice_length_min)
        self.slice_length_max = settings.get('slice_length_max', self.slice_length_max)
        
        self.slice_fade_in = settings.get('slice_fade_in', self.slice_fade_in)
        self.slice_fade_out = settings.get('slice_fade_out', self.slice_fade_out)
        
        self.iterations = settings.get('iterations', self.iterations)

    
    def set_paths(self, paths):
        self.paths = paths
    
    
    def choose_samples(self):

        self.samples = []

        while len(self.samples) < self.sample_count:

            path_choice = str(choice(self.paths))

            try:
                sample = AudioSegment.from_file(path_choice, format='wav')
                self.samples.append(sample)
                print("loaded " + path_choice)

            except Exception:
                print("cannot load " + path_choice)


    def create_collage(self):
        
        self.collage = AudioSegment.silent(self.output_length, frame_rate=44100)

        db_adjust = 20 * log(1 / self.iterations, 10)    # really don't need to reduce gain by this much...maybe base more on rms of each sample?????

        for i in range(self.iterations):

            sample = choice(self.samples)
            slice_length = randint(self.slice_length_min, self.slice_length_max)

            if len(sample) > slice_length:  # if sample is smaller than slice length, it just uses entire sample
                start = randint(0, len(sample) - slice_length)
                sample = sample[start : start + slice_length]
                
            sample = sample.apply_gain(db_adjust)
                        
            sample = sample.fade_in(int(self.slice_fade_in * slice_length)).fade_out(int(self.slice_fade_out * slice_length))
       
            self.collage = self.collage.overlay(sample, position=randint(0, self.output_length - slice_length))
               
        self.collage = normalize(self.collage)
        
        
    
    def export_collage(self):
        self.collage.export(datetime.now().strftime('%m-%d-%Y %H.%M.%S.wav'), format='wav')
    
    
    
    




# ideas - min/max length, recurring sounds, repetitions, xfade, changes(pitch/vol/pan/etc), fx(filter, others), overlay, reverse, pieces of sounds
#sync to a bpm?  rhythmic and or melodic algorithms?   note/beat detection...etc
#normalize slices before adding them



test1 = {
    'sample_count': 5,
    'output_length': 10000,
    'slice_length_min': 50,
    'slice_length_max': 150,
    'slice_fade_in': 0,
    'slice_fade_out': 1,
    'iterations': 100,
}

test2 = {
    'sample_count': 5,
    'output_length': 10000,
    'slice_length_min': 50,
    'slice_length_max': 150,
    'slice_fade_in': 0,
    'slice_fade_out': 1,
    'iterations': 100,
}

test3 = {}


c = CollageMaker()

c.set_paths(get_wav_paths())
c.update_settings(test3)
c.choose_samples()

c.create_collage()
c.export_collage()








