# Littlebird 🐦

A local macOS voice dictation tool — hold a key, speak, and your words are typed wherever your cursor is. 

## How it works

1. Hold `fn` to record your voice
2. Release to transcribe with Whisper (runs locally)
3. Text is injected directly into whatever app is focused

No cloud, no subscription — everything runs on your Mac.

## Requirements

- macOS (Apple Silicon or Intel)
- Python 3.11+
- An [Anthropic API key](https://console.anthropic.com) (optional, for AI cleanup)
- Microphone access
- Accessibility access (for text injection)

## Setup

See [setup.md](setup.md) for full instructions.

**Quick start:**

```bash
brew install portaudio ffmpeg
/opt/homebrew/bin/python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # add your API key
python run.py
```

Hold `fn` to record. Release to transcribe and inject text.

## Install as a background service

Runs at login, no terminal needed:

```bash
./install.sh
```

Uninstall with `./uninstall.sh`. Logs at `~/Library/Logs/littlebird.log`.

## Stack

- **Transcription** — faster-whisper (local)
- **Audio capture** — sounddevice
- **Text injection** — PyObjC (Accessibility API)
- **Hotkey detection** — PyObjC (Quartz event tap)
