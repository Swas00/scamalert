import { useEffect, useMemo, useRef, useState } from "react";
import Waveform from "./Waveform.jsx";
import { toWav } from "../wav.js";
import { LANG_CODES, MAX_SECONDS, SAMPLES } from "../lib/samples.js";
import { useAudioPeaks, useElapsed } from "../lib/hooks.js";
import { useI18n } from "../lib/i18n.jsx";

const fmt = (s) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;

export default function InputPanel({ file, setFile, sample, setSample, lang, setLang, onAnalyze, loading, setError }) {
  const { t } = useI18n();
  const [recording, setRecording] = useState(false);
  const [drag, setDrag] = useState(false);
  const [playing, setPlaying] = useState(false);
  const [progress, setProgress] = useState(0);
  const recorder = useRef(null);
  const chunks = useRef([]);
  const audioEl = useRef(null);
  const recSeconds = useElapsed(recording);
  const { peaks, duration, error: decodeError } = useAudioPeaks(file);
  const tooLong = duration > MAX_SECONDS + 0.5;

  // Object URL for playing the selected call back; revoked when the file changes.
  const url = useMemo(() => (file ? URL.createObjectURL(file) : null), [file]);
  useEffect(() => () => { if (url) URL.revokeObjectURL(url); }, [url]);
  useEffect(() => { setPlaying(false); setProgress(0); }, [url]);
  useEffect(() => { if (loading) audioEl.current?.pause(); }, [loading]); // listening to the original isn't needed during analysis

  // Smooth playhead: follow currentTime on animation frames while playing.
  useEffect(() => {
    if (!playing) return;
    let raf;
    const tick = () => {
      const a = audioEl.current;
      if (a && a.duration) setProgress(a.currentTime / a.duration);
      raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [playing]);

  useEffect(() => { if (recording && recSeconds >= MAX_SECONDS) recorder.current?.stop(); }, [recording, recSeconds]);
  useEffect(() => () => recorder.current?.state === "recording" && recorder.current.stop(), []);

  function choose(f) {
    if (!f) return;
    setError(""); setSample(null); setFile(f);
  }

  function togglePlay() {
    const a = audioEl.current;
    if (!a) return;
    if (a.paused) a.play().catch(() => {}); else a.pause();
  }

  function seek(fraction) {
    const a = audioEl.current;
    if (!a || !a.duration) return;
    a.currentTime = fraction * a.duration;
    setProgress(fraction);
  }

  async function toggleRecord() {
    if (recording) { recorder.current.stop(); return; }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const rec = new MediaRecorder(stream);
      chunks.current = [];
      rec.ondataavailable = (e) => chunks.current.push(e.data);
      rec.onstop = async () => {
        stream.getTracks().forEach((tr) => tr.stop());
        setRecording(false);
        try { choose(await toWav(new Blob(chunks.current, { type: rec.mimeType }))); }
        catch { setError("err.rec"); }
      };
      rec.start();
      recorder.current = rec;
      setError(""); setRecording(true);
    } catch {
      setError("err.mic");
    }
  }

  async function loadSample(s) {
    setError("");
    try {
      const res = await fetch(`/samples/${s.file}`);
      if (!res.ok) throw new Error();
      setFile(new File([await res.blob()], s.file, { type: "audio/wav" }));
      setSample(s.file); setLang(s.lang);
    } catch {
      setError("err.sample");
    }
  }

  const blocked = !file || tooLong || recording || loading;

  return (
    <div className="space-y-8">
      <section aria-labelledby="step1">
        <p className="label mb-3" id="step1">{t("step1")}</p>
        <p className="mb-4 border-l-2 border-ink pl-3 text-[0.8125rem] leading-snug text-ink-2" data-testid="data-notice">
          <strong className="font-semibold text-ink">{t("notice.strong")}</strong>{t("notice.body")}
        </p>

        {!file ? (
          <label className="dropzone p-6 sm:p-7" data-drag={drag}
            onDragOver={(e) => { e.preventDefault(); setDrag(true); }} onDragLeave={() => setDrag(false)}
            onDrop={(e) => { e.preventDefault(); setDrag(false); choose(e.dataTransfer.files?.[0]); }}>
            <input type="file" accept="audio/*" className="sr-only" onChange={(e) => choose(e.target.files?.[0])} />
            <span className="display block text-[1.375rem]">{t("drop.title")}</span>
            <span className="mt-1 block text-[0.9375rem] text-ink-2">{t("drop.or")}<span className="link-quiet">{t("drop.choose")}</span>{t("drop.rest", { max: MAX_SECONDS })}</span>
          </label>
        ) : (
          <div className="rounded border border-rule bg-surface p-4">
            <audio ref={audioEl} src={url} preload="auto" onPlay={() => setPlaying(true)} onPause={() => setPlaying(false)}
              onEnded={() => { setPlaying(false); setProgress(0); }} />
            <div className="flex items-baseline justify-between gap-3">
              <p className="truncate text-[0.9375rem] font-medium" title={file.name}>{file.name}</p>
              <p className="label shrink-0">{duration ? fmt(duration) : "…"}</p>
            </div>
            <div className="mt-3"><Waveform peaks={peaks} scanning={loading} progress={progress} onSeek={loading ? undefined : seek} /></div>
            <div className="mt-3 flex items-center justify-between gap-3">
              <button type="button" className="btn btn-ghost !px-3 !py-2 text-[0.8125rem]" onClick={togglePlay} disabled={loading || !peaks}>
                {playing
                  ? <svg width="10" height="10" viewBox="0 0 12 12" aria-hidden="true"><path d="M2 1h3v10H2zM7 1h3v10H7z" fill="currentColor" /></svg>
                  : <svg width="10" height="10" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 1l8 5-8 5z" fill="currentColor" /></svg>}
                {playing ? t("pause") : t("play")}
              </button>
              <button type="button" className="link-quiet text-[0.8125rem] disabled:opacity-40" disabled={loading}
                onClick={() => { audioEl.current?.pause(); setFile(null); setSample(null); setError(""); }}>{t("file.remove")}</button>
            </div>
            <p className="mt-2 text-[0.8125rem] text-muted">{sample ? t("file.sample") : t("file.upload")}</p>
            {tooLong && <p role="alert" className="mt-3 text-[0.875rem] text-danger">{t("file.tooLong", { d: fmt(duration), max: MAX_SECONDS })}</p>}
            {decodeError && <p className="mt-3 text-[0.8125rem] text-muted">{t("file.noPreview")}</p>}
          </div>
        )}

        <div className="mt-4 flex items-center gap-3">
          <button type="button" onClick={toggleRecord} disabled={loading}
            className={`btn ${recording ? "btn-record-live" : "btn-ghost"}`} aria-pressed={recording}>
            {recording ? (<><span className="rec-dot" aria-hidden="true" /> {t("rec.stop", { t: fmt(recSeconds), max: fmt(MAX_SECONDS) })}</>) : t("rec.start")}
          </button>
        </div>
      </section>

      <section aria-labelledby="samples">
        <p className="label mb-1" id="samples">{t("samples.label")}</p>
        <p className="mb-3 text-[0.8125rem] text-muted">{t("samples.help")}</p>
        <div className="flex flex-wrap gap-2" role="group" aria-labelledby="samples">
          {SAMPLES.map((s) => (
            <button key={s.file} type="button" className="chip" aria-pressed={sample === s.file} disabled={loading} onClick={() => loadSample(s)}>
              {t(s.labelKey)}
            </button>
          ))}
        </div>
      </section>

      <section aria-labelledby="step2">
        <label className="label mb-3 block" id="step2" htmlFor="lang">{t("step2")}</label>
        <div className="relative">
          <select id="lang" value={lang} onChange={(e) => setLang(e.target.value)} disabled={loading}
            className="w-full appearance-none rounded-lg border border-[rgba(150,180,220,0.34)] bg-[rgba(255,255,255,0.03)] py-3 pl-3.5 pr-10 text-[0.9375rem] text-ink transition-colors hover:border-accent">
            {LANG_CODES.map((c) => <option key={c} value={c}>{t(`lang.${c}`)}</option>)}
          </select>
          <svg className="pointer-events-none absolute right-3.5 top-1/2 -translate-y-1/2" width="12" height="8" viewBox="0 0 12 8" aria-hidden="true">
            <path d="M1 1.5l5 5 5-5" fill="none" stroke="var(--accent)" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
      </section>

      <button type="button" className="btn btn-primary w-full py-[1.05rem] text-base" disabled={blocked} onClick={onAnalyze}>
        {loading ? t("analyze.busy") : (<>{t("analyze")} <span className="arrow" aria-hidden="true">→</span></>)}
      </button>
    </div>
  );
}
