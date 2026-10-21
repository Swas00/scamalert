import { useI18n } from "../lib/i18n.jsx";

export default function Header() {
  const { lang, setLang, t } = useI18n();
  return (
    <header className="flex items-center justify-between gap-4 border-b border-rule pb-4">
      <a href="/" className="flex items-center gap-2.5 no-underline" aria-label="ScamAlert">
        <svg width="22" height="22" viewBox="0 0 32 32" aria-hidden="true" className="translate-y-[1px]">
          <g fill="none" stroke="var(--ink)" strokeWidth="2.6" strokeLinecap="round">
            <path d="M5 16h2M11 11v10M16 6v20M21 12v8M27 16h0" />
          </g>
          <circle cx="27" cy="7" r="3.2" fill="var(--danger)" />
        </svg>
        <span className="display text-[1.375rem]">ScamAlert</span>
      </a>
      <div className="flex items-center gap-5">
        <p className="label hidden md:block">{t("brand.tag")}</p>
        <div role="group" aria-label={t("lang.toggle")} className="flex items-center rounded-[3px] border border-ink text-[0.8125rem]">
          {[["en", "EN"], ["hi", "हिंदी"]].map(([code, label]) => (
            <button key={code} type="button" lang={code} aria-pressed={lang === code} onClick={() => setLang(code)}
              className="lang-btn min-h-[34px] min-w-[44px] px-3 font-medium">
              {label}
            </button>
          ))}
        </div>
      </div>
    </header>
  );
}
