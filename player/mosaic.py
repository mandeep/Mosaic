import os
import sys
from PyQt5.QtMultimedia import QMediaPlayer
from PyQt5.QtWidgets import QMainWindow, QApplication


class MusicPlayer(QMainWindow):

    def __init__(self, parent=None):

        QMainWindow.__init__(self, parent)
        self.interface()

    def interface(self):
        self.player = QMediaPlayer()


def main():
    application = QApplication(sys.argv)
    application.setApplicationName('Mosaic')
    window = MusicPlayer()
    window.show()
    window.resize(1024, 768)
    window.move(400, 200)
    sys.exit(application.exec_())

main()
