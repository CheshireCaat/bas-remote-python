import os
import platform
import unittest

ABS_PATH = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))  # root project directory

is_windows = platform.system() != "windows"
windows_test = unittest.skipIf(
    is_windows, "OS not supported: %s" % platform.system()
)
