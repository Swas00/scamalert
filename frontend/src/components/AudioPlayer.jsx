import { useEffect, useRef, useState } from "react";
import { useI18n } from "../lib/i18n.jsx";

const fmt = (s) => (Number.isFinite(s) ? `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}` : "0:00");

/** Minimal accessible player: a real <audio> element drives a button and a seek slider. */
export default function AudioPlayer({ src, label }) {
  const { t } = useI18n();
  const el = useRef(null);
  const [playing, setPlaying] = useState(false);
  const [time, setTime] = useState(0);
  const [dur, setDur] = useState(0);

  useEffect(() => { setPlaying(false); setTime(0); }, [src]);

  const pct = dur ? (time / dur) * 100 : 0;
  return (
    <div className="flex w-full max-w-[34rem] items-center gap-3 border-y border-rule py-3 sm:gap-4">
      <audio ref={el} src={src} preload="metadata"
        onLoadedMetadata={(e) => setDur(e.currentTarget.duration)}
        onTimeUpdate={(e) => setTime(e.currentTarget.currentTime)}
        onPlay={() => setPlaying(true)} onPause={() => setPlaying(false)} onEnded={() => setPlaying(false)} />
      <button type="button" className="btn btn-primary !h-10 !w-10 !min-h-10 !min-w-10 shrink-0 !rounded-full !p-0"
        aria-label={playing ? t("player.pause", { label }) : t("player.play", { label })}
        onClick={() => (playing ? el.current.pause() : el.current.play())}>
        {playing
          ? <svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M2 1h3v10H2zM7 1h3v10H7z" fill="currentColor" /></svg>
          : <svg width="12" height="12" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 1l8 5-8 5z" fill="currentColor" /></svg>}
      </button>
      <input type="range" className="seek min-w-0 flex-1" min={0} max={dur || 0} step="0.05" value={time} aria-label={t("player.seek")} style={{ "--p": `${pct}%` }}
        onChange={(e) => { el.current.currentTime = Number(e.target.value); setTime(Number(e.target.value)); }} />
      <span className="label shrink-0 whitespace-nowrap tabular-nums">{fmt(time)} / {fmt(dur)}</span>
    </div>
  );
}
