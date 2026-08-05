# Turkish Autocorrect for Mac

*🇹🇷 Türkçe sürüm için [README.tr.md](README.tr.md) dosyasına bakın.*

Type Turkish on an English keyboard — this little menu bar app fixes the
letters for you, automatically, as you type.

For example, if you type:

> bugun cok guzel bir gun

it instantly becomes:

> bugün çok güzel bir gün

It works everywhere on your Mac — in your browser, in Mail, in WhatsApp, in
any app. You turn it on and off with a single click from the menu bar (the
row of small icons at the top-right of your screen).

- **TR·off** in the menu bar means it's currently doing nothing.
- **TR·on** means it's actively correcting as you type.

When it's off, your typing is completely untouched.

---

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
   **Enabled** to turn correction on. 🎉
5. The first time it tries to listen to your keystrokes, macOS will ask for
   two permissions — click **Open System Settings** on each prompt (or go
   there manually) and turn **TurkishAutocorrect** on under:
   - **Privacy & Security → Accessibility**
   - **Privacy & Security → Input Monitoring**

   If you don't see a prompt and correction just does nothing, check both
   of those lists directly — the toggle is probably still off.
6. Want it running automatically every time you log in? Click the menu bar
   icon and check **Start at Login**.

That's it — no Python, no `git clone`, no Terminal required. Everything
below this point is for developers building or modifying the app from
source.

## Using it

1. Click **TR·off** in the menu bar.
2. Check **Enabled** — the title changes to **TR·on**.
3. Type anywhere — words are corrected the moment you press space, enter,
   or punctuation.
4. To pause it, uncheck **Enabled** again (back to **TR·off**).
5. **Quit** disables correction but leaves the icon in the menu bar, so
   you're never stuck without a way to turn it back on — it doesn't fully
   exit the app. If you enabled **Start at Login**, the background process
   also keeps running so it's ready the moment you re-enable it.

### Try it out

Open the **TextEdit** app, start a new document, and type
`bugun cok guzel bir gun ` (with a space at the end). It should turn into
`bugün çok güzel bir gün `.

## How it works

- The menu bar icon and menu are built with
  [`rumps`](https://github.com/jaredks/rumps).
- Keystrokes are observed system-wide (without blocking them) using
  [`pynput`](https://github.com/moses-palmer/pynput).
- While enabled, the app collects the letters of the word you're currently
  typing. At each word boundary (space, punctuation, enter, tab) it runs
  the word through
  [`turkish-deasciifier`](https://github.com/emres/turkish-deasciifier) —
  the Python port of Deniz Yüret's context-based Turkish deasciification
  algorithm (so it correctly picks e.g. `güzel` vs `gzel` based on
  surrounding letters). If the result differs, it sends backspaces to erase
  the ASCII word and types the corrected Turkish word in its place.
- That library isn't published on PyPI, so `requirements.txt` installs it
  directly from GitHub via `git+https://github.com/emres/turkish-deasciifier.git`.
- The downloadable `.app` is built with [`py2app`](https://py2app.readthedocs.io/)
  (see `setup.py`), bundling its own Python interpreter so end users don't
  need Python installed at all.

## Known limitations

- If you move the cursor mid-word (arrow keys, clicking elsewhere), that
  word is left alone rather than risking a wrong correction.
- Words containing digits (like `gun2`) aren't corrected.
- The correction is context-aware but not perfect — very occasionally a
  word may be corrected in a way you didn't intend. Just press backspace
  and retype it with correction toggled off.
- There's a small window where an injected backspace/retype and your next
  keystroke could theoretically interleave; not observed in practice but
  worth knowing about if you ever see garbled output.

## Ideas for later

- Custom `.icns` app icon (currently uses py2app's generic default).
- A proper menu bar icon instead of the `TR·on` / `TR·off` text.
- Notarize the release with a paid Apple Developer account to remove the
  Gatekeeper "Open Anyway" step entirely.

---

## Running from source (developers / contributors)

Everything below this point is for building or modifying the app. If you
just want to use it, see [Download](#download-for-everyone--no-terminal-needed)
above.

### What you need

- A Mac (macOS).
- Python 3 installed. Most Macs already have it; if not, you can download
  it from [python.org](https://www.python.org/downloads/).

### One-time setup

**1. Clone the repo:**

```bash
git clone https://github.com/eicyer/os-turkish-deasciifier.git
cd os-turkish-deasciifier
```

**2. Install its dependencies:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

This creates a private folder called `venv` with everything the app needs;
it doesn't change anything else on your Mac.

### Running it

```bash
source venv/bin/activate
python app.py
```

You should see `TR·off` appear in your menu bar. Click it and check
**Enabled** to turn correction on.

#### Running automatically in the background (recommended)

Instead of launching `app.py` by hand every time, register it as a per-user
**LaunchAgent** so macOS starts it automatically at login and relaunches it
(`KeepAlive`) if it ever crashes:

```bash
./install-launchagent.sh
```

This writes `~/Library/LaunchAgents/com.github.eicyer.tr-autocorrect.plist`
and starts it immediately — `TR·off` should appear in the menu bar within a
few seconds, no Terminal window needed from then on.

To stop the background process entirely (e.g. before uninstalling or
updating the code):

```bash
./uninstall-launchagent.sh
```

This stops it and removes the plist so it won't come back at next login
either. Re-run `./install-launchagent.sh` (or double-click
`TurkishAutocorrect.command`) to bring it back.

Trade-offs of running this way, worth knowing:
- Accessibility/Input Monitoring permissions are effectively granted
  continuously, not just while you have it open.
- A small amount of CPU/memory stays resident all the time, even when
  **Enabled** is off, until you uninstall it.
- If the app fails at startup, `launchd` retries every ~10s
  (`ThrottleInterval`) rather than looping instantly.
- There's no attached Terminal window, so errors go to
  `tr-autocorrect.log` in this folder instead of stdout — check there if
  something's not working.

If you'd rather not run it as a background daemon, just run `python app.py`
manually each time — to stop it you'll need `Ctrl+C` in the Terminal window
it's running in.

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
3. In the file picker that opens, press `Cmd+Shift+G`, then paste in the
   path to your venv's Python and press Enter. To find that path, run this
   in Terminal from the app's folder:
   ```bash
   venv/bin/python3 -c "import sys; print(sys.executable)"
   ```
   Copy the line it prints — that's the path to add.
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

### Building the downloadable `.app`

```bash
source venv/bin/activate
pip install py2app
python3 setup.py py2app
```

Produces `dist/TurkishAutocorrect.app`. See `.github/workflows/release.yml`
for how this is built, ad-hoc signed, packaged into a DMG, and published to
GitHub Releases automatically when a `v*.*.*` tag is pushed.
