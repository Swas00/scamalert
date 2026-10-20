export default function Header() {
  return (
    <header className="flex items-baseline justify-between gap-4 border-b border-rule pb-4">
      <a href="/" className="flex items-center gap-2.5 no-underline" aria-label="ScamAlert home">
        <svg width="22" height="22" viewBox="0 0 32 32" aria-hidden="true" className="translate-y-[3px]">
          <g fill="none" stroke="var(--ink)" strokeWidth="2.6" strokeLinecap="round">
            <path d="M5 16h2M11 11v10M16 6v20M21 12v8M27 16h0" />
          </g>
          <circle cx="27" cy="7" r="3.2" fill="var(--danger)" />
        </svg>
        <span className="display text-[1.375rem]">ScamAlert</span>
      </a>
      <p className="label hidden sm:block">Gnani Prisma STT · Gnani Timbre TTS</p>
    </header>
  );
}
