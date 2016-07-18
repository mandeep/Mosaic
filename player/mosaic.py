import sys
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QToolBar, QAction
from PyQt5.QtCore import Qt


class MusicPlayer(QMainWindow):

    def __init__(self, parent=None):

        QMainWindow.__init__(self, parent)
        self.player = QMediaPlayer()
        self.media_controls()

    def media_controls(self):

        self.toolbar = QToolBar()
        self.addToolBar(Qt.BottomToolBarArea, self.toolbar)
        self.toolbar.setMovable(False)

        self.play_action = QAction(QIcon().fromTheme('media-playback-start'), 'Play', self)
        self.toolbar.addAction(self.play_action)


def main():
    application = QApplication(sys.argv)
    application.setApplicationName('Mosaic')
    window = MusicPlayer()
    window.show()
    window.resize(1024, 768)
    window.move(400, 200)
    sys.exit(application.exec_())

main()
