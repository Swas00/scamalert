import { segments } from "../lib/highlight.js";
import { levelOf } from "../lib/samples.js";
import { useCountUp } from "../lib/hooks.js";
import AudioPlayer from "./AudioPlayer.jsx";

function Measure({ score, level }) {
  return (
    <div className="mt-5">
      <div className="relative h-[6px] bg-[color-mix(in_srgb,var(--ink)_10%,transparent)] rounded-full" role="meter"
        aria-valuemin={0} aria-valuemax={100} aria-valuenow={score} aria-label="Risk score">
        <div className="measure-fill absolute inset-y-0 left-0 rounded-full" style={{ width: `${score}%`, background: level.bar }} />
        {[30, 70].map((t) => <span key={t} className="absolute -top-1 h-[14px] w-px bg-ink-2/50" style={{ left: `${t}%` }} aria-hidden="true" />)}
      </div>
      <div className="label mt-2 flex" aria-hidden="true">
        <span style={{ width: "30%" }}>Safe</span><span style={{ width: "40%" }}>Suspicious</span><span className="flex-1 text-right">High risk</span>
      </div>
    </div>
  );
}

export default function Report({ result }) {
  const level = levelOf(result.riskScore);
  const shown = useCountUp(result.riskScore, true);
  const flags = result.riskScore >= 30 ? result.flaggedPhrases || [] : [];
  const parts = segments(result.transcript || "", flags);
  let hitIndex = 0;

  return (
    <div aria-live="polite" className="space-y-10">
      <section className="reveal" style={{ "--i": 0 }} aria-label="Verdict">
        <p className="label">Verdict</p>
        <div className="mt-2 flex flex-wrap items-end justify-between gap-x-8 gap-y-2">
          <div>
            <h2 className={`display text-[clamp(2.25rem,6vw,3.5rem)] ${level.cls}`}>{level.word}</h2>
            {result.categoryLabel && <p className="mt-1 text-[1.0625rem] text-ink-2">Looks like: <strong className="font-semibold text-ink">{result.categoryLabel}</strong></p>}
          </div>
          <p className="display text-[clamp(4rem,11vw,7.5rem)] leading-[0.85] tabular-nums" aria-label={`Risk score ${result.riskScore} out of 100`}>
            {shown}<span className="ml-1 text-[0.28em] font-normal text-muted">/100</span>
          </p>
        </div>
        <Measure score={result.riskScore} level={level} />
      </section>

      {result.explanation && (
        <section className="reveal" style={{ "--i": 1 }}>
          <p className="label mb-2">Why</p>
          <p className="max-w-[60ch] text-[1.0625rem] leading-relaxed">{result.explanation}</p>
        </section>
      )}

      <section className="reveal" style={{ "--i": 2 }} aria-label="Transcript">
        <p className="label mb-3">Transcript{flags.length > 0 && <span className="normal-case tracking-normal"> — suspicious phrases marked</span>}</p>
        <p className="transcript max-w-[62ch] border-l-2 border-rule pl-5" lang={/[ऀ-ॿ]/.test(result.transcript) ? "hi" : "en"}>
          {result.transcript
            ? parts.map((p, i) => p.hit
              ? <mark key={i} className="hit" style={{ "--mark": level.mark, "--n": hitIndex++ }}>{p.text}</mark>
              : <span key={i}>{p.text}</span>)
            : "No speech was detected."}
        </p>
      </section>

      {result.warningAudio && (
        <section className="reveal" style={{ "--i": 3 }} aria-label="Spoken warning">
          <p className="label mb-2">Spoken warning <span className="normal-case tracking-normal">— voiced by Gnani Timbre</span></p>
          <AudioPlayer src={result.warningAudio} label="spoken warning" />
        </section>
      )}

      {result.riskScore >= 30 && (
        <section className="reveal border-t border-rule pt-6" style={{ "--i": 4 }} aria-label="What to do now">
          <p className="label mb-3">If this was a real call</p>
          <ol className="max-w-[60ch] space-y-2 text-[0.9375rem] text-ink-2 [counter-reset:n]">
            {[
              "Hang up. Don’t call back on a number the caller gave you.",
              "Never share an OTP, PIN, CVV or card number — a real bank will not ask for them.",
              <>Already lost money? Call <strong className="text-ink">1930</strong>, the National Cyber Crime Helpline, or report at <a className="link-quiet" href="https://cybercrime.gov.in" target="_blank" rel="noreferrer">cybercrime.gov.in</a>.</>,
            ].map((t, i) => (
              <li key={i} className="grid grid-cols-[1.5rem_1fr]"><span className="label pt-[3px]">{i + 1}.</span><span>{t}</span></li>
            ))}
          </ol>
        </section>
      )}

      {result.riskScore < 30 && (
        <section className="reveal border-t border-rule pt-6" style={{ "--i": 3 }} aria-label="Staying safe">
          <p className="max-w-[60ch] text-[0.9375rem] text-ink-2">
            Nothing in this call matched the scam patterns ScamAlert knows. That isn’t a guarantee — whatever the caller says, a real bank will never ask for your OTP, PIN or CVV.
          </p>
        </section>
      )}

      <p className="label border-t border-rule pt-4 normal-case tracking-normal">
        Transcribed by Gnani Prisma · analysed by {result.reasoner === "claude+rules" ? "Claude and a rule engine" : "a rule engine"} · results are an aid, not a guarantee.
      </p>
    </div>
  );
}
