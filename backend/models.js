import mongoose from "mongoose";

const analysisSchema = new mongoose.Schema(
  {
    transcript: String,
    languageCode: String,
    riskScore: Number,
    category: String,
    categoryLabel: String,
    flaggedPhrases: [String],
    sttRequestId: String,
  },
  { timestamps: true }
);

export const Analysis = mongoose.model("Analysis", analysisSchema);
