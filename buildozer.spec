[app]
# ... (title, package info, source.dir are fine) ...
source.include_exts = py,kv,mp3,png,jpg,ttf,wav

# Update requirements to specify a known-good pyjnius version (e.g., 1.5.0 or later)
requirements = python3,kivy,six,pyjnius==1.5.0 

# ... (orientation, fullscreen are fine) ...

# Change API back to 33, which has highly stable P4A recipes
android.api = 33 
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
version = 1.0

[buildozer]
log_level = 3
warn_on_root = 0
