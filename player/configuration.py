import os
import pkg_resources
import pytoml
from appdirs import AppDirs
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QCheckBox, QDialog, QFileDialog, QGroupBox,
                             QHBoxLayout, QLabel, QLineEdit, QListWidget,
                             QListWidgetItem, QPushButton, QStackedWidget,
                             QVBoxLayout, QWidget)


class FileOptions(QWidget):
    """Contains all of the user configurable options related to the
    file menu."""

    def __init__(self, parent=None):
        """Initializes a page of options to be shown in the
        preferences dialog."""
        super(FileOptions, self).__init__(parent)

        file_config = QGroupBox("File Menu Configuration")

        self.recursive_directory = QCheckBox(
            'Recursively Open Directories (open files in all subdirectories)', self)

        self.check_directory_option()

        file_config_layout = QHBoxLayout()
        file_config_layout.addWidget(self.recursive_directory)

        file_config.setLayout(file_config_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(file_config)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

        self.recursive_directory.stateChanged.connect(self.recursive_directory_option)

    def recursive_directory_option(self):
        """This setting changes the behavior of the Open Directory item in
        the file menu. The default setting only opens songs in the
        selected directory. With this option checked, Open Directory will
        open all songs in the directory and its subdirectories."""
        settings_stream = pkg_resources.resource_stream(__name__, 'settings.toml')
        with settings_stream as conffile:
            config = pytoml.load(conffile)

        if self.recursive_directory.isChecked():
            config['recursive_directory'] = True

        elif not self.recursive_directory.isChecked():
            config['recursive_directory'] = False

        with settings_stream as conffile:            
            pytoml.dump(config, conffile)

    def check_directory_option(self):
        """Sets the options in the preferences dialog to the
        settings defined in settings.toml."""
        try:
            settings_stream = self.settings_file()

        except FileNotFoundError:
            settings_stream = pkg_resources.resource_stream(__name__, 'settings.toml')

        try:
            with open(settings_stream) as conffile:
                config = pytoml.load(conffile)
        except ValueError:
            with settings_stream as conffile:
                config = pytoml.load(conffile)

        if config['recursive_directory'] is True:
            self.recursive_directory.setChecked(True)
        elif config['recursive_directory'] is False:
            self.recursive_directory.setChecked(False)

    def settings_file(self):
        config_directory = AppDirs('mosaic', 'Mandeep').user_config_dir
        if not os.path.exists(config_directory):
            os.makedirs(config_directory)

        settings = pkg_resources.resource_filename(__name__, 'settings.toml')
        with open(settings) as conffile:
            config = conffile.read()

        config_file = os.path.join(config_directory, 'settings.toml')
        if not os.path.isfile(config_file):
            with open(config_file, 'a') as new_config_file:
                new_config_file.write(config)
            return new_config_file
        else:
            return config_file


class MediaLibrary(QWidget):
    """Contains all of the user configurable options related to the
    media library."""

    def __init__(self, parent=None):
        """Initializes a page of options to be shown in the
        preferences dialog."""
        super(MediaLibrary, self).__init__(parent)

        media_library_config = QGroupBox("Media Library Configuration")

        self.media_library_label = QLabel('Media Library', self)
        self.media_library_line = QLineEdit()
        self.media_library_button = QPushButton('Select Path')

        self.media_library_button.clicked.connect(self.select_media_library)

        media_library_config_layout = QHBoxLayout()
        media_library_config_layout.addWidget(self.media_library_label)
        media_library_config_layout.addWidget(self.media_library_line)
        media_library_config_layout.addWidget(self.media_library_button)

        media_library_config.setLayout(media_library_config_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(media_library_config)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

        self.media_library_settings()

    def select_media_library(self):
        """Opens a file dialog to allow the user to select the media library
        path. The path is then written to settings.toml."""
        library = QFileDialog.getExistingDirectory(self, 'Select Media Library Directory')
        if library:
            self.media_library_line.setText(library)

            settings_stream = pkg_resources.resource_stream(__name__, 'settings.toml')
            with settings_stream as conffile:
                config = pytoml.load(conffile)
                config['media_library_path'] = library

            with settings_stream as conffile:            
                pytoml.dump(config, conffile)

    def media_library_settings(self):
        """If the user has already defined a media library path that was
        previously written to settings.toml, the path is set as the text
        of the text box on the media library options page."""
        settings_stream = pkg_resources.resource_stream(__name__, 'settings.toml')
        with settings_stream as conffile:
            config = pytoml.load(conffile)

        library = config['media_library_path']
        if len(library) > 1:
            self.media_library_line.setText(library)


class PreferencesDialog(QDialog):
    """Creates a dialog that shows the user all of the user configurable
    options. A list on the left shows all of the available pages, with
    the page's contents shown on the right."""

    def __init__(self, parent=None):
        """Initializes the preferences dialog with a list box on the left
        and a content layout on the right."""

        super(PreferencesDialog, self).__init__(parent)
        self.setWindowTitle('Preferences')
        settings_icon = pkg_resources.resource_filename('player.images', 'md_settings.png')
        self.setWindowIcon(QIcon(settings_icon))
        self.setFixedSize(800, 700)

        self.contents = QListWidget()
        self.pages = QStackedWidget()

        self.pages.addWidget(FileOptions())
        self.pages.addWidget(MediaLibrary())
        self.list_items()

        layout = QHBoxLayout()
        layout.addWidget(self.contents)
        layout.addWidget(self.pages, 1)

        self.setLayout(layout)

        self.contents.currentItemChanged.connect(self.change_page)

    def list_items(self):
        """Lists all of the pages available to the user. Each page houses
        its own user configurable options."""
        file_options = QListWidgetItem(self.contents)
        file_options.setText('File Options')
        file_options.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
        self.contents.setCurrentRow(0)

        media_library_options = QListWidgetItem(self.contents)
        media_library_options.setText('Media Library')

    def change_page(self, current, previous):
        """Changes the page according to the clicked list item."""
        if not current:
            current = previous

        self.pages.setCurrentIndex(self.contents.row(current))
