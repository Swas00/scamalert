import test from "node:test";
import assert from "node:assert/strict";
import { langOf } from "./script.js";

test("detects the dominant script", () => {
  assert.equal(langOf("आपका केवाईसी अपडेट"), "hi");
  assert.equal(langOf("ನಿಮ್ಮ ಒಟಿಪಿ ಹೇಳಿ"), "kn");
  assert.equal(langOf("உங்கள் கணக்கு"), "ta");
  assert.equal(langOf("మీ ఖాతా"), "te");
  assert.equal(langOf("your account will be blocked"), "en");
});

test("mixed text follows whichever script has more letters; empty falls back to English", () => {
  assert.equal(langOf("हेलो sir आपका OTP बताओ"), "hi");
  assert.equal(langOf(""), "en");
  assert.equal(langOf(undefined), "en");
});
