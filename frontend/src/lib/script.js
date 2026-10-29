// Guess a BCP-47 language tag for a transcript from its dominant script, so screen readers and the browser's font fallback
// treat Kannada as Kannada, and so on. Latin text is reported as English.
const SCRIPTS = [
  ["hi", /[ऀ-ॿ]/g], ["kn", /[ಀ-೿]/g], ["ta", /[஀-௿]/g], ["te", /[ఀ-౿]/g],
  ["ml", /[ഀ-ൿ]/g], ["bn", /[ঀ-৿]/g], ["gu", /[઀-૿]/g], ["pa", /[਀-੿]/g],
];

export function langOf(text) {
  let best = "en", most = 0;
  for (const [code, re] of SCRIPTS) {
    const n = (text || "").match(re)?.length || 0;
    if (n > most) { best = code; most = n; }
  }
  return best;
}
