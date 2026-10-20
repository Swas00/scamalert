# ScamAlert

Telephonic scam-call detector built on Gnani AI speech APIs (Prisma STT, Timbre TTS).

```
frontend/    React + Vite + Tailwind      :5173
backend/     Node + Express + Mongoose    :4000   POST /api/analyze
classifier/  Python + FastAPI             :8000   POST /classify, POST /warn
```

Flow: browser uploads audio → backend calls Gnani STT (`/stt/v3`) → classifier `/classify` →
classifier `/warn` (Gnani Timbre TTS) → combined result returned and stored in MongoDB.

## Prerequisites
Node 20+, Python 3.10+, MongoDB running locally (optional: without it results just aren't stored), and a Gnani API key.

## Setup
```bash
cp backend/.env.example backend/.env       # set GNANI_API_KEY
cp classifier/.env.example classifier/.env # set GNANI_API_KEY
```

## Run (three terminals)
```bash
# 1. classifier
cd classifier && python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# 2. backend
cd backend && npm install && npm run dev

# 3. frontend
cd frontend && npm install && npm run dev     # http://localhost:5173
```
Start MongoDB with `brew services start mongodb-community` (or `mongod`).

## Notes
- STT accepts audio up to 60 s (WAV, MP3, OGG, FLAC, AAC, M4A). Browser recordings are WebM; if Gnani rejects them, upload WAV/MP3.
- TTS model/voice are configurable via `TTS_MODEL` / `TTS_VOICE` in `classifier/.env` (defaults `timbre-v2.5` / `Nalini`).
- Classification is rule-based (`classifier/rules.py`); the API key is only read from `.env`.

## Tests
```bash
cd classifier && pip install -r requirements-dev.txt && python -m pytest
```
Sample scam/safe transcripts (English, Hinglish, Hindi) live in `classifier/tests/samples.json`.
