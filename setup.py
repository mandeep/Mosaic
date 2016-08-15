from setuptools import setup

setup(name='mosaic-music',
      version='1.1.0',
      author='Mandeep Bhutani',
      author_email='info@mandeep.xyz',
      url='https://github.com/mandeepbhutani/Mosaic',
      description='A cross-platform cover art focused music player.',
      packages=['mosaic', 'mosaic.images', 'mosaic.tests'],
      package_data={'mosaic.images': ['*.png'], 'mosaic': ['*.toml']},
      install_requires=[
        'mutagen==1.34',
        'pytoml==0.1.10',
        'appdirs==1.4.0',
      ],
      entry_points='''
        [console_scripts]
        mosaic=mosaic.player:main
        ''',
      )
