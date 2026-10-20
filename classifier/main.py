import os
import secrets

from dotenv import load_dotenv

load_dotenv()  # must run before local imports that read env vars

import requests
from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from classifier import classify_full
from language import detect_language
from warning_texts import warning_text

GNANI_TTS_URL = "https://api.vachana.ai/api/v1/tts/inference"
TTS_MODEL = os.getenv("TTS_MODEL", "timbre-v2.5")
TTS_VOICE = os.getenv("TTS_VOICE", "Nalini")

def require_token(x_internal_token: str | None = Header(default=None)):
    """When INTERNAL_TOKEN is set, only callers that send it (our backend) may use the API."""
    expected = os.getenv("INTERNAL_TOKEN")
    if expected and not secrets.compare_digest(x_internal_token or "", expected):
        raise HTTPException(401, "Unauthorized")


app = FastAPI(title="ScamAlert Classifier")


class ClassifyIn(BaseModel):
    transcript: str


class WarnIn(BaseModel):
    category: str | None = None
    transcript: str | None = None  # language is detected from this when given
    language: str = "en-IN"  # fallback / explicit hint


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/classify", dependencies=[Depends(require_token)])
def classify(body: ClassifyIn):
    return {**classify_full(body.transcript), "language": detect_language(body.transcript)}


@app.post("/warn", dependencies=[Depends(require_token)])
def warn(body: WarnIn):
    api_key = os.getenv("GNANI_API_KEY")
    if not api_key:
        raise HTTPException(500, "GNANI_API_KEY is not set")
    language = detect_language(body.transcript) if body.transcript else body.language
    text, language = warning_text(body.category, language)
    resp = requests.post(
        GNANI_TTS_URL,
        headers={"X-API-Key-ID": api_key, "Content-Type": "application/json"},
        json={
            "text": text, "model": TTS_MODEL, "voice": TTS_VOICE, "language": language,
            "speed": 1.0,
            "audio_config": {"sample_rate": 24000, "num_channels": 1, "sample_width": 2,
                             "encoding": "linear_pcm", "container": "wav"},
        },
        timeout=30,
    )
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"Gnani TTS error: {resp.text[:300]}")
    return Response(content=resp.content, media_type="audio/wav",
                    headers={"X-Warning-Language": language})
