"""Score the classifier on an independent public corpus: BothBosu/scam-dialogue (Apache-2.0).

1,600 English phone-call dialogues written by an LLM (nothing real): 800 scams (ssn, refund, support, reward) and 800
legitimate calls (delivery, insurance, telemarketing, wrong number). The data is downloaded at run time and is not stored
in this repository. Use --split train|test|all. The rules were tuned on `train` only; `test` was scored once afterwards.

Run from the repo root:  classifier/venv/bin/python samples/eval_external.py test
"""
import csv
import io
import re
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "classifier"))
from classifier import classify_transcript  # noqa: E402

URL = "https://huggingface.co/datasets/BothBosu/scam-dialogue/resolve/main/scam-dialogue_{}.csv"
split = sys.argv[1] if len(sys.argv) > 1 else "test"
raw = urllib.request.urlopen(URL.format(split)).read().decode("utf-8-sig")
rows = list(csv.DictReader(io.StringIO(raw)))

stats = defaultdict(lambda: [0, 0, 0])  # n, warned (>=30), confident (>=60)
for row in rows:
    text = re.sub(r"\b(?:caller|receiver|suspect|innocent)\s*:", " ", row["dialogue"], flags=re.I)
    score = classify_transcript(text)["risk_score"]
    s = stats[("scam" if row["label"] == "1" else "legit", row["type"])]
    s[0] += 1
    s[1] += score >= 30
    s[2] += score >= 60
for (kind, typ), (n, warned, confident) in sorted(stats.items()):
    print(f"{kind:5s} {typ:13s} n={n:4d}  warned>=30: {warned:4d} ({100 * warned / n:5.1f}%)   >=60: {confident:4d} ({100 * confident / n:5.1f}%)")
scam = [v for (k, _), v in stats.items() if k == "scam"]
legit = [v for (k, _), v in stats.items() if k == "legit"]
print(f"\nscams that warn: {sum(v[1] for v in scam)}/{sum(v[0] for v in scam)}   legit calls falsely warned: {sum(v[1] for v in legit)}/{sum(v[0] for v in legit)}")
