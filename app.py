"""
Turkish Autocorrect - macOS menu bar utility.

Listens to global keystrokes; when enabled, buffers the word currently being
typed and, on word-boundary (space/punctuation/enter/tab), runs it through
the Turkish deasciifier. If the deasciified form differs from what was
typed, backspaces the ASCII word and retypes the corrected Turkish version.

Requires macOS "Accessibility" and "Input Monitoring" permissions for the
process running this script (see README.md).
"""

import os
import plistlib
import subprocess
import sys
import threading

import rumps
from pynput.keyboard import Controller, Key, Listener
from turkish.deasciifier import Deasciifier

# Characters we accumulate into the "current word" buffer. Apostrophe is
# included because Turkish uses it before suffixes on proper nouns
# (e.g. "Turkiye'de" -> "Türkiye'de").
WORD_CHARS_EXTRA = "'"

BOUNDARY_KEYS = (Key.space, Key.enter, Key.tab)

# Same label install-launchagent.sh/uninstall-launchagent.sh use for the
# source/dev workflow — kept identical so only one LaunchAgent can ever be
# registered for this app at a time, however it was installed.
LAUNCH_AGENT_LABEL = "com.github.eicyer.tr-autocorrect"
LAUNCH_AGENT_PLIST_PATH = os.path.expanduser(
    f"~/Library/LaunchAgents/{LAUNCH_AGENT_LABEL}.plist"
)


def _launch_agent_program_arguments():
    """Args that relaunch this exact running app, whether it's a packaged
    .app (py2app sets sys.frozen, and the bundle's own executable is the
    entry point) or a source checkout run via `python app.py`."""
    if getattr(sys, "frozen", False):
        return [sys.executable]
    return [sys.executable, os.path.abspath(__file__)]


def _is_launch_agent_installed():
    return os.path.exists(LAUNCH_AGENT_PLIST_PATH)


def _install_launch_agent():
    os.makedirs(os.path.dirname(LAUNCH_AGENT_PLIST_PATH), exist_ok=True)
    plist = {
        "Label": LAUNCH_AGENT_LABEL,
        "ProgramArguments": _launch_agent_program_arguments(),
        "RunAtLoad": True,
        "KeepAlive": True,
        "ThrottleInterval": 10,
        "ProcessType": "Interactive",
        "LimitLoadToSessionType": "Aqua",
    }
    with open(LAUNCH_AGENT_PLIST_PATH, "wb") as f:
        plistlib.dump(plist, f)

    uid = os.getuid()
    bootstrapped = subprocess.run(
        ["launchctl", "bootstrap", f"gui/{uid}", LAUNCH_AGENT_PLIST_PATH],
        capture_output=True,
    )
    if bootstrapped.returncode != 0:
        # Older launchctl without `bootstrap`, or agent already loaded.
        subprocess.run(
            ["launchctl", "unload", "-w", LAUNCH_AGENT_PLIST_PATH],
            capture_output=True,
        )
        subprocess.run(["launchctl", "load", "-w", LAUNCH_AGENT_PLIST_PATH], check=True)


def _uninstall_launch_agent():
    """Stop the app from auto-starting at future logins only.

    Deliberately does NOT launchctl bootout/unload the current job — that
    would kill the running process immediately, since it's the very job
    being unregistered. Start at Login only controls whether launchd
    relaunches the app later; it must stay independent of whether the app
    (or correction) is currently enabled/running.
    """
    if not _is_launch_agent_installed():
        return
    os.remove(LAUNCH_AGENT_PLIST_PATH)


def _resource_path(name):
    """Locate a bundled resource, whether running as a packaged .app
    (resources live in Contents/Resources, next to Contents/MacOS) or a
    source checkout (resources/ next to app.py)."""
    if getattr(sys, "frozen", False):
        base = os.path.join(os.path.dirname(sys.executable), "..", "Resources")
    else:
        base = os.path.join(os.path.dirname(os.path.abspath(__file__)), "resources")
    return os.path.normpath(os.path.join(base, name))


ICON_ON = _resource_path("icon-on.png")
ICON_OFF = _resource_path("icon-off.png")


class TurkishAutocorrectApp(rumps.App):
    """Menu bar app that live-corrects ASCII-typed Turkish system-wide.

    Shows a "TR" template icon in the menu bar — solid when enabled, dimmed
    when off. While enabled, a global keystroke listener buffers the word
    being typed and replaces it with its deasciified form at each word
    boundary.
    """

    def __init__(self):
        super().__init__("", icon=ICON_OFF, template=True, quit_button=None)

        self.enabled = False
        self.buffer = ""
        self.injecting = False  # true while we're posting our own synthetic keys
        self.buffer_lock = threading.Lock()
        self.controller = Controller()

        self.toggle_item = rumps.MenuItem("Enabled", callback=self.toggle)
        self.toggle_item.state = False

        self.start_at_login_item = rumps.MenuItem(
            "Start at Login", callback=self.toggle_start_at_login
        )
        self.start_at_login_item.state = _is_launch_agent_installed()

        self.menu = [
            self.toggle_item,
            self.start_at_login_item,
            None,
            rumps.MenuItem("Quit", callback=self.quit_app),
        ]

        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

    # -- menu bar --------------------------------------------------------

    def toggle(self, sender):
        """Flip correction on/off and reset the word buffer."""
        self.enabled = not self.enabled
        sender.state = self.enabled
        with self.buffer_lock:
            self.buffer = ""
        self.icon = ICON_ON if self.enabled else ICON_OFF

    def toggle_start_at_login(self, sender):
        """Register/unregister the self-referencing login LaunchAgent."""
        try:
            if sender.state:
                _uninstall_launch_agent()
            else:
                _install_launch_agent()
        except (OSError, subprocess.CalledProcessError) as exc:
            rumps.alert(
                title="Start at Login",
                message=f"Couldn't update the login item: {exc}",
            )
            return
        sender.state = not sender.state

    def quit_app(self, sender):
        """Disable correction but keep the process and menu bar icon alive.

        The menu bar icon is meant to stay put — "Quit" just disables
        correction (like unchecking Enabled) rather than exiting the
        process, so you're never stuck without a menu to re-enable from.
        To actually stop the background process, uncheck Start at Login
        (or use uninstall-launchagent.sh / Ctrl+C if running app.py
        manually).
        """
        self.enabled = False
        self.toggle_item.state = False
        with self.buffer_lock:
            self.buffer = ""
        self.icon = ICON_OFF

    # -- keystroke handling ----------------------------------------------

    def on_press(self, key):
        """pynput callback for every global key press.

        Runs on the listener thread; must never raise, or the listener dies
        silently and correction stops working until restart.
        """
        # Ignore keystrokes we generate ourselves (backspace/retype),
        # otherwise we'd re-buffer our own corrected output.
        if self.injecting:
            return
        if not self.enabled:
            return

        try:
            self._handle_key(key)
        except Exception as exc:  # keep the listener thread alive no matter what
            print(f"[turkish-autocorrect] error handling key {key!r}: {exc}")
            with self.buffer_lock:
                self.buffer = ""

    def _handle_key(self, key):
        """Buffer word characters; flush or reset on everything else."""
        char = getattr(key, "char", None)

        if char is not None:
            if char.isascii() and (char.isalpha() or char in WORD_CHARS_EXTRA):
                with self.buffer_lock:
                    self.buffer += char
            else:
                # punctuation, digits, or a non-ASCII char typed directly:
                # treat as a word boundary and don't add it to the buffer.
                # The OS delivers this keystroke to the focused app on its
                # own (we're a passive listener), and it typically lands
                # before we get around to backspacing, so we have to delete
                # it along with the word and retype it afterwards.
                self.flush_word(boundary_char=char)
            return

        # Special (non-character) keys.
        if key == Key.backspace:
            with self.buffer_lock:
                self.buffer = self.buffer[:-1]
        elif key in BOUNDARY_KEYS:
            # Same reasoning as above: space/enter/tab has usually already
            # been typed by the OS by the time this callback runs.
            self.flush_word(boundary_key=key)
        else:
            # Arrow keys, cmd, option, etc. — cursor position may have moved,
            # so abandon the buffer rather than risk corrupting text.
            with self.buffer_lock:
                self.buffer = ""

    def flush_word(self, boundary_char=None, boundary_key=None):
        """Deasciify the buffered word and replace it in-place if it changed.

        ``boundary_char``/``boundary_key`` is the keystroke that ended the
        word (space, punctuation, enter, ...); it's passed along so the
        replacement can retype it after the corrected word.
        """
        with self.buffer_lock:
            word, self.buffer = self.buffer, ""

        if not word:
            return

        corrected = Deasciifier(word).convert_to_turkish()
        if corrected != word:
            self.inject_replacement(word, corrected, boundary_char, boundary_key)

    def inject_replacement(self, original, corrected, boundary_char=None, boundary_key=None):
        """Backspace over ``original`` (plus the boundary keystroke) and
        type ``corrected`` followed by the boundary keystroke."""
        self.injecting = True
        try:
            # +1 to also remove the boundary keystroke (space/tab/enter/
            # punctuation) that triggered this flush, since it has usually
            # already been typed by the OS by this point.
            backspaces = len(original) + (1 if (boundary_char or boundary_key) else 0)
            for _ in range(backspaces):
                self.controller.tap(Key.backspace)
            self.controller.type(corrected)
            if boundary_char is not None:
                self.controller.type(boundary_char)
            elif boundary_key is not None:
                self.controller.tap(boundary_key)
        finally:
            self.injecting = False


if __name__ == "__main__":
    TurkishAutocorrectApp().run()
