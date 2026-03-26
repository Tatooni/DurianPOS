[app]

title = Durian POS
package.name = durianpos
package.domain = org.durian

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = python3==3.10.11,kivy==2.2.1,sqlite3

orientation = portrait
fullscreen = 0

android.permissions = INTERNET

android.api = 33
android.minapi = 24
android.ndk = 25b

p4a.branch = develop

android.accept_sdk_license = True

[buildozer]

log_level = 2
warn_on_root = 1
