import sys
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBar, QAction
from PyQt5.QtCore import Qt


class MusicPlayer(QMainWindow):

    def __init__(self, parent=None):

        QMainWindow.__init__(self, parent)
        """
        Initializes the QMainWindow widget and calls other widgets that
        need to be displayed in the main window.
        """
        self.player = QMediaPlayer()
        self.media_controls()

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
