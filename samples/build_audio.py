"""Generate the synthetic call-audio bank with Gnani Timbre, then make phone-quality noisy variants.

Run from the repo root with the classifier venv:  classifier/venv/bin/python samples/build_audio.py
Only synthetic scripts are used (samples/scripts.json) - never real calls or personal data.
Existing clean clips are reused, so re-runs don't spend Gnani credits again.
"""
import io
import json
import os
import sys
import wave
from pathlib import Path

import numpy as np
import requests
from dotenv import load_dotenv
from scipy.signal import butter, resample_poly, sosfilt

ROOT = Path(__file__).parent
load_dotenv(ROOT.parent / "classifier" / ".env")
KEY = os.environ["GNANI_API_KEY"]
TTS_URL = "https://api.vachana.ai/api/v1/tts/inference"
SR = 16000
CLEAN, NOISY, HARSH = ROOT / "audio" / "clean", ROOT / "audio" / "noisy", ROOT / "audio" / "harsh"
rng = np.random.default_rng(7)


def tts(text, voice, language):
    r = requests.post(TTS_URL, headers={"X-API-Key-ID": KEY, "Content-Type": "application/json"}, timeout=60, json={
        "text": text, "model": "timbre-v2.5", "voice": voice, "language": language, "speed": 1.0,
        "audio_config": {"sample_rate": SR, "num_channels": 1, "sample_width": 2,
                         "encoding": "linear_pcm", "container": "wav"}})
    r.raise_for_status()
    with wave.open(io.BytesIO(r.content)) as w:
        assert w.getframerate() == SR and w.getnchannels() == 1, "unexpected TTS format"
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


def write_wav(path, x, sr):
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr)
        w.writeframes((np.clip(x, -1, 1) * 32767).astype(np.int16).tobytes())


def phone_noise(x, snr_db=12, babble=False, dropouts=0):
    """Narrowband 300-3400 Hz telephone channel at 8 kHz + hiss, low hum and mu-law style companding."""
    sos = butter(4, [300, 3400], btype="band", fs=SR, output="sos")
    y = resample_poly(sosfilt(sos, x), 1, 2)  # 16 kHz -> 8 kHz
    t = np.arange(len(y)) / 8000
    noise = rng.normal(size=len(y)) + 0.8 * np.sin(2 * np.pi * 120 * t) + 0.4 * np.sin(2 * np.pi * 240 * t)
    noise *= np.sqrt(np.mean(y**2) / np.mean(noise**2)) / (10 ** (snr_db / 20))
    if babble:  # crowd-like noise: speech-band noise with ~4 Hz syllable-rate amplitude modulation
        b = sosfilt(butter(2, [200, 3000], btype="band", fs=8000, output="sos"), rng.normal(size=len(y)))
        b *= 0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 4 * t + rng.uniform(0, 6)))
        noise += 2.0 * b
        noise *= np.sqrt(np.mean(y**2) / np.mean(noise**2)) / (10 ** (snr_db / 20))
    y = y + noise
    for _ in range(dropouts):  # brief packet-loss gaps (~80 ms)
        i = int(rng.integers(0, max(1, len(y) - 640))); y[i:i + 640] = 0
    mu = 255
    y = np.sign(y) * np.log1p(mu * np.abs(np.clip(y, -1, 1))) / np.log1p(mu)  # companding artefacts
    y = np.round(y * 127) / 127
    y = np.sign(y) * ((1 + mu) ** np.abs(y) - 1) / mu
    return y / max(1e-6, np.max(np.abs(y))) * 0.9


def main():
    for d in (CLEAN, NOISY, HARSH):
        d.mkdir(parents=True, exist_ok=True)
    scripts = json.loads((ROOT / "scripts.json").read_text())
    gap = np.zeros(int(0.5 * SR), dtype=np.float32)
    for s in scripts:
        clean = CLEAN / f"{s['id']}.wav"
        if not clean.exists():
            parts = []
            for seg in s["segments"]:
                parts += [tts(seg["text"], seg["voice"], s["lang"]), gap]
                print(f"  TTS {s['id']} / {seg['voice']}")
            write_wav(clean, np.concatenate(parts), SR)
        with wave.open(str(clean)) as w:
            x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        write_wav(NOISY / f"{s['id']}.wav", phone_noise(x), 8000)
        write_wav(HARSH / f"{s['id']}.wav", phone_noise(x, snr_db=2, babble=True, dropouts=2), 8000)
        print(f"ok {s['id']}: {len(x) / SR:.1f}s")


if __name__ == "__main__":
    sys.exit(main())
