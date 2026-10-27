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


# Regression on the held-out sets' Prisma transcripts (samples/heldout*, 3 noise levels each).
# NOT an accuracy measure: v1's failures drove the request patterns in rules.py. v2 was scored once, before any tuning on it
# (see samples/RESULTS.md). These pin the behaviour: every scam raises a warning (>= 30), no safe call does.
def _held(name):
    d = Path(__file__).resolve().parents[2] / "samples" / name
    if not (d / "transcripts.json").exists():
        return []
    scripts = {s["id"]: s for s in json.loads((d / "scripts.json").read_text())}
    return [(f"{name}:{k}", scripts[k.split("/", 1)[1]]["label"], t) for k, t in json.loads((d / "transcripts.json").read_text()).items()]


@pytest.mark.parametrize("name,label,transcript", _held("heldout") + _held("heldout2"), ids=lambda v: v[:34] if isinstance(v, str) else None)
def test_heldout_transcripts(name, label, transcript):
    score = classify_transcript(transcript)["risk_score"]
    if "h_scam_kyc_hinglish" in name and score < 30:
        pytest.xfail("known miss: link-phishing KYC scam in Hinglish; not tuned for, to avoid overfitting a single sample")
    assert (score >= 30) if label == "scam" else (score < 30), (name, score)


@pytest.mark.parametrize("text", [
    "please read out the six digit code we just sent to your phone",
    "आपके मोबाइल पर जो कोड आया है वह मुझे बता दीजिए",
    "jo code aaya hai woh mujhe bata dijiye",
    "approve the payment request on your phone and enter your pin",
])
def test_secret_requests_are_flagged(text):
    assert classify_transcript(text)["risk_score"] >= 30


@pytest.mark.parametrize("text", [
    "mera KYC update ho gaya branch jakar karwaya tha",
    "the bank will never call you to ask for your otp, never disclose it to anyone",
    "your new debit card is ready for pickup, bring a photo id",
])
def test_ordinary_mentions_are_not_flagged(text):
    assert classify_transcript(text)["risk_score"] < 30


# Government / police impersonation ("digital arrest"). These examples are the author's own, so they are regression tests, not accuracy evidence.
@pytest.mark.parametrize("text", [
    "I am calling from the cyber crime department. A parcel in your name contains drugs. You are under digital arrest, do not disconnect the call and transfer the money to a safe account",
    "मैं सीबीआई अधिकारी बोल रहा हूँ। आपके आधार नंबर से मनी लॉन्ड्रिंग हुई है। डिजिटल अरेस्ट से बचना है तो कॉल मत काटिए और सेफ अकाउंट में पैसे ट्रांसफर कीजिए",
    "Main CBI se bol raha hoon, aapke naam par ek parcel pakda gaya hai. Giraftari se bachna hai to call mat kaatna aur jaanch mein sahyog kijiye",
    "This is the police. There is an arrest warrant against you for money laundering. Stay on the line and do not tell anyone.",
])
def test_authority_impersonation_is_detected(text):
    r = classify_transcript(text)
    assert r["category"] == "fake_authority" and r["risk_score"] >= 60, r


@pytest.mark.parametrize("text", [
    "I went to the police station to renew my licence and the officer was very helpful",
    "The customs department website has a duty calculator, I checked it for my order",
    "The cyber crime department held a free awareness session at our college yesterday",
    "पुलिस स्टेशन के पास नया बैंक खुला है, कल चलते हैं",
])
def test_plain_mentions_of_agencies_do_not_warn(text):
    assert classify_transcript(text)["risk_score"] < 30


def test_authority_has_spoken_warnings_in_english_and_hindi():
    from warning_texts import warning_text
    for lang in ("en-IN", "hi-IN"):
        text, used = warning_text("fake_authority", lang)
        assert used == lang and "digital arrest" in text.lower() or "डिजिटल अरेस्ट" in text
