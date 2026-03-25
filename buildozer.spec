[app]

title = Durian POS
package.name = durianpos
package.domain = org.chong.durian

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,db

version = 1.0

requirements = python3,kivy==2.3.0,sqlite3

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

android.archs = arm64-v8a,armeabi-v7a

android.enable_androidx = False
android.accept_sdk_license = True
android.release_artifact = apk

android.entrypoint = org.kivy.android.PythonActivity

android.presplash_color = #FFFFFF
android.logcat_filters = *:S python:D

p4a.branch = develop

[buildozer]

log_level = 2
warn_on_root = 1
