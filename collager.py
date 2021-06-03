import collagemaker.collage as cm

c = cm.Collage()

c.create_section('a')
c.create_section('b')
c.build('a', 'b', 'a', 'b', 'a')



