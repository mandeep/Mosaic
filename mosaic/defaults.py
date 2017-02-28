import os
import pkg_resources

from appdirs import AppDirs
import pytoml

from PyQt5.QtCore import Qt


class Settings(object):
    """Settings module provides the Music Player access to the settings.toml file."""

    def __init__(self):
        """Using AppDirs, checks for an existing config folder for Mosaic.

        If the directory doesn't exist, it is created. The default settings from settings.toml
        is read into memory and then written to a new settings.toml file in the
        user config directory.
        """
        self.config_directory = AppDirs('mosaic', 'Mandeep').user_config_dir

        if not os.path.exists(self.config_directory):
            os.makedirs(self.config_directory)

        settings = pkg_resources.resource_filename(__name__, 'settings.toml')
        with open(settings) as default_config:
            config = default_config.read()

        self.user_config_file = os.path.join(self.config_directory, 'settings.toml')
        if not os.path.isfile(self.user_config_file):
            with open(self.user_config_file, 'a') as new_config_file:
                new_config_file.write(config)

        with open(self.user_config_file) as conffile:
            self.config = pytoml.load(conffile)

    def media_library_path(self):
        """Set the user defined media library path as the default path in file dialogs."""
        return self.config['media_library']['media_library_path']

    def media_library_on_start(self):
        """Set the state of the media library view checkbox from settings.toml."""
        return self.config['media_library']['show_on_start']

    def playlist_on_start(self):
        """Check the state of the playlist view checkbox from settings.toml."""
        return self.config['playlist']['show_on_start']

    def save_playlist_on_close(self):
        """Check the state of the save playlist close setting from settings.toml."""
        return self.config['playlist']['save_on_close']

    def playlist_path(self):
        """Return the user config directory as the location to save the playlist."""
        return self.config_directory

    def dock_position(self):
        """Return the dock area selected by the user in the preferences dialog."""
        radio_button_state = self.config['dock']['position']
        if radio_button_state == 'left':
            return Qt.LeftDockWidgetArea
        elif radio_button_state == 'right':
            return Qt.RightDockWidgetArea

    def window_size(self):
        """Set the user defined window size as the size of the current window.

        The sizes list contains widths from 900 to 400. Because the width of the window
        will be the same as the height, there's no need to differentiate between the two. The
        index contained in the settings.toml selects the index from the sizes list and sets
        the window and image size accordingly.
        """
        sizes = [900, 800, 700, 600, 500, 400]

        return sizes[self.config['view_options']['window_size']]
