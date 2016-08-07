import sys
import mutagen
import mutagen.flac
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QMainWindow, QApplication, QToolBar,
                             QAction, QFileDialog, QLabel, QSlider,
                             QDesktopWidget, QMessageBox, QDockWidget,
                             QListWidget, QDialog, QStackedWidget)
from PyQt5.QtCore import Qt, QUrl, QByteArray, QTime, QDir, QFileInfo


class MusicPlayer(QMainWindow):

    def __init__(self, parent=None):
        """Initializes the QMainWindow widget and calls methods that house
        other widgets that need to be displayed in the main window."""
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Mosaic')
        self.setWindowIcon(QIcon('images/icon.png'))

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

        self.player.metaDataChanged.connect(self.retrieve_meta_data)
        self.slider.sliderMoved.connect(self.seek)
        self.player.durationChanged.connect(self.song_duration)
        self.player.positionChanged.connect(self.song_position)
        self.player.stateChanged.connect(self.set_state)

        self.art.mousePressEvent = self.press_playback

        self.duration = 0

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

        self.play_action = QAction(QIcon('images/md_play.png'), 'Play', self)
        self.play_action.triggered.connect(self.player.play)

        self.stop_action = QAction(QIcon('images/md_stop.png'), 'Stop', self)
        self.stop_action.triggered.connect(self.player.stop)

        self.previous_action = QAction(QIcon('images/md_previous.png'), 'Previous', self)
        self.previous_action.triggered.connect(self.playlist.previous)

        self.next_action = QAction(QIcon('images/md_next.png'), 'Next', self)
        self.next_action.triggered.connect(self.playlist.next)

        self.repeat_action = QAction(QIcon('images/md_repeat.png'), 'Repeat', self)
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

        self.open_directory_action = QAction('Open Directory', self)
        self.open_directory_action.setShortcut('CTRL+D')
        self.open_directory_action.triggered.connect(self.open_directory)

        self.exit_action = QAction('Quit', self)
        self.exit_action.setShortcut('CTRL+Q')
        self.exit_action.triggered.connect(self.exit_application)

        self.file.addAction(self.open_action)
        self.file.addAction(self.open_multiple_files_action)
        self.file.addAction(self.open_directory_action)
        self.file.addSeparator()
        self.file.addAction(self.exit_action)

    def edit_menu(self):
        """"""
        self.preferences_action = QAction('Preferences', self)
        self.preferences_action.setShortcut('CTRL+P')
        self.preferences_action.triggered.connect(self.preferences)

        self.edit.addAction(self.preferences_action)

    def view_menu(self):
        """Provides items that allow the user to customize the viewing
        experience of the main window."""
        self.dock_action = self.sidebar.toggleViewAction()
        self.view.addAction(self.dock_action)

    def help_menu(self):
        """Provides informational items regarding the application."""
        self.about_action = QAction('About', self)
        self.about_action.triggered.connect(self.about_dialog)

        self.help_.addAction(self.about_action)

    def open_file(self):
        """Opens the selected file and adds it to a new playlist."""
        filename, ok = QFileDialog.getOpenFileUrl(self, 'Open File', '', 'Audio (*.mp3 *.flac)')
        if ok:
            self.playlist.clear()
            self.playlist_view.clear()
            self.playlist.addMedia(QMediaContent(filename))
            self.player.setPlaylist(self.playlist)
            self.playlist_view.addItem(filename.fileName())
            self.player.play()

    def open_multiple_files(self):
        """Opens the selected files and adds them to a new playlist."""
        filenames, ok = QFileDialog.getOpenFileUrls(self, 'Open Multiple Files', '', 'Audio (*.mp3 *.flac)')
        if ok:
            self.playlist.clear()
            self.playlist_view.clear()
            for file in filenames:
                self.playlist.addMedia(QMediaContent(file))
                self.player.setPlaylist(self.playlist)
                self.playlist_view.addItem(file.fileName())
            self.player.play()

    def open_directory(self):
        """Opens the chosen directory and adds supported audio filetypes within
        the directory to an empty playlist"""
        directory = QFileDialog.getExistingDirectory(self, 'Open Directory')
        if directory:
            self.playlist.clear()
            self.playlist_view.clear()
            contents = QDir(directory).entryInfoList()
            for filename in contents:
                file = filename.absoluteFilePath()
                if file.endswith('mp3') or file.endswith('flac'):
                    self.playlist.addMedia(QMediaContent(QUrl().fromLocalFile(file)))
                    self.player.setPlaylist(self.playlist)
                    self.playlist_view.addItem(filename.fileName())
                    self.player.play()

    def exit_application(self):
        """Closes the window and quits the music player application."""
        QApplication.quit()

    def preferences(self):
        """"""
        dialog = QDialog()
        layout = QStackedWidget(dialog)
        dialog.setWindowTitle('Preferences')
        dialog.exec_()

    def about_dialog(self):
        """Pops up a dialog that shows application informaion."""
        message = QMessageBox()
        message.setWindowTitle('Mosaic')
        message.setText('Created by Mandeep Bhutani')
        message.setInformativeText('Material design icons created by Google\n\n'
                                   'GitHub: mandeepbhutani')
        message.exec_()

    def retrieve_meta_data(self):
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
            if file_path.endswith('mp3'):
                song = mutagen.File(file_path)
                album_title = song.get('TALB', '??')
                album_artist = song.get('TPE1', '??')
                track_title = song.get('TIT2', '??')
                track_number = song.get('TRCK', '??')
                try:
                    for tag in song.tags:
                        if 'APIC' in tag:
                            artwork = self.byte_array.append(song.tags[tag].data)
                    self.pixmap.loadFromData(artwork)
                except KeyError:
                    self.pixmap = QPixmap('images/nocover.png', 'png')
            elif file_path.endswith('flac'):
                song = mutagen.flac.FLAC(file_path)
                song_data = dict(song.tags)
                song_data = dict((k, "".join(v)) for k, v in song_data.items())
                album_title = song_data.get('album', '??')
                album_artist = song_data.get('artist', '??')
                track_title = song_data.get('title', '??')
                track_number = song_data.get('tracknumber', '??')
                try:
                    artwork = self.byte_array.append(song.pictures[0].data)
                    self.pixmap.loadFromData(artwork)
                except IndexError:
                    self.pixmap = QPixmap('images/nocover.png', 'png')

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
            self.play_action.setIcon(QIcon('images/md_pause.png'))
            self.play_action.triggered.connect(self.player.pause)
        elif (self.player.state() == QMediaPlayer.PausedState or
              self.player.state() == QMediaPlayer.StoppedState):
            self.play_action.triggered.connect(self.player.play)
            self.play_action.setIcon(QIcon('images/md_play.png'))

    def repeat_song(self):
        """Sets the current media to repeat and changes the repeat icon
        accordingly."""
        if self.playlist.playbackMode() != QMediaPlaylist.CurrentItemInLoop:
            self.playlist.setPlaybackMode(QMediaPlaylist.CurrentItemInLoop)
            self.repeat_action.setIcon(QIcon('images/md_repeat_on.png'))
        elif self.playlist.playbackMode() == QMediaPlaylist.CurrentItemInLoop:
            self.playlist.setPlaybackMode(QMediaPlaylist.Sequential)
            self.repeat_action.setIcon(QIcon('images/md_repeat.png'))


def main():
    application = QApplication(sys.argv)
    window = MusicPlayer()
    desktop = QDesktopWidget().availableGeometry()
    width = (desktop.width() - window.width()) / 2
    height = (desktop.height() - window.height()) / 2
    window.show()
    window.move(width, height)
    sys.exit(application.exec_())

main()
