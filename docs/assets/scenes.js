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
    api.paint = paint; api._target = (id) => spec.target?.(id, S);
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
  V._stage = stage; V._k = { mk, stream, show, esc, label, blocker, cite, clamp, lerp, calm, pal };
})();

// ================================================================ shared icon library (simple line art, drawn in a color)
(function () {
  const V = window.dpasViz; if (!V || !V._k) return;
  const { mk, stream, show, esc, label, blocker, cite, clamp, lerp, calm } = V._k;
  const P = (d, c, w = 2, f = "none") => `<path d="${d}" fill="${f}" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
  const fillc = (c) => `color-mix(in srgb, ${c} 16%, var(--vz-bg))`;
  // each icon is drawn in a 40×40 box centered on 0,0
  const ICON = {
    enzyme: (c) => `<path d="M0,0 L17,-9 A19,19 0 1 0 17,9 Z" fill="${fillc(c)}" stroke="${c}" stroke-width="2"/><circle cx="-4" cy="-8" r="2.4" fill="${c}"/>`,
    receptor: (c) => P("M-14,-14 V4 Q-14,14 -4,14 M14,-14 V4 Q14,14 4,14", c, 3.2) + `<rect x="-20" y="12" width="40" height="7" rx="3.5" fill="${fillc(c)}" stroke="${c}" stroke-width="1.4"/>`,
    molecule: (c) => [[-9, 6], [0, -8], [9, 6], [12, -6]].map(([x, y], i, a) => (i ? P(`M${a[i - 1][0]},${a[i - 1][1]}L${x},${y}`, c, 1.6) : "") + `<circle cx="${x}" cy="${y}" r="5" fill="${fillc(c)}" stroke="${c}" stroke-width="1.6"/>`).join(""),
    cell: (c) => `<circle r="17" fill="${fillc(c)}" stroke="${c}" stroke-width="2"/><circle cx="4" cy="-3" r="6" fill="${c}" opacity=".5"/>`,
    effect: (c) => `<circle r="9" fill="${c}" opacity=".85"/>` + [0, 45, 90, 135, 180, 225, 270, 315].map((a) => { const r = (a * Math.PI) / 180; return P(`M${Math.cos(r) * 13},${Math.sin(r) * 13}L${Math.cos(r) * 18},${Math.sin(r) * 18}`, c, 2.2); }).join(""),
    liver: (c) => P("M-18,-4 C-16,-14 4,-16 18,-10 C20,-2 10,10 -4,12 C-12,12 -19,6 -18,-4Z", c, 2, fillc(c)) + P("M2,-13 C0,-4 2,4 -2,11", c, 1.4),
    kidney: (c) => P("M4,-17 C-12,-19 -17,-4 -14,8 C-11,18 4,19 8,10 C10,5 4,3 4,-2 C4,-7 10,-8 9,-13 C8,-16 6,-17 4,-17Z", c, 2, fillc(c)) + P("M6,-2 L16,-2", c, 2),
    heart: (c) => P("M0,16 C-22,2 -16,-16 -6,-14 C-2,-13 0,-9 0,-7 C0,-9 2,-13 6,-14 C16,-16 22,2 0,16Z", c, 2, fillc(c)),
    brain: (c) => P("M-16,4 C-20,-8 -10,-17 -2,-14 C4,-19 16,-14 16,-6 C21,0 16,12 6,12 C2,16 -6,15 -8,11 C-14,12 -18,9 -16,4Z", c, 2, fillc(c)) + P("M-6,-8 C-2,-4 -8,0 -2,4 M6,-8 C2,-2 8,2 4,8", c, 1.3),
    gut: (c) => P("M-14,-12 C-2,-18 16,-14 12,-4 C8,4 -10,-2 -12,6 C-14,14 4,16 14,12", c, 6.5) + P("M-14,-12 C-2,-18 16,-14 12,-4 C8,4 -10,-2 -12,6 C-14,14 4,16 14,12", "var(--vz-bg)", 3),
    stomach: (c) => P("M-6,-17 C-6,-6 -18,-2 -14,8 C-10,18 10,18 14,6 C16,-2 8,-6 4,-2 C2,-8 4,-14 4,-17", c, 2, fillc(c)),
    bone: (c) => P("M-12,-12 a4,4 0 1 1 5,-4 L7,8 a4,4 0 1 1 4,5 a4,4 0 1 1 -5,4 L-8,-7 a4,4 0 1 1 -4,-5Z", c, 2, fillc(c)),
    joint: (c) => P("M-14,-18 V-4 Q-14,2 -6,2 H6 Q14,2 14,-4 V-18 M-14,18 V8 Q-14,4 -8,4 M14,18 V8 Q14,4 8,4", c, 2.4),
    vessel: (c) => `<rect x="-19" y="-9" width="38" height="18" rx="9" fill="${fillc(c)}" stroke="${c}" stroke-width="2"/>` + [-10, 0, 10].map((x) => `<circle cx="${x}" cy="0" r="3" fill="${c}"/>`).join(""),
    nerve: (c) => P("M-18,0 H4", c, 2.6) + `<circle cx="10" cy="0" r="7" fill="${fillc(c)}" stroke="${c}" stroke-width="2"/>` + P("M-12,-6 L-6,0 L-12,6", c, 1.4),
    gland: (c) => P("M-14,10 C-18,-6 -8,-16 0,-16 C8,-16 18,-6 14,10 C10,16 -10,16 -14,10Z", c, 2, fillc(c)) + `<circle cx="-4" cy="0" r="2.5" fill="${c}"/><circle cx="5" cy="4" r="2.5" fill="${c}"/><circle cx="2" cy="-7" r="2.5" fill="${c}"/>`,
    thyroid: (c) => P("M-2,-4 C-6,-16 -18,-12 -16,2 C-15,12 -6,14 -2,6 Z M2,-4 C6,-16 18,-12 16,2 C15,12 6,14 2,6 Z", c, 2, fillc(c)),
    pancreas: (c) => P("M-18,4 C-14,-6 0,-6 8,-8 C16,-10 20,-2 16,4 C10,10 -10,12 -18,4Z", c, 2, fillc(c)),
    uterus: (c) => P("M-8,-10 C-8,6 -4,14 0,14 C4,14 8,6 8,-10 Z M-8,-10 C-14,-12 -18,-8 -18,-4 M8,-10 C14,-12 18,-8 18,-4", c, 2, fillc(c)),
    breast: (c) => P("M-16,-8 C-18,10 -2,16 6,10 C14,4 12,-8 4,-10", c, 2, fillc(c)) + `<circle cx="4" cy="2" r="2.4" fill="${c}"/>`,
    bladder: (c) => P("M-14,-6 C-16,-16 16,-16 14,-6 C12,6 6,10 3,12 V17 H-3 V12 C-6,10 -12,6 -14,-6Z", c, 2, fillc(c)),
    prostate: (c) => `<ellipse cx="0" cy="2" rx="15" ry="11" fill="${fillc(c)}" stroke="${c}" stroke-width="2"/>` + P("M0,-17 V17", c, 2.2),
    fat: (c) => [[-8, -6], [6, -8], [-6, 7], [8, 6]].map(([x, y]) => `<circle cx="${x}" cy="${y}" r="8" fill="${fillc(c)}" stroke="${c}" stroke-width="1.6"/>`).join(""),
    muscle: (c) => P("M-18,0 C-12,-12 12,-12 18,0 C12,12 -12,12 -18,0Z", c, 2, fillc(c)) + P("M-10,-4 H10 M-12,2 H12", c, 1.2),
    bug: (c) => P("M-14,0 Q-7,-8 0,0 T14,0", c, 4) + P("M14,0 q6,-5 10,-1", c, 1.2),
    drop: (c) => P("M0,-16 C6,-6 12,0 12,6 A12,12 0 0 1 -12,6 C-12,0 -6,-6 0,-16Z", c, 2, fillc(c)),
    shield: (c) => P("M0,-17 L14,-11 V0 C14,9 6,15 0,17 C-6,15 -14,9 -14,0 V-11Z", c, 2, fillc(c)),
    pill: (c) => `<rect x="-16" y="-7" width="32" height="14" rx="7" fill="${fillc(c)}" stroke="${c}" stroke-width="2"/>` + P("M0,-7 V7", c, 1.6),
    clock: (c) => `<circle r="15" fill="${fillc(c)}" stroke="${c}" stroke-width="2"/>` + P("M0,-9 V0 L7,5", c, 2),
    lungs: (c) => P("M-3,-14 V0 M-3,-4 C-8,-8 -18,-4 -16,8 C-14,16 -6,14 -4,8 Z M3,-14 V0 M3,-4 C8,-8 18,-4 16,8 C14,16 6,14 4,8 Z", c, 2, fillc(c)),
  };
  const RULES = [
    [/membrane|phospholipid/i, "cell"],
    [/cox|enzyme|ase\b|ase |reductase|oxidase|dhfr|dhodh|cyp|aromatase|synthase|kinase|ace\b|\(ace\)|renin|pde5|vkor|guanylate|tpo|organification|hydroxylase|conjugation|glucuronid|sulfation|uricase|plc|phospholipase/i, "enzyme"],
    [/receptor|\bR\b|\bAT1\b|\bGR\b|\bMR\b|\bER\b|D2|5-HT|nk1|h1|m3|alpha|beta|casr|ksatp|k-atp|channel|sglt|ncc|nkcc|enac|transporter|urat|integrin|α4β7|cd20|cd28/i, "receptor"],
    [/liver|hepat|gluconeo/i, "liver"], [/kidney|renal|nephr|glomer|urine|tubul|duct|creatinine|gfr/i, "kidney"], [/heart|cardi|afterload|preload|contractil|heart rate/i, "heart"],
    [/brain|cns|central|hypothal|cortex|ctz|spinal|brainstem|psych|confusion/i, "brain"], [/pituitary|somatotroph|lactotroph/i, "gland"], [/thyroid/i, "thyroid"], [/adrenal|cortisol/i, "gland"],
    [/stomach|gastric|parietal/i, "stomach"], [/gut|bowel|colon|intestin|ileum|lumen|stool|peristal|enteric|mucosa|diarrhea/i, "gut"], [/bone|osteo|fracture/i, "bone"], [/joint|synov|cartilage|arthr/i, "joint"],
    [/vessel|arteriol|vaso|blood pressure|\bbp\b|vascular|venodil|plasma volume|hypotension|syncope/i, "vessel"], [/nerve|neuron|vagus|motor|sympath|parasymp|nanc|acetylcholine released|norepinephrine/i, "nerve"],
    [/pancrea|β-cell|beta-cell|insulin/i, "pancreas"], [/uter|endometri|ovar|ovulat|follicle|lining|cervical/i, "uterus"], [/breast/i, "breast"], [/prostate/i, "prostate"], [/bladder|detrusor|outlet|storage|urgency/i, "bladder"],
    [/fat|adipose/i, "fat"], [/muscle|contraction|tone|spasm/i, "muscle"], [/infect|bacteri|tb\b|h\. pylori/i, "bug"], [/inr|bleed|clot|platelet|txa/i, "drop"], [/pain|inflam|fever|swelling|erosion|damage|toxicity|necrosis|ulcer|injury|risk|aki|cancer|hyperplasia/i, "effect"],
    [/protect|defense|barrier|mucus|glutathione|nac\b|safe/i, "shield"], [/tablet|dose|drug|pill/i, "pill"], [/cell|lymphocyte|t-cell|b cells|neutrophil|macrophage/i, "cell"],
  ];
  const iconFor = (n) => n.icon || (RULES.find(([re]) => re.test(n.label.replace(/\n/g, " "))) || [, n.glyph === "membrane" ? "cell" : n.glyph === "enzyme" ? "enzyme" : n.glyph === "cell" ? "cell" : n.glyph === "effect" ? "effect" : "molecule"])[1];
  V._icons = { ICON, iconFor };

  // ================================================================ FACTORY: the labelled pathway, drawn as a working machine
  // Same config as "pathway" (nodes, edges, drugs with at/off/less, point, read). Each step gets an icon; molecules flow
  // along the arrows; a drug docks where it acts (molecules pile up behind it) and the end result's gauge drains.
  V.factory = (host, cfg = {}) => {
    const N = (cfg.nodes || []).map((n) => ({ w: 130, col: "teal", ...n })), E = cfg.edges || [], D = cfg.drugs || [];
    const COLV = { teal: "var(--vz-1)", coral: "var(--vz-2)", amber: "var(--vz-3)", blue: "var(--vz-4)", sage: "var(--vz-5)", deep: "var(--vz-text)", ink: "var(--vz-ink)" };
    const narrow = (host.clientWidth || 640) < 560, NH = narrow ? 78 : 62;
    let h = (cfg.h || 300) + 24;
    const by = Object.fromEntries(N.map((n) => [n.id, n]));
    if (narrow) {  // phones: re-stack top to bottom by step, at most two per row
      const rank = Object.fromEntries(N.map((n) => [n.id, 0]));
      for (let k = 0; k < N.length; k++) E.forEach(([a, b]) => (rank[b] = Math.max(rank[b], rank[a] + 1)));
      const byR = []; N.forEach((n) => (byR[rank[n.id]] ||= []).push(n.id));
      const rows = byR.filter(Boolean).flatMap((ids) => ids.length > 2 ? Array.from({ length: Math.ceil(ids.length / 2) }, (_, k) => ids.slice(2 * k, 2 * k + 2)) : [ids]);
      rows.forEach((ids, r) => { const w = (640 - 28 - (ids.length - 1) * 24) / ids.length; ids.forEach((id, j) => Object.assign(by[id], { x: 14 + j * (w + 24), y: 18 + r * (NH + 70), w })); });
      h = 36 + rows.length * (NH + 70) - 70;
    }
    const outs = new Set(E.map((e) => e[0])), terminal = N.filter((n) => !outs.has(n.id)).map((n) => n.id);
    const drugs = D.map((d, i) => ({ id: `d${i}`, label: d.label, note: d.note, col: ["var(--vz-1)", "var(--vz-2)", "var(--vz-4)", "var(--vz-3)", "var(--vz-5)"][i % 5], src: d }));
    const ctr = (n) => [n.x + n.w / 2, n.y + NH / 2];
    const link = (A, B) => {
      const [ax, ay] = ctr(A), [bx, by2] = ctr(B), g = 6;
      if (Math.abs(by2 - ay) < NH) { const s = Math.sign(bx - ax), x1 = ax + s * (A.w / 2 + g), x2 = bx - s * (B.w / 2 + g); return [[x1, ay], [(x1 + x2) / 2, ay], [(x1 + x2) / 2, by2], [x2, by2]]; }
      const s = Math.sign(by2 - ay), y1 = ay + s * (NH / 2 + g), y2 = by2 - s * (NH / 2 + g); return [[ax, y1], [ax, (y1 + y2) / 2], [bx, (y1 + y2) / 2], [bx, y2]];
    };
    const st = V._stage(host, {
      h, drugs, label: cfg.title || "pathway", point: cfg.point, hint: "Drag a drug onto the picture, or tap it",
      target: (id) => { const d = drugs.find((x) => x.id === id).src; if (!d.at) return [320, h / 2]; if (d.at.includes(">")) { const [a, b] = d.at.split(">"); const pts = link(by[a], by[b]); return pts[1].map((v, k) => (v + pts[2][k]) / 2); } return by[d.at] ? ctr(by[d.at]) : [320, h / 2]; },
      read(S) {
        const d = drugs.find((x) => S.on.has(x.id));
        const lv = terminal.map((id) => `${by[id].label.replace(/\n/g, " ")}: <b>${Math.round(level(S, id) * 100)}%</b>`).join(" · ");
        return `${d ? `<b>${esc(d.label)}.</b> ${d.note || ""}` : esc(cfg.read || "Drag a drug onto the picture to see where it acts and what goes quiet downstream.")}${d ? `<span class="vz-meter-t">${lv}</span>` : ""}`;
      },
    });
    const { svg } = st;
    const cur = (S) => drugs.find((x) => S.on.has(x.id))?.src;
    // "on": a step the drug sets in motion (its label already says which way things go), shown lit rather than as more/less
    const isOn = (S, id) => (cur(S)?.on || []).includes(id);
    function level(S, id) { const d = cur(S); if (!d) return 1; return (d.off || []).includes(id) ? 0.12 : (d.less || []).includes(id) ? 0.55 : 1; }
    const L = { lines: mk("g", {}, svg), flow: mk("g", {}, svg), nodes: mk("g", {}, svg), top: mk("g", {}, svg) };
    const streams = E.map(([a, b]) => {
      const pts = link(by[a], by[b]);
      mk("path", { d: `M${pts[0]}C${pts[1]} ${pts[2]} ${pts[3]}`, class: "vz-fx-line" }, L.lines);
      const arrow = mk("path", { d: "M-5,-4L1,0L-5,4", class: "vz-fx-arrow", transform: `translate(${pts[3][0]},${pts[3][1]}) rotate(${Math.atan2(pts[3][1] - pts[2][1], pts[3][0] - pts[2][0]) * 180 / Math.PI})` }, L.lines);
      // sample the cubic into a polyline for the particles
      const cub = (t) => [0, 1].map((k) => (1 - t) ** 3 * pts[0][k] + 3 * (1 - t) ** 2 * t * pts[1][k] + 3 * (1 - t) * t * t * pts[2][k] + t ** 3 * pts[3][k]);
      const poly = Array.from({ length: 13 }, (_, i) => cub(i / 12));
      const col = COLV[by[a].col] || "var(--vz-1)";
      return { a, b, s: stream(L.flow, poly, { col: () => getComputedStyle(st.el).getPropertyValue(col.slice(4, -1)) || "#888", rate: 1.8, speed: 55, r: narrow ? 4.4 : 3.4, jitter: 2 }), arrow };
    });
    const NODE = N.map((n) => {
      const col = COLV[n.col] || "var(--vz-1)", g = mk("g", { class: "vz-fx-node", transform: `translate(${n.x},${n.y})` }, L.nodes);
      const term = terminal.includes(n.id), r = NH / 2;
      mk("rect", { width: n.w, height: NH, rx: 18, class: "vz-fx-card", style: `--c:${col}` }, g);
      const ic = mk("g", { transform: `translate(${r},${r}) scale(${narrow ? 1.05 : 0.9})` }, g); ic.innerHTML = ICON[iconFor(n)](col);
      const ls = String(n.label).split("\n"), tx = r * 2 + (n.w - r * 2) / 2 - 2;
      const t = mk("text", { x: tx, y: r, "text-anchor": "middle", class: `vz-fx-t${narrow ? " lg" : ""}` }, g);
      ls.forEach((l, i) => { const sp = mk("tspan", { x: tx, dy: i ? "1.15em" : `${0.35 - (ls.length - 1) * 0.58}em` }, t); sp.textContent = l; });
      let ring = null;
      if (term) {  // the end result: a gauge that drains when the pathway is cut
        const gx = n.w - 2, gy = -2;
        mk("circle", { cx: gx, cy: gy, r: 13, class: "vz-fx-gt" }, g);
        ring = mk("circle", { cx: gx, cy: gy, r: 13, class: "vz-fx-gr", "stroke-dasharray": `${2 * Math.PI * 13}`, transform: `rotate(-90 ${gx} ${gy})` }, g);
        ring.lv = 1; ring.txt = mk("text", { x: gx, y: gy + 3.5, "text-anchor": "middle", class: "vz-fx-gp" }, g);
      }
      const badge = mk("text", { x: n.w - 10, y: NH - 8, "text-anchor": "end", class: "vz-fx-down" }, g);
      return { n, g, ring, badge };
    });
    const dock = mk("g", { class: "vz-hide" }, L.top);
    const dockPill = mk("rect", { x: -18, y: -9, width: 36, height: 18, rx: 9, class: "vz-fx-dock" }, dock);
    mk("path", { d: "M-5,-5L5,5M5,-5L-5,5", stroke: "#fff", "stroke-width": 2.6, "stroke-linecap": "round" }, dock);
    st.changed = () => {
      const S = st.S, d = cur(S), dd = drugs.find((x) => S.on.has(x.id));
      NODE.forEach(({ n, g, badge }) => { const lv = level(S, n.id); g.style.opacity = lv < 0.2 ? 0.42 : lv < 1 ? 0.75 : 1; badge.textContent = lv < 1 ? (lv < 0.2 ? "↓↓" : "↓") : ""; });
      show(dock, !!d?.at);
      if (d?.at) { const [x, y] = st._target(dd.id); dock.setAttribute("transform", `translate(${x},${y})`); dockPill.style.fill = dd.col; }
      streams.forEach((s) => {
        const cut = d && (d.at === `${s.a}>${s.b}` || d.at === s.b);
        const quiet = d && ((d.off || []).includes(s.a) || (d.off || []).includes(s.b));
        s.s.stop = cut ? 0.72 : null; s.s.rate = quiet && !cut ? 0.25 : (d?.less || []).includes(s.b) ? 0.9 : 1.8;
      });
    };
    st.tick = (dt) => {
      streams.forEach((s) => s.s.tick(dt));
      NODE.forEach(({ n, ring }) => {
        if (!ring) return;
        const t = level(st.S, n.id); ring.lv += (t - ring.lv) * Math.min(1, dt * 3);
        ring.setAttribute("stroke-dashoffset", `${2 * Math.PI * 13 * (1 - ring.lv)}`); ring.txt.textContent = `${Math.round(ring.lv * 100)}`;
      });
    };
    st.changed();
    return st;
  };
})();

// ================================================================ organ-level scenes
(function () {
  const V = window.dpasViz; if (!V || !V._k || !V._icons) return;
  const { mk, stream, show, esc, label, blocker, cite, clamp, lerp, calm } = V._k, { ICON, iconFor } = V._icons;
  const W = 640;
  const drugList = (ds) => ds.map((d, i) => ({ col: ["var(--vz-1)", "var(--vz-2)", "var(--vz-4)", "var(--vz-3)", "var(--vz-5)"][i % 5], ...d }));
  const noteOf = (S, drugs) => { const d = drugs.find((x) => x.id === S.last) || drugs.find((x) => S.on.has(x.id)); return d ? `<b>${esc(d.label)}.</b> ${d.note || ""} ` : ""; };
  const bar = (g, x, y, w, h, title) => {
    label(g, x + w / 2, y - 8, title, { cls: "vz-sc-s" });
    mk("rect", { x, y, width: w, height: h, rx: Math.min(w, h) / 2, class: "vz-sc-mtrack" }, g);
    const f = mk("rect", { x, y, width: w, height: h, rx: Math.min(w, h) / 2, class: "vz-sc-mfill" }, g);
    const t = mk("text", { x: x + w / 2, y: y + h + 15, "text-anchor": "middle", class: "vz-sc-s" }, g);
    let v = 0.5;
    return { set(target, dt, txt, col) { v += (target - v) * Math.min(1, dt * 3); const hh = h * clamp(v, 0, 1); f.setAttribute("y", y + h - hh); f.setAttribute("height", hh); if (col) f.style.fill = col; t.textContent = txt; } };
  };
  const icon = (g, name, x, y, col, s = 1) => { const e = mk("g", { transform: `translate(${x},${y}) scale(${s})` }, g); e.innerHTML = ICON[name](col); return e; };

  // ---------------------------------------------------------------- NEPHRON: anatomical nephron (cortex/medulla), transporters where they sit
  // cfg: {segments:[{id:pt|tal|dct|cd,label,frac,tr}], drugs:[{id,label,seg,k,ca,glu,water,fe,note}], show:["na","k","ca","glu","water"]}
  // Na⁺ in urine accounts for downstream compensation: block the proximal tubule and the loop recaptures most of it.
  const hbar = (g, x, y, w, title) => {
    label(g, x, y, title, { a: "start", cls: "vz-sc-r" });
    mk("rect", { x, y: y + 7, width: w, height: 9, rx: 4.5, class: "vz-sc-mtrack" }, g);
    const f = mk("rect", { x, y: y + 7, width: 0, height: 9, rx: 4.5, class: "vz-sc-mfill" }, g);
    const t = label(g, x, y + 32, "", { a: "start", cls: "vz-sc-s" });
    let v = 0.5;
    return { set(target, dt, txt, col) { v += (target - v) * Math.min(1, dt * 3); f.setAttribute("width", w * clamp(v, 0.02, 1)); f.style.fill = col || ""; t.textContent = txt; } };
  };
  V.nephron = (host, cfg = {}) => {
    const H = 440;
    const SEG = cfg.segments || [{ id: "pt", label: "Proximal tubule", frac: 0.65, tr: "" }, { id: "tal", label: "Thick ascending limb", frac: 0.25, tr: "" }, { id: "dct", label: "Distal tubule", frac: 0.07, tr: "" }, { id: "cd", label: "Collecting duct", frac: 0.03, tr: "" }];
    const PASS = { pt: 0.08, tal: 0.85, dct: 0.9, cd: 1 };  // share of the extra Na⁺ that escapes recapture downstream
    const drugs = drugList(cfg.drugs || []), showM = cfg.show || ["na", "k", "ca"];
    const siteOf = (d) => (d.seg === "sglt2" ? "pt" : d.seg);
    const st = V._stage(host, {
      h: H, drugs, multi: !!cfg.multi, label: "Nephron: cortex to medulla, with each diuretic's transporter", point: cfg.point, hint: "Drag a drug onto the nephron, or tap it", steps: cfg.steps,
      target: (id) => { const d = drugs.find((x) => x.id === id); return SITE[siteOf(d)] || [240, 200]; },
      read(S) {
        const m = model(S), bits = [];
        if (showM.includes("na")) bits.push(`Na⁺ in urine: <b>${m.naTxt}</b>`);
        if (showM.includes("water")) bits.push(`Urine water: <b>${m.waterTxt}</b>`);
        if (showM.includes("k")) bits.push(`Serum K⁺: <b>${m.kTxt}</b>`);
        if (showM.includes("ca")) bits.push(`Urine Ca²⁺: <b>${m.caTxt}</b>`);
        if (showM.includes("glu")) bits.push(`Urine glucose: <b>${m.gluTxt}</b>`);
        return `${noteOf(S, drugs) || esc(cfg.read || "Each segment pulls sodium back into the peritubular capillary. Block a segment's transporter and that sodium — and the water that follows it — stays in the urine.")}<span class="vz-meter-t">${bits.join(" · ")}</span>`;
      },
    });
    const { svg } = st;
    const naBlocked = (S) => new Set(drugs.filter((d) => S.on.has(d.id) && d.seg !== "sglt2").map((d) => d.seg));
    function model(S) {
      const on = drugs.filter((d) => S.on.has(d.id)), bl = naBlocked(S);
      let na = 0.01;
      SEG.forEach((sg) => { if (bl.has(sg.id)) { const d = on.find((x) => x.seg === sg.id && x.fe != null); na += d ? d.fe : sg.frac * (PASS[sg.id] ?? 1); } });
      na = clamp(na, 0.01, 1);
      const k = on.reduce((a, d) => a + (d.k || 0), 0), ca = on.reduce((a, d) => a + (d.ca || 0), 0), glu = on.some((d) => d.glu), water = on.reduce((a, d) => a + (d.water || 0), 0);
      const naTxt = na < 0.02 ? "~1% (normal)" : `~${Math.round(na * 100)}%`;
      return { na, k, ca, glu, water, naTxt, kTxt: k < 0 ? "falls (K⁺ lost)" : k > 0 ? "rises (K⁺ kept)" : "normal", caTxt: ca > 0 ? "up" : ca < 0 ? "down (Ca²⁺ kept)" : "normal",
        gluTxt: glu ? "glucose spills" : "none", waterTxt: water > 0 ? "less (concentrated)" : water < 0 ? "more water lost" : na > 0.1 ? "more" : "normal" };
    }
    // ---- anatomy: cortex / medulla, glomerulus in Bowman's capsule, PCT → thin descending → hairpin → thin ascending → TAL → macula densa → DCT → collecting duct
    const g0 = mk("g", {}, svg);
    mk("rect", { x: 0, y: 0, width: 470, height: 196, rx: 16, class: "vz-nx-cortex" }, g0);
    mk("rect", { x: 0, y: 196, width: 470, height: H - 196, rx: 16, class: "vz-nx-medulla" }, g0);
    label(g0, 462, 188, "CORTEX", { a: "end", cls: "vz-nx-zone" }); label(g0, 462, 214, "MEDULLA", { a: "end", cls: "vz-nx-zone" });
    const path = [[176, 86], [154, 66], [134, 92], [114, 64], [94, 92], [76, 84], [62, 110], [62, 384], [92, 408], [122, 384], [122, 300], [122, 150], [134, 124], [160, 114],
      [212, 112], [236, 92], [262, 122], [288, 92], [314, 120], [340, 100], [372, 100], [372, 420]];
    const IDX = { pt: [1, 6], tal: [10, 12], dct: [14, 19], cd: [20, 21] };
    const d = `M${path.map((p) => p.join(",")).join("L")}`;
    // peritubular capillary running beside the tubule (where reabsorbed ions go)
    mk("path", { d: "M44,100 L44,372 M140,160 L140,330 M210,130 C250,142 300,142 350,130 M388,112 L388,404", class: "vz-nx-ptc" }, g0);
    mk("path", { d: "M200,6 L200,44", class: "vz-nx-art" }, g0);
    label(g0, 208, 22, "afferent arteriole", { a: "start", cls: "vz-sc-s" });
    mk("path", { d, class: "vz-nx-tube" }, g0);
    mk("path", { d: "M122,300 L122,150 L134,124 L160,114", class: "vz-nx-thick" }, g0);  // TAL: thicker epithelium
    mk("path", { d, class: "vz-nx-lumen" }, g0);
    mk("circle", { cx: 200, cy: 72, r: 30, class: "vz-nx-bowman" }, g0);
    for (let i = 0; i < 6; i++) mk("circle", { cx: 200 + Math.cos(i * 1.05) * 11, cy: 70 + Math.sin(i * 1.05) * 11, r: 7, class: "vz-nx-cap" }, g0);
    mk("ellipse", { cx: 166, cy: 106, rx: 9, ry: 5, class: "vz-nx-md" }, g0);
    label(g0, 236, 62, "Glomerulus", { a: "start", cls: "vz-sc-s" });
    label(g0, 176, 154, "macula densa", { a: "middle", cls: "vz-sc-m" });
    label(g0, 372, H - 4, "→ urine", { a: "start", cls: "vz-sc-h" });
    label(g0, 30, 300, "thin descending limb", { a: "middle", cls: "vz-sc-m" }).setAttribute("transform", "rotate(-90 30 300)");
    // transporter sites + labels
    const SITE = { pt: [114, 64], tal: [122, 236], dct: [288, 92], cd: [372, 290] };
    const LAB = { pt: [100, 30, "middle"], tal: [142, 230, "start"], dct: [300, 168, "middle"], cd: [358, 330, "end"] };
    const X = {};
    SEG.forEach((sg) => {
      const [sx, sy] = SITE[sg.id] || [240, 200];
      mk("rect", { x: sx - 9, y: sy - 6, width: 18, height: 12, rx: 6, class: "vz-nx-site" }, g0);
      const [lx, ly, an] = LAB[sg.id] || [240, 20, "middle"];
      label(g0, lx, ly, sg.label, { cls: "vz-sc-r", a: an });
      label(g0, lx, ly + 14, `${sg.tr ? sg.tr + " · " : ""}~${Math.round(sg.frac * 100)}% of Na⁺`, { cls: "vz-sc-s", a: an });
      X[sg.id] = blocker(g0, sx, sy, "var(--vz-2)");
    });
    // ---- flowing filtrate: Na⁺ (blue) and glucose (amber); reabsorbed ions hop into the capillary
    const flow = mk("g", {}, svg), ps = [], segLen = []; let tot = 0;
    for (let i = 1; i < path.length; i++) { const l = Math.hypot(path[i][0] - path[i - 1][0], path[i][1] - path[i - 1][1]); segLen.push(l); tot += l; }
    const posAt = (dd) => { let k = 0; while (k < segLen.length - 1 && dd > segLen[k]) { dd -= segLen[k]; k++; } const t = clamp(dd / segLen[k], 0, 1); return { k, p: [lerp(path[k][0], path[k + 1][0], t), lerp(path[k][1], path[k + 1][1], t)] }; };
    const urine = mk("g", {}, svg);
    // ---- readout panel (horizontal bars; never overlaps the anatomy)
    const bars = mk("g", {}, svg), M = {};
    let by = 40;
    const mtr = (key, title) => { if (!showM.includes(key)) return; M[key] = hbar(bars, 488, by, 140, title); by += 62; };
    mtr("na", "Na⁺ in urine"); mtr("water", "Urine water"); mtr("k", "Serum K⁺"); mtr("ca", "Urine Ca²⁺"); mtr("glu", "Urine glucose");
    st.changed = () => { const on = drugs.filter((dd) => st.S.on.has(dd.id)); SEG.forEach((sg) => show(X[sg.id], on.some((dd) => siteOf(dd) === sg.id))); };
    st.tick = (dt) => {
      const S = st.S, m = model(S), bl = naBlocked(S);
      if (Math.random() < dt * 9) ps.push({ d: 0, c: mk("circle", { r: 3.4, class: "vz-nx-na" }, flow), out: null, glu: showM.includes("glu") && Math.random() < 0.35 });
      for (let i = ps.length - 1; i >= 0; i--) {
        const p = ps[i];
        if (p.out) { p.out.t += dt * 1.8; p.c.setAttribute("cx", lerp(p.out.x, p.out.tx, p.out.t)); p.c.setAttribute("cy", lerp(p.out.y, p.out.ty, p.out.t)); p.c.setAttribute("opacity", 1 - p.out.t); if (p.out.t >= 1) { p.c.remove(); ps.splice(i, 1); } continue; }
        p.d += dt * 120;
        const { k, p: xy } = posAt(p.d);
        p.c.setAttribute("cx", xy[0]); p.c.setAttribute("cy", xy[1]);
        if (p.glu) p.c.setAttribute("class", "vz-nx-glu");
        for (const sg of SEG) {
          const [a, b] = IDX[sg.id] || [1, 2];
          if (k >= a && k < b && !p[sg.id]) {
            p[sg.id] = 1;
            // remaining share of filtered Na⁺ at this point, so each segment takes its taught fraction; a blocked segment lets most of it pass,
            // and later segments recapture part (compensation)
            const left = SEG.slice(SEG.indexOf(sg)).reduce((s2, x) => s2 + x.frac, 0) + 0.01;
            let keep = p.glu ? (sg.id === "pt" && !m.glu ? 1 : 0) : bl.has(sg.id) ? 0 : sg.frac / left;
            if (!p.glu && !bl.has(sg.id) && sg.id === "tal" && bl.has("pt")) keep = Math.min(1, keep * 1.35);
            if (Math.random() < keep) { const off = sg.id === "cd" ? [14, 0] : sg.id === "dct" ? [0, 20] : sg.id === "tal" ? [12, 0] : [-12, 10]; p.out = { t: 0, x: xy[0], y: xy[1], tx: xy[0] + off[0], ty: xy[1] + off[1] }; break; }
          }
        }
        if (p.d >= tot) { p.c.remove(); ps.splice(i, 1); const u = mk("circle", { cx: 372 + (Math.random() - 0.5) * 16, cy: H - 16 + Math.random() * 6, r: 3, class: p.glu ? "vz-nx-glu" : "vz-nx-na" }, urine); setTimeout(() => u.remove(), 900); }
      }
      M.na?.set(clamp(m.na * 3.5, 0.03, 1), dt, m.naTxt);
      M.water?.set(m.water > 0 ? 0.15 : m.water < 0 ? 0.9 : clamp(m.na * 3.5, 0.05, 1), dt, m.waterTxt);
      M.k?.set(0.5 + m.k * 0.3, dt, m.kTxt, m.k < 0 ? "var(--vz-3)" : m.k > 0 ? "var(--vz-2)" : "");
      M.ca?.set(0.5 + m.ca * 0.3, dt, m.caTxt);
      M.glu?.set(m.glu ? 0.85 : 0.04, dt, m.gluTxt);
    };
    st.changed();
    return st;
  };

  // ---------------------------------------------------------------- GLOMERULUS: inflow, outflow, volume → filtration pressure
  V.glomerulus = (host, cfg = {}) => {
    const H = 330, drugs = drugList(cfg.drugs || []);
    const st = V._stage(host, {
      h: H, drugs, multi: true, label: "Glomerulus", point: cfg.point, hint: "Add drugs one by one and watch the pressure", steps: cfg.steps,
      target: (id) => { const d = drugs.find((x) => x.id === id); return d.aff ? [130, 150] : d.eff ? [500, 150] : [320, 70]; },
      read(S) { const m = model(S); return `${noteOf(S, drugs) || esc(cfg.read || "")}<span class="vz-meter-t">Filtration pressure: <b>${Math.round(m.p * 100)}%</b>${m.p < 0.45 ? " — <b>AKI risk</b>" : ""}${cfg.protein ? ` · Proteinuria: <b>${m.prot ? "less" : "baseline"}</b>` : ""}</span>`; },
    });
    const { svg } = st;
    function model(S) {
      const on = drugs.filter((d) => S.on.has(d.id));
      const aff = on.reduce((a, d) => a * (d.aff || 1), 1), eff = on.reduce((a, d) => a * (d.eff || 1), 1), vol = on.reduce((a, d) => a * (d.vol || 1), 1);
      const p = clamp(vol * aff / Math.pow(eff, 0.9), 0.05, 1.2);
      return { aff, eff, vol, p, prot: eff > 1.05 };
    }
    const g = mk("g", {}, svg);
    mk("path", { d: "M300,80 C210,80 200,250 300,270 C420,290 460,120 380,84 C360,76 330,76 300,80Z", class: "vz-gl-caps" }, g);
    label(g, 330, 300, "Bowman’s capsule → filtrate to the tubule", { cls: "vz-sc-s" });
    const affR = mk("rect", { x: 20, y: 150, width: 230, height: 30, rx: 15, class: "vz-gl-vessel" }, g);
    const effR = mk("rect", { x: 400, y: 150, width: 220, height: 30, rx: 15, class: "vz-gl-vessel" }, g);
    label(g, 120, 140, "Afferent arteriole (in)", { cls: "vz-sc-r" }); label(g, 520, 140, "Efferent arteriole (out)", { cls: "vz-sc-r" });
    const tuft = mk("g", {}, g);
    for (let i = 0; i < 7; i++) mk("circle", { cx: 320 + Math.cos(i) * 34, cy: 170 + Math.sin(i * 1.4) * 28, r: 18, class: "vz-gl-loop" }, tuft);
    const gauge = mk("g", { transform: "translate(320,62)" }, svg);
    mk("path", { d: "M-46,0 A46,46 0 0 1 46,0", class: "vz-gl-gt" }, gauge);
    const needle = mk("path", { d: "M0,0 L0,-40", class: "vz-gl-needle" }, gauge);
    mk("circle", { r: 5, class: "vz-gl-hub" }, gauge);
    label(gauge, 0, 18, "Filtration pressure", { cls: "vz-sc-s" });
    const aki = label(svg, 320, 112, "AKI", { cls: "vz-sc-h vz-sc-red" });
    const blood = stream(svg, [[20, 165], [250, 165], [300, 172], [340, 168], [400, 165], [620, 165]], { col: () => st.C.red, rate: 6, speed: 110, r: 3.6, jitter: 7 });
    const filt = stream(svg, [[320, 200], [325, 240], [330, 286]], { col: () => st.C.amber, rate: 3, speed: 60, r: 3, jitter: 10 });
    let pv = 1;
    st.tick = (dt) => {
      const m = model(st.S);
      pv += (m.p - pv) * Math.min(1, dt * 2.5);
      affR.setAttribute("height", 30 * clamp(m.aff, 0.35, 1.4)); affR.setAttribute("y", 165 - 15 * clamp(m.aff, 0.35, 1.4));
      effR.setAttribute("height", 30 * clamp(m.eff, 0.6, 1.6)); effR.setAttribute("y", 165 - 15 * clamp(m.eff, 0.6, 1.6));
      blood.rate = 6 * m.vol * m.aff; blood.tick(dt);
      filt.rate = 5 * pv; filt.tick(dt);
      needle.setAttribute("transform", `rotate(${-80 + 160 * clamp(pv / 1.2, 0, 1)})`);
      aki.setAttribute("opacity", pv < 0.45 ? 1 : 0);
    };
    st.changed = () => {};
    return st;
  };

  // ---------------------------------------------------------------- AXIS: hypothalamus → pituitary → gland → hormone, with negative feedback
  // cfg: {axes:[{id,label,top,topH,mid,midH,gland,glandIcon,hormone,effect,brake}], drugs:[{id,label,kind,axis,amt,note}]}
  // kinds: exo (adds hormone), synth (gland can't make it), receptor (tissue blocked), pit (pituitary release ↓), agonist (more brake/less release), inducer (exo ↓), taper (exo fades slowly)
  V.axis = (host, cfg = {}) => {
    const H = 400, AX = cfg.axes, drugs = drugList(cfg.drugs || []);
    const st = V._stage(host, {
      h: H, drugs, multi: true, label: "Hormone axis", point: cfg.point, hint: "Add a drug and watch the feedback loop respond", steps: cfg.steps,
      modes: AX.length > 1 ? { label: "Axis", opts: AX.map((a) => [a.id, a.label]) } : null, start: { mode: AX[0].id },
      target: (id) => { const d = drugs.find((x) => x.id === id); return d.kind === "exo" || d.kind === "inducer" || d.kind === "taper" ? [250, 280] : d.kind === "synth" ? [250, 240] : d.kind === "receptor" ? [470, 300] : [250, 150]; },
      read(S) {
        const a = ax(S), m = sim.cur;
        const lv = (v) => (v > 1.25 ? "high" : v < 0.6 ? (v < 0.25 ? "very low" : "low") : "normal");
        return `${noteOf(S, drugs) || esc(cfg.read || "Each level drives the next; the final hormone switches the top two off — negative feedback.")}<span class="vz-meter-t">${a.topH}: <b>${lv(m.top)}</b> · ${a.midH}: <b>${lv(m.mid)}</b>${a.brake ? "" : m.exo > 0.1 ? ` · ${a.hormone} + drug: <b>${lv(m.hor)}</b> · made by the ${String(a.gland).toLowerCase()}: <b>${lv(m.made ?? 1)}</b>` : ` · ${a.hormone}: <b>${lv(m.hor)}</b>`}${m.gland < 0.7 ? ` · ${a.gland}: <b>shrunken</b>` : ""}${m.hor < 0.4 && m.gland < 0.7 && !drugs.some((d) => S.on.has(d.id) && (d.kind === "exo")) ? " — <b>crisis risk</b>" : ""}</span>`;
      },
    });
    const { svg } = st;
    const ax = (S) => AX.find((a) => a.id === S.mode) || AX[0];
    const act = (S) => drugs.filter((d) => S.on.has(d.id) && (!d.axis || d.axis === ax(S).id));
    const sim = { cur: { top: 1, mid: 1, hor: 1, gland: 1, exo: 0, eff: 1 }, taperT: 0 };
    // drawing
    const g = mk("g", {}, svg), dyn = mk("g", {}, svg);
    const T = { y: 60 }, Mi = { y: 160 }, G = { y: 265 }, X = 250;
    const brainI = mk("g", { transform: `translate(${X},${T.y}) scale(1.6)` }, g);
    const pitI = mk("g", { transform: `translate(${X},${Mi.y}) scale(1.3)` }, g);
    const glandI = mk("g", { transform: `translate(${X},${G.y}) scale(1.5)` }, g);
    const tLab = label(g, X - 52, T.y + 4, "", { a: "end", cls: "vz-sc-r" }), mLab = label(g, X - 52, Mi.y + 4, "", { a: "end", cls: "vz-sc-r" }), gLab = label(g, X - 52, G.y + 4, "", { a: "end", cls: "vz-sc-r" });
    const s1 = stream(dyn, [[X, T.y + 26], [X, Mi.y - 24]], { col: () => st.C.blue, rate: 3, speed: 50, r: 3.4, jitter: 6 });
    const s2 = stream(dyn, [[X, Mi.y + 22], [X, G.y - 28]], { col: () => st.C.purple, rate: 3, speed: 50, r: 3.4, jitter: 6 });
    const s3 = stream(dyn, [[X + 30, G.y + 6], [400, G.y + 30], [450, 300]], { col: () => st.C.amber, rate: 3, speed: 60, r: 3.6, jitter: 6 });
    const fb = mk("path", { d: `M${X + 40},${G.y - 10} C${X + 190},${G.y - 60} ${X + 190},${T.y - 10} ${X + 40},${T.y}`, class: "vz-ax-fb" }, g);
    mk("path", { d: `M${X + 40},${G.y - 10} C${X + 130},${G.y - 50} ${X + 130},${Mi.y - 10} ${X + 36},${Mi.y}`, class: "vz-ax-fb" }, g);
    const fbL = label(g, X + 150, 150, "− feedback", { cls: "vz-sc-s" });
    const fbs = stream(dyn, [[X + 40, G.y - 10], [X + 150, G.y - 60], [X + 160, T.y + 40], [X + 40, T.y]], { col: () => st.C.amber, rate: 1.5, speed: 70, r: 2.6, jitter: 1 });
    const tissue = mk("g", { transform: "translate(500,320) scale(1.4)" }, g);
    const effL = label(g, 500, 365, "", { cls: "vz-sc-r" });
    const recX = blocker(g, 470, 300, "var(--vz-2)"), synX = blocker(g, X + 26, G.y + 20, "var(--vz-2)"), pitX = blocker(g, X + 22, Mi.y + 18, "var(--vz-2)");
    const exoP = mk("g", { class: "vz-hide" }, g);
    icon(exoP, "pill", 140, G.y + 60, "var(--vz-1)", 1.2); const exoL = label(exoP, 140, G.y + 88, "", { cls: "vz-sc-s" });
    const exoS = stream(dyn, [[160, G.y + 60], [360, G.y + 40], [440, 300]], { col: () => st.C.blue, rate: 0, speed: 60, r: 3.6, jitter: 6 });
    const bars = mk("g", {}, svg);
    const B = { top: bar(bars, 560, 40, 18, 70, ""), mid: bar(bars, 560, 140, 18, 70, ""), hor: bar(bars, 560, 240, 18, 70, "") };
    const bT = [label(bars, 569, 32, "", { cls: "vz-sc-s" }), label(bars, 569, 132, "", { cls: "vz-sc-s" }), label(bars, 569, 232, "", { cls: "vz-sc-s" })];
    function relabel() {
      const a = ax(st.S);
      brainI.innerHTML = ICON.brain("var(--vz-4)"); pitI.innerHTML = ICON.gland("var(--vz-4)"); glandI.innerHTML = ICON[a.glandIcon || "gland"]("var(--vz-3)");
      tLab.textContent = `${a.top} · ${a.topH}${a.brake ? " (brake)" : ""}`; mLab.textContent = `${a.mid} · ${a.midH}`; gLab.textContent = `${a.gland} · ${a.hormone}`;
      tissue.innerHTML = ICON[a.effectIcon || "effect"]("var(--vz-5)"); effL.textContent = a.effect;
      bT[0].textContent = a.topH; bT[1].textContent = a.midH; bT[2].textContent = a.hormone;
      fb.style.display = a.brake ? "none" : ""; fbL.textContent = a.brake ? "" : "− feedback";
    }
    st.changed = (why) => {
      if (why?.mode !== undefined || why?.reset || why?.preset) relabel();
      const A = act(st.S);
      show(recX, A.some((d) => d.kind === "receptor")); show(synX, A.some((d) => d.kind === "synth")); show(pitX, A.some((d) => d.kind === "pit"));
      const exo = A.find((d) => d.kind === "exo" || d.kind === "taper");
      show(exoP, !!exo); exoL.textContent = exo ? exo.label : "";
      if (why?.drug && A.some((d) => d.id === why.drug && d.kind === "taper")) sim.taperT = 0;
    };
    st.tick = (dt) => {
      const S = st.S, a = ax(S), A = act(S), m = sim.cur;
      const has = (k) => A.some((d) => d.kind === k);
      // exogenous hormone: on, or fading during a taper; an inducer lowers it
      let exo = A.filter((d) => d.kind === "exo").reduce((s, d) => s + (d.amt || 1.4), 0);
      if (has("taper")) { sim.taperT += dt; exo = Math.max(0, 1.4 * (1 - sim.taperT / 14)); }
      if (has("inducer")) exo *= 0.45;
      m.exo += (exo - m.exo) * Math.min(1, dt * 2);
      const fbk = clamp(m.hor - 1, -0.6, 3);
      let top = a.brake ? 1 : clamp(1 - 0.9 * fbk, 0.05, 2.2);
      if (has("agonist")) top *= a.brake ? 1.8 : 0.5;
      if (has("antag")) top *= a.brake ? 0.25 : 1;
      let mid = a.brake ? clamp(1.6 - top * 0.6, 0.05, 2.5) : clamp(top * (1 - 0.35 * fbk), 0.05, 2.5);
      if (has("pit")) mid *= 0.35;
      if (has("gnrh")) mid *= 0.25;
      // the gland follows its drive slowly: weeks of suppression shrink it, recovery takes time too
      m.gland += (clamp(mid, 0.15, 1.3) - m.gland) * Math.min(1, dt * 0.18);
      let made = a.brake ? 0 : m.gland * clamp(mid, 0, 2) * (has("synth") ? 0.2 : 1);
      if (a.brake) made = 0;
      m.made = (m.made ?? 1) + (made - (m.made ?? 1)) * Math.min(1, dt * 1.5);
      const exoOn = m.exo > 0.1; if (exoOn !== sim.exoOn) { sim.exoOn = exoOn; bT[2].textContent = exoOn ? `${a.hormone} + drug` : a.hormone; }
      const horT = a.brake ? mid : made + m.exo;
      m.hor += (horT - m.hor) * Math.min(1, dt * 1.5);
      m.top += (top - m.top) * Math.min(1, dt * 1.5); m.mid += (mid - m.mid) * Math.min(1, dt * 1.5);
      const eff = has("receptor") ? 0.15 : clamp(m.hor, 0, 2);
      s1.rate = 4 * m.top; s2.rate = 4 * m.mid; s3.rate = 4 * clamp(made + (a.brake ? m.mid : 0), 0, 2); exoS.rate = 4 * m.exo; fbs.rate = a.brake ? 0 : 2.5 * clamp(m.hor, 0, 2);
      [s1, s2, s3, exoS, fbs].forEach((s) => s.tick(dt));
      glandI.setAttribute("transform", `translate(${X},${G.y}) scale(${1.5 * (0.55 + 0.45 * m.gland)})`);
      B.top.set(m.top / 2, dt, ""); B.mid.set(m.mid / 2, dt, ""); B.hor.set(m.hor / 2, dt, "");
      tissue.setAttribute("opacity", 0.35 + 0.65 * clamp(eff, 0, 1));
      sim.pt = (sim.pt || 0) + dt; if (sim.pt > 0.3) { sim.pt = 0; st.paint(); }  // readout follows the bars
    };
    relabel(); st.changed({ reset: true });
    return st;
  };

  // ---------------------------------------------------------------- TISSUES: one drug, different effects organ by organ
  // cfg: {tissues:[{id,label,icon,rec}], drugs:[{id,label,fx:{tid:["act"|"block"|"none", "short text"]},note}], base:{tid:"text"}}
  const wrap = (t, txt, n) => {  // up to two lines in a card
    t.textContent = "";
    const words = String(txt).split(" "), lines = [""];
    words.forEach((w) => { if ((lines[lines.length - 1] + " " + w).trim().length > n && lines.length < 2 && lines[lines.length - 1]) lines.push(w); else lines[lines.length - 1] = (lines[lines.length - 1] + " " + w).trim(); });
    lines.forEach((l, i) => { const sp = mk("tspan", { x: t.getAttribute("x"), dy: i ? "1.2em" : 0 }, t); sp.textContent = l; });
  };
  // ---------------------------------------------------------------- BODY MAP: each tissue drawn where it sits in the body, its effect card beside it
  const ORG = {  // [x, y] in a 260×400 body, and the drawing (line art, centred on 0,0)
    brain: [130, 36, '<path d="M-19,3 C-21,-13 -7,-21 0,-17 C7,-21 21,-13 19,3 C17,13 7,15 0,13 C-7,15 -17,13 -19,3Z"/><path class="ln" d="M0,-17V13M-12,-6c4,2 6,0 8,4M12,-6c-4,2 -6,0 -8,4M-13,6c4,-1 6,1 8,-2M13,6c-4,-1 -6,1 -8,-2"/>'],
    stem: [130, 64, '<path d="M-5,-8 C-6,0 -4,8 -3,14 H3 C4,8 6,0 5,-8Z"/>'],
    mouth: [130, 54, '<path d="M-9,0 C-4,-4 4,-4 9,0 C4,5 -4,5 -9,0Z"/>'],
    cord: [130, 150, '<path class="ln" d="M0,-80V80"/><path d="M-3,-20h6v40h-6z"/>'],
    breast: [148, 126, '<path d="M-14,-2 C-12,10 12,10 14,-2"/><circle r="2.2" cx="0" cy="4"/>'],
    heart: [140, 140, '<path d="M-2,-12 C-12,-22 -26,-8 -16,6 L0,20 C12,8 20,-6 10,-14 C6,-17 0,-16 -2,-12Z"/><path class="ln" d="M-4,-14 C-4,-24 8,-26 10,-18"/>'],
    liver: [112, 166, '<path d="M-26,-4 C-20,-15 12,-14 24,-8 C28,-5 22,1 12,5 C0,11 -16,12 -24,7 C-29,3 -29,-1 -26,-4Z"/>'],
    stomach: [150, 172, '<path d="M-6,-16 C-1,-9 -4,0 -9,6 C-13,14 -2,20 8,16 C19,11 20,1 14,-5 C10,-9 6,-10 4,-17Z"/>'],
    pancreas: [132, 188, '<path d="M-22,2 C-22,-6 -10,-6 0,-4 C10,-3 18,-5 23,-1 C20,3 10,4 0,4 C-10,6 -22,9 -22,2Z"/>'],
    kidney: [152, 200, '<path d="M-4,-13 C8,-15 12,-2 10,6 C8,15 -4,15 -6,8 C-2,4 -2,-4 -6,-8 C-8,-11 -6,-13 -4,-13Z"/>'],
    kidneyL: [108, 200, '<path d="M4,-13 C-8,-15 -12,-2 -10,6 C-8,15 4,15 6,8 C2,4 2,-4 6,-8 C8,-11 6,-13 4,-13Z"/>'],
    gut: [130, 226, '<path d="M-22,14 V-12 C-22,-15 -19,-16 -16,-16 H16 C19,-16 22,-15 22,-12 V14"/><path class="ln" d="M-12,-6 c6,-4 10,4 16,0 s10,4 0,8 s-14,2 -10,8 s10,2 14,-2"/>'],
    uterus: [130, 250, '<path d="M-14,-10 C-6,-4 6,-4 14,-10 C12,0 6,8 2,14 H-2 C-6,8 -12,0 -14,-10Z"/><path class="ln" d="M-14,-10 C-20,-12 -22,-6 -18,-4M14,-10 C20,-12 22,-6 18,-4"/>'],
    bladder: [130, 262, '<path d="M-13,-6 C-13,-17 13,-17 13,-6 C13,6 6,12 0,12 C-6,12 -13,6 -13,-6Z"/>'],
    prostate: [130, 280, '<ellipse rx="9" ry="6"/><path class="ln" d="M0,-6V6"/>'],
    penis: [130, 298, '<rect x="-5" y="-9" width="10" height="20" rx="5"/>'],
    femur: [110, 316, '<path d="M-3,-26 C-8,-30 -10,-24 -6,-20 L-3,20 C-7,25 -3,30 2,26 C6,30 9,24 5,20 L3,-20 C8,-24 5,-30 -1,-26Z"/>'],
    knee: [110, 350, '<path d="M-7,-16 V-6 C-9,-2 9,-2 7,-6 V-16M-7,16 V6 C-9,2 9,2 7,6 V16"/><path class="ln" d="M-11,-8 C-15,0 -15,0 -11,8M11,-8 C15,0 15,0 11,8"/>'],
    knee2: [150, 350, '<path d="M-7,-16 V-6 C-9,-2 9,-2 7,-6 V-16M-7,16 V6 C-9,2 9,2 7,6 V16"/><path class="ln" d="M-11,-8 C-15,0 -15,0 -11,8M11,-8 C15,0 15,0 11,8"/>'],
    muscle: [150, 312, '<path d="M0,-24 C10,-14 10,14 0,24 C-10,14 -10,-14 0,-24Z"/><path class="ln" d="M-5,-10H5M-6,0H6M-5,10H5"/>'],
    armmuscle: [62, 150, '<path d="M0,-22 C9,-12 9,12 0,22 C-9,12 -9,-12 0,-22Z"/><path class="ln" d="M-4,-8H4M-5,0H5M-4,8H4"/>'],
    nmj: [62, 178, '<path class="ln" d="M-16,-14 C-8,-10 -4,-6 -2,-2"/><circle r="4"/><path d="M-10,6 H10 V10 H-10Z"/>'],
    artery: [198, 160, '<path d="M-5,-26 C-3,-8 -3,8 -5,26M5,-26 C7,-8 7,8 5,26" class="ln2"/><path class="ln" d="M0,-20V20"/>'],
    lungs: [130, 132, '<path d="M-6,-22 C-20,-20 -26,0 -24,18 C-18,22 -10,20 -6,14Z"/><path d="M6,-22 C20,-20 26,0 24,18 C18,22 10,20 6,14Z"/>'],
    adrenal: [152, 184, '<path d="M-8,4 C-6,-6 4,-8 8,2 Z"/>'],
    thyroid: [130, 82, '<path d="M-3,0 C-6,-8 -14,-8 -14,2 C-14,10 -6,10 -3,4 H3 C6,10 14,10 14,2 C14,-8 6,-8 3,0Z"/>'],
    pituitary: [130, 50, '<path class="ln" d="M0,-8V-2"/><circle r="5"/>'],
    hypothal: [130, 34, '<ellipse rx="10" ry="6"/>'],
    ovary: [150, 254, '<ellipse rx="7" ry="5"/>'],
    testis: [130, 312, '<ellipse cx="-6" rx="5" ry="7"/><ellipse cx="6" rx="5" ry="7"/>'],
    ileum: [116, 232, '<path class="ln2" d="M-12,-6 c6,-6 12,6 18,0 s6,8 -2,10"/>'],
    fat: [150, 228, '<ellipse rx="10" ry="7"/><ellipse cx="8" cy="6" rx="7" ry="5"/>'],
    toe: [146, 396, '<path d="M-8,-4 C-8,-9 8,-9 8,-4 V3 C8,7 -8,7 -8,3Z"/>'],
    parathyroid: [130, 82, '<path class="ln" d="M-3,0 C-6,-8 -14,-8 -14,2 C-14,10 -6,10 -3,4 H3 C6,10 14,10 14,2 C14,-8 6,-8 3,0Z"/><circle cx="-9" cy="-3" r="2.8"/><circle cx="9" cy="-3" r="2.8"/><circle cx="-9" cy="5" r="2.8"/><circle cx="9" cy="5" r="2.8"/>'],
    face: [130, 48, '<path d="M-9,6 C-4,10 4,10 9,6"/><path class="ln" d="M-8,-4h4M4,-4h4"/>'],
    blood: [202, 206, '<path d="M-5,-14 C-3,-4 -3,4 -5,14M5,-14 C7,-4 7,4 5,14" class="ln2"/><ellipse cx="0" cy="-5" rx="3" ry="1.6"/><ellipse cx="1" cy="3" rx="3" ry="1.6"/>'],
  };
  function organOf(t) {
    if (t.organ && ORG[t.organ]) return t.organ;
    const L = String(t.label).toLowerCase();
    const K = [["brainstem", "stem"], ["spinal cord", "cord"], ["neuromuscular", "nmj"], ["muscle fiber", "armmuscle"], ["muscle", "muscle"], ["platelet", "blood"], ["corpus", "penis"],
      ["mouth", "mouth"], ["flaring", "knee2"], ["knee", "knee"], ["joint", "knee"], ["endometri", "uterus"], ["β-cell", "pancreas"], ["pancrea", "pancreas"], ["prostate", "prostate"],
      ["detrusor", "bladder"], ["bladder", "bladder"], ["arteriol", "artery"], ["vessel", "artery"], ["kidney", "kidney"], ["stomach", "stomach"], ["liver", "liver"], ["gut", "gut"],
      ["heart", "heart"], ["breast", "breast"], ["bone", "femur"], ["brain", "brain"]];
    const hit = K.find(([k]) => L.includes(k));
    return hit ? hit[1] : { stomach: "stomach", drop: "blood", kidney: "kidney", joint: "knee", vessel: "artery", brain: "brain", nerve: "cord", muscle: "muscle", breast: "breast", bone: "femur", uterus: "uterus", pancreas: "pancreas", liver: "liver", gut: "gut", heart: "heart", bladder: "bladder", prostate: "prostate" }[t.icon] || "gut";
  }
  const BODY = '<circle cx="130" cy="40" r="25"/><path d="M118,64 h24 v12 C168,78 190,86 196,100 L214,206 C216,216 206,220 202,212 L184,124 L178,190 C182,226 184,262 178,290 L170,394 C168,402 154,402 154,394 L148,300 H112 L106,394 C106,402 92,402 90,394 L82,290 C76,262 78,226 82,190 L76,124 L58,212 C54,220 44,216 46,206 L64,100 C70,86 92,78 118,76Z"/>';
  V.tissues = (host, cfg = {}) => {
    const TS = cfg.tissues, drugs = drugList(cfg.drugs || []), n = TS.length, rowH = n > 4 ? 72 : 84, H = Math.max(400, 24 + n * rowH);
    const sb = (H - 8) / 404, BX = 8;
    const st = V._stage(host, {
      h: H, drugs, multi: !!cfg.multi, label: "Body map: where the drug acts, organ by organ", point: cfg.point, hint: "Drag a drug onto the body, or tap it", steps: cfg.steps,
      target: () => [BX + 130 * sb, H / 2],
      read(S) { return `${noteOf(S, drugs) || esc(cfg.read || "Pick a drug to see what it does in each tissue.")}${cfg.meter ? `<span class="vz-meter-t">${cfg.meter.label}: <b>${meter(S)}</b></span>` : ""}`; },
    });
    const { svg } = st;
    const meter = (S) => { const on = drugs.filter((d) => S.on.has(d.id)); const v = on.reduce((a, d) => a + (d.m || 0), 0); return cfg.meter.text?.[clamp(v, 0, cfg.meter.text.length - 1)] || v; };
    const body = mk("g", { transform: `translate(${BX},4) scale(${sb})` }, svg);
    const sil = mk("g", { class: "vz-bm-body" }, body); sil.innerHTML = BODY;
    const used = new Set(TS.map(organOf));
    if (used.has("cord") || used.has("stem")) { const c = mk("g", { class: "vz-bm-org faint", transform: "translate(130,150)" }, body); c.innerHTML = '<path class="ln" d="M0,-80V80"/>'; }
    const leaders = mk("g", {}, svg), cardsL = mk("g", {}, svg);
    const CX = 300, CW = W - CX - 6;
    const T = TS.map((t, i) => {
      const key = organOf(t), [ox, oy, art] = ORG[key];
      const og = mk("g", { class: "vz-bm-org", transform: `translate(${ox},${oy}) scale(1.3)` }, body);
      const halo = mk("circle", { r: 26, class: "vz-bm-halo" }, og);
      const draw = mk("g", {}, og); draw.innerHTML = art;
      const px = BX + ox * sb, py = 4 + oy * sb;
      const y = 12 + i * rowH, cy = y + (rowH - 10) / 2;
      const lead = mk("path", { d: `M${px + 14},${py} C${px + 70},${py} ${CX - 50},${cy} ${CX},${cy}`, class: "vz-bm-lead" }, leaders);
      const dot = mk("circle", { cx: px, cy: py, r: 3, class: "vz-bm-dot" }, leaders);
      const g = mk("g", { transform: `translate(${CX},${y})` }, cardsL);
      const card = mk("rect", { x: 0, y: 0, width: CW, height: rowH - 10, rx: 14, class: "vz-ts-card" }, g);
      label(g, 14, 20, t.label, { a: "start", cls: "vz-sc-r" });
      if (t.rec) label(g, 14, 35, t.rec, { a: "start", cls: "vz-sc-s" });
      const fx = label(g, 14, t.rec ? 52 : 38, cfg.base?.[t.id] || "", { a: "start", cls: "vz-ts-fx" });
      const x2 = blocker(svg, px + 14, py - 12, "var(--vz-1)");
      return { t, og, halo, card, fx, x2, lead, dot };
    });
    st.changed = () => {
      const S = st.S, on = drugs.filter((d) => S.on.has(d.id));
      T.forEach((o) => {
        const fxs = on.map((d) => d.fx?.[o.t.id]).filter(Boolean);
        const combo = (cfg.combos || []).find((c) => c.ids.every((id) => S.on.has(id)) && c.fx[o.t.id]);
        if (combo) fxs.splice(0, fxs.length, combo.fx[o.t.id]);
        const kind = ["risk", "block", "act"].find((k) => fxs.some((f) => f[0] === k)) || (fxs.length ? "none" : "");
        show(o.x2, kind === "block");
        o.og.setAttribute("class", `vz-bm-org ${kind}`);
        o.card.setAttribute("class", `vz-ts-card ${kind}`);
        o.lead.setAttribute("class", `vz-bm-lead ${kind}`); o.dot.setAttribute("class", `vz-bm-dot ${kind}`);
        wrap(o.fx, fxs.length ? fxs.map((f) => f[1]).join(" · ") : cfg.base?.[o.t.id] || "", Math.floor((CW - 24) / 6.3));
        o.fx.setAttribute("class", `vz-ts-fx ${kind} l`);
      });
    };
    st.tick = () => { const t = performance.now() / 600; T.forEach((o, i) => o.halo.setAttribute("r", 22 + Math.sin(t + i) * 3)); };
    st.changed();
    return st;
  };

  // ---------------------------------------------------------------- ANAT: a pathway drawn on the anatomy where it happens
  // Same config as "pathway" (nodes, edges, drugs with at/off/less/more) plus bg (body|cell|joint|gut|vessel|bladder|nerve),
  // opts (backdrop labels), pos {node:[x,y]} or organ {node: ORG key}, lab {node: "l"|"r"|"t"|"b"}. Steps are markers on the
  // anatomy, molecules flow between them, a drug docks where it acts; "more" raises a step (↑), off/less quiet it.
  const BG = {
    // concept figures (a treatment ladder, a checklist, a two-way choice) get a quiet backdrop instead of anatomy
    plain(g, H, o) { (o.lanes || []).forEach(([y, t, h]) => { mk("rect", { x: 14, y: y - (h || 70) / 2, width: W - 28, height: h || 70, rx: 18, class: "vz-an-lane" }, g); label(g, 30, y - (h || 70) / 2 + 18, String(t).toUpperCase(), { a: "start", cls: "vz-nx-zone" }); }); },
    steps(g, H, o) {
      const n = o.n || 4, x0 = 40, x1 = W - 40, y0 = H - 40, y1 = 70, dx = (x1 - x0) / n, dy = (y0 - y1) / n;
      let d = `M${x0},${y0}`; for (let i = 0; i < n; i++) d += `H${x0 + dx * (i + 1)}${i < n - 1 ? `V${y0 - dy * (i + 1)}` : ""}`;
      mk("path", { d: `${d}V${H - 14}H${x0}Z`, class: "vz-an-stairs" }, g);
      if (o.axis) label(g, x0 + 4, H - 20, String(o.axis).toUpperCase(), { a: "start", cls: "vz-nx-zone" });
    },
    cell(g, H, o) {
      const R = o.right ? 470 : 600, L = o.left === false ? 20 : 150;
      if (o.left !== false) { mk("rect", { x: 0, y: 0, width: L - 8, height: H, rx: 16, class: `vz-an-ext ${o.leftCls || "blood"}` }, g); label(g, 12, 22, (o.left || "Blood").toUpperCase(), { a: "start", cls: "vz-nx-zone" }); }
      if (o.right) { mk("rect", { x: R + 8, y: 0, width: W - R - 8, height: H, rx: 16, class: `vz-an-ext ${o.rightCls || "lumen"}` }, g); label(g, W - 12, 22, o.right.toUpperCase(), { a: "end", cls: "vz-nx-zone" }); }
      mk("rect", { x: L, y: 14, width: R - L, height: H - 28, rx: 44, class: "vz-an-cell" }, g);
      mk("rect", { x: L + 6, y: 20, width: R - L - 12, height: H - 40, rx: 38, class: "vz-an-cell2" }, g);
      if (o.nuc) { mk("ellipse", { cx: o.nuc[0], cy: o.nuc[1], rx: 58, ry: 40, class: "vz-an-nuc" }, g); label(g, o.nuc[0], o.nuc[1] + 56, "nucleus", { cls: "vz-sc-m" }); }
      label(g, R - 22, H - 30, o.name || "Cell", { a: "end", cls: "vz-sc-h" });
    },
    body(g, H, o, ctx) {
      const sb = (H - 8) / 404, bx = (o.x ?? 320) - 130 * sb;
      const b = mk("g", { transform: `translate(${bx},4) scale(${sb})` }, g);
      mk("g", { class: "vz-bm-body" }, b).innerHTML = BODY;
      ctx.toXY = (key) => { const q = ORG[key]; return q ? [bx + q[0] * sb, 4 + q[1] * sb] : [320, H / 2]; };
      (o.organs || []).forEach((k) => { const q = ORG[k]; if (!q) return; const og = mk("g", { class: "vz-bm-org", transform: `translate(${q[0]},${q[1]}) scale(1.3)` }, b); og.innerHTML = q[2]; });
    },
    joint(g, H) {
      mk("path", { d: `M200,0 H440 V120 C440,165 390,178 320,170 C250,178 200,165 200,120 Z`, class: "vz-an-bone" }, g);
      mk("path", { d: `M210,${H} H430 V${H - 120} C430,${H - 160} 380,${H - 168} 320,${H - 164} C260,${H - 168} 210,${H - 160} 210,${H - 120} Z`, class: "vz-an-bone" }, g);
      mk("path", { d: `M206,132 C214,166 262,178 320,172 C378,178 426,166 434,132`, class: "vz-an-cart" }, g);
      mk("path", { d: `M216,${H - 126} C226,${H - 158} 270,${H - 166} 320,${H - 162} C370,${H - 166} 414,${H - 158} 424,${H - 126}`, class: "vz-an-cart" }, g);
      mk("path", { d: `M196,110 C150,150 150,${H - 150} 206,${H - 110} M444,110 C490,150 490,${H - 150} 434,${H - 110}`, class: "vz-an-syn" }, g);
      label(g, 320, 40, "BONE", { cls: "vz-nx-zone" }); label(g, 320, H - 28, "BONE", { cls: "vz-nx-zone" });
      label(g, 320, H / 2 + 4, "joint fluid", { cls: "vz-sc-m" }); label(g, 150, H / 2 - 64, "SYNOVIUM", { cls: "vz-nx-zone" }); label(g, 470, 196, "cartilage", { a: "start", cls: "vz-sc-m" });
    },
    gut(g, H, o) {
      mk("rect", { x: 0, y: 0, width: W, height: 104, rx: 14, class: "vz-an-ext lumen" }, g);
      label(g, 12, 22, (o.lumen || "Gut lumen").toUpperCase(), { a: "start", cls: "vz-nx-zone" });
      for (let x = 6; x < W - 10; x += 34) mk("rect", { x, y: 100, width: 30, height: 58, rx: 10, class: "vz-an-epi" }, g);
      mk("rect", { x: 0, y: 162, width: W, height: H - 162, rx: 14, class: "vz-an-lp" }, g);
      label(g, 12, 182, "LAMINA PROPRIA (mucosa)", { a: "start", cls: "vz-nx-zone" });
      mk("rect", { x: 0, y: H - 56, width: W, height: 34, rx: 17, class: "vz-an-ves" }, g);
      label(g, W - 12, H - 34, "blood vessel", { a: "end", cls: "vz-sc-m" });
      label(g, W - 12, 150, "epithelium", { a: "end", cls: "vz-sc-m" });
    },
    vessel(g, H, o) {
      mk("rect", { x: 0, y: 40, width: W, height: 74, class: "vz-an-smc" }, g);
      for (let x = 10; x < W; x += 46) mk("ellipse", { cx: x + 20, cy: 77, rx: 20, ry: 7, class: "vz-an-spindle" }, g);
      mk("rect", { x: 0, y: 114, width: W, height: 8, class: "vz-an-endo" }, g);
      mk("rect", { x: 0, y: 122, width: W, height: H - 160, class: "vz-an-ext blood" }, g);
      label(g, 12, 30, (o.wall || "Vascular smooth muscle").toUpperCase(), { a: "start", cls: "vz-nx-zone" });
      label(g, W - 12, 136, "endothelium", { a: "end", cls: "vz-sc-m" });
      label(g, 12, 144, (o.lumen || "Blood").toUpperCase(), { a: "start", cls: "vz-nx-zone" });
    },
    bladder(g, H) {
      mk("path", { d: "M180,150 C180,40 460,40 460,150 C460,232 392,262 352,272 L346,300 H294 L288,272 C248,262 180,232 180,150Z", class: "vz-an-detr" }, g);
      mk("path", { d: "M206,150 C206,66 434,66 434,150 C434,216 380,240 340,250 H300 C260,240 206,216 206,150Z", class: "vz-an-urine" }, g);
      mk("ellipse", { cx: 320, cy: 312, rx: 66, ry: 34, class: "vz-an-pros" }, g);
      mk("rect", { x: 312, y: 250, width: 16, height: H - 250, rx: 8, class: "vz-an-ureth" }, g);
      label(g, 320, 150, "urine", { cls: "vz-sc-m" }); label(g, 470, 110, "DETRUSOR (bladder wall)", { a: "start", cls: "vz-nx-zone" });
      label(g, 400, 350, "PROSTATE", { a: "start", cls: "vz-nx-zone" }); label(g, 352, 284, "bladder neck", { a: "start", cls: "vz-sc-m" }); label(g, 334, H - 10, "urethra", { a: "start", cls: "vz-sc-m" });
    },
    nerve(g, H) {
      mk("rect", { x: 0, y: 0, width: 330, height: H, rx: 16, class: "vz-an-ext tissue" }, g);
      for (let i = 0; i < 9; i++) mk("circle", { cx: 40 + (i % 3) * 90, cy: 70 + Math.floor(i / 3) * 110, r: 30, class: "vz-an-tcell" }, g);
      mk("path", { d: `M600,${H / 2} C470,${H / 2} 420,${H / 2} 330,${H / 2} M360,${H / 2} C320,${H / 2 - 40} 290,${H / 2 - 90} 250,${H / 2 - 110} M360,${H / 2} C320,${H / 2 + 30} 300,${H / 2 + 90} 240,${H / 2 + 120} M330,${H / 2} C300,${H / 2} 260,${H / 2 + 10} 200,${H / 2 - 6}`, class: "vz-an-axon" }, g);
      label(g, 12, 22, "INFLAMED TISSUE", { a: "start", cls: "vz-nx-zone" }); label(g, W - 12, H / 2 - 14, "→ spinal cord, brain", { a: "end", cls: "vz-sc-m" });
      label(g, 470, H / 2 + 22, "nociceptor (pain fiber)", { cls: "vz-sc-m" });
    },
  };
  V.anat = (host, cfg = {}) => {
    const H = cfg.h || 380, N = (cfg.nodes || []).map((n) => ({ col: "teal", ...n })), E = cfg.edges || [], D = cfg.drugs || [], O = cfg.opts || {};
    const COLV = { teal: "var(--vz-1)", coral: "var(--vz-2)", amber: "var(--vz-3)", blue: "var(--vz-4)", sage: "var(--vz-5)", deep: "var(--vz-text)", ink: "var(--vz-ink)" };
    const by = Object.fromEntries(N.map((n) => [n.id, n]));
    const outs = new Set(E.map((e) => e[0])), terminal = N.filter((n) => !outs.has(n.id) && E.some((e) => e[1] === n.id)).map((n) => n.id);
    const drugs = D.map((d, i) => ({ id: `d${i}`, label: d.label, note: d.note, col: ["var(--vz-1)", "var(--vz-2)", "var(--vz-4)", "var(--vz-3)", "var(--vz-5)"][i % 5], src: d }));
    const ctx = {};
    const P = (id) => by[id]._xy;
    const st = V._stage(host, {
      h: H, drugs, label: cfg.title || "Pathway on the anatomy", point: cfg.point, hint: "Drag a drug onto the picture, or tap it",
      target: (id) => { const d = drugs.find((x) => x.id === id).src; if (!d.at) return [320, H / 2]; if (d.at.includes(">")) { const [a, b] = d.at.split(">"); return mid(a, b); } return by[d.at] ? P(d.at) : [320, H / 2]; },
      read(S) {
        const d = drugs.find((x) => S.on.has(x.id));
        const lv = (cfg.noring ? [] : terminal).filter((id) => !isOn(S, id)).map((id) => { const v = level(S, id); return `${by[id].label.replace(/\n/g, " ")}: <b>${v > 1 ? "↑ more" : Math.round(v * 100) + "%"}</b>`; }).join(" · ");
        return `${d ? `<b>${esc(d.label)}.</b> ${d.note || ""}` : esc(cfg.read || "Drag a drug onto the picture to see where it acts and what changes downstream.")}${chain(S)}${d && lv && [d.src.off, d.src.less, d.src.more].some((x) => (x || []).length) ? `<span class="vz-meter-t">${lv}</span>` : ""}`;
      },
    });
    const { svg } = st;
    const cur = (S) => drugs.find((x) => S.on.has(x.id))?.src;
    // the causal chain in words, in pathway order: the normal sequence first, then where the drug acts and what changes after it
    const order = (() => {
      const ind = Object.fromEntries(N.map((n) => [n.id, 0])); E.forEach(([, b]) => { if (b in ind) ind[b]++; });
      const q = N.filter((n) => !ind[n.id]).map((n) => n.id), seen = new Set(q), out = [];
      while (q.length) { const a = q.shift(); out.push(a); E.forEach(([x, y]) => { if (x === a && !seen.has(y) && by[y]) { seen.add(y); q.push(y); } }); }
      N.forEach((n) => { if (!seen.has(n.id)) out.push(n.id); });
      return out;
    })();
    const nm = (id) => esc(String(by[id].label).replace(/\n/g, " "));
    function chain(S) {
      const d = cur(S), row = (cls, id, html, i) => `<span class="vz-ch ${cls}"${id ? ` data-n="${id}"` : ""} style="--i:${i}"><i></i><span>${html}</span></span>`;
      if (!d) return N.length < 2 ? "" : `<span class="vz-chain"><span class="vz-ch-h">${esc(cfg.normal || "Normal pathway")}</span>${order.map((id, i) => row("", id, nm(id), i)).join("")}</span>`;
      const rows = []; let i = 0;
      if (d.at) {
        const [a, b] = d.at.split(">");
        const lv = b ? 1 : level(S, a), tag = lv === 1 ? "" : ` <b class="${lv > 1 ? "up" : "dn"}">${lv > 1 ? "↑ more" : lv < 0.2 ? "↓↓ off" : "↓ less"}</b>`;
        if (by[a] && (!b || by[b])) rows.push(row("at", b ? "" : a, `<em>${cfg.verb || (d.act === "up" ? "Starts at" : "Acts at")}</em> ${b ? `${nm(a)} → ${nm(b)}` : nm(a)}${tag}`, i++));
      }
      order.forEach((id) => { const lv = level(S, id); if (id === d.at && by[id]) return;
        if (isOn(S, id)) return rows.push(row("on", id, nm(id), i++));
        if (lv === 1) return; rows.push(row(lv > 1 ? "up" : "dn", id, `${nm(id)} <b>${lv > 1 ? "↑ more" : lv < 0.2 ? "↓↓ off" : "↓ less"}</b>`, i++)); });
      return rows.length ? `<span class="vz-chain"><span class="vz-ch-h">${rows.length === 1 ? "Where it fits" : (d.on || []).length ? "What happens, in order" : "What changes, in order"}</span>${rows.join("")}</span>` : "";
    }
    const hl = (e, on) => { const r = e.target.closest?.(".vz-ch[data-n]"); if (!r) return; NODE.find((x) => x.n.id === r.dataset.n)?.g.classList.toggle("hl", on); };
    st.el.addEventListener("pointerover", (e) => hl(e, true)); st.el.addEventListener("pointerout", (e) => hl(e, false));
    // "on": a step the drug sets in motion (its label already says which way things go), shown lit rather than as more/less
    const isOn = (S, id) => (cur(S)?.on || []).includes(id);
    function level(S, id) { const d = cur(S); if (!d) return 1; return (d.off || []).includes(id) ? 0.12 : (d.less || []).includes(id) ? 0.55 : (d.more || []).includes(id) ? 1.6 : 1; }
    const L = { bg: mk("g", {}, svg), lines: mk("g", {}, svg), flow: mk("g", {}, svg), nodes: mk("g", {}, svg), top: mk("g", {}, svg) };
    (BG[cfg.bg] || BG.cell)(L.bg, H, O, ctx);
    N.forEach((n) => { n._xy = cfg.organ?.[n.id] && ctx.toXY ? ctx.toXY(cfg.organ[n.id]) : cfg.pos?.[n.id] || [n.x + 65, n.y + 30]; n._mk = n._xy; });
    // body map: an organ's marker sits outside the body, joined to the organ by a leader; flows still run organ to organ
    if (ctx.toXY) {
      ["l", "r"].forEach((side) => {
        const list = N.filter((n) => cfg.organ?.[n.id] && (cfg.lab?.[n.id] || "r") === side).sort((a, b) => a._xy[1] - b._xy[1]);
        let last = -99;
        list.forEach((n) => { const y = Math.max(n._xy[1], last + 50); last = y; n._mk = [side === "l" ? 190 : 450, y]; });
      });
    }
    function mid(a, b) { const [ax, ay] = P(a), [bx, bY] = P(b); return [(ax + bx) / 2, (ay + bY) / 2]; }
    const streams = E.map(([a, b]) => {
      const [ax, ay] = P(a), [bx, bY] = P(b), dx = bx - ax, dy = bY - ay, len = Math.hypot(dx, dy) || 1, bend = (cfg.bend?.[`${a}>${b}`] ?? 0.12) * len;
      const c = [(ax + bx) / 2 - (dy / len) * bend, (ay + bY) / 2 + (dx / len) * bend];
      const q = (t) => [(1 - t) ** 2 * ax + 2 * (1 - t) * t * c[0] + t * t * bx, (1 - t) ** 2 * ay + 2 * (1 - t) * t * c[1] + t * t * bY];
      const tEnd = 1 - 24 / len, tStart = 22 / len;
      const poly = Array.from({ length: 15 }, (_, i) => q(tStart + (tEnd - tStart) * i / 14));
      mk("path", { d: `M${poly.map((p) => p.join(",")).join("L")}`, class: "vz-an-line" }, L.lines);
      const e = poly[14], e0 = poly[13];
      mk("path", { d: "M-6,-5L1,0L-6,5", class: "vz-fx-arrow", transform: `translate(${e[0]},${e[1]}) rotate(${Math.atan2(e[1] - e0[1], e[0] - e0[0]) * 180 / Math.PI})` }, L.lines);
      const col = COLV[by[a].col] || "var(--vz-1)";
      return { a, b, s: stream(L.flow, poly, { col: () => getComputedStyle(st.el).getPropertyValue(col.slice(4, -1)) || "#888", rate: 1.8, speed: 50, r: 3.6, jitter: 2 }) };
    });
    const NODE = N.map((n) => {
      const col = COLV[n.col] || "var(--vz-1)", [x, y] = n._mk, g = mk("g", { class: "vz-an-node", transform: `translate(${x},${y})` }, L.nodes);
      if (n._mk !== n._xy) {  // leader from the organ to its marker, and a glowing dot on the organ
        const [ox, oy] = n._xy;
        mk("path", { d: `M${ox - x},${oy - y} C${(ox - x) * 0.5},${oy - y} ${(ox - x) * 0.3},0 ${ox > x ? 19 : -19},0`, class: "vz-an-lead", style: `--c:${col}` }, g);
        mk("circle", { cx: ox - x, cy: oy - y, r: 9, class: "vz-an-orgdot", style: `--c:${col}` }, g);
      }
      mk("circle", { r: 19, class: "vz-an-mk", style: `--c:${col}` }, g);
      const ic = mk("g", { transform: "scale(0.62)" }, g); ic.innerHTML = ICON[iconFor(n)](col);
      const side = cfg.lab?.[n.id] || (x > 470 ? "l" : "r"), ls = String(n.label).split("\n");
      const [tx, ty, an] = side === "l" ? [-26, 4, "end"] : side === "t" ? [0, -28 - (ls.length - 1) * 14, "middle"] : side === "b" ? [0, 36, "middle"] : [26, 4, "start"];
      const t = mk("text", { x: tx, y: ty - (side === "l" || side === "r" ? (ls.length - 1) * 7 : 0), "text-anchor": an, class: "vz-an-t" }, g);
      ls.forEach((l, i) => { const sp = mk("tspan", { x: tx, dy: i ? "1.15em" : 0 }, t); sp.textContent = l; });
      let ring = null;
      if (terminal.includes(n.id) && !cfg.noring) {
        mk("circle", { cx: 15, cy: -15, r: 10, class: "vz-fx-gt" }, g);
        ring = mk("circle", { cx: 15, cy: -15, r: 10, class: "vz-fx-gr", "stroke-dasharray": `${2 * Math.PI * 10}`, transform: "rotate(-90 15 -15)" }, g);
        ring.lv = 1;
      }
      const badge = mk("text", { x: 0, y: 34, "text-anchor": "middle", class: "vz-an-badge" }, g);
      if (side === "b") badge.setAttribute("y", -26);
      return { n, g, ring, badge };
    });
    const dock = mk("g", { class: "vz-hide" }, L.top);
    const dockPill = mk("rect", { x: -18, y: -9, width: 36, height: 18, rx: 9, class: "vz-fx-dock" }, dock);
    const dockMark = mk("path", { d: "M-5,-5L5,5M5,-5L-5,5", stroke: "#fff", "stroke-width": 2.6, "stroke-linecap": "round" }, dock);
    st.changed = () => {
      const S = st.S, d = cur(S), dd = drugs.find((x) => S.on.has(x.id));
      // an agonist / enhancer docks with "+", a blocker with "×"
      dockMark.setAttribute("d", d?.act === "up" ? "M0,-5.5V5.5M-5.5,0H5.5" : "M-5,-5L5,5M5,-5L-5,5");
      NODE.forEach(({ n, g, badge }) => { const lv = level(S, n.id); g.style.opacity = lv < 0.2 ? 0.38 : lv < 1 ? 0.72 : 1; g.classList.toggle("up", lv > 1 || isOn(S, n.id)); badge.textContent = lv > 1 ? "↑ more" : lv < 1 ? (lv < 0.2 ? "↓↓ off" : "↓ less") : ""; });
      show(dock, !!d?.at);
      if (d?.at) { const [x, y] = st._target(dd.id); dock.setAttribute("transform", `translate(${x},${y})`); dockPill.style.fill = dd.col; }
      streams.forEach((s) => {
        const cut = d && (d.at === `${s.a}>${s.b}` || d.at === s.b && (d.off || []).length);
        const quiet = d && ((d.off || []).includes(s.a) || (d.off || []).includes(s.b));
        s.s.stop = cut ? 0.72 : null; s.s.rate = quiet && !cut ? 0.25 : (d?.less || []).includes(s.b) ? 0.9 : (d?.more || []).includes(s.b) || (d?.on || []).includes(s.b) ? 3.4 : 1.8;
      });
    };
    st.tick = (dt) => {
      streams.forEach((s) => s.s.tick(dt));
      NODE.forEach(({ n, ring }) => { if (!ring) return; const t = Math.min(1, level(st.S, n.id)); ring.lv += (t - ring.lv) * Math.min(1, dt * 3); ring.setAttribute("stroke-dashoffset", `${2 * Math.PI * 10 * (1 - ring.lv)}`); });
    };
    st.changed();
    return st;
  };

  // ---------------------------------------------------------------- CYCLE: a vicious circle you can break
  V.cycle = (host, cfg = {}) => {
    const H = 360, N = cfg.nodes, drugs = drugList(cfg.drugs || []), R = 120, C0 = [250, 180];
    const st = V._stage(host, {
      h: H, drugs, multi: true, label: "Vicious cycle", point: cfg.point, hint: "Break the cycle: drag a drug onto a step", steps: cfg.steps,
      target: (id) => { const d = drugs.find((x) => x.id === id), i = N.findIndex((n) => n.id === d.at); return pos(i); },
      read(S) { const b = drugs.filter((d) => S.on.has(d.id)).length; return `${noteOf(S, drugs) || esc(cfg.read || "Each step feeds the next, all the way around.")}<span class="vz-meter-t">Cycle: <b>${b ? "broken — it slows down" : "spinning"}</b></span>`; },
    });
    const { svg } = st;
    const pos = (i) => { const a = -Math.PI / 2 + (i * 2 * Math.PI) / N.length; return [C0[0] + R * Math.cos(a), C0[1] + R * Math.sin(a)]; };
    mk("circle", { cx: C0[0], cy: C0[1], r: R, class: "vz-cy-ring" }, svg);
    const X = {};
    N.forEach((n, i) => {
      const [x, y] = pos(i), g = mk("g", { transform: `translate(${x},${y})` }, svg);
      mk("circle", { r: 34, class: "vz-cy-node" }, g);
      const ic = mk("g", { transform: "scale(1.05)" }, g); ic.innerHTML = ICON[n.icon || "effect"](["var(--vz-2)", "var(--vz-3)", "var(--vz-4)", "var(--vz-1)"][i % 4]);
      const lx = x > C0[0] + 10 ? 42 : x < C0[0] - 10 ? -42 : 0, ly = y < C0[1] - 10 ? -42 : y > C0[1] + 10 ? 50 : 4;
      const t = label(g, lx, ly, "", { a: lx > 0 ? "start" : lx < 0 ? "end" : "middle", cls: "vz-sc-r" });
      String(n.label).split("\n").forEach((l, k) => { const sp = mk("tspan", { x: lx, dy: k ? "1.2em" : 0 }, t); sp.textContent = l; });
      X[n.id] = blocker(g, 22, -24, "var(--vz-2)");
    });
    const dots = Array.from({ length: 14 }, (_, k) => ({ a: (k / 14) * Math.PI * 2, c: mk("circle", { r: 4.5, class: "vz-cy-dot" }, svg) }));
    let speed = 1;
    const bars = mk("g", {}, svg), sp = bar(bars, 520, 90, 22, 180, "Cycle speed");
    st.changed = () => { const S = st.S, on = new Set(drugs.filter((d) => S.on.has(d.id)).map((d) => d.at)); N.forEach((n) => show(X[n.id], on.has(n.id))); };
    st.tick = (dt) => {
      const S = st.S, br = drugs.filter((d) => S.on.has(d.id)).length, target = br ? Math.max(0.08, 0.35 - 0.12 * (br - 1)) : 1;
      speed += (target - speed) * Math.min(1, dt * 1.5);
      dots.forEach((d) => { d.a += dt * 0.9 * speed; const x = C0[0] + R * Math.cos(d.a), y = C0[1] + R * Math.sin(d.a); d.c.setAttribute("cx", x); d.c.setAttribute("cy", y); });
      sp.set(speed, dt, br ? "slower" : "fast");
    };
    st.changed();
    return st;
  };

  // ---------------------------------------------------------------- COLON: laxatives and antidiarrheals in a cross-section
  V.colon = (host, cfg = {}) => {
    const H = 300, drugs = drugList(cfg.drugs || []);
    const FX = { bulk: { size: 1.5, water: 0.6, speed: 1.1 }, osm: { size: 1.2, water: 1, speed: 1.4, pull: true }, stim: { size: 1, water: 0.2, speed: 1.8, waves: true }, sec: { size: 1.15, water: 0.8, speed: 1.4, secrete: true }, opioid: { size: 0.85, water: -0.4, speed: 0.4, slow: true } };
    const st = V._stage(host, {
      h: H, drugs, label: "Colon", point: cfg.point, hint: "Drag a drug onto the colon, or tap it", steps: cfg.steps, target: () => [320, 150],
      read(S) { const f = fx(S); return `${noteOf(S, drugs) || esc(cfg.read || "Stool moves along as the wall squeezes in waves; water moves in and out across the lining.")}<span class="vz-meter-t">Transit: <b>${f.speed > 1.2 ? "faster" : f.speed < 0.7 ? "slower" : "normal"}</b> · Stool water: <b>${f.water > 0.5 ? "more (softer)" : f.water < 0 ? "less (firmer)" : "normal"}</b></span>`; },
    });
    const { svg } = st;
    const fx = (S) => { const d = drugs.find((x) => S.on.has(x.id)); return d ? FX[d.fx] : { size: 1, water: 0, speed: 1 }; };
    mk("rect", { x: 10, y: 70, width: 620, height: 160, rx: 70, class: "vz-co-wall" }, svg);
    mk("rect", { x: 10, y: 96, width: 620, height: 108, rx: 54, class: "vz-co-lumen" }, svg);
    label(svg, 30, 60, "Colon wall (enteric nerves, lining)", { a: "start", cls: "vz-sc-s" });
    const nerves = Array.from({ length: 8 }, (_, i) => mk("circle", { cx: 50 + i * 78, cy: 84, r: 5, class: "vz-co-nerve" }, svg));
    const cid = `coClip${Math.random().toString(36).slice(2, 7)}`;
    const cp = mk("clipPath", { id: cid }, mk("defs", {}, svg)); mk("rect", { x: 10, y: 70, width: 620, height: 160, rx: 70 }, cp);
    const ring = mk("g", { "clip-path": `url(#${cid})` }, svg), waves = [0, 1, 2].map(() => ({ x: -100, e: mk("ellipse", { cx: 0, cy: 150, rx: 16, ry: 74, class: "vz-co-wave" }, ring) }));
    const stools = Array.from({ length: 3 }, (_, i) => ({ x: 80 + i * 210, e: mk("ellipse", { cx: 0, cy: 150, rx: 34, ry: 22, class: "vz-co-stool" }, svg), drops: [] }));
    const water = mk("g", {}, svg);
    let wT = 0;
    st.changed = () => {};
    st.tick = (dt) => {
      const f = fx(st.S);
      stools.forEach((s) => { s.x += dt * 28 * f.speed; if (s.x > 680) s.x = -40; const sz = f.size; s.e.setAttribute("cx", s.x); s.e.setAttribute("rx", 34 * sz); s.e.setAttribute("ry", 20 * sz); s.e.style.opacity = f.water < 0 ? 0.95 : 0.85; });
      waves.forEach((w, i) => { w.x += dt * 60 * f.speed * (f.waves ? 1.6 : 1); if (w.x > 700) w.x = -60 - i * 230; w.e.setAttribute("cx", w.x); w.e.setAttribute("opacity", f.waves ? 0.6 : f.slow ? 0.12 : 0.3); });
      nerves.forEach((n, i) => n.setAttribute("class", `vz-co-nerve${f.waves && Math.sin(performance.now() / 200 + i) > 0.6 ? " on" : ""}`));
      wT += dt;
      if (wT > 0.12) {
        wT = 0;
        if (f.pull || f.secrete || f.water < 0 || f.size > 1.3) {
          const x = 30 + Math.random() * 580, up = Math.random() < 0.5, inward = f.water >= 0;
          const y0 = inward ? (up ? 84 : 216) : 150 + (Math.random() - 0.5) * 60, y1 = inward ? 150 + (Math.random() - 0.5) * 60 : up ? 84 : 216;
          const d = mk("text", { x, y: y0, class: `vz-co-drop${f.secrete ? " cl" : ""}`, "text-anchor": "middle" }, water); d.textContent = f.secrete && Math.random() < 0.4 ? "Cl⁻" : "💧";
          const t0 = performance.now(); const step = () => { const t = (performance.now() - t0) / 900; d.setAttribute("y", lerp(y0, y1, Math.min(1, t))); d.setAttribute("opacity", 1 - Math.max(0, t - 0.6) * 2.5); if (t < 1) requestAnimationFrame(step); else d.remove(); }; requestAnimationFrame(step);
        }
      }
    };
    return st;
  };

  // ---------------------------------------------------------------- RENAL DOSING: repeated doses as kidney function falls
  V.renaldose = (host, cfg = {}) => {
    const H = 300, drugs = drugList(cfg.drugs || [{ id: "std", label: "Usual dose and interval" }, { id: "dose", label: "Lower the dose" }, { id: "int", label: "Extend the interval" }]);
    const st = V._stage(host, {
      h: H, drugs, label: "Drug levels with falling GFR", point: cfg.point, hint: "Pick kidney function, then a dosing strategy",
      modes: { label: "Kidney function", opts: [["100", "Normal"], ["50", "GFR halved"], ["25", "Severe CKD"]] }, start: { mode: "100", on: ["std"] },
      steps: cfg.steps, target: () => [320, 150],
      read(S) { const r = run(S); return `${noteOf(S, drugs)}<span class="vz-meter-t">Peak level: <b>${r.peak > 1 ? "above the toxic line" : r.trough < 0.25 ? "below the effective range" : "in the window"}</b></span>`; },
    });
    const { svg } = st;
    const X0 = 50, X1 = 620, Y0 = 260, Y1 = 30, days = 7;
    function run(S) {
      const g = +S.mode / 100, d = drugs.find((x) => S.on.has(x.id))?.id || "std";
      const ke = 0.9 * g, dose = d === "dose" ? 0.42 * Math.max(g, 0.3) / 0.5 : 0.42, tau = d === "int" ? 1 / Math.max(g, 0.25) : 1;
      const pts = []; let c = 0, peak = 0, trough = 1;
      for (let t = 0; t <= days; t += 0.02) { const k = Math.round(t / 0.02); if (k % Math.round(tau / 0.02) === 0) c += dose; c *= Math.exp(-ke * 0.02); pts.push([t, c]); if (t > 4) { peak = Math.max(peak, c); trough = Math.min(trough, c); } }
      return { pts, peak: peak / 0.95, trough: trough / 0.95 };
    }
    const sx = (t) => X0 + (t / days) * (X1 - X0), sy = (c) => Y0 - (c / 1.25) * (Y0 - Y1);
    mk("rect", { x: X0, y: sy(0.95), width: X1 - X0, height: sy(0.25) - sy(0.95), class: "vz-rd-win" }, svg);
    mk("line", { x1: X0, x2: X1, y1: sy(0.95), y2: sy(0.95), class: "vz-rd-tox" }, svg);
    label(svg, X1, sy(0.95) - 6, "Toxic", { a: "end", cls: "vz-sc-s vz-sc-red" }); label(svg, X1, sy(0.25) + 14, "Effective range", { a: "end", cls: "vz-sc-s" });
    mk("line", { x1: X0, x2: X1, y1: Y0, y2: Y0, class: "vz-rd-ax" }, svg); label(svg, X1, Y0 + 20, "Days of dosing", { a: "end", cls: "vz-sc-s" });
    const line = mk("path", { class: "vz-rd-line" }, svg);
    let shown = null;
    st.changed = () => { const r = run(st.S); shown = r.pts; line.setAttribute("d", `M${r.pts.map(([t, c]) => `${sx(t).toFixed(1)},${sy(Math.min(c, 1.24)).toFixed(1)}`).join("L")}`); };
    st.tick = () => {};
    st.changed();
    return st;
  };
  window.dpasVizRefresh?.();  // draw any figure that came into view before this file loaded
})();
