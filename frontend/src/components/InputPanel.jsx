import { useEffect, useRef, useState } from "react";
import Waveform from "./Waveform.jsx";
import { toWav } from "../wav.js";
import { LANGS, MAX_SECONDS, SAMPLES } from "../lib/samples.js";
import { useAudioPeaks, useElapsed } from "../lib/hooks.js";

const fmt = (s) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;

export default function InputPanel({ file, setFile, sample, setSample, lang, setLang, onAnalyze, loading, setError }) {
  const [recording, setRecording] = useState(false);
  const [drag, setDrag] = useState(false);
  const recorder = useRef(null);
  const chunks = useRef([]);
  const recSeconds = useElapsed(recording);
  const { peaks, duration, error: decodeError } = useAudioPeaks(file);
  const tooLong = duration > MAX_SECONDS + 0.5;

  useEffect(() => { if (recording && recSeconds >= MAX_SECONDS) recorder.current?.stop(); }, [recording, recSeconds]);
  useEffect(() => () => recorder.current?.state === "recording" && recorder.current.stop(), []);

  function choose(f) {
    if (!f) return;
    setError(""); setSample(null); setFile(f);
  }

  async function toggleRecord() {
    if (recording) { recorder.current.stop(); return; }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const rec = new MediaRecorder(stream);
      chunks.current = [];
      rec.ondataavailable = (e) => chunks.current.push(e.data);
      rec.onstop = async () => {
        stream.getTracks().forEach((t) => t.stop());
        setRecording(false);
        try { choose(await toWav(new Blob(chunks.current, { type: rec.mimeType }))); }
        catch { setError("Could not process the recording. Try uploading a file instead."); }
      };
      rec.start();
      recorder.current = rec;
      setError(""); setRecording(true);
    } catch {
      setError("Microphone access was blocked. Allow it in your browser, or upload a file instead.");
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
      setError("Could not load the sample call.");
    }
  }

  const blocked = !file || tooLong || recording || loading;

  return (
    <div className="space-y-8">
      <section aria-labelledby="step1">
        <p className="label mb-3" id="step1">01 — The call</p>
        <p className="mb-4 border-l-2 border-ink pl-3 text-[0.8125rem] leading-snug text-ink-2" data-testid="data-notice">
          <strong className="font-semibold text-ink">Synthetic or test audio only.</strong> Please don’t upload real phone calls or anyone’s
          personal details — phone, bank account, Aadhaar or PAN numbers. Transcripts are not stored.
        </p>

        {!file ? (
          <label className="dropzone p-6 sm:p-7" data-drag={drag}
            onDragOver={(e) => { e.preventDefault(); setDrag(true); }} onDragLeave={() => setDrag(false)}
            onDrop={(e) => { e.preventDefault(); setDrag(false); choose(e.dataTransfer.files?.[0]); }}>
            <input type="file" accept="audio/*" className="sr-only" onChange={(e) => choose(e.target.files?.[0])} />
            <span className="display block text-[1.375rem]">Drop a recording here</span>
            <span className="mt-1 block text-[0.9375rem] text-ink-2">or <span className="link-quiet">choose a file</span> — WAV, MP3 or M4A, up to {MAX_SECONDS} seconds.</span>
          </label>
        ) : (
          <div className="border border-rule bg-surface p-4 rounded">
            <div className="flex items-baseline justify-between gap-3">
              <p className="truncate text-[0.9375rem] font-medium" title={file.name}>{file.name}</p>
              <p className="label shrink-0">{duration ? fmt(duration) : "…"}</p>
            </div>
            <div className="mt-3"><Waveform peaks={peaks} scanning={loading} /></div>
            <div className="mt-3 flex items-center justify-between">
              <p className="text-[0.8125rem] text-muted">{sample ? "Synthetic sample — not a real call" : "Your recording stays between you, this site and Gnani."}</p>
              <button type="button" className="link-quiet text-[0.8125rem] disabled:opacity-40" disabled={loading}
                onClick={() => { setFile(null); setSample(null); setError(""); }}>Remove</button>
            </div>
            {tooLong && <p role="alert" className="mt-3 text-[0.875rem] text-danger">This clip is {fmt(duration)} long. Gnani Prisma accepts up to {MAX_SECONDS} seconds — trim it and try again.</p>}
            {decodeError && <p className="mt-3 text-[0.8125rem] text-muted">Preview unavailable for this format; analysis may still work.</p>}
          </div>
        )}

        <div className="mt-4 flex items-center gap-3">
          <button type="button" onClick={toggleRecord} disabled={loading}
            className={`btn ${recording ? "btn-record-live" : "btn-ghost"}`} aria-pressed={recording}>
            {recording ? (<><span className="rec-dot" aria-hidden="true" /> Stop · {fmt(recSeconds)} / {fmt(MAX_SECONDS)}</>) : "Record from microphone"}
          </button>
        </div>
      </section>

      <section aria-labelledby="samples">
        <p className="label mb-1" id="samples">Or try a sample</p>
        <p className="mb-3 text-[0.8125rem] text-muted">Synthetic calls generated with Gnani Timbre — not real calls.</p>
        <div className="flex flex-wrap gap-2" role="group" aria-labelledby="samples">
          {SAMPLES.map((s) => (
            <button key={s.file} type="button" className="chip" aria-pressed={sample === s.file} disabled={loading} onClick={() => loadSample(s)}>
              {s.label}
            </button>
          ))}
        </div>
      </section>

      <section aria-labelledby="step2">
        <label className="label mb-3 block" id="step2" htmlFor="lang">02 — Language spoken</label>
        <div className="relative">
          <select id="lang" value={lang} onChange={(e) => setLang(e.target.value)} disabled={loading}
            className="w-full appearance-none rounded-[3px] border border-ink bg-transparent py-3 pl-3.5 pr-10 text-[0.9375rem] text-ink">
            {LANGS.map(([c, n]) => <option key={c} value={c}>{n}</option>)}
          </select>
          <svg className="pointer-events-none absolute right-3.5 top-1/2 -translate-y-1/2" width="12" height="8" viewBox="0 0 12 8" aria-hidden="true">
            <path d="M1 1.5l5 5 5-5" fill="none" stroke="var(--ink)" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
        </div>
      </section>

      <button type="button" className="btn btn-primary w-full py-[1.05rem] text-base" disabled={blocked} onClick={onAnalyze}>
        {loading ? "Listening for scam patterns…" : (<>Analyze call <span className="arrow" aria-hidden="true">→</span></>)}
      </button>
    </div>
  );
}
