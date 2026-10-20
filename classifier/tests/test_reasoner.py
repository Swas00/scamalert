from types import SimpleNamespace

import classifier
import reasoner
from reasoner import Verdict

SCAM = "Sir your KYC expired, share the OTP immediately or account will be blocked"


def fake(verdict):
    return lambda transcript: verdict


def test_falls_back_to_rules_without_claude(monkeypatch):
    monkeypatch.setattr(reasoner, "analyze", fake(None))
    r = classifier.classify_full(SCAM)
    assert r["reasoner"] == "rules" and r["explanation"] is None
    assert r["risk_score"] >= 60 and r["category"] == "fake_kyc_update"


def test_blends_claude_verdict(monkeypatch):
    v = Verdict(category="fake_bank_officer", risk_score=90, explanation="Asks for OTP.",
                flagged_phrases=["share the OTP", "made up phrase not in transcript"])
    monkeypatch.setattr(reasoner, "analyze", fake(v))
    r = classifier.classify_full(SCAM)
    assert r["reasoner"] == "claude+rules"
    assert r["category"] == "fake_bank_officer"
    assert "made up phrase not in transcript" not in r["flagged_phrases"]  # hallucinated phrases dropped
    assert r["explanation"] == "Asks for OTP."
    assert 60 <= r["risk_score"] <= 100


def test_claude_can_clear_false_positive(monkeypatch):
    text = "I want a refund for my order, it arrived damaged."
    v = Verdict(category="none", risk_score=2, explanation="Normal customer request.")
    monkeypatch.setattr(reasoner, "analyze", fake(v))
    r = classifier.classify_full(text)
    assert r["risk_score"] < 30 and r["category"] is None


def test_analyze_returns_none_without_key(monkeypatch):
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    monkeypatch.setattr(reasoner, "_client", None)
    assert reasoner.analyze(SCAM) is None


def test_analyze_handles_refusal(monkeypatch):
    stub = SimpleNamespace(messages=SimpleNamespace(
        parse=lambda **kw: SimpleNamespace(stop_reason="refusal", parsed_output=None)))
    monkeypatch.setattr(reasoner, "_get_client", lambda: stub)
    assert reasoner.analyze(SCAM) is None
