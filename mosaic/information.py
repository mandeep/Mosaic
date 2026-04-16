from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (QDialog, QHBoxLayout, QLabel, QLineEdit, QTabWidget, QTableWidget,
                             QTableWidgetItem, QTextEdit, QVBoxLayout, QWidget)

from mosaic import metadata, utilities


class GeneralInformation(QWidget):
    """MediaInformation houses all of the widgets and layouts in order to show general metadata."""

    def __init__(self, file=None, parent=None):
        """Initialize the widgets and layouts needed to create a dialog."""
        super(GeneralInformation, self).__init__(parent)

        if file is not None:
            (album, artist, title, track_number, date, genre, description, sample_rate,
             bitrate, bitrate_mode, bits_per_sample, *__) = metadata.metadata(file)

            artist_info = QHBoxLayout()
            artist_info.addLayout(self.info_field('Artist', artist))
            artist_info.addLayout(self.info_field('Album', album))
            artist_info.addLayout(self.info_field('Album Date', date))
            artist_info.addStretch(1)

            song_info = QHBoxLayout()
            song_info.addLayout(self.info_field('Track Title', title))
            song_info.addLayout(self.info_field('Track Number', track_number))
            song_info.addLayout(self.info_field('Genre', genre))
            song_info.addStretch(1)

            audio_info = QHBoxLayout()
            audio_info.addLayout(self.info_field('Bitrate', bitrate))
            audio_info.addLayout(self.info_field('Bitrate Mode', bitrate_mode))
            audio_info.addLayout(self.info_field('Sample Rate', sample_rate))
            audio_info.addLayout(self.info_field('Bits Per Sample', bits_per_sample))
            audio_info.addStretch(1)

            audio_description_label = QLabel('Description', self)
            audio_description_label.setStyleSheet('font-weight: bold')
            audio_description_line = QTextEdit()
            audio_description_line.setText(description)
            audio_description_line.setReadOnly(True)
            song_description = QVBoxLayout()
            song_description.addWidget(audio_description_label)
            song_description.addWidget(audio_description_line)

            media_information_layout = QVBoxLayout()
            media_information_layout.addLayout(artist_info)
            media_information_layout.addLayout(song_info)
            media_information_layout.addLayout(audio_info)
            media_information_layout.addLayout(song_description)
            media_information_layout.addStretch(1)

            self.setLayout(media_information_layout)

    def info_field(self, label_text, value, fixed_width=None):
        """Create a labeled read-only line edit sized to fit its content."""
        label = QLabel(label_text, self)
        label.setStyleSheet('font-weight: bold')
        line = QLineEdit()
        line.setText(value)
        line.setReadOnly(True)
        width = fixed_width or line.fontMetrics().horizontalAdvance(value) + 20
        width = max(width, 50)
        line.setMinimumWidth(width)
        line.setMaximumWidth(width)

        box = QVBoxLayout()
        box.addWidget(label)
        box.addWidget(line)

        return box


class FullInformation(QWidget):
    """Abstract class that provides a table with two columns.

    One column for the current audio file's metadata tags and one column for the
    values of the tags.
    """

    def __init__(self, file=None, parent=None):
        """Provide data on every tag embedded within the audio file."""
        super(FullInformation, self).__init__(parent)

        table_layout = QHBoxLayout()
        table = QTableWidget()
        table.setColumnCount(2)
        table.setColumnWidth(0, 270)
        table.setColumnWidth(1, 270)

        if file is not None:
            file = metadata.extract_metadata(file)
            table.setRowCount(len(file))
            for i, (tag, data) in enumerate(sorted(file.items())):
                table.setItem(i, 0, QTableWidgetItem(tag))
                table.setItem(i, 1, QTableWidgetItem(', '.join(data)))

        table_layout.addWidget(table)

        self.setLayout(table_layout)


class InformationDialog(QDialog):
    """InformationDialog displays a dialog containing tabs for metadata."""

    def __init__(self, file=None, parent=None):
        """Initialize QTabWidget with tabs for each metadata page."""
        super(InformationDialog, self).__init__(parent)
        self.setWindowTitle('Media Information')

        info_icon = utilities.resource_filename('mosaic.images', 'md_info.png')
        self.setWindowIcon(QIcon(info_icon))

        media_information = GeneralInformation(file)
        metadata_information = FullInformation(file)

        page = QTabWidget()
        page.addTab(media_information, 'General')
        page.addTab(metadata_information, 'Metadata')

        dialog_layout = QHBoxLayout()
        dialog_layout.addWidget(page)

        self.setLayout(dialog_layout)
