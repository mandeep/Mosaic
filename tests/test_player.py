import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
import pytest

from mosaic import configuration, information, player


@pytest.fixture
def window(qtbot):
    """Initializes the music player window for each test.

    Showing the window has the indirect effect of testing items assigned
    to the main window such as the menu bar and the toolbar. Because the window
    would crash if these items did not exist or did not show, they are covered
    by this setup method."""
    music_player = player.MusicPlayer()
    qtbot.add_widget(music_player)
    music_player.show()
    yield music_player
    music_player.player.stop()


@pytest.fixture
def config(qtbot):
    """Provide the preferences dialog as a fixture to the tests."""
    preferences = configuration.PreferencesDialog()
    qtbot.add_widget(preferences)
    return preferences


@pytest.fixture
def flac_file():
    """Pass a FLAC file resource as an argument to the unit tests."""
    file = os.path.join(os.path.dirname(__file__), '02_Ghosts_I.flac')
    return file


@pytest.fixture
def mp3_file():
    """Pass an MP3 file resource as an argument to the unit tests."""
    file = os.path.join(os.path.dirname(__file__), '01_Ghosts_I_320kb.mp3')
    return file


@pytest.fixture
def blank_flac_file():
    """Pass a blank FLAC file resource as an argument to the unit tests.

    The metadata from this file has been removed to test cases where a file
    has no metadata."""
    file = os.path.join(os.path.dirname(__file__), '03_Ghosts_I.flac')
    return file


@pytest.fixture
def blank_mp3_file():
    """Pass an MP3 file resource as an argument to the unit tests.

    The metadata from this file has been removed to test cases where a file
    has no metadata."""
    file = os.path.join(os.path.dirname(__file__), '04_Ghosts_I_320kb.mp3')
    return file


def test_window(window):
    """Test the window title and window icon."""
    assert window.windowTitle() == 'Mosaic'
    assert window.windowIcon().isNull() is False


def test_open_flac_file(qtbot, mocker, window, flac_file):
    """Test the opening of a FLAC media file.

    Qtbot clicks on the file menu then Qt.Key_Down highlights
    the open file item. The mock plugin creates a mock of the
    QFileDialog window while Key_Enter executes it."""
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mocker.patch.object(QFileDialog, 'getOpenFileName', return_value=(flac_file, '*.flac'))
    qtbot.keyClick(window.file, Qt.Key_Enter)
    qtbot.mouseClick(window.art, Qt.LeftButton)
    window.player.play()
    qtbot.mouseClick(window.art, Qt.LeftButton)


def test_open_blank_flac_file(qtbot, mocker, window, blank_flac_file):
    """Test the opening of a blank FLAC media file.

    Qtbot clicks on the file menu then Qt.Key_Down highlights the open file item.
    The mock plugin creates a mock of the QFileDialog window while Qt.Key_Enter executes it.
    This test opens a blank flac file to test cases where metadata is not embedded in the file."""
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mocker.patch.object(QFileDialog, 'getOpenFileName', return_value=(blank_flac_file, '*.flac'))
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_open_blank_mp3_file(qtbot, mocker, window, blank_mp3_file):
    """Test the opening of a blank MP3 file.

    Qtbot clicks on the file menu then Qt.Key_Down highlights the open file item.
    The mock plugin creates a mock of the QFileDialog window while Qt.Key_Enter executes it.
    This test opens a blank flac file to test cases where metadata is not embedded in the file."""
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mocker.patch.object(QFileDialog, 'getOpenFileName', return_value=(blank_mp3_file, '*.mp3'))
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_open_mp3_file(qtbot, mocker, window, mp3_file):
    """Test the opening of an MP3 file.

    Qtbot clicks on the file menu then Qt.Key_Down highlights
    the open file item. The mock plugin creates a mock of the
    QFileDialog window while Key_Enter executes it."""
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mocker.patch.object(QFileDialog, 'getOpenFileName', return_value=(mp3_file, '*.mp3'))
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_open_files(qtbot, mocker, window, flac_file, mp3_file):
    """Test the opening of multiple media files.

    Qtbot clicks on the file menu then Qt.Key_Down highlights
    the open files item. The mock plugin creates a mock of the
    QFileDialog window while Key_Enter executes it."""
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mocker.patch.object(QFileDialog, 'getOpenFileNames', return_value=(
                      [flac_file, mp3_file], '*.flac *.mp3'))
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_open_playlist(qtbot, mocker, window):
    """Test the opening of a playlist file.

    Qtbot clicks on the file menu then Qt.Key_Down highlights
    the open playlist item. The mock plugin creates a mock of the
    QFileDialog window while Key_Enter executes it."""
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mocker.patch.object(QFileDialog, 'getOpenFileName', return_value=('test.m3u', '*.m3u'))
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_save_playlist(qtbot, mocker, window, tmpdir):
    """Test the saving of media in the playlist dock.

    Qtbot clicks on the file menu then Qt.Key_Down highlights
    the save playlist item. The mock plugin creates a mock of the
    QFileDialog window while Key_Enter executes it."""
    tmpdir.chdir()

    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mocker.patch.object(QFileDialog, 'getSaveFileName', return_value=('test', '*.m3u'))
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_open_directory(qtbot, mocker, window):
    """Test the opening of a media directory.

    Qtbot clicks on the file menu then Qt.Key_Down highlights
    the open directory item. The mock plugin creates a mock of the
    QFileDialog window while Key_Enter executes it."""
    file = os.path.join(os.path.dirname(__file__), '')
    qtbot.mouseClick(window.file, Qt.LeftButton)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    mocker.patch.object(QFileDialog, 'getExistingDirectory', return_value=file)
    qtbot.keyClick(window.file, Qt.Key_Enter)


def test_quit_application(qtbot, monkeypatch, window):
    """Test that the application exits properly.

    Qtbot clicks on the file menu and Qt.Key_Down highlights the quit application
    item. Monkeypatch is set to intercept the exit call and will append 1 to exit_calls
    when it does."""
    exit_calls = []
    monkeypatch.setattr(QApplication, 'quit', lambda: exit_calls.append(1))
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Down)
    qtbot.keyClick(window.file, Qt.Key_Enter)
    assert exit_calls == [1]


def test_preferences(qtbot, mocker, window):
    """Test the preferences dialog.

    Qtbot clicks on the edit menu then Qt.Key_Down highlights
    the preferences item. The mock plugin creates a mock of the
    QDialog window while Key_Enter executes it."""
    qtbot.mouseClick(window.edit, Qt.LeftButton)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    mocker.patch.object(QDialog, 'exec_', return_value='accept')
    qtbot.keyClick(window.edit, Qt.Key_Enter)


def test_media_library_path(qtbot, mocker, tmpdir, window, config):
    """Test the media library path setting in the preferences dialog.

    Qtbot tests the media library path selection by opening the preferences
    dialog, clicking on the set path button, and using the tmpdir fixture to provide
    a temporary directory."""
    qtbot.mouseClick(window.edit, Qt.LeftButton)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    mocker.patch.object(QDialog, 'exec_', return_value='')
    qtbot.keyClick(window.edit, Qt.Key_Enter)
    mocker.patch.object(QFileDialog, 'getExistingDirectory', return_value=str(tmpdir))
    qtbot.mouseClick(config.dialog_media_library.media_library_button, Qt.LeftButton)


def test_playback_options(qtbot, mocker, window, config):
    """Test the playback settings in the preferences dialog.

    Qtbot tests the functionality of the items in the Playback page of
    the preferences dialog. All of the checkboxes are selected and de-selected in
    order to test for segmentation faults."""
    qtbot.mouseClick(window.edit, Qt.LeftButton)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    mocker.patch.object(QDialog, 'exec_', return_value='')
    qtbot.keyClick(window.edit, Qt.Key_Enter)
    config.contents.setCurrentRow(1)
    qtbot.mouseClick(config.dialog_playback.cover_art_playback, Qt.LeftButton)
    qtbot.mouseClick(config.dialog_playback.cover_art_playback, Qt.LeftButton)


def test_view_options(qtbot, mocker, window, config):
    """Test the view options in the preferences dialog.

    Qtbot tests the functionality of the items in the View Options page of
    the preferences dialog. All of the checkboxes and radio buttons are selected,
    and the window size dropdown box is set to the 400x400 window size."""
    qtbot.mouseClick(window.edit, Qt.LeftButton)
    qtbot.keyClick(window.edit, Qt.Key_Down)
    mocker.patch.object(QDialog, 'exec_', return_value='')
    qtbot.keyClick(window.edit, Qt.Key_Enter)
    config.contents.setCurrentRow(2)
    qtbot.mouseClick(config.dialog_view_options.media_library_view_button, Qt.LeftButton)
    qtbot.mouseClick(config.dialog_view_options.media_library_view_button, Qt.LeftButton)
    qtbot.mouseClick(config.dialog_view_options.playlist_view_button, Qt.LeftButton)
    qtbot.mouseClick(config.dialog_view_options.playlist_view_button, Qt.LeftButton)
    qtbot.mouseClick(config.dialog_view_options.dock_left_side, Qt.LeftButton)
    qtbot.mouseClick(config.dialog_view_options.dock_right_side, Qt.LeftButton)
    config.dialog_view_options.dropdown_box.setCurrentIndex(5)
    config.dialog_view_options.dropdown_box.setCurrentIndex(0)


def test_about_dialog(qtbot, mocker, window):
    """Test that the about dialog opens correctly.

    Qtbot clicks on the help menu then Qt.Key_Down highlights
    the about item. The mock plugin creates a mock of the
    QMessageBox window while Key_Enter executes it."""
    qtbot.mouseClick(window.help_, Qt.LeftButton)
    qtbot.keyClick(window.help_, Qt.Key_Down)
    mocker.patch.object(QDialog, 'exec_', return_value='finished')
    qtbot.keyClick(window.help_, Qt.Key_Enter)


def test_playlist_view(qtbot, mocker, window):
    """Test that the playlist dock widget opens correctly.

    Qtbot selects the view menu then keys down to the view playlist
    item. Once highlighted, qtbot simulates the enter key on the item."""
    qtbot.mouseClick(window.view, Qt.LeftButton)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Enter)


def test_minimalist_view(qtbot, window):
    """Test the minimalist view setting.

    Qtbot clicks on the view menu then Qt.Key_Down highlights the
    minimalist view item and selects it."""
    qtbot.mouseClick(window.view, Qt.LeftButton)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Enter)


def test_media_information(qtbot, mocker, window):
    """Test that the media information dialog opens correctly..

    Qtbot clicks on the view menu then Qt.Key_Down highlights
    the media information item. The mock plugin creates a mock of the
    QDialog window while Key_Enter executes it."""
    qtbot.mouseClick(window.view, Qt.LeftButton)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Down)
    mocker.patch.object(QDialog, 'exec_', return_value='finished')
    qtbot.keyClick(window.view, Qt.Key_Enter)


def test_media_library(qtbot, window):
    """Test that the media library dock widget opens correctly.

    Qtbot clicks on the view menu then navigates to the View Media Library
    item and uses Qt.Key_Enter to select it."""
    qtbot.mouseClick(window.view, Qt.LeftButton)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Down)
    qtbot.keyClick(window.view, Qt.Key_Enter)


def test_media_information_directly(qtbot, flac_file, mp3_file):
    """Test that the media information dialog shows information correctly.

    Creates an instance of the GenralInformation and FullInformation classes to see
    if there are any errors."""
    information.GeneralInformation(flac_file)
    information.FullInformation(flac_file)
    information.GeneralInformation(mp3_file)
    information.FullInformation(mp3_file)


def test_playback_play(qtbot, window):
    """Test the play item in the playback menu."""
    qtbot.mouseClick(window.playback, Qt.LeftButton)
    qtbot.keyClick(window.playback, Qt.Key_Down)
    qtbot.keyClick(window.playback, Qt.Key_Enter)


def test_playback_stop(qtbot, window):
    """Test the stop item in the playback menu."""
    qtbot.mouseClick(window.playback, Qt.LeftButton)
    qtbot.keyClick(window.playback, Qt.Key_Down)
    qtbot.keyClick(window.playback, Qt.Key_Down)
    qtbot.keyClick(window.playback, Qt.Key_Enter)


def test_playback_previous(qtbot, window):
    """Test the previous item in the playback menu."""
    qtbot.mouseClick(window.playback, Qt.LeftButton)
    qtbot.keyClick(window.playback, Qt.Key_Down)
    qtbot.keyClick(window.playback, Qt.Key_Down)
    qtbot.keyClick(window.playback, Qt.Key_Down)
    qtbot.keyClick(window.playback, Qt.Key_Enter)


def test_playback_next(qtbot, window):
    """Test the next item in the playback menu."""
    qtbot.mouseClick(window.playback, Qt.LeftButton)
    qtbot.keyClick(window.playback, Qt.Key_Down)
    qtbot.keyClick(window.playback, Qt.Key_Down)
    qtbot.keyClick(window.playback, Qt.Key_Down)
    qtbot.keyClick(window.playback, Qt.Key_Down)
    qtbot.keyClick(window.playback, Qt.Key_Enter)
