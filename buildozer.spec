[app]

title = Durian POS
package.name = durianpos
package.domain = org.chong

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,db

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 0

osx.python_version = 3
osx.kivy_version = 2.3.1

android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license = True
android.archs = arm64-v8a, armeabi-v7a

presplash_color = #228B22
icon.filename =

[buildozer]
log_level = 1
warn_on_root = 1
android.skip_update = True
