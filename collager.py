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
        self.settings = {
            'number_to_load': 2,
            'output_length': 1000,
            'slice_length': 100,
            'iterations': 10,
        }
    
    
    def set_paths(self, paths):
        self.paths = paths
    
    
    def choose_samples(self):
        """
       
        """

        self.samples = []

        while len(self.samples) < self.settings['number_to_load']:

            path_choice = str(choice(self.paths))

            try:
                sample = AudioSegment.from_file(path_choice, format='wav')
                self.samples.append(sample)
                print("loaded " + path_choice)

            except Exception:
                print("cannot load " + path_choice)

    
    def update_settings(self, new_settings):
        for k, v in new_settings:
            self.settings[k] = v or self.settings[k]
    
    
    

    def create_collage(self):
        """
             
        """
        
        self.collage = AudioSegment.silent(self.settings['output_length'], frame_rate=44100)

        db_adjust = 20 * log(1/self.settings['iterations'], 10)    # really don't need to reduce gain by this much...maybe base more on rms????

        for i in range(self.settings['iterations']):

            sample = choice(self.samples)

            if len(sample) > self.settings['slice_length']:
                start = randint(0, len(sample) - self.settings['slice_length'])
                sample = sample[start : start + self.settings['slice_length']]
                
            sample = sample.apply_gain(db_adjust) 
            self.collage = self.collage.overlay(sample, position=randint(0, self.settings['output_length']-self.settings['slice_length']))
               
        self.collage = normalize(self.collage)
        
        
    
    def export_collage(self):
        self.collage.export(datetime.now().strftime('%m-%d-%Y %H.%M.%S.wav'), format='wav')
    
    
    
    




# ideas - min/max length, recurring sounds, repetitions, xfade, changes(pitch/vol/pan/etc), fx(filter, others), overlay, reverse, pieces of sounds
#sync to a bpm?  rhythmic and or melodic algorithms?   note/beat detection...etc
#normalize slices before adding them




c = CollageMaker()
c.set_paths(get_wav_paths())
c.choose_samples()
c.create_collage()
c.export_collage()








