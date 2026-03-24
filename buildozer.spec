[app]

title = Durian POS
package.name = durianpos
package.domain = org.chong.durian

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db

version = 1.0

requirements = python3,kivy,sqlite3

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.api = 31
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21

android.archs = arm64-v8a, armeabi-v7a

android.gradle_dependencies = androidx.core:core-ktx:1.6.0

android.accept_sdk_license = True

android.entrypoint = org.kivy.android.PythonActivity

android.presplash_color = #FFFFFF
android.logcat_filters = *:S python:D

[buildozer]

log_level = 2
warn_on_root = 1
