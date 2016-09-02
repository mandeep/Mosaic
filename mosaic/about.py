import pkg_resources
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox


class AboutDialog(QMessageBox):
    """Contains the necessary elements to show helpful text in a dialog."""

    def __init__(self, parent=None):
        """Displays a dialog that shows application information."""
        super(AboutDialog, self).__init__(parent)

        self.setWindowTitle('About')
        help_icon = pkg_resources.resource_filename('mosaic.images', 'md_help.png')
        self.setWindowIcon(QIcon(help_icon))

        self.setText('Created by Mandeep Bhutani')
        self.setInformativeText('Material design icons created by Google\n\n'
                                'GitHub: mandeepbhutani')
