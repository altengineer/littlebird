import threading
import AppKit

from .recorder import Recorder
from .transcriber import Transcriber
from .statusbar import StatusBar
from . import injector
from . import hotkey


class LittleBird:
    def __init__(self):
        self._recorder = Recorder()
        self._transcriber = Transcriber()
        self._status = StatusBar.alloc().init().setup()
        self._busy = False
        self._lock = threading.Lock()

    def _on_fn_press(self):
        with self._lock:
            if self._busy:
                return
        print("\n🎙  Recording...")
        self._status.set_state("recording")
        self._recorder.start()

    def _on_fn_release(self):
        audio = self._recorder.stop()
        if audio is None:
            print("(too short, ignored)")
            self._status.set_state("idle")
            return
        threading.Thread(target=self._process, args=(audio,), daemon=True).start()

    def _process(self, audio):
        with self._lock:
            self._busy = True
        self._status.set_state("processing")
        try:
            text = self._transcriber.transcribe(audio)
            if not text:
                print("(nothing transcribed)")
                return
            print(f"  transcribed: {text}")

            injector.inject(text)
        finally:
            with self._lock:
                self._busy = False
            self._status.set_state("idle")

    def run(self):
        print("littlebird is running. Hold fn to dictate. Ctrl+C to quit.\n")

        # NSApplication must run on the main thread; it subsumes CFRunLoop
        app = AppKit.NSApplication.sharedApplication()
        app.setActivationPolicy_(AppKit.NSApplicationActivationPolicyAccessory)

        # Install event tap before starting the run loop
        hotkey.install(self._on_fn_press, self._on_fn_release)

        app.run()


def run():
    LittleBird().run()
