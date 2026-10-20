"""Run the audio bank through Gnani Prisma STT and the classifier; print a results table.

Run from the repo root:  classifier/venv/bin/python samples/evaluate.py [--refresh]
Transcripts are cached in samples/transcripts.json so re-runs don't spend Gnani credits (use --refresh to redo).
"""
import json
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent / "classifier"))
load_dotenv(ROOT.parent / "classifier" / ".env")
os.environ.pop("ANTHROPIC_API_KEY", None)  # rules-only evaluation

from classifier import classify_transcript  # noqa: E402

STT_URL = "https://api.vachana.ai/stt/v3"
CACHE = ROOT / "transcripts.json"
SCAM_MIN, SAFE_MAX = 60, 30  # same thresholds as the unit tests


def stt(path: Path, lang: str) -> str:
    with open(path, "rb") as f:
        r = requests.post(STT_URL, headers={"X-API-Key-ID": os.environ["GNANI_API_KEY"]}, timeout=90,
                          files={"audio_file": (path.name, f, "audio/wav")},
                          data={"language_code": lang, "format": "transcribe"})
    r.raise_for_status()
    return r.json().get("transcript", "")


def main():
    scripts = json.loads((ROOT / "scripts.json").read_text())
    cache = {} if "--refresh" in sys.argv else (json.loads(CACHE.read_text()) if CACHE.exists() else {})
    ok = total = 0
    print(f"{'clip':<24}{'cond':<7}{'score':>6}  {'category':<24}{'verdict'}")
    for s in scripts:
        for cond in ("clean", "noisy", "harsh"):
            key = f"{cond}/{s['id']}"
            if key not in cache:
                cache[key] = stt(ROOT / "audio" / cond / f"{s['id']}.wav", s["lang"])
                CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1))
            r = classify_transcript(cache[key])
            if s["label"] == "scam":
                good = r["risk_score"] >= SCAM_MIN and r["category"] == s["category"]
            else:
                good = r["risk_score"] < SAFE_MAX
            ok += good; total += 1
            print(f"{s['id']:<24}{cond:<7}{r['risk_score']:>6}  {str(r['category']):<24}{'PASS' if good else 'FAIL'}")
    print(f"\n{ok}/{total} passed")


main()
