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
android.permissions = INTERNET, READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE

# (str) Application icon file
icon.filename = %(source.dir)s/app_icon.png
presplash.filename = %(source.dir)s/splash.png


[buildozer]
# (int) Log level (3=debug, 2=info, 1=warning, 0=error)
log_level = 2

# (int) Skip warning when run as root
warn_on_root = 0

# (str) NDK version override: If API 33 fails to compile pyjnius with the automatic NDK,
# you can uncomment the line below and try NDK r23b which is very stable:
android.ndk = 23b
requirements = python3==3.10.12,kivy==2.3.0,hostpython3==3.10.12,pyjnius==1.5.0
osx.python_version = 3.10.12
osx.kivy_version = 2.3.0
