// Physiology scenes: hands-on, picture-first versions of the lecture figures. Molecules move, receptors fill, pumps
// spin; drag a drug onto the scene (or tap it) and watch what changes in the body. Facts and citations come from the
// lecture (each scene's notes); the drawings are illustrative. Registered into window.dpasViz so viz.js picks them up.
(function () {
  const V = window.dpasViz;
  if (!V) return;
  const NS = "http://www.w3.org/2000/svg", W = 640;
  const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const lerp = (a, b, t) => a + (b - a) * t;
  const mk = (tag, attrs = {}, parent) => { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); parent?.append(e); return e; };
  const pal = (el) => {
    const cs = getComputedStyle(el), v = (n, d) => cs.getPropertyValue(n).trim() || d;
    return { blue: v("--vz-1", "#0a84ff"), red: v("--vz-2", "#ff375f"), amber: v("--vz-3", "#ff9f0a"), purple: v("--vz-4", "#af52de"), green: v("--vz-5", "#34c759"),
      text: v("--vz-text", "#1d1d1f"), ink: v("--vz-ink", "#86868b"), grid: v("--vz-grid", "#ececf0"), bg: v("--vz-bg", "#fff") };
  };

  // ---------------------------------------------------------------- shared stage: header, svg, drug tray, condition switch, readout
  function stage(host, spec) {
    const el = document.createElement("div");
    el.className = "viz vz-scene";
    el.innerHTML = `<div class="vz-top"><span class="vz-pill">Interactive</span><span class="vz-hint">${spec.hint || "Drag a drug onto the picture, or tap it"}</span>
      <button type="button" class="vz-btn vz-reset" title="Start over">Reset</button><button type="button" class="vz-btn vz-swap">Original</button></div>
      ${spec.point ? `<p class="vz-point">${spec.point}</p>` : ""}
      ${spec.modes ? `<div class="vz-modes"><span class="vz-try">${esc(spec.modes.label)}</span><div class="seg" data-mode>${spec.modes.opts.map(([v, t]) => `<button type="button" data-v="${v}">${t}</button>`).join("")}</div></div>` : ""}
      <svg viewBox="0 0 ${W} ${spec.h}" role="img" aria-label="${esc(spec.label || "Interactive physiology scene")}"></svg>
      <div class="vz-tray" role="group" aria-label="Drugs">${spec.drugs.map((d) => `<button type="button" class="vz-chip" data-id="${d.id}" style="--c:${d.col || "var(--vz-1)"}"><i></i>${esc(d.label)}</button>`).join("")}</div>
      ${spec.steps ? `<div class="vz-steps"><span class="vz-try">Try it</span>${spec.steps.map((s, i) => `<button type="button" data-step="${i}"><b>${i + 1}</b>${esc(s.label)}</button>`).join("")}</div>` : ""}
      <p class="vz-read" aria-live="polite"></p>`;
    host.prepend(el);
    const svg = el.querySelector("svg"), read = el.querySelector(".vz-read");
    const S = { on: new Set(spec.start?.on || []), mode: spec.start?.mode ?? spec.modes?.opts[0][0], last: null };
    const api = { el, svg, S, C: pal(el), changed: () => {} };
    const paint = () => {
      el.querySelectorAll(".vz-chip").forEach((b) => { const on = S.on.has(b.dataset.id); b.classList.toggle("on", on); b.setAttribute("aria-pressed", on); });
      el.querySelectorAll("[data-mode] button").forEach((b) => b.classList.toggle("on", String(S.mode) === b.dataset.v));
      read.innerHTML = spec.read(S);
    };
    const set = (fn, why) => { fn(); api.changed(why); paint(); touch(); };
    const toggle = (id, from) => set(() => {
      const d = spec.drugs.find((x) => x.id === id);
      if (S.on.has(id)) S.on.delete(id);
      else { if (!spec.multi) S.on.clear(); (d.excl || []).forEach((x) => S.on.delete(x)); S.on.add(id); }
      S.last = S.on.has(id) ? id : null;
      if (S.on.has(id) && from) fly(from, id);
    }, { drug: id });
    // a pill flies from where it was dropped to the place it acts
    function fly([x0, y0], id) {
      const to = spec.target?.(id, S);
      if (!to || calm) return;
      const d = spec.drugs.find((x) => x.id === id), g = mk("g", { class: "vz-fly" }, svg);
      mk("rect", { x: -16, y: -7, width: 32, height: 14, rx: 7, fill: d.col || api.C.blue }, g);
      mk("rect", { x: 0, y: -7, width: 16, height: 14, rx: 0, fill: "#fff", opacity: 0.35 }, g);
      const t0 = performance.now();
      const step = (now) => {
        const t = Math.min(1, (now - t0) / 650), e = 1 - (1 - t) ** 3;
        g.setAttribute("transform", `translate(${lerp(x0, to[0], e)},${lerp(y0, to[1], e) - Math.sin(Math.PI * t) * 40}) scale(${1 - 0.4 * t})`);
        g.setAttribute("opacity", t > 0.85 ? (1 - t) / 0.15 : 1);
        if (t < 1) requestAnimationFrame(step); else g.remove();
      };
      requestAnimationFrame(step);
    }
    // drag a chip onto the picture (a tap toggles it too)
    el.querySelectorAll(".vz-chip").forEach((b) => {
      let ghost = null, sx = 0, sy = 0, moved = false;
      b.addEventListener("pointerdown", (e) => { sx = e.clientX; sy = e.clientY; moved = false; b.setPointerCapture(e.pointerId); });
      b.addEventListener("pointermove", (e) => {
        if (!b.hasPointerCapture(e.pointerId)) return;
        if (!moved && Math.hypot(e.clientX - sx, e.clientY - sy) < 8) return;
        if (!ghost) { moved = true; ghost = b.cloneNode(true); ghost.className = "vz-chip on vz-ghost"; document.body.append(ghost); }
        ghost.style.left = `${e.clientX}px`; ghost.style.top = `${e.clientY}px`;
        svg.classList.toggle("vz-drop", isOver(e));
      });
      const isOver = (e) => { const r = svg.getBoundingClientRect(); return e.clientX > r.left && e.clientX < r.right && e.clientY > r.top && e.clientY < r.bottom; };
      b.addEventListener("pointerup", (e) => {
        svg.classList.remove("vz-drop");
        if (ghost) {
          ghost.remove(); ghost = null;
          if (isOver(e)) { const r = svg.getBoundingClientRect(), x = ((e.clientX - r.left) / r.width) * W, y = ((e.clientY - r.top) / r.height) * spec.h; if (!S.on.has(b.dataset.id)) toggle(b.dataset.id, [x, y]); }
        } else toggle(b.dataset.id, [W / 2, spec.h + 20]);
      });
      b.addEventListener("pointercancel", () => { ghost?.remove(); ghost = null; svg.classList.remove("vz-drop"); });
    });
    el.querySelectorAll("[data-mode] button").forEach((b) => (b.onclick = () => set(() => { S.mode = isNaN(+b.dataset.v) ? b.dataset.v : +b.dataset.v; }, { mode: S.mode })));
    const stepBtns = [...el.querySelectorAll("[data-step]")];
    stepBtns.forEach((b) => (b.onclick = () => {
      const st = spec.steps[+b.dataset.step];
      stepBtns.forEach((x) => x.classList.toggle("on", x === b));
      set(() => { S.on = new Set(); if (st.mode !== undefined) S.mode = st.mode; api.changed({ preset: true }); }, { preset: true });
      // drugs in a preset arrive one after another, so each effect is visible
      (st.on || []).forEach((id, k) => setTimeout(() => toggle(id, [W / 2, spec.h + 20]), 350 + k * 650));
    }));
    let idle = 0;
    function touch() { el.classList.add("dirty"); clearTimeout(idle); idle = setTimeout(reset, 30000); }
    function reset() {
      clearTimeout(idle); stepBtns.forEach((x) => x.classList.remove("on"));
      S.on = new Set(spec.start?.on || []); S.mode = spec.start?.mode ?? spec.modes?.opts[0][0]; S.last = null;
      api.changed({ reset: true }); paint(); el.classList.remove("dirty");
    }
    el.querySelector(".vz-reset").onclick = reset;
    // animation loop: runs only while the figure is on screen
    let raf = 0, visible = false, t0 = 0;
    const loop = (now) => { const dt = Math.min(0.05, (now - (t0 || now)) / 1000); t0 = now; api.tick?.(dt); raf = visible && !document.hidden ? requestAnimationFrame(loop) : 0; };
    const kick = () => { if (!raf && visible) { t0 = 0; raf = requestAnimationFrame(loop); } };
    new IntersectionObserver(([e]) => { visible = e.isIntersecting; kick(); }).observe(el);
    document.addEventListener("visibilitychange", kick);
    new MutationObserver(() => { api.C = pal(el); api.recolor?.(); }).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    api.paint = paint;
    setTimeout(paint, 0);
    return api;
  }

  // ---------------------------------------------------------------- particles that travel a polyline and can be stopped part-way
  function stream(layer, pts, o) {
    const segs = [], ps = [];
    let total = 0;
    for (let i = 1; i < pts.length; i++) { const l = Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]); segs.push(l); total += l; }
    const at = (d) => { let k = 0; while (k < segs.length - 1 && d > segs[k]) { d -= segs[k]; k++; } const t = segs[k] ? clamp(d / segs[k], 0, 1) : 0; return [lerp(pts[k][0], pts[k + 1][0], t), lerp(pts[k][1], pts[k + 1][1], t)]; };
    const s = { rate: o.rate ?? 2, speed: o.speed ?? 70, stop: null, acc: Math.random(), col: o.col, r: o.r ?? 3.2, on: true, total, onArrive: o.onArrive };
    s.tick = (dt) => {
      s.acc += dt * (s.on ? s.rate : 0);
      while (s.acc >= 1 && ps.length < 40) { s.acc -= 1; const c = mk("circle", { r: s.r, fill: s.col() }, layer); ps.push({ d: 0, c, fade: 0, j: (Math.random() - 0.5) * (o.jitter ?? 4) }); }
      for (let i = ps.length - 1; i >= 0; i--) {
        const p = ps[i], lim = s.stop != null ? s.stop * total : total;
        if (p.fade) { p.fade -= dt * 2.2; p.c.setAttribute("opacity", Math.max(0, p.fade)); if (p.fade <= 0) { p.c.remove(); ps.splice(i, 1); } continue; }
        p.d += dt * s.speed;
        if (p.d >= lim) { p.d = lim - (s.stop != null ? 6 : 0); p.fade = 1; if (s.stop == null) s.onArrive?.(); }
        const [x, y] = at(p.d);
        p.c.setAttribute("cx", x + (o.perp ? 0 : 0)); p.c.setAttribute("cy", y + p.j);
        p.c.setAttribute("fill", s.col());
      }
    };
    s.clear = () => { ps.forEach((p) => p.c.remove()); ps.length = 0; };
    return s;
  }
  const label = (parent, x, y, txt, o = {}) => { const t = mk("text", { x, y, "text-anchor": o.a || "middle", class: o.cls || "vz-sc-l" }, parent); t.textContent = txt; return t; };
  const blocker = (parent, x, y, col) => {  // a drug sitting in a receptor or pump: a small capsule with an X
    const g = mk("g", { class: "vz-block", transform: `translate(${x},${y})` }, parent);
    mk("circle", { r: 11, fill: col, class: "vz-bk-c" }, g);
    mk("path", { d: "M-4,-4L4,4M4,-4L-4,4", stroke: "#fff", "stroke-width": 2.4, "stroke-linecap": "round" }, g);
    return g;
  };
  const show = (e, on) => e && e.classList.toggle("vz-hide", !on);
  const cite = (s) => ` <span class="cite">${esc(s)}</span>`;

  // ================================================================ PARIETAL CELL: three inputs converge on the proton pump
  V.parietal = (host, cfg = {}) => {
    const H = 340, drugs = cfg.drugs || [
      { id: "fam", label: "Famotidine (H2 blocker)" }, { id: "ppi", label: "Omeprazole (PPI)" }, { id: "ant", label: "Antacid" }];
    const COL = { fam: "var(--vz-1)", ppi: "var(--vz-2)", ant: "var(--vz-5)", cim: "var(--vz-4)" };
    drugs.forEach((d) => (d.col ||= COL[d.id]));
    const INP = [{ k: "his", y: 70, src: "ECL cell", mol: "histamine", rec: "H2 receptor", c: "purple" },
      { k: "ach", y: 170, src: "Vagus nerve", mol: "acetylcholine", rec: "ACh receptor", c: "green" },
      { k: "gas", y: 270, src: "G cell", mol: "gastrin", rec: "Gastrin receptor", c: "amber" }];
    const PUMPS = [78, 138, 198, 258];
    let locked = new Set(), antT = 0, acid = 0.25, ion = [];
    const blocked = (S) => new Set([...(S.on.has("fam") || S.on.has("cim") ? ["his"] : [])]);
    const activePumps = (S) => (S.mode === "meal" ? [0, 1, 2, 3] : [1]);
    const output = (S) => {
      const f = INP.filter((i) => !blocked(S).has(i.k)).length / 3;
      return (activePumps(S).filter((p) => !locked.has(p)).length / 4) * f;
    };
    const notes = cfg.notes || {};
    const st = stage(host, {
      h: H, drugs, multi: true, label: "Parietal cell: acid secretion", point: cfg.point || "Three signals — histamine, acetylcholine and gastrin — all switch on the same proton pump. Block one signal, or block the pump itself?",
      modes: { label: "Stomach", opts: [["fast", "Fasting"], ["meal", "Meal (pumps switch on)"]] }, start: { mode: cfg.mode || "meal" },
      steps: cfg.steps || [{ label: "A meal: all three signals", mode: "meal" }, { label: "Famotidine", mode: "meal", on: ["fam"] }, { label: "Omeprazole before a meal", mode: "meal", on: ["ppi"] },
        { label: "Omeprazole while fasting", mode: "fast", on: ["ppi"] }, { label: "Antacid", mode: "meal", on: ["ant"] }],
      target: (id) => (id === "fam" || id === "cim" ? [206, 70] : id === "ppi" ? [470, 168] : [560, 200]),
      read(S) {
        const pct = Math.round(output(S) * 100), bits = [];
        if (!S.on.size) bits.push(notes.base || `<b>All three inputs converge on the pump.</b> Histamine (H2), acetylcholine and gastrin each switch the H⁺/K⁺ ATPase on; it pumps acid into the stomach.${cite("S8")}`);
        if (S.on.has("fam")) bits.push(notes.fam || `<b>Famotidine blocks only the histamine (H2) input.</b> Acetylcholine and gastrin still drive the pump, so acid falls only partly. Best for nocturnal acid; tachyphylaxis; reduce dose in renal impairment.${cite("S8; S13–S14")}`);
        if (S.on.has("cim")) bits.push(notes.cim || `<b>Cimetidine also blocks H2</b> — plus it inhibits CYP450 (1A2, 2C19, 3A4) and has antiandrogenic effects.${cite("S13–S14")}`);
        if (S.on.has("ppi")) {
          const missed = activePumps({ mode: "meal" }).filter((p) => !locked.has(p)).length;
          bits.push(notes.ppi || `<b>Omeprazole locks the pump itself — the final common pathway.</b> Acid falls whichever signal is active. The bond is irreversible: a locked pump stays off until the cell makes a new one.${cite("S8; S15–S16")}`);
          if (missed) bits.push(`<b>Taken while fasting, it only caught ${4 - missed} of 4 pumps</b> — PPIs work only on pumps that are actively secreting. ${S.mode === "fast" ? "Switch to <i>Meal</i>: the idle pumps turn on and acid comes back." : ""} That's why it's taken 30–60 minutes before the first meal.${cite("S16")}`);
        }
        if (S.on.has("ant")) bits.push(notes.ant || `<b>An antacid neutralizes acid already in the stomach</b> — fast but short-lived; the pumps keep working.${cite("S12; S22")}`);
        return `${bits.join(" ")} <span class="vz-meter-t">Acid output: <b>${pct}%</b></span>`;
      },
    });
    const { svg } = st;
    let C = st.C;
    // ---- static drawing
    const bgL = mk("g", {}, svg), cellL = mk("g", {}, svg), flowL = mk("g", {}, svg), topL = mk("g", {}, svg);
    const lumen = mk("rect", { x: 486, y: 18, width: 150, height: 304, rx: 22, class: "vz-sc-lumen" }, bgL);
    label(bgL, 552, 40, "Stomach lumen", { cls: "vz-sc-h" });
    const cell = mk("rect", { x: 196, y: 24, width: 278, height: 292, rx: 46, class: "vz-sc-cell" }, cellL);
    mk("rect", { x: 202, y: 30, width: 266, height: 280, rx: 40, class: "vz-sc-cell2" }, cellL);
    label(cellL, 335, 304, "Parietal cell", { cls: "vz-sc-h" });
    const nuc = mk("ellipse", { cx: 318, cy: 168, rx: 34, ry: 26, class: "vz-sc-nuc" }, cellL);
    const recs = {}, msg = {};
    INP.forEach((i) => {
      // source
      const g = mk("g", {}, bgL);
      if (i.k === "ach") { mk("path", { d: `M8,${i.y}H66`, class: "vz-sc-nerve" }, g); mk("circle", { cx: 74, cy: i.y, r: 14, class: "vz-sc-src", style: `--c:var(--vz-${i.c === "green" ? 5 : 3})` }, g); }
      else mk("circle", { cx: 62, cy: i.y, r: 24, class: "vz-sc-src", style: `--c:var(--vz-${i.c === "purple" ? 4 : 3})` }, g);
      label(g, 62, i.y + (i.k === "ach" ? 30 : 40), i.src, { cls: "vz-sc-s" });
      label(g, 140, i.y - 12, i.mol, { cls: "vz-sc-m" });
      // receptor: a cup on the membrane
      const r = mk("g", { transform: `translate(198,${i.y})` }, cellL);
      mk("path", { d: "M-10,-13 Q-2,-13 -2,-6 L-2,6 Q-2,13 -10,13 M-2,-6 Q6,-6 6,0 Q6,6 -2,6", class: "vz-sc-rec", style: `--c:var(--vz-${{ purple: 4, green: 5, amber: 3 }[i.c]})` }, r);
      label(cellL, 214, i.y + 4, i.rec, { a: "start", cls: "vz-sc-r" });
      recs[i.k] = r;
      // signal inside the cell → pumps
      const pts = [[214, i.y + 12], [300, i.y + 12], [400, 168], [458, 168]];
      mk("path", { d: `M${pts.map((p) => p.join(",")).join("L")}`, class: "vz-sc-path" }, cellL);
      msg[i.k] = stream(flowL, pts, { col: () => C.amber, rate: 1.4, speed: 90, r: 2.6, jitter: 2 });
      i.str = stream(flowL, [[90, i.y], [194, i.y]], { col: () => C[i.c], rate: 3, speed: 60, r: 3.4, jitter: 9 });
    });
    label(cellL, 452, 54, "Proton pumps", { a: "end", cls: "vz-sc-r" });
    label(cellL, 452, 68, "H⁺/K⁺ ATPase", { a: "end", cls: "vz-sc-s" });
    const pumps = PUMPS.map((y) => {
      const g = mk("g", { transform: `translate(474,${y})` }, cellL);
      mk("rect", { x: -10, y: -17, width: 20, height: 34, rx: 8, class: "vz-sc-pump" }, g);
      const rot = mk("g", {}, g);
      mk("path", { d: "M-5,-6H4M1,-9L5,-6L1,-3", class: "vz-sc-rotor" }, rot);
      mk("path", { d: "M5,6H-4M-1,3L-5,6L-1,9", class: "vz-sc-rotor k" }, rot);
      const lock = mk("g", { class: "vz-hide" }, g);
      mk("rect", { x: -7, y: -3, width: 14, height: 11, rx: 2.5, class: "vz-sc-lock" }, lock);
      mk("path", { d: "M-4,-3V-6A4,4 0 0 1 4,-6V-3", class: "vz-sc-lockarc" }, lock);
      return { g, rot, lock, a: 0 };
    });
    const famB = blocker(topL, 192, 70, "var(--vz-1)"); show(famB, false);
    // acid meter
    mk("rect", { x: 606, y: 66, width: 16, height: 236, rx: 8, class: "vz-sc-mtrack" }, topL);
    const meter = mk("rect", { x: 606, y: 66, width: 16, height: 236, rx: 8, class: "vz-sc-mfill" }, topL);
    label(topL, 614, 58, "Acid", { cls: "vz-sc-s" });
    const ions = mk("g", {}, flowL), base = mk("g", {}, flowL);
    // ---- behavior
    st.changed = (why) => {
      const S = st.S;
      if (why?.drug === "ppi") locked = S.on.has("ppi") ? new Set(activePumps(S)) : new Set();
      if (why?.reset || why?.preset) locked = new Set();
      if (why?.drug === "ant" && S.on.has("ant")) antT = 7;
      show(famB, S.on.has("fam") || S.on.has("cim"));
      pumps.forEach((p, k) => { show(p.lock, locked.has(k)); p.g.classList.toggle("vz-idle", !activePumps(S).includes(k)); });
    };
    st.recolor = () => { C = st.C; };
    st.tick = (dt) => {
      const S = st.S, bl = blocked(S), meal = S.mode === "meal", out = output(S);
      INP.forEach((i) => {
        i.str.rate = meal ? 3 : 1; i.str.stop = bl.has(i.k) ? 0.93 : null; i.str.tick(dt);
        msg[i.k].on = !bl.has(i.k); msg[i.k].rate = meal ? 1.6 : 0.6; msg[i.k].tick(dt);
      });
      pumps.forEach((p, k) => {
        const run = activePumps(S).includes(k) && !locked.has(k);
        p.a += dt * (run ? 6 * (0.4 + out) : 0); p.rot.setAttribute("transform", `translate(${run ? Math.sin(p.a) * 2.5 : 0},0)`);
        if (run && Math.random() < dt * 1.6 * (0.3 + out)) ion.push({ x: 490, y: PUMPS[k] + (Math.random() - 0.5) * 10, vx: 30 + Math.random() * 40, vy: (Math.random() - 0.5) * 50, c: mk("text", { class: "vz-sc-ion" }, ions), life: 5 });
      });
      antT = Math.max(0, antT - dt);
      if (S.on.has("ant") && antT > 0 && Math.random() < dt * 6) { const b = mk("circle", { cx: 500 + Math.random() * 90, cy: 80 + Math.random() * 220, r: 4, class: "vz-sc-base" }, base); setTimeout(() => b.remove(), 1200); }
      ion = ion.filter((p) => {
        p.life -= dt * (S.on.has("ant") && antT > 0 ? 2.5 : 1); p.x += p.vx * dt; p.y += p.vy * dt; p.vx *= 0.985; p.vy *= 0.99; if (p.x > 588) p.vx = -Math.abs(p.vx); if (p.y < 60 || p.y > 312) p.vy = -p.vy;
        p.c.textContent = "H⁺"; p.c.setAttribute("x", p.x); p.c.setAttribute("y", p.y); p.c.setAttribute("opacity", clamp(p.life, 0, 1));
        if (p.life <= 0) { p.c.remove(); return false; } return true;
      });
      const target = out * (S.on.has("ant") && antT > 0 ? 0.3 : 1);
      acid += (target - acid) * Math.min(1, dt * 2);
      meter.setAttribute("y", 66 + 236 * (1 - acid)); meter.setAttribute("height", 236 * acid);
    };
    st.changed({ reset: true });
    return st;
  };

  // ================================================================ SEESAW: aggressive vs protective (or any two-sided balance)
  V.seesaw = (host, cfg = {}) => {
    const H = cfg.h || 300, left = cfg.left, right = cfg.right;  // {title, items:[{id,label,w}]}
    const st = stage(host, {
      h: H, drugs: cfg.drugs, multi: true, label: cfg.title || "Balance", point: cfg.point, hint: cfg.hint || "Tap factors and drugs to add or remove weight",
      steps: cfg.steps, start: { on: cfg.startOn || [] },
      target: () => [320, 120],
      read(S) {
        const t = tilt(S), d = cfg.drugs.filter((x) => S.on.has(x.id)), last = cfg.drugs.find((x) => x.id === S.last);
        const verdict = t > 0.15 ? cfg.verdict?.left || "Tipped toward injury." : t < -0.15 ? cfg.verdict?.right || "Defenses win." : cfg.verdict?.even || "Balanced.";
        return `${last ? `<b>${esc(last.label)}.</b> ${last.note || ""} ` : d.length ? "" : cfg.read || ""}<span class="vz-meter-t">${verdict}</span>`;
      },
    });
    const { svg } = st;
    const weights = (S, side) => {
      let items = side.items.map((x) => ({ ...x }));
      cfg.drugs.forEach((d) => { if (!S.on.has(d.id)) return; (d.remove || []).forEach((id) => (items = items.filter((x) => x.id !== id))); (d.scale || []).forEach(([id, k]) => items.forEach((x) => { if (x.id === id) x.w *= k; })); if (d.add && d.side === (side === left ? "L" : "R")) items.push({ id: d.id, label: d.add, w: d.w || 1, drug: true, col: d.col }); });
      return items;
    };
    const sum = (xs) => xs.reduce((a, b) => a + b.w, 0);
    const tilt = (S) => clamp((sum(weights(S, left)) - sum(weights(S, right))) / 4, -1, 1);
    const P = [320, 196];
    mk("path", { d: `M${P[0] - 34},${H - 22}L${P[0]},${P[1] + 6}L${P[0] + 34},${H - 22}Z`, class: "vz-sc-fulcrum" }, svg);
    mk("rect", { x: 40, y: H - 24, width: 560, height: 6, rx: 3, class: "vz-sc-ground" }, svg);
    const beam = mk("g", {}, svg);
    mk("rect", { x: -250, y: -5, width: 500, height: 10, rx: 5, class: "vz-sc-beam" }, beam);
    const panL = mk("g", {}, svg), panR = mk("g", {}, svg);
    const titleL = label(svg, 115, 26, left.title, { cls: "vz-sc-h vz-sc-red" }), titleR = label(svg, 525, 26, right.title, { cls: "vz-sc-h vz-sc-green" });
    const verdict = label(svg, 320, H - 6, "", { cls: "vz-sc-s" });
    let ang = 0;
    const blocks = (g, items, x0, col) => {
      g.innerHTML = "";
      let y = 0;
      items.slice().reverse().forEach((it) => {
        const h = 16 + it.w * 10, w = 132;
        const b = mk("g", { class: `vz-sc-wt${it.drug ? " drug" : ""}`, transform: `translate(${x0 - w / 2},${-y - h})` }, g);
        mk("rect", { width: w, height: h - 3, rx: 9, style: `--c:${it.col || col}` }, b);
        label(b, w / 2, (h - 3) / 2 + 4, it.label, { cls: "vz-sc-wl" });
        y += h;
      });
    };
    st.changed = () => { const S = st.S; blocks(panL, weights(S, left), 0, "var(--vz-2)"); blocks(panR, weights(S, right), 0, "var(--vz-5)"); };
    st.tick = (dt) => {
      const target = tilt(st.S) * 14;
      ang += (target - ang) * Math.min(1, dt * (calm ? 30 : 3));
      beam.setAttribute("transform", `translate(${P[0]},${P[1]}) rotate(${-ang})`);
      const r = (-ang * Math.PI) / 180, px = (dx) => [P[0] + dx * Math.cos(r), P[1] + dx * Math.sin(r)];
      const [lx, ly] = px(-205), [rx, ry] = px(205);
      panL.setAttribute("transform", `translate(${lx},${ly - 6})`); panR.setAttribute("transform", `translate(${rx},${ry - 6})`);
      verdict.textContent = "";
      titleL.classList.toggle("vz-sc-win", ang > 2); titleR.classList.toggle("vz-sc-win", ang < -2);
    };
    st.changed();
    return st;
  };

  // ================================================================ H. PYLORI: why one drug isn't enough
  V.hpylori = (host, cfg = {}) => {
    const H = 320;
    const drugs = [{ id: "ppi", label: "PPI", col: "var(--vz-2)" }, { id: "amox", label: "Amoxicillin", col: "var(--vz-1)" }, { id: "clar", label: "Clarithromycin", col: "var(--vz-4)" },
      { id: "metro", label: "Metronidazole", col: "var(--vz-3)" }, { id: "bis", label: "Bismuth", col: "var(--vz-5)" }, { id: "tet", label: "Tetracycline", col: "var(--vz-1)" }];
    const st = stage(host, {
      h: H, drugs, multi: true, label: "H. pylori in the gastric mucus", hint: "Build a regimen: tap or drag drugs onto the stomach lining",
      point: cfg.point || "H. pylori hides in the mucus and makes ammonia to buffer acid. Build a regimen that actually clears it.",
      modes: { label: "Patient", opts: [["none", "No allergies"], ["pcn", "Penicillin allergy"], ["mac", "Recent macrolide"], ["both", "Both"]] }, start: { mode: "none" },
      steps: [{ label: "Amoxicillin alone", on: ["amox"] }, { label: "Triple therapy", on: ["ppi", "amox", "clar"] }, { label: "Recent macrolide + triple", mode: "mac", on: ["ppi", "amox", "clar"] },
        { label: "Bismuth quadruple", mode: "both", on: ["ppi", "bis", "tet", "metro"] }],
      target: () => [320, 196],
      read(S) { return verdict(S).html; },
    });
    const { svg } = st;
    const pcn = (S) => S.mode === "pcn" || S.mode === "both", mac = (S) => S.mode === "mac" || S.mode === "both";
    function verdict(S) {
      const on = (k) => S.on.has(k), abx = ["amox", "clar", "metro", "tet"].filter(on);
      const warn = [];
      if (on("amox") && pcn(S)) warn.push(`<b>Penicillin allergy rules out amoxicillin.</b> In triple therapy, metronidazole substitutes for it — or choose bismuth quadruple therapy.${cite("S23; S25")}`);
      if (on("clar") && mac(S)) warn.push(`<b>Recent macrolide exposure raises concern for clarithromycin resistance</b> — the bacteria shrug it off.${cite("S23; S25")}`);
      const works = (k) => on(k) && !(k === "amox" && pcn(S)) && !(k === "clar" && mac(S));
      const triple = on("ppi") && works("clar") && (works("amox") || works("metro"));
      const quad = on("ppi") && on("bis") && works("tet") && works("metro");
      let kill = 0, html;
      if (quad || triple) { kill = 1; html = `<b>Eradicated.</b> ${quad ? "Bismuth quadruple therapy: PPI + bismuth + tetracycline + metronidazole — preferred with penicillin allergy or recent macrolide exposure." : "Triple therapy: PPI + clarithromycin + amoxicillin (or metronidazole if penicillin-allergic)."} Usual course 14 days; confirm with a urea breath test or stool antigen at least 4 weeks later, PPI held 2 weeks.${cite("S23; S24")}`; }
      else if (!S.on.size) html = `<b>H. pylori lives in the mucus layer</b> and buffers acid with urease-made ammonia. It's the leading identifiable cause of peptic ulcer disease — eradication, not just acid suppression, is the goal.${cite("S23; S24")}`;
      else {
        const good = abx.filter(works).length;
        kill = clamp(good * 0.3 + (on("ppi") ? 0.1 : 0), 0, 0.8);
        html = !on("ppi") && good >= 2 ? `<b>Close — add a PPI.</b> Raising gastric pH lets the bacteria enter a replicating state and keeps the antibiotics stable.${cite("S24")}`
          : on("ppi") && !good ? `<b>A PPI alone doesn't eradicate it.</b> It raises pH so the antibiotics work — you still need the antibiotics.${cite("S23; S24")}`
          : `<b>Survivors regrow.</b> ${good < 2 ? "One working antibiotic isn't enough — regimens pair two (plus a PPI)." : "This combination isn't one of the taught regimens."}${cite("S23; S24")}`;
      }
      return { kill, html: `${warn.join(" ")} ${html}` };
    }
    // lining, mucus, lumen
    mk("rect", { x: 0, y: 0, width: W, height: 120, class: "vz-sc-lumen" }, svg);
    label(svg, 24, 26, "Stomach lumen (acid)", { a: "start", cls: "vz-sc-h" });
    mk("path", { d: `M0,120 ${Array.from({ length: 17 }, (_, i) => `Q${i * 40 + 20},${i % 2 ? 108 : 132} ${(i + 1) * 40},120`).join(" ")} V240 H0Z`, class: "vz-sc-mucus" }, svg);
    label(svg, 24, 150, "Mucus layer", { a: "start", cls: "vz-sc-s" });
    for (let i = 0; i < 16; i++) mk("rect", { x: i * 40 + 2, y: 240, width: 36, height: 64, rx: 10, class: "vz-sc-epi" }, svg);
    label(svg, 24, 296, "Gastric epithelium", { a: "start", cls: "vz-sc-s" });
    const hs = mk("g", {}, svg), bugs = mk("g", {}, svg), shields = mk("g", {}, svg);
    const acidIons = Array.from({ length: 16 }, () => ({ x: Math.random() * W, y: 40 + Math.random() * 70, c: mk("text", { class: "vz-sc-ion" }, hs) }));
    const B = Array.from({ length: 12 }, (_, i) => {
      const g = mk("g", {}, bugs), x = 50 + i * 48 + (i % 2) * 10, y = 170 + (i % 3) * 22;
      mk("path", { d: "M-12,0 Q-6,-7 0,0 T12,0", class: "vz-sc-bug" }, g);
      mk("path", { d: "M12,0 q5,-4 8,-1 M12,0 q6,2 9,6", class: "vz-sc-flag" }, g);
      const cloud = mk("text", { x: 0, y: -14, class: "vz-sc-nh3", "text-anchor": "middle" }, g); cloud.textContent = "NH₃";
      return { g, x, y, ph: Math.random() * 6, alive: 1, cut: i / 12 };
    });
    let killT = 0, kill = 0;
    st.changed = () => { kill = verdict(st.S).kill; killT = 0; };
    st.tick = (dt) => {
      const S = st.S, ppi = S.on.has("ppi");
      acidIons.forEach((p, k) => { p.x = (p.x + dt * 12) % W; p.c.textContent = "H⁺"; p.c.setAttribute("x", p.x); p.c.setAttribute("y", p.y + Math.sin(performance.now() / 700 + k) * 3); p.c.setAttribute("opacity", ppi && k % 3 ? 0.08 : 0.55); });
      killT = Math.min(1, killT + dt * 0.6);
      B.forEach((b) => {
        const dead = b.cut < kill, target = dead ? 0 : 1;
        b.alive += (target - b.alive) * Math.min(1, dt * (dead ? 1.5 * killT : 0.8));
        b.ph += dt * (ppi ? 4 : 1.6);
        b.g.setAttribute("transform", `translate(${b.x + Math.sin(b.ph) * 6},${b.y + Math.cos(b.ph * 0.7) * 3}) rotate(${Math.sin(b.ph) * 12}) scale(${0.6 + 0.4 * b.alive})`);
        b.g.setAttribute("opacity", 0.1 + 0.9 * b.alive);
      });
    };
    st.changed();
    return st;
  };

  // ================================================================ VOMITING MAP: four inputs converge on the vomiting center
  V.emesis = (host, cfg = {}) => {
    const H = 380;
    const ALL = {
      ond: { label: "Ondansetron", col: "var(--vz-4)", blocks: ["gut:5HT3", "ctz:5HT3"] },
      meto: { label: "Metoclopramide", col: "var(--vz-1)", blocks: ["ctz:D2"], prokinetic: true },
      pro: { label: "Prochlorperazine", col: "var(--vz-1)", blocks: ["ctz:D2"] },
      apr: { label: "Aprepitant", col: "var(--vz-3)", blocks: ["ctz:NK1"] },
      mec: { label: "Meclizine", col: "var(--vz-5)", blocks: ["ves:H1/M1"] },
      sco: { label: "Scopolamine", col: "var(--vz-5)", blocks: ["ves:H1/M1"] },
      dro: { label: "Dronabinol", col: "var(--vz-2)", cb1: true },
      bzd: { label: "Benzodiazepine", col: "var(--vz-2)", blocks: ["cor:anx"] },
    };
    const ids = cfg.drugs || Object.keys(ALL), notes = cfg.notes || {};
    const drugs = ids.map((id) => ({ id, ...ALL[id], note: notes[id] }));
    // inputs: where each signal starts and which receptors carry it
    const IN = {
      gut: { name: "GI tract → vagus", rec: ["5HT3"], at: [150, 300], path: [[150, 300], [150, 220], [255, 205]] },
      ctz: { name: "Chemoreceptor trigger zone", rec: ["D2", "5HT3", "NK1"], at: [330, 150], path: [[330, 150], [300, 180], [285, 196]] },
      ves: { name: "Vestibular system", rec: ["H1/M1"], at: [470, 175], path: [[470, 175], [380, 196], [300, 200]] },
      cor: { name: "Cortex (anxiety, anticipation)", rec: ["anx"], at: [250, 70], path: [[250, 70], [262, 130], [270, 186]] },
    };
    const TRIG = { chemo: { gut: 1, ctz: 1 }, motion: { ves: 1 }, anx: { cor: 1 } };
    const st = stage(host, {
      h: H, drugs, multi: true, label: "The vomiting reflex", hint: "Pick a cause, then drag antiemetics onto the brain or gut",
      point: cfg.point || "Four inputs converge on the vomiting center in the medulla. Each antiemetic blocks one input — so match the drug to the cause.",
      modes: { label: "Cause", opts: (cfg.causes || ["chemo", "motion", "anx"]).map((k) => [k, { chemo: "Chemotherapy", motion: "Motion sickness", anx: "Anticipatory / anxiety" }[k]]) },
      start: { mode: cfg.mode || "chemo" }, steps: cfg.steps,
      target: (id) => { const d = ALL[id]; if (d.cb1) return [270, 205]; const k = d.blocks[0].split(":")[0]; return IN[k].at; },
      read(S) {
        const n = Math.round(level(S) * 100), last = drugs.find((d) => d.id === S.last);
        const mism = last && !last.cb1 && !last.blocks.some((b) => TRIG[S.mode][b.split(":")[0]]);
        return `${last ? `<b>${esc(last.label)}.</b> ${last.note || ""}${mism ? ` <b>It doesn't touch this cause</b> — the signal comes in through a different input.` : ""}` : esc(cfg.read || "")} <span class="vz-meter-t">Nausea signal: <b>${n}%</b>${S.on.has("meto") ? " · Gastric emptying: <b>faster</b>" : ""}</span>`;
      },
    });
    const { svg } = st;
    let C = st.C;
    const blockedSet = (S) => new Set([...S.on].flatMap((id) => ALL[id].blocks || []));
    function level(S) {
      const bl = blockedSet(S), tr = TRIG[S.mode];
      let tot = 0, live = 0;
      Object.entries(tr).forEach(([k]) => { const rs = IN[k].rec; tot += 1; live += rs.filter((r) => !bl.has(`${k}:${r}`)).length / rs.length; });
      return (live / Math.max(1, tot)) * ([...S.on].some((id) => ALL[id].cb1) ? 0.5 : 1);
    }
    // anatomy: head outline, brain, brainstem, ear, stomach
    const G = mk("g", {}, svg);
    mk("path", { d: "M200,40 C270,6 400,10 440,70 C470,110 470,160 440,190 L410,215 C380,230 330,236 300,232 L290,260 C285,276 270,282 258,276 C238,266 222,250 214,230 C180,210 170,150 176,110 C180,80 188,52 200,40Z", class: "vz-sc-brain" }, G);
    label(G, 360, 60, "Brain", { cls: "vz-sc-s" });
    mk("ellipse", { cx: 270, cy: 205, rx: 26, ry: 18, class: "vz-sc-vc" }, G);
    const vcGlow = mk("ellipse", { cx: 270, cy: 205, rx: 26, ry: 18, class: "vz-sc-vcg" }, G);
    label(G, 270, 239, "Vomiting center", { cls: "vz-sc-r" }); label(G, 270, 251, "(medulla)", { cls: "vz-sc-s" });
    mk("path", { d: "M480,160 c18,-10 34,4 30,22 c-3,14 -18,18 -26,10", class: "vz-sc-ear" }, G);
    label(G, 520, 150, "Inner ear", { cls: "vz-sc-s" });
    mk("path", { d: "M120,300 C110,330 140,360 180,352 C220,346 236,318 220,300 C206,286 186,300 170,296 C150,292 130,284 120,300Z", class: "vz-sc-stomach" }, G);
    label(G, 196, 372, "Stomach / gut", { cls: "vz-sc-s" });
    const food = mk("g", {}, G);
    const badges = {}, streams = {};
    Object.entries(IN).forEach(([k, inp]) => {
      mk("path", { d: `M${inp.path.map((p) => p.join(",")).join("L")}`, class: "vz-sc-nervep" }, G);
      label(G, inp.at[0] + (k === "ves" ? 46 : k === "gut" ? -60 : 0), inp.at[1] + (k === "cor" ? -14 : k === "ctz" ? -14 : 4), inp.name, { cls: "vz-sc-r", a: k === "gut" ? "end" : k === "ves" ? "start" : "middle" });
      inp.rec.forEach((r, j) => {
        if (r === "anx") return;
        const x = inp.at[0] + (j - (inp.rec.length - 1) / 2) * 44 + (k === "ctz" ? 0 : 0), y = inp.at[1] + (k === "ctz" ? -2 : 0) + (k === "gut" ? -30 : 0) + (k === "ves" ? 22 : 0);
        const g = mk("g", { class: "vz-sc-badge", transform: `translate(${x},${y})` }, G);
        mk("rect", { x: -20, y: -9, width: 40, height: 18, rx: 9 }, g);
        label(g, 0, 4, r.replace("5HT3", "5-HT3"), { cls: "vz-sc-bt" });
        const x2 = blocker(g, 16, -8, "var(--vz-2)"); x2.setAttribute("transform", "translate(16,-9) scale(.7)");
        badges[`${k}:${r}`] = { g, x: x2 };
      });
      if (k === "cor") { const x2 = blocker(G, inp.at[0] + 22, inp.at[1] + 8, "var(--vz-2)"); x2.setAttribute("transform", `translate(${inp.at[0] + 24},${inp.at[1] + 10}) scale(.7)`); badges["cor:anx"] = { g: mk("g", {}, G), x: x2 }; }
      streams[k] = stream(G, inp.path, { col: () => C.red, rate: 2.4, speed: 80, r: 3.6, jitter: 3 });
    });
    const cb1 = mk("g", { class: "vz-hide" }, G);
    mk("circle", { cx: 270, cy: 205, r: 34, class: "vz-sc-cb1" }, cb1); label(cb1, 306, 186, "CB1", { cls: "vz-sc-bt" });
    // nausea meter
    mk("rect", { x: 566, y: 230, width: 50, height: 120, rx: 12, class: "vz-sc-mtrack" }, svg);
    const fill = mk("rect", { x: 566, y: 230, width: 50, height: 120, rx: 12, class: "vz-sc-mfill red" }, svg);
    label(svg, 591, 222, "Nausea", { cls: "vz-sc-s" });
    let lv = 1, flash = 0;
    const foods = Array.from({ length: 6 }, (_, i) => ({ c: mk("circle", { r: 4, class: "vz-sc-food" }, food), t: i / 6 }));
    st.changed = () => {
      const S = st.S, bl = blockedSet(S);
      Object.entries(badges).forEach(([key, b]) => { show(b.x, bl.has(key)); b.g.classList.toggle("vz-dim", !TRIG[S.mode][key.split(":")[0]]); });
      show(cb1, [...S.on].some((id) => ALL[id].cb1));
    };
    st.recolor = () => { C = st.C; };
    st.tick = (dt) => {
      const S = st.S, bl = blockedSet(S), tr = TRIG[S.mode], cb = [...S.on].some((id) => ALL[id].cb1);
      Object.entries(IN).forEach(([k, inp]) => {
        const s = streams[k], rs = inp.rec.filter((r) => !bl.has(`${k}:${r}`)).length / inp.rec.length;
        s.on = !!tr[k]; s.rate = 2.6 * rs * (cb ? 0.5 : 1) + (tr[k] && rs === 0 ? 1.2 : 0); s.stop = tr[k] && rs === 0 ? 0.35 : null;
        s.tick(dt);
      });
      lv += (level(S) - lv) * Math.min(1, dt * 2.5);
      fill.setAttribute("y", 230 + 120 * (1 - lv)); fill.setAttribute("height", 120 * lv);
      flash += dt * 6; vcGlow.setAttribute("opacity", lv * (0.45 + 0.35 * Math.sin(flash)));
      const sp = S.on.has("meto") ? 0.5 : 0.18;
      foods.forEach((f) => { f.t = (f.t + dt * sp * 0.4) % 1; const a = f.t * Math.PI * 1.4; f.c.setAttribute("cx", 170 + Math.cos(a + 2) * 26 + f.t * 40); f.c.setAttribute("cy", 322 + Math.sin(a) * 12); f.c.setAttribute("opacity", f.t > 0.9 ? (1 - f.t) * 10 : 0.8); });
    };
    st.changed();
    return st;
  };
})();
