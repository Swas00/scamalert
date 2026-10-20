import test from "node:test";
import assert from "node:assert/strict";
import { segments } from "./highlight.js";

const hits = (text, phrases) => segments(text, phrases).filter((s) => s.hit).map((s) => s.text);

test("matches classifier phrases against Prisma's letter-by-letter Hindi acronyms", () => {
  const t = "आपका के वाई सी एक्सपायर हो गया है, के वाई सी अपडेट करना पड़ेगा। वो ओ टी पी बताओ";
  assert.deepEqual(hits(t, ["केवाईसी एक्सपायर", "केवाईसी अपडेट", "ओटीपी बताओ"]), ["के वाई सी एक्सपायर", "के वाई सी अपडेट", "ओ टी पी बताओ"]);
});

test("Latin phrases do not match inside longer words and ignore case", () => {
  assert.deepEqual(hits("My OTP, robotp and Share the OTP now", ["otp", "share the otp"]), ["OTP", "Share the OTP"]);
});

test("prefers the longest phrase and preserves the full text", () => {
  const segs = segments("share the otp now", ["otp", "share the otp"]);
  assert.equal(segs.map((s) => s.text).join(""), "share the otp now");
  assert.deepEqual(hits("share the otp now", ["otp", "share the otp"]), ["share the otp"]);
});

test("handles empty input", () => {
  assert.deepEqual(segments("", ["x"]), [{ text: "", hit: false }]);
  assert.deepEqual(segments("hello", []), [{ text: "hello", hit: false }]);
});
