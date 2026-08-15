[app]
title = Rmad
source.dir = .
source.include_exts = py, txt
version = 1.0
requirements = python3,kivy,jnius
package.name = rmad
package.domain = org.h1x1o
source.version = 1
android.permissions = INTERNET,WAKE_LOCK,ACCESS_NETWORK_STATE,ACCESS_WIFI_STATE,WAKE_LOCK
android.api = 33
android.minapi = 21
android.sdk = 28
android.ndk = 21b
android.ndk_path = /home/toor/.buildozer/android/platform/android-ndk-r21b
fullscreen = 0
orientation = portrait
EOF

# 3. تأكد من أن الملف تم إنشاؤه بشكل صحيح
cat buildozer.spec

# 4. الآن نفذ الأمر مرة أخرى
buildozer android debug
