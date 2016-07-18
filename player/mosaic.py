import os
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication


class MusicPlayer(QMainWindow):

    def __init__(self, parent=None):

        QMainWindow.__init__(self, parent)
        self.init_ui()

    def init_ui(self):
        self.setGeometry(400, 200, 1024, 768)
        self.setWindowTitle('Mosaic')


def main():
    application = QApplication(sys.argv)
    player = MusicPlayer()
    player.show()
    sys.exit(application.exec_())

main()
