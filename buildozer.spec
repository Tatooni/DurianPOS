[app]

title = Durian POS
package.name = durianpos
package.domain = org.durianpos

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = kivy

orientation = portrait
fullscreen = 0

android.permissions = INTERNET
android.api = 33
android.minapi = 24
android.archs = arm64-v8a
android.accept_sdk_license = True

p4a.branch = develop

[buildozer]

log_level = 2
warn_on_root = 1
