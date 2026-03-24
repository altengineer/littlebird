import objc
import AppKit
from Foundation import NSObject

ICONS = {
    "idle":       "🐦",
    "recording":  "🔴",
    "processing": "⏳",
}


class StatusBar(NSObject):
    @objc.python_method
    def setup(self):
        bar = AppKit.NSStatusBar.systemStatusBar()
        self._item = bar.statusItemWithLength_(AppKit.NSVariableStatusItemLength)

        btn = self._item.button()
        btn.setTitle_(ICONS["idle"])
        btn.setToolTip_("littlebird — hold fn to dictate")

        # Menu with a Quit option
        menu = AppKit.NSMenu.alloc().init()
        quit_item = AppKit.NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Quit littlebird", "terminate:", "q"
        )
        menu.addItem_(quit_item)
        self._item.setMenu_(menu)

        return self

    @objc.python_method
    def set_state(self, state: str):
        """Call from any thread — safely updates on main thread."""
        title = ICONS.get(state, ICONS["idle"])
        self.performSelectorOnMainThread_withObject_waitUntilDone_(
            "applyTitle:", title, False
        )

    def applyTitle_(self, title):
        self._item.button().setTitle_(title)
