// Motion layer: Lenis smooth scrolling + GSAP/ScrollTrigger reveals, hero entrance, count-ups, a sliding nav
// underline and a soft cursor spotlight on cards. Polish only: every page works the same without it, and it
// all switches off for reduced-motion or the "Motion" setting.
(function () {
  const html = document.documentElement;
  const calm = matchMedia("(prefers-reduced-motion: reduce)").matches || html.dataset.pmotion === "off";
  const gsap = window.gsap, ST = window.ScrollTrigger;
  if (calm || !gsap || !ST) return;
  gsap.registerPlugin(ST);
  html.classList.add("gsap");

  // ---- smooth scrolling (mouse wheel / trackpad; touch keeps native scrolling)
  let lenis = null;
  if (window.Lenis) {
    const pad = parseFloat(getComputedStyle(html).scrollPaddingTop) || 72;
    lenis = new window.Lenis({
      lerp: 0.11, wheelMultiplier: 1, anchors: { offset: -pad },
      // panels, quizzes, search and Sidekick scroll on their own
      prevent: (node) => !!node.closest?.(".dx-sheet, .sk-panel, .qm, .sr-box, .set-pop, .deeper-pop, .tipcard, .sx-gate, .tabbar, [data-lenis-prevent]"),
    });
    lenis.on("scroll", ST.update);
    gsap.ticker.add((t) => lenis.raf(t * 1000));
    gsap.ticker.lagSmoothing(0);
    // when a sheet or quiz locks the page (overflow: hidden), the smooth scroller pauses too
    new MutationObserver(() => (html.style.overflow === "hidden" ? lenis.stop() : lenis.start())).observe(html, { attributes: true, attributeFilter: ["style"] });
    window.dpasLenis = lenis;
  }

  // ---- hero: lines rise out of a soft blur, then drift up and fade a little as you scroll away
  const lines = gsap.utils.toArray(".hero-title .line");
  if (lines.length) {
    gsap.fromTo(lines, { opacity: 0, y: 34, filter: "blur(10px)" }, { opacity: 1, y: 0, filter: "blur(0px)", duration: 1.15, ease: "expo.out", stagger: 0.12, delay: 0.05, clearProps: "filter" });
    const hero = document.querySelector(".first-screen .hero, .hero");
    if (hero && !matchMedia("(max-width: 760px)").matches) gsap.to(hero, { y: -36, opacity: 0.55, ease: "none", scrollTrigger: { trigger: hero, start: "top top+=60", end: "bottom top", scrub: true } });
  }

  // ---- scroll reveals: whatever enters together rises together, in a short stagger
  const counted = new WeakSet();
  const count = (el) => {
    if (counted.has(el)) return; counted.add(el);
    const to = +el.dataset.count; if (!to) return;
    const o = { v: 0 }; gsap.to(o, { v: to, duration: 1.4, ease: "power3.out", onUpdate: () => (el.textContent = Math.round(o.v).toLocaleString()) });
  };
  const reveal = (els) => {
    els = els.filter((e) => !e.classList.contains("in"));
    if (!els.length) return;
    els.forEach((e) => { e.classList.add("in"); e.querySelectorAll("[data-count]").forEach(count); });
    gsap.fromTo(els, { opacity: 0, y: 26, scale: 0.985, transition: "none" }, { opacity: 1, y: 0, scale: 1, duration: 0.95, ease: "expo.out", stagger: 0.07, clearProps: "transform,opacity,transition" });
  };
  ST.batch(".appear", { start: "top 94%", onEnter: reveal, interval: 0.08, batchMax: 8 });
  // things that appear later (cards drawn by scripts, unhidden sections) still get revealed and measured
  const refresh = (() => { let t = 0; return () => { clearTimeout(t); t = setTimeout(() => { ST.refresh(); document.querySelectorAll(".appear:not(.in)").forEach((e) => { const r = e.getBoundingClientRect(); if (r.top < innerHeight * 0.94 && r.bottom > 0 && e.offsetParent) reveal([e]); }); }, 120); }; })();
  new ResizeObserver(refresh).observe(document.body);
  // safety net: anything already on screen gets revealed even if a fast jump skipped its trigger
  let sweep = 0;
  addEventListener("scroll", () => { if (sweep) return; sweep = setTimeout(() => { sweep = 0; const els = [...document.querySelectorAll(".appear:not(.in)")].filter((e) => { const r = e.getBoundingClientRect(); return e.offsetParent && r.top < innerHeight && r.bottom > -innerHeight * 3; }); if (els.length) reveal(els); }, 250); }, { passive: true });
  addEventListener("load", refresh);

  // ---- nav: one underline that glides to the link you point at, and back to the current page
  const nav = document.querySelector(".nav-main");
  if (nav && matchMedia("(hover: hover)").matches) {
    const ink = document.createElement("span"); ink.className = "nav-ink"; nav.append(ink);
    const cur = () => nav.querySelector("a[aria-current]");
    const to = (a, instant) => {
      if (!a) return gsap.to(ink, { opacity: 0, duration: 0.25 });
      const r = a.getBoundingClientRect(), n = nav.getBoundingClientRect();
      gsap.to(ink, { x: r.left - n.left, y: r.bottom - n.top, width: r.width, opacity: 1, duration: instant ? 0 : 0.45, ease: "expo.out" });
    };
    html.classList.add("has-ink");
    requestAnimationFrame(() => to(cur(), true));
    nav.addEventListener("pointerover", (e) => { const a = e.target.closest("a"); if (a) to(a); });
    nav.addEventListener("pointerleave", () => to(cur()));
    addEventListener("resize", () => to(cur(), true));
    new MutationObserver(() => to(cur(), true)).observe(nav, { childList: true });  // e.g. the Sketch tab arriving
  }

  // ---- cards: a soft light follows the cursor
  if (matchMedia("(hover: hover)").matches) {
    const SEL = ".tile, .upcard, .dx-tile, .rv-act, .foot-tile, .sx-file, .card, .dotd, .now-fig";
    document.addEventListener("pointermove", (e) => {
      const c = e.target.closest?.(SEL); if (!c) return;
      const r = c.getBoundingClientRect();
      c.style.setProperty("--mx", `${e.clientX - r.left}px`); c.style.setProperty("--my", `${e.clientY - r.top}px`);
    }, { passive: true });
  }
})();
