export const SAMPLES = [
  { file: "kyc-hindi-harsh.wav", label: "Fake KYC · Hindi · very noisy", lang: "hi-IN" },
  { file: "upi-hindi-noisy.wav", label: "UPI refund · Hindi · noisy", lang: "hi-IN" },
  { file: "bank-english-harsh.wav", label: "Fake bank officer · English · very noisy", lang: "en-IN" },
  { file: "safe-otp-notice.wav", label: "Genuine OTP notice · safe", lang: "en-IN" },
];

export const LANGS = [
  ["en-IN", "English"], ["hi-IN", "Hindi"], ["ta-IN", "Tamil"], ["te-IN", "Telugu"], ["kn-IN", "Kannada"],
  ["ml-IN", "Malayalam"], ["mr-IN", "Marathi"], ["bn-IN", "Bengali"], ["gu-IN", "Gujarati"], ["pa-IN", "Punjabi"],
];

export const MAX_SECONDS = 60; // Gnani Prisma REST limit

export function levelOf(score) {
  if (score >= 70) return { key: "high", word: "High risk", cls: "text-danger", mark: "var(--danger-mark)", bar: "var(--danger)" };
  if (score >= 30) return { key: "mid", word: "Suspicious", cls: "text-warn", mark: "var(--warn-mark)", bar: "var(--warn)" };
  return { key: "low", word: "Looks safe", cls: "text-safe", mark: "var(--safe-mark)", bar: "var(--safe)" };
}
