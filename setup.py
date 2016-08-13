from setuptools import setup

setup(name='Mosaic',
      version='1.0.0',
      author='Mandeep Bhutani',
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
