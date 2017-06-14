import os
import pkg_resources
import sys

import natsort

from PyQt5.QtCore import Qt, QFileInfo, QTime, QTimer, QUrl
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget, QDockWidget, QFileDialog,
                             QLabel, QListWidget, QListWidgetItem, QMainWindow, QSizePolicy,
                             QSlider, QToolBar, QVBoxLayout, QWidget)

from mosaic import about, configuration, defaults, information, library, metadata


class MusicPlayer(QMainWindow):
    """MusicPlayer houses all of elements that directly interact with the main window."""

    def __init__(self, parent=None):
        """Initialize the QMainWindow widget.

        The window title, window icon, and window size are initialized here as well
        as the following widgets: QMediaPlayer, QMediaPlaylist, QMediaContent, QMenuBar,
        QToolBar, QLabel, QPixmap, QSlider, QDockWidget, QListWidget, QWidget, and
        QVBoxLayout. The connect signals for relavant widgets are also initialized.
        """
        super(MusicPlayer, self).__init__(parent)
        self.setWindowTitle('Mosaic')
        window_icon = pkg_resources.resource_filename('mosaic.images', 'icon.png')
        self.setWindowIcon(QIcon(window_icon))
        self.resize(defaults.Settings().window_size(), defaults.Settings().window_size() + 63)

        # Initiates Qt objects to be used by MusicPlayer
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.playlist_location = defaults.Settings().playlist_path()
        self.content = QMediaContent()
        self.menu = self.menuBar()
        self.toolbar = QToolBar()
        self.art = QLabel()
        self.pixmap = QPixmap()
        self.slider = QSlider(Qt.Horizontal)
        self.duration_label = QLabel()
        self.playlist_dock = QDockWidget('Playlist', self)
        self.library_dock = QDockWidget('Media Library', self)
        self.playlist_view = QListWidget()
        self.library_view = library.MediaLibraryView()
        self.library_model = library.MediaLibraryModel()
        self.preferences = configuration.PreferencesDialog()
        self.widget = QWidget()
        self.layout = QVBoxLayout(self.widget)
        self.duration = 0
        self.playlist_dock_state = None
        self.library_dock_state = None

        # Sets QWidget() as the central widget of the main window
        self.setCentralWidget(self.widget)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.art.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

        # Initiates the playlist dock widget and the library dock widget
        self.addDockWidget(defaults.Settings().dock_position(), self.playlist_dock)
        self.playlist_dock.setWidget(self.playlist_view)
        self.playlist_dock.setVisible(defaults.Settings().playlist_on_start())
        self.playlist_dock.setFeatures(QDockWidget.DockWidgetClosable)

        self.addDockWidget(defaults.Settings().dock_position(), self.library_dock)
        self.library_dock.setWidget(self.library_view)
        self.library_dock.setVisible(defaults.Settings().media_library_on_start())
        self.library_dock.setFeatures(QDockWidget.DockWidgetClosable)
        self.tabifyDockWidget(self.playlist_dock, self.library_dock)

        # Sets the range of the playback slider and sets the playback mode as looping
        self.slider.setRange(0, self.player.duration() / 1000)
        self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)

        # OSX system menu bar causes conflicts with PyQt5 menu bar
        if sys.platform == 'darwin':
            self.menu.setNativeMenuBar(False)

        # Initiates Settings in the defaults module to give access to settings.toml
        defaults.Settings()

        # Signals that connect to other methods when they're called
        self.player.metaDataChanged.connect(self.display_meta_data)
        self.slider.sliderMoved.connect(self.seek)
        self.player.durationChanged.connect(self.song_duration)
        self.player.positionChanged.connect(self.song_position)
        self.player.stateChanged.connect(self.set_state)
        self.playlist_view.itemActivated.connect(self.activate_playlist_item)
        self.library_view.activated.connect(self.open_media_library)
        self.playlist.currentIndexChanged.connect(self.change_index)
        self.playlist.mediaInserted.connect(self.initialize_playlist)
        self.playlist_dock.visibilityChanged.connect(self.dock_visiblity_change)
        self.library_dock.visibilityChanged.connect(self.dock_visiblity_change)
        self.preferences.dialog_media_library.media_library_line.textChanged.connect(
            self.change_media_library_path)
        self.preferences.dialog_view_options.dropdown_box.currentIndexChanged.connect(
            self.change_window_size)
        self.art.mousePressEvent = self.press_playback

        # Creating the menu controls, media controls, and window size of the music player
        self.menu_controls()
        self.media_controls()
        self.load_saved_playlist()

    def menu_controls(self):
        """Initiate the menu bar and add it to the QMainWindow widget."""
        self.file = self.menu.addMenu('File')
        self.edit = self.menu.addMenu('Edit')
        self.view = self.menu.addMenu('View')
        self.help_ = self.menu.addMenu('Help')

        self.file_menu()
        self.edit_menu()
        self.view_menu()
        self.help_menu()

    def media_controls(self):
        """Create the bottom toolbar and controls used for media playback."""
        self.addToolBar(Qt.BottomToolBarArea, self.toolbar)
        self.toolbar.setMovable(False)

        play_icon = pkg_resources.resource_filename('mosaic.images', 'md_play.png')
        self.play_action = QAction(QIcon(play_icon), 'Play', self)
        self.play_action.triggered.connect(self.player.play)

        stop_icon = pkg_resources.resource_filename('mosaic.images', 'md_stop.png')
        self.stop_action = QAction(QIcon(stop_icon), 'Stop', self)
        self.stop_action.triggered.connect(self.player.stop)

        previous_icon = pkg_resources.resource_filename('mosaic.images', 'md_previous.png')
        self.previous_action = QAction(QIcon(previous_icon), 'Previous', self)
        self.previous_action.triggered.connect(self.previous)

        next_icon = pkg_resources.resource_filename('mosaic.images', 'md_next.png')
        self.next_action = QAction(QIcon(next_icon), 'Next', self)
        self.next_action.triggered.connect(self.playlist.next)

        repeat_icon = pkg_resources.resource_filename('mosaic.images', 'md_repeat_none.png')
        self.repeat_action = QAction(QIcon(repeat_icon), 'Repeat', self)
        self.repeat_action.triggered.connect(self.repeat_song)

        self.toolbar.addAction(self.play_action)
        self.toolbar.addAction(self.stop_action)
        self.toolbar.addAction(self.previous_action)
        self.toolbar.addAction(self.next_action)
        self.toolbar.addAction(self.repeat_action)
        self.toolbar.addWidget(self.slider)
        self.toolbar.addWidget(self.duration_label)

    def file_menu(self):
        """Add a file menu to the menu bar.

        The file menu houses the Open File, Open Multiple Files, Open Playlist,
        Open Directory, and Exit Application menu items.
        """
        self.open_action = QAction('Open File', self)
        self.open_action.setShortcut('CTRL+O')
        self.open_action.triggered.connect(self.open_file)

        self.open_multiple_files_action = QAction('Open Multiple Files', self)
        self.open_multiple_files_action.setShortcut('CTRL+SHIFT+O')
        self.open_multiple_files_action.triggered.connect(self.open_multiple_files)

        self.open_playlist_action = QAction('Open Playlist', self)
        self.open_playlist_action.setShortcut('CTRL+P')
        self.open_playlist_action.triggered.connect(self.open_playlist)

        self.open_directory_action = QAction('Open Directory', self)
        self.open_directory_action.setShortcut('CTRL+D')
        self.open_directory_action.triggered.connect(self.open_directory)

        self.exit_action = QAction('Quit', self)
        self.exit_action.setShortcut('CTRL+Q')
        self.exit_action.triggered.connect(self.closeEvent)

        self.file.addAction(self.open_action)
        self.file.addAction(self.open_multiple_files_action)
        self.file.addAction(self.open_playlist_action)
        self.file.addAction(self.open_directory_action)
        self.file.addSeparator()
        self.file.addAction(self.exit_action)

    def edit_menu(self):
        """Add an edit menu to the menu bar.

        The edit menu houses the preferences item that opens a preferences dialog
        that allows the user to customize features of the music player.
        """
        self.preferences_action = QAction('Preferences', self)
        self.preferences_action.setShortcut('CTRL+SHIFT+P')
        self.preferences_action.triggered.connect(lambda: self.preferences.exec_())

        self.edit.addAction(self.preferences_action)

    def view_menu(self):
        """Add a view menu to the menu bar.

        The view menu houses the Playlist, Media Library, Minimalist View, and Media
        Information menu items. The Playlist item toggles the playlist dock into and
        out of view. The Media Library items toggles the media library dock into and
        out of view. The Minimalist View item resizes the window and shows only the
        menu bar and player controls. The Media Information item opens a dialog that
        shows information relevant to the currently playing song.
        """
        self.dock_action = self.playlist_dock.toggleViewAction()
        self.dock_action.setShortcut('CTRL+ALT+P')

        self.library_dock_action = self.library_dock.toggleViewAction()
        self.library_dock_action.setShortcut('CTRL+ALT+L')

        self.minimalist_view_action = QAction('Minimalist View', self)
        self.minimalist_view_action.setShortcut('CTRL+ALT+M')
        self.minimalist_view_action.setCheckable(True)
        self.minimalist_view_action.triggered.connect(self.minimalist_view)

        self.view_media_info_action = QAction('Media Information', self)
        self.view_media_info_action.setShortcut('CTRL+SHIFT+M')
        self.view_media_info_action.triggered.connect(self.media_information_dialog)

        self.view.addAction(self.dock_action)
        self.view.addAction(self.library_dock_action)
        self.view.addSeparator()
        self.view.addAction(self.minimalist_view_action)
        self.view.addSeparator()
        self.view.addAction(self.view_media_info_action)

    def help_menu(self):
        """Add a help menu to the menu bar.

        The help menu houses the about dialog that shows the user information
        related to the application.
        """
        self.about_action = QAction('About', self)
        self.about_action.setShortcut('CTRL+H')
        self.about_action.triggered.connect(lambda: about.AboutDialog().exec_())

        self.help_.addAction(self.about_action)

    def open_file(self):
        """Open the selected file and add it to a new playlist."""
        filename, ok = QFileDialog.getOpenFileName(
            self, 'Open File', '', 'Audio (*.mp3 *.flac)', '',
            QFileDialog.ReadOnly)

        if ok:
            file_info = QFileInfo(filename).fileName()
            playlist_item = QListWidgetItem(file_info)
            self.playlist.clear()
            self.playlist_view.clear()
            self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(filename)))
            self.player.setPlaylist(self.playlist)
            playlist_item.setToolTip(file_info)
            self.playlist_view.addItem(playlist_item)
            self.playlist_view.setCurrentRow(0)
            self.player.play()

    def open_multiple_files(self):
        """Open the selected files and add them to a new playlist."""
        filenames, ok = QFileDialog.getOpenFileNames(
            self, 'Open Multiple Files', '',
            'Audio (*.mp3 *.flac)', '', QFileDialog.ReadOnly)

        if ok:
            self.playlist.clear()
            self.playlist_view.clear()
            for file in natsort.natsorted(filenames, alg=natsort.ns.PATH):
                file_info = QFileInfo(file).fileName()
                playlist_item = QListWidgetItem(file_info)
                self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(file)))
                self.player.setPlaylist(self.playlist)
                playlist_item.setToolTip(file_info)
                self.playlist_view.addItem(playlist_item)
                self.playlist_view.setCurrentRow(0)
                self.player.play()

    def open_playlist(self):
        """Load an M3U or PLS file into a new playlist."""
        playlist, ok = QFileDialog.getOpenFileName(
            self, 'Open Playlist', '',
            'Playlist (*.m3u *.pls)', '', QFileDialog.ReadOnly)
        if ok:
            playlist = QUrl.fromLocalFile(playlist)
            self.playlist.clear()
            self.playlist_view.clear()
            self.playlist.load(playlist)
            self.player.setPlaylist(self.playlist)

            for song_index in range(self.playlist.mediaCount()+1):
                file_info = self.playlist.media(song_index).canonicalUrl().fileName()
                playlist_item = QListWidgetItem(file_info)
                playlist_item.setToolTip(file_info)
                self.playlist_view.addItem(playlist_item)

            self.playlist_view.setCurrentRow(0)
            self.player.play()

    def load_saved_playlist(self):
        """Load the saved playlist if user setting permits."""
        saved_playlist = "{}/.m3u" .format(self.playlist_location)
        if os.path.exists(saved_playlist):
            playlist = QUrl().fromLocalFile(saved_playlist)
            self.playlist.load(playlist)
            self.player.setPlaylist(self.playlist)

            for song_index in range(self.playlist.mediaCount()+1):
                file_info = self.playlist.media(song_index).canonicalUrl().fileName()
                playlist_item = QListWidgetItem(file_info)
                playlist_item.setToolTip(file_info)
                self.playlist_view.addItem(playlist_item)

            self.playlist_view.setCurrentRow(0)

    def open_directory(self):
        """Open the selected directory and add the files within to an empty playlist."""
        directory = QFileDialog.getExistingDirectory(
            self, 'Open Directory', '', QFileDialog.ReadOnly)

        if directory:
            self.playlist.clear()
            self.playlist_view.clear()
            for dirpath, __, files in os.walk(directory):
                for filename in natsort.natsorted(files, alg=natsort.ns.PATH):
                    file = os.path.join(dirpath, filename)
                    if filename.endswith(('mp3', 'flac')):
                        self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(file)))
                        playlist_item = QListWidgetItem(filename)
                        playlist_item.setToolTip(filename)
                        self.playlist_view.addItem(playlist_item)

            self.player.setPlaylist(self.playlist)
            self.playlist_view.setCurrentRow(0)
            self.player.play()

    def open_media_library(self, index):
        """Open a directory or file from the media library into an empty playlist."""
        self.playlist.clear()
        self.playlist_view.clear()

        if self.library_model.fileName(index).endswith(('mp3', 'flac')):
            self.playlist.addMedia(
                QMediaContent(QUrl().fromLocalFile(self.library_model.filePath(index))))
            self.playlist_view.addItem(self.library_model.fileName(index))

        elif self.library_model.isDir(index):
            directory = self.library_model.filePath(index)
            for dirpath, __, files in os.walk(directory):
                for filename in natsort.natsorted(files, alg=natsort.ns.PATH):
                    file = os.path.join(dirpath, filename)
                    if filename.endswith(('mp3', 'flac')):
                        self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(file)))
                        playlist_item = QListWidgetItem(filename)
                        playlist_item.setToolTip(filename)
                        self.playlist_view.addItem(playlist_item)

        self.player.setPlaylist(self.playlist)
        self.player.play()

    def display_meta_data(self):
        """Display the current song's metadata in the main window.

        If the current song contains metadata, its cover art is extracted and shown in
        the main window while the track number, artist, album, and track title are shown
        in the window title.
        """
        if self.player.isMetaDataAvailable():
            file_path = self.player.currentMedia().canonicalUrl().toLocalFile()
            (album, artist, title, track_number, *__, artwork) = metadata.metadata(file_path)

            try:
                self.pixmap.loadFromData(artwork)
            except TypeError:
                self.pixmap = QPixmap(artwork)

            meta_data = '{} - {} - {} - {}' .format(
                    track_number, artist, album, title)
            self.setWindowTitle(meta_data)

            self.art.setScaledContents(True)
            self.art.setPixmap(self.pixmap)

            self.layout.addWidget(self.art)

    def initialize_playlist(self, start):
        """Display playlist and reset playback mode when media inserted into playlist."""
        if start == 0:
            if self.library_dock.isVisible():
                self.playlist_dock.setVisible(True)
                self.playlist_dock.show()
                self.playlist_dock.raise_()

            if self.playlist.playbackMode() == QMediaPlaylist.CurrentItemInLoop:
                self.repeat_song()

    def press_playback(self, event):
        """Change the playback of the player on cover art mouse event.

        When the cover art is clicked, the player will play the media if the player is
        either paused or stopped. If the media is playing, the media is set
        to pause.
        """
        if event.button() == 1 and configuration.Playback().cover_art_playback.isChecked():
            if (self.player.state() == QMediaPlayer.StoppedState or
                    self.player.state() == QMediaPlayer.PausedState):
                self.player.play()
            elif self.player.state() == QMediaPlayer.PlayingState:
                self.player.pause()

    def seek(self, seconds):
        """Set the position of the song to the position dragged to by the user."""
        self.player.setPosition(seconds * 1000)

    def song_duration(self, duration):
        """Set the slider to the duration of the currently played media."""
        duration /= 1000
        self.duration = duration
        self.slider.setMaximum(duration)

    def song_position(self, progress):
        """Move the horizontal slider in sync with the duration of the song.

        The progress is relayed to update_duration() in order
        to display the time label next to the slider.
        """
        progress /= 1000

        if not self.slider.isSliderDown():
            self.slider.setValue(progress)

        self.update_duration(progress)

    def update_duration(self, current_duration):
        """Calculate the time played and the length of the song.

        Both of these times are sent to duration_label() in order to display the
        times on the toolbar.
        """
        duration = self.duration

        if current_duration or duration:
            time_played = QTime((current_duration / 3600) % 60, (current_duration / 60) % 60,
                                (current_duration % 60), (current_duration * 1000) % 1000)
            song_length = QTime((duration / 3600) % 60, (duration / 60) % 60, (duration % 60),
                                (duration * 1000) % 1000)

            if duration > 3600:
                time_format = "hh:mm:ss"
            else:
                time_format = "mm:ss"

            time_display = "{} / {}" .format(time_played.toString(time_format),
                                             song_length.toString(time_format))
        else:
            time_display = ""

        self.duration_label.setText(time_display)

    def set_state(self, state):
        """Change the icon in the toolbar in relation to the state of the player.

        The play icon changes to the pause icon when a song is playing and
        the pause icon changes back to the play icon when either paused or
        stopped.
        """
        if self.player.state() == QMediaPlayer.PlayingState:
            pause_icon = pkg_resources.resource_filename('mosaic.images', 'md_pause.png')
            self.play_action.setIcon(QIcon(pause_icon))
            self.play_action.triggered.connect(self.player.pause)

        elif (self.player.state() == QMediaPlayer.PausedState or
              self.player.state() == QMediaPlayer.StoppedState):
            self.play_action.triggered.connect(self.player.play)
            play_icon = pkg_resources.resource_filename('mosaic.images', 'md_play.png')
            self.play_action.setIcon(QIcon(play_icon))

    def previous(self):
        """Move to the previous song in the playlist.

        Moves to the previous song in the playlist if the current song is less
        than five seconds in. Otherwise, restarts the current song.
        """
        if self.player.position() <= 5000:
            self.playlist.previous()
        else:
            self.player.setPosition(0)

    def repeat_song(self):
        """Set the current media to repeat and change the repeat icon accordingly.

        There are four playback modes: repeat none, repeat all, repeat once, and shuffle.
        Clicking the repeat button cycles through each playback mode.
        """
        if self.playlist.playbackMode() == QMediaPlaylist.Sequential:
            self.playlist.setPlaybackMode(QMediaPlaylist.Loop)
            repeat_on_icon = pkg_resources.resource_filename('mosaic.images', 'md_repeat_all.png')
            self.repeat_action.setIcon(QIcon(repeat_on_icon))

        elif self.playlist.playbackMode() == QMediaPlaylist.Loop:
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
            repeat_on_icon = pkg_resources.resource_filename('mosaic.images', 'md_repeat_once.png')
            self.repeat_action.setIcon(QIcon(repeat_on_icon))

        elif self.playlist.playbackMode() == QMediaPlaylist.CurrentItemInLoop:
            self.playlist.setPlaybackMode(QMediaPlaylist.Random)
            repeat_icon = pkg_resources.resource_filename('mosaic.images', 'md_shuffle.png')
            self.repeat_action.setIcon(QIcon(repeat_icon))

        elif self.playlist.playbackMode() == QMediaPlaylist.Random:
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
            repeat_icon = pkg_resources.resource_filename('mosaic.images', 'md_repeat_none.png')
            self.repeat_action.setIcon(QIcon(repeat_icon))

    def activate_playlist_item(self, item):
        """Set the active media to the playlist item dobule-clicked on by the user."""
        current_index = self.playlist_view.row(item)
        if self.playlist.currentIndex() != current_index:
            self.playlist.setCurrentIndex(current_index)

        if self.player.state() != QMediaPlayer.PlayingState:
            self.player.play()

    def change_index(self, row):
        """Highlight the row in the playlist of the active media."""
        self.playlist_view.setCurrentRow(row)

    def minimalist_view(self):
        """Resize the window to only show the menu bar and audio controls."""
        if self.minimalist_view_action.isChecked():

            if self.playlist_dock.isVisible():
                self.playlist_dock_state = True
            if self.library_dock.isVisible():
                self.library_dock_state = True

            self.library_dock.close()
            self.playlist_dock.close()

            QTimer.singleShot(10, lambda: self.resize(500, 0))

        else:
            self.resize(defaults.Settings().window_size(), defaults.Settings().window_size() + 63)

            if self.library_dock_state:
                self.library_dock.setVisible(True)

            if self.playlist_dock_state:
                self.playlist_dock.setVisible(True)

    def dock_visiblity_change(self, visible):
        """Change the size of the main window when the docks are toggled."""
        if visible and self.playlist_dock.isVisible() and not self.library_dock.isVisible():
            self.resize(defaults.Settings().window_size() + self.playlist_dock.width() + 6,
                        self.height())

        elif visible and not self.playlist_dock.isVisible() and self.library_dock.isVisible():
            self.resize(defaults.Settings().window_size() + self.library_dock.width() + 6,
                        self.height())

        elif visible and self.playlist_dock.isVisible() and self.library_dock.isVisible():
            self.resize(defaults.Settings().window_size() + self.library_dock.width() + 6,
                        self.height())

        elif (not visible and not self.playlist_dock.isVisible() and not
                self.library_dock.isVisible()):
            self.resize(defaults.Settings().window_size(), defaults.Settings().window_size() + 63)

    def media_information_dialog(self):
        """Show a dialog of the current song's metadata."""
        if self.player.isMetaDataAvailable():
            file_path = self.player.currentMedia().canonicalUrl().toLocalFile()
        else:
            file_path = None
        dialog = information.InformationDialog(file_path)
        dialog.exec_()

    def change_window_size(self):
        """Change the window size of the music player."""
        self.playlist_dock.close()
        self.library_dock.close()
        self.resize(defaults.Settings().window_size(), defaults.Settings().window_size() + 63)

    def change_media_library_path(self, path):
        """Change the media library path to the new path selected in the preferences dialog."""
        self.library_model.setRootPath(path)
        self.library_view.setModel(self.library_model)
        self.library_view.setRootIndex(self.library_model.index(path))

    def closeEvent(self, event):
        """Override the PyQt close event in order to handle save playlist on close."""
        playlist = "{}/.m3u" .format(self.playlist_location)
        if defaults.Settings().save_playlist_on_close():
            self.playlist.save(QUrl().fromLocalFile(playlist), "m3u")
        else:
            if os.path.exists(playlist):
                os.remove(playlist) 
        QApplication.quit()


def main():
    """Create an instance of the music player and use QApplication to show the GUI.

    QDesktopWidget() is used to move the application to the center of the user's screen.
    """
    application = QApplication(sys.argv)
    window = MusicPlayer()
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())
