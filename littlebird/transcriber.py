import numpy as np
from faster_whisper import WhisperModel
from . import config


class Transcriber:
    def __init__(self):
        print(f"Loading Whisper model '{config.WHISPER_MODEL}'...")
        self._model = WhisperModel(
            config.WHISPER_MODEL,
            device=config.WHISPER_DEVICE,
            compute_type=config.WHISPER_COMPUTE_TYPE,
        )
        print("Whisper model ready.")

    def transcribe(self, audio: np.ndarray) -> str:
        segments, _ = self._model.transcribe(
            audio,
            language="en",
            vad_filter=True,
            word_timestamps=False,
        )
        return " ".join(seg.text for seg in segments).strip()
