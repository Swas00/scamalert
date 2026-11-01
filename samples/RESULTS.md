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

## 5. Kannada (beta), 2026-10-27
Kannada support = Prisma transcription (`kn-IN`) + Timbre spoken warnings (voice Saanvi) + a first set of Kannada rules.
All audio is synthetic (Timbre voices Saanvi and Kavin), as above. Scripts were written by the author (an AI assistant); the
spoken warnings were checked by a round trip (Timbre speech -> Prisma transcription) but **no native speaker has reviewed
the Kannada text** (warnings or rules).

**Transcription (Prisma), word error rate vs the script text**

| Set | Clean | Noisy | Harsh | n |
|---|---|---|---|---|
| Kannada v2 | 6.1% | 6.9% | 17.2% | 10 |
| Kannada v3 | 10.9% | 13.2% | 14.5% | 10 |

**Scam detection (rules only)**

| Set | What it is | Scams >= 60 | Scams that warn (>= 30) | False alarms |
|---|---|---|---|---|
| `kannada` (6 scam, 4 safe) | development set the rules were built from | 6/6 | 6/6 | 0/4 |
| `kannada2` (5 + 5), BEFORE fixes | fresh wording, scored once | **1/5** | **2/5** | 1/5 |
| `kannada2`, after fixes | contaminated: the fixes came from its misses | 5/5 | 5/5 | 0/5 |
| **`kannada3` (5 + 5), scored once** | fresh wording, written after the fixes | **1/5** | **3/5** | **0/5** |

Same pattern as Hindi: the rules fit the scripts they were built from and generalise poorly to new wording. Kannada scam
detection is therefore **beta**: on unseen scripts it raised a warning for 3 of 5 scams and missed 2. No further tuning was
done on `kannada3`. Because of this, the app tells the user so on Kannada results, and for languages with no rules at all
(Tamil, Telugu, Malayalam, Marathi, Bengali, Gujarati, Punjabi) it shows the transcript without any verdict.

The repo keeps these sets so the numbers can be re-run: `classifier/venv/bin/python samples/measure.py kannada3`.

## 5. Wider rules, 2026-11-01 (what was and was not measured)
Added: nine more scam types, extra wording for the original six, request patterns drawn from public reports of how the calls run
(digital-arrest sequences, APK lures, prepaid-task jobs, pension and KYC-executive calls, gift-card and "safe account" demands), and
beta rules for Tamil, Telugu, Bengali, Gujarati, Malayalam, Punjabi and Marathi.

- **Re-scoring every cached Prisma transcript** (in-sample, v1, v2, Kannada v1-v3; clean, noisy, harsh) with the new rules: the numbers in
  sections 2 and 3 are unchanged, except v1 under harsh noise, which went from 3/6 to 4/6 detected. v1 is already contaminated by earlier
  tuning. No new false alarms on any safe call. (A first version of this change lost two detections because new patterns replaced the
  tuned ones instead of extending them; the before/after comparison caught it and it was fixed in a separate commit.)
- **The new scam types and the regional languages are NOT measured.** Their tests (`classifier/tests/test_more_scams.py`,
  `test_regional.py`) use text written by the same author as the rules, so they prove the rules fire on the intended wording, not that
  they catch real calls. No audio exists for these (Timbre has no voices for the regional languages, and no real calls are used).
- Honest expectation: coverage of the *kind* of call has widened, but unseen wording will still slip through, as the held-out sets showed.

## 6. Independent public corpus, 2026-11-01 (BothBosu/scam-dialogue, Apache-2.0)
1,600 English call dialogues written by an LLM (800 scams: ssn, refund, support, reward; 800 legitimate: delivery, insurance,
telemarketing, wrong number). Not real calls, no personal data; downloaded at run time (`samples/eval_external.py`), not stored here.
This is the first test set the author of the rules did not write. Text only (no audio), so it measures the rules, not Prisma.

| Rules | Scams that warn (>= 30) | Legitimate calls falsely warned |
|---|---|---|
| Before this pass (whole corpus) | 699 / 800 (87.4%) | 32 / 800 (4.0%) |
| After this pass, TRAIN split (tuned on) | 632 / 640 (98.8%) | 28 / 640 (4.4%) |
| After this pass, **TEST split (scored once)** | **158 / 160 (98.8%)** | **4 / 160 (2.5%)** |

Gaps this exposed and fixed: "we overcharged you, give us your bank account and routing number" refund calls (75% caught before),
and unsolicited "your computer is infected, let us remote in" support calls (76% caught before). The first attempt at the fix
raised false alarms on ordinary marketing ("limited time", a price "plus tax"); those patterns were narrowed.

Read these numbers carefully:
- The test split comes from the same LLM and prompt templates as the train split, so it contains near-paraphrases of the training
  dialogues. It is optimistic. Real callers vary far more than 1,600 template-generated dialogues.
- Several "legitimate" delivery calls in the corpus ask for a credit-card number. A real courier would not, so some of the 28-32
  false alarms are arguably label noise; they were deliberately NOT tuned away.
- US-style English only. It says nothing about Hindi, Hinglish or the regional languages (still unmeasured), or about real speech.
- Earlier audio sets (section 2) re-scored identically after this pass.
