import sys
import mutagen
import mutagen.flac
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QMainWindow, QApplication, QToolBar,
                             QAction, QFileDialog, QLabel, QSlider)
from PyQt5.QtCore import Qt, QUrl, QByteArray, QTime


class MusicPlayer(QMainWindow):

    def __init__(self, parent=None):
        """Initializes the QMainWindow widget and calls methods that house
        other widgets that need to be displayed in the main window.
        """
        QMainWindow.__init__(self, parent)
        self.setWindowTitle('Mosaic')

        self.player = QMediaPlayer()
        self.playlist = QMediaPlaylist()
        self.slider = QSlider(Qt.Horizontal)
        self.duration_label = QLabel()
        self.art = QLabel(self)
        self.setCentralWidget(self.art)

        self.slider.setRange(0, self.player.duration() / 1000)

        self.player.metaDataChanged.connect(self.retrieve_meta_data)
        self.slider.sliderMoved.connect(self.seek)
        self.player.durationChanged.connect(self.song_duration)
        self.player.positionChanged.connect(self.song_position)

        self.art.mousePressEvent = self.press_playback

        self.setWindowIcon(QIcon('images/icon.png'))

        self.duration = 0
        self.filename = None

        self.menu_controls()
        self.media_controls()
        self.file_menu()

        self.retrieve_meta_data()

        self.setFixedSize(900, 952)

    def menu_controls(self):
        """Initiates the menu bar and adds it to the QMainWindow widget.
        """
        self.menu = self.menuBar()
        self.file = self.menu.addMenu('File')

    def media_controls(self):
        """Creates the bottom toolbar and controls used for media playback.
        """
        self.toolbar = QToolBar()
        self.addToolBar(Qt.BottomToolBarArea, self.toolbar)
        self.toolbar.setMovable(False)

        self.play_action = QAction(QIcon().fromTheme('media-playback-start'), 'Play', self)
        self.play_action.triggered.connect(self.player.play)

        self.pause_action = QAction(QIcon().fromTheme('media-playback-pause'), 'Pause', self)
        self.pause_action.triggered.connect(self.player.pause)

        self.stop_action = QAction(QIcon().fromTheme('media-playback-stop'), 'Stop', self)
        self.stop_action.triggered.connect(self.player.stop)

        self.previous_action = QAction(QIcon().fromTheme('media-playback-previous'), 'Previous', self)
        self.previous_action.triggered.connect(self.playlist.previous)

        self.next_action = QAction(QIcon().fromTheme('media-playback-next'), 'Next', self)
        self.next_action.triggered.connect(self.playlist.next)

        self.toolbar.addAction(self.play_action)
        self.toolbar.addAction(self.pause_action)
        self.toolbar.addAction(self.stop_action)
        self.toolbar.addAction(self.previous_action)
        self.toolbar.addAction(self.next_action)
        self.toolbar.addWidget(self.slider)
        self.toolbar.addWidget(self.duration_label)

    def file_menu(self):
        """Adds a file menu to the menu bar. Allows the user to choose actions
        related to audio files."""
        self.open_action = QAction('Open file', self)
        self.open_action.setStatusTip('Open an audio file for playback.')
        self.open_action.setShortcut('CTRL+O')
        self.open_action.triggered.connect(self.open_file)

        self.exit_action = QAction('Quit', self)
        self.exit_action.setStatusTip('Quit the application.')
        self.exit_action.setShortcut('CTRL+Q')
        self.exit_action.triggered.connect(self.exit_application)

        self.file.addAction(self.open_action)
        self.file.addAction(self.exit_action)

    def open_file(self):
        """Retrieves the path of a file and opens it for playback.
        """
        self.filename, ok = QFileDialog.getOpenFileName(self, 'Open file')
        if ok:
            self.player.setMedia(QMediaContent(QUrl().fromLocalFile(self.filename)))
            self.player.play()

    def exit_application(self):
        """Closes the window and quits the music player application.
        """
        QApplication.quit()

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
        cover art image.
        """
        self.pixmap = QPixmap()
        self.byte_array = QByteArray()

        if self.player.isMetaDataAvailable() and self.filename:
            if self.filename.endswith('mp3'):
                song = mutagen.File(self.filename)
                album_title = song.get('TALB', '??')
                album_artist = song.get('TPE1', '??')
                track_title = song.get('TIT2', '??')
                track_number = song.get('TRCK', '??')
                self.setWindowTitle('{} - {} - {} - {}' .format(
                    track_number, album_artist, album_title, track_title))
                try:
                    for tag in song.tags:
                        if 'APIC' in tag:
                            artwork = self.byte_array.append(song.tags[tag].data)
                    self.pixmap.loadFromData(artwork)
                except KeyError:
                    self.pixmap = QPixmap('images/nocover.png', 'png')

            elif self.filename.endswith('flac'):
                song = mutagen.flac.FLAC(self.filename)
                song_data = dict(song.tags)
                song_data = dict((k, "".join(v)) for k, v in song_data.items())
                album_title = song_data.get('album', '??')
                album_artist = song_data.get('artist', '??')
                track_title = song_data.get('title', '??')
                track_number = song_data.get('tracknumber', '??')
                self.setWindowTitle('{} - {} - {} - {}' .format(
                    track_number, album_artist, album_title, track_title))
                try:
                    artwork = self.byte_array.append(song.pictures[0].data)
                    self.pixmap.loadFromData(artwork)
                except IndexError:
                    self.pixmap = QPixmap('images/nocover.png', 'png')

            self.art.setScaledContents(True)
            self.art.setPixmap(self.pixmap)
            self.art.setFixedSize(900, 900)

    def press_playback(self, event):
        """Plays the loaded media if the player is either stopped or paused.
        """
        if self.player.StoppedState or self.player.PausedState:
            self.player.play()

    def seek(self, seconds):
        """When the user drags the horizontal slider, this function sets
        the position of the song to the position dragged to.
        """
        self.player.setPosition(seconds * 1000)

    def song_duration(self, duration):
        """Sets the slider to the duration of the currently played media.
        """
        duration /= 1000
        self.duration = duration
        self.slider.setMaximum(duration)

    def song_position(self, progress):
        """As the song plays, the slider moves in sync with the duration
        of the song. The progress is relayed to update_duration() in order
        to display the time label next to the slider.
        """
        progress /= 1000

        if not self.slider.isSliderDown():
            self.slider.setValue(progress)

        self.update_duration(progress)

    def update_duration(self, current_duration):
        """Calculates the time played and length of the song in time. Both
        of these times are sent to duration_label() in order to display the
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


def main():
    application = QApplication(sys.argv)
    window = MusicPlayer()
    window.show()
    window.move(400, 200)
    sys.exit(application.exec_())

main()
