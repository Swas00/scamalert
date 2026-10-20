from rules import CATEGORIES, URGENCY_PHRASES


def classify_transcript(transcript: str) -> dict:
    text = transcript.lower()
    best = None
    for key, cat in CATEGORIES.items():
        hits = [p for p in cat["phrases"] if p in text]
        if hits and (best is None or len(hits) > len(best["hits"])):
            best = {"key": key, "cat": cat, "hits": hits}
    urgency = [p for p in URGENCY_PHRASES if p in text]
    if best is None:
        return {"risk_score": min(len(urgency) * 10, 30), "category": None,
                "category_label": None, "flagged_phrases": urgency}
    score = best["cat"]["weight"] + 15 * (len(best["hits"]) - 1) + 8 * len(urgency)
    return {"risk_score": min(score, 100), "category": best["key"],
            "category_label": best["cat"]["label"], "flagged_phrases": best["hits"] + urgency}
