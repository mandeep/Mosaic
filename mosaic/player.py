from appdirs import AppDirs
from mosaic import configuration, library, metadata
from mutagen import easyid3, flac, mp3
import natsort
import os
import pkg_resources
from PyQt5.QtCore import Qt, QByteArray, QFileInfo, QTime, QUrl
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget, QDialog,
                             QDockWidget, QFileDialog, QHBoxLayout, QLabel,
                             QListWidget, QMainWindow, QMessageBox, QSlider,
                             QTabWidget, QToolBar)
import pytoml
import sys


class MusicPlayer(QMainWindow):
    """MusicPlayer houses all of the methods and attributes needed to
    instantiate a fully functional music player."""

    def __init__(self, parent=None):
        """Initializes the QMainWindow widget and calls methods that house
        other widgets that need to be displayed in the main window."""
        super(MusicPlayer, self).__init__(parent)
        self.setWindowTitle('Mosaic')
        window_icon = pkg_resources.resource_filename('mosaic.images', 'icon.png')
        self.setWindowIcon(QIcon(window_icon))

        # Initiate Qt objects to be used by MusicPlayer
        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.content = QMediaContent()
        self.art = QLabel()
        self.pixmap = QPixmap()
        self.slider = QSlider(Qt.Horizontal)
        self.duration_label = QLabel()
        self.sidebar = QDockWidget('Playlist', self)
        self.library = QDockWidget('Media Library', self)
        self.playlist_view = QListWidget()
        self.library_view = library.MediaLibraryView()
        self.library_model = library.MediaLibraryModel()

        # Sets the cover art as the central widget of the main window
        self.setCentralWidget(self.art)

        # Initiates the playlist dock widget and sets it as invisible until toggled on
        self.addDockWidget(Qt.RightDockWidgetArea, self.sidebar)
        self.sidebar.setWidget(self.playlist_view)
        self.sidebar.setFloating(True)
        self.sidebar.resize(300, 800)
        self.sidebar.setVisible(False)

        self.addDockWidget(Qt.RightDockWidgetArea, self.library)
        self.library.setWidget(self.library_view)
        self.library.setFloating(True)
        self.library.resize(400, 800)
        self.library.setVisible(False)

        # Sets the range of the playback slider and sets the playback mode as looping
        self.slider.setRange(0, self.player.duration() / 1000)
        self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)

        # Initiates the settings file and preferences dialog
        self.config_directory = AppDirs('mosaic', 'Mandeep').user_config_dir
        self.create_settings_file()
        self.preferences_dialog = configuration.PreferencesDialog()

        # Signals that connect to other methods when they're called
        self.player.metaDataChanged.connect(self.display_meta_data)
        self.slider.sliderMoved.connect(self.seek)
        self.player.durationChanged.connect(self.song_duration)
        self.player.positionChanged.connect(self.song_position)
        self.player.stateChanged.connect(self.set_state)
        self.playlist_view.currentRowChanged.connect(self.playlist_item)
        self.library_view.activated.connect(self.media_library_item)
        self.playlist.currentIndexChanged.connect(self.change_index)
        self.preferences_dialog.finished.connect(self.window_size)
        self.art.mousePressEvent = self.press_playback

        # Creating the menu controls, media controls, and window size of the music player
        self.menu_controls()
        self.media_controls()
        self.window_size()

        # Creating variables to be used for meta data
        self.duration = 0
        self.metadata = None
        self.artwork = None
        self.album = None
        self.artist = None
        self.title = None
        self.track_number = None
        self.date = None
        self.genre = None
        self.description = None
        self.sample_rate = None
        self.bitrate = None
        self.bitrate_mode = None
        self.bits_per_sample = None

    def menu_controls(self):
        """Initiates the menu bar and adds it to the QMainWindow widget."""
        self.menu = self.menuBar()
        self.file = self.menu.addMenu('File')
        self.edit = self.menu.addMenu('Edit')
        self.view = self.menu.addMenu('View')
        self.help_ = self.menu.addMenu('Help')

        self.file_menu()
        self.edit_menu()
        self.view_menu()
        self.help_menu()

    def media_controls(self):
        """Creates the bottom toolbar and controls used for media playback."""
        self.toolbar = QToolBar()
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
        self.previous_action.triggered.connect(self.playlist.previous)

        next_icon = pkg_resources.resource_filename('mosaic.images', 'md_next.png')
        self.next_action = QAction(QIcon(next_icon), 'Next', self)
        self.next_action.triggered.connect(self.playlist.next)

        repeat_icon = pkg_resources.resource_filename('mosaic.images', 'md_repeat.png')
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
        """Adds a file menu to the menu bar. Allows the user to choose actions
        related to audio files."""
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
        self.exit_action.triggered.connect(self.exit_application)

        self.file.addAction(self.open_action)
        self.file.addAction(self.open_multiple_files_action)
        self.file.addAction(self.open_playlist_action)
        self.file.addAction(self.open_directory_action)
        self.file.addSeparator()
        self.file.addAction(self.exit_action)

    def edit_menu(self):
        """Provides items that allow the user to customize
        the options of the music player."""
        self.preferences_action = QAction('Preferences', self)
        self.preferences_action.setShortcut('CTRL+SHIFT+P')
        self.preferences_action.triggered.connect(self.preferences)

        self.edit.addAction(self.preferences_action)

    def view_menu(self):
        """Provides items that allow the user to customize the viewing
        experience of the main window."""
        self.dock_action = self.sidebar.toggleViewAction()
        self.dock_action.setShortcut('CTRL+ALT+P')

        self.library_dock_action = self.library.toggleViewAction()
        self.library_dock_action.setShortcut('CTRL+ALT+L')

        self.view_media_info_action = QAction('Media Information', self)
        self.view_media_info_action.setShortcut('CTRL+SHIFT+M')
        self.view_media_info_action.triggered.connect(self.view_media_info)

        self.view.addAction(self.dock_action)
        self.view.addAction(self.library_dock_action)
        self.view.addAction(self.view_media_info_action)

    def help_menu(self):
        """Provides informational items regarding the application."""
        self.about_action = QAction('About', self)
        self.about_action.setShortcut('CTRL+H')
        self.about_action.triggered.connect(self.about_dialog)

        self.help_.addAction(self.about_action)

    def open_file(self):
        """Opens the selected file and adds it to a new playlist."""
        filename, ok = QFileDialog.getOpenFileName(
            self, 'Open File', self.media_library_path(), 'Audio (*.mp3 *.flac)', '',
            QFileDialog.ReadOnly)
        if ok:
            file_info = QFileInfo(filename).fileName()
            self.playlist.clear()
            self.playlist_view.clear()
            self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(filename)))
            self.player.setPlaylist(self.playlist)
            self.playlist_view.addItem(file_info)
            self.playlist_view.setCurrentRow(0)
            self.player.play()

    def open_multiple_files(self):
        """Opens the selected files and adds them to a new playlist."""
        filenames, ok = QFileDialog.getOpenFileNames(
            self, 'Open Multiple Files', self.media_library_path(), 'Audio (*.mp3 *.flac)', '',
            QFileDialog.ReadOnly)
        if ok:
            self.playlist.clear()
            self.playlist_view.clear()
            for file in natsort.natsorted(filenames, alg=natsort.ns.PATH):
                file_info = QFileInfo(file).fileName()
                self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(file)))
                self.player.setPlaylist(self.playlist)
                self.playlist_view.addItem(file_info)
                self.playlist_view.setCurrentRow(0)
                self.player.play()

    def open_playlist(self):
        """Loads an m3u or pls file into an empty playlist and adds the
        content of the chosen playlist to playlist_view."""
        playlist, ok = QFileDialog.getOpenFileName(
            self, 'Open Playlist', self.media_library_path(), 'Playlist (*.m3u *.pls)', '',
            QFileDialog.ReadOnly)
        if ok:
            playlist = QUrl.fromLocalFile(playlist)
            self.playlist.clear()
            self.playlist_view.clear()
            self.playlist.load(playlist)
            self.player.setPlaylist(self.playlist)

            for song_index in range(self.playlist.mediaCount()+1):
                song = self.playlist.media(song_index).canonicalUrl().fileName()
                self.playlist_view.addItem(song)

            self.player.play()

    def open_directory(self):
        """Opens the chosen directory and adds supported audio filetypes within
        the directory to an empty playlist."""
        settings_stream = os.path.join(self.config_directory, 'settings.toml')
        with open(settings_stream) as conffile:
            config = pytoml.load(conffile)

        directory = QFileDialog.getExistingDirectory(
            self, 'Open Directory', self.media_library_path(), QFileDialog.ReadOnly)
        if directory:
            self.playlist.clear()
            self.playlist_view.clear()

            if config['file_options']['recursive_directory'] is False:
                for filename in natsort.natsorted(os.listdir(directory), alg=natsort.ns.PATH):
                    file = os.path.join(directory, filename)
                    if filename.endswith(('mp3', 'flac')):
                        self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(file)))
                        self.playlist_view.addItem(filename)

            elif config['file_options']['recursive_directory'] is True:
                for dirpath, dirnames, files in os.walk(directory):
                    for filename in natsort.natsorted(files, alg=natsort.ns.PATH):
                        file = os.path.join(dirpath, filename)
                        if filename.endswith(('mp3', 'flac')):
                            self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(file)))
                            self.playlist_view.addItem(filename)

            self.player.setPlaylist(self.playlist)
            self.playlist_view.setCurrentRow(0)
            self.player.play()

    def retrieve_meta_data(self, file):
        """The mutagen library is imported to retrieve meta data from the opened audio file.
        Mp3s and FLAC audio formats house pictures differently, so two different methods
        are used to extract the meta data. Once the artwork data (in bytes) is retrieved from
        the audio file, it is appeneded to a QByteArray()."""
        if file.endswith('mp3'):
            song = mp3.MP3(file, ID3=easyid3.EasyID3)

            for tag in mp3.MP3(file):
                try:
                    if 'APIC' in tag:
                        self.artwork = QByteArray().append(mp3.MP3(file)[tag].data)
                except KeyError:
                    self.artwork = pkg_resources.resource_filename('mosaic.images', 'nocover.png')

        elif file.endswith('flac'):
            song = flac.FLAC(file)

            try:
                self.artwork = QByteArray().append(song.pictures[0].data)
            except IndexError:
                self.artwork = pkg_resources.resource_filename('mosaic.images', 'nocover.png')

        song_data = dict(song.tags)
        song_data = dict((k, "".join(v)) for k, v in song_data.items())
        self.metadata = song_data
        self.album = song_data.get('album', '??')
        self.artist = song_data.get('artist', '??')
        self.title = song_data.get('title', '??')
        self.track_number = song_data.get('tracknumber', '??')
        self.date = song_data.get('date', '')
        self.genre = song_data.get('genre', '')
        self.description = song_data.get('description', '')
        self.sample_rate = "{} Hz" .format(song.info.sample_rate)

        try:  # Bitrate only applies to mp3 files
            self.bitrate = "{} kb/s" .format(song.info.bitrate // 1000)
            self.bitrate_mode = "{}" .format(song.info.bitrate_mode)
        except AttributeError:
            self.bitrate = ''
            self.bitrate_mode = ''
        try:  # Bits per sample only applies to flac files
            self.bits_per_sample = "{}" .format(song.info.bits_per_sample)
        except AttributeError:
            self.bits_per_sample = ''

    def display_meta_data(self):
        """QPixmap() is initiated in order to send an image to QLabel() which then
        displays the image in QMainWindow. When a file is loaded, this function
        affirms that meta data in the audio file exists."""
        if self.player.isMetaDataAvailable():
            file_path = self.player.currentMedia().canonicalUrl().toLocalFile()
            self.retrieve_meta_data(file_path)

            try:
                self.pixmap.loadFromData(self.artwork)
            except:
                self.pixmap = QPixmap(self.artwork)

            meta_data = '{} - {} - {} - {}' .format(
                    self.track_number, self.artist, self.album, self.title)
            self.setWindowTitle(meta_data)

            self.art.setScaledContents(True)
            self.art.setPixmap(self.pixmap)

    def view_media_info(self):
        """Creates a dialog window displaying all of the metadata
        available in the audio file. mosaic.metadata.GeneralInformation
        is instantiated to fill the dialog window with the necessary
        widgets and layouts."""
        dialog = QDialog()
        dialog.setWindowTitle('Media Information')
        info_icon = pkg_resources.resource_filename('mosaic.images', 'md_info.png')
        dialog.setWindowIcon(QIcon(info_icon))
        dialog.setFixedSize(600, 600)
        if self.player.isMetaDataAvailable():
            media_information = metadata.GeneralInformation(
                self.artist, self.album, self.date, self.title, self.track_number,
                self.genre, self.bitrate, self.bitrate_mode, self.sample_rate,
                self.bits_per_sample, self.description)
            metadata_information = metadata.FullInformation(self.metadata)
        else:
            media_information = metadata.GeneralInformation()
            metadata_information = metadata.FullInformation()

        page = QTabWidget()
        page.addTab(media_information, 'General')
        page.addTab(metadata_information, 'Metadata')

        dialog_layout = QHBoxLayout()
        dialog_layout.addWidget(page)

        dialog.setLayout(dialog_layout)
        dialog.exec_()

    def press_playback(self, event):
        """On mouse event, the player will play the media if the player is
        either paused or stopped. If the media is playing, the media is set
        to pause."""
        if (self.player.state() == QMediaPlayer.StoppedState or
                self.player.state() == QMediaPlayer.PausedState):
            self.player.play()
        elif self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()

    def seek(self, seconds):
        """When the user drags the horizontal slider, this function sets
        the position of the song to the position dragged to."""
        self.player.setPosition(seconds * 1000)

    def song_duration(self, duration):
        """Sets the slider to the duration of the currently played media."""
        duration /= 1000
        self.duration = duration
        self.slider.setMaximum(duration)

    def song_position(self, progress):
        """As the song plays, the slider moves in sync with the duration
        of the song. The progress is relayed to update_duration() in order
        to display the time label next to the slider."""
        progress /= 1000

        if not self.slider.isSliderDown():
            self.slider.setValue(progress)

        self.update_duration(progress)

    def update_duration(self, current_duration):
        """Calculates the time played and length of the song in time. Both
        of these times are sent to duration_label() in order to display the
        times on the toolbar."""
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
        """Changes the play icon to the pause icon when a song is playing and
        changes the pause icon back to the play icon when either paused or
        stopped. The action of the button changes with respect to its icon."""
        if self.player.state() == QMediaPlayer.PlayingState:
            pause_icon = pkg_resources.resource_filename('mosaic.images', 'md_pause.png')
            self.play_action.setIcon(QIcon(pause_icon))
            self.play_action.triggered.connect(self.player.pause)
        elif (self.player.state() == QMediaPlayer.PausedState or
              self.player.state() == QMediaPlayer.StoppedState):
            self.play_action.triggered.connect(self.player.play)
            play_icon = pkg_resources.resource_filename('mosaic.images', 'md_play.png')
            self.play_action.setIcon(QIcon(play_icon))

    def repeat_song(self):
        """Sets the current media to repeat and changes the repeat icon
        accordingly."""
        if self.playlist.playbackMode() != QMediaPlaylist.CurrentItemInLoop:
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
            repeat_on_icon = pkg_resources.resource_filename('mosaic.images', 'md_repeat_on.png')
            self.repeat_action.setIcon(QIcon(repeat_on_icon))
        elif self.playlist.playbackMode() == QMediaPlaylist.CurrentItemInLoop:
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
            repeat_icon = pkg_resources.resource_filename('mosaic.images', 'md_repeat.png')
            self.repeat_action.setIcon(QIcon(repeat_icon))

    def playlist_item(self, row):
        """Changes the current media to the index of the media selected
        in the playlist view by the user."""
        if self.playlist.currentIndex() != row:
            self.playlist.setCurrentIndex(row)

    def media_library_item(self, index):
        """Allows the user to add a directory or audio file from the media library
        to a new playlist."""
        self.playlist.clear()
        self.playlist_view.clear()

        if self.library_model.fileName(index).endswith(('mp3', 'flac')):
            self.playlist.addMedia(
                QMediaContent(QUrl().fromLocalFile(self.library_model.filePath(index))))
            self.playlist_view.addItem(self.library_model.fileName(index))

        elif self.library_model.isDir(index):
            directory = self.library_model.filePath(index)
            for dirpath, dirnames, files in os.walk(directory):
                for filename in natsort.natsorted(files, alg=natsort.ns.PATH):
                    file = os.path.join(dirpath, filename)
                    if filename.endswith(('mp3', 'flac')):
                        self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(file)))
                        self.playlist_view.addItem(filename)

        self.player.setPlaylist(self.playlist)
        self.player.play()

    def change_index(self, row):
        """Changes the playlist view in relation to the current media."""
        self.playlist_view.setCurrentRow(row)

    def media_library_path(self):
        """Sets the user defined media library path as the default path
        in file dialogs."""
        settings_stream = os.path.join(self.config_directory, 'settings.toml')
        with open(settings_stream) as conffile:
            config = pytoml.load(conffile)

        return config['media_library']['media_library_path']

    def window_size(self):
        """Sets the user defined window size as the size of the current window. The
        sizes list contains widths from 900 to 400. Because the width of the window
        will be the same as the height, there's no need to differentiate between the two. The
        index contained in the settings.toml selects the index from the sizes list and sets
        the window and image size accordingly."""
        settings_stream = os.path.join(self.config_directory, 'settings.toml')
        with open(settings_stream) as conffile:
            config = pytoml.load(conffile)

        sizes = [900, 800, 700, 600, 500, 400]

        try:
            size = sizes[config['view_options']['window_size']]
        except KeyError:
            size = 900

        self.setFixedWidth(size)
        self.setFixedHeight(size + 63)

        self.art.setFixedWidth(size)
        self.art.setFixedHeight(size)

    def create_settings_file(self):
        """Creates a copy of the settings.toml file in the user's system
        config directory. This copy then becomes the default config file
        for user configurable settings."""
        if not os.path.exists(self.config_directory):
            os.makedirs(self.config_directory)

        settings = pkg_resources.resource_filename(__name__, 'settings.toml')
        with open(settings) as default_config:
            config = default_config.read()

        user_config_file = os.path.join(self.config_directory, 'settings.toml')
        if not os.path.isfile(user_config_file):
            with open(user_config_file, 'a') as new_config_file:
                new_config_file.write(config)

    def preferences(self):
        """Opens a dialog with user configurable options."""
        self.preferences_dialog.exec_()

    def about_dialog(self):
        """Pops up a dialog that shows application information."""
        message = QMessageBox()
        message.setWindowTitle('About')
        help_icon = pkg_resources.resource_filename('mosaic.images', 'md_help.png')
        message.setWindowIcon(QIcon(help_icon))
        message.setText('Created by Mandeep Bhutani')
        message.setInformativeText('Material design icons created by Google\n\n'
                                   'GitHub: mandeepbhutani')
        message.exec_()

    def exit_application(self):
        """Closes the window and quits the music player application."""
        QApplication.quit()


def main():
    application = QApplication(sys.argv)
    window = MusicPlayer()
    playlist = window.sidebar
    library = window.library
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)
    playlist.move(width + window.width(), height)
    library.move(width - library.width(), height)
    sys.exit(application.exec_())
