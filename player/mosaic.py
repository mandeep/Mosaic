import sys
import mutagen
import mutagen.flac
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QMainWindow, QApplication, QToolBar,
                             QAction, QFileDialog, QLabel)
from PyQt5.QtCore import Qt, QUrl, QByteArray


class MusicPlayer(QMainWindow):

    def __init__(self, parent=None):
        """Initializes the QMainWindow widget and calls methods that house
        other widgets that need to be displayed in the main window.
        """
        QMainWindow.__init__(self, parent)

        self.player = QMediaPlayer()
        self.setWindowTitle('Mosaic')

        self.player.metaDataChanged.connect(self.retrieve_meta_data)

        self.art = QLabel(self)
        self.setCentralWidget(self.art)

        self.setWindowIcon(QIcon('images/icon.png'))

        self.filename = None

        self.menu_controls()
        self.media_controls()

        self.file_menu()

        self.retrieve_meta_data()

        self.setFixedSize(900, 952)

    def menu_controls(self):
        """Initiates the menu bar and adds it to the QMainWindow widget.
        """
        self.menu = self.menuBar()
        self.file = self.menu.addMenu('File')

    def media_controls(self):
        """Creates the bottom toolbar and controls used for media playback.
        """
        self.toolbar = QToolBar()
        self.addToolBar(Qt.BottomToolBarArea, self.toolbar)
        self.toolbar.setMovable(False)

        self.play_action = QAction(QIcon().fromTheme('media-playback-start'), 'Play', self)
        self.play_action.triggered.connect(self.player.play)

        self.pause_action = QAction(QIcon().fromTheme('media-playback-pause'), 'Pause', self)
        self.pause_action.triggered.connect(self.player.pause)

        self.stop_action = QAction(QIcon().fromTheme('media-playback-stop'), 'Stop', self)
        self.stop_action.triggered.connect(self.player.stop)

        self.toolbar.addAction(self.play_action)
        self.toolbar.addAction(self.pause_action)
        self.toolbar.addAction(self.stop_action)

    def file_menu(self):
        """Adds a file menu to the menu bar. Allows the user to choose actions
        related to audio files."""
        self.open_action = QAction('Open file', self)
        self.open_action.setStatusTip('Add an audio file to an empty playlist.')
        self.open_action.setShortcut('CTRL+O')
        self.open_action.triggered.connect(self.open_file)

        self.file.addAction(self.open_action)

    def open_file(self):
        """Retrieves the path of a file and adds it to a new playlist.
        """
        self.filename, ok = QFileDialog.getOpenFileName(self, 'Open file')
        if ok:
            self.player.setMedia(QMediaContent(QUrl().fromLocalFile(self.filename)))
            self.player.play()

    def retrieve_meta_data(self):
        """QPixmap() is initiated in order to send an image to QLabel() which then
        displays the image in QMainWindow. When a file is loaded, this function
        affirms that meta data in the audio file exists. The mutagen library is
        imported to retrieve cover art from the meta data. Mp3s and FLAC audio
        formats house pictures differently, so two different methods are used
        to extract the meta data. Once the data (in bytes) is retrieved from
        the audio file, it is appeneded to a QByteArray() which allows the
        data to be passed to QPixmap(). Once QPixmap() receives the data,
        the application's height and width are changed to match that of the
        cover art image.
        """
        self.pixmap = QPixmap()
        self.byte_array = QByteArray()

        if self.player.isMetaDataAvailable() and self.filename:
            if self.filename.endswith('mp3'):
                song = mutagen.File(self.filename)
                try:
                    artwork = self.byte_array.append(song.tags['APIC:'].data)
                    self.pixmap.loadFromData(artwork)
                except KeyError:
                    self.pixmap = QPixmap('images/nocover.png', 'png')
                try:
                    album_title = song.tags['TALB']
                    album_artist = song.tags['TPE1']
                    track_title = song.tags['TIT2']
                    self.setWindowTitle('{} - {} - {}' .format(album_artist, album_title, track_title))
                except KeyError:
                    pass
            elif self.filename.endswith('flac'):
                song = mutagen.flac.FLAC(self.filename)
                try:
                    artwork = self.byte_array.append(song.pictures[0].data)
                    self.pixmap.loadFromData(artwork)
                except IndexError:
                    self.pixmap = QPixmap('images/nocover.png', 'png')
                try:
                    album_title = song.tags['ALBUM'][0]
                    album_artist = song.tags['ALBUM ARTIST'][0]
                    track_title = song.tags['TITLE'][0]
                    self.setWindowTitle('{} - {} - {}' .format(album_artist, album_title, track_title))
                except KeyError:
                    pass

            self.art.setScaledContents(True)
            self.art.setPixmap(self.pixmap)
            self.art.setFixedSize(900, 900)


def main():
    application = QApplication(sys.argv)
    window = MusicPlayer()
    window.show()
    window.move(400, 200)
    sys.exit(application.exec_())

main()
