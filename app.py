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
import subprocess
import threading

import rumps
from pynput import keyboard
from pynput.keyboard import Controller, Key, Listener
from turkish.deasciifier import Deasciifier

# Characters we accumulate into the "current word" buffer. Apostrophe is
# included because Turkish uses it before suffixes on proper nouns
# (e.g. "Turkiye'de" -> "Türkiye'de").
WORD_CHARS_EXTRA = "'"

BOUNDARY_KEYS = (Key.space, Key.enter, Key.tab)

# Must match the Label/plist filename install-launchagent.sh generates.
LAUNCH_AGENT_LABEL = "com.github.eicyer.tr-autocorrect"
LAUNCH_AGENT_PLIST = os.path.expanduser(
    f"~/Library/LaunchAgents/{LAUNCH_AGENT_LABEL}.plist"
)


class TurkishAutocorrectApp(rumps.App):
    def __init__(self):
        super().__init__("TR·off", quit_button=None)

        self.enabled = False
        self.buffer = ""
        self.injecting = False  # true while we're posting our own synthetic keys
        self.buffer_lock = threading.Lock()
        self.controller = Controller()

        self.toggle_item = rumps.MenuItem("Enabled", callback=self.toggle)
        self.toggle_item.state = False

        self.menu = [
            self.toggle_item,
            None,
            rumps.MenuItem("Quit", callback=self.quit_app),
        ]

        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

    # -- menu bar --------------------------------------------------------

    def toggle(self, sender):
        self.enabled = not self.enabled
        sender.state = self.enabled
        with self.buffer_lock:
            self.buffer = ""
        self.title = "TR·on" if self.enabled else "TR·off"

    def quit_app(self, sender):
        self.listener.stop()
        self._unload_launch_agent()
        # rumps.quit_application() just calls NSApplication.terminate_(),
        # which for a plain (non-bundled) script can tear down the menu bar
        # icon without actually killing the process — leaving the keystroke
        # listener running invisibly in the background. Force the issue.
        os._exit(0)

    def _unload_launch_agent(self):
        # If we're running as the KeepAlive LaunchAgent (see
        # install-launchagent.sh), launchd will instantly relaunch us the
        # moment this process exits unless we tell it to stop first. If
        # we're just a plain `python app.py` run with no LaunchAgent
        # installed, both commands fail harmlessly and Quit behaves as a
        # normal exit.
        if not os.path.exists(LAUNCH_AGENT_PLIST):
            return
        uid = os.getuid()
        target = f"gui/{uid}/{LAUNCH_AGENT_LABEL}"
        result = subprocess.run(
            ["launchctl", "bootout", target],
            capture_output=True,
        )
        if result.returncode != 0:
            subprocess.run(
                ["launchctl", "unload", "-w", LAUNCH_AGENT_PLIST],
                capture_output=True,
            )

    # -- keystroke handling ----------------------------------------------

    def on_press(self, key):
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
        with self.buffer_lock:
            word, self.buffer = self.buffer, ""

        if not word:
            return

        corrected = Deasciifier(word).convert_to_turkish()
        if corrected != word:
            self.inject_replacement(word, corrected, boundary_char, boundary_key)

    def inject_replacement(self, original, corrected, boundary_char=None, boundary_key=None):
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
