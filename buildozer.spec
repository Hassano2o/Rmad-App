cat > buildozer.spec << 'EOF'
[app]
title = Rmad
package.name = rmad
package.domain = org.h1x1o
source.dir = .
source.include_exts = py,txt
version = 1.0
requirements = python3,kivy,jnius
android.api = 33
android.minapi = 21
p4a.bootstrap = sdl2
orientation = sensor
fullscreen = 0
log_level = 2
warn_on_root = 1
EOF
