from PyQt5.QtWidgets import (QHBoxLayout, QLabel, QLineEdit,
                             QTextEdit, QVBoxLayout, QWidget)


class MediaInformation(QWidget):
    """MediaInformation houses all of the widgets and layouts necessary
    to create a dialog filled with audio metadata."""

    def __init__(self, artist, album, date, title, number, genre, bitrate,
                 bitrate_mode, sample_rate, bits_per_sample,
                 description, parent=None):
        """Initializes the widgets and layouts needed to create a
        dialog containing audio metadata."""
        super(MediaInformation, self).__init__(parent)

        artist_label = QLabel('Artist', self)
        artist_line = QLineEdit()
        artist_line.setText(artist)
        artist_line.setReadOnly(True)
        artist_box = QVBoxLayout()
        artist_box.addWidget(artist_label)
        artist_box.addWidget(artist_line)

        album_label = QLabel('Album', self)
        album_line = QLineEdit()
        album_line.setText(album)
        album_line.setReadOnly(True)
        album_box = QVBoxLayout()
        album_box.addWidget(album_label)
        album_box.addWidget(album_line)

        album_date_label = QLabel('Album Date', self)
        album_date_line = QLineEdit()
        album_date_line.setText(date)
        album_date_line.setReadOnly(True)
        album_date_line.setFixedWidth(70)
        date_box = QVBoxLayout()
        date_box.addWidget(album_date_label)
        date_box.addWidget(album_date_line)

        track_label = QLabel('Track Title', self)
        track_line = QLineEdit()
        track_line.setText(title)
        track_line.setReadOnly(True)
        track_box = QVBoxLayout()
        track_box.addWidget(track_label)
        track_box.addWidget(track_line)

        track_number_label = QLabel('Track Number', self)
        track_number_line = QLineEdit()
        track_number_line.setText(number)
        track_number_line.setReadOnly(True)
        track_number_line.setFixedWidth(80)
        number_box = QVBoxLayout()
        number_box.addWidget(track_number_label)
        number_box.addWidget(track_number_line)

        genre_label = QLabel('Genre', self)
        genre_line = QLineEdit()
        genre_line.setText(genre)
        genre_line.setReadOnly(True)
        genre_line.setFixedWidth(100)
        genre_box = QVBoxLayout()
        genre_box.addWidget(genre_label)
        genre_box.addWidget(genre_line)

        bitrate_label = QLabel('Bitrate', self)
        bitrate_line = QLineEdit()
        bitrate_line.setText(bitrate)
        bitrate_line.setReadOnly(True)
        bitrate_line.setFixedWidth(70)
        bitrate_box = QVBoxLayout()
        bitrate_box.addWidget(bitrate_label)
        bitrate_box.addWidget(bitrate_line)

        bitrate_mode_label = QLabel('Bitrate Mode', self)
        bitrate_mode_line = QLineEdit()
        bitrate_mode_line.setText(bitrate_mode)
        bitrate_mode_line.setReadOnly(True)
        bitrate_mode_box = QVBoxLayout()
        bitrate_mode_box.addWidget(bitrate_mode_label)
        bitrate_mode_box.addWidget(bitrate_mode_line)

        sample_rate_label = QLabel('Sample Rate', self)
        sample_rate_line = QLineEdit()
        sample_rate_line.setText(sample_rate)
        sample_rate_line.setReadOnly(True)
        sample_rate_box = QVBoxLayout()
        sample_rate_box.addWidget(sample_rate_label)
        sample_rate_box.addWidget(sample_rate_line)

        bits_per_sample_label = QLabel('Bits Per Sample', self)
        bits_per_sample_line = QLineEdit()
        bits_per_sample_line.setText(bits_per_sample)
        bits_per_sample_line.setReadOnly(True)
        bits_per_sample_box = QVBoxLayout()
        bits_per_sample_box.addWidget(bits_per_sample_label)
        bits_per_sample_box.addWidget(bits_per_sample_line)

        audio_description_label = QLabel('Description')
        audio_description_line = QTextEdit()
        audio_description_line.setText(description)
        audio_description_line.setReadOnly(True)
        audio_description_box = QVBoxLayout()
        audio_description_box.addWidget(audio_description_label)
        audio_description_box.addWidget(audio_description_line)

        artist_info = QHBoxLayout()
        artist_info.addLayout(artist_box)
        artist_info.addLayout(album_box)
        artist_info.addLayout(date_box)

        song_info = QHBoxLayout()
        song_info.addLayout(track_box)
        song_info.addLayout(number_box)
        song_info.addLayout(genre_box)

        audio_info = QHBoxLayout()
        audio_info.addLayout(bitrate_box)
        audio_info.addLayout(bitrate_mode_box)
        audio_info.addLayout(sample_rate_box)
        audio_info.addLayout(bits_per_sample_box)

        song_description = QHBoxLayout()
        song_description.addLayout(audio_description_box)

        media_information_layout = QVBoxLayout()
        media_information_layout.addLayout(artist_info)
        media_information_layout.addLayout(song_info)
        media_information_layout.addLayout(audio_info)
        media_information_layout.addLayout(song_description)
        media_information_layout.addStretch(1)

        self.setLayout(media_information_layout)
