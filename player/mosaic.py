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

        self.player.metaDataChanged.connect(self.retrieve_meta_data)

        self.art = QLabel(self)

        self.filename = None

        self.menu_controls()
        self.media_controls()

        self.file_menu()

        self.retrieve_meta_data()

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
        self.pixmap = QPixmap()
        self.byte_array = QByteArray()

        if self.player.isMetaDataAvailable() and self.filename:
            if self.filename.endswith('mp3'):
                song = mutagen.File(self.filename)
                artwork = self.byte_array.append(song.tags['APIC:'].data)
            elif self.filename.endswith('flac'):
                song = mutagen.flac.FLAC(self.filename)
                artwork = self.byte_array.append(song.pictures[0].data)
 
            self.pixmap.loadFromData(artwork, 'jpg')
            self.art.setPixmap(self.pixmap)
            self.art.setFixedWidth(self.pixmap.width())
            self.art.setFixedHeight(self.pixmap.height())
            self.setFixedSize(self.pixmap.width(), self.pixmap.height()+25)


def main():
    application = QApplication(sys.argv)
    application.setApplicationName('Mosaic')
    window = MusicPlayer()
    window.show()
    window.resize(600, 600)
    window.move(400, 200)
    sys.exit(application.exec_())

main()
