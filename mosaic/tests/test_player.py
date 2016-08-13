from mosaic import player
from PyQt5.QtWidgets import (QApplication)
import sys

app = QApplication(sys.argv)


class TestMusicPlayer:

    def setup(self):
        self.music_player = player.MusicPlayer()
        self.music_player.show()

    def test_window(self):
        assert self.music_player.windowTitle() == 'Mosaic'
        assert self.music_player.width() == 900
        assert self.music_player.height() == 963
        assert self.music_player.windowIcon().isNull() is False

    def test_menubar(self):
        assert self.music_player.menu.isVisible()

    def test_toolbar(self):
        assert self.music_player.toolbar.isVisible()
