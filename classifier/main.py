import os

import requests
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel

from classifier import classify_transcript
from warning_texts import warning_text

load_dotenv()

GNANI_TTS_URL = "https://api.vachana.ai/api/v1/tts/inference"
TTS_MODEL = os.getenv("TTS_MODEL", "timbre-v2.5")
TTS_VOICE = os.getenv("TTS_VOICE", "Nalini")

app = FastAPI(title="ScamAlert Classifier")


class ClassifyIn(BaseModel):
    transcript: str


class WarnIn(BaseModel):
    category: str | None = None
    language: str = "en-IN"


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/classify")
def classify(body: ClassifyIn):
    return classify_transcript(body.transcript)


@app.post("/warn")
def warn(body: WarnIn):
    api_key = os.getenv("GNANI_API_KEY")
    if not api_key:
        raise HTTPException(500, "GNANI_API_KEY is not set")
    text = warning_text(body.category)
    resp = requests.post(
        GNANI_TTS_URL,
        headers={"X-API-Key-ID": api_key, "Content-Type": "application/json"},
        json={
            "text": text, "model": TTS_MODEL, "voice": TTS_VOICE, "language": body.language,
            "speed": 1.0,
            "audio_config": {"sample_rate": 24000, "num_channels": 1, "sample_width": 2,
                             "encoding": "linear_pcm", "container": "wav"},
        },
        timeout=30,
    )
    if resp.status_code != 200:
        raise HTTPException(resp.status_code, f"Gnani TTS error: {resp.text[:300]}")
    return Response(content=resp.content, media_type="audio/wav",
                    headers={"X-Warning-Text": text})
