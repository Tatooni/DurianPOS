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


[buildozer]

log_level = 2


[app:android]

android.permissions = INTERNET

android.api = 33
android.minapi = 24
android.arch = arm64-v8a

p4a.branch = stable


[app:android:logcat]

log_level = I
