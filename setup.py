"""
py2app packaging config — builds a standalone TurkishAutocorrect.app with its
own embedded interpreter, so end users don't need Python, pip, or a venv.

Build with:
    python3 setup.py py2app

Produces dist/TurkishAutocorrect.app. Version defaults to 0.0.0 for local
builds; CI overrides it via the APP_VERSION env var (set from the git tag).
"""

import os

from setuptools import setup

APP = ["app.py"]
DATA_FILES = []
VERSION = os.environ.get("APP_VERSION", "0.0.0")

OPTIONS = {
    "argv_emulation": False,
    "packages": ["rumps", "pynput", "turkish"],
    "plist": {
        "CFBundleName": "TurkishAutocorrect",
        "CFBundleDisplayName": "TurkishAutocorrect",
        "CFBundleIdentifier": "com.github.eicyer.tr-autocorrect",
        "CFBundleShortVersionString": VERSION,
        "CFBundleVersion": VERSION,
        # Menu-bar-only app: no Dock icon, no app switcher entry.
        "LSUIElement": True,
        "NSHumanReadableCopyright": "",
    },
}

setup(
    app=APP,
    name="TurkishAutocorrect",
    data_files=DATA_FILES,
    options={"py2app": OPTIONS},
    setup_requires=["py2app"],
)
