##########
Change Log
##########

All notable changes to this project will be documented in this file.


0.21.1 - 2017-03-10
===================

Added
-----

-  New screenshots in README


0.21.0 - 2017-02-27
===================

Added
-----

-  Ability to save playlist on player close
-  Ability to open previously saved playlist

0.20.1 - 2017-01-18
===================

Changed
-------

-  Updated screenshot on README to reflect new icons

0.20.0 - 2017-01-17
===================

Added
-----

-  Ability to shuffle playlist

Changed
-------

-  New repeat playlist icons


0.19.3 - 2016-12-28
===================

Changed
-------

-  Rewrote docstrings in test functions

0.19.2 - 2016-12-25
===================

Fixed
-----

-  First index of playlist now highlighted when media added from playlist file

0.19.1 - 2016-12-23
===================

Fixed
-----

-  Missing repeat icons now appear

0.19.0 - 2016-12-23
===================

Added
-----

-  Ability to loop playlist

0.18.6 - 2016-12-06
===================

Changed
-------

-  Repeat turns off when new media added to empty playlist

0.18.5 - 2016-11-19
===================

Fixed
-----

-  Playlist now shown when new media added if media library dock open

0.18.4 - 2016-10-08
===================

Added
-----

-  OK button to preferences dialog

0.18.3 - 2016-10-07
===================

Fixed
-----

-  The docks no longer close when options other than window size are changed

Changed
-------

-  Removed the OK and Cancel buttons from the preferences dialog

0.18.2 - 2016-10-06
===================

Fixed
-----

-  Media library now updates without restart when library path changed

0.18.1 - 2016-09-23
===================

Fixed
-----

-  Mosaic no longer crashes when file without metadata is opened
-  No Cover image now shows when file without metadata is playing

0.18.0 - 2016-09-18
===================

Added
-----

-  Current song restarts when previous button clicked unless song is less
   than five seconds in
-  New playback preference item where user can change whether or not
   playback can be controlled via cover art mouse clicks

0.17.2 - 2016-09-13
===================

Fixed
-----

-  python -m mosaic now correctly discovers music player application

0.17.1 - 2016-09-13
===================

Fixed
-----

-  When the window size is changed in preferences, the library dock and playlist dock close
   in order to properly resize the window
-  Minimalist View now resizes properly when playlist dock or library dock are open

0.17.0 - 2016-09-10
===================

Added
-----

-  Minimalist View in view menu shows only menu bar and tool bar when selected

Changed
-------

-  Mouse press event on cover art now occurs only on left mouse button click

0.16.4 - 2016-09-09
===================

Fixed
-----

-  About dialog reformatted to display text properly

0.16.3 - 2016-09-06
===================

Changed
-------

-  Library dock width now same as playlist dock width

Fixed
-----

-  Fixed issue with window size prefeence not correctly resizing when library dock was visible

0.16.2 - 2016-09-05
===================

Fixed
-----

-  Window size changes when preferences dialog is accepted if a new setting is selected

0.16.1 - 2016-08-30
===================

Added
-----

-  Added OK and Cancel buttons to Preferences dialog

0.16.0 - 2016-08-29
===================

Added
-----

-  Ability to select which side of the application the playlist and
   media library docks show

Changed
-------

-  Playlist and media library docks are no longer floatable or movable


0.15.0 - 2016-08-29
===================

Added
-----

-  Preference to show playlist dock on startup

Changed
-------

-  Renamed Window Options in preferences menu to View Options
-  Moved Media Library on Start checkbox to View Options

0.14.4 - 2016-08-28
===================

Fixed
-----

-  Fixed issue with travis building from source rather than wheel

0.14.3 - 2016-08-28
===================

Changed
-------

-  Preferences dialog size now smaller

0.14.2 - 2016-08-27
===================

Added
-----

-  New CHANGELOG that describes changes between versions
-  CHANGELOG link in README
-  Test requirements in requirements folder
-  Dependency CI and software status badge to README
-  Separator added in view menu between docks and media information

Changed
-------

-  Playlist and media library docks now shown in tabs by default when both are open


0.14.1 - 2016-08-26
===================

Added
-----

-  Playlist items now have tooltips

0.14.0 - 2016-08-25
===================

Added
-----

-  Uploaded license to repository
-  Window now resizes to fit media library and playlist docks so that cover art size remains the same
-  New screenshots that showcase new features

Changed
-------

-  Items in media library browser and playlist dock now require double click to play

Removed
-------

-  Removed setting for recursive directories as the setting is now default behavior
-  Removed media library from file dialogs now that media library browser has been added

0.13.2 - 2016-08-24
===================

Added
-----

- New setting that allows user to show media library on startup

0.13.1 - 2016-08-23
===================

Added
-----

-  63 pixels added to window height to account for menubar and toolbar pixels

0.13.0 - 2016-08-22
===================

Added
-----

-  New tab on media information dialog that shows all metadata extracted from current media
-  New media library file browser

Changed
-------

-  README install instructions now use pip3 instead of pip

0.12.4 - 2016-08-20
===================

Added
-----

-  README now displays features

0.12.3 - 2016-08-19
===================

Fixed
-----

-  Fixed issue where player would crash if user settings file was missing settings

0.12.2 - 2016-08-18
===================

Changed
-------

-  Rewrote tests to use Pytest fixtures

0.12.1 - 2016-08-17
===================

Changed
-------

-  Unit tests now use real audio files

0.12.0 - 2016-08-16
===================

Added
-----

-  New setting that allows user to change window size


Changed
-------

-  Audio files opened are now naturally sorted in playlist

Fixed
-----

-  Fixed issue with MP3 cover art not being extracted from audio file

0.11.4 - 2016-08-15
===================

Changed
-------

-  File dialogs are now read only

0.11.3 - 2016-08-14
===================

Added
-----

-  New header image for README

0.11.2 - 2016-08-13
===================

Added
-----

-  PyPI install instructions in README

Fixed
-----

-  Refactored QUrl().path() to QUrl().toLocalFile() for true file path discovery

0.11.1 - 2016-08-12
===================

Added
-----

-  Link to PyQt5 download page in install instructions

0.11.0 - 2016-08-10
===================

Added
-----

-  Media information dialog that displays current media metadata
-  Keyboard shortcut to about dialog
-  Keyboard shortcut to media information dialog

Changed
-------

-  Set media library text box now read only

0.10.0 - 2016-08-09
===================

Added
-----

-  Check for settings file in user config directory
-  New open playlist item in file menu

Changed
-------

-  Settings file now created on application open
-  Settings file now uses nested settings for increased readability

Fixed
-----

-  Fixed issue with TOML file not reading in correctly

0.9.0 - 2016-08-08
==================

Added
-----

-  Playlist dock selects index 0 when media added
-  New media library path setting in preferences
-  Keyboard shortcut for playlist dock
-  New window title and icon for about dialog
-  Imported pkg_resources in order for resources to be correctly shown to users


0.8.0 - 2016-08-07
==================

Added
-----

-  New edit menu with preferences item
-  Configuration dialog for user preferences
-  User setting that allows user to specify if directories are opened recursively
-  Settings file in TOML format
-  New window icon for preferences dialog
-  New signal for playlist dock to change index of item according to index of media playlist

Fixed
-----

-  Refactored open directory to eliminate directories being opened twice
-  Fixed issue where current media would restart when playlist dock clicked

0.7.1 - 2016-08-06
==================

Changed
-------

-  Playlist dock now only shows filenames of media in current playlist

0.7.0 - 2016-08-05
==================

Added
-----

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
-------

-  Repeat button now repeats current media instead of repeating current playlist

Fixed
-----

-  Fixed typo in getOpenFileNames dialog filter so that MP3 and FLAC filetypes show
-  Current playlist now clears when directory opened

0.6.2 - 2016-08-04
==================

Changed
-------

-  Switched toolbar icons from system icons to Google Material Design icons

0.6.1 - 2016-08-03
==================

Added
-----

-  Import QDesktopWidget in order to move application to center of user's screen

0.6.0 - 2016-08-02
==================

Added
-----

-  Horizontal slider on media toolbar
-  New signals to track position and duration of current media
-  Exit application item in file menu
-  New screenshots showcasing horizontal slider

0.5.0 - 2016-07-28
==================

Added
-----

-  New screenshots that show new metadata features
-  Track number now shows in window title
-  Audio files without metadata return ?? in lieu of metadata

Changed
-------

-  FLAC metadata extraction changed from album artist to artist

Fixed
-----

-  Search for keys containing 'APIC' in MP3 audio files instead of 'APIC' key

0.4.0 - 2016-07-27
==================

Added
-----

-  Installation instructions, usage documentation, and screenshot of media player in README
-  Set cover art to scale to window size
-  New window icon
-  Blank cover image if no cover art found in media
-  README states which file formats are supported
-  Window title changes to include meta data of media currently playing
-  Media player responds to playback events when user clicks on cover art


Fixed
-----

-  Window resized to deal with cover art cutoff issues
-  Filetype removed from QByteArray in order to append both 'jpg' and 'png' cover art data

0.3.0 - 2016-07-23
==================

Added
-----

-  __main__.py for Python discovery
-  Cover art and other meta data extracted from current media with mutagen library

Changed
-------

-  File loaded into music player only if user selects 'OK'

Removed
-------

-  PyQt5 from setup.py. Package must be installed independently

0.2.0 - 2016-07-23
==================

Added
-----

-  New menubar on application window
-  Setup.py with entrypoint for easy installation and use
-  Added QMediaPlaylist for playlist capability

0.1.0 - 2016-07-18
==================

Added
-----

-  Basic Music Player application built with PyQt5
-  Empty README
