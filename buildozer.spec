[app]

# (str) Title of your application
title = Rmad Pro

# (str) Package name
package.name = rmad

# (str) Package domain (needed for android/ios packaging)
package.domain = org.h1x1o

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to use all files in .source_dir)
source.include_exts = py,txt,jpg,png,spec,md

# (list) Source files to exclude (let empty to not exclude files)
source.exclude_exts = spec

# (list) List of source file patterns to add to the apk archive
source.include_patterns = assets/*,images/*

# (list) List of dependencies
requirements = python3,kivy,jnius,requests

# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) List of service to declare
[android]

# (list) Permissions for Android
permissions = INTERNET,WAKE_LOCK,ACCESS_WIFI_STATE,CHANGE_WIFI_STATE,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,ACCESS_NETWORK_STATE

# (str) The android activity to use
android.entrypoint = org.renpy.android.PythonActivity

# (str) The android app theme
android.apptheme = @android:style/Theme.Material.Light.NoActionBar

# (int) Android SDK API version
android.api = 33

# (int) Minimum Android SDK version
android.minapi = 21

# (int) Android NDK version
android.ndk = 25b

# (int) Version of the python binary to use
android.python_version = 3.11

# (str) The bootstrap to use
android.bootstrap = sdl2

# (list) Android libraries to add
android.add_aars =

# (list) Android jars to add
android.add_jars =

# (list) Files to add to the Android project's assets directory
android.add_assets =

# (list) Java classes to add
android.add_source_dirs =

# (str) The android theme to use
android.apptheme = @android:style/Theme.Material.Light.NoActionBar

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, i.e. as --cache-dir in the build command.
build_dir = .buildozer

# (str) Path to build output (i.e. .apk, .aab) storage.
bin_dir = bin

# (list) The patterns to use when deleting cache directories in order to free up disk space
# For example, the following patterns will remove all directories and files starting with (.)
# and ending with (cache) or (cache-)
#
# .*/cache.*
# .*/cache-.*
#
# Note: this will not work for all operating systems, as it depends on the shell
# used to run the command.
#
# Example:
# cache_patterns = .*/cache.*
#
cache_patterns =

# (list) Download URL patterns for android dependencies
# Note: Example patterns are for the `buildozer` package, not for the app
#download_url_patterns =

# (list) Extra buildozer plugins
#extra_buildozer_plugins =

# (str) Extra arguments to pass to the buildozer binary
#extra_buildozer_args =

# (str) Path to buildozer log file
#log_file =

# (str) Version of buildozer
#version =

# (str) URL of the buildozer repository
#repository =

# (str) Branch of the buildozer repository
#branch =

# (str) Commit of the buildozer repository
#commit =

# (str) Directory to clone the buildozer repository into
#clone_dir =

# (str) Directory to clone the buildozer repository into
#clone_branch =

# (str) Directory to clone the buildozer repository into
#clone_commit =

# (str) Directory to clone the buildozer repository into
#clone_submodule =

# (str) Directory to clone the buildozer repository into
#clone_tag =

# (str) Directory to clone the buildozer repository into
#clone_depth =

# (str) Directory to clone the buildozer repository into
#clone_shallow =

# (str) Directory to clone the buildozer repository into
#clone_recursive =

# (str) Directory to clone the buildozer repository into
#clone_no_checkout =

# (str) Directory to clone the buildozer repository into
#clone_single_branch =

# (str) Directory to clone the buildozer repository into
#clone_filter =

# (str) Directory to clone the buildozer repository into
#clone_sparse_checkout =

# (str) Directory to clone the buildozer repository into
#clone_shallow_since =

# (str) Directory to clone the buildozer repository into
#clone_shallow_exclude =

# (str) Directory to clone the buildozer repository into
#clone_shallow_include =

# (str) Directory to clone the buildozer repository into
#clone_shallow_skip =

# (str) Directory to clone the buildozer repository into
#clone_shallow_verbosity =

# (str) Directory to clone the buildozer repository into
#clone_shallow_debug =

# (str) Directory to clone the buildozer repository into
#clone_shallow_info =

# (str) Directory to clone the buildozer repository into
#clone_shallow_error =

# (str) Directory to clone the buildozer repository into
#clone_shallow_warn =

# (str) Directory to clone the buildozer repository into
#clone_shallow_log =

# (str) Directory to clone the buildozer repository into
#clone_shallow_trace =

# (str) Directory to clone the buildozer repository into
#clone_shallow_verbose =

# (str) Directory to clone the buildozer repository into
#clone_shallow_quiet =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_all =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_none =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_some =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_many =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_few =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_one =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_zero =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_all =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_none =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_some =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_many =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_few =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_one =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_zero =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_all =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_none =
]
# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_some =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_many =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_few =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_one =

# (str) Directory to clone the buildozer repository into
#clone_shallow_silent_zero =
