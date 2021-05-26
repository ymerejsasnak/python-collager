from collagemaker import CollageMaker

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


## rework this so its more meta in that you can specific settings for each section of resultant collage 


test1 = {
    'sample_count': 5,
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

c.settings.load_wav_paths()
c.settings.update_settings(test1)

c.choose_samples()
c.create_collage()
c.export_collage('t1 ')







