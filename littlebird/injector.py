import time
import subprocess
import Quartz
from . import config

# Keycode for 'v'
_KEYCODE_V = 0x09


def inject(text: str):
    # 1. Save current clipboard
    original = subprocess.run(["pbpaste"], capture_output=True, text=True).stdout

    # 2. Write new text to clipboard
    subprocess.run(["pbcopy"], input=text, text=True)
    time.sleep(0.05)

    # 3. Simulate Cmd+V
    src = Quartz.CGEventSourceCreate(Quartz.kCGEventSourceStateHIDSystemState)

    key_down = Quartz.CGEventCreateKeyboardEvent(src, _KEYCODE_V, True)
    Quartz.CGEventSetFlags(key_down, Quartz.kCGEventFlagMaskCommand)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, key_down)

    key_up = Quartz.CGEventCreateKeyboardEvent(src, _KEYCODE_V, False)
    Quartz.CGEventSetFlags(key_up, Quartz.kCGEventFlagMaskCommand)
    Quartz.CGEventPost(Quartz.kCGHIDEventTap, key_up)

    # 4. Wait for the target app to consume the paste, then restore clipboard
    time.sleep(config.CLIPBOARD_RESTORE_SECONDS)
    subprocess.run(["pbcopy"], input=original, text=True)
