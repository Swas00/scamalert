/** Placeholder shaped like the report while analysis runs. */
export default function Skeleton() {
  return (
    <div className="space-y-10" aria-hidden="true">
      <div>
        <div className="skel h-2.5 w-14" />
        <div className="mt-5 flex items-end justify-between gap-6">
          <div className="skel h-9 w-[min(15rem,50%)]" />
          <div className="skel h-14 w-28" />
        </div>
        <div className="skel mt-6 h-[6px] w-full rounded-full" />
      </div>
      <div className="space-y-3 border-l-2 border-rule pl-5">
        {["92%", "100%", "84%", "60%"].map((w, i) => <div key={i} className="skel h-3.5" style={{ width: w, animationDelay: `${i * 120}ms` }} />)}
      </div>
    </div>
  );
}
