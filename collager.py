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





  
def choose_samples(paths, num_to_load=2):
    """
    Choose a number of samples from a given list of sample paths
    Also displays a message on load or on load failure for each sound
    
    **NOTE THAT THERE IS NO CHECK FOR SITUATIONS WHERE NOT ENOUGH FILES CAN BE LOADED!**
    
    Arguments:
    paths -- list of full pathnames of .wav files (typically from get_wav_paths)
    num_to_load -- number of files to load, defaults to 10
    
    Returns:
    a list of samples (pydub AudioSegments)
    """

    samples = []

    while len(samples) < num_to_load:

        path_choice = str(choice(paths))

        try:
            sample = AudioSegment.from_file(path_choice, format='wav')
            samples.append(sample)
            print("loaded " + path_choice)

        except Exception:
            print("cannot load " + path_choice)

    return samples





class CollageMaker:

    self.settings = {
    
    }
    
    self.settings[output_length=
    
    def __init__(self):
        pass
    
    
    def set_samples(self, samples):
        this.samples = samples
    
    
    def collage_settings(settings_dict):
        for k, v in settings_dict:
            self.k = self.kv
    
    
    

def create_collage(samples, output_length=1000, slice_length=100, iterations=10):
    """
    Create a collage by providing a list of AudioSegments, with various optional settings.
    
    
    Arguments:
    output_length --
    slice_count --
    
    
    """
    
    collage = AudioSegment.silent(output_length, frame_rate=44100)

    db_adjust = 20 * log(1/iterations, 10)    # really don't need to reduce gain by this much...maybe base more on rms????

    for i in range(iterations):

        sample = choice(samples)

        if len(sample) > slice_length:
            start = randint(0, len(sample) - slice_length)
            sample = sample[start : start + slice_length]
            
        sample = sample.apply_gain(db_adjust) 
        collage = collage.overlay(sample, position=randint(0, output_length-slice_length))
           
    return collage
    
    
    
    


# ideas - min/max length, recurring sounds, repetitions, xfade, changes(pitch/vol/pan/etc), fx(filter, others), overlay, reverse, pieces of sounds
#sync to a bpm?  rhythmic and or melodic algorithms?   note/beat detection...etc
#normalize slices before adding them

'''
paths = get_wav_paths()
samples = choose_samples(paths)
collage = create_collage(samples)
'''

paths = get_wav_paths(sub_dirs=['FROM TABLET'])
samples = choose_samples(paths, num_to_load=20)
collage = create_collage(samples, output_length=20000, iterations=1000, slice_length=50)

collage = normalize(collage)

collage.export(datetime.now().strftime("%m-%d-%Y %H.%M.%S.wav"), format="wav")   

