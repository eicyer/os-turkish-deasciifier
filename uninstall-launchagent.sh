#!/bin/bash
# Fully removes the LaunchAgent installed by install-launchagent.sh:
# stops it (if running) and deletes the plist so it won't come back at
# next login either.

set -e

LABEL="com.github.eicyer.tr-autocorrect"
PLIST="$HOME/Library/LaunchAgents/${LABEL}.plist"
UID_NUM="$(id -u)"

if [ ! -f "$PLIST" ]; then
  echo "No LaunchAgent installed (nothing at ${PLIST})."
  exit 0
fi

launchctl bootout "gui/${UID_NUM}/${LABEL}" 2>/dev/null || \
  launchctl unload -w "$PLIST" 2>/dev/null || true

rm -f "$PLIST"
echo "Removed ${LABEL}."
