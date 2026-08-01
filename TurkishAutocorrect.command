#!/bin/bash
# Double-click this in Finder to bring the Turkish autocorrect menu bar
# icon back, without needing to open Terminal yourself. Quit no longer
# removes the icon (it just disables correction — see app.py), so this is
# mainly for: the LaunchAgent isn't installed yet, it was stopped via
# uninstall-launchagent.sh, or it crashed and KeepAlive hasn't caught up.
#
# If the LaunchAgent from install-launchagent.sh is installed, this just
# (re)loads it. Otherwise it falls back to a direct `python app.py` run.

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
