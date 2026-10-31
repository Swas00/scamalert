// Splits a transcript into plain and highlighted segments for the phrases the classifier flagged.
// The classifier works on a normalised transcript (acronyms joined, punctuation removed), while
// Prisma's raw text may read "के वाई सी अपडेट," - so each phrase may be separated by spaces/punctuation.
const GAP = "[\\s,.;:!?।]*";
const escape = (c) => c.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

function phrasePattern(phrase) {
  const body = [...phrase].filter((c) => !/\s/.test(c)).map(escape).join(GAP);
  // Latin phrases must not match inside longer words ("otp" in "robotp"); Devanagari has no such boundary.
  return [...phrase].every((c) => c.charCodeAt(0) < 128) ? `(?<![\\p{L}\\p{N}])${body}(?![\\p{L}\\p{N}])` : body;
}

export function segments(text, phrases) {
  const unique = [...new Set((phrases || []).map((p) => p.trim()).filter(Boolean))].sort((a, b) => b.length - a.length);
  if (!text || !unique.length) return [{ text, hit: false }];
  const re = new RegExp(unique.map(phrasePattern).join("|"), "giu");
  const out = [];
  let last = 0;
  for (const m of text.matchAll(re)) {
    if (m[0] === "") continue;
    if (m.index > last) out.push({ text: text.slice(last, m.index), hit: false });
    out.push({ text: m[0], hit: true });
    last = m.index + m[0].length;
  }
  if (last < text.length) out.push({ text: text.slice(last), hit: false });
  return out;
}
