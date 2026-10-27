import { useI18n } from "../lib/i18n.jsx";

const KINDS = ["kyc", "upi", "lottery", "bank", "relative", "authority"];

export default function EmptyReport() {
  const { t } = useI18n();
  return (
    <div className="space-y-12">
      <section className="reveal" style={{ "--i": 0 }}>
        <p className="label mb-4">{t("how.title")}</p>
        <ol className="space-y-6">
          {[1, 2, 3].map((n) => (
            <li key={n} className="grid grid-cols-[2.25rem_1fr] border-t border-rule pt-4">
              <span className="label pt-1">0{n}</span>
              <span><span className="display block text-[1.25rem]">{t(`how.${n}.h`)}</span><span className="mt-1 block max-w-[52ch] text-[0.9375rem] text-ink-2">{t(`how.${n}.t`)}</span></span>
            </li>
          ))}
        </ol>
      </section>
      <section className="reveal" style={{ "--i": 1 }}>
        <p className="label mb-4">{t("watch.title")}</p>
        <ul className="flex flex-wrap gap-x-7 gap-y-3 font-display text-[1.125rem]">
          {KINDS.map((k) => <li key={k} className="border-b border-rule pb-0.5">{t(`kind.${k}`)}</li>)}
        </ul>
      </section>
    </div>
  );
}
