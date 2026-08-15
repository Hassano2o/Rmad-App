[app]

title = Rmad
package.name = rmad
package.domain = org.h1x1o
source.dir = .
source.include_exts = py,txt,jpg,png
requirements = python3,kivy,jnius
android.api = 33
android.minapi = 21
android.ndk = 25b
p4a.bootstrap = sdl2
p4a.archs = armeabi-v7a,arm64-v8a
android.permissions = INTERNET,WAKE_LOCK,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE
log_level = 2
warn_on_root = 1
