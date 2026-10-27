export const SAMPLES = [
  { file: "kyc-hindi-harsh.wav", labelKey: "sample.kyc", lang: "hi-IN" },
  { file: "upi-hindi-noisy.wav", labelKey: "sample.upi", lang: "hi-IN" },
  { file: "bank-english-harsh.wav", labelKey: "sample.bank", lang: "en-IN" },
  { file: "safe-otp-notice.wav", labelKey: "sample.safe", lang: "en-IN" },
];

export const LANG_CODES = ["en-IN", "hi-IN", "ta-IN", "te-IN", "kn-IN", "ml-IN", "mr-IN", "bn-IN", "gu-IN", "pa-IN"];

// How well scam detection works for the language the user says is spoken. "none" = no rules exist, so no verdict is shown.
export const DETECTION = { "en-IN": "full", "hi-IN": "full", "kn-IN": "beta" };
export const detectionFor = (code) => DETECTION[code] || "none";

export const MAX_SECONDS = 60; // Gnani Prisma REST limit

export function levelOf(score) {
  if (score >= 70) return { key: "high", cls: "text-danger", mark: "var(--danger-mark)", bar: "var(--danger)" };
  if (score >= 30) return { key: "mid", cls: "text-warn", mark: "var(--warn-mark)", bar: "var(--warn)" };
  return { key: "low", cls: "text-safe", mark: "var(--safe-mark)", bar: "var(--safe)" };
}
