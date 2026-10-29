import { useState } from "react";
import { segments } from "../lib/highlight.js";
import { levelOf } from "../lib/samples.js";
import { useCountUp } from "../lib/hooks.js";
import { saveResultCard } from "../lib/shareCard.js";
import { langOf } from "../lib/script.js";
import { useI18n } from "../lib/i18n.jsx";
import AudioPlayer from "./AudioPlayer.jsx";

function Measure({ score, level, t }) {
  return (
    <div className="mt-5">
      <div className="relative h-[6px] rounded-full bg-[color-mix(in_srgb,var(--ink)_10%,transparent)]" role="meter"
        aria-valuemin={0} aria-valuemax={100} aria-valuenow={score} aria-label={t("meter.aria")}>
        <div className="measure-fill absolute inset-y-0 left-0 rounded-full" style={{ width: `${score}%`, background: level.bar }} />
        {[30, 70].map((p) => <span key={p} className="absolute -top-1 h-[14px] w-px bg-ink-2/50" style={{ left: `${p}%` }} aria-hidden="true" />)}
      </div>
      <div className="label mt-2 grid grid-cols-[auto_1fr_auto] gap-x-2 text-[0.6875rem] tracking-[0.04em] sm:text-xs sm:tracking-[0.08em]" aria-hidden="true">
        <span>{t("meter.safe")}</span><span className="text-center">{t("meter.mid")}</span><span className="text-right">{t("meter.high")}</span>
      </div>
    </div>
  );
}

function TranscriptOnly({ result, t }) {
  return (
    <div aria-live="polite" className="space-y-10">
      <section className="reveal border-l-2 border-warn pl-4" style={{ "--i": 0 }} aria-label={t("unsupported.title")}>
        <h2 className="display text-[1.5rem] text-warn">{t("unsupported.title")}</h2>
        <p className="mt-2 max-w-[60ch] text-[0.9375rem] text-ink-2">{t("unsupported.body")}</p>
      </section>
      <section className="reveal" style={{ "--i": 1 }} aria-label={t("transcript")}>
        <p className="label mb-3">{t("transcript")}</p>
        <p className="transcript max-w-[62ch] border-l-2 border-rule pl-5" lang={langOf(result.transcript)}>{result.transcript || t("transcript.none")}</p>
      </section>
    </div>
  );
}

export default function Report({ result, synthetic = false }) {
  const { t, lang } = useI18n();
  const [saving, setSaving] = useState("idle"); // idle | busy | done | error
  const shown = useCountUp(result.riskScore, true); // hooks first: the early return below must come after all of them
  if (result.detection === "none") return <TranscriptOnly result={result} t={t} />;
  const level = levelOf(result.riskScore);
  const flags = result.riskScore >= 30 ? result.flaggedPhrases || [] : [];
  const parts = segments(result.transcript || "", flags);
  const category = result.category ? t(`cat.${result.category}`) : null;
  let hitIndex = 0;

  async function save() {
    setSaving("busy");
    try { await saveResultCard(result, { synthetic, t, category, levelKey: level.key }); setSaving("done"); }
    catch { setSaving("error"); }
    setTimeout(() => setSaving("idle"), 2500);
  }

  return (
    <div aria-live="polite" className="space-y-10">
      <section className="reveal" style={{ "--i": 0 }} aria-label={t("verdict")}>
        <p className="label">{t("verdict")}</p>
        <div className="mt-2 flex flex-wrap items-end justify-between gap-x-8 gap-y-2">
          <div>
            <h2 className={`display glow text-[clamp(2.25rem,6vw,3.5rem)] ${level.cls}`}>{t(`level.${level.key}`)}</h2>
            {category && <p className="mt-1 text-[1.0625rem] text-ink-2">{t("looks.like")} <strong className="font-semibold text-ink">{category}</strong></p>}
          </div>
          <p className="display text-[clamp(4rem,11vw,7.5rem)] leading-[0.85] tabular-nums" aria-label={t("score.aria", { n: result.riskScore })}>
            {shown}<span className="ml-1 text-[0.28em] font-normal text-muted">/100</span>
          </p>
        </div>
        <Measure score={result.riskScore} level={level} t={t} />
        {result.detection === "beta" && (
          <p className="mt-5 max-w-[60ch] border-l-2 border-warn pl-3 text-[0.875rem] text-ink-2" data-testid="beta-note">{t("beta.note")}</p>
        )}
      </section>

      {result.explanation && (
        <section className="reveal" style={{ "--i": 1 }}>
          <p className="label mb-2">{t("why")}</p>
          <p className="max-w-[60ch] text-[1.0625rem] leading-relaxed">{result.explanation}</p>
        </section>
      )}

      <section className="reveal" style={{ "--i": 2 }} aria-label={t("transcript")}>
        <p className="label mb-3">{t("transcript")}{flags.length > 0 && <span className="normal-case tracking-normal">{t("transcript.marked")}</span>}</p>
        <p className="transcript max-w-[62ch] border-l-2 border-rule pl-5" lang={langOf(result.transcript)}>
          {result.transcript
            ? parts.map((p, i) => p.hit
              ? <mark key={i} className="hit" style={{ "--mark": level.mark, "--n": hitIndex++ }}>{p.text}</mark>
              : <span key={i}>{p.text}</span>)
            : t("transcript.none")}
        </p>
      </section>

      {result.warningAudio && (
        <section className="reveal no-print" style={{ "--i": 3 }} aria-label={t("warn.title")}>
          <p className="label mb-2">{t("warn.title")} <span className="normal-case tracking-normal">{t("warn.by")}</span></p>
          <AudioPlayer src={result.warningAudio} label={t("warn.label")} />
        </section>
      )}

      {result.riskScore >= 30 && (
        <section className="reveal border-t border-rule pt-6" style={{ "--i": 4 }} aria-label={t("todo.title")}>
          <p className="label mb-3">{t("todo.title")}</p>
          <ol className="max-w-[60ch] space-y-2 text-[0.9375rem] text-ink-2">
            {[
              t("todo.1"),
              t("todo.2"),
              <>{t("todo.3a")}<strong className="text-ink">1930</strong>{t("todo.3b")}<a className="link-quiet" href="https://cybercrime.gov.in" target="_blank" rel="noreferrer">cybercrime.gov.in</a>{lang === "en" ? "." : "।"}</>,
            ].map((item, i) => (
              <li key={i} className="grid grid-cols-[1.5rem_1fr]"><span className="label pt-[3px]">{i + 1}.</span><span>{item}</span></li>
            ))}
          </ol>
        </section>
      )}

      {result.riskScore < 30 && (
        <section className="reveal border-t border-rule pt-6" style={{ "--i": 3 }} aria-label={t("safe.note").slice(0, 20)}>
          <p className="max-w-[60ch] text-[0.9375rem] text-ink-2">{t("safe.note")}</p>
        </section>
      )}

      <div className="no-print flex flex-wrap items-center gap-x-4 gap-y-2 border-t border-rule pt-6">
        <button type="button" className="btn btn-ghost" onClick={save} disabled={saving === "busy"}>
          {saving === "busy" ? t("save.busy") : t("save")}
        </button>
        <span className="text-[0.8125rem] text-muted" role="status">
          {saving === "done" ? t("save.done") : saving === "error" ? t("save.err") : t("save.hint")}
        </span>
      </div>

      <p className="label border-t border-rule pt-4 normal-case tracking-normal">
        {t("foot.report", { who: t(result.reasoner === "claude+rules" ? "who.llm" : "who.rules") })}
      </p>
    </div>
  );
}
