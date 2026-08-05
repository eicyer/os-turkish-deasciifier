"""
py2app packaging config — builds a standalone TurkishAutocorrect.app with its
own embedded interpreter, so end users don't need Python, pip, or a venv.

Build with:
    python3 setup.py py2app

Produces dist/TurkishAutocorrect.app. Version defaults to 0.0.0 for local
builds; CI overrides it via the APP_VERSION env var (set from the git tag).
"""

import ctypes.util
import os
import subprocess

from setuptools import setup

APP = ["app.py"]
DATA_FILES = []
VERSION = os.environ.get("APP_VERSION", "0.0.0")


def _find_real_libffi():
    """Locate an on-disk libffi.dylib for py2app to bundle.

    py2app's static dependency scan doesn't always find libffi on
    interpreters where ctypes resolves it via @rpath at runtime (observed
    with Anaconda's Python) — without it, the built .app crashes on launch
    with:
        ImportError: dlopen(.../_ctypes.so): Library not loaded: @rpath/libffi.8.dylib

    `ctypes.util.find_library` sometimes returns a dyld-shared-cache-only
    path (e.g. /usr/lib/libffi.dylib) that has no file on disk for py2app
    to copy, so fall back to asking otool where the current interpreter's
    _ctypes extension actually resolves libffi from via its rpaths.
    """
    candidate = ctypes.util.find_library("ffi")
    if candidate and os.path.exists(candidate):
        return candidate

    try:
        import _ctypes

        ext_path = _ctypes.__file__
        deps = subprocess.run(
            ["otool", "-L", ext_path], capture_output=True, text=True, check=True
        ).stdout
        libffi_ref = next(
            (line.split()[0] for line in deps.splitlines() if "libffi" in line), None
        )
        if not libffi_ref:
            return None
        if not libffi_ref.startswith("@rpath/"):
            return libffi_ref if os.path.exists(libffi_ref) else None

        leaf = os.path.basename(libffi_ref)
        ext_dir = os.path.dirname(ext_path)
        load_commands = subprocess.run(
            ["otool", "-l", ext_path], capture_output=True, text=True, check=True
        ).stdout
        lines = load_commands.splitlines()
        for i, line in enumerate(lines):
            if "LC_RPATH" not in line:
                continue
            for follow in lines[i : i + 4]:
                if "path " not in follow:
                    continue
                rpath = follow.strip().split("path ", 1)[1].split(" (offset")[0]
                # @loader_path is relative to the file that references it
                # (our extension module); resolve it before joining.
                rpath = rpath.replace("@loader_path", ext_dir)
                real_path = os.path.normpath(os.path.join(rpath, leaf))
                if os.path.exists(real_path):
                    return real_path
    except (OSError, subprocess.CalledProcessError, ImportError):
        pass
    return None


FRAMEWORKS = []
_libffi = _find_real_libffi()
if _libffi:
    FRAMEWORKS.append(_libffi)

OPTIONS = {
    "argv_emulation": False,
    "packages": ["rumps", "pynput", "turkish"],
    "frameworks": FRAMEWORKS,
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
