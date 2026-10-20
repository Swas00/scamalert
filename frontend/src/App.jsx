import { useEffect, useRef, useState } from "react";
import Header from "./components/Header.jsx";
import InputPanel from "./components/InputPanel.jsx";
import Report from "./components/Report.jsx";
import EmptyReport from "./components/EmptyReport.jsx";
import Skeleton from "./components/Skeleton.jsx";
import { useElapsed } from "./lib/hooks.js";

// Empty in local dev (Vite proxies /api); set VITE_API_URL to the deployed backend in production.
const API = import.meta.env.VITE_API_URL || "";

export default function App() {
  const [file, setFile] = useState(null);
  const [sample, setSample] = useState(null);
  const [lang, setLang] = useState("en-IN");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null);
  const waited = useElapsed(loading);
  const reportRef = useRef(null);

  // Free hosting sleeps when idle: ping the backend on load so it (and the classifier behind it) is awake by the time the user analyzes.
  useEffect(() => { fetch(`${API}/api/health`).catch(() => {}); }, []);

  // On narrow screens the report sits below the form; bring it into view when analysis starts or finishes.
  useEffect(() => {
    if (!(loading || result || error) || window.matchMedia("(min-width: 1024px)").matches) return;
    const calm = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    reportRef.current?.scrollIntoView({ behavior: calm ? "auto" : "smooth", block: "start" });
  }, [loading, result, error]);

  async function analyze() {
    setLoading(true); setError(""); setResult(null);
    const form = new FormData();
    form.append("audio", file);
    form.append("language_code", lang);
    try {
      const res = await fetch(`${API}/api/analyze`, { method: "POST", body: form });
      const data = await res.json().catch(() => ({}));
      if (!res.ok) throw new Error(res.status === 429 ? data.error || "Too many analyses right now. Please try again in a while." : data.error || "The analysis failed. Please try again.");
      setResult(data);
    } catch (e) {
      setError(e instanceof TypeError ? "Couldn’t reach the server. Check your connection and try again." : e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="mx-auto max-w-[1120px] px-4 pb-16 pt-6 sm:px-8 sm:pt-8">
      <Header />

      <div className="mt-10 grid gap-x-16 gap-y-12 lg:grid-cols-12 lg:mt-14">
        <div className="lg:col-span-5">
          <h1 className="display text-[clamp(2.25rem,5.2vw,3.25rem)]">Is this call<br />a scam?</h1>
          <p className="mb-9 mt-4 max-w-[40ch] text-[1.0625rem] text-ink-2">Upload or record a suspicious call. ScamAlert transcribes it, marks what sounds like fraud, and speaks a warning.</p>
          <div className="lg:sticky lg:top-8">
            <InputPanel {...{ file, setFile, sample, setSample, lang, setLang, loading, setError }} onAnalyze={analyze} />
          </div>
        </div>

        <main ref={reportRef} className="scroll-mt-4 lg:col-span-7 lg:border-l lg:border-rule lg:pl-16" aria-busy={loading}>
          {error && (
            <div role="alert" className="reveal mb-8 border-l-2 border-danger pl-4 text-[0.9375rem]">
              <p className="font-medium text-danger">Something went wrong</p>
              <p className="mt-1 text-ink-2">{error}</p>
            </div>
          )}
          {loading && (
            <div className="reveal mb-8" role="status">
              <p className="display text-[1.375rem]">Analyzing the call…</p>
              <p className="mt-1 max-w-[50ch] text-[0.9375rem] text-ink-2">
                {waited >= 8
                  ? "The free server is waking up after a quiet spell — the first analysis can take up to a minute."
                  : "Transcribing, reading for scam patterns, preparing the warning."}
              </p>
            </div>
          )}
          {loading ? <Skeleton /> : result ? <Report result={result} /> : !error && <EmptyReport />}
        </main>
      </div>

      <footer className="mt-20 border-t border-rule pt-5 text-[0.8125rem] text-muted">
        Built on Gnani AI’s Prisma and Timbre. Sample calls are synthetic; no real calls or personal data are used.
      </footer>
    </div>
  );
}
