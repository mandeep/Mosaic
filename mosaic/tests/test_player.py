from mosaic import player, configuration
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QCheckBox, QDialog, QFileDialog, QMessageBox
import sys

app = QApplication(sys.argv)


class TestMusicPlayer:

    def setup(self):
        """Initializes the music player window for each test. Showing the window
        has the indirect effect of testing items assigned to the main window such
        as the menu bar and the toolbar. Since the window would crash if these items
        did not exist or did not show, they are covered by this setup method."""
        self.music_player = player.MusicPlayer()
        self.config_file = configuration.FileOptions()
        self.music_player.show()

    def test_window(self):
        """Asserts that the window contains the proper title as well as the
        propeer height and width. Also asserts that the window icon appears
        correctly."""
        assert self.music_player.windowTitle() == 'Mosaic'
        assert self.music_player.width() == 900
        assert self.music_player.height() == 963
        assert self.music_player.windowIcon().isNull() is False

    def test_open_file(self, qtbot, mock):
        """Qtbot clicks on the file menu then Qt.Key_Down highlights
        the open file item. The mock plugin creates a mock of the
        QFileDialog window while Key_Enter executes it."""
        qtbot.mouseClick(self.music_player.file, Qt.LeftButton)
        qtbot.keyClick(self.music_player.file, Qt.Key_Down)
        mock.patch.object(QFileDialog, 'getOpenFileName', return_value=('test.mp3', '*.mp3'))
        qtbot.keyClick(self.music_player.file, Qt.Key_Enter)

    def test_open_files(self, qtbot, mock):
        """Qtbot clicks on the file menu then Qt.Key_Down highlights
        the open files item. The mock plugin creates a mock of the
        QFileDialog window while Key_Enter executes it."""
        qtbot.mouseClick(self.music_player.file, Qt.LeftButton)
        qtbot.keyClick(self.music_player.file, Qt.Key_Down)
        qtbot.keyClick(self.music_player.file, Qt.Key_Down)
        mock.patch.object(QFileDialog, 'getOpenFileNames', return_value=(
                          ['test.flac', 'test.mp3'], '*.flac *.mp3'))
        qtbot.keyClick(self.music_player.file, Qt.Key_Enter)

    def test_open_playlist(self, qtbot, mock):
        """Qtbot clicks on the file menu then Qt.Key_Down highlights
        the open playlist item. The mock plugin creates a mock of the
        QFileDialog window while Key_Enter executes it."""
        qtbot.mouseClick(self.music_player.file, Qt.LeftButton)
        qtbot.keyClick(self.music_player.file, Qt.Key_Down)
        qtbot.keyClick(self.music_player.file, Qt.Key_Down)
        qtbot.keyClick(self.music_player.file, Qt.Key_Down)
        mock.patch.object(QFileDialog, 'getOpenFileName', return_value=('test.m3u', '*.m3u'))
        qtbot.keyClick(self.music_player.file, Qt.Key_Enter)

    def test_open_directory(self, qtbot, mock):
        """Qtbot clicks on the file menu then Qt.Key_Down highlights
        the open directory item. The mock plugin creates a mock of the
        QFileDialog window while Key_Enter executes it."""
        qtbot.mouseClick(self.music_player.file, Qt.LeftButton)
        qtbot.keyClick(self.music_player.file, Qt.Key_Down)
        qtbot.keyClick(self.music_player.file, Qt.Key_Down)
        qtbot.keyClick(self.music_player.file, Qt.Key_Down)
        qtbot.keyClick(self.music_player.file, Qt.Key_Down)
        mock.patch.object(QFileDialog, 'getExistingDirectory', return_value='/home/')
        qtbot.keyClick(self.music_player.file, Qt.Key_Enter)

    def test_quit_application(self, qtbot, monkeypatch):
        exit_calls = []
        monkeypatch.setattr(QApplication, 'quit', lambda: exit_calls.append(1))
        qtbot.keyClick(self.music_player.file, Qt.Key_Down)
        qtbot.keyClick(self.music_player.file, Qt.Key_Down)
        qtbot.keyClick(self.music_player.file, Qt.Key_Down)
        qtbot.keyClick(self.music_player.file, Qt.Key_Down)
        qtbot.keyClick(self.music_player.file, Qt.Key_Down)
        qtbot.keyClick(self.music_player.file, Qt.Key_Enter)
        assert exit_calls == [1]

    def test_preferences(self, qtbot, mock):
        """Qtbot clicks on the edit menu then Qt.Key_Down highlights
        the preferences item. The mock plugin creates a mock of the
        QDialog window while Key_Enter executes it."""
        qtbot.mouseClick(self.music_player.edit, Qt.LeftButton)
        qtbot.keyClick(self.music_player.edit, Qt.Key_Down)
        mock.patch.object(QDialog, 'exec_', return_value='')
        qtbot.keyClick(self.music_player.edit, Qt.Key_Enter)

    def test_playlist_view(self, qtbot, mock):
        """Qtbot selects the view menu then keys down to the view playlist
        item. Once highlighted, qtbot simulates the enter key on the item."""
        qtbot.mouseClick(self.music_player.view, Qt.LeftButton)
        qtbot.keyClick(self.music_player.view, Qt.Key_Down)
        qtbot.keyClick(self.music_player.view, Qt.Key_Enter)

    def test_media_information(self, qtbot, mock):
        """Qtbot clicks on the view menu then Qt.Key_Down highlights
        the media information item. The mock plugin creates a mock of the
        QDialog window while Key_Enter executes it."""
        qtbot.mouseClick(self.music_player.view, Qt.LeftButton)
        qtbot.keyClick(self.music_player.view, Qt.Key_Down)
        qtbot.keyClick(self.music_player.view, Qt.Key_Down)
        mock.patch.object(QDialog, 'exec_', return_value='')
        qtbot.keyClick(self.music_player.view, Qt.Key_Enter)

    def test_about_dialog(self, qtbot, mock):
        """Qtbot clicks on the help menu then Qt.Key_Down highlights
        the about item. The mock plugin creates a mock of the
        QMessageBox window while Key_Enter executes it."""
        qtbot.mouseClick(self.music_player.help_, Qt.LeftButton)
        qtbot.keyClick(self.music_player.help_, Qt.Key_Down)
        mock.patch.object(QMessageBox, 'exec_', return_value='')
        qtbot.keyClick(self.music_player.help_, Qt.Key_Enter)

    def test_checkbox(self, qtbot, mock):
        """Qtbot clicks on the edit menu then Qt.Key_Down highlights
        the preferences item. The mock plugin creates a mock of the
        QDialog window and the QCheckBox. The Qtbot's keyClick executes
        the QDialog while its mouseClick clicks on the checkbox to test
        for activity. """
        qtbot.mouseClick(self.music_player.edit, Qt.LeftButton)
        qtbot.keyClick(self.music_player.edit, Qt.Key_Down)
        mock.patch.object(QDialog, 'exec_', return_value='')
        mock.patch.object(QCheckBox, 'toggle', return_value='')
        qtbot.keyClick(self.music_player.edit, Qt.Key_Enter)
        qtbot.mouseClick(self.config_file.recursive_directory, Qt.LeftButton)
        qtbot.mouseClick(self.config_file.recursive_directory, Qt.LeftButton)
