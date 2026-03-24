#!/bin/bash
PLIST="$HOME/Library/LaunchAgents/com.littlebird.plist"

launchctl bootout "gui/$(id -u)/com.littlebird" 2>/dev/null || true
rm -f "$PLIST"

echo "littlebird uninstalled."
