from setuptools import setup, find_packages

setup(name='Mosaic',
      version='1.0',
      author='Mandeep Bhutani',
      packages=['player', 'player.images'],
      package_data={"player.images": ['*.png']},
      install_requires=[
        'mutagen>=1.34'
      ],
      entry_points='''
        [console_scripts]
        mosaic=player.mosaic:main
        ''',
      )
