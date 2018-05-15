from setuptools import setup

setup(name='mosaic-music',
      version='0.28.1',
      author='Mandeep Bhutani',
      author_email='mandeep@keemail.me',
      url='https://github.com/mandeep/Mosaic',
      description='A cross-platform cover art focused music player.',
      license='GPLv3+',
      packages=['mosaic', 'mosaic.images'],
      package_data={'mosaic.images': ['*.png'], 'mosaic': ['*.toml']},
      install_requires=[
        'importlib_resources>=0.5',
        'appdirs>=1.4.0',
        'mutagen>=1.37',
        'toml>=0.9.2',
        'natsort>=5.0.1'
      ],
      entry_points='''
        [console_scripts]
        mosaic=mosaic.player:main
        ''',
      classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        ]
      )
