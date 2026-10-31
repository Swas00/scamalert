import { useCallback, useEffect, useRef, useState } from "react";
import Header from "./components/Header.jsx";
import InputPanel from "./components/InputPanel.jsx";
import Report from "./components/Report.jsx";
import EmptyReport from "./components/EmptyReport.jsx";
import Skeleton from "./components/Skeleton.jsx";
import { useElapsed } from "./lib/hooks.js";
import { useI18n } from "./lib/i18n.jsx";
import { detectionFor } from "./lib/samples.js";
import DataRain from "@/components/ui/data-rain";

// Local dev: empty, so requests go to the Vite proxy (/api). Production builds default to the deployed backend; set VITE_API_URL to override it.
const DEFAULT_API = "https://scamalert-1-backend.onrender.com";
const API = (import.meta.env.VITE_API_URL || (import.meta.env.PROD ? DEFAULT_API : "")).replace(/\/+$/, "");

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

  // Probe the backend. This doubles as the wake-up ping for free hosting that sleeps when idle (so the backend and the classifier
  // behind it are awake by the time someone analyzes). A slow answer is a cold start, not an outage; only a refusal or error counts as offline.
  const [serviceDown, setServiceDown] = useState(false);
  const checkService = useCallback(async () => {
    // "Up" means a genuine JSON answer {"status":"ok"} - not merely an HTTP 200, which a misconfigured address or a catch-all page can also return.
    const probe = fetch(`${API}/api/health`).then(
      async (r) => { try { return r.ok && (await r.json())?.status === "ok" ? "up" : "down"; } catch { return "down"; } },
      () => "down",
    );
    const outcome = await Promise.race([probe, new Promise((resolve) => setTimeout(() => resolve("slow"), 20000))]);
    if (outcome === "slow") probe.then((o) => setServiceDown(o === "down")); // settle whenever it finally answers
    else setServiceDown(outcome === "down");
  }, []);
  useEffect(() => {
    checkService();
    window.addEventListener("focus", checkService);
    return () => window.removeEventListener("focus", checkService);
  }, [checkService]);

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
      setServiceDown(false);
    } catch (e) {
      if (e instanceof TypeError) setServiceDown(true);
      setError(e instanceof TypeError ? "err.net" : e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
    <DataRain />
    <div className="relative z-10 mx-auto max-w-[70rem] px-4 pb-16 pt-6 sm:px-8 sm:pt-8">
      <a href="#results" className="skip-link">{t("skip")}</a>
      <Header />

      {serviceDown && (
        <div role="status" className="panel mt-6 flex flex-wrap items-center justify-between gap-x-6 gap-y-3 border-l-2 !border-l-warn">
          <div className="min-w-0">
            <p className="font-medium text-warn">{t("offline.title")}</p>
            <p className="mt-1 max-w-[60ch] text-[0.9375rem] text-ink-2">{t("offline.body")}</p>
          </div>
          <button type="button" className="btn btn-ghost" onClick={checkService}>{t("offline.retry")}</button>
        </div>
      )}

      <main className="mt-10 grid gap-x-10 gap-y-10 lg:grid-cols-12 lg:mt-14">
        <div className="min-w-0 lg:col-span-5">
          <h1 className="display text-[clamp(2.25rem,5.2vw,3.25rem)]">{t("h1.a")}<br />{t("h1.b")}</h1>
          <p className="mb-8 mt-4 max-w-[40ch] text-[1.0625rem] text-ink-2">{t("intro")}</p>
          <div className="panel">
            <InputPanel {...{ file, setFile, sample, setSample, lang, setLang, loading, setError }} onAnalyze={analyze} />
          </div>
        </div>

        <section id="results" tabIndex={-1} ref={reportRef} className="panel min-w-0 scroll-mt-4 lg:col-span-7" aria-busy={loading} aria-label={t("results.label")}>
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
        </section>
      </main>

      <footer className="mt-20 border-t border-rule pt-5 text-[0.8125rem] text-muted">
        {t("foot.page")}
      </footer>
    </div>
    </>
  );
}
