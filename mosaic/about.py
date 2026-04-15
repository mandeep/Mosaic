from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout

from mosaic import utilities


class AboutDialog(QDialog):
    """Contains the necessary elements to show the about dialog."""

    def __init__(self, parent=None):
        """Display a dialog that shows application information."""
        super(AboutDialog, self).__init__(parent)
        self.setWindowTitle('About')

        help_icon = utilities.resource_filename('mosaic.images', 'md_help.png')
        self.setWindowIcon(QIcon(help_icon))
        self.resize(300, 200)

        author = QLabel('Created by mandeep')
        author.setAlignment(Qt.AlignmentFlag.AlignCenter)

        github = QLabel('GitHub: mandeep')
        github.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.dialog_layout = QVBoxLayout()
        self.dialog_layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

        self.dialog_layout.addWidget(author)
        self.dialog_layout.addWidget(github)

        self.setLayout(self.dialog_layout)
