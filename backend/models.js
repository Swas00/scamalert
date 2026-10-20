import mongoose from "mongoose";

const analysisSchema = new mongoose.Schema(
  {
    languageCode: String,
    riskScore: Number,
    category: String,
    categoryLabel: String,
    reasoner: String,
    sttRequestId: String,
  },
  { timestamps: true }
);

export const Analysis = mongoose.model("Analysis", analysisSchema);
