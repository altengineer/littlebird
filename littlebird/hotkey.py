"""
Installs a listen-only CGEventTap to detect fn key press/release.
Uses kCGEventFlagsChanged + NX_SECONDARYFNMASK (0x800000).

The tap callback is minimal — it only flips a threading.Event.
All heavy work happens on a separate worker thread.
"""

import Quartz
import CoreFoundation
from . import config


def install(on_press, on_release):
    """
    Install a global fn-key event tap.
    on_press / on_release are callables invoked on the main thread (fast, no I/O).
    Returns the tap handle (keep alive).
    """
    _state = {"fn_down": False}

    def _callback(proxy, event_type, event, refcon):
        if event_type != Quartz.kCGEventFlagsChanged:
            return event

        flags = Quartz.CGEventGetFlags(event)
        fn_now = bool(flags & config.FN_KEY_FLAG)

        if fn_now and not _state["fn_down"]:
            _state["fn_down"] = True
            on_press()
        elif not fn_now and _state["fn_down"]:
            _state["fn_down"] = False
            on_release()

        return event

    # kCGEventTapOptionListenOnly = 1  (won't block events even if callback is slow)
    tap = Quartz.CGEventTapCreate(
        Quartz.kCGSessionEventTap,
        Quartz.kCGHeadInsertEventTap,
        1,  # kCGEventTapOptionListenOnly
        Quartz.CGEventMaskBit(Quartz.kCGEventFlagsChanged),
        _callback,
        None,
    )

    if tap is None:
        raise RuntimeError(
            "Could not create event tap.\n"
            "Grant Accessibility access to Terminal (or your Python binary) in:\n"
            "  System Settings → Privacy & Security → Accessibility"
        )

    source = Quartz.CFMachPortCreateRunLoopSource(None, tap, 0)
    CoreFoundation.CFRunLoopAddSource(
        CoreFoundation.CFRunLoopGetCurrent(),
        source,
        CoreFoundation.kCFRunLoopDefaultMode,
    )
    Quartz.CGEventTapEnable(tap, True)
    return tap, source
