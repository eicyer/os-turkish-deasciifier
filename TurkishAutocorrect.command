#!/bin/bash
# Double-click this in Finder to (re)launch the Turkish autocorrect menu bar
# app without needing to open Terminal and type commands yourself.
#
# Quitting the app from its menu bar (Quit) fully exits the process, which
# also removes the menu bar icon — since it isn't a packaged .app, there's
# nothing left to click to bring it back except this script (or a fresh
# `python app.py` from Terminal).

set -e
cd "$(dirname "$0")"

if [ ! -d venv ]; then
  echo "venv/ not found — run the Setup steps in README.md first." >&2
  read -n 1 -s -r -p "Press any key to close..."
  exit 1
fi

source venv/bin/activate
exec python app.py
