import mosaic.configuration
import mosaic.metadata
import mutagen.easyid3
import mutagen.flac
import mutagen.mp3
import os
import pkg_resources
import pytoml
import sys
from appdirs import AppDirs
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer, QMediaPlaylist
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QAction, QApplication, QDesktopWidget, QDialog,
                             QDockWidget, QFileDialog, QHBoxLayout, QLabel,
                             QListWidget, QMainWindow, QMessageBox, QSlider,
                             QStackedWidget, QToolBar)
from PyQt5.QtCore import Qt, QByteArray,  QDir, QFileInfo, QTime, QUrl


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

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.content = QMediaContent()
        self.art = QLabel()
        self.slider = QSlider(Qt.Horizontal)
        self.duration_label = QLabel()
        self.sidebar = QDockWidget('Playlist', self)
        self.playlist_view = QListWidget()

        self.setCentralWidget(self.art)
        self.slider.setRange(0, self.player.duration() / 1000)

        self.addDockWidget(Qt.RightDockWidgetArea, self.sidebar)
        self.sidebar.setWidget(self.playlist_view)
        self.sidebar.setFloating(True)
        self.sidebar.setGeometry(0, 0, 300, 800)
        self.sidebar.setVisible(False)

        self.player.metaDataChanged.connect(self.display_meta_data)
        self.slider.sliderMoved.connect(self.seek)
        self.player.durationChanged.connect(self.song_duration)
        self.player.positionChanged.connect(self.song_position)
        self.player.stateChanged.connect(self.set_state)
        self.playlist_view.currentRowChanged.connect(self.change_item)
        self.playlist.currentIndexChanged.connect(self.change_index)

        self.art.mousePressEvent = self.press_playback

        self.duration = 0
        self.config_directory = AppDirs('mosaic', 'Mandeep').user_config_dir
        self.create_settings_file()

        self.menu_controls()
        self.media_controls()

        self.setFixedSize(900, 963)

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

        self.view_media_info_action = QAction('Media Information', self)
        self.view_media_info_action.triggered.connect(self.view_media_info)

        self.view.addAction(self.dock_action)
        self.view.addAction(self.view_media_info_action)

    def help_menu(self):
        """Provides informational items regarding the application."""
        self.about_action = QAction('About', self)
        self.about_action.triggered.connect(self.about_dialog)

        self.help_.addAction(self.about_action)

    def open_file(self):
        """Opens the selected file and adds it to a new playlist."""
        filename, ok = QFileDialog.getOpenFileName(
            self, 'Open File', self.media_library_path(), 'Audio (*.mp3 *.flac)')
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
            self, 'Open Multiple Files', self.media_library_path(), 'Audio (*.mp3 *.flac)')
        if ok:
            self.playlist.clear()
            self.playlist_view.clear()
            for file in filenames:
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
            self, 'Open Playlist', self.media_library_path(), 'Playlist (*.m3u *.pls)')
        if ok:
            playlist = QUrl.fromLocalFile(playlist)
            self.playlist.clear()
            self.playlist_view.clear()
            self.playlist.load(playlist)
            self.player.setPlaylist(self.playlist)
            self.player.play()

            for song_index in range(self.playlist.mediaCount()+1):
                song = self.playlist.media(song_index).canonicalUrl().fileName()
                self.playlist_view.addItem(song)

    def open_directory(self):
        """Opens the chosen directory and adds supported audio filetypes within
        the directory to an empty playlist"""
        settings_stream = os.path.join(self.config_directory, 'settings.toml')
        with open(settings_stream) as conffile:
            config = pytoml.load(conffile)

        directory = QFileDialog.getExistingDirectory(self, 'Open Directory', self.media_library_path())
        if directory:
            self.playlist.clear()
            self.playlist_view.clear()
            contents = QDir(directory).entryInfoList()

            for filename in contents:
                if config['file_options']['recursive_directory'] is False:
                    file = filename.absoluteFilePath()
                    if file.endswith('mp3') or file.endswith('flac'):
                        self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(file)))
                        self.playlist_view.addItem(filename.fileName())
                        self.playlist_view.setCurrentRow(0)
                        self.player.setPlaylist(self.playlist)
                elif config['file_options']['recursive_directory'] is True:
                    if filename.isDir():
                        sub_directory = QDir(filename.filePath()).entryInfoList()
                        for sub_files in sub_directory:
                            sub_file = sub_files.absoluteFilePath()
                            if sub_file.endswith('mp3') or sub_file.endswith('flac'):
                                self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(sub_file)))
                                self.player.setPlaylist(self.playlist)
                                self.playlist_view.addItem(sub_files.fileName())
                                self.playlist_view.setCurrentRow(0)
            self.player.play()

    def exit_application(self):
        """Closes the window and quits the music player application."""
        QApplication.quit()

    def preferences(self):
        """Opens a dialog with user configurable options."""
        dialog = mosaic.configuration.PreferencesDialog()
        dialog.exec_()

    def view_media_info(self):
        """Creates a dialog window displaying all of the metadata
        available in the audio file. mosaic.metadata.MediaInformation
        is instantiated to fill the dialog window with the necessary
        widgets and layouts."""
        dialog = QDialog()
        dialog.setWindowTitle('Media Information')
        info_icon = pkg_resources.resource_filename('mosaic.images', 'md_info.png')
        dialog.setWindowIcon(QIcon(info_icon))
        dialog.setFixedSize(600, 600)

        if self.player.isMetaDataAvailable():
            file_path = self.player.currentMedia().canonicalUrl().path()

            if file_path.endswith('mp3'):
                song = mutagen.mp3.MP3(file_path, ID3=mutagen.easyid3.EasyID3)
            elif file_path.endswith('flac'):
                song = mutagen.flac.FLAC(file_path)

            song_data = dict(song.tags)
            song_data = dict((k, "".join(v)) for k, v in song_data.items())

            artist = song_data.get('artist', '')
            album = song_data.get('album', '')
            date = song_data.get('date', '')
            title = song_data.get('title', '')
            track_number = song_data.get('tracknumber', '')
            genre = song_data.get('genre', '')
            description = song_data.get('description', '')
            sample_rate = "{} Hz" .format(song.info.sample_rate)
            try:
                bitrate = "{} kb/s" .format(song.info.bitrate // 1000)
                bitrate_mode = "{}" .format(song.info.bitrate_mode)
            except AttributeError:
                bitrate = ''
                bitrate_mode = ''
            try:
                bits_per_sample = "{}" .format(song.info.bits_per_sample)
            except AttributeError:
                bits_per_sample = ''

            media_information = mosaic.metadata.MediaInformation(
                artist, album, date, title, track_number, genre, bitrate,
                bitrate_mode, sample_rate, bits_per_sample, description)
        else:
            media_information = mosaic.metadata.MediaInformation(
                '', '', '', '', '', '', '', '', '', '', '')

        page = QStackedWidget()
        page.addWidget(media_information)

        dialog_layout = QHBoxLayout()
        dialog_layout.addWidget(page)

        dialog.setLayout(dialog_layout)
        dialog.exec_()

    def about_dialog(self):
        """Pops up a dialog that shows application informaion."""
        message = QMessageBox()
        message.setWindowTitle('About')
        help_icon = pkg_resources.resource_filename('mosaic.images', 'md_help.png')
        message.setWindowIcon(QIcon(help_icon))
        message.setText('Created by Mandeep Bhutani')
        message.setInformativeText('Material design icons created by Google\n\n'
                                   'GitHub: mandeepbhutani')
        message.exec_()

    def display_meta_data(self):
        """QPixmap() is initiated in order to send an image to QLabel() which then
        displays the image in QMainWindow. When a file is loaded, this function
        affirms that meta data in the audio file exists. The mutagen library is
        imported to retrieve cover art from the meta data. Mp3s and FLAC audio
        formats house pictures differently, so two different methods are used
        to extract the meta data. Once the data (in bytes) is retrieved from
        the audio file, it is appeneded to a QByteArray() which allows the
        data to be passed to QPixmap(). Once QPixmap() receives the data,
        the application's height and width are changed to match that of the
        cover art image."""
        self.pixmap = QPixmap()
        self.byte_array = QByteArray()

        if self.player.isMetaDataAvailable():
            file_path = self.player.currentMedia().canonicalUrl().path()
            no_cover_image = pkg_resources.resource_filename('mosaic.images', 'nocover.png')

            if file_path.endswith('mp3'):
                song = mutagen.mp3.MP3(file_path, ID3=mutagen.easyid3.EasyID3)

                try:
                    mp3_bytes = mutagen.mp3.MP3(file_path)
                    for tag in mp3_bytes:
                        if 'APIC' in tag:
                            artwork = self.byte_array.append(mp3_bytes.tags[tag].data)
                            self.pixmap.loadFromData(artwork)
                except KeyError:
                    self.pixmap = QPixmap(no_cover_image)

            elif file_path.endswith('flac'):
                song = mutagen.flac.FLAC(file_path)

                try:
                    artwork = self.byte_array.append(song.pictures[0].data)
                    self.pixmap.loadFromData(artwork)
                except IndexError:
                    self.pixmap = QPixmap(no_cover_image)

            song_data = dict(song.tags)
            song_data = dict((k, "".join(v)) for k, v in song_data.items())
            album_title = song_data.get('album', '??')
            album_artist = song_data.get('artist', '??')
            track_title = song_data.get('title', '??')
            track_number = song_data.get('tracknumber', '??')

            meta_data = '{} - {} - {} - {}' .format(
                    track_number, album_artist, album_title, track_title)
            self.setWindowTitle(meta_data)

            self.art.setScaledContents(True)
            self.art.setPixmap(self.pixmap)
            self.art.setFixedSize(900, 900)

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

    def change_item(self, row):
        """Changes the current media to the index of the media selected
        in the playlist view by the user."""
        if self.playlist.currentIndex() != row:
            self.playlist.setCurrentIndex(row)

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


def main():
    application = QApplication(sys.argv)
    window = MusicPlayer()
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())
