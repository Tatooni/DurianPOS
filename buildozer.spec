[app]

title = Durian POS
package.name = durianpos
package.domain = org.test

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,db
version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 1

android.api = 34
android.minapi = 24
android.ndk = 25b
android.accept_sdk_license = True
android.permissions = INTERNET
android.archs = arm64-v8a

android.wakelock = False
android.private_storage = True

log_level = 2
warn_on_root = 1


[buildozer]

log_level = 2
warn_on_root = 1
