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

## Hosting the API without depending on one provider
The repo root has a `Dockerfile` that runs the **whole API in one container**: the Node backend (public) and the Python classifier
(loopback only, started first by `deploy/start.sh`). One free instance instead of two; either process dying restarts the whole service.
Python dependencies are installed from `classifier/requirements.lock` (the exact versions the tests passed with).

**Option A: Hugging Face Spaces (free, no card)**
1. Create a Space at https://huggingface.co/new-space: SDK **Docker**, template **Blank**.
2. Space **Settings → Variables and secrets**: add `GNANI_API_KEY` and `FRONTEND_ORIGIN` (`https://scamalert-tau.vercel.app`); optionally `MONGODB_URI` and `RATE_LIMIT_PER_HOUR`.
3. From this repo run `deploy/push-to-hf.sh https://huggingface.co/spaces/<user>/<space>` (Git asks for your username and a **write** access token as the password).
4. When the Space shows *Running*, open `https://<user>-<space>.hf.space/api/health`, then set `VITE_API_URL` to that address in Vercel and redeploy the frontend.

**Option B: Render (Docker runtime)**: New → Web Service → connect this repo → Language **Docker** → add the same environment variables.
`INTERNAL_TOKEN` is not needed in the single-container setup, because the classifier is not reachable from outside the container.

## Deployment (Vercel + Render + MongoDB Atlas)
1. **MongoDB Atlas:** create a free M0 cluster, a database user, and allow access from anywhere (Render IPs change). Copy the connection string as `MONGODB_URI`.
2. **Render:** New -> Blueprint, point at this repo (`render.yaml` defines `scamalert-classifier` and `scamalert-backend`). Enter the secrets Render asks for: `GNANI_API_KEY` on both, `MONGODB_URI`, `CLASSIFIER_URL` (the classifier's public URL), and later `FRONTEND_ORIGIN`.
3. **Vercel:** import the repo with root directory `frontend`, and set `VITE_API_URL` to the backend's Render URL. Then put the Vercel URL into the backend's `FRONTEND_ORIGIN` on Render and redeploy it.
4. Check `https://<backend>/api/health`, then try a sample call on the site.

**Service-to-service address:** on Render, set the backend's `CLASSIFIER_URL` to the classifier's **Internal** address (classifier service → Connect → Internal; `http://<name>:<port>`, same region and workspace), not its public `https://…onrender.com` address, which Render's edge can bot-challenge (HTTP 429 "Just a moment…") when called server-to-server. The single-container image avoids this entirely.

Notes: Render's free tier sleeps after inactivity (first request can take about a minute), so open the site before recording a demo. `/api/analyze` is rate limited per IP (`RATE_LIMIT_PER_HOUR`, default 20) because every analysis spends Gnani credits. The Claude layer stays off unless `ANTHROPIC_API_KEY` is set on the classifier service.

## Measured accuracy
Held-out scam/safe tests, Prisma transcription error (English, Hindi, Hinglish; clean, noisy and harsh audio) and honest caveats are in [samples/RESULTS.md](samples/RESULTS.md). Reproduce with `classifier/venv/bin/python samples/measure.py heldout2`.

## Data handling
Use synthetic or test audio only: no real calls, phone/account/Aadhaar/PAN numbers. The backend stores only usage statistics (language, score, category), never transcripts or the phrases quoted from them.

## Language support
| Language | Transcription (Prisma) | Scam detection | Spoken warning (Timbre) |
|---|---|---|---|
| English | yes | yes | yes |
| Hindi / Hinglish | yes | yes | yes |
| Kannada | yes | **beta** (weak on unseen wording, see `samples/RESULTS.md`) | yes |
| Tamil, Telugu, Malayalam, Marathi, Bengali, Gujarati, Punjabi | yes | **no**: the transcript is shown without a verdict | no |

The interface is available in English and Hindi. Hindi and Kannada text has not been reviewed by a native speaker.

## Frontend design and the DataRain background
The interface is a dark glass-panel design over an animated canvas background (`frontend/src/components/ui/data-rain.tsx`).

- **Where things live:** reusable UI primitives go in `frontend/src/components/ui/` (the shadcn convention: the shadcn CLI writes there and `@/components/ui/...` is the import path other tools expect); app-specific components stay in `frontend/src/components/`. Styles and design tokens are in `frontend/src/index.css`.
- **TypeScript:** the app is JavaScript, but `.tsx` components work out of the box (Vite compiles them). `npm run typecheck` checks the TypeScript files. The `@/` alias maps to `frontend/src/` (see `vite.config.js` and `tsconfig.json`).
- **shadcn CLI:** not installed, because the component is self-contained. To add more shadcn components later, run `npx shadcn@latest init` in `frontend/` and point its aliases at `@/components`.
- **Tuning the background:** `<DataRain />` accepts `count`, `flowSpeed`, `obstacleRadius`, `autopilot`, `fullscreen` and `palette`. Its colours come from the `--dr-*` variables in `index.css`. It never takes pointer events, pauses when the tab is hidden, lowers its own particle count on slow devices, and renders a single static frame (no animation loop) when the visitor prefers reduced motion.
- **Legibility:** all text sits on `.panel` glass surfaces; text colours are checked for WCAG AA contrast against the panel colour, including when bright streaks show through.
- **Printing:** the print stylesheet switches to dark-on-white and leaves out the background and controls.
