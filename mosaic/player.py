import os
import sys

import natsort

from PySide6.QtCore import Qt, QFileInfo, QTime, QTimer, QUrl
from PySide6.QtGui import QAction, QIcon, QKeySequence, QPixmap, QShortcut
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer
from PySide6.QtWidgets import (QApplication, QDockWidget, QFileDialog,
                             QLabel, QListWidget, QListWidgetItem, QMainWindow, QSizePolicy,
                             QSlider, QToolBar, QVBoxLayout, QWidget)

from mosaic import about, configuration, defaults, information, library, metadata, utilities


class MusicPlayer(QMainWindow):
    """MusicPlayer houses all of elements that directly interact with the main window."""

    def __init__(self, parent=None):
        """Initialize the QMainWindow widget.

        The window title, window icon, and window size are initialized here as well
        as the following widgets: QMediaPlayer, QAudioOutput, QMenuBar,
        QToolBar, QLabel, QPixmap, QSlider, QDockWidget, QListWidget, QWidget, and
        QVBoxLayout. The connect signals for relevant widgets are also initialized.
        """
        super(MusicPlayer, self).__init__(parent)
        self.setWindowTitle('Mosaic')

        window_icon = utilities.resource_filename('mosaic.images', 'icon.png')
        self.setWindowIcon(QIcon(window_icon))

        # Read settings.toml once and cache the Settings object.  Calls that need
        # fresh values after the preferences dialog closes go through
        # self.reload_settings() instead of constructing new Settings objects.
        self.settings = defaults.Settings()
        self.resize(self.settings.window_size, self.settings.window_size)

        # Initiates Qt objects to be used by MusicPlayer
        self.player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.player.setAudioOutput(self.audio_output)
        self.playlist = []
        self.current_index = -1
        self.playlist_location = self.settings.playlist_path
        self.menu = self.menuBar()
        self.toolbar = QToolBar()
        self.art = QLabel()
        self.pixmap = QPixmap()
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.duration_label = QLabel()
        self.playlist_dock = QDockWidget('Playlist', self)
        self.library_dock = QDockWidget('Media Library', self)
        self.playlist_view = QListWidget()
        self.playlist_view.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.library_view = library.MediaLibraryView()
        self.preferences = configuration.PreferencesDialog()
        self.widget = QWidget()
        self.player_layout = QVBoxLayout(self.widget)
        self.duration = 0
        self.playlist_dock_state = None
        self.library_dock_state = None

        # Sets QWidget() as the central widget of the main window
        self.setCentralWidget(self.widget)
        self.player_layout.setContentsMargins(0, 0, 0, 0)
        self.art.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        # Initiates the playlist dock widget and the library dock widget
        self.addDockWidget(self.settings.dock_position, self.playlist_dock)
        self.playlist_dock.setWidget(self.playlist_view)
        self.playlist_dock.setVisible(self.settings.playlist_on_start)
        self.playlist_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable)

        self.addDockWidget(self.settings.dock_position, self.library_dock)
        self.library_dock.setWidget(self.library_view)
        self.library_dock.setVisible(self.settings.media_library_on_start)
        self.library_dock.setFeatures(QDockWidget.DockWidgetFeature.DockWidgetClosable)
        self.tabifyDockWidget(self.playlist_dock, self.library_dock)

        # Sets the range of the playback slider and sets the playback mode as looping
        self.slider.setRange(0, self.player.duration() // 1000)

        # OSX system menu bar causes conflicts with PyQt5 menu bar
        if sys.platform == 'darwin':
            self.menu.setNativeMenuBar(False)

        # Signals that connect to other methods when they're called
        self.player.metaDataChanged.connect(self.display_meta_data)
        self.player.mediaStatusChanged.connect(self.handle_media_status)
        self.slider.sliderMoved.connect(self.seek)
        self.player.durationChanged.connect(self.song_duration)
        self.player.positionChanged.connect(self.song_position)
        self.player.playbackStateChanged.connect(self.set_state)
        self.playlist_view.itemActivated.connect(self.activate_playlist_item)
        self.library_view.activated.connect(self.open_media_library)
        self.playlist_dock.visibilityChanged.connect(self.dock_visibility_change)
        self.library_dock.visibilityChanged.connect(self.dock_visibility_change)
        self.preferences.dialog_media_library.media_library_line.textChanged.connect(self.change_media_library_path)
        self.preferences.dialog_view_options.dropdown_box.currentIndexChanged.connect(self.change_window_size)
        self.preferences.finished.connect(self.reload_settings)
        self.art.mousePressEvent = self.press_playback
        self.delete_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Delete), self.playlist_view)
        self.delete_shortcut.activated.connect(self.remove_from_playlist)

        # Creating the menu controls, media controls, and window size of the music player
        self.menu_controls()
        self.media_controls()
        self.load_saved_playlist()

    def handle_media_status(self, status):
        """Auto-play next track when current ends."""
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.next()

    def play_index(self, index):
        """Play specific track from the manual playlist."""
        if 0 <= index and index < len(self.playlist):
            self.current_index = index
            self.player.setSource(self.playlist[index])
            self.playlist_view.setCurrentRow(index)
            self.player.play()

    def menu_controls(self):
        """Initiate the menu bar and add it to the QMainWindow widget."""
        self.file = self.menu.addMenu('File')
        self.edit = self.menu.addMenu('Edit')
        self.playback = self.menu.addMenu('Playback')
        self.view = self.menu.addMenu('View')
        self.help_ = self.menu.addMenu('Help')

        self.file_menu()
        self.edit_menu()
        self.playback_menu()
        self.view_menu()
        self.help_menu()

    def media_controls(self):
        """Create the bottom toolbar and controls used for media playback."""
        self.addToolBar(Qt.ToolBarArea.BottomToolBarArea, self.toolbar)
        self.toolbar.setMovable(False)

        play_icon = utilities.resource_filename('mosaic.images', 'md_play.png')
        self.play_action = QAction(QIcon(play_icon), 'Play', self)
        self.play_action.triggered.connect(self.toggle_playback)

        stop_icon = utilities.resource_filename('mosaic.images', 'md_stop.png')
        self.stop_action = QAction(QIcon(stop_icon), 'Stop', self)
        self.stop_action.triggered.connect(self.player.stop)

        previous_icon = utilities.resource_filename('mosaic.images', 'md_previous.png')
        self.previous_action = QAction(QIcon(previous_icon), 'Previous', self)
        self.previous_action.triggered.connect(self.previous)

        next_icon = utilities.resource_filename('mosaic.images', 'md_next.png')
        self.next_action = QAction(QIcon(next_icon), 'Next', self)
        self.next_action.triggered.connect(self.next)

        self.toolbar.addAction(self.play_action)
        self.toolbar.addAction(self.stop_action)
        self.toolbar.addAction(self.previous_action)
        self.toolbar.addAction(self.next_action)
        self.toolbar.addWidget(self.slider)
        self.toolbar.addWidget(self.duration_label)

    def file_menu(self):
        """Add a file menu to the menu bar.

        The file menu houses the Open File, Open Multiple Files, Open Playlist,
        Open Directory, and Exit Application menu items.
        """
        self.open_action = QAction('Open File', self)
        self.open_action.setShortcut('O')
        self.open_action.triggered.connect(self.open_file)

        self.open_multiple_files_action = QAction('Open Multiple Files', self)
        self.open_multiple_files_action.setShortcut('M')
        self.open_multiple_files_action.triggered.connect(self.open_multiple_files)

        self.open_playlist_action = QAction('Open Playlist', self)
        self.open_playlist_action.setShortcut('CTRL+P')
        self.open_playlist_action.triggered.connect(self.open_playlist)

        self.open_directory_action = QAction('Open Directory', self)
        self.open_directory_action.setShortcut('D')
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

    def playback_menu(self):
        """Add a playback menu to the menu bar.

        The playback menu houses
        """
        self.play_playback_action = QAction('Play', self)
        self.play_playback_action.setShortcut('P')
        self.play_playback_action.triggered.connect(self.toggle_playback)

        self.stop_playback_action = QAction('Stop', self)
        self.stop_playback_action.setShortcut('S')
        self.stop_playback_action.triggered.connect(self.player.stop)

        self.previous_playback_action = QAction('Previous', self)
        self.previous_playback_action.setShortcut('B')
        self.previous_playback_action.triggered.connect(self.previous)

        self.next_playback_action = QAction('Next', self)
        self.next_playback_action.setShortcut('N')
        self.next_playback_action.triggered.connect(self.next)

        self.playback.addAction(self.play_playback_action)
        self.playback.addAction(self.stop_playback_action)
        self.playback.addAction(self.previous_playback_action)
        self.playback.addAction(self.next_playback_action)

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
        self.about_action.setShortcut('H')
        self.about_action.triggered.connect(lambda: about.AboutDialog().exec_())

        self.help_.addAction(self.about_action)

    def open_file(self):
        """Open the selected file and add it to a new playlist."""
        filename, success = QFileDialog.getOpenFileName(self, 'Open File', '', 'Audio (*.mp3 *.flac)', '', QFileDialog.Option.ReadOnly)

        if success:
            file_info = QFileInfo(filename).baseName()
            playlist_item = QListWidgetItem(file_info)
            self.playlist = [QUrl.fromLocalFile(filename)]
            playlist_item.setToolTip(file_info)
            self.playlist_view.addItem(playlist_item)
            self.playlist_view.setCurrentRow(0)
            self.play_index(0)

    def open_multiple_files(self):
        """Open the selected files and add them to a new playlist."""
        filenames, success = QFileDialog.getOpenFileNames(self, 'Open Multiple Files', '', 'Audio (*.mp3 *.flac)', '', QFileDialog.Option.ReadOnly)

        if success:
            for file in natsort.natsorted(filenames, alg=natsort.ns.PATH):
                file_info = QFileInfo(file).baseName()
                playlist_item = QListWidgetItem(file_info)
                self.playlist.append(QUrl().fromLocalFile(file))
                playlist_item.setToolTip(file_info)
                self.playlist_view.addItem(playlist_item)
            self.playlist_view.setCurrentRow(0)
            self.play_index(0)

    def open_playlist(self):
        """Load an M3U file into a new playlist."""
        playlist, success = QFileDialog.getOpenFileName(self, 'Open Playlist', '', 'Playlist (*.m3u)', '', QFileDialog.Option.ReadOnly)

        if success:
            self.playlist.clear()
            self.playlist_view.clear()
            self.current_index = -1

            with open(playlist, 'r', encoding='utf-8') as f:
                for line in f:
                    file = line.strip()
                    if file and not file.startswith('#') and os.path.exists(file):
                        self.playlist.append(QUrl.fromLocalFile(file))
                        file_info = QFileInfo(file).fileName()
                        playlist_item = QListWidgetItem(file_info)
                        playlist_item.setToolTip(file_info)
                        self.playlist_view.addItem(playlist_item)

            if self.playlist:
                self.playlist_view.setCurrentRow(0)
                self.play_index(0)

    def save_playlist(self):
        """Save the media in the playlist dock as a new M3U playlist."""
        playlist_path = os.path.join(self.playlist_location, 'saved_playlist.m3u')
        with open(playlist_path, 'w', encoding='utf-8') as f:
            for url in self.playlist:
                f.write(url.toLocalFile() + '\n')

    def load_saved_playlist(self):
        """Load the saved playlist if user setting permits."""
        saved_playlist = os.path.join(self.playlist_location, 'saved_playlist.m3u')
        if os.path.exists(saved_playlist):
            with open(saved_playlist, 'r', encoding='utf-8') as f:
                for line in f:
                    file = line.strip()
                    if file and not file.startswith('#') and os.path.exists(file):
                        self.playlist.append(QUrl.fromLocalFile(file))
                        file_info = QFileInfo(file).fileName()
                        playlist_item = QListWidgetItem(file_info)
                        playlist_item.setToolTip(file_info)
                        self.playlist_view.addItem(playlist_item)

            if self.playlist:
                self.playlist_view.setCurrentRow(0)
                self.current_index = 0
                self.player.setSource(self.playlist[0])

    def open_directory(self):
        """Open the selected directory and add the files within to an empty playlist."""
        directory = QFileDialog.getExistingDirectory(self, 'Open Directory', '', QFileDialog.Option.ReadOnly)

        if directory:
            self.playlist.clear()
            self.playlist_view.clear()
            for dirpath, __, files in os.walk(directory):
                for filename in natsort.natsorted(files, alg=natsort.ns.PATH):
                    file = os.path.join(dirpath, filename)
                    if filename.lower().endswith(('.mp3', '.flac')):
                        self.playlist.append(QUrl.fromLocalFile(os.path.join(dirpath, filename)))
                        playlist_item = QListWidgetItem(filename)
                        playlist_item.setToolTip(filename)
                        self.playlist_view.addItem(playlist_item)

            self.playlist_view.setCurrentRow(0)
            self.play_index(0)

    def open_media_library(self, index):
        """Open a directory or file from the media library into an empty playlist."""
        for index in self.library_view.selectedIndexes():
            if self.library_view.media_model.fileName(index).lower().endswith(('.mp3', '.flac')):
                file = self.library_view.media_model.filePath(index)
                track_name = os.path.basename(self.library_view.media_model.fileName(index))
                self.playlist.append(QUrl().fromLocalFile(file))
                playlist_item = QListWidgetItem(track_name)
                playlist_item.setToolTip(track_name)
                self.playlist_view.addItem(playlist_item)

            elif self.library_view.media_model.isDir(index):
                directory = self.library_view.media_model.filePath(index)
                for dirpath, __, files in os.walk(directory):
                    for filename in natsort.natsorted(files, alg=natsort.ns.PATH):
                        file = os.path.join(dirpath, filename)
                        if filename.lower().endswith(('.mp3', '.flac')):
                            self.playlist.append(QUrl().fromLocalFile(file))
                            track_name = os.path.splitext(filename)[0]
                            playlist_item = QListWidgetItem(track_name)
                            playlist_item.setToolTip(track_name)
                            self.playlist_view.addItem(playlist_item)

        if self.current_index == -1:
            self.play_index(0)

    def display_meta_data(self):
        """Display the current song's metadata in the main window.

        If the current song contains metadata, its cover art is extracted and shown in
        the main window while the track number, artist, album, and track title are shown
        in the window title.
        """        
        file_path = self.player.source().toLocalFile()
        (album, artist, title, track_number, *__, artwork) = metadata.metadata(file_path)

        try:
            self.pixmap.loadFromData(artwork)
        except TypeError:
            self.pixmap = QPixmap(artwork)

        meta_data = '{} - {} - {} - {}' .format(track_number.zfill(2), artist, album, title)

        self.setWindowTitle(meta_data)
        self.art.setScaledContents(True)
        self.art.setPixmap(self.pixmap)
        self.player_layout.addWidget(self.art)

    def press_playback(self, event):
        """Change the playback of the player on cover art mouse event.

        When the cover art is clicked, the player will play the media if the player is
        either paused or stopped. If the media is playing, the media is set
        to pause.
        """
        if event.button() == Qt.MouseButton.LeftButton and self.settings.config['playback']['cover_art']:
            if (self.player.playbackState() == QMediaPlayer.PlaybackState.StoppedState or
                    self.player.playbackState() == QMediaPlayer.PlaybackState.PausedState):
                self.player.play()
            elif self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
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
            time_played = QTime((current_duration // 3600) % 60,
                                (current_duration // 60) % 60,
                                (current_duration % 60),
                                (current_duration * 1000) % 1000,
                                )
            song_length = QTime((duration // 3600) % 60,
                                (duration // 60) % 60,
                                (duration % 60),
                                (duration * 1000) % 1000,
                                )

            if duration > 3600:
                time_format = "hh:mm:ss"
            else:
                time_format = "mm:ss"

            time_display = "{} / {}" .format(time_played.toString(time_format), song_length.toString(time_format))

        else:
            time_display = ""

        self.duration_label.setText(time_display)

    def toggle_playback(self):
        """Play or pause depending on the current playback state."""
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.player.pause()
        else:
            self.player.play()

    def set_state(self, state):
        """Change the icon in the toolbar in relation to the state of the player.

        The play icon changes to the pause icon when a song is playing and
        the pause icon changes back to the play icon when either paused or
        stopped.
        """
        if self.player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            pause_icon = utilities.resource_filename('mosaic.images', 'md_pause.png')
            self.play_action.setIcon(QIcon(pause_icon))
        else:
            play_icon = utilities.resource_filename('mosaic.images', 'md_play.png')
            self.play_action.setIcon(QIcon(play_icon))

    def previous(self):
        """Move to the previous song in the playlist.

        Moves to the previous song in the playlist if the current song is less
        than five seconds in. Otherwise, restarts the current song.
        """
        if self.player.position() > 5000:
            self.player.setPosition(0)
        elif self.current_index > 0:
            self.play_index(self.current_index - 1)

    def next(self):
        if self.current_index < len(self.playlist) - 1:
            self.play_index(self.current_index + 1)

    def activate_playlist_item(self, item):
        """Set the active media to the playlist item double-clicked on by the user."""
        self.play_index(self.playlist_view.row(item))

    def remove_from_playlist(self):
        """Remove selected tracks from the playlist."""
        rows = sorted({self.playlist_view.row(item) for item in self.playlist_view.selectedItems()},
                      reverse=True)
        for row in rows:
            self.playlist_view.takeItem(row)
            del self.playlist[row]

            if row == self.current_index:
                self.player.stop()
                self.current_index = -1
            elif row < self.current_index:
                self.current_index -= 1

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
            self.resize(self.settings.window_size, self.settings.window_size)

            if self.library_dock_state:
                self.library_dock.setVisible(True)

            if self.playlist_dock_state:
                self.playlist_dock.setVisible(True)

    def dock_visibility_change(self, visible):
        """Change the size of the main window when the docks are toggled."""
        if visible and self.playlist_dock.isVisible() and not self.library_dock.isVisible():
            self.resize(self.settings.window_size + self.playlist_dock.width() + 6,
                        self.height())

        elif visible and not self.playlist_dock.isVisible() and self.library_dock.isVisible():
            self.resize(self.settings.window_size + self.library_dock.width() + 6,
                        self.height())

        elif visible and self.playlist_dock.isVisible() and self.library_dock.isVisible():
            self.resize(self.settings.window_size + self.library_dock.width() + 6,
                        self.height())

        elif (not visible and not self.playlist_dock.isVisible() and not
                self.library_dock.isVisible()):
            self.resize(self.settings.window_size, self.settings.window_size)

    def media_information_dialog(self):
        """Show a dialog of the current song's metadata."""
        if self.player.metaData():
            file_path = self.player.source().toLocalFile()
        else:
            file_path = None
        dialog = information.InformationDialog(file_path)
        dialog.exec_()

    def change_window_size(self):
        """Change the window size of the music player."""
        # This fires as soon as the dropdown changes - before the preferences
        # dialog closes - so self.settings is still stale. Reload to pick up
        # the freshly-written value.
        self._reload_settings()
        self.playlist_dock.close()
        self.library_dock.close()
        self.resize(self.settings.window_size, self.settings.window_size)

    def change_media_library_path(self, path):
        """Change the media library path to the new path selected in the preferences dialog."""
        self.library_view.media_model.setRootPath(path)
        self.library_view.setRootIndex(self.library_view.media_model.index(path))


    def reload_settings(self):
        """Re-read settings.toml after the preferences dialog closes.

        The cached self.settings object is replaced so subsequent reads
        (dock position, window size, cover-art playback, etc.) see the
        values the user just saved.
        """
        self.settings = defaults.Settings()

    def closeEvent(self, event):
        """Override the PyQt close event in order to handle save playlist on close."""
        if self.settings.save_playlist_on_close:
            self.save_playlist()

        QApplication.quit()


def main():
    """Create an instance of the music player and use QApplication to show the GUI.

    QDesktopWidget() is used to move the application to the center of the user's screen.
    """
    # os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"
    os.environ["QT_LOGGING_RULES"] = "qt.multimedia.*=false"

    application = QApplication(sys.argv)
    window = MusicPlayer()

    desktop = application.primaryScreen().availableGeometry()

    if window.width() > desktop.width() or window.height() > desktop.height():
        window.resize(desktop.width(), desktop.height())

    width = (desktop.width() - window.width()) // 2
    height = (desktop.height() - window.height()) // 2

    window.show()
    window.move(width, height)
    sys.exit(application.exec_())
