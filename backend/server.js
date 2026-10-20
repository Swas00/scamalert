import "dotenv/config";
import express from "express";
import cors from "cors";
import multer from "multer";
import axios from "axios";
import FormData from "form-data";
import mongoose from "mongoose";
import { Analysis } from "./models.js";

const PORT = process.env.PORT || 4000;
const CLASSIFIER_URL = process.env.CLASSIFIER_URL || "http://127.0.0.1:8000";
const STT_URL = "https://api.vachana.ai/stt/v3";

const app = express();
app.use(cors());
const upload = multer({ storage: multer.memoryStorage(), limits: { fileSize: 25 * 1024 * 1024 } });

app.get("/api/health", (_req, res) =>
  res.json({ status: "ok", mongo: mongoose.connection.readyState === 1 })
);

app.post("/api/analyze", upload.single("audio"), async (req, res) => {
  if (!req.file) return res.status(400).json({ error: "audio file is required (field: audio)" });
  if (!process.env.GNANI_API_KEY) return res.status(500).json({ error: "GNANI_API_KEY is not set" });

  const languageCode = req.body.language_code || "en-IN";
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
    const { data: cls } = await axios.post(`${CLASSIFIER_URL}/classify`, { transcript });

    // 3. Spoken warning (only when risk is meaningful)
    let warningAudio = null;
    if (cls.risk_score >= 30) {
      const tts = await axios.post(
        `${CLASSIFIER_URL}/warn`,
        { category: cls.category, transcript },
        { responseType: "arraybuffer", timeout: 45000 }
      );
      warningAudio = `data:audio/wav;base64,${Buffer.from(tts.data).toString("base64")}`;
    }

    const result = {
      transcript,
      riskScore: cls.risk_score,
      category: cls.category,
      categoryLabel: cls.category_label,
      flaggedPhrases: cls.flagged_phrases,
      warningAudio,
    };

    // 4. Persist (don't fail the request if Mongo is down)
    if (mongoose.connection.readyState === 1) {
      Analysis.create({ ...result, warningAudio: undefined, languageCode, sttRequestId: stt.data.request_id })
        .catch((e) => console.error("Mongo save failed:", e.message));
    }
    res.json(result);
  } catch (err) {
    const status = err.response?.status || 502;
    const detail = err.response?.data
      ? Buffer.isBuffer(err.response.data) ? err.response.data.toString() : err.response.data
      : err.message;
    console.error("analyze failed:", status, detail);
    res.status(status >= 400 && status < 600 ? status : 502).json({ error: "Analysis failed", detail });
  }
});

mongoose
  .connect(process.env.MONGODB_URI || "mongodb://127.0.0.1:27017/scamalert", { serverSelectionTimeoutMS: 3000 })
  .then(() => console.log("MongoDB connected"))
  .catch((e) => console.warn("MongoDB unavailable (results won't be stored):", e.message));

app.listen(PORT, () => console.log(`Backend listening on :${PORT}`));
