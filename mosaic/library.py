import os

from appdirs import AppDirs
from PySide6.QtWidgets import QFileSystemModel, QTreeView
import toml


class MediaLibraryModel(QFileSystemModel):
    """Creates a model of the media library to be shown in a view."""

    def __init__(self, parent=None):
        """Read the path of the media library from settings.toml.

        This path is set as the root path of the file system model.
        """
        super(MediaLibraryModel, self).__init__(parent)

        self.setNameFilters(['*.mp3', '*.flac'])
        self.config_directory = AppDirs('mosaic', 'mandeep').user_config_dir
        self.user_config_file = os.path.join(self.config_directory, 'settings.toml')

        with open(self.user_config_file, 'r') as conffile:
            config = toml.load(conffile)
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

        self.media_model = MediaLibraryModel()
        self.setModel(self.media_model)

        if os.path.isdir(self.media_model.library):
            self.setRootIndex(self.media_model.index(self.media_model.library))

        for column in range(1, 4):
            self.hideColumn(column)
