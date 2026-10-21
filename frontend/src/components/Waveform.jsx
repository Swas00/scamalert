import { useEffect, useRef, useState } from "react";
import { useI18n } from "../lib/i18n.jsx";

/**
 * The call's waveform. While `scanning` a scan line sweeps across it; while playing, `progress` (0-1) shows a playhead.
 * `onSeek(fraction)` makes the bars clickable; a visually hidden range input gives keyboard users the same control.
 */
export default function Waveform({ peaks, scanning, progress = 0, onSeek }) {
  const { t } = useI18n();
  const box = useRef(null);
  const [w, setW] = useState(0);
  useEffect(() => {
    if (!box.current) return;
    const ro = new ResizeObserver(([e]) => setW(e.contentRect.width));
    ro.observe(box.current);
    return () => ro.disconnect();
  }, []);

  const H = 56;
  const seekable = !!(onSeek && peaks);
  const showHead = !scanning && progress > 0 && progress < 1;
  return (
    <div ref={box} className={`relative h-14 w-full overflow-hidden ${seekable ? "cursor-pointer" : ""}`}
      style={{ "--scan-w": `${Math.max(0, w - 2)}px` }}
      role="img" aria-label={peaks ? t("wave.alt") : t("wave.none")}
      onClick={seekable ? (e) => { const r = e.currentTarget.getBoundingClientRect(); onSeek(Math.min(1, Math.max(0, (e.clientX - r.left) / r.width))); } : undefined}>
      {peaks ? (
        <svg width="100%" height={H} viewBox={`0 0 ${peaks.length * 4} ${H}`} preserveAspectRatio="none" aria-hidden="true">
          {peaks.map((p, i) => {
            const h = Math.max(2, p * (H - 6));
            const played = i / peaks.length < progress;
            return <rect key={i} x={i * 4 + 0.5} y={(H - h) / 2} width="2.2" height={h} rx="1"
              fill={played ? "var(--ink)" : "var(--ink-2)"} opacity={played ? 1 : scanning ? 0.9 : 0.6} />;
          })}
        </svg>
      ) : (
        <div className="h-full border-y border-dashed border-rule" />
      )}
      {scanning && <div className="scanline" aria-hidden="true" />}
      {showHead && <div className="playhead" style={{ left: `${progress * 100}%` }} aria-hidden="true" />}
      {seekable && (
        <input type="range" className="sr-only" min={0} max={100} step={1} value={Math.round(progress * 100)} aria-label={t("player.seek")}
          onChange={(e) => onSeek(Number(e.target.value) / 100)} />
      )}
    </div>
  );
}
