import { createContext, createElement, useContext, useEffect, useMemo, useState } from "react";
import { STR } from "./strings.js";

const fmt = (s, p) => (p ? s.replace(/\{(\w+)\}/g, (_, k) => (k in p ? p[k] : `{${k}}`)) : s);

function initialLang() {
  try { const s = localStorage.getItem("scamalert-lang"); if (s === "en" || s === "hi") return s; } catch { /* storage unavailable */ }
  return navigator.language?.toLowerCase().startsWith("hi") ? "hi" : "en";
}

const Ctx = createContext(null);

export function I18nProvider({ children }) {
  const [lang, setLang] = useState(initialLang);
  useEffect(() => {
    document.documentElement.lang = lang;
    try { localStorage.setItem("scamalert-lang", lang); } catch { /* storage unavailable */ }
  }, [lang]);
  const value = useMemo(() => ({ lang, setLang, t: (k, p) => fmt(STR[lang][k] ?? STR.en[k] ?? k, p) }), [lang]);
  return createElement(Ctx.Provider, { value }, children);
}

export const useI18n = () => useContext(Ctx);
