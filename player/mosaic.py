import sys
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBar, QAction
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

        self.player.setPlaylist(self.playlist)
        self.menu_controls()
        self.media_controls()

        self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile('')))

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


def main():
    application = QApplication(sys.argv)
    application.setApplicationName('Mosaic')
    window = MusicPlayer()
    window.show()
    window.resize(1024, 768)
    window.move(400, 200)
    sys.exit(application.exec_())

main()
