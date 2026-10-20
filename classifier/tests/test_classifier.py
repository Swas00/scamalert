import json
from pathlib import Path

import pytest

from classifier import classify_transcript

SAMPLES = json.loads((Path(__file__).parent / "samples.json").read_text())
SCAM_THRESHOLD = 60  # scam transcripts must score at least this
SAFE_THRESHOLD = 30  # safe transcripts must score below this (the app warns at >= 30)


@pytest.mark.parametrize("s", SAMPLES["scam"], ids=lambda s: f'{s["lang"]}-{s["category"]}')
def test_scam_detected(s):
    r = classify_transcript(s["text"])
    assert r["risk_score"] >= SCAM_THRESHOLD, r
    assert r["category"] == s["category"], r


@pytest.mark.parametrize("s", SAMPLES["safe"], ids=lambda s: f'{s["lang"]}-{s["text"][:20]}')
def test_safe_not_flagged(s):
    r = classify_transcript(s["text"])
    assert r["risk_score"] < SAFE_THRESHOLD, r


from language import detect_language
from warning_texts import warning_text


@pytest.mark.parametrize("s", SAMPLES["scam"] + SAMPLES["safe"], ids=lambda s: s["text"][:25])
def test_language_detection(s):
    expected = {"en": "en-IN", "hinglish": "hi-IN", "hi": "hi-IN"}[s["lang"]]
    assert detect_language(s["text"]) == expected


def test_warning_language_fallback():
    assert warning_text("lottery_scam", "hi-IN")[1] == "hi-IN"
    assert warning_text("lottery_scam", "ta-IN")[1] == "en-IN"  # no Tamil translation yet


def test_normalizes_spaced_acronyms_and_punctuation():
    r = classify_transcript("आपका के वाई सी एक्सपायर हो गया है, अभी के अभी के वाई सी अपडेट करना पड़ेगा। वो ओ टी पी बताओ!")
    assert r["category"] == "fake_kyc_update" and r["risk_score"] >= SCAM_THRESHOLD, r


def test_weak_match_reports_no_category():
    assert classify_transcript("I want a refund for my order")["category"] is None


# Regression on real Prisma STT output for the synthetic audio bank (samples/transcripts.json).
_ROOT = Path(__file__).resolve().parents[2] / "samples"
_BANK = {s["id"]: s for s in json.loads((_ROOT / "scripts.json").read_text())}
_STT = json.loads((_ROOT / "transcripts.json").read_text()) if (_ROOT / "transcripts.json").exists() else {}


@pytest.mark.parametrize("key", sorted(_STT))
def test_prisma_transcripts(key):
    s = _BANK[key.split("/", 1)[1]]
    r = classify_transcript(_STT[key])
    if s["label"] == "scam":
        assert r["risk_score"] >= SCAM_THRESHOLD and r["category"] == s["category"], r
    else:
        assert r["risk_score"] < SAFE_THRESHOLD, r
