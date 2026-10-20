const STEPS = [
  ["Transcribe", "Gnani Prisma turns the call — even noisy, phone-quality audio — into text in Hindi, English or Hinglish."],
  ["Read for patterns", "The transcript is checked for urgency, threats, and requests for OTPs, PINs or money."],
  ["Warn", "You get a risk score, the exact phrases that raised it, and a spoken warning in the caller’s language."],
];
const KINDS = ["Fake KYC update", "UPI refund fraud", "Lottery or prize scam", "Fake bank officer", "Relative in trouble"];

export default function EmptyReport() {
  return (
    <div className="space-y-12">
      <section className="reveal" style={{ "--i": 0 }}>
        <p className="label mb-4">How it reads a call</p>
        <ol className="space-y-6">
          {STEPS.map(([h, t], i) => (
            <li key={h} className="grid grid-cols-[2.25rem_1fr] border-t border-rule pt-4">
              <span className="label pt-1">0{i + 1}</span>
              <span><span className="display block text-[1.25rem]">{h}</span><span className="mt-1 block max-w-[52ch] text-[0.9375rem] text-ink-2">{t}</span></span>
            </li>
          ))}
        </ol>
      </section>
      <section className="reveal" style={{ "--i": 1 }}>
        <p className="label mb-4">What it watches for</p>
        <ul className="flex flex-wrap gap-x-7 gap-y-3 font-display text-[1.125rem]">
          {KINDS.map((k) => <li key={k} className="border-b border-rule pb-0.5">{k}</li>)}
        </ul>
      </section>
    </div>
  );
}
