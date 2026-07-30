#!/bin/bash
# Registers the Turkish autocorrect app as a per-user LaunchAgent so it
# starts automatically at login and is relaunched by launchd (KeepAlive)
# if it ever crashes or exits on its own.
#
# After this, Quit in the menu bar unloads/disables the LaunchAgent
# (see quit_app / _unload_launch_agent in app.py) so it stays stopped
# instead of being instantly respawned. Re-run this script (or
# TurkishAutocorrect.command) to bring it back.

set -e
cd "$(dirname "$0")"
REPO_DIR="$(pwd)"

if [ ! -x "$REPO_DIR/venv/bin/python3" ]; then
  echo "venv/ not found — run the Setup steps in README.md first." >&2
  exit 1
fi

LABEL="com.github.eicyer.tr-autocorrect"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
LOG="$REPO_DIR/tr-autocorrect.log"

mkdir -p "$HOME/Library/LaunchAgents"

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>${REPO_DIR}/venv/bin/python3</string>
        <string>${REPO_DIR}/app.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>${REPO_DIR}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>ThrottleInterval</key>
    <integer>10</integer>
    <key>ProcessType</key>
    <string>Interactive</string>
    <key>LimitLoadToSessionType</key>
    <string>Aqua</string>
    <key>StandardOutPath</key>
    <string>${LOG}</string>
    <key>StandardErrorPath</key>
    <string>${LOG}</string>
</dict>
</plist>
EOF

# Modern launchctl (macOS 10.11+); fall back to the legacy unload/load pair
# on systems where bootstrap isn't available.
UID_NUM="$(id -u)"
if launchctl bootstrap "gui/${UID_NUM}" "$PLIST" 2>/dev/null; then
  :
else
  launchctl unload -w "$PLIST" 2>/dev/null || true
  launchctl load -w "$PLIST"
fi

echo "Installed and started ${LABEL}."
echo "Logs: ${LOG}"
echo "You should see TR·off appear in the menu bar within a few seconds."
