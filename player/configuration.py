import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog, QGroupBox, QHBoxLayout,
    QLabel, QListWidget, QListWidgetItem, QPushButton,
    QStackedWidget, QVBoxLayout, QWidget)


class FilePage(QWidget):

    def __init__(self, parent=None):
        super(FilePage, self).__init__(parent)

        file_config = QGroupBox("File Menu Configuration")

        self.recursive_directory = QCheckBox('Recursive Open Directory '
                                        '(open files in all subdirectories)', self)
        self.recursive_directory.setChecked(False)

        file_config_layout = QHBoxLayout()
        file_config_layout.addWidget(self.recursive_directory)

        file_config.setLayout(file_config_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(file_config)
        main_layout.addStretch(1)

        self.recursive_directory.stateChanged.connect(self.recursive_directory_option)

        self.setLayout(main_layout)

    def recursive_directory_option(self):
        """This setting changes the behavior of the Open Directory item in
        the file menu. The default setting only searches for songs in the
        selected directory. With this option checked, Open Directory will
        also search subdirectories for songs."""


class PreferencesDialog(QDialog):

    def __init__(self, parent=None):

        super(PreferencesDialog, self).__init__(parent)
        self.setWindowTitle('Preferences')
        self.setFixedSize(800, 700)

        self.contents = QListWidget()
        self.pages = QStackedWidget()

        self.contents.setCurrentRow(0)
        self.pages.addWidget(FilePage())
        self.list_items()

        layout = QHBoxLayout()
        layout.addWidget(self.contents)
        layout.addWidget(self.pages, 1)

        self.setLayout(layout)

    def list_items(self):
        file_options = QListWidgetItem(self.contents)
        file_options.setText('File Options')
        file_options.setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)

        self.contents.currentItemChanged.connect(self.change_page)

    def change_page(self, current, previous):
        if not current:
            current = previous

        self.pages.setCurrentIndex(self.contents.row(current))
