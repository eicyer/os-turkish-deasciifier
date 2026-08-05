# tr-autocorrect

A macOS menu bar utility that auto-corrects ASCII-typed Turkish into proper
Turkish with diacritics, system-wide, as you type. Toggle it on/off from the
menu bar; when off, typing is completely untouched.

Example: typing `bugun cok guzel bir gun` produces `bugün çok güzel bir gün`.

## Download (for everyone — no Terminal needed)

1. Go to the [latest release](https://github.com/eicyer/os-turkish-deasciifier/releases/latest)
   and download `TurkishAutocorrect.dmg`.
2. Open the downloaded `.dmg`, then drag **TurkishAutocorrect** into the
   **Applications** folder shortcut shown alongside it.
3. Open **Applications** and double-click **TurkishAutocorrect**.
   - Since this app isn't sold through the App Store or paid-signed by
     Apple, macOS will likely block it the first time with a message like
     *"Apple could not verify TurkishAutocorrect is free of malware."*
     This is expected — to allow it: open **System Settings → Privacy &
     Security**, scroll down to the security notice near the bottom, and
     click **Open Anyway**, then confirm **Open** in the dialog that
     appears. You only need to do this once.
4. You should see `TR·off` appear in the menu bar. Click it and check
   **Enabled** to turn correction on.
5. The first time it tries to listen to your keystrokes, macOS will ask for
   two permissions — click **Open System Settings** on each prompt (or go
   there manually) and turn **TurkishAutocorrect** on under:
   - **Privacy & Security → Accessibility**
   - **Privacy & Security → Input Monitoring**

   If you don't see a prompt and correction just does nothing, check both
   of those lists directly — the toggle is probably still off.
6. Want it running automatically every time you log in? Click the menu bar
   icon and check **Start at Login**.

That's it — no Python, no `git clone`, no Terminal required. The rest of
this README (below) documents running the app **from source**, which is
only relevant if you're developing or modifying it.

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

## Running from source (developers / contributors)

Everything below this point is for building or modifying the app. If you
just want to use it, see [Download](#download-for-everyone--no-terminal-needed)
above.

### Setup

```bash
cd ~/Desktop/tr-autocorrect
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

(Already done in this session — the venv at `venv/` is ready to go.)

### Running it

```bash
source venv/bin/activate
python app.py
```

You should see `TR·off` appear in your menu bar. Click it and check
**Enabled** to turn correction on.

#### Running automatically in the background (recommended)

Instead of launching `app.py` by hand every time, you can register it as a
per-user **LaunchAgent** so macOS starts it automatically at login and
relaunches it (`KeepAlive`) if it ever crashes:

```bash
./install-launchagent.sh
```

This writes `~/Library/LaunchAgents/com.github.eicyer.tr-autocorrect.plist`
and starts it immediately — `TR·off` should appear in the menu bar within a
few seconds, no Terminal window needed from then on.

**The menu bar icon is meant to stay put.** Clicking **Quit** doesn't exit
the process or touch the LaunchAgent — it just disables correction (same as
unchecking **Enabled**), so the icon is always there to turn it back on. To
actually stop the background process (e.g. before uninstalling or updating
the code), use:

```bash
./uninstall-launchagent.sh
```

which stops it and removes the plist so it won't come back at next login
either. Re-run `./install-launchagent.sh` (or double-click
`TurkishAutocorrect.command`) to bring it back.

Trade-offs of running this way, worth knowing:
- Accessibility/Input Monitoring permissions are effectively granted
  continuously, not just while you have it open.
- A small amount of CPU/memory stays resident all the time, even when
  **Enabled** is off — and now, since Quit no longer exits the process
  either, that's true until you explicitly uninstall it.
- If the app fails at startup, `launchd` retries every ~10s
  (`ThrottleInterval`) rather than looping instantly.
- There's no attached Terminal window, so errors go to
  `tr-autocorrect.log` in this folder instead of stdout — check there if
  something's not working.

If you'd rather not run it as a background daemon at all, just run
`python app.py` manually each time (see below) — Quit behaves the same way
(disables correction, keeps the icon), so to stop it you'll need `Ctrl+C` in
the Terminal window it's running in.

The first time it runs, macOS will block the global keystroke listener
until you grant permissions (see below) — you'll likely get a system
prompt, or correction will just silently do nothing until you grant access
manually.

### Granting macOS permissions (running from source)

This section is for the `python app.py` / venv workflow above, where the
permission has to be granted to the raw interpreter binary. If you
installed the downloaded `.app` instead, use the simpler steps in
[Download](#download-for-everyone--no-terminal-needed) — the permission
prompt there is just labeled **TurkishAutocorrect**.

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

- Custom `.icns` app icon (currently uses py2app's generic default).
- Menu bar icon (vs. text title) for the on/off indicator.
- Notarize the release with a paid Apple Developer account to remove the
  Gatekeeper "Open Anyway" step entirely.
