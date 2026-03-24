# Setup

## 1. Install system dependencies

```bash
brew install portaudio ffmpeg
```

## 2. Create a virtual environment

> Use Homebrew Python, not conda — pyobjc requires system framework linkage.

```bash
/opt/homebrew/bin/python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

The first `pip install` will download the Whisper `base.en` model (~145 MB) on first run.

## 3. Add your Anthropic API key

```bash
cp .env.example .env
# edit .env and paste your key
```

## 4. Grant permissions (one-time)

Run the app once:
```bash
source .venv/bin/activate
python run.py
```

macOS will prompt for **Microphone** access — allow it.

For **Accessibility** (required for fn key detection and text injection):
- Open **System Settings → Privacy & Security → Accessibility**
- Click `+` and add **Terminal** (or your terminal app)
- Restart the app after granting

## 5. Install as a background service (runs at login, no terminal needed)

```bash
./install.sh
```

This registers a launchd agent that starts littlebird at login and keeps it running.
Logs go to `~/Library/Logs/littlebird.log`.

To uninstall:
```bash
./uninstall.sh
```

### Run manually (terminal, for debugging)

```bash
source .venv/bin/activate
python run.py
```

Hold `fn` to record. Release to transcribe and inject text into the focused app.

## Changing the Whisper model

Edit `littlebird/config.py`:
- `tiny.en` — fastest, least accurate (~75 MB)
- `base.en` — good balance (~145 MB) ← default
- `small.en` — better accuracy, ~2x slower (~465 MB)
