import os
import pkg_resources
import pytoml
from appdirs import AppDirs
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QComboBox, QCheckBox, QDialog, QFileDialog, QGroupBox,
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

        self.user_config_file = os.path.join(AppDirs('mosaic', 'Mandeep').user_config_dir,
                                             'settings.toml')

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
        settings_stream = self.user_config_file
        with open(settings_stream) as conffile:
            config = pytoml.load(conffile)

        if self.recursive_directory.isChecked():
            config['file_options']['recursive_directory'] = True

        elif not self.recursive_directory.isChecked():
            config['file_options']['recursive_directory'] = False

        with open(settings_stream, 'w') as conffile:            
            pytoml.dump(conffile, config)

    def check_directory_option(self):
        """Sets the options in the preferences dialog to the
        settings defined in settings.toml."""
        settings_stream = self.user_config_file
        with open(settings_stream) as conffile:
            config = pytoml.load(conffile)

        if config['file_options']['recursive_directory'] is True:
            self.recursive_directory.setChecked(True)
        elif config['file_options']['recursive_directory'] is False:
            self.recursive_directory.setChecked(False)


class MediaLibrary(QWidget):
    """Contains all of the user configurable options related to the
    media library."""

    def __init__(self, parent=None):
        """Initializes a page of options to be shown in the
        preferences dialog."""
        super(MediaLibrary, self).__init__(parent)
        self.user_config_file = os.path.join(AppDirs('mosaic', 'Mandeep').user_config_dir,
                                             'settings.toml')

        media_library_config = QGroupBox("Media Library Configuration")

        self.media_library_label = QLabel('Media Library', self)
        self.media_library_line = QLineEdit()
        self.media_library_line.setReadOnly(True)
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
            settings_stream = self.user_config_file
            with open(settings_stream) as conffile:
                config = pytoml.load(conffile)

            config['media_library']['media_library_path'] = library

            with open(settings_stream, 'w') as conffile:           
                pytoml.dump(conffile, config)

    def media_library_settings(self):
        """If the user has already defined a media library path that was
        previously written to settings.toml, the path is set as the text
        of the text box on the media library options page."""
        settings_stream = self.user_config_file
        with open(settings_stream) as conffile:
            config = pytoml.load(conffile)

        library = config['media_library']['media_library_path']
        if os.path.isdir(library):
            self.media_library_line.setText(library)


class ViewOptions(QWidget):
    """Contains all of the user configurable options related to the UI functionality
    of the music player."""

    def __init__(self, parent=None):
        """Initiates the View Options page in the preferences dialog."""
        super(ViewOptions, self).__init__(parent)

        self.user_config_file = os.path.join(AppDirs('mosaic', 'Mandeep').user_config_dir,
                                             'settings.toml')

        view_options_config = QGroupBox("View Configuration")

        size_option = QLabel('Window Size', self)
       
        self.dropdown_box = QComboBox()
        self.dropdown_box.addItem('900 x 900')
        self.dropdown_box.addItem('800 x 800')
        self.dropdown_box.addItem('700 x 700')
        self.dropdown_box.addItem('600 x 600')
        self.dropdown_box.addItem('500 x 500')
        self.dropdown_box.addItem('400 x 400')

        view_config_layout = QHBoxLayout()
        view_config_layout.addWidget(size_option)
        view_config_layout.addWidget(self.dropdown_box)

        view_options_config.setLayout(view_config_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(view_options_config)
        main_layout.addStretch(1)
        self.setLayout(main_layout)

        self.check_window_size()

        self.dropdown_box.currentIndexChanged.connect(self.change_size)

    def change_size(self):
        """Records the change in window size to the settings.toml file."""
        settings_stream = self.user_config_file
        with open(settings_stream) as conffile:
            config = pytoml.load(conffile)

        if self.dropdown_box.currentIndex() != -1:
            config.setdefault('view_options', {})['window_size'] = self.dropdown_box.currentIndex()

        with open(settings_stream, 'w') as conffile:
            pytoml.dump(conffile, config)

    def check_window_size(self):
        """Sets the dropdown box to the current window size provided by the settings.toml
        file."""
        settings_stream = self.user_config_file
        with open(settings_stream) as conffile:
            config = pytoml.load(conffile)

        self.dropdown_box.setCurrentIndex(config['view_options']['window_size'])


class PreferencesDialog(QDialog):
    """Creates a dialog that shows the user all of the user configurable
    options. A list on the left shows all of the available pages, with
    the page's contents shown on the right."""

    def __init__(self, parent=None):
        """Initializes the preferences dialog with a list box on the left
        and a content layout on the right."""

        super(PreferencesDialog, self).__init__(parent)
        self.setWindowTitle('Preferences')
        settings_icon = pkg_resources.resource_filename('mosaic.images', 'md_settings.png')
        self.setWindowIcon(QIcon(settings_icon))
        self.setFixedSize(800, 700)

        self.contents = QListWidget()
        self.pages = QStackedWidget()

        self.pages.addWidget(FileOptions())
        self.pages.addWidget(ViewOptions())
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

        view_options = QListWidgetItem(self.contents)
        view_options.setText('View Options')
        view_options.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        media_library_options = QListWidgetItem(self.contents)
        media_library_options.setText('Media Library')
        media_library_options.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

    def change_page(self, current, previous):
        """Changes the page according to the clicked list item."""
        if not current:
            current = previous

        self.pages.setCurrentIndex(self.contents.row(current))
