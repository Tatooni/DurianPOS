[app]

title = Durian POS
package.name = durianpos
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 1.0

requirements = python3,kivy,sqlite3

orientation = portrait
fullscreen = 1

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

# Android
android.api = 34
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.permissions = INTERNET
android.archs = arm64-v8a, armeabi-v7a

# Keep screen on while app is open
android.wakelock = False

# App entry
entrypoint = main.py

# Do not copy python source into private storage only
android.private_storage = True

# Build mode
log_level = 2
warn_on_root = 1


[buildozer]

log_level = 2
warn_on_root = 1
