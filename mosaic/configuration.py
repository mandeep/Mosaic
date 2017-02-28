import os
import pkg_resources

from appdirs import AppDirs
import pytoml

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QComboBox, QCheckBox, QDialog, QDialogButtonBox, QFileDialog,
                             QGroupBox, QHBoxLayout, QLabel, QLineEdit, QListWidget,
                             QListWidgetItem, QPushButton, QRadioButton, QStackedWidget,
                             QVBoxLayout, QWidget)


class MediaLibrary(QWidget):
    """Contains all of the user configurable options related to the media library."""

    def __init__(self, parent=None):
        """Initialize a page of options to be shown in the preferences dialog."""
        super(MediaLibrary, self).__init__(parent)
        self.user_config_file = os.path.join(AppDirs('mosaic', 'Mandeep').user_config_dir,
                                             'settings.toml')

        with open(self.user_config_file) as conffile:
            config = pytoml.load(conffile)

        media_library_config = QGroupBox("Media Library Configuration")

        self.media_library_label = QLabel('Media Library', self)
        self.media_library_line = QLineEdit()
        self.media_library_line.setReadOnly(True)
        self.media_library_button = QPushButton('Select Path')

        self.media_library_button.clicked.connect(lambda: self.select_media_library(config))

        media_library_layout = QVBoxLayout()

        media_library_config_layout = QHBoxLayout()
        media_library_config_layout.addWidget(self.media_library_label)
        media_library_config_layout.addWidget(self.media_library_line)
        media_library_config_layout.addWidget(self.media_library_button)

        media_library_layout.addLayout(media_library_config_layout)

        media_library_config.setLayout(media_library_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(media_library_config)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

        self.media_library_settings(config)

    def select_media_library(self, config):
        """Open a file dialog to allow the user to select the media library path.

        The selected path is written to settings.toml.
        """
        library = QFileDialog.getExistingDirectory(self, 'Select Media Library Directory')
        if library:
            self.media_library_line.setText(library)

            config['media_library']['media_library_path'] = library

            with open(self.user_config_file, 'w') as conffile:
                pytoml.dump(conffile, config)

    def media_library_settings(self, config):
        """Set the media library text box to the path of the media library.

        If the user has already defined a media library path that was
        previously written to settings.toml, the path is shown when the
        preferences dialog is opened.
        """
        library = config['media_library']['media_library_path']
        if os.path.isdir(library):
            self.media_library_line.setText(library)


class Playback(QWidget):
    """Contains all of the user configurable options related to media playback."""

    def __init__(self, parent=None):
        """Initiate the abstract widget that is displayed in the preferences dialog."""
        super(Playback, self).__init__(parent)
        self.user_config_file = os.path.join(AppDirs('mosaic', 'Mandeep').user_config_dir,
                                             'settings.toml')

        with open(self.user_config_file) as conffile:
            config = pytoml.load(conffile)

        playback_config = QGroupBox('Playback Configuration')
        playback_config_layout = QVBoxLayout()
        playback_config_layout.setAlignment(Qt.AlignTop)

        self.cover_art_playback = QCheckBox('Cover Art Playback')
        self.playlist_save_checkbox = QCheckBox('Save Playlist on Close')

        playback_config_layout.addWidget(self.cover_art_playback)
        playback_config_layout.addWidget(self.playlist_save_checkbox)

        playback_config.setLayout(playback_config_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(playback_config)

        self.setLayout(main_layout)

        self.check_playback_setting(config)
        self.check_playlist_save(config)
        self.cover_art_playback.clicked.connect(lambda: self.cover_art_playback_setting(config))
        self.playlist_save_checkbox.clicked.connect(lambda: self.playlist_save_setting(config))

    def cover_art_playback_setting(self, config):
        """Change the cover art playback behavior of the music player.

        The default setting allows for the current media
        to be paused and played with mouse button clicks on the cover art.
        """
        if self.cover_art_playback.isChecked():
            config.setdefault('playback', {})['cover_art'] = True

        elif not self.cover_art_playback.isChecked():
            config.setdefault('playback', {})['cover_art'] = False

        with open(self.user_config_file, 'w') as conffile:
            pytoml.dump(conffile, config)

    def playlist_save_setting(self, config):
        """Change the save playlist on close behavior of the music player."""
        if self.playlist_save_checkbox.isChecked():
            config.setdefault('playlist', {})['save_on_close'] = True

        elif not self.playlist_save_checkbox.isChecked():
            config.setdefault('playlist', {})['save_on_close'] = False

        with open(self.user_config_file, 'w') as conffile:
            pytoml.dump(conffile, config)

    def check_playback_setting(self, config):
        """Set the cover art playback checkbox state from settings.toml."""
        self.cover_art_playback.setChecked(config['playback']['cover_art'])

    def check_playlist_save(self, config):
        """Set the playlist save on close state from settings.toml."""
        self.playlist_save_checkbox.setChecked(config['playlist']['save_on_close'])


class ViewOptions(QWidget):
    """Contains all of the user configurable options related to the music player window."""

    def __init__(self, parent=None):
        """Initiate the View Options page in the preferences dialog."""
        super(ViewOptions, self).__init__(parent)

        self.user_config_file = os.path.join(AppDirs('mosaic', 'Mandeep').user_config_dir,
                                             'settings.toml')

        with open(self.user_config_file) as conffile:
            config = pytoml.load(conffile)

        dock_config = QGroupBox('Dock Configuration')

        self.media_library_view_button = QCheckBox('Show Media Library on Start', self)
        self.playlist_view_button = QCheckBox('Show Playlist on Start', self)

        dock_start_layout = QVBoxLayout()
        dock_start_layout.addWidget(self.media_library_view_button)
        dock_start_layout.addWidget(self.playlist_view_button)

        self.dock_position = QLabel('Dock Position:')
        self.dock_left_side = QRadioButton('Left Side')
        self.dock_right_side = QRadioButton('Right Side')

        dock_position_layout = QHBoxLayout()
        dock_position_layout.addWidget(self.dock_position)
        dock_position_layout.addWidget(self.dock_left_side)
        dock_position_layout.addWidget(self.dock_right_side)

        main_dock_layout = QVBoxLayout()
        main_dock_layout.addLayout(dock_start_layout)
        main_dock_layout.addLayout(dock_position_layout)
        dock_config.setLayout(main_dock_layout)

        window_config = QGroupBox("Window Configuration")

        size_option = QLabel('Window Size', self)

        self.dropdown_box = QComboBox()
        self.dropdown_box.addItem('900 x 900')
        self.dropdown_box.addItem('800 x 800')
        self.dropdown_box.addItem('700 x 700')
        self.dropdown_box.addItem('600 x 600')
        self.dropdown_box.addItem('500 x 500')
        self.dropdown_box.addItem('400 x 400')

        window_size_layout = QHBoxLayout()
        window_size_layout.addWidget(size_option)
        window_size_layout.addWidget(self.dropdown_box)

        window_config.setLayout(window_size_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(dock_config)
        main_layout.addWidget(window_config)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

        self.check_window_size(config)
        self.check_media_library(config)
        self.check_playlist_dock(config)
        self.check_dock_position(config)

        self.dropdown_box.currentIndexChanged.connect(lambda: self.change_size(config))
        self.media_library_view_button.clicked.connect(lambda: self.media_library_view_settings(config))
        self.playlist_view_button.clicked.connect(lambda: self.playlist_view_settings(config))
        self.dock_left_side.clicked.connect(lambda: self.dock_positon_settings(config))
        self.dock_right_side.clicked.connect(lambda: self.dock_positon_settings(config))

    def change_size(self, config):
        """Record the change in window size to the settings.toml file."""
        if self.dropdown_box.currentIndex() != -1:
            config.setdefault('view_options', {})['window_size'] = self.dropdown_box.currentIndex()

        with open(self.user_config_file, 'w') as conffile:
            pytoml.dump(conffile, config)

    def check_window_size(self, config):
        """Set the dropdown box to the current window size provided by settings.toml."""
        self.dropdown_box.setCurrentIndex(config['view_options']['window_size'])

    def media_library_view_settings(self, config):
        """Change the behavior of the Media Library dock widget.

        The default setting hides the dock on application start. With this option
        checked, the media library dock will show on start.
        """
        if self.media_library_view_button.isChecked():
            config.setdefault('media_library', {})['show_on_start'] = True

        elif not self.media_library_view_button.isChecked():
            config.setdefault('media_library', {})['show_on_start'] = False

        with open(self.user_config_file, 'w') as conffile:
            pytoml.dump(conffile, config)

    def check_media_library(self, config):
        """Set the media library checkbox state from settings.toml."""
        self.media_library_view_button.setChecked(config['media_library']['show_on_start'])

    def playlist_view_settings(self, config):
        """Change the behavior of the Playlist dock widget.

        The default setting hides the dock on application start. With this option
        checked, the playlist dock will show on start.
        """
        if self.playlist_view_button.isChecked():
            config.setdefault('playlist', {})['show_on_start'] = True

        elif not self.playlist_view_button.isChecked():
            config.setdefault('playlist', {})['show_on_start'] = False

        with open(self.user_config_file, 'w') as conffile:
            pytoml.dump(conffile, config)

    def check_playlist_dock(self, config):
        """Set the playlist dock checkbox state from settings.toml."""
        self.playlist_view_button.setChecked(config['playlist']['show_on_start'])

    def dock_positon_settings(self, config):
        """Write to the settings.toml the radio button chosen by the user."""
        if self.dock_left_side.isChecked():
            config.setdefault('dock', {})['position'] = 'left'

        elif self.dock_right_side.isChecked():
            config.setdefault('dock', {})['position'] = 'right'

        with open(self.user_config_file, 'w') as conffile:
            pytoml.dump(conffile, config)

    def check_dock_position(self, config):
        """Select the radio button previously chosen by the user in the preferences dialog."""
        if config['dock']['position'] == 'left':
            self.dock_left_side.setChecked(True)
        elif config['dock']['position'] == 'right':
            self.dock_right_side.setChecked(True)


class PreferencesDialog(QDialog):
    """Creates a dialog that shows the user all of the user configurable options.

    A list on the left shows all of the available pages, with
    the page's contents shown on the right.
    """

    def __init__(self, parent=None):
        """Initialize the preferences dialog with a list box and a content layout."""
        super(PreferencesDialog, self).__init__(parent)
        self.setWindowTitle('Preferences')
        settings_icon = pkg_resources.resource_filename('mosaic.images', 'md_settings.png')
        self.setWindowIcon(QIcon(settings_icon))
        self.resize(600, 450)

        self.contents = QListWidget()
        self.contents.setFixedWidth(175)
        self.pages = QStackedWidget()
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok)

        self.dialog_media_library = MediaLibrary()
        self.dialog_playback = Playback()
        self.dialog_view_options = ViewOptions()
        self.pages.addWidget(self.dialog_media_library)
        self.pages.addWidget(self.dialog_playback)
        self.pages.addWidget(self.dialog_view_options)
        self.list_items()

        stack_layout = QVBoxLayout()
        stack_layout.addWidget(self.pages)
        stack_layout.addWidget(self.button_box)

        layout = QHBoxLayout()
        layout.addWidget(self.contents)
        layout.addLayout(stack_layout)

        self.setLayout(layout)

        self.contents.currentItemChanged.connect(self.change_page)
        self.button_box.accepted.connect(self.accept)

    def list_items(self):
        """List all of the pages available to the user."""
        media_library_options = QListWidgetItem(self.contents)
        media_library_options.setText('Media Library')
        media_library_options.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.contents.setCurrentRow(0)

        playback_options = QListWidgetItem(self.contents)
        playback_options.setText('Playback')
        playback_options.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        view_options = QListWidgetItem(self.contents)
        view_options.setText('View Options')
        view_options.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def change_page(self, current, previous):
        """Change the page according to the clicked list item."""
        if not current:
            current = previous

        self.pages.setCurrentIndex(self.contents.row(current))
