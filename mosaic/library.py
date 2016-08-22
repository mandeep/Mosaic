from appdirs import AppDirs
import os
from PyQt5.QtWidgets import QFileSystemModel, QTreeView
import pytoml


class MediaLibraryModel(QFileSystemModel):
    """Creates a model of the media library to be shown in a view."""

    def __init__(self, parent=None):
        """Reads the path of the media library from settings.toml and sets it as the
        root path of the file system model."""
        super(MediaLibraryModel, self).__init__(parent)

        self.setNameFilters(['*.mp3', '*.flac'])
        self.config_directory = AppDirs('mosaic', 'Mandeep').user_config_dir

        try:
            settings_stream = os.path.join(self.config_directory, 'settings.toml')
            with open(settings_stream) as conffile:
                config = pytoml.load(conffile)
            self.library = config['media_library']['media_library_path']

        except FileNotFoundError:
            self.library = ''

        if os.path.isdir(self.library):
            self.setRootPath(self.library)


class MediaLibraryView(QTreeView):
    """Creates a view of the media library from a model."""

    def __init__(self, parent=None):
        """Sets MediaLibraryModel as the model of the view and sets the root index as the
        path of the media library. Removes the 2nd, 3rd, and 4th columns which display
        size, type, and date modified."""
        super(MediaLibraryView, self).__init__(parent)

        self.model = MediaLibraryModel()
        self.setModel(self.model)

        if os.path.isdir(self.model.library):
            self.setRootIndex(self.model.index(self.model.library))

        for i in range(1, 4):
            self.hideColumn(i)
