import threading
import numpy as np
import sounddevice as sd
from . import config


class Recorder:
    def __init__(self):
        self._frames = []
        self._lock = threading.Lock()
        self._stream = None

    def start(self):
        with self._lock:
            self._frames = []
        self._stream = sd.InputStream(
            samplerate=config.SAMPLE_RATE,
            channels=config.CHANNELS,
            dtype="float32",
            latency="low",
            callback=self._callback,
        )
        self._stream.start()

    def stop(self) -> np.ndarray | None:
        if self._stream:
            self._stream.stop()
            self._stream.close()
            self._stream = None

        with self._lock:
            frames = list(self._frames)

        if not frames:
            return None

        audio = np.concatenate(frames, axis=0).flatten()
        duration = len(audio) / config.SAMPLE_RATE
        if duration < config.MIN_AUDIO_SECONDS:
            return None
        return audio

    def _callback(self, indata, frames, time, status):
        with self._lock:
            self._frames.append(indata.copy())
