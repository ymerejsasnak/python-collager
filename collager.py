import collagemaker
from collagemaker.collage import Collage

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

c = Collage()

c.load_wav_paths()
c.build_sample_pool(sample_pool_size=15)

c.create_section('a')
c.create_section('b')
c.build_structure('a', 'b', 'a')

# c.choose_samples()
# c.create_collage()
# c.export_collage()
