import sys
from PyQt5.QtWidgets import QApplication, QDialog, QListWidget, QStackedWidget, QWidget


class ConfigurationPage(QWidget):

    def __init__(self, parent=None):
        super(ConfigurationPage, self).__init__(parent)


class PreferencesDialog(QDialog):

    def __init__(self, parent=None):

        super(PreferencesDialog, self).__init__(parent)
        self.setWindowTitle('Preferences')
