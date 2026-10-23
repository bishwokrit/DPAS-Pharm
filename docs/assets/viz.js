// Hands-on figures: each lecture diagram (by its image name) gets an interactive twin you can drag and adjust.
// Same illustrative models and values as the original figures; the original stays one tap away and in print/PDF.
(function () {
  const C = { teal: "#0F7173", coral: "#D1495B", amber: "#E9A23B", blue: "#2A6F97", deep: "#123C44", sage: "#6B9080", grid: "#ececf0", ink: "#86868b" };
  const W = 640, H = 330, L = 46, R = 620, T = 34, B = 290;  // plot box inside the viewBox
  // shared defs: a soft shadow for handles, an arrowhead, and a fading fill for each series color
  const DEFS = `<defs><filter id="vzSh" x="-50%" y="-50%" width="200%" height="200%"><feDropShadow dx="0" dy="1.5" stdDeviation="2" flood-color="#000" flood-opacity=".22"/></filter>
    <marker id="vzA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="9" markerHeight="9" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1L9,5L1,9" fill="none" stroke="#86868b" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></marker>
    ${["teal", "coral", "amber", "blue"].map((k) => `<linearGradient id="vzF-${k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${C[k]}" stop-opacity=".16"/><stop offset="1" stop-color="${C[k]}" stop-opacity="0"/></linearGradient>`).join("")}</defs>`;
  const sx = (v, a, b) => L + ((v - a) / (b - a)) * (R - L), sy = (v, a, b) => B - ((v - a) / (b - a)) * (B - T);
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const f1 = (v) => (Math.abs(v) >= 100 ? Math.round(v) : Math.abs(v) >= 10 ? Math.round(v * 10) / 10 : Math.round(v * 100) / 100).toLocaleString();
  const pct = (v) => `${Math.round(v)}%`;
  const path = (fn, a, b, n = 140) => Array.from({ length: n + 1 }, (_, i) => { const x = a + ((b - a) * i) / n, p = fn(x); return `${i ? "L" : "M"}${p[0].toFixed(1)},${p[1].toFixed(1)}`; }).join("");
  // quiet axes: hairline grid, no y-axis line, gray tick labels, the unit written once at top-left
  const axes = (xl, yl, xt, yt) => `<g class="vz-ax">${yt.map(([v, y]) => `<line x1="${L}" x2="${R}" y1="${y}" y2="${y}" stroke="${C.grid}"/><text class="vz-tk" x="${L - 8}" y="${y + 4}" text-anchor="end">${v}</text>`).join("")}
    ${xt.map(([v, x]) => `<text class="vz-tk" x="${x}" y="${B + 19}" text-anchor="middle">${v}</text>`).join("")}
    <line x1="${L}" x2="${R}" y1="${B}" y2="${B}" stroke="#d2d2d7"/>
    ${xl ? `<text x="${R}" y="${H - 2}" text-anchor="end" class="vz-lab">${xl}</text>` : ""}${yl ? `<text x="${L - 8}" y="${T - 16}" text-anchor="start" class="vz-lab">${yl}</text>` : ""}</g>`;
  const dot = (x, y, col, r = 7) => `<circle cx="${x}" cy="${y}" r="${r + 9}" fill="${col}" opacity=".12"/><circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${col}" stroke-width="3" filter="url(#vzSh)"/>`;
  const bar = (x, y, w, h, col, r = 8) => (h <= 0 ? "" : `<path d="M${x},${y + h}V${y + Math.min(r, h)}Q${x},${y} ${x + r},${y}H${x + w - r}Q${x + w},${y} ${x + w},${y + Math.min(r, h)}V${y + h}Z" fill="${col}"/>`);  // rounded top only
  const area = (d, col) => `<path d="${d}L${R},${B}L${L},${B}Z" fill="url(#vzF-${col})"/>`;  // soft fill under a curve that spans the plot
  const tag = (x, y, txt, col, anchor = "middle") => `<text x="${x}" y="${y}" text-anchor="${anchor}" class="vz-tag" fill="${col}">${txt}</text>`;
  const logTicks = (a, b) => { const t = []; for (let e = Math.ceil(a); e <= b; e++) t.push([10 ** e >= 1 ? 10 ** e : 10 ** e, sx(e, a, b)]); return t.map(([v, x]) => [v >= 1 ? v : v.toFixed(-Math.log10(v)), x]); };
  const hill = (d, ec, emax) => (emax * d) / (d + ec);

  // ---- widget shell: svg + controls + one plain-English readout; drag on the svg moves the main handle
  function shell(host, spec) {
    const el = document.createElement("div");
    el.className = "viz";
    el.innerHTML = `<div class="vz-top"><span class="vz-pill">Interactive</span><span class="vz-hint">${spec.hint || "Drag the chart or use the controls"}</span>
      <button type="button" class="vz-btn vz-reset" title="Back to the original figure's values">Reset</button><button type="button" class="vz-btn vz-swap">Original</button></div>
      <svg viewBox="0 0 ${W} ${spec.h || H}" role="img" aria-label="${spec.label}"></svg>
      <div class="vz-ctl">${spec.controls}</div><p class="vz-read" aria-live="polite"></p>`;
    host.prepend(el);
    const svg = el.querySelector("svg"), read = el.querySelector(".vz-read");
    const D = { ...spec.state }, S = { ...spec.state };
    const ctl = (n) => el.querySelector(`[name="${n}"]`);
    const sync = () => {
      el.querySelectorAll("input[type=range]").forEach((i) => {
        i.value = S[i.name]; i.style.setProperty("--p", `${((S[i.name] - i.min) / (i.max - i.min)) * 100}%`);
        const o = i.parentElement.querySelector("output"); if (o) o.textContent = (spec.fmt?.[i.name] || f1)(+S[i.name], S);
      });
      el.querySelectorAll(".seg[data-k] button").forEach((b) => { const on = String(S[b.parentElement.dataset.k]) === b.dataset.v; b.classList.toggle("on", on); b.setAttribute("aria-pressed", on); });
      const out = spec.draw(S); svg.innerHTML = DEFS + out.svg; read.innerHTML = out.read;
    };
    // after 30 s without a touch, glide back to the original figure's values (or right away with Reset)
    let idle = 0, held = false, anim = 0;
    const touch = () => { cancelAnimationFrame(anim); el.classList.add("dirty"); clearTimeout(idle); idle = setTimeout(() => (held ? touch() : reset()), 30000); };
    function reset() {
      clearTimeout(idle); cancelAnimationFrame(anim);
      const from = { ...S }, t0 = performance.now(), ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2);
      Object.keys(D).forEach((k) => { if (typeof D[k] !== "number") S[k] = D[k]; });
      const step = (now) => {
        const t = Math.min(1, (now - t0) / 900), e = ease(t);
        Object.keys(D).forEach((k) => { if (typeof D[k] === "number") S[k] = from[k] + (D[k] - from[k]) * e; });
        sync();
        if (t < 1) anim = requestAnimationFrame(step); else el.classList.remove("dirty");
      };
      anim = requestAnimationFrame(step);
    }
    el.querySelector(".vz-reset").onclick = reset;
    el.addEventListener("input", (e) => { if (e.target.name) { S[e.target.name] = +e.target.value; touch(); sync(); } });
    el.addEventListener("click", (e) => { const b = e.target.closest(".seg[data-k] button"); if (b) { const v = b.dataset.v; S[b.parentElement.dataset.k] = isNaN(+v) ? v : +v; spec.onSeg?.(S, b.parentElement.dataset.k); touch(); sync(); } });
    if (!spec.drag) el.classList.add("vz-static");
    if (spec.drag) {
      let on = false;
      const move = (e) => { const r = svg.getBoundingClientRect(); spec.drag(S, ((e.clientX - r.left) / r.width) * W, ((e.clientY - r.top) / r.height) * (spec.h || H), on === "start"); on = true; touch(); sync(); };
      svg.addEventListener("pointerdown", (e) => { on = "start"; held = true; svg.setPointerCapture(e.pointerId); move(e); });
      svg.addEventListener("pointermove", (e) => { if (on) move(e); });
      const up = () => { on = false; held = false; };
      svg.addEventListener("pointerup", up); svg.addEventListener("pointercancel", up);
    }
    sync();
    return { el, S, ctl };
  }
  const range = (name, label, min, max, step) => `<label class="vz-r"><span>${label}</span><output></output><input type="range" name="${name}" min="${min}" max="${max}" step="${step}"></label>`;
  const seg = (k, opts) => `<div class="seg" data-k="${k}">${opts.map(([v, t]) => `<button type="button" data-v="${v}">${t}</button>`).join("")}</div>`;

  const V = {};
  // log-dose axis shared by the receptor figures: 0.01 → 1000 (illustrative units)
  const LA = -2, LB = 3, lx = (d) => sx(Math.log10(d), LA, LB), xToD = (x) => 10 ** (LA + ((clamp(x, L, R) - L) / (R - L)) * (LB - LA));
  const yP = (v) => sy(v, 0, 110), yTicks = [0, 25, 50, 75, 100].map((v) => [v + "%", yP(v)]);

  // Figure 2 · the dose-response curve
  V.S31 = (host) => shell(host, {
    label: "Interactive dose-response curve", hint: "Drag along the curve to change the dose",
    state: { d: 3, ec: 0, emax: 100, scale: "log" },
    controls: seg("scale", [["log", "Log dose (sigmoid)"], ["lin", "Linear dose"]]) + range("ec", "EC₅₀", -1, 2, 0.05) + range("emax", "Emax", 20, 100, 1),
    fmt: { ec: (v) => f1(10 ** v) + " mg", emax: pct },
    drag: (S, x) => { S.d = S.scale === "log" ? xToD(x) : clamp(((x - L) / (R - L)) * 20, 0.01, 20); },
    draw(S) {
      const ec = 10 ** S.ec, e = hill(S.d, ec, S.emax), log = S.scale === "log";
      const X = log ? lx : (d) => sx(d, 0, 20), a = log ? 10 ** LA : 0.001, b = log ? 10 ** LB : 20;
      const curve = path((t) => { const d = log ? 10 ** t : t; return [X(d), yP(hill(d, ec, S.emax))]; }, log ? LA : 0, log ? LB : 20);
      const xt = log ? logTicks(LA, LB) : [0, 5, 10, 15, 20].map((v) => [v, sx(v, 0, 20)]);
      return {
        svg: axes(log ? "Dose (mg, log scale)" : "Dose (mg, linear scale)", "Response (% of max)", xt, yTicks) +
          `<line x1="${L}" x2="${R}" y1="${yP(S.emax)}" y2="${yP(S.emax)}" stroke="${C.coral}" stroke-dasharray="5 5"/>${tag(R - 4, yP(S.emax) - 6, "Emax (ceiling)", C.coral, "end")}
          <path d="M${L},${yP(S.emax / 2)}H${X(ec)}V${B}" fill="none" stroke="${C.blue}" stroke-dasharray="4 4"/>${tag(X(ec) + 6, B - 8, "EC₅₀", C.blue, "start")}
          ${area(curve, "teal")}<path d="${curve}" fill="none" stroke="${C.teal}" stroke-width="3" stroke-linecap="round"/>${dot(X(clamp(S.d, a, b)), yP(e), C.teal)}`,
        read: `At <b>${f1(S.d)} mg</b> the response is <b>${pct((100 * e) / S.emax)} of this drug's maximum</b>. ${S.d > 10 * ec ? "You're on the plateau: more drug adds almost nothing (ceiling effect)." : S.d < ec / 10 ? "Below the steep part: little effect yet." : "This is the steep middle, where small dose changes matter most."}${log ? "" : " On a linear axis the same curve looks hyperbolic; the log axis is what makes it an S."}`,
      };
    },
  });

  // Figure 1 · agonist with a competitive or noncompetitive antagonist
  V.S23 = (host) => shell(host, {
    label: "Interactive agonist and antagonist curves", hint: "Add antagonist, then drag to raise the agonist dose",
    state: { kind: "comp", b: 4, d: 30 },
    controls: seg("kind", [["comp", "Competitive"], ["non", "Noncompetitive / irreversible"]]) + range("b", "Antagonist", 0, 20, 0.5),
    fmt: { b: (v) => (v ? `${f1(v)}×` : "none") },
    drag: (S, x) => { S.d = xToD(x); },
    draw(S) {
      const comp = S.kind === "comp", ec = comp ? 1 + S.b : 1, emax = comp ? 100 : 100 / (1 + S.b / 2);
      const base = path((t) => [lx(10 ** t), yP(hill(10 ** t, 1, 100))], LA, LB), cur = path((t) => [lx(10 ** t), yP(hill(10 ** t, ec, emax))], LA, LB);
      const e = hill(S.d, ec, emax);
      return {
        svg: axes("Agonist dose (log scale)", "Response (% of max)", logTicks(LA, LB), yTicks) +
          `<path d="${base}" fill="none" stroke="${C.teal}" stroke-width="3" opacity=".35"/>${tag(lx(0.02), yP(hill(0.02, 1, 100)) - 40, "Agonist alone", C.teal, "start")}
          <path d="${cur}" fill="none" stroke="${C.coral}" stroke-width="3" stroke-linecap="round"/>${dot(lx(S.d), yP(e), C.coral)}
          ${comp ? "" : `<line x1="${L}" x2="${R}" y1="${yP(emax)}" y2="${yP(emax)}" stroke="${C.coral}" stroke-dasharray="5 5"/>${tag(R - 4, yP(emax) - 6, `new ceiling ${pct(emax)}`, C.coral, "end")}`}`,
        read: !S.b ? "No antagonist: the agonist alone. Add some with the slider." : comp
          ? `Competitive: the curve <b>shifts right</b> (you need more agonist for the same effect), but <b>Emax is unchanged</b>. At an agonist dose of ${f1(S.d)} the response is ${pct(e)}. Drag far right: enough agonist still reaches the full 100%, it <b>surmounts</b> the block.`
          : `Noncompetitive/irreversible: the <b>maximum drops to ${pct(emax)}</b>. At an agonist dose of ${f1(S.d)} the response is ${pct(e)}. Drag far right: no amount of agonist gets back above ${pct(emax)}, it is <b>insurmountable</b>.`,
      };
    },
  });

  // Figure 3 · potency vs efficacy
  V.S35 = (host) => shell(host, {
    label: "Interactive potency versus efficacy", hint: "Change Drug B and compare it with Drug A",
    state: { ec: 1, emax: 100 },
    controls: range("ec", "Drug B EC₅₀", -1, 2, 0.05) + range("emax", "Drug B Emax", 20, 100, 1),
    fmt: { ec: (v) => f1(10 ** v) + " mg", emax: pct },
    draw(S) {
      const ecB = 10 ** S.ec, A = path((t) => [lx(10 ** t), yP(hill(10 ** t, 1, 100))], LA, LB), Bp = path((t) => [lx(10 ** t), yP(hill(10 ** t, ecB, S.emax))], LA, LB);
      const pot = Math.abs(S.ec) < 0.03 ? "Same potency" : S.ec > 0 ? "<b>Drug A is more potent</b> (lower EC₅₀: less drug for half its max)" : "<b>Drug B is more potent</b> (lower EC₅₀)";
      const eff = S.emax >= 99.5 ? "same efficacy (both reach 100%)" : `<b>Drug A is more efficacious</b> (higher Emax: ${pct(100)} vs ${pct(S.emax)})`;
      return {
        svg: axes("Dose (mg, log scale)", "Response (% of max)", logTicks(LA, LB), yTicks) +
          `<path d="${A}" fill="none" stroke="${C.teal}" stroke-width="3" stroke-linecap="round"/><path d="${Bp}" fill="none" stroke="${C.amber}" stroke-width="3" stroke-linecap="round" stroke-dasharray="8 5"/>
          ${dot(lx(1), yP(50), C.teal, 5)}${dot(lx(ecB), yP(S.emax / 2), C.amber, 5)}
          ${tag(L + 10, T + 14, "— Drug A (EC₅₀ 1 mg, Emax 100%)", C.teal, "start")}${tag(L + 10, T + 34, "- - Drug B", "#b9781c", "start")}`,
        read: `${pot}; ${eff}. Remember: <b>efficacy usually matters more clinically</b> than potency; a less potent drug just needs a bigger dose.`,
      };
    },
  });

  // Quantal curves: % of people responding vs % with toxicity (therapeutic index)
  const quantal = (host, label) => shell(host, {
    label, hint: "Drag to set a dose; slide ED₅₀ and TD₅₀ apart or together",
    state: { ed: 0, td: 1.6, d: 0.6 },
    controls: range("ed", "ED₅₀", -1, 1.5, 0.05) + range("td", "TD₅₀", -0.5, 2.5, 0.05),
    fmt: { ed: (v) => f1(10 ** v) + " mg", td: (v) => f1(10 ** v) + " mg" },
    drag: (S, x) => { S.d = Math.log10(xToD(x)); },
    draw(S) {
      if (S.td < S.ed) S.td = S.ed;
      const q = (t, m) => 100 / (1 + Math.exp(-(t - m) * 5)), ti = 10 ** (S.td - S.ed);
      const eff = path((t) => [sx(t, LA, LB), yP(q(t, S.ed))], LA, LB), tox = path((t) => [sx(t, LA, LB), yP(q(t, S.td))], LA, LB);
      const gap = sx(S.td, LA, LB) - sx(S.ed, LA, LB), narrow = ti < 3;
      return {
        svg: axes("Dose (mg, log scale)", "% of people", logTicks(LA, LB), yTicks) +
          `<rect x="${sx(S.ed, LA, LB)}" y="${T}" width="${Math.max(0, gap)}" height="${B - T}" fill="${narrow ? C.coral : C.sage}" opacity=".13"/>
          <path d="${eff}" fill="none" stroke="${C.teal}" stroke-width="3" stroke-linecap="round"/><path d="${tox}" fill="none" stroke="${C.coral}" stroke-width="3" stroke-linecap="round"/>
          ${tag(sx(S.ed, LA, LB) - 10, yP(50), "therapeutic (ED₅₀)", C.teal, "end")}${tag(sx(S.td, LA, LB) + 10, yP(50) + 16, "toxic (TD₅₀)", C.coral, "start")}
          <line x1="${sx(S.d, LA, LB)}" x2="${sx(S.d, LA, LB)}" y1="${T}" y2="${B}" stroke="${C.deep}" stroke-dasharray="3 4"/>
          ${dot(sx(S.d, LA, LB), yP(q(S.d, S.ed)), C.teal, 5)}${dot(sx(S.d, LA, LB), yP(q(S.d, S.td)), C.coral, 5)}`,
        read: `<b>TI = TD₅₀ ÷ ED₅₀ = ${f1(ti)}</b>. At ${f1(10 ** S.d)} mg, <b>${pct(q(S.d, S.ed))}</b> of people get the therapeutic effect and <b>${pct(q(S.d, S.td))}</b> have toxicity. ${narrow ? "The curves nearly overlap: a <b>narrow</b> index, little room for error, so these drugs need careful dosing and level monitoring." : "A wide gap between the curves: a dose that helps most people harms few."}`,
      };
    },
  });
  V.TB_quantal = (host) => quantal(host, "Interactive quantal dose-response and therapeutic window");
  V.S39 = (host) => quantal(host, "Interactive therapeutic index");

  // Figure 6 · CYP450 inhibition vs induction (the bar chart)
  V.S7 = (host) => {
    let shown = [100, 100, 100], raf = 0;
    const w = shell(host, {
      label: "Interactive CYP450 inhibitor and inducer bar chart", hint: "Pick an interaction and set its strength",
      state: { mode: "both", s: 1 },
      controls: seg("mode", [["both", "Compare all"], ["inh", "+ Inhibitor"], ["ind", "+ Inducer"]]) + range("s", "Strength", 0, 1, 0.01),
      fmt: { s: (v) => (v < 0.34 ? "weak" : v < 0.67 ? "moderate" : "strong") },
      draw(S) {
        const inh = 100 + 140 * S.s, ind = 100 - 58 * S.s;
        const want = S.mode === "inh" ? [100, inh, 100] : S.mode === "ind" ? [100, 100, ind] : [100, inh, ind];
        cancelAnimationFrame(raf);
        const step = () => { shown = shown.map((v, i) => v + (want[i] - v) * 0.2); if (shown.some((v, i) => Math.abs(v - want[i]) > 0.3)) { raf = requestAnimationFrame(step); paint(); } else { shown = want; paint(); } };
        raf = requestAnimationFrame(step);
        const lvl = S.mode === "ind" ? ind : S.mode === "inh" ? inh : null;
        return { svg: bars(shown), read: S.mode === "both"
          ? `Same substrate drug, same dose. An <b>inhibitor raises</b> its level to <b>${pct(inh)}</b> of baseline (toxicity risk); an <b>inducer lowers</b> it to <b>${pct(ind)}</b> (risk of losing effect).`
          : S.mode === "inh" ? `Inhibitor: metabolism slows, so the substrate builds up to <b>${pct(lvl)}</b>${lvl > 160 ? ", above the window: <b>toxicity risk</b>, consider a lower dose" : ", still inside the window"}.`
          : `Inducer: more enzyme, faster metabolism, the level falls to <b>${pct(lvl)}</b>${lvl < 60 ? ", below the window: <b>therapeutic failure</b> risk" : ", still inside the window"}.` };
      },
    });
    function bars(v) {
      const y = (p) => sy(p, 0, 260), cols = [C.teal, C.coral, C.blue], names = ["Normal", "+ Inhibitor", "+ Inducer"];
      return axes("", "Drug level (% of baseline)", [], [0, 50, 100, 150, 200, 250].map((t) => [t, y(t)])) +
        `<rect x="${L}" y="${y(160)}" width="${R - L}" height="${y(60) - y(160)}" fill="${C.sage}" opacity=".1"/>${tag(R - 4, y(132), "therapeutic", C.sage, "end")}${tag(R - 4, y(132) + 15, "window", C.sage, "end")}
        ${tag(R - 4, y(160) - 6, "toxicity risk ↑", C.coral, "end")}${tag(R - 4, y(60) + 16, "too low ↓", C.blue, "end")}
        <line x1="${L}" x2="${R}" y1="${y(100)}" y2="${y(100)}" stroke="${C.ink}" stroke-dasharray="2 4"/>` +
        v.map((p, i) => { const cx = L + 70 + i * 135; return `${bar(cx - 46, y(p), 92, B - y(p), cols[i])}${tag(cx, y(p) - 8, pct(p), C.deep)}<text x="${cx}" y="${B + 19}" text-anchor="middle" class="vz-tk">${names[i]}</text>`; }).join("");
    }
    function paint() { w.el.querySelector("svg").innerHTML = DEFS + bars(shown); }
    return w;
  };

  // Figure 7 · exponential decay over half-lives
  V.S20 = (host) => shell(host, {
    label: "Interactive half-life decay", hint: "Drag through time",
    state: { n: 2, th: 6 },
    controls: range("n", "Time", 0, 6, 0.05) + range("th", "Half-life", 1, 48, 1),
    fmt: { n: (v) => `${f1(v)} half-lives`, th: (v) => `${v} h` },
    drag: (S, x) => { S.n = clamp(((x - L) / (R - L)) * 6, 0, 6); },
    draw(S) {
      const c = 100 * 0.5 ** S.n, curve = path((t) => [sx(t, 0, 6), sy(100 * 0.5 ** t, 0, 110)], 0, 6);
      const marks = [1, 2, 3, 4, 5].map((k) => `<circle cx="${sx(k, 0, 6)}" cy="${sy(100 * 0.5 ** k, 0, 110)}" r="3.5" fill="${C.teal}"/>${tag(sx(k, 0, 6) + 4, sy(100 * 0.5 ** k, 0, 110) - 9, f1(100 * 0.5 ** k) + "%", C.ink, "start")}`).join("");
      return {
        svg: axes("Time (half-lives)", "Concentration (% of start)", [0, 1, 2, 3, 4, 5, 6].map((v) => [v, sx(v, 0, 6)]), [0, 25, 50, 75, 100].map((v) => [v, sy(v, 0, 110)])) +
          `${area(curve, "teal")}<path d="${curve}" fill="none" stroke="${C.teal}" stroke-width="3" stroke-linecap="round"/>${marks}${dot(sx(S.n, 0, 6), sy(c, 0, 110), C.teal)}`,
        read: `After <b>${f1(S.n)} half-lives</b> (${f1(S.n * S.th)} h if t½ = ${S.th} h): <b>${f1(c)}% remains</b>, ${f1(100 - c)}% eliminated. Each half-life removes half of what's left, so after ~5 half-lives about 97% is gone.`,
      };
    },
  });

  // Figure 8 · steady state with and without a loading dose
  V.S24 = (host) => shell(host, {
    label: "Interactive steady state and loading dose", hint: "Drag through time; toggle the loading dose",
    state: { load: 1, tau: 1, t: 4 },
    controls: seg("load", [[1, "With loading dose"], [0, "Maintenance only"]]) + range("tau", "Dose every", 0.5, 2, 0.25) + range("t", "Time", 0, 9, 0.05),
    fmt: { tau: (v) => `${f1(v)} × t½`, t: (v) => `${f1(v)} t½` },
    drag: (S, x) => { S.t = clamp(((x - L) / (R - L)) * 9, 0, 9); },
    draw(S) {
      const k = Math.LN2, acc = 1 / (1 - Math.exp(-k * S.tau)), peakSS = 100 * acc;
      const conc = (t, load) => { let c = 0; for (let j = 0; j * S.tau <= t + 1e-9; j++) c += (j === 0 && load ? 100 * acc : 100) * Math.exp(-k * (t - j * S.tau)); return c; };
      const top = Math.ceil((peakSS * 1.1) / 50) * 50, Y = (v) => sy(v, 0, top);
      const line = (load) => path((t) => [sx(t, 0, 9), Y(conc(t, load))], 0, 9, 540);
      const avgSS = 100 / (k * S.tau), frac = 1 - 0.5 ** S.t;
      return {
        svg: axes("Time (half-lives)", "Concentration (relative)", Array.from({ length: 10 }, (_, i) => [i, sx(i, 0, 9)]), Array.from({ length: top / 50 + 1 }, (_, i) => [i * 50, Y(i * 50)])) +
          `<line x1="${L}" x2="${R}" y1="${Y(avgSS)}" y2="${Y(avgSS)}" stroke="${C.ink}" stroke-dasharray="2 4"/>${tag(R - 4, Y(avgSS) - 6, "average at steady state", C.ink, "end")}
          <path d="${line(0)}" fill="none" stroke="${C.teal}" stroke-width="3" opacity="${S.load ? 0.35 : 1}"/>${S.load ? `<path d="${line(1)}" fill="none" stroke="${C.amber}" stroke-width="3" stroke-linecap="round" stroke-dasharray="9 5"/>` : ""}
          <line x1="${sx(S.t, 0, 9)}" x2="${sx(S.t, 0, 9)}" y1="${T}" y2="${B}" stroke="${C.deep}" stroke-dasharray="3 4"/>${dot(sx(S.t, 0, 9), Y(conc(S.t, S.load)), S.load ? C.amber : C.teal, 6)}`,
        read: S.load
          ? `With a <b>loading dose</b> the level starts at the target right away. Without one (faint line), at ${f1(S.t)} half-lives you'd be at <b>${pct(100 * frac)}</b> of steady state.`
          : `<b>Maintenance only</b>: at ${f1(S.t)} half-lives you're at <b>${pct(100 * frac)}</b> of steady state; it takes about <b>4–5 half-lives</b> to get there. ${S.tau > 1 ? "Dosing less often than every half-life makes the peaks and troughs swing wider." : S.tau < 1 ? "Dosing more often than every half-life flattens the swings and raises the level." : ""}`,
      };
    },
  });

  // Textbook concept · five to fill, five to empty
  V.TB_fill_empty = (host) => shell(host, {
    label: "Interactive five to fill, five to empty", hint: "Drag or slide through the half-lives",
    state: { n: 3, mode: "fill" },
    controls: seg("mode", [["fill", "Start dosing (fill)"], ["empty", "Stop dosing (empty)"]]) + range("n", "Half-lives", 0, 6, 0.05),
    fmt: { n: f1 },
    drag: (S, x) => { S.n = clamp(((x - L) / (R - L)) * 6, 0, 6); },
    draw(S) {
      const fill = S.mode === "fill", v = (t) => (fill ? 100 * (1 - 0.5 ** t) : 100 * 0.5 ** t), c = v(S.n);
      const steps = [1, 2, 3, 4, 5].map((k) => `<line x1="${sx(k, 0, 6)}" x2="${sx(k, 0, 6)}" y1="${B}" y2="${sy(v(k), 0, 110)}" stroke="${C.grid}"/>${tag(sx(k, 0, 6), sy(v(k), 0, 110) + (fill ? -10 : -10), f1(v(k)) + "%", C.ink)}`).join("");
      return {
        svg: axes("Time (half-lives)", fill ? "% of steady state" : "% of drug remaining", [0, 1, 2, 3, 4, 5, 6].map((t) => [t, sx(t, 0, 6)]), [0, 25, 50, 75, 100].map((t) => [t, sy(t, 0, 110)])) +
          steps + `${area(path((t) => [sx(t, 0, 6), sy(v(t), 0, 110)], 0, 6), fill ? "teal" : "coral")}<path d="${path((t) => [sx(t, 0, 6), sy(v(t), 0, 110)], 0, 6)}" fill="none" stroke="${fill ? C.teal : C.coral}" stroke-width="3" stroke-linecap="round"/>${dot(sx(S.n, 0, 6), sy(c, 0, 110), fill ? C.teal : C.coral)}`,
        read: fill ? `After <b>${f1(S.n)} half-lives</b> of regular dosing you're at <b>${f1(c)}%</b> of steady state. Each half-life closes half the remaining gap: 50 → 75 → 87.5 → 93.75 → ~97%.`
          : `<b>${f1(S.n)} half-lives</b> after the last dose, <b>${f1(c)}%</b> remains. Same math in reverse: after ~5 half-lives about 97% is gone.`,
      };
    },
  });

  // Figure 5 · ADME: where an oral dose goes vs an IV dose
  V.S46 = (host) => shell(host, {
    label: "Interactive ADME pathway", h: 266, hint: "Switch the route and change first-pass loss",
    state: { route: "oral", fp: 50 },
    controls: seg("route", [["iv", "IV"], ["oral", "Oral"], ["sl", "Sublingual"]]) + range("fp", "First-pass loss", 0, 90, 1),
    fmt: { fp: pct },
    draw(S) {
      const lost = S.route === "oral" ? S.fp : 0, F = 100 - lost;
      const box = (x, y, w, t, sub, col, on = true) => `<g opacity="${on ? 1 : 0.28}"><rect x="${x}" y="${y}" width="${w}" height="58" rx="12" fill="${col}" opacity=".12" stroke="${col}"/>${tag(x + w / 2, y + 25, t, col)}<text x="${x + w / 2}" y="${y + 44}" text-anchor="middle" class="vz-ax-t">${sub}</text></g>`;
      const arrow = (x1, y1, x2, y2, w, col, on = true) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="${Math.max(1.5, w)}" stroke-linecap="round" opacity="${on ? 0.85 : 0.15}" marker-end="url(#vzA)"/>`;
      const oral = S.route === "oral";
      return {
        svg: "" +
          box(10, 40, 120, "Dose", S.route === "iv" ? "IV injection" : S.route === "sl" ? "under the tongue" : "swallowed", C.deep) +
          box(175, 0, 140, "Gut → portal vein", "absorption", C.amber, oral) + box(175, 100, 140, "Liver (1st pass)", `${pct(lost)} metabolized`, C.coral, oral) +
          box(380, 40, 160, "Systemic blood", `${pct(F)} reaches it`, C.teal) +
          box(330, 200, 92, "Tissues", "distribution", C.blue) + box(430, 200, 92, "Liver", "metabolism", C.coral) + box(530, 200, 92, "Kidney", "excretion", C.sage) +
          (oral ? arrow(130, 60, 172, 36, 5, C.amber) + arrow(245, 58, 245, 97, 5, C.amber) + arrow(315, 125, 377, 84, Math.max(1.5, 5 * F / 100), C.teal)
                : arrow(130, 69, 377, 69, 5, C.teal)) +
          arrow(420, 98, 380, 197, 3, C.blue) + arrow(460, 98, 476, 197, 3, C.coral) + arrow(500, 98, 572, 197, 3, C.sage),
        read: S.route === "iv" ? "IV goes straight into systemic blood: <b>bioavailability 100%</b>, no first pass."
          : S.route === "sl" ? "Sublingual drug enters systemic veins directly, <b>bypassing the portal vein and liver</b>: no first-pass loss."
          : `Oral drug is absorbed into the portal vein and passes the liver first: <b>${pct(lost)}</b> is lost, so <b>bioavailability is ${pct(F)}</b>. ${lost >= 60 ? "A large first-pass effect is why the oral dose must be much higher than the IV dose." : ""}`,
      };
    },
  });

  // ---- enhance every figure that has an interactive twin; the original image stays one tap away
  function enhance(fig) {
    const key = fig.dataset.viz, make = V[key];
    if (!make || fig.dataset.vizOn) return;
    fig.dataset.vizOn = 1;
    make(fig);
    const t = fig.querySelector(".vz-swap");
    t.onclick = () => { const o = fig.classList.toggle("vz-orig"); t.textContent = o ? "Interactive" : "Original"; };
    // with the original showing, the header stays so you can switch back
    fig.querySelector(".viz").after(Object.assign(document.createElement("div"), { className: "vz-back" }));
    fig.querySelector(".vz-back").append(Object.assign(document.createElement("button"), { type: "button", className: "vz-btn", textContent: "Back to interactive", onclick: () => t.click() }));
  }
  const io = "IntersectionObserver" in window ? new IntersectionObserver((es) => es.forEach((e) => { if (e.isIntersecting) { io.unobserve(e.target); enhance(e.target); } }), { rootMargin: "300px" }) : null;
  document.querySelectorAll("[data-viz]").forEach((f) => (io ? io.observe(f) : enhance(f)));
  window.dpasViz = V;
})();
