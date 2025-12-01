[app]
# (str) Title of your application
title = GTM Game

# (str) Package name (must be lowercase)
package.name = gtmgame

# (str) Package domain (needed for unique app identifier)
package.domain = org.example

# (str) Source code directory
source.dir = .

# (list) File extensions to include (added mp3 and wav for your music)
source.include_exts = py,kv,mp3,png,jpg,ttf,wav

# (list) Application requirements (using specific version 1.5.0 to fix compilation error)
requirements = python3,kivy,six,pyjnius==1.5.0

# (str) App version
version = 1.0

# (list) Supported orientations
orientation = portrait

# (bool) Fullscreen mode
fullscreen = 1

# (int) Target Android API (API 33 is stable and compatible with pyjnius==1.5.0)
android.api = 33

# (int) Minimum API your APK will support (API 24+ is a good minimum now)
android.minapi = 24

# (list) The Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (list) Permissions
android.permissions = INTERNET

# (str) Application icon file
icon.filename = %(source.dir)s/icon.png


[buildozer]
# (int) Log level (3=debug, 2=info, 1=warning, 0=error)
log_level = 3

# (int) Skip warning when run as root
warn_on_root = 0
