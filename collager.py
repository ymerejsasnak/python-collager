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
        
        # slice length range
        self.length_min = 50
        self.length_max = 100
        
        self.fade_in = .1  # 0..1  no fade to full length fade
        self.fade_out = .1  # 0..1  no fade to full length fade  (these will overlap if in+out > 1)
        
        # number of times to repeat slice
        self.repeat_min = 1
        self.repeat_max = 1
        
        self.iterations = 10
    
    
    def update_settings(self, settings):
        #get values from dictionary - can omit and will default to already set values   **ideally should check for validity/range
        self.sample_count = settings.get('sample_count', self.sample_count)
        self.output_length = settings.get('output_length', self.output_length)
        
        self.length_min = settings.get('length_min', self.length_min)
        self.length_max = settings.get('length_max', self.length_max)
        
        self.fade_in = settings.get('fade_in', self.fade_in)
        self.fade_out = settings.get('fade_out', self.fade_out)
        
        self.repeat_min = settings.get('repeat_min', self.repeat_min)
        self.repeat_max = settings.get('repeat_max', self.repeat_max)
        
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

        
            if i % (self.iterations // 10) == 0:
                print("{} of {} done".format(i, self.iterations)), 

            sample = choice(self.samples)
            slice_length = randint(self.length_min, self.length_max)


            if len(sample) > slice_length:  # if sample is smaller than slice length, it just uses entire sample
                start = randint(0, len(sample) - slice_length)
                sample = sample[start : start + slice_length]

                
            sample = sample.apply_gain(db_adjust)
                        
           
            if self.fade_in > 0:
                sample = sample.fade_in(int(self.fade_in * slice_length))
                
            if self.fade_out > 0:
                sample = sample.fade_out(int(self.fade_out * slice_length))

            position = randint(0, self.output_length - slice_length)
            repeats = randint(self.repeat_min, self.repeat_max)
            counter = 0
            while counter < repeats and position + slice_length < self.output_length:
                self.collage = self.collage.overlay(sample, position=position)
                position += slice_length
                counter += 1
                

               
        self.collage = normalize(self.collage)
        
        
    
    def export_collage(self, str_prefix=''):
        self.collage.export(datetime.now().strftime(str_prefix + '%m-%d-%Y %H.%M.%S.wav'), format='wav')
    
    
    
    



# normalize slices before applying gain reduction?  
# deal with gain adjustments using rms rather than peak would prob be better

# more settings:  repetitions(min, max?), sound changes(pitch, vol, pan, etc) and fx (filter, bitcrush, etc), reverse %
# sync to bpm option?  -  then have specific algorithms for rhythmic collage vs melodic????

# incorporate freesound stuff (and can use various categories/filters)

# more advanced stuff: feature detection/analysis for more intelligent collaging (note, spectrum, beatdetection, etc)
# ML stuff to identify aspects of a sound?
    



# ideas - recurring sounds (ie create a pool of reusable slices from pool of samples -- even slightly different slices)
        #repetitions, xfade, pitch/vol/pan/filter/etc, overlay %, reverse %, pieces of sounds
#sync to a bpm?  rhythmic and or melodic algorithms?   note/beat detection...etc



# repetition spacing (min/max and hold/random)



test1 = {
    'sample_count': 50,
    'output_length': 30000,
    
    'length_min': 50,
    'length_max': 150,
    'fade_in': 0,
    'fade_out': 1,
    'repeat_min': 5,
    'repeat_max': 20,
    
    'iterations': 100,
}

test2 = {
    'sample_count': 20,
    'output_length': 10000,
    'length_min': 200,
    'length_max': 500,
    'fade_in': .1,
    'fade_out': .1,
    
    'repeat_min': 2,
    'repeat_max': 4,
    
    'iterations': 500,
}



c = CollageMaker()

c.set_paths(get_wav_paths())
c.update_settings(test1)
c.choose_samples()

c.create_collage()
c.export_collage('t1 ')







