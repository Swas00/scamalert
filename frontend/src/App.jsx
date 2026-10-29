import { useEffect, useRef, useState } from "react";
import Header from "./components/Header.jsx";
import InputPanel from "./components/InputPanel.jsx";
import Report from "./components/Report.jsx";
import EmptyReport from "./components/EmptyReport.jsx";
import Skeleton from "./components/Skeleton.jsx";
import { useElapsed } from "./lib/hooks.js";
import { useI18n } from "./lib/i18n.jsx";
import { detectionFor } from "./lib/samples.js";
import DataRain from "@/components/ui/data-rain";

// Empty in local dev (Vite proxies /api); set VITE_API_URL to the deployed backend in production.
const API = import.meta.env.VITE_API_URL || "";

export default function App() {
  const { t } = useI18n();
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
      if (!res.ok) throw new Error(res.status === 429 ? "err.limit" : "err.generic");
      setResult({ ...data, synthetic: !!sample, detection: detectionFor(lang) });
    } catch (e) {
      setError(e instanceof TypeError ? "err.net" : e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
    <DataRain />
    <div className="relative z-10 mx-auto max-w-[1120px] px-4 pb-16 pt-6 sm:px-8 sm:pt-8">
      <a href="#results" className="skip-link">{t("skip")}</a>
      <Header />

      <div className="mt-10 grid gap-x-10 gap-y-10 lg:grid-cols-12 lg:mt-14">
        <div className="min-w-0 lg:col-span-5">
          <h1 className="display text-[clamp(2.25rem,5.2vw,3.25rem)]">{t("h1.a")}<br />{t("h1.b")}</h1>
          <p className="mb-8 mt-4 max-w-[40ch] text-[1.0625rem] text-ink-2">{t("intro")}</p>
          <div className="panel lg:sticky lg:top-8">
            <InputPanel {...{ file, setFile, sample, setSample, lang, setLang, loading, setError }} onAnalyze={analyze} />
          </div>
        </div>

        <main id="results" tabIndex={-1} ref={reportRef} className="panel min-w-0 scroll-mt-4 lg:col-span-7" aria-busy={loading}>
          {error && (
            <div role="alert" className="reveal mb-8 border-l-2 border-danger pl-4 text-[0.9375rem]">
              <p className="font-medium text-danger">{t("err.title")}</p>
              <p className="mt-1 text-ink-2">{t(error)}</p>
            </div>
          )}
          {loading && (
            <div className="reveal mb-8" role="status">
              <p className="display text-[1.375rem]">{t("loading.title")}</p>
              <p className="mt-1 max-w-[50ch] text-[0.9375rem] text-ink-2">
                {waited >= 8 ? t("loading.wake") : t("loading.body")}
              </p>
            </div>
          )}
          {loading ? <Skeleton /> : result ? <Report result={result} synthetic={result.synthetic} /> : !error && <EmptyReport />}
        </main>
      </div>

      <footer className="mt-20 border-t border-rule pt-5 text-[0.8125rem] text-muted">
        {t("foot.page")}
      </footer>
    </div>
    </>
  );
}
