from collagemaker.collage import Collage

c = Collage()

c.load_wav_paths()
c.build_sample_pool(sample_pool_size=15)

c.create_section('a')
c.create_section('b')
c.build_structure('a', 'b', 'a')

# c.create_collage()
# c.export_collage()
