---
title: ScamAlert API
emoji: 🛡️
colorFrom: blue
colorTo: pink
sdk: docker
app_port: 7860
pinned: false
---

# ScamAlert API

Backend for [ScamAlert](https://scamalert-tau.vercel.app): a Node/Express API that transcribes a call with Gnani Prisma,
scores it for scam patterns with a Python rule engine, and speaks a warning with Gnani Timbre. One container runs both
processes; only the Node API is public.

Health check: `/api/health`. Source: https://github.com/Swas00/scamalert

Required Space secrets: `GNANI_API_KEY`, and `FRONTEND_ORIGIN` (the website's URL, for CORS).
Optional: `MONGODB_URI` (usage statistics only), `RATE_LIMIT_PER_HOUR` (default 20).
