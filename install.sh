#!/bin/bash
set -e

DIR="$(cd "$(dirname "$0")" && pwd)"
PLIST="$HOME/Library/LaunchAgents/com.littlebird.plist"
PYTHON="$DIR/.venv/bin/python"
LOG="$HOME/Library/Logs/littlebird.log"

if [ ! -f "$PYTHON" ]; then
  echo "ERROR: virtualenv not found at $PYTHON"
  echo "Run: /opt/homebrew/bin/python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
  exit 1
fi

cat > "$PLIST" <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>com.littlebird</string>

  <key>ProgramArguments</key>
  <array>
    <string>$PYTHON</string>
    <string>$DIR/run.py</string>
  </array>

  <key>WorkingDirectory</key>
  <string>$DIR</string>

  <key>RunAtLoad</key>
  <true/>

  <key>KeepAlive</key>
  <true/>

  <key>StandardOutPath</key>
  <string>$LOG</string>

  <key>StandardErrorPath</key>
  <string>$LOG</string>

  <key>EnvironmentVariables</key>
  <dict>
    <key>PATH</key>
    <string>/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin</string>
  </dict>
</dict>
</plist>
EOF

# Unload existing if running
launchctl bootout "gui/$(id -u)/com.littlebird" 2>/dev/null || true

launchctl bootstrap "gui/$(id -u)" "$PLIST"

echo "littlebird installed and running."
echo "Logs: $LOG"
echo ""
echo "To stop:      launchctl stop com.littlebird"
echo "To uninstall: ./uninstall.sh"
