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
