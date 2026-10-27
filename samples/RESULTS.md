# Measured results (synthetic calls, 2026-10-20)

All audio is synthetic: scripted by the author, voiced with Gnani Timbre, then degraded with simulated telephone
channels (clean 16 kHz; "noisy" = 300-3400 Hz band-limit, 8 kHz, 12 dB hiss/hum and mu-law companding; "harsh" = 2 dB SNR
crowd-like noise plus brief dropouts). Transcribed with Gnani Prisma (`/stt/v3`, `format=transcribe`). No real calls or
personal data. Reproduce: `classifier/venv/bin/python samples/measure.py [heldout|heldout2]` (cached transcripts, no credits).

## 1. Prisma transcription error (vs. the scripts' reference text)
WER ignores punctuation and joins letter-by-letter acronyms; CER ignores spaces (Prisma writes Hindi acronyms as
"ओ टी पी"). Hindi/Hinglish references are one valid spelling each, so WER there is an upper bound.

| Language group | Clean | Noisy | Harsh | n clips |
|---|---|---|---|---|
| English | WER 0.0% | 2.7% | 11.1% | 10 |
| Hindi + Hinglish | WER 8.4% (CER 2.9%) | 7.9% (CER 2.8%) | 13.6% (CER 6.0%) | 14 |

(Two script sets pooled, v1 and v2; per-set numbers are in the `measure.py` output.)

## 2. Scam detection, rules-only (the Claude layer was OFF)
"Detected" = score >= 60 with the right category; "warns" = score >= 30 (the app shows "Suspicious" or higher and plays the spoken warning).

| Set | What it is | Scams detected (>=60) | Scams that warn (>=30) | False alarms on safe calls |
|---|---|---|---|---|
| in-sample bank (12 scripts) | rules were written alongside these | 8/8 | 8/8 | 0/4 |
| held-out v1 (12), BEFORE fixes | written without looking at the rules | **0/6** | 0/6 | 1/6 |
| held-out v1, after fixes | contaminated: the fixes came from its failures | 4/6 (3/6 harsh) | 5/6 | 0/6 |
| **held-out v2 (12), scored once** | written before any tuning on it | **3/6** | **6/6** | **0/6** |

v2 numbers were identical across clean, noisy and harsh audio. v2 was scored once; there was no tuning on it afterwards.

## 3. Reading these honestly
- Prisma is not the weak link: error stays low even in 2 dB noise.
- The keyword/pattern rules over-fitted the in-sample scripts (100% there, 0/6 on unseen v1). Request-shape patterns
  ("tell me the code", "approve the request", "send money") generalised: on unseen v2 every scam raised a warning, but only
  half reached the confident level (48-50 vs. a bar of 60).
- Known miss: link-phishing KYC scam in Hinglish (v1), recorded as an expected failure in the tests.
- n is tiny (12 scripts per set, 6 scams each), so the intervals are wide. Scripts were written by the same author who wrote the
  rules (an AI assistant), so v2 is still optimistic. Voices are TTS, not real telephone speech or real scammers.
- The next real gains: the LLM reasoning layer (built, off pending Gnani's answer on third-party LLMs), and real,
  consented, scrubbed call samples. Neither is claimed here.

## 4. Changes made after v2 was scored (2026-10-27)
A "police / government impersonation" ("digital arrest") category was added, partly motivated by one v2 clip
(`g_scam_officer_hi`) that had no matching category. The table in section 2 is the original, pre-change v2 score
and is left as it was. For transparency, re-scoring after the change gives:

- v2 (rules only): scams >= 60: 3/6 clean, **4/6 noisy**, 3/6 harsh; warns (>= 30): 6/6; false alarms: 0/6. The one clip that
  moved is the impersonation call (now labelled `fake_authority`; 50 clean, 78 noisy, 50 harsh).
- v1 and the in-sample set: unchanged.
- v2 is therefore no longer fully held out for that clip. The new category is covered by the author's own regression tests
  (`classifier/tests/test_classifier.py`), which are not accuracy evidence.
