import os

from appdirs import AppDirs
import pytoml

from PyQt5.QtWidgets import QFileSystemModel, QTreeView


class MediaLibraryModel(QFileSystemModel):
    """Creates a model of the media library to be shown in a view."""

    def __init__(self, parent=None):
        """Read the path of the media library from settings.toml.

        This path is set as the root path of the file system model.
        """
        super(MediaLibraryModel, self).__init__(parent)

        self.setNameFilters(['*.mp3', '*.flac'])
        self.config_directory = AppDirs('mosaic', 'Mandeep').user_config_dir
        self.user_config_file = os.path.join(self.config_directory, 'settings.toml')

        with open(self.user_config_file) as conffile:
            config = pytoml.load(conffile)
        self.library = config['media_library']['media_library_path']

        if os.path.isdir(self.library):
            self.setRootPath(self.library)


class MediaLibraryView(QTreeView):
    """Creates a view of the media library from a model."""

    def __init__(self, parent=None):
        """Set MediaLibraryModel as the model of the view.

        Sets the root index as the path of the media library. Removes
        the 2nd, 3rd, and 4th columns which display size, type, and date modified.
        """
        super(MediaLibraryView, self).__init__(parent)

        self.model = MediaLibraryModel()
        self.setModel(self.model)

        if os.path.isdir(self.model.library):
            self.setRootIndex(self.model.index(self.model.library))

        for column in range(1, 4):
            self.hideColumn(column)
