"""Honest accuracy report for a script set: Prisma transcription error rates and rules-only scam detection.

Run from the repo root:  classifier/venv/bin/python samples/measure.py [bank|heldout|heldout2] [--refresh] [--with-llm]
Transcripts are cached (samples/transcripts.json or samples/<set>/transcripts.json) so re-runs spend no credits.

Transcription: WER/CER against each script's `reference` text (when present), after removing punctuation and
joining letter-by-letter acronyms the way the classifier does. CER ignores spaces, because Prisma spells Hindi
acronyms letter by letter ("ओ टी पी") which would otherwise inflate WER.
Detection: scam clips must score >= 60 with the right category; safe clips must score < 30.
"""
import json
import os
import re
import sys
from collections import defaultdict
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).parent
sys.path.insert(0, str(ROOT.parent / "classifier"))
load_dotenv(ROOT.parent / "classifier" / ".env")
WITH_LLM = "--with-llm" in sys.argv  # also score the Claude + rules blend (needs ANTHROPIC_API_KEY)
if not WITH_LLM:
    os.environ.pop("ANTHROPIC_API_KEY", None)  # rules-only measurement (default)

import hashlib  # noqa: E402

import reasoner  # noqa: E402
from classifier import _normalize, classify_full, classify_transcript  # noqa: E402

TRANSCRIBE_ONLY = "--transcribe-only" in sys.argv  # fetch/cache transcripts without scoring them (keeps a set unseen)
SET = next((a for a in sys.argv[1:] if not a.startswith("--")), "bank")
SCRIPTS = ROOT / "scripts.json" if SET == "bank" else ROOT / SET / "scripts.json"
AUDIO = ROOT / "audio" if SET == "bank" else ROOT / "audio" / SET
CACHE = ROOT / "transcripts.json" if SET == "bank" else ROOT / SET / "transcripts.json"
LLM_CACHE = ROOT / "llm_cache.json" if SET == "bank" else ROOT / SET / "llm_cache.json"
STT_URL = "https://api.vachana.ai/stt/v3"
CONDS = ("clean", "noisy", "harsh")
SCAM_MIN, SAFE_MAX = 60, 30


def stt(path, lang):
    with open(path, "rb") as f:
        r = requests.post(STT_URL, headers={"X-API-Key-ID": os.environ["GNANI_API_KEY"]}, timeout=90,
                          files={"audio_file": (path.name, f, "audio/wav")}, data={"language_code": lang, "format": "transcribe"})
    r.raise_for_status()
    return r.json().get("transcript", "")


def edit_distance(a, b):
    prev = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        cur = [i]
        for j, y in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (x != y)))
        prev = cur
    return prev[-1]


def words(text):
    return _normalize(text).split()


def wer(ref, hyp):
    r = words(ref)
    return edit_distance(r, words(hyp)) / max(1, len(r))


def cer(ref, hyp):
    r, h = "".join(words(ref)), "".join(words(hyp))
    return edit_distance(r, h) / max(1, len(r))


def script_of(s):
    ref = s.get("reference", "")
    if re.search("[\u0C80-\u0CFF]", ref):
        return "Kannada"
    if re.search("[\u0900-\u097F]", ref):
        return "Hindi/Hinglish"
    return "English"


def install_llm_cache():
    """Cache Claude's verdict per transcript so re-runs are free and reproducible; the prompt is never tuned on these sets."""
    if not os.getenv("ANTHROPIC_API_KEY"):
        sys.exit("--with-llm needs ANTHROPIC_API_KEY (set it in classifier/.env)")
    cache = json.loads(LLM_CACHE.read_text()) if LLM_CACHE.exists() else {}
    real = reasoner.analyze

    def cached(transcript):
        key = f"{reasoner.MODEL}|{hashlib.sha256(transcript.encode()).hexdigest()[:16]}"
        if key not in cache:
            v = real(transcript)
            if v is None:
                return None  # failures are not cached
            cache[key] = v.model_dump()
            LLM_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1))
        return reasoner.Verdict(**cache[key])

    reasoner.analyze = cached


def main():
    if WITH_LLM:
        install_llm_cache()
    score = classify_full if WITH_LLM else classify_transcript
    scripts = json.loads(SCRIPTS.read_text())
    cache = {} if "--refresh" in sys.argv else (json.loads(CACHE.read_text()) if CACHE.exists() else {})
    rows, wer_acc = [], defaultdict(list)
    for s in scripts:
        for cond in CONDS:
            key = f"{cond}/{s['id']}"
            if key not in cache:
                cache[key] = stt(AUDIO / cond / f"{s['id']}.wav", s["lang"])
                CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1))
            hyp = cache[key]
            if TRANSCRIBE_ONLY:
                continue
            r = score(hyp)
            flagged_scam = r["risk_score"] >= SCAM_MIN
            cat_ok = s["category"] in ("any", None) or r["category"] == s["category"]
            ok = (flagged_scam and cat_ok) if s["label"] == "scam" else r["risk_score"] < SAFE_MAX
            warn = r["risk_score"] >= 30
            w = c = None
            if s.get("reference"):
                w, c = wer(s["reference"], hyp), cer(s["reference"], hyp)
                wer_acc[(script_of(s), cond)].append((w, c))
            rows.append(dict(id=s["id"], label=s["label"], cond=cond, score=r["risk_score"], cat=r["category"], expected=s["category"], ok=ok, flagged=flagged_scam, cat_ok=cat_ok, warn=warn, wer=w, cer=c))

    if TRANSCRIBE_ONLY:
        print(f"{SET}: cached {len(cache)} transcripts; nothing scored.")
        return
    print(f"\n=== {SET}: per-clip ===")
    print(f"{'clip':<26}{'cond':<7}{'score':>6}  {'got':<24}{'expected':<24}{'WER':>6}{'CER':>6}  verdict")
    for x in rows:
        print(f"{x['id']:<26}{x['cond']:<7}{x['score']:>6}  {str(x['cat']):<24}{str(x['expected']):<24}"
              f"{'' if x['wer'] is None else format(x['wer'], '.0%'):>6}{'' if x['cer'] is None else format(x['cer'], '.0%'):>6}  {'ok' if x['ok'] else 'MISS' if x['label'] == 'scam' else 'FALSE ALARM'}")

    print(f"\n=== {SET}: detection ({'Claude + rules' if WITH_LLM else 'rules only'}) ===")
    for cond in CONDS:
        sc = [x for x in rows if x["cond"] == cond and x["label"] == "scam"]
        sf = [x for x in rows if x["cond"] == cond and x["label"] == "safe"]
        hi = sum(x["flagged"] for x in sc); cat = sum(x["flagged"] and x["cat_ok"] for x in sc); lo = sum(x["warn"] for x in sc)
        fa = sum(not x["ok"] for x in sf)
        print(f"{cond:<6} scams flagged >=60: {hi}/{len(sc)} (right category: {cat}/{len(sc)}) | flagged >=30: {lo}/{len(sc)} | safe false alarms: {fa}/{len(sf)}")

    print(f"\n=== {SET}: Prisma transcription error vs reference ===")
    for (kind, cond), v in sorted(wer_acc.items()):
        print(f"{kind:<16}{cond:<7} WER {sum(a for a, _ in v) / len(v):5.1%}   CER {sum(b for _, b in v) / len(v):5.1%}   (n={len(v)} clips)")


main()
