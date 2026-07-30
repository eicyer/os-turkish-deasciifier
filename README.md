# tr-autocorrect

A macOS menu bar utility that auto-corrects ASCII-typed Turkish into proper
Turkish with diacritics, system-wide, as you type. Toggle it on/off from the
menu bar; when off, typing is completely untouched.

Example: typing `bugun cok guzel bir gun` produces `bugün çok güzel bir gün`.

## How it works

- **Menu bar toggle** ([`rumps`](https://github.com/jaredks/rumps)) — an
  "Enabled" checkbox item; the menu bar title shows `TR·on` / `TR·off` as a
  quick visual indicator.
- **Global keystroke listener** ([`pynput`](https://github.com/moses-palmer/pynput))
  — watches keystrokes system-wide (any app) without blocking them, so
  normal typing always goes through untouched.
- **Word buffering** — while enabled, it accumulates the letters of the
  word you're currently typing. On space / punctuation / enter / tab, it
  runs the buffered word through the deasciifier. If the result differs
  from what you typed, it sends backspaces to delete the ASCII word and
  types the corrected Turkish word in its place.
- **Conversion engine** — [`turkish-deasciifier`](https://github.com/emres/turkish-deasciifier),
  the Python 3 port of Deniz Yüret's original Turkish deasciification
  algorithm (context-based, so it correctly picks e.g. `güzel` vs `gzel`,
  `için` vs `için`, etc. based on surrounding letters).

Note: this package isn't published on PyPI under an installable name, so
`requirements.txt` pulls it straight from GitHub via
`git+https://github.com/emres/turkish-deasciifier.git`.

## Setup

```bash
cd ~/Desktop/tr-autocorrect
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

(Already done in this session — the venv at `venv/` is ready to go.)

## Running it

```bash
source venv/bin/activate
python app.py
```

You should see `TR·off` appear in your menu bar. Click it and check
**Enabled** to turn correction on.

### Running automatically in the background (recommended)

Instead of launching `app.py` by hand every time, you can register it as a
per-user **LaunchAgent** so macOS starts it automatically at login and
relaunches it (`KeepAlive`) if it ever crashes:

```bash
./install-launchagent.sh
```

This writes `~/Library/LaunchAgents/com.github.eicyer.tr-autocorrect.plist`
and starts it immediately — `TR·off` should appear in the menu bar within a
few seconds, no Terminal window needed from then on.

**This changes what Quit does.** Because `launchd` would otherwise respawn
the process the instant it exits, clicking **Quit** now also unloads/disables
the LaunchAgent (see `_unload_launch_agent` in `app.py`) so it actually stays
stopped, rather than exiting and immediately bouncing back. To bring it back
after Quit, either double-click **`TurkishAutocorrect.command`** (it detects
the installed LaunchAgent and reloads it) or re-run
`./install-launchagent.sh`.

Trade-offs of running this way, worth knowing:
- Accessibility/Input Monitoring permissions are effectively granted
  continuously, not just while you have it open.
- A small amount of CPU/memory stays resident all the time, even when
  **Enabled** is off.
- If the app fails at startup, `launchd` retries every ~10s
  (`ThrottleInterval`) rather than looping instantly.
- There's no attached Terminal window, so errors go to
  `tr-autocorrect.log` in this folder instead of stdout — check there if
  something's not working.

To fully remove the LaunchAgent (stop it and prevent it from returning at
login):

```bash
./uninstall-launchagent.sh
```

If you'd rather not run it as a background daemon at all, just run
`python app.py` manually each time (see below) — in that mode Quit is a
plain process exit like before, and `TurkishAutocorrect.command` falls back
to relaunching it directly.

The first time it runs, macOS will block the global keystroke listener
until you grant permissions (see below) — you'll likely get a system
prompt, or correction will just silently do nothing until you grant access
manually.

## Granting macOS permissions

Two separate privacy permissions are involved:

1. **Accessibility** — needed to simulate the backspace/retype keystrokes.
2. **Input Monitoring** — needed to observe global keystrokes (required
   since macOS Catalina for any app doing system-wide key listening).

Steps:

1. Open **System Settings → Privacy & Security → Accessibility**.
2. Click the **+** button (you may need to unlock with your password
   first).
3. Press `Cmd+Shift+G` in the file picker and paste in this path, then hit
   Enter:
   ```
   /opt/anaconda3/bin/python3
   ```
   (This is the real interpreter your venv points to — confirmed via
   `venv/bin/python3 -c "import sys; print(sys.executable)"`. If you ever
   recreate the venv with a different Python, re-check this path.)
4. Make sure the toggle next to it is switched **on**.
5. Repeat the same steps under **System Settings → Privacy & Security →
   Input Monitoring**.
6. If **Terminal** (or iTerm, or whatever app you launched `python app.py`
   from) also appears in either list, make sure it's toggled on too — some
   macOS versions attribute the permission to the launching terminal app
   instead of (or in addition to) the interpreter binary.
7. Quit and restart the script (`Ctrl+C`, then `python app.py` again) —
   permission changes usually require the process to relaunch.

If you don't see a prompt at all and correction just doesn't do anything,
that almost always means one of these two permissions is still missing —
double check both lists.

## Testing v1

With the app running and **Enabled** checked:

1. Open **TextEdit**, click into a new document, and type:
   `bugun cok guzel bir gun ` (with a trailing space). It should turn into
   `bugün çok güzel bir gün `.
2. Open **Terminal** (a second window/tab, separate from the one running
   `python app.py`) and type the same phrase at a shell prompt — it should
   correct there too, since the listener is system-wide, not
   browser/app-specific.
3. Toggle **Enabled** off from the menu bar and confirm typing the same
   text now stays as plain ASCII, untouched.

## Known limitations (v1)

- If you move the cursor mid-word (arrow keys, clicking elsewhere) the
  buffer is discarded defensively rather than risking a wrong correction.
- Digits inside a "word" (e.g. `gun2`) flush the buffer without correcting
  it, since digits aren't treated as word characters.
- There's a small window where our injected backspace/retype and your next
  keystroke could theoretically interleave; not observed in practice but
  worth knowing about if you ever see garbled output.

## Later / nice-to-have

- Package as a standalone `.app` with `py2app` so it doesn't need to run
  from a terminal, and can be added to Login Items.
- Menu bar icon (vs. text title) for the on/off indicator.
