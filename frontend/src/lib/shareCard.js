// Draws a 1200x630 result card (verdict, score, marked phrases) on a canvas, in the page's current theme.
// No transcript text is drawn - only the verdict and the short flagged phrases - so a card is safe to post.
import { levelOf } from "./samples.js";

const W = 1200, H = 630, PAD = 64, SCALE = 2;
const SERIF = '"Fraunces", "Noto Serif Devanagari", Georgia, serif';
const SANS = '"Public Sans", "Noto Sans Devanagari", system-ui, sans-serif';
const MONO = '"IBM Plex Mono", ui-monospace, Menlo, monospace';

function tokens() {
  const css = getComputedStyle(document.documentElement);
  const v = (n) => css.getPropertyValue(n).trim();
  return { paper: v("--paper"), surface: v("--surface"), ink: v("--ink"), ink2: v("--ink-2"), muted: v("--muted"), rule: v("--rule") };
}

async function loadFonts() {
  await Promise.all([
    document.fonts.load(`600 72px Fraunces`, "High risk 0123456789"),
    document.fonts.load(`400 26px "Noto Serif Devanagari"`, "अआक"),
    document.fonts.load(`400 24px Fraunces`, "phrase"),
    document.fonts.load(`500 22px "Public Sans"`, "Looks like"),
    document.fonts.load(`500 14px "IBM Plex Mono"`, "SAFE"),
  ].map((p) => p.catch(() => null)));
}

function fit(ctx, text, maxW) {
  if (ctx.measureText(text).width <= maxW) return text;
  let t = text;
  while (t.length > 1 && ctx.measureText(t + "…").width > maxW) t = t.slice(0, -1);
  return t.trimEnd() + "…";
}

function spaced(ctx, text, x, y, px = 1.4) {
  // letter-spaced mono label (canvas letterSpacing is not universal yet)
  let cx = x;
  for (const ch of text) { ctx.fillText(ch, cx, y); cx += ctx.measureText(ch).width + px; }
}

export async function renderResultCard(result, { synthetic = false } = {}) {
  await loadFonts();
  const t = tokens();
  const level = levelOf(result.riskScore);
  const css = getComputedStyle(document.documentElement);
  const color = { high: css.getPropertyValue("--danger"), mid: css.getPropertyValue("--warn"), low: css.getPropertyValue("--safe") }[level.key].trim();
  const mark = { high: css.getPropertyValue("--danger-mark"), mid: css.getPropertyValue("--warn-mark"), low: css.getPropertyValue("--safe-mark") }[level.key].trim();

  const canvas = document.createElement("canvas");
  canvas.width = W * SCALE; canvas.height = H * SCALE;
  const ctx = canvas.getContext("2d");
  ctx.scale(SCALE, SCALE);
  ctx.textBaseline = "alphabetic";

  ctx.fillStyle = t.paper; ctx.fillRect(0, 0, W, H);

  // wordmark: same glyph as the site header/favicon, drawn in a 30px box aligned to the text
  ctx.fillStyle = t.ink; ctx.font = `600 30px ${SERIF}`; ctx.fillText("ScamAlert", PAD + 40, 85);
  ctx.save();
  ctx.translate(PAD, 58); ctx.scale(30 / 32, 30 / 32);
  ctx.strokeStyle = t.ink; ctx.lineWidth = 2.6; ctx.lineCap = "round";
  [[5, 16, 7, 16], [11, 11, 11, 21], [16, 6, 16, 26], [21, 12, 21, 20]].forEach(([x1, y1, x2, y2]) => {
    ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
  });
  ctx.fillStyle = css.getPropertyValue("--danger").trim(); ctx.beginPath(); ctx.arc(27, 7, 3.2, 0, Math.PI * 2); ctx.fill();
  ctx.restore();

  // verdict + score
  ctx.fillStyle = color; ctx.font = `600 84px ${SERIF}`; ctx.fillText(level.word, PAD, 218);
  if (result.categoryLabel) {
    ctx.fillStyle = t.ink2; ctx.font = `400 28px ${SANS}`; ctx.fillText("Looks like:", PAD, 272);
    const lw = ctx.measureText("Looks like: ").width;
    ctx.fillStyle = t.ink; ctx.font = `600 28px ${SANS}`; ctx.fillText(result.categoryLabel, PAD + lw, 272);
  }
  ctx.textAlign = "right";
  ctx.fillStyle = t.muted; ctx.font = `400 34px ${SERIF}`; ctx.fillText("/100", W - PAD, 218);
  const slashW = ctx.measureText("/100").width;
  ctx.fillStyle = t.ink; ctx.font = `600 150px ${SERIF}`; ctx.fillText(String(result.riskScore), W - PAD - slashW - 8, 218);
  ctx.textAlign = "left";

  // measure bar
  const bx = PAD, bw = W - PAD * 2, by = 312;
  ctx.fillStyle = t.rule; ctx.fillRect(bx, by, bw, 8);
  ctx.fillStyle = color; ctx.fillRect(bx, by, Math.max(0, bw * result.riskScore / 100), 8);
  ctx.fillStyle = t.ink2;
  [30, 70].forEach((p) => ctx.fillRect(bx + bw * p / 100, by - 5, 1, 18));
  ctx.fillStyle = t.muted; ctx.font = `500 14px ${MONO}`;
  spaced(ctx, "SAFE", bx, by + 34);
  spaced(ctx, "SUSPICIOUS", bx + bw * 0.3, by + 34);
  ctx.textAlign = "right"; spaced(ctx, "HIGH RISK", bx + bw - 108, by + 34); ctx.textAlign = "left";

  // marked phrases
  ctx.fillStyle = t.muted; ctx.font = `500 14px ${MONO}`;
  const flags = result.riskScore >= 30 ? (result.flaggedPhrases || []).slice(0, 8) : [];
  spaced(ctx, flags.length ? "SUSPICIOUS PHRASES" : "RESULT", PAD, 404);
  if (!flags.length) {
    ctx.fillStyle = t.ink2; ctx.font = `400 26px ${SANS}`;
    ctx.fillText("No scam patterns known to ScamAlert were found in this call.", PAD, 450);
  } else {
    ctx.font = `400 26px ${SERIF}`;
    let x = PAD, y = 452; const gap = 14, rowH = 50, maxX = W - PAD;
    for (const raw of flags) {
      const label = fit(ctx, raw, 330);
      const w = ctx.measureText(label).width + 22;
      if (x + w > maxX) { x = PAD; y += rowH; }
      if (y > 506) break;
      ctx.fillStyle = mark; ctx.fillRect(x, y - 30, w, 42);
      ctx.fillStyle = t.ink; ctx.fillText(label, x + 11, y);
      x += w + gap;
    }
  }

  // footer
  ctx.fillStyle = t.rule; ctx.fillRect(PAD, 548, W - PAD * 2, 1);
  ctx.fillStyle = t.muted; ctx.font = `500 14px ${MONO}`;
  spaced(ctx, synthetic ? "SYNTHETIC SAMPLE CALL · NOT A REAL CALL" : "ANALYSED WITH SCAMALERT", PAD, 584);
  spaced(ctx, "BUILT ON GNANI AI · PRISMA + TIMBRE", PAD, 606);
  ctx.textAlign = "right"; spaced(ctx, "SCAMALERT-TAU.VERCEL.APP", W - PAD - 215, 606); ctx.textAlign = "left";

  return new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
}

/** Shares the card via the native share sheet when available (phones), otherwise downloads it. */
export async function saveResultCard(result, opts) {
  const blob = await renderResultCard(result, opts);
  if (!blob) throw new Error("Could not create the image.");
  const file = new File([blob], "scamalert-result.png", { type: "image/png" });
  const coarse = window.matchMedia?.("(pointer: coarse)").matches;
  if (coarse && navigator.canShare?.({ files: [file] })) {
    try { await navigator.share({ files: [file], title: "ScamAlert result" }); return "shared"; }
    catch (e) { if (e?.name === "AbortError") return "cancelled"; /* fall through to download */ }
  }
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = "scamalert-result.png";
  document.body.appendChild(a); a.click(); a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
  return "downloaded";
}
