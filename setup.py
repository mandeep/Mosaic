from setuptools import setup

setup(name='mosaic-music',
      version='1.1.14',
      author='Mandeep Bhutani',
      author_email='info@mandeep.xyz',
      url='https://github.com/mandeepbhutani/Mosaic',
      description='A cross-platform cover art focused music player.',
      license='GPL',
      packages=['mosaic', 'mosaic.images', 'mosaic.tests'],
      package_data={'mosaic.images': ['*.png'], 'mosaic': ['*.toml']},
      install_requires=[
        'appdirs==1.4.0',
        'mutagen==1.34',
        'pytoml==0.1.10',
        'natsort==5.0.1'
      ],
      entry_points='''
        [console_scripts]
        mosaic=mosaic.player:main
        ''',
      classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        ]
      )
