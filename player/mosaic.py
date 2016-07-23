import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QMainWindow, QApplication, QToolBar,
                             QAction, QFileDialog)
from PyQt5.QtCore import Qt, QUrl


class MusicPlayer(QMainWindow):

    def __init__(self, parent=None):
        """
        Initializes the QMainWindow widget and calls methods that house
        other widgets that need to be displayed in the main window.
        """
        QMainWindow.__init__(self, parent)

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()

        self.file_name = None

        self.player.setPlaylist(self.playlist)
        self.menu_controls()
        self.media_controls()

        self.file_menu()

    def menu_controls(self):

        self.menu = self.menuBar()
        self.file = self.menu.addMenu('File')

    def media_controls(self):
        """
        Creates the bottom toolbar and controls used for media playback.
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
        self.open_action = QAction('Open file', self)
        self.open_action.setStatusTip('Add an audio file to an empty playlist.')
        self.open_action.setShortcut('CTRL+O')
        self.open_action.triggered.connect(self.open_file)

        self.file.addAction(self.open_action)

    def open_file(self):
        self.file_name, ok = QFileDialog.getOpenFileName(self, 'Open file')
        self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(self.file_name)))


def main():
    application = QApplication(sys.argv)
    application.setApplicationName('Mosaic')
    window = MusicPlayer()
    window.show()
    window.resize(1024, 768)
    window.move(400, 200)
    sys.exit(application.exec_())

main()
