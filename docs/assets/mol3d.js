// The drug's real 3D structure (heavy atoms, from work/mol3d.json) drawn as a faint constellation of white stars.
// It turns as its panel scrolls, eases rather than snaps, and recedes while you read. Purely decorative.
window.dpasMol3d = function (host, scroller, mol, opts = {}) {
  const wrap = document.createElement("div"); wrap.className = "mol3d-wrap" + (opts.cls ? " " + opts.cls : ""); wrap.setAttribute("aria-hidden", "true");
  const cv = document.createElement("canvas"); cv.className = "mol3d"; wrap.append(cv); host.prepend(wrap);
  const S = opts.size || 260, dpr = Math.min(2, devicePixelRatio || 1);
  cv.width = S * dpr; cv.height = S * dpr; const g = cv.getContext("2d"); g.scale(dpr, dpr);
  const R = Math.max(...mol.a.map(([, x, y, z]) => Math.hypot(x, y, z))) || 1, k = (S * 0.4) / R;
  // starlight: white on a dark page; on a light page white would vanish, so the same stars in soft graphite
  const bg = getComputedStyle(document.body).backgroundColor.match(/\d+/g) || [255, 255, 255];
  const dark = (0.299 * bg[0] + 0.587 * bg[1] + 0.114 * bg[2]) < 128, ink = dark ? "255,255,255" : "40,44,52";
  const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const pos = () => (scroller === window ? scrollY : scroller.scrollTop) || 0;
  let shown = pos(), raf = 0;
  function draw(y) {
    const t = y / 140, ay = 0.6 + t, ax = -0.35 + Math.sin(t * 0.5) * 0.2;
    const cy = Math.cos(ay), sy = Math.sin(ay), cx = Math.cos(ax), sx = Math.sin(ax);
    const P = mol.a.map(([el, x, yy, z], i) => { const x1 = x * cy + z * sy, z1 = -x * sy + z * cy, y1 = yy * cx - z1 * sx, z2 = yy * sx + z1 * cx, s = 1 / (1 - z2 / (R * 3.5));
      return { el, i, x: S / 2 + x1 * k * s, y: S / 2 - y1 * k * s, z: z2, s }; });
    g.clearRect(0, 0, S, S);
    const depth = (z) => 0.3 + 0.7 * ((z / R + 1) / 2);  // far stars dim, like distance
    g.lineWidth = 0.6;
    for (const [i, j] of mol.b) { const A = P[i], B = P[j];
      g.strokeStyle = `rgba(${ink},${0.3 * depth((A.z + B.z) / 2)})`; g.beginPath(); g.moveTo(A.x, A.y); g.lineTo(B.x, B.y); g.stroke(); }
    for (const p of P.sort((a, b) => a.z - b.z)) {
      // heteroatoms (O, N, S…) are the brighter stars; carbons the faint ones
      const d = depth(p.z), tw = 0.82 + 0.18 * Math.sin(t * 3 + p.i * 1.7), r = (p.el === "C" ? 1.2 : 1.9) * p.s, halo = r * 4.5;
      const gr = g.createRadialGradient(p.x, p.y, 0, p.x, p.y, halo);
      gr.addColorStop(0, `rgba(${ink},${0.28 * d * tw})`); gr.addColorStop(1, `rgba(${ink},0)`);
      g.fillStyle = gr; g.beginPath(); g.arc(p.x, p.y, halo, 0, 7); g.fill();
      g.fillStyle = `rgba(${ink},${0.9 * d * tw})`; g.beginPath(); g.arc(p.x, p.y, r, 0, 7); g.fill();
    }
    // recede while reading: full strength at the top, about half once you're into the details
    if (opts.recede !== false) wrap.style.setProperty("--recede", String(1 - 0.45 * Math.min(1, y / 600)));
  }
  function frame() {  // ease toward the scroll position so the turn glides
    const target = pos(); shown += (target - shown) * (calm ? 1 : 0.12);
    draw(shown);
    raf = Math.abs(target - shown) > 0.5 ? requestAnimationFrame(frame) : 0;
  }
  const onScroll = () => { if (!raf) raf = requestAnimationFrame(frame); };
  scroller.addEventListener("scroll", onScroll, { passive: true });
  draw(shown); requestAnimationFrame(() => wrap.classList.add("on"));
  setTimeout(() => wrap.classList.add("settled"), 2000);  // after the fade-in, follow the reading quickly
  return () => { scroller.removeEventListener("scroll", onScroll); cancelAnimationFrame(raf); wrap.remove(); };
};
let molP = null;  // structures load once, on first use
window.dpasMolData = (root = document.documentElement.dataset.root || "") => (molP ||= fetch(`${root}drugs/mol3d.json?v=${document.documentElement.dataset.v || ""}`).then((r) => r.json()).catch(() => ({})));
