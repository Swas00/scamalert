import test from "node:test";
import assert from "node:assert/strict";
import { STR } from "./strings.js";

const keys = (o) => Object.keys(o).sort();
const placeholders = (s) => [...s.matchAll(/\{(\w+)\}/g)].map((m) => m[1]).sort().join(",");

test("Hindi has exactly the same keys as English", () => {
  assert.deepEqual(keys(STR.hi), keys(STR.en));
});

test("no empty strings", () => {
  for (const lang of ["en", "hi"]) for (const [k, v] of Object.entries(STR[lang])) assert.ok(v.trim().length > 0, `${lang}.${k} is empty`);
});

test("placeholders match between languages", () => {
  for (const k of Object.keys(STR.en)) assert.equal(placeholders(STR.hi[k]), placeholders(STR.en[k]), `placeholders differ for ${k}`);
});

test("Hindi strings are not just copies of English (except brand/technical text)", () => {
  const allowed = new Set(["brand.tag"]);
  for (const k of Object.keys(STR.en)) if (!allowed.has(k)) assert.notEqual(STR.hi[k], STR.en[k], `${k} looks untranslated`);
});

test("every category the classifier can return has a label", () => {
  for (const c of ["fake_kyc_update", "upi_refund_fraud", "lottery_scam", "fake_bank_officer", "relative_impersonation", "fake_authority", "other_scam"]) {
    assert.ok(STR.en[`cat.${c}`] && STR.hi[`cat.${c}`], `missing category label ${c}`);
  }
});
