import { useEffect, useRef, useState } from "react";

/** The call's waveform. While `scanning`, a scan line sweeps across it. */
export default function Waveform({ peaks, scanning }) {
  const box = useRef(null);
  const [w, setW] = useState(0);
  useEffect(() => {
    if (!box.current) return;
    const ro = new ResizeObserver(([e]) => setW(e.contentRect.width));
    ro.observe(box.current);
    return () => ro.disconnect();
  }, []);

  const H = 56;
  return (
    <div ref={box} className="relative h-14 w-full overflow-hidden" style={{ "--scan-w": `${Math.max(0, w - 2)}px` }}
      role="img" aria-label={peaks ? "Waveform of the selected call" : "Waveform unavailable"}>
      {peaks ? (
        <svg width="100%" height={H} viewBox={`0 0 ${peaks.length * 4} ${H}`} preserveAspectRatio="none" aria-hidden="true">
          {peaks.map((p, i) => {
            const h = Math.max(2, p * (H - 6));
            return <rect key={i} x={i * 4 + 0.5} y={(H - h) / 2} width="2.2" height={h} rx="1" fill="var(--ink-2)" opacity={scanning ? 0.9 : 0.75} />;
          })}
        </svg>
      ) : (
        <div className="h-full border-y border-dashed border-rule" />
      )}
      {scanning && <div className="scanline" aria-hidden="true" />}
    </div>
  );
}
