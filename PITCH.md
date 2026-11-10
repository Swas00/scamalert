# ScamAlert: a spoken scam-call warning, built on Gnani Prisma and Timbre

**Solo entry, Great Indian AI Internship Challenge** · Swastik Sahu · Live: https://scamalert-tau.vercel.app · Code: https://github.com/Swas00/scamalert

## Problem
Voice scams ("your KYC is expiring, tell me the OTP", "digital arrest", fake refunds, parcel-with-drugs calls) reach millions of Indians in Hindi, English, Hinglish and regional languages. Targets are often elderly or first-time digital users, the caller creates panic, and the victim has seconds to decide. Most tools check SMS or links, not the spoken call, and few work in Indian languages.

## Solution
Upload or record a call (up to 30 s). ScamAlert transcribes it, scores how likely it is a scam, highlights the exact phrases that caused the score, and **speaks a warning back** in the listener's language.

1. **Gnani Prisma (STT v3)** transcribes the audio, including noisy and code-mixed speech.
2. A **rule engine** (FastAPI) scores the transcript. It looks at what the caller *asks the listener to do* (read out a code, approve a request, stay on the line, move money to a "safe account"), plus urgency, threat and secrecy signals. Fifteen scam types are covered, from fake KYC and UPI refunds to digital arrest, fake jobs, investment groups, APK-link lures and courier/customs scams.
3. **Gnani Timbre (TTS, timbre-v2.5)** turns the verdict into a spoken warning (English, Hindi, Kannada voices).
4. A React app shows the risk score, flagged phrases and a waveform, and can save a share card. A Node/Express backend runs the pipeline.

It is **rules-based, with no LLM**, so it runs for almost nothing, and every flagged phrase can be explained.

## My contribution
Everything: the pipeline and API, the rules and their tests, the evaluation method, the interface (English and Hindi), and the deployment (Vercel + Render). I researched public scam reports and advisories to write the rules.

## Honest results
- **Prisma accuracy:** word error 0-11% in English and 8-14% in Hindi/Hinglish, even at 2 dB noise (synthetic calls, simulated phone-line noise).
- **Independent public test (English text, 1,600 LLM-written dialogues I did not write):** warned on 158 of 160 scam calls, falsely flagged 4 of 160 normal calls. Scored once, after tuning only on the training part. It is optimistic because the test and training parts come from the same generator.
- **My own held-out Hindi/Hinglish audio:** every scam raised a warning, but only about half reached the confident level. A known miss is recorded as a test.
- **Beta, not measured:** Kannada is measured on a small set; Tamil, Telugu, Bengali, Gujarati, Malayalam, Punjabi and Marathi have rules but no real-call tests and need native-speaker review.

## Data and limits
All test calls are **synthetic** (scripted, voiced with Timbre, degraded with simulated noise). No real calls, phone numbers, Aadhaar or PAN anywhere. Only counts are stored, never transcripts. Real-world wording will vary more than my tests do, so a low score is never proof that a call is safe. The free hosting sleeps when idle, so the first request can take up to a minute.

## What's next
Native-speaker review of the regional rules, tests on consented and anonymised real calls, and on-device screening of incoming calls.

Full methodology and numbers: `samples/RESULTS.md`.
