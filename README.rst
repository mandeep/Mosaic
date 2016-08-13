.. image:: mosaic/images/album.png

|travis| |coverage|

Mosaic is a cover art focused media player built with Python and the PyQt5 library. The application displays in the main window the cover art of the song currently playing. The goal of the application is to be a media player that allows the user to browse their media library by the cover art of the albums in the library. Supported file formats are MP3 and FLAC.

.. image:: mosaic/images/screen.png

.. image:: mosaic/images/screen2.png

.. image:: mosaic/images/screen3.png

*************
Installation
*************

Mosaic requires Python and the PyQt5 library installed locally. For PyQt5 install instructions please visit: https://www.riverbankcomputing.com/software/pyqt/download5

With your environment set, run the following commands to install Mosaic::

    git clone https://github.com/mandeepbhutani/Mosaic.git
    cd Mosaic
    pip install .

When the package has finished installing, Mosaic can be run with the following command::

    mosaic

.. |travis| image:: https://travis-ci.org/mandeepbhutani/Mosaic.svg?branch=master
    :target: https://travis-ci.org/mandeepbhutani/Mosaic
.. |coverage| image:: https://coveralls.io/repos/github/mandeepbhutani/Mosaic/badge.svg?branch=master :target: https://coveralls.io/github/mandeepbhutani/Mosaic?branch=master


