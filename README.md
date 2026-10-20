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

## Deployment (Vercel + Render + MongoDB Atlas)
1. **MongoDB Atlas:** create a free M0 cluster, a database user, and allow access from anywhere (Render IPs change). Copy the connection string as `MONGODB_URI`.
2. **Render:** New -> Blueprint, point at this repo (`render.yaml` defines `scamalert-classifier` and `scamalert-backend`). Enter the secrets Render asks for: `GNANI_API_KEY` on both, `MONGODB_URI`, `CLASSIFIER_URL` (the classifier's public URL), and later `FRONTEND_ORIGIN`.
3. **Vercel:** import the repo with root directory `frontend`, and set `VITE_API_URL` to the backend's Render URL. Then put the Vercel URL into the backend's `FRONTEND_ORIGIN` on Render and redeploy it.
4. Check `https://<backend>/api/health`, then try a sample call on the site.

Notes: Render's free tier sleeps after inactivity (first request can take about a minute), so open the site before recording a demo. `/api/analyze` is rate limited per IP (`RATE_LIMIT_PER_HOUR`, default 20) because every analysis spends Gnani credits. The Claude layer stays off unless `ANTHROPIC_API_KEY` is set on the classifier service.

## Measured accuracy
Held-out scam/safe tests, Prisma transcription error (English, Hindi, Hinglish; clean, noisy and harsh audio) and honest caveats are in [samples/RESULTS.md](samples/RESULTS.md). Reproduce with `classifier/venv/bin/python samples/measure.py heldout2`.

## Data handling
Use synthetic or test audio only: no real calls, phone/account/Aadhaar/PAN numbers. The backend stores only usage statistics (language, score, category), never transcripts or the phrases quoted from them.
