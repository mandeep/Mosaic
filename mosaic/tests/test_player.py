from mosaic import player
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog
import sys

app = QApplication(sys.argv)


class TestMusicPlayer:

    def setup(self):
        """Initializes the music player window for each test. Showing the window
        has the indirect effect of testing items assigned to the main window such
        as the menu bar and the toolbar. Since the window would crash if these items
        did not exist or did not show, they are covered by this setup method."""
        self.music_player = player.MusicPlayer()
        self.music_player.show()

    def test_window(self):
        """Asserts that the window contains the proper title as well as the
        propeer height and width. Also asserts that the window icon appears
        correctly."""
        assert self.music_player.windowTitle() == 'Mosaic'
        assert self.music_player.width() == 900
        assert self.music_player.height() == 963
        assert self.music_player.windowIcon().isNull() is False

    def test_preferences(self, qtbot, mock):
        """Qtbot clicks on the edit menu then Qt.Key_Down highlights
        the preferences item. The mock plugin creates a mock of the
        QDialog window while Key_Enter executes it."""
        qtbot.mouseClick(self.music_player.edit, Qt.LeftButton)
        qtbot.keyClick(self.music_player.edit, Qt.Key_Down)
        mock.patch.object(QDialog, 'exec_', return_value='')
        qtbot.keyClick(self.music_player.edit, Qt.Key_Enter)

    def test_playlist_view(self, qtbot, mock):
        qtbot.mouseClick(self.music_player.view, Qt.LeftButton)
        qtbot.keyClick(self.music_player.view, Qt.Key_Down)
        qtbot.keyClick(self.music_player.view, Qt.Key_Enter)

    def test_media_information(self, qtbot, mock):
        qtbot.mouseClick(self.music_player.view, Qt.LeftButton)
        qtbot.keyClick(self.music_player.view, Qt.Key_Down)
        qtbot.keyClick(self.music_player.view, Qt.Key_Down)
        mock.patch.object(QDialog, 'exec_', return_value='')
        qtbot.keyClick(self.music_player.view, Qt.Key_Enter)
