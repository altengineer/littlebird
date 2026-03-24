# Audio
SAMPLE_RATE = 16000
CHANNELS = 1
MIN_AUDIO_SECONDS = 0.3  # discard clips shorter than this

# Whisper
WHISPER_MODEL = "base.en"  # options: tiny.en, base.en, small.en
WHISPER_DEVICE = "cpu"
WHISPER_COMPUTE_TYPE = "int8"

# Hotkey
FN_KEY_FLAG = 0x800000  # NX_SECONDARYFNMASK

# Injection
PASTE_SETTLE_SECONDS = 0.3   # wait after Cmd+V before restoring clipboard
CLIPBOARD_RESTORE_SECONDS = 0.5  # total wait before restoring original clipboard
