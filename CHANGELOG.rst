Change Log
==========

All notable changes to this project will be documented in this file.

0.14.2 - 2016-08-27
-------------------

Added
^^^^^

-  New CHANGELOG that describes changes between versions
-  Added CHANGELOG link in README
-  Added test requirements
-  Added Dependency CI badge to README

0.14.1 - 2016-08-26
-------------------

Added
^^^^^

-  Playlist items now have tooltips

0.14.0 - 2016-08-25
-------------------

Added
^^^^^

-  Uploaded license to repository
-  Window now resizes to fit media library and playlist docks so that cover art size remains the same
-  New screenshots that showcase new features

Changed
^^^^^^^

-  Items in media library browser and playlist dock now require double click to play

Removed
^^^^^^^

-  Removed setting for recursive directories as the setting is now default behavior
-  Removed media library from file dialogs now that media library browser has been added

0.13.2 - 2016-08-24
-------------------

Added
^^^^^

- New setting that allows user to show media library on startup
- More unit tests

Changed
^^^^^^^

-  Refactored code into separate modules to increase readability


0.13.1 - 2016-08-23
-------------------

Added
^^^^^

-  63 pixels added to window height to account for menubar and toolbar pixels

0.13.0 - 2016-08-22
-------------------

Added
^^^^^

-  New tab on media information dialog that shows all metadata extracted from current media
-  New media library file browser

Changed
^^^^^^^

-  README install instructions now use pip3 instead of pip

0.12.4 - 2016-08-20
-------------------

Added
^^^^^

-  New badges for PyPI version and License
-  README now displays features

0.12.3 - 2016-08-19
-------------------

Added
^^^^^

-  Widgets now added to Qtbot for proper closing during tests

Fixed
^^^^^

-  Fixed issue where player would crash if user settings file was missing settings

0.12.2 - 2016-08-18
-------------------

Changed
^^^^^^^

-  Rewrote tests to use Pytest fixtures

0.12.1 - 2016-08-17
-------------------

Changed
^^^^^^^

-  Unit tests now use real audio files

0.12.0 - 2016-08-16
-------------------

Added
^^^^^

-  New setting that allows user to change window size


Changed
^^^^^^^

-  Audio files opened are now naturally sorted in playlist

Fixed
^^^^^

-  Fixed issue with MP3 cover art not being extracted from audio file

0.11.4 - 2016-08-15
-------------------

Added
^^^^^

-  New unit tests

Changed
^^^^^^^

-  Refactored recursive open directory item
-  File dialogs are now read only

0.11.3 - 2016-08-14
-------------------

Added
^^^^^

-  New header image for README

0.11.2 - 2016-08-13
-------------------

Added
^^^^^

-  Travis CI, Coveralls, and PyPI badges in README
-  More unit tests for media player
-  More metadata in setup.py
-  PyPI install instructions in README

Fixed
^^^^^

-  Refactored QUrl().path() to QUrl().toLocalFile() for true file path discovery

Removed
^^^^^^^

-  MANIFEST.in

0.11.1 - 2016-08-12
-------------------

Added
^^^^^

-  Link to PyQt5 download page in install instructions
-  Unit tests for media player
-  Continuous integration with Travis CI 

0.11.0 - 2016-08-10
-------------------

Added
^^^^^

-  Media information dialog that displays current media metadata
-  Keyboard shortcut to about dialog
-  Keyboard shortcut to media information dialog

Changed
^^^^^^^

-  Set media library text box now read only

0.10.0 - 2016-08-09
-------------------

Added
^^^^^

-  New method to check for settings file in user config directory
-  New open playlist item in file menu

Changed
^^^^^^^

-  Package renamed from 'player' to 'mosaic'
-  Settings file now created on application open
-  Settings file now uses nested settings for increased readability
-  Changed how mutagen extracts metadata from MP3 files

Fixed
^^^^^

-  Fixed issue with TOML file not reading in correctly

0.9.0 - 2016-08-08
------------------

Added
^^^^^

-  Playlist dock selects index 0 when media added
-  New docstrings for MusicPlayer class and its methods
-  New media library path setting in preferences
-  Keyboard shortcut for playlist dock
-  New window title and icon for about dialog
-  Packages names added to setup.py
-  Imported pkg_resources in order for resources to be correctly shown to users
-  Mutagen, pytoml, and appdirs listed as requirements in setup.py

Changed
^^^^^^^

-  Moved configuration page signal to __init__ 

0.8.0 - 2016-08-07
------------------

Added
^^^^^

-  New edit menu with preferences item
-  Configuration dialog for user preferences
-  User setting that allows user to specify if directories are opened recursively
-  Settings file in TOML format
-  New window icon for preferences dialog
-  New signal for playlist dock to change index of item according to index of media playlist

Changed
^^^^^^^

-  Refactored window title metadata code block for reduced redundancy
-  Rearranged imports in alphabetical order
-  Replaced Object.__init with super()

Fixed
^^^^^

-  Refactored open directory to eliminate directories being opened twice
-  Fixed issue where current media would restart when playlist dock clicked

0.7.1 - 2016-08-06
-------------------

Changed
^^^^^^^

-  Playlist dock now only shows filenames of media in current playlist

0.7.0 - 2016-08-05
------------------

Added
^^^^^

-  statusChanged signal changes toolbar icon according to playback
-  New screenshots that showcase updated icons
-  Opened audio now added to QMediaPlaylist
-  New repeat button and related action
-  Playlist dock clears when new audio opened
-  File dialog now filters for MP3 and FLAC audio filetypes
-  New separator in file menu
-  Capability to open multiple files
-  New keyboard shortcuts to open file dialogs
-  Capability to open directory
-  New help menu with about item


Changed
^^^^^^^

-  Repeat button now repeats current media instead of repeating current playlist
-  repeat_song docstring changed to match new repeat action
-  Metadata code block now tries to identify filetype with string.endswith() method
-  Global filename variable changed to a local variable for each open dialog
-  Renamed open file methods to be more descriptive

Fixed
^^^^^

-  Fixed typo in getOpenFileNames dialog filter so that MP3 and FLAC filetypes show
-  Current playlist now clears when directory opened

Removed
^^^^^^^

-  Status tips as there is no status bar
-  include_package_data removed from setup.py


0.6.2 - 2016-08-04
------------------

Changed
^^^^^^^

-  Switched toolbar icons from system icons to Google Material Design icons

0.6.1 - 2016-08-03
------------------

Added
^^^^^

-  Import QDesktopWidget in order to move application to center of user's screen

0.6.0 - 2016-08-02
------------------

Added
^^^^^

-  Horizontal slider on media toolbar
-  New signals to track position and duration of current media
-  Exit application item in file menu
-  Docstrings written for new methods
-  New screenshots showcasing horizontal slider

0.5.0 - 2016-07-28
------------------

Added
^^^^^

-  New screenshots that show new metadata features
-  Line breaks in code for increased readability
-  Track number now shows in window title
-  Audio files without metadata return ?? in lieu of metadata

Changed
^^^^^^^

-  FLAC metadata extraction changed from album artist to artist

Fixed
^^^^^

-  Search for keys containing 'APIC' in MP3 audio files instead of 'APIC' key

0.4.0 - 2016-07-27
------------------

Added
^^^^^

-  Installation instructions, usage documentation, and screenshot of media player in README
-  Set cover art to scale to window size
-  New window icon
-  Methods now contain docstrings
-  Blank cover image if no cover art found in media
-  README states which file formats are supported
-  Window title changes to include meta data of media currently playing
-  Media player responds to playback events when user clicks on cover art

Changed
^^^^^^^

-  Window resized to deal with cover art cutoff issues
-  Refactored metadata extraction code to reduce redundancy

Removed
^^^^^^^

-  Filetype removed from QByteArray in order to append both 'jpg' and 'png' cover art data


0.3.0 - 2016-07-23
------------------

Added
^^^^^

-  __main__.py for Python discovery
-  File loaded into music player only if user selects 'OK'
-  Cover art and other meta data extracted from current media with mutagen library

Removed
^^^^^^^

-  PyQt5 from setup.py. Package must be installed independently
-  Unused imports from main application


0.2.0 - 2016-07-23
-------------------

Added
^^^^^

-  New menubar on application window
-  Setup.py with entrypoint for easy installation and use
-  Added QMediaPlaylist for playlist capability


0.1.0 - 2016-07-18
------------------

Added
^^^^^

-  Basic Music Player application built with PyQt5
-  Empty README
