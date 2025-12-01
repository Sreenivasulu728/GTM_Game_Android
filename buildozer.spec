[app]
# (str) Title of your application
title = GTM Game

# (str) Package name
package.name = gtmgame

# (str) Package domain (needed for unique app identifier)
package.domain = org.example

# (str) Source code directory
source.dir = .

# (list) File extensions to include (added mp3 and wav for your music)
source.include_exts = py,kv,mp3,png,jpg,ttf,wav

# (list) Application requirements
requirements = python3,kivy,six,pyjnius

# (str) App version
version = 1.0

# (list) Supported orientations (portrait, landscape, etc.)
orientation = portrait

# (bool) Fullscreen mode
fullscreen = 1

# (int) Target Android API (API 34 is required for new apps on Google Play as of Aug 2024)
android.api = 34

# (int) Minimum API your APK will support (API 24+ is a good minimum now)
android.minapi = 24

# (list) The Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (list) Permissions (added INTERNET for general app functionality, though maybe not strictly needed for this game)
android.permissions = INTERNET

# (str) Presplash file (optional, defaults to Kivy logo)
# presplash.filename = %(source.dir)s/icons/presplash.png

# (str) Application icon file (optional, defaults to Kivy logo)
# icon.filename = %(source.dir)s/icons/app_icon.png


[buildozer]
# (int) Log level (3=debug, 2=info, 1=warning, 0=error)
log_level = 3

# (int) Skip warning when run as root
warn_on_root = 0

# The following lines are commented out because buildozer manages these automatically and best
# android.ndk = 25b 
# android.sdk = 30

