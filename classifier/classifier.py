import re
from functools import lru_cache

from rules import CATEGORIES, COMBOS, DAMPENERS, SIGNALS

SIGNAL_CAP = 40  # keep generic signals from dominating on their own


@lru_cache(maxsize=None)
def _pattern(phrase: str) -> re.Pattern:
    # Word boundaries only make sense for Latin phrases; Devanagari uses plain substring matching.
    if phrase.isascii():
        return re.compile(r"(?<![a-z0-9])" + re.escape(phrase) + r"(?![a-z0-9])")
    return re.compile(re.escape(phrase))


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower().replace("’", "'")).strip()


def _matches(text: str, phrases: list[tuple[str, int]]) -> list[tuple[str, int]]:
    """Matched phrases, dropping any that are contained in a longer matched phrase."""
    hits = [(p, w) for p, w in phrases if _pattern(p).search(text)]
    return [(p, w) for p, w in hits if not any(p != q and p in q for q, _ in hits)]


def classify_transcript(transcript: str) -> dict:
    text = _normalize(transcript)

    # Per-category score: sum of matched phrase weights.
    best_key, best_score, best_hits = None, 0, []
    for key, cat in CATEGORIES.items():
        hits = _matches(text, cat["phrases"])
        score = sum(w for _, w in hits)
        if score > best_score:
            best_key, best_score, best_hits = key, score, hits

    # Cross-category signals.
    signal_hits = {g: _matches(text, ph) for g, ph in SIGNALS.items()}
    present = {g for g, h in signal_hits.items() if h}
    signal_score = min(sum(w for h in signal_hits.values() for _, w in h), SIGNAL_CAP)
    combo_score = sum(b for groups, b in COMBOS if all(g in present for g in groups))

    dampen = sum(w for _, w in _matches(text, DAMPENERS))
    total = max(0, best_score + signal_score + combo_score - dampen)

    flagged = []
    for p, _ in best_hits + [h for hits in signal_hits.values() for h in hits]:
        if p not in flagged:
            flagged.append(p)

    return {
        "risk_score": min(total, 100),
        "category": best_key,
        "category_label": CATEGORIES[best_key]["label"] if best_key else None,
        "flagged_phrases": flagged,
        "signals": sorted(present),
    }
