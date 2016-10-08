import pkg_resources

from mutagen import easyid3, flac, mp3

from PyQt5.QtCore import QByteArray


def identify_filetype(file):
    """Identify the given file as either MP3 or FLAC and return a Mutagen object."""
    if file.endswith('.mp3'):
        audio_file = mp3.MP3(file, ID3=easyid3.EasyID3)

    elif file.endswith('.flac'):
        audio_file = flac.FLAC(file)

    return audio_file


def extract_metadata(file):
    """Extract all of the metadata embedded within the audio file.

    Creates a dictionary with the tag and data pairs so that the MP3 and FLAC
    tags are in the same dictionary.
    """
    audio_file = identify_filetype(file)

    # Mutagen returns None if there is no metadata embedded within a file
    if audio_file.tags is None:
        return {}

    tags_dictionary = dict(audio_file.tags)
    metadata_dictionary = dict((k, "".join(v)) for k, v in tags_dictionary.items())
    return metadata_dictionary


def metadata(file):
    """Create a list of all the media file's extracted metadata."""
    audio_file = identify_filetype(file)
    file_metadata = extract_metadata(file)

    album = file_metadata.get('album', '??')
    artist = file_metadata.get('artist', '??')
    title = file_metadata.get('title', '??')
    track_number = file_metadata.get('tracknumber', '??')
    date = file_metadata.get('date', '')
    genre = file_metadata.get('genre', '')
    description = file_metadata.get('description', '')
    sample_rate = "{} Hz" .format(audio_file.info.sample_rate)
    artwork = pkg_resources.resource_filename('mosaic.images', 'nocover.png')

    try:  # Bitrate only applies to mp3 files
        bitrate = "{} kb/s" .format(audio_file.info.bitrate // 1000)
        bitrate_mode = "{}" .format(audio_file.info.bitrate_mode)
    except AttributeError:
        bitrate = ''
        bitrate_mode = ''
    try:  # Bits per sample only applies to flac files
        bits_per_sample = "{}" .format(audio_file.info.bits_per_sample)
    except AttributeError:
        bits_per_sample = ''

    try:  # Searches for cover art in flac files
        artwork = QByteArray().append(audio_file.pictures[0].data)
    except (IndexError, flac.FLACNoHeaderError):
        artwork = pkg_resources.resource_filename('mosaic.images', 'nocover.png')
    except AttributeError:  # Searches for cover art in mp3 files
        for tag in mp3.MP3(file):
            if 'APIC' in tag:
                artwork = QByteArray().append(mp3.MP3(file)[tag].data)

    return [album, artist, title, track_number, date, genre, description, sample_rate,
            bitrate, bitrate_mode, bits_per_sample, artwork]
