# Turkish Autocorrect for Mac

*🇹🇷 Türkçe sürüm için [README.tr.md](README.tr.md) dosyasına bakın.*

Type Turkish on an English keyboard — this little app fixes the letters for
you, automatically, as you type.

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

## What you need

- A Mac (macOS).
- Python 3 installed. Most Macs already have it; if not, you can download it
  from [python.org](https://www.python.org/downloads/).
- About 5 minutes for the one-time setup below.

## One-time setup

You'll need to copy and paste a few commands into the **Terminal** app
(find it with the magnifying-glass search at the top right of your screen —
press `Cmd + Space`, type "Terminal", press Enter).

**Step 1 — Download the app.** In Terminal, paste this and press Enter:

```bash
git clone https://github.com/eicyer/os-turkish-deasciifier.git
cd os-turkish-deasciifier
```

**Step 2 — Install its dependencies.** Paste these lines and press Enter:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

This creates a private folder called `venv` with everything the app needs.
It doesn't change anything else on your Mac.

**Step 3 — Start it:**

```bash
python app.py
```

You should now see **TR·off** appear in your menu bar at the top of the
screen. 🎉

**Step 4 — Give it permission (important!).** The first time you run it,
macOS will block it from seeing your keystrokes until you allow it. See the
next section.

## Giving macOS permission

For the app to read what you type and fix it, macOS requires you to allow it
in **two** places. This is a one-time thing.

1. Open **System Settings → Privacy & Security → Accessibility**.
2. Click the **+** button (you may need to enter your Mac password first).
3. In the file picker that opens, press `Cmd + Shift + G`, paste the path to
   the app's Python, and press Enter. To find that path, run this in
   Terminal from the app's folder:
   ```bash
   venv/bin/python3 -c "import sys; print(sys.executable)"
   ```
   Copy the line it prints — that's the path to add.
4. Make sure the switch next to the newly added item is turned **on**.
5. Now do the exact same thing under **System Settings → Privacy &
   Security → Input Monitoring**.
6. If **Terminal** also appears in either of those lists, turn it on too —
   some Mac versions assign the permission to Terminal instead.
7. Quit the app and start it again (permissions only take effect after a
   restart).

> **Nothing happening when you type?** It's almost always one of these two
> permissions missing. Double-check both lists.

## Using it

1. Click **TR·off** in the menu bar.
2. Click **Enabled** so it gets a checkmark. The title changes to **TR·on**.
3. Type anywhere — words are corrected the moment you press space,
   enter, or punctuation.
4. To pause it, click **Enabled** again (back to **TR·off**).
5. To quit completely, click the menu bar icon and choose **Quit**.

### Try it out

Open the **TextEdit** app, start a new document, and type
`bugun cok guzel bir gun ` (with a space at the end). It should turn into
`bugün çok güzel bir gün `.

## Starting it automatically (recommended)

Instead of starting the app by hand every time, you can have your Mac start
it automatically whenever you log in. In Terminal, from the app's folder,
run:

```bash
./install-launchagent.sh
```

That's it — from now on the **TR·off** icon appears on its own a few seconds
after you log in, no Terminal window needed. If the app ever crashes, macOS
quietly restarts it for you.

A few things worth knowing about this mode:

- **Quit really quits.** Choosing **Quit** from the menu bar also switches
  off the auto-start, so the app doesn't instantly reappear.
- **To bring it back after Quit**, double-click the file
  **`TurkishAutocorrect.command`** in the app's folder (in Finder), or run
  `./install-launchagent.sh` again.
- **If something goes wrong**, error messages are saved to a file called
  `tr-autocorrect.log` in the app's folder instead of being shown on
  screen.
- It uses a small amount of memory even while switched off — comparable to
  any other small menu bar utility.

To completely remove the auto-start:

```bash
./uninstall-launchagent.sh
```

## Good to know (current limitations)

- If you move the cursor in the middle of a word (arrow keys, clicking
  somewhere else), that word is left alone rather than risking a wrong
  correction.
- Words containing digits (like `gun2`) are not corrected.
- The correction is context-aware but not perfect — very occasionally a
  word may be corrected in a way you didn't intend. Just press backspace
  and retype it with correction toggled off.

## For the curious: how it works

- The menu bar icon and menu are built with
  [`rumps`](https://github.com/jaredks/rumps).
- Keystrokes are observed system-wide (without blocking them) using
  [`pynput`](https://github.com/moses-palmer/pynput).
- While enabled, the app collects the letters of the word you're currently
  typing. At each word boundary (space, punctuation, enter, tab) it runs
  the word through
  [`turkish-deasciifier`](https://github.com/emres/turkish-deasciifier) —
  the Python port of Deniz Yüret's context-based Turkish deasciification
  algorithm. If the result differs, it sends backspaces to erase the ASCII
  word and types the corrected Turkish word in its place.
- That library isn't published on PyPI, so `requirements.txt` installs it
  directly from GitHub.
- `install-launchagent.sh` registers the app as a per-user macOS
  **LaunchAgent** (`~/Library/LaunchAgents/com.github.eicyer.tr-autocorrect.plist`)
  with `RunAtLoad` and `KeepAlive`, which is what provides start-at-login
  and auto-restart.

## Ideas for later

- Package as a standalone `.app` with `py2app` so no Terminal setup is
  needed at all.
- A proper menu bar icon instead of the `TR·on` / `TR·off` text.
