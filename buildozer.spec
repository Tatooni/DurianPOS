[app]

title = Durian POS
package.name = durianpos
package.domain = org.durian

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3,kivy

orientation = portrait
fullscreen = 1

# Android settings
android.permissions = INTERNET
android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = arm64-v8a
android.accept_sdk_license = True
android.enable_androidx = True

# Fix build issues
android.gradle_dependencies =
android.add_src =
android.add_aars =

# Logging
log_level = 2

[buildozer]

log_level = 2
warn_on_root = 1
