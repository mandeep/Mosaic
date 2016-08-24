from mosaic import metadata
from mutagen import easyid3, flac, mp3
import pkg_resources
import pytest


@pytest.fixture
def mp3_file():
    file = pkg_resources.resource_filename('mosaic.tests', '01_Ghosts_I_320kb.mp3')
    return file


@pytest.fixture
def flac_file():
    file = pkg_resources.resource_filename('mosaic.tests', '02_Ghosts_I.flac')
    return file


def test_identify_mp3_filetype(mp3_file):
    assert metadata.identify_filetype(mp3_file) == mp3.MP3(mp3_file, ID3=easyid3.EasyID3)


def test_identify_flac_filetype(flac_file):
    assert metadata.identify_filetype(flac_file) == flac.FLAC(flac_file)


def test_mp3_tags(mp3_file):
    assert isinstance(metadata.extract_meta_data(mp3_file), dict)
    assert 'Ghosts I-IV' in metadata.extract_meta_data(mp3_file).values()


def test_flac_tags(flac_file):
    assert isinstance(metadata.extract_meta_data(flac_file), dict)
    assert 'Ghosts I-IV' in metadata.extract_meta_data(flac_file).values()


def test_mp3_metadata(mp3_file):
    data = metadata.metadata(mp3_file)
    assert data[0] == 'Ghosts I-IV'
    assert data[1] == 'Nine Inch Nails'
    assert data[2] == '1 Ghosts I'


def test_flac_metadata(flac_file):
    data = metadata.metadata(flac_file)
    assert data[0] == 'Ghosts I-IV'
    assert data[1] == 'Nine Inch Nails'
    assert data[2] == '2 Ghosts I'
