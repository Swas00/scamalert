import { useEffect, useRef, useState } from "react";

const prefersReducedMotion = () => window.matchMedia?.("(prefers-reduced-motion: reduce)").matches;

/** Decodes an audio File into ~N waveform peaks (0-1) and a duration in seconds. */
export function useAudioPeaks(file, bars = 96) {
  const [state, setState] = useState({ peaks: null, duration: 0, error: false });
  useEffect(() => {
    if (!file) { setState({ peaks: null, duration: 0, error: false }); return; }
    let cancelled = false;
    (async () => {
      try {
        const buf = await file.arrayBuffer();
        const audio = await new OfflineAudioContext(1, 1, 44100).decodeAudioData(buf);
        const data = audio.getChannelData(0);
        const size = Math.max(1, Math.floor(data.length / bars));
        const peaks = Array.from({ length: bars }, (_, i) => {
          let max = 0;
          for (let j = i * size; j < Math.min(data.length, (i + 1) * size); j++) max = Math.max(max, Math.abs(data[j]));
          return max;
        });
        const top = Math.max(...peaks, 0.001);
        if (!cancelled) setState({ peaks: peaks.map((p) => p / top), duration: audio.duration, error: false });
      } catch {
        if (!cancelled) setState({ peaks: null, duration: 0, error: true });
      }
    })();
    return () => { cancelled = true; };
  }, [file, bars]);
  return state;
}

/** Eases a number from 0 to `target` once `active`; jumps straight to the target under reduced motion. */
export function useCountUp(target, active, ms = 700) {
  const [value, setValue] = useState(0);
  useEffect(() => {
    if (!active) { setValue(0); return; }
    if (prefersReducedMotion()) { setValue(target); return; }
    let raf; const start = performance.now();
    const tick = (now) => {
      const t = Math.min(1, (now - start) / ms);
      setValue(Math.round(target * (1 - Math.pow(1 - t, 3))));
      if (t < 1) raf = requestAnimationFrame(tick);
    };
    raf = requestAnimationFrame(tick);
    return () => cancelAnimationFrame(raf);
  }, [target, active, ms]);
  return value;
}

/** Seconds elapsed while `running`. */
export function useElapsed(running) {
  const [s, setS] = useState(0);
  const t0 = useRef(0);
  useEffect(() => {
    if (!running) { setS(0); return; }
    t0.current = Date.now();
    const id = setInterval(() => setS(Math.floor((Date.now() - t0.current) / 1000)), 500);
    return () => clearInterval(id);
  }, [running]);
  return s;
}
