import collagemaker.collage as cm

c = cm.Collage()

c.load_wav_paths()
c.build_sample_pool()

c.create_section('a')
c.create_section('b')
c.build('a', 'b', 'a')


