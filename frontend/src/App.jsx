import { useRef, useState } from "react";
import { toWav } from "./wav.js";

const LANGS = [["en-IN", "English"], ["hi-IN", "Hindi"], ["ta-IN", "Tamil"], ["te-IN", "Telugu"],
  ["kn-IN", "Kannada"], ["ml-IN", "Malayalam"], ["mr-IN", "Marathi"], ["bn-IN", "Bengali"],
  ["gu-IN", "Gujarati"], ["pa-IN", "Punjabi"]];

function riskStyle(score) {
  if (score >= 70) return { label: "High risk", cls: "bg-red-50 text-red-700 border-red-200" };
  if (score >= 30) return { label: "Suspicious", cls: "bg-amber-50 text-amber-700 border-amber-200" };
  return { label: "Looks safe", cls: "bg-green-50 text-green-700 border-green-200" };
}

function Highlighted({ text, phrases }) {
  if (!phrases?.length) return <>{text}</>;
  const esc = phrases.map((p) => p.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  const parts = text.split(new RegExp(`(${esc.join("|")})`, "gi"));
  return parts.map((part, i) =>
    phrases.some((p) => p.toLowerCase() === part.toLowerCase())
      ? <mark key={i} className="bg-red-100 text-red-800 rounded px-0.5">{part}</mark>
      : part
  );
}

export default function App() {
  const [file, setFile] = useState(null);
  const [lang, setLang] = useState("en-IN");
  const [recording, setRecording] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const recorder = useRef(null);
  const chunks = useRef([]);

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
        try {
          setFile(await toWav(new Blob(chunks.current, { type: rec.mimeType })));
        } catch {
          setError("Could not process the recording.");
        }
      };
      rec.start();
      recorder.current = rec;
      setRecording(true);
    } catch {
      setError("Microphone access denied.");
    }
  }

  async function analyze() {
    setLoading(true); setError(""); setResult(null);
    const form = new FormData();
    form.append("audio", file);
    form.append("language_code", lang);
    try {
      const res = await fetch("/api/analyze", { method: "POST", body: form });
      const data = await res.json();
      if (!res.ok) throw new Error([data.error, typeof data.detail === "string" ? data.detail : JSON.stringify(data.detail)].filter(Boolean).join(": ") || "Request failed");
      setResult(data);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  const risk = result && riskStyle(result.riskScore);

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900">
      <main className="mx-auto max-w-2xl px-4 py-10 space-y-6">
        <header>
          <h1 className="text-3xl font-bold">ScamAlert</h1>
          <p className="text-slate-600">Upload or record a call. We transcribe it and check it for scam patterns.</p>
        </header>

        <section className="rounded-xl bg-white p-5 shadow-sm border border-slate-200 space-y-4">
          <div className="flex flex-wrap gap-3 items-center">
            <label className="cursor-pointer rounded-lg bg-slate-900 px-4 py-2 text-white text-sm font-medium hover:bg-slate-700">
              Upload audio
              <input type="file" accept="audio/*" hidden onChange={(e) => setFile(e.target.files[0] || null)} />
            </label>
            <button onClick={toggleRecord}
              className={`rounded-lg px-4 py-2 text-sm font-medium border ${recording ? "bg-red-600 text-white border-red-600" : "bg-white border-slate-300 hover:bg-slate-100"}`}>
              {recording ? "Stop recording" : "Record"}
            </button>
            <select value={lang} onChange={(e) => setLang(e.target.value)}
              className="rounded-lg border border-slate-300 px-3 py-2 text-sm">
              {LANGS.map(([c, n]) => <option key={c} value={c}>{n}</option>)}
            </select>
          </div>
          {file && <p className="text-sm text-slate-600">Selected: {file.name}</p>}
          <button onClick={analyze} disabled={!file || loading}
            className="w-full rounded-lg bg-indigo-600 py-2.5 text-white font-medium disabled:opacity-40">
            {loading ? "Analyzing…" : "Analyze call"}
          </button>
          {error && <p className="text-sm text-red-600">{error}</p>}
        </section>

        {result && (
          <>
            <section className={`rounded-xl border p-5 ${risk.cls}`}>
              <div className="flex items-baseline justify-between">
                <div>
                  <p className="text-sm uppercase tracking-wide opacity-70">Risk score</p>
                  <p className="text-5xl font-bold">{result.riskScore}<span className="text-xl">/100</span></p>
                </div>
                <div className="text-right">
                  <p className="font-semibold">{risk.label}</p>
                  {result.categoryLabel && <p className="text-sm">{result.categoryLabel}</p>}
                </div>
              </div>
              {result.flaggedPhrases?.length > 0 && (
                <div className="mt-4 flex flex-wrap gap-2">
                  {result.flaggedPhrases.map((p) => (
                    <span key={p} className="rounded-full bg-white/70 px-3 py-1 text-xs font-medium">{p}</span>
                  ))}
                </div>
              )}
            </section>

            <section className="rounded-xl bg-white p-5 shadow-sm border border-slate-200">
              <h2 className="font-semibold mb-2">Transcript</h2>
              <p className="whitespace-pre-wrap leading-relaxed">
                {result.transcript ? <Highlighted text={result.transcript} phrases={result.flaggedPhrases} /> : "No speech detected."}
              </p>
            </section>

            {result.warningAudio && (
              <section className="rounded-xl bg-white p-5 shadow-sm border border-slate-200">
                <h2 className="font-semibold mb-2">Spoken warning</h2>
                <audio controls src={result.warningAudio} className="w-full" />
              </section>
            )}
          </>
        )}
      </main>
    </div>
  );
}
