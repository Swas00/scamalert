import re
from functools import lru_cache

import reasoner
from rules import CATEGORIES, CATEGORY_PATTERNS, COMBOS, DAMPENER_PATTERNS, DAMPENERS, SIGNAL_PATTERNS, SIGNALS

LOW_RISK = 30   # below this no scam category is reported
SIGNAL_CAP = 40  # keep generic signals from dominating on their own


@lru_cache(maxsize=None)
def _pattern(phrase: str) -> re.Pattern:
    # Word boundaries only make sense for Latin phrases; Devanagari uses plain substring matching.
    if phrase.isascii():
        return re.compile(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])")
    return re.compile(re.escape(phrase))


# Prisma spells Hindi acronyms letter by letter ("के वाई सी"); join them so rules match.
_SPACED_ACRONYMS = [
    (r"के\s*वाई\s*सी", "केवाईसी"), (r"ओ\s*टी\s*पी", "ओटीपी"), (r"यू\s*पी\s*आई|यु\s*पी\s*आई", "यूपीआई"),
    (r"सी\s*वी\s*वी", "सीवीवी"), (r"ए\s*टी\s*एम", "एटीएम"), (r"\bk\s*y\s*c\b", "kyc"),
    (r"\bo\s*t\s*p\b", "otp"), (r"\bu\s*p\s*i\b", "upi"), (r"\bc\s*v\s*v\b", "cvv"),
]
_PUNCT = re.compile(r"[,.;:!?\"“”‘()\[\]।|-]+")


def _normalize(text: str) -> str:
    text = text.lower().replace("’", "'")
    text = _PUNCT.sub(" ", text)
    text = re.sub(r"\s+", " ", text).strip()
    for pattern, repl in _SPACED_ACRONYMS:
        text = re.sub(pattern, repl, text)
    return text


def _matches(text: str, phrases: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Matched phrases, dropping any that are contained in a longer matched phrase."""
    hits = [(p, w) for p, w in phrases if _pattern(p).search(text)]
    return [(p, w) for p, w in hits if not any(p != q and p in q for q, _ in hits)]


def _regex_hits(text: str, patterns: list[tuple[str, int]]) -> list[tuple[str, int]]:
    hits = []
    for pat, weight in patterns:
        m = re.search(pat, text)
        if m:
            hits.append((m.group(0).strip(), weight))
    return hits


def classify_transcript(transcript: str) -> dict:
    text = _normalize(transcript)

    # Per-category score: sum of matched phrase weights.
    best_key, best_score, best_hits = None, 0, []
    for key, cat in CATEGORIES.items():
        hits = _matches(text, cat["phrases"]) + _regex_hits(text, CATEGORY_PATTERNS.get(key, []))
        score = sum(w for _, w in hits)
        if score > best_score:
            best_key, best_score, best_hits = key, score, hits

    # Cross-category signals.
    signal_hits = {g: _matches(text, ph) + _regex_hits(text, SIGNAL_PATTERNS.get(g, [])) for g, ph in SIGNALS.items()}
    present = {g for g, h in signal_hits.items() if h}
    signal_score = min(sum(w for h in signal_hits.values() for _, w in h), SIGNAL_CAP)
    combo_score = sum(b for groups, b in COMBOS if all(g in present for g in groups))

    dampen = sum(w for _, w in _matches(text, DAMPENERS)) + sum(w for _, w in _regex_hits(text, DAMPENER_PATTERNS))
    total = max(0, best_score + signal_score + combo_score - dampen)

    flagged = []
    for p, _ in best_hits + [h for hits in signal_hits.values() for h in hits]:
        if p not in flagged:
            flagged.append(p)

    if total < LOW_RISK:
        best_key = None  # too weak to name a scam type
    return {
        "risk_score": min(total, 100),
        "category": best_key,
        "category_label": CATEGORIES[best_key]["label"] if best_key else None,
        "flagged_phrases": flagged,
        "signals": sorted(present),
    }


RULES_WEIGHT = 0.4  # final score = 40% rules + 60% Claude when both are available


def classify_full(transcript: str) -> dict:
    """Rules first, then Claude's judgement blended in. Falls back to rules alone if Claude is unavailable."""
    result = classify_transcript(transcript)
    result["reasoner"] = "rules"
    result["explanation"] = None

    verdict = reasoner.analyze(transcript)
    if verdict is None:
        return result

    lowered = transcript.lower()
    verified = [p for p in verdict.flagged_phrases if p.strip() and p.lower() in lowered]  # must be verbatim
    flagged = list(result["flagged_phrases"])
    flagged += [p for p in verified if p.lower() not in (f.lower() for f in flagged)]

    result["risk_score"] = round(RULES_WEIGHT * result["risk_score"] + (1 - RULES_WEIGHT) * verdict.risk_score)
    if verdict.category in CATEGORIES:
        result["category"] = verdict.category
        result["category_label"] = CATEGORIES[verdict.category]["label"]
    elif verdict.category == "other_scam":
        result["category"], result["category_label"] = "other_scam", "Other scam"
    elif verdict.category == "none" and verdict.risk_score < 30:
        result["category"] = result["category_label"] = None
    result["flagged_phrases"] = flagged
    result["explanation"] = verdict.explanation
    result["reasoner"] = "claude+rules"
    return result
