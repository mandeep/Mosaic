from appdirs import AppDirs
import os
import pkg_resources
import pytoml


class Settings(object):
    """Settings module provides the Music Player application with access to the
    settings.toml file."""

    def __init__(self):
        """Using AppDirs, checks for an existing config folder for Mosaic. If the directory
        doesn't exist, it is created. The default settings from settings.toml is read into memory
        and then written to a new settings.toml file in the user config directory."""

        config_directory = AppDirs('mosaic', 'Mandeep').user_config_dir

        if not os.path.exists(config_directory):
            os.makedirs(config_directory)

        settings = pkg_resources.resource_filename(__name__, 'settings.toml')
        with open(settings) as default_config:
            config = default_config.read()

        self.config_path = os.path.join(config_directory, 'settings.toml')
        if not os.path.isfile(self.config_path):
            with open(self.config_path, 'a') as new_config_file:
                new_config_file.write(config)

    def media_library_path(self):
        """Sets the user defined media library path as the default path
        in file dialogs."""

        with open(self.config_path) as conffile:
            config = pytoml.load(conffile)

        return config['media_library']['media_library_path']

    def media_library_on_start(self):
        """Checks the state of the media library view checkbox in settings.toml and returns this
        state for use by the Music Player application."""

        with open(self.config_path) as conffile:
            config = pytoml.load(conffile)

        try:
            checkbox_state = config['media_library']['show_on_start']
        except KeyError:
            checkbox_state = False

        return checkbox_state

    def playlist_on_start(self):
        """Checks the state of the playlist view checkbox in settings.toml and returns this
        state for use by the Music Player application."""

        with open(self.config_path) as conffile:
            config = pytoml.load(conffile)

        try:
            checkbox_state = config['playlist']['show_on_start']
        except KeyError:
            checkbox_state = False

        return checkbox_state

    def window_size(self):
        """Sets the user defined window size as the size of the current window. The
        sizes list contains widths from 900 to 400. Because the width of the window
        will be the same as the height, there's no need to differentiate between the two. The
        index contained in the settings.toml selects the index from the sizes list and sets
        the window and image size accordingly."""

        with open(self.config_path) as conffile:
            config = pytoml.load(conffile)

        sizes = [900, 800, 700, 600, 500, 400]

        try:
            size = sizes[config['view_options']['window_size']]
        except KeyError:
            size = 900

        return size
