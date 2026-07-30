#!/bin/bash
# Double-click this in Finder to bring the Turkish autocorrect menu bar
# icon back after Quit, without needing to open Terminal yourself.
#
# If the LaunchAgent from install-launchagent.sh is installed, this just
# reloads it (Quit unloads/disables it — see app.py — so it won't come
# back on its own). Otherwise it falls back to a direct `python app.py`
# run, same as before the LaunchAgent existed.

set -e
cd "$(dirname "$0")"

LABEL="com.github.eicyer.tr-autocorrect"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
UID_NUM="$(id -u)"

if [ -f "$PLIST" ]; then
  if launchctl print "gui/${UID_NUM}/${LABEL}" >/dev/null 2>&1; then
    echo "${LABEL} is already running."
    read -n 1 -s -r -p "Press any key to close..."
    exit 0
  fi
  launchctl bootstrap "gui/${UID_NUM}" "$PLIST" 2>/dev/null || \
    launchctl load -w "$PLIST"
  echo "Reloaded ${LABEL} — the menu bar icon should appear shortly."
  read -n 1 -s -r -p "Press any key to close..."
  exit 0
fi

if [ ! -d venv ]; then
  echo "venv/ not found — run the Setup steps in README.md first." >&2
  read -n 1 -s -r -p "Press any key to close..."
  exit 1
fi

source venv/bin/activate
exec python app.py
