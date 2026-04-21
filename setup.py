from setuptools import setup

setup(name='mosaic-music',
      version='0.36.0',
      author='mandeep',
      url='https://github.com/mandeep/Mosaic',
      description='A cross-platform cover art focused music player.',
      license='GPLv3+',
      packages=['mosaic', 'mosaic.images'],
      package_data={'mosaic.images': ['*.png'], 'mosaic': ['*.toml']},
      install_requires=[
        'platformdirs',
        'mutagen',
        'toml',
        'natsort',
        'PySide6',
      ],
      extras_require={
        'tests': [
            'pytest',
            'pytest-cov',
            'pytest-qt',
            'pytest-xvfb',
            'pytest-mock',
        ]
      },
      entry_points={
        'gui_scripts': ['mosaic=mosaic.player:main'],
      },
      classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'Programming Language :: Python :: 3.14',
        ]
      )