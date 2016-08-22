from mosaic import player, configuration, library
import pkg_resources
import pytest
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QCheckBox, QDialog, QFileDialog, QMessageBox


@pytest.fixture
def window(qtbot):
    """Initializes the music player window for each test. Showing the window
    has the indirect effect of testing items assigned to the main window such
    as the menu bar and the toolbar. Since the window would crash if these items
    did not exist or did not show, they are covered by this setup method."""
    music_player = player.MusicPlayer()
    qtbot.add_widget(music_player)
    music_player.show()
    return music_player


@pytest.fixture
def config(qtbot):
    config_file = configuration.FileOptions()
    qtbot.add_widget(config_file)
    return config_file


def test_window(window):
    """Asserts that the window contains the proper title as well as the
    propeer height and width. Also asserts that the window icon appears
    correctly."""
    assert window.windowTitle() == 'Mosaic'
    assert window.width() == 900
    assert window.height() == 963
    assert window.windowIcon().isNull() is False


def test_open_mp3_file(qtbot, mock, window):
    """Qtbot clicks on the file menu then Qt.Key_Down highlights
    the open file item. The mock plugin creates a mock of the
    QFileDialog window while Key_Enter executes it."""
    file = pkg_resources.resource_filename('mosaic.tests', '01_Ghosts_I_320kb.mp3')
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mock.patch.object(QFileDialog, 'getOpenFileName', return_value=(file, '*.mp3'))
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_open_flac_file(qtbot, mock, window):
    """Qtbot clicks on the file menu then Qt.Key_Down highlights
    the open file item. The mock plugin creates a mock of the
    QFileDialog window while Key_Enter executes it."""
    file = pkg_resources.resource_filename('mosaic.tests', '02_Ghosts_I.flac')
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mock.patch.object(QFileDialog, 'getOpenFileName', return_value=(file, '*.flac'))
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_open_files(qtbot, mock, window):
    """Qtbot clicks on the file menu then Qt.Key_Down highlights
    the open files item. The mock plugin creates a mock of the
    QFileDialog window while Key_Enter executes it."""
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mock.patch.object(QFileDialog, 'getOpenFileNames', return_value=(
                      ['test.flac', '01_Ghosts_I_320kb.mp3'], '*.flac *.mp3'))
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_open_playlist(qtbot, mock, window):
    """Qtbot clicks on the file menu then Qt.Key_Down highlights
    the open playlist item. The mock plugin creates a mock of the
    QFileDialog window while Key_Enter executes it."""
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mock.patch.object(QFileDialog, 'getOpenFileName', return_value=('test.m3u', '*.m3u'))
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_open_directory(qtbot, mock, window):
    """Qtbot clicks on the file menu then Qt.Key_Down highlights
    the open directory item. The mock plugin creates a mock of the
    QFileDialog window while Key_Enter executes it."""
    file = pkg_resources.resource_filename('mosaic.tests', '')
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mock.patch.object(QFileDialog, 'getExistingDirectory', return_value=file)
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_quit_application(qtbot, monkeypatch, window):
    """Qtbot clicks on the file menu and Qt.Key_Down highlights the quit application
    item. Monkeypatch is set to intercept the exit call and will append 1 to exit_calls
    when it does."""
    exit_calls = []
    monkeypatch.setattr(QApplication, 'quit', lambda: exit_calls.append(1))
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Enter)
    assert exit_calls == [1]


def test_preferences(qtbot, mock, window):
    """Qtbot clicks on the edit menu then Qt.Key_Down highlights
    the preferences item. The mock plugin creates a mock of the
    QDialog window while Key_Enter executes it."""
    qtbot.mouseClick(window.edit, Qt.LeftButton)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    mock.patch.object(QDialog, 'exec_', return_value='accept')
    qtbot.keyClick(window.edit, Qt.Key_Enter)


def test_about_dialog(qtbot, mock, window):
    """Qtbot clicks on the help menu then Qt.Key_Down highlights
    the about item. The mock plugin creates a mock of the
    QMessageBox window while Key_Enter executes it."""
    qtbot.mouseClick(window.help_, Qt.LeftButton)
    qtbot.keyClick(window.help_, Qt.Key_Down)
    mock.patch.object(QMessageBox, 'exec_', return_value='')
    qtbot.keyClick(window.help_, Qt.Key_Enter)


def test_playlist_view(qtbot, mock, window):
    """Qtbot selects the view menu then keys down to the view playlist
    item. Once highlighted, qtbot simulates the enter key on the item."""
    qtbot.mouseClick(window.view, Qt.LeftButton)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Enter)


def test_media_information(qtbot, mock, window):
    """Qtbot clicks on the view menu then Qt.Key_Down highlights
    the media information item. The mock plugin creates a mock of the
    QDialog window while Key_Enter executes it."""
    qtbot.mouseClick(window.view, Qt.LeftButton)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Down)
    mock.patch.object(QDialog, 'exec_', return_value='accept')
    qtbot.keyClick(window.view, Qt.Key_Enter)


def test_checkbox(qtbot, mock, window, config):
    """Qtbot clicks on the edit menu then Qt.Key_Down highlights
    the preferences item. The mock plugin creates a mock of the
    QDialog window and the QCheckBox. The Qtbot's keyClick executes
    the QDialog while its mouseClick clicks on the checkbox to test
    for activity. """
    qtbot.mouseClick(window.edit, Qt.LeftButton)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    mock.patch.object(QDialog, 'exec_', return_value='')
    mock.patch.object(QCheckBox, 'toggle', return_value='')
    qtbot.keyClick(window.edit, Qt.Key_Enter)
    qtbot.mouseClick(config.recursive_directory, Qt.LeftButton)
    qtbot.mouseClick(config.recursive_directory, Qt.LeftButton)
    file = pkg_resources.resource_filename('mosaic.tests', '')
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mock.patch.object(QFileDialog, 'getExistingDirectory', return_value=file)
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_media_library(qtbot, window):
    """Qtbot clicks on the view menu then navigates to the View Media Library
    item and uses Qt.Key_Enter to select it."""
    qtbot.mouseClick(window.view, Qt.LeftButton)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Enter)
