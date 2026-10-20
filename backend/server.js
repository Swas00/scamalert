import "dotenv/config";
import express from "express";
import cors from "cors";
import multer from "multer";
import axios from "axios";
import FormData from "form-data";
import mongoose from "mongoose";
import rateLimit from "express-rate-limit";
import { Analysis } from "./models.js";

const PORT = process.env.PORT || 4000;
const CLASSIFIER_URL = process.env.CLASSIFIER_URL || "http://127.0.0.1:8000";
const STT_URL = "https://api.vachana.ai/stt/v3";
const internalHeaders = process.env.INTERNAL_TOKEN ? { "X-Internal-Token": process.env.INTERNAL_TOKEN } : {};

const app = express();
// Lock CORS to the deployed frontend when FRONTEND_ORIGIN is set (comma-separated); open in local dev.
const origins = (process.env.FRONTEND_ORIGIN || "").split(",").map((o) => o.trim().replace(/\/+$/, "")).filter(Boolean); // browsers send no trailing slash
app.use(cors(origins.length ? { origin: origins } : undefined));
app.set("trust proxy", 1); // behind Render/Railway's proxy, so rate limiting sees the real client IP

// Each analysis spends Gnani credits, so cap requests per IP on the public deployment.
const analyzeLimiter = rateLimit({
  windowMs: 60 * 60 * 1000,
  limit: Number(process.env.RATE_LIMIT_PER_HOUR || 20),
  standardHeaders: true,
  legacyHeaders: false,
  message: { error: "Too many analyses from this address. Please try again later." },
});
// STT accepts <= 60 s of audio, which fits well within 8 MB
const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 8 * 1024 * 1024 } });

// Free hosting puts idle services to sleep. Opening the site pings this endpoint, which also wakes the classifier
// in the background so it is warm by the time someone presses "Analyze".
app.get("/api/health", (_req, res) => {
  axios.get(`${CLASSIFIER_URL}/health`, { timeout: 90000 }).catch(() => {});
  res.json({ status: "ok", mongo: mongoose.connection.readyState === 1 });
});

// A sleeping Render service answers with 502/503/504 (or drops the connection) while it boots; retry until it is up.
const WAKING = new Set([502, 503, 504]);
async function callClassifier(request, { attempts = 14, delayMs = Number(process.env.CLASSIFIER_RETRY_MS || 6000) } = {}) {
  for (let i = 1; ; i++) {
    try {
      return await request();
    } catch (err) {
      const status = err.response?.status;
      const transient = status ? WAKING.has(status) : ["ECONNRESET", "ECONNREFUSED", "ETIMEDOUT", "ECONNABORTED"].includes(err.code);
      if (!transient || i >= attempts) throw err;
      console.warn(`classifier not ready (status=${status || err.code}), retry ${i}/${attempts - 1}`);
      await new Promise((r) => setTimeout(r, delayMs));
    }
  }
}

app.post("/api/analyze", analyzeLimiter, upload.single("audio"), async (req, res) => {
  if (!req.file) return res.status(400).json({ error: "audio file is required (field: audio)" });
  if (!process.env.GNANI_API_KEY) return res.status(500).json({ error: "GNANI_API_KEY is not set" });

  const languageCode = req.body.language_code || "en-IN";
  let stage = "stt"; // which upstream call is running, for error reports
  try {
    // 1. Speech-to-text (Gnani Prisma)
    const form = new FormData();
    form.append("audio_file", req.file.buffer, {
      filename: req.file.originalname || "audio.wav",
      contentType: req.file.mimetype,
    });
    form.append("language_code", languageCode);
    form.append("format", "transcribe");
    const stt = await axios.post(STT_URL, form, {
      headers: { ...form.getHeaders(), "X-API-Key-ID": process.env.GNANI_API_KEY },
      timeout: 60000,
    });
    const transcript = stt.data.transcript || "";

    // 2. Classify
    stage = "classifier /classify";
    const { data: cls } = await callClassifier(() =>
      axios.post(`${CLASSIFIER_URL}/classify`, { transcript }, { headers: internalHeaders, timeout: 70000 })
    );

    // 3. Spoken warning (only when risk is meaningful)
    let warningAudio = null;
    if (cls.risk_score >= 30) {
      stage = "classifier /warn";
      const tts = await callClassifier(() =>
        axios.post(`${CLASSIFIER_URL}/warn`, { category: cls.category, transcript },
          { responseType: "arraybuffer", timeout: 70000, headers: internalHeaders })
      );
      warningAudio = `data:audio/wav;base64,${Buffer.from(tts.data).toString("base64")}`;
    }

    const result = {
      transcript,
      riskScore: cls.risk_score,
      category: cls.category,
      categoryLabel: cls.category_label,
      flaggedPhrases: cls.flagged_phrases,
      explanation: cls.explanation,
      reasoner: cls.reasoner,
      warningAudio,
    };

    // 4. Persist usage statistics only (don't fail the request if Mongo is down). The transcript and the phrases
    // quoted from it are deliberately NOT stored: uploads are untrusted and may contain personal data.
    if (mongoose.connection.readyState === 1) {
      Analysis.create({
        languageCode,
        riskScore: result.riskScore,
        category: result.category,
        categoryLabel: result.categoryLabel,
        reasoner: result.reasoner,
        sttRequestId: stt.data.request_id,
      }).catch((e) => console.error("Mongo save failed:", e.message));
    }
    res.json(result);
  } catch (err) {
    const status = err.response?.status || 502;
    const raw = err.response?.data
      ? Buffer.isBuffer(err.response.data) ? err.response.data.toString() : err.response.data
      : err.message;
    // Upstream error pages can be huge HTML; keep logs and responses short.
    const detail = (typeof raw === "string" ? raw : JSON.stringify(raw)).replace(/\s+/g, " ").slice(0, 300);
    console.error(`analyze failed at [${stage}] status=${status} code=${err.code || "-"}:`, detail);
    res.status(status >= 400 && status < 600 ? status : 502).json({ error: "Analysis failed", stage, detail });
  }
});

app.use((err, _req, res, _next) => {
  if (err.code === "LIMIT_FILE_SIZE") return res.status(413).json({ error: "Audio file too large (max 8 MB, 60 seconds)." });
  console.error(err);
  res.status(500).json({ error: "Server error" });
});

mongoose
  .connect(process.env.MONGODB_URI || "mongodb://127.0.0.1:27017/scamalert", { serverSelectionTimeoutMS: 3000 })
  .then(() => console.log("MongoDB connected"))
  .catch((e) => console.warn("MongoDB unavailable (results won't be stored):", e.message));

app.listen(PORT, () => console.log(`Backend listening on :${PORT}`));
