/* ExamiQ motion helpers (shared by index.html and physics.html; embedded at build time, no network).
   Rules: motion runs only when the user has not asked for reduced motion; every animation is timestamp-based
   (frame-rate independent) and finite: nothing loops forever, so nothing needs a pause control. */
const ExamiQMotion = {
  get reduced() { return !document.documentElement.classList.contains('motion'); },
  /* Runs onFrame(f) with f = elapsed/duration in [0,1] using rAF timestamps, then onDone().
     A 30 Hz and a 120 Hz screen see the same state at the same wall-clock time. Returns a cancel function. */
  play(duration, onFrame, onDone) {
    if (this.reduced || duration <= 0) { onFrame(1); onDone && onDone(); return () => {}; }
    let start = null, id = 0, live = true;
    const tick = now => {
      if (!live) return;
      if (start === null) start = now;
      const f = Math.min(1, (now - start) / duration);
      onFrame(f);
      if (f < 1) id = requestAnimationFrame(tick); else { live = false; onDone && onDone(); }
    };
    id = requestAnimationFrame(tick);
    return () => { live = false; cancelAnimationFrame(id); };
  },
  /* Calls cb once, the first time el is at least `ratio` visible (immediately if IntersectionObserver is missing). */
  once(el, cb, ratio = 0.2) {
    if (!el) return;
    if (this.reduced || !('IntersectionObserver' in window)) { cb(); return; }
    const io = new IntersectionObserver(entries => {
      if (entries.some(e => e.isIntersecting)) { io.disconnect(); cb(); }
    }, { threshold: ratio });
    io.observe(el);
  }
};
