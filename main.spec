# main.spec
from nuitka import __version__

Options = {
    "include-package" : "kivy",
    "include-package" : "jnius",
    "include-package" : "android",
    "include-package" : "ssl",
    "include-package" : "urllib",
    "include-package" : "http",
    "include-package" : "json",
    "include-package" : "time",
    "include-package" : "os",
    "include-package" : "threading",
    "include-package" : "socket",
    "include-package" : "subprocess",
    "include-package" : "webbrowser",
    "include-package" : "uuid",
    "standalone" : True,
    "output-dir" : "build",
    "python-version" : "3.10", # تأكد من توافق نسخة بايثون المثبتة
    "lto" : "no",
    "nofollow-imports" : True,
    "enable-plugin" : "kivy",
}
