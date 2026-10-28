// Hands-on figures: each lecture diagram (by its image name) gets an interactive twin you can drag and adjust.
// Same illustrative models and values as the original figures; the original stays one tap away and in print/PDF.
(function () {
  // colors come from the site's palette (CSS variables), re-read on every draw so light/dark mode just works
  const C = { teal: "#0a84ff", coral: "#ff375f", amber: "#ff9f0a", blue: "#af52de", deep: "#1d1d1f", sage: "#34c759", grid: "#ececf0", ink: "#86868b", bg: "#fff" };
  function palette(el) {
    const cs = getComputedStyle(el), v = (n, d) => cs.getPropertyValue(n).trim() || d;
    Object.assign(C, { teal: v("--vz-1", C.teal), coral: v("--vz-2", C.coral), amber: v("--vz-3", C.amber), blue: v("--vz-4", C.blue), sage: v("--vz-5", C.sage),
      deep: v("--vz-text", C.deep), grid: v("--vz-grid", C.grid), ink: v("--vz-ink", C.ink), bg: v("--vz-bg", C.bg) });
  }
  const W = 640, H = 330, L = 46, R = 620, T = 34, B = 290;  // plot box inside the viewBox
  // shared defs: a soft shadow for handles, an arrowhead, and a fading fill for each series color
  const DEFS = () => `<defs><filter id="vzSh" x="-50%" y="-50%" width="200%" height="200%"><feDropShadow dx="0" dy="1.5" stdDeviation="2" flood-color="#000" flood-opacity=".22"/></filter>
    <marker id="vzA" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="9" markerHeight="9" markerUnits="userSpaceOnUse" orient="auto"><path d="M1,1L9,5L1,9" fill="none" stroke="${C.ink}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></marker>
    <linearGradient id="vzGloss" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".30"/><stop offset=".45" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <filter id="vzBarSh" x="-20%" y="-10%" width="140%" height="130%"><feDropShadow dx="0" dy="3" stdDeviation="4" flood-color="#000" flood-opacity=".12"/></filter>
    <filter id="vzSoft" x="-20%" y="-30%" width="140%" height="170%"><feDropShadow dx="0" dy="5" stdDeviation="7" flood-color="#000" flood-opacity=".09"/></filter>
    ${["teal", "coral", "amber", "blue"].map((k) => `<linearGradient id="vzF-${k}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="${C[k]}" stop-opacity=".22"/><stop offset="1" stop-color="${C[k]}" stop-opacity="0"/></linearGradient>`).join("")}</defs>`;
  const sx = (v, a, b) => L + ((v - a) / (b - a)) * (R - L), sy = (v, a, b) => B - ((v - a) / (b - a)) * (B - T);
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  const f1 = (v) => (Math.abs(v) >= 100 ? Math.round(v) : Math.abs(v) >= 10 ? Math.round(v * 10) / 10 : Math.round(v * 100) / 100).toLocaleString();
  const pct = (v) => `${Math.round(v)}%`;
  const path = (fn, a, b, n = 140) => Array.from({ length: n + 1 }, (_, i) => { const x = a + ((b - a) * i) / n, p = fn(x); return `${i ? "L" : "M"}${p[0].toFixed(1)},${p[1].toFixed(1)}`; }).join("");
  // quiet axes: hairline grid, no y-axis line, gray tick labels, the unit written once at top-left
  const axes = (xl, yl, xt, yt) => `<g class="vz-ax">${yt.map(([v, y]) => `<line x1="${L}" x2="${R}" y1="${y}" y2="${y}" stroke="${C.grid}"/><text class="vz-tk" x="${L - 8}" y="${y + 4}" text-anchor="end">${v}</text>`).join("")}
    ${xt.map(([v, x]) => `<text class="vz-tk" x="${x}" y="${B + 19}" text-anchor="middle">${v}</text>`).join("")}
    <line x1="${L}" x2="${R}" y1="${B}" y2="${B}" stroke="${C.ink}" stroke-opacity=".45"/>
    ${xl ? `<text x="${R}" y="${H - 2}" text-anchor="end" class="vz-lab">${xl}</text>` : ""}${yl ? `<text x="${L - 8}" y="${T - 16}" text-anchor="start" class="vz-lab">${yl}</text>` : ""}</g>`;
  const dot = (x, y, col, r = 7) => `<circle cx="${x}" cy="${y}" r="${r + 9}" fill="${col}" opacity=".12"/><circle cx="${x}" cy="${y}" r="${r}" fill="${C.bg}" stroke="${col}" stroke-width="3" filter="url(#vzSh)" class="vz-dot"/>`;
  // a rounded column with a soft top-lit sheen and a quiet shadow under it
  const bar = (x, y, w, h, col) => {
    if (h <= 0) return "";
    const r = Math.min(10, w * 0.14, h), d = `M${x},${y + h}V${y + r}Q${x},${y} ${x + r},${y}H${x + w - r}Q${x + w},${y} ${x + w},${y + r}V${y + h}Z`;
    return `<path d="${d}" fill="${col}" filter="url(#vzBarSh)"/><path d="${d}" fill="url(#vzGloss)"/>`;
  };
  const area = (d, col) => `<path d="${d}L${R},${B}L${L},${B}Z" fill="url(#vzF-${col})"/>`;  // soft fill under a curve that spans the plot
  const tag = (x, y, txt, col, anchor = "middle") => `<text x="${x}" y="${y}" text-anchor="${anchor}" class="vz-tag" fill="${col}">${txt}</text>`;
  const logTicks = (a, b) => { const t = []; for (let e = Math.ceil(a); e <= b; e++) t.push([10 ** e >= 1 ? 10 ** e : 10 ** e, sx(e, a, b)]); return t.map(([v, x]) => [v >= 1 ? v : v.toFixed(-Math.log10(v)), x]); };
  const hill = (d, ec, emax) => (emax * d) / (d + ec);

  // morph the live SVG toward new markup: same elements, new attributes (CSS transitions do the in-between)
  const NS = "http://www.w3.org/2000/svg";
  function morph(a, b) {
    if (a.nodeName !== b.nodeName || a.childElementCount !== b.childElementCount) { a.replaceWith(b.cloneNode(true)); return; }
    for (const { name } of [...a.attributes]) if (!b.hasAttribute(name)) a.removeAttribute(name);
    for (const { name, value } of [...b.attributes]) if (a.getAttribute(name) !== value) a.setAttribute(name, value);
    if (!b.childElementCount) { if (a.textContent !== b.textContent) a.textContent = b.textContent; return; }
    [...a.children].forEach((c, i) => morph(c, b.children[i]));
  }
  function patch(svg, markup) {
    const t = document.createElementNS(NS, "svg"); t.innerHTML = markup;
    if (svg.childElementCount !== t.childElementCount || [...svg.children].some((c, i) => c.nodeName !== t.children[i].nodeName)) { svg.innerHTML = markup; return; }
    [...svg.children].forEach((c, i) => morph(c, t.children[i]));
  }

  // each figure keeps its own gradient/filter/marker ids: with shared ids a hidden figure (home carousel) would own
  // the definitions and the visible one would draw without them
  let UID = 0;
  const scope = (svg, markup) => { svg.dataset.uid ||= String(++UID); return markup.replace(/(id="|url\(#)vz/g, `$1v${svg.dataset.uid}z`); };

  const LEG = { teal: "--vz-1", coral: "--vz-2", amber: "--vz-3", blue: "--vz-4", sage: "--vz-5", ink: "--vz-ink" };

  // ---- widget shell: svg + controls + one plain-English readout; drag on the svg moves the main handle
  function shell(host, spec) {
    const el = document.createElement("div");
    el.className = "viz";
    el.innerHTML = `<div class="vz-top"><span class="vz-pill">Interactive</span><span class="vz-hint">${spec.hint || "Drag the chart or use the controls"}</span>
      <button type="button" class="vz-btn vz-reset" title="Back to the original figure's values">Reset</button><button type="button" class="vz-btn vz-swap">Original</button></div>
      ${spec.point ? `<p class="vz-point">${spec.point}</p>` : ""}
      ${spec.legend ? `<div class="vz-legend">${spec.legend.map(([k, t, dash]) => `<span><i class="${dash ? "dash" : ""}" style="--c:var(${LEG[k]})"></i>${t}</span>`).join("")}</div>` : ""}
      <svg viewBox="0 0 ${W} ${spec.h || H}" role="img" aria-label="${spec.label}"></svg>
      ${spec.steps ? `<div class="vz-steps"><span class="vz-try">Try it</span>${spec.steps.map((st, i) => `<button type="button" data-step="${i}"><b>${i + 1}</b>${st.label}</button>`).join("")}</div>` : ""}
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
      palette(el);
      const out = spec.draw(S); patch(svg, scope(svg, DEFS() + out.svg)); read.innerHTML = out.read;
    };
    // after 30 s without a touch, glide back to the original figure's values (or right away with Reset)
    let idle = 0, held = false, anim = 0;
    const touch = () => { cancelAnimationFrame(anim); el.classList.add("dirty"); clearTimeout(idle); idle = setTimeout(() => (held ? touch() : reset()), 30000); };
    // glide every number to a target state (switches flip at the start); Reset and the "Try it" steps share it
    function glide(target, done) {
      cancelAnimationFrame(anim);
      const from = { ...S }, t0 = performance.now(), ease = (t) => (t < 0.5 ? 4 * t * t * t : 1 - (-2 * t + 2) ** 3 / 2);
      Object.keys(target).forEach((k) => { if (typeof target[k] !== "number") S[k] = target[k]; });
      const step = (now) => {
        const t = Math.min(1, (now - t0) / 900), e = ease(t);
        Object.keys(target).forEach((k) => { if (typeof target[k] === "number") S[k] = from[k] + (target[k] - from[k]) * e; });
        el.classList.add("live"); sync();
        if (t < 1) anim = requestAnimationFrame(step); else { el.classList.remove("live"); done?.(); }
      };
      anim = requestAnimationFrame(step);
    }
    const stepBtns = [...el.querySelectorAll("[data-step]")];
    const mark = (i) => stepBtns.forEach((b, k) => b.classList.toggle("on", k === i));
    function reset() { clearTimeout(idle); mark(-1); glide(D, () => el.classList.remove("dirty")); }
    el.querySelector(".vz-reset").onclick = reset;
    stepBtns.forEach((b) => (b.onclick = () => { const i = +b.dataset.step; mark(i); touch(); glide({ ...D, ...spec.steps[i].state }); }));
    let liveT = 0;
    const live = () => { el.classList.add("live"); clearTimeout(liveT); liveT = setTimeout(() => el.classList.remove("live"), 180); };
    el.addEventListener("input", (e) => { if (e.target.name) { S[e.target.name] = +e.target.value; mark(-1); live(); touch(); sync(); } });
    el.addEventListener("click", (e) => { const b = e.target.closest(".seg[data-k] button"); if (b) { const v = b.dataset.v; S[b.parentElement.dataset.k] = isNaN(+v) ? v : +v; spec.onSeg?.(S, b.parentElement.dataset.k); touch(); sync(); } });
    if (!spec.drag) el.classList.add("vz-static");
    if (spec.drag) {
      let on = false;
      const move = (e) => { live(); const r = svg.getBoundingClientRect(); spec.drag(S, ((e.clientX - r.left) / r.width) * W, ((e.clientY - r.top) / r.height) * (spec.h || H), on === "start"); on = true; touch(); sync(); };
      svg.addEventListener("pointerdown", (e) => { on = "start"; held = true; try { svg.setPointerCapture(e.pointerId); } catch { /* pointer already gone */ } move(e); });
      svg.addEventListener("pointermove", (e) => { if (on) move(e); });
      const up = () => { on = false; held = false; };
      svg.addEventListener("pointerup", up); svg.addEventListener("pointercancel", up);
    }
    if (matchMedia("(hover: hover) and (prefers-reduced-motion: no-preference)").matches) {
      const flat = () => svg.style.setProperty("--tilt", "rotateX(0deg) rotateY(0deg)");
      el.addEventListener("pointermove", (e) => {
        if (held) return flat();
        const r = svg.getBoundingClientRect(), dx = (e.clientX - r.left) / r.width - 0.5, dy = (e.clientY - r.top) / r.height - 0.5;
        if (Math.abs(dx) > 0.6 || Math.abs(dy) > 0.6) return flat();
        svg.style.setProperty("--tilt", `rotateX(${(-dy * 2).toFixed(2)}deg) rotateY(${(dx * 2.5).toFixed(2)}deg)`);
      });
      el.addEventListener("pointerleave", flat); svg.addEventListener("pointerdown", flat);
    }
    el.classList.add("intro"); sync(); setTimeout(() => el.classList.remove("intro"), 1600);
    matchMedia("(prefers-color-scheme: dark)").addEventListener?.("change", () => sync());
    new MutationObserver(() => sync()).observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme", "data-paccent"] });
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
    point: "Effect climbs steeply through the middle, then flattens: past the ceiling, more drug adds side effects, not benefit.",
    legend: [["teal", "Response"], ["coral", "Emax: the ceiling", 1], ["blue", "EC₅₀: half of Emax", 1]],
    steps: [{ label: "Low dose", state: { d: 0.08 } }, { label: "At EC₅₀", state: { d: 1 } }, { label: "On the plateau", state: { d: 300 } }, { label: "Same curve, linear axis", state: { scale: "lin", d: 6 } }],
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
          ${area(curve, "teal")}<path d="${curve}" fill="none" stroke="${C.teal}" stroke-width="3" stroke-linecap="round" class="vz-line" pathLength="1"/>${dot(X(clamp(S.d, a, b)), yP(e), C.teal)}`,
        read: `At <b>${f1(S.d)} mg</b> the response is <b>${pct((100 * e) / S.emax)} of this drug's maximum</b>. ${S.d > 10 * ec ? "You're on the plateau: more drug adds almost nothing (ceiling effect)." : S.d < ec / 10 ? "Below the steep part: little effect yet." : "This is the steep middle, where small dose changes matter most."}${log ? "" : " On a linear axis the same curve looks hyperbolic; the log axis is what makes it an S."}`,
      };
    },
  });

  // Figure 1 · agonist with a competitive or noncompetitive antagonist
  V.S23 = (host) => shell(host, {
    label: "Interactive agonist and antagonist curves", hint: "Add antagonist, then drag to raise the agonist dose",
    point: "A competitive antagonist can be outcompeted (curve shifts right, same ceiling). A noncompetitive or irreversible one lowers the ceiling.",
    legend: [["teal", "Agonist alone"], ["coral", "Agonist + antagonist"]],
    steps: [{ label: "Add a competitive antagonist", state: { kind: "comp", b: 4, d: 1 } }, { label: "Flood with agonist", state: { kind: "comp", b: 4, d: 800 } }, { label: "Make it irreversible", state: { kind: "non", b: 4, d: 800 } }],
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
          <path d="${cur}" fill="none" stroke="${C.coral}" stroke-width="3" stroke-linecap="round" class="vz-line" pathLength="1"/>${dot(lx(S.d), yP(e), C.coral)}
          <g opacity="${comp ? 0 : 1}"><line x1="${L}" x2="${R}" y1="${yP(emax)}" y2="${yP(emax)}" stroke="${C.coral}" stroke-dasharray="5 5"/>${tag(R - 4, yP(emax) - 6, `new ceiling ${pct(emax)}`, C.coral, "end")}</g>`,
        read: !S.b ? "No antagonist: the agonist alone. Add some with the slider." : comp
          ? `Competitive: the curve <b>shifts right</b> (you need more agonist for the same effect), but <b>Emax is unchanged</b>. At an agonist dose of ${f1(S.d)} the response is ${pct(e)}. Drag far right: enough agonist still reaches the full 100%, it <b>surmounts</b> the block.`
          : `Noncompetitive/irreversible: the <b>maximum drops to ${pct(emax)}</b>. At an agonist dose of ${f1(S.d)} the response is ${pct(e)}. Drag far right: no amount of agonist gets back above ${pct(emax)}, it is <b>insurmountable</b>.`,
      };
    },
  });

  // Figure 3 · potency vs efficacy
  V.S35 = (host) => shell(host, {
    label: "Interactive potency versus efficacy", hint: "Change Drug B and compare it with Drug A",
    point: "Potency is how much drug you need (EC₅₀). Efficacy is how high the effect can go (Emax). Efficacy usually matters more.",
    legend: [["teal", "Drug A"], ["amber", "Drug B", 1]],
    steps: [{ label: "Less potent, same efficacy", state: { ec: 1, emax: 100 } }, { label: "More potent, less efficacious", state: { ec: -0.7, emax: 55 } }, { label: "Identical drugs", state: { ec: 0, emax: 100 } }],
    state: { ec: 1, emax: 100 },
    controls: range("ec", "Drug B EC₅₀", -1, 2, 0.05) + range("emax", "Drug B Emax", 20, 100, 1),
    fmt: { ec: (v) => f1(10 ** v) + " mg", emax: pct },
    draw(S) {
      const ecB = 10 ** S.ec, A = path((t) => [lx(10 ** t), yP(hill(10 ** t, 1, 100))], LA, LB), Bp = path((t) => [lx(10 ** t), yP(hill(10 ** t, ecB, S.emax))], LA, LB);
      const pot = Math.abs(S.ec) < 0.03 ? "Same potency" : S.ec > 0 ? "<b>Drug A is more potent</b> (lower EC₅₀: less drug for half its max)" : "<b>Drug B is more potent</b> (lower EC₅₀)";
      const eff = S.emax >= 99.5 ? "same efficacy (both reach 100%)" : `<b>Drug A is more efficacious</b> (higher Emax: ${pct(100)} vs ${pct(S.emax)})`;
      return {
        svg: axes("Dose (mg, log scale)", "Response (% of max)", logTicks(LA, LB), yTicks) +
          `<path d="${A}" fill="none" stroke="${C.teal}" stroke-width="3" stroke-linecap="round" class="vz-line" pathLength="1"/><path d="${Bp}" fill="none" stroke="${C.amber}" stroke-width="3" stroke-linecap="round" class="vz-dash" stroke-dasharray="8 5"/>
          ${dot(lx(1), yP(50), C.teal, 5)}${dot(lx(ecB), yP(S.emax / 2), C.amber, 5)}
          ${tag(L + 10, T + 14, "— Drug A (EC₅₀ 1 mg, Emax 100%)", C.teal, "start")}${tag(L + 10, T + 34, "- - Drug B", C.amber, "start")}`,
        read: `${pot}; ${eff}. Remember: <b>efficacy usually matters more clinically</b> than potency; a less potent drug just needs a bigger dose.`,
      };
    },
  });

  // Quantal curves: % of people responding vs % with toxicity (therapeutic index)
  const quantal = (host, label) => shell(host, {
    label,
    point: "TI = TD₅₀ ÷ ED₅₀. The closer the two curves, the less room there is between helping and harming.",
    legend: [["teal", "Therapeutic effect (% of people)"], ["coral", "Toxicity (% of people)"], ["sage", "Therapeutic window"]],
    steps: [{ label: "Wide index", state: { ed: 0, td: 1.6, d: 0.6 } }, { label: "Narrow index (warfarin, lithium, digoxin)", state: { ed: 0, td: 0.35, d: 0.2 } }, { label: "Dose too high", state: { ed: 0, td: 1.6, d: 1.9 } }], hint: "Drag to set a dose; slide ED₅₀ and TD₅₀ apart or together",
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
          `<rect x="${sx(S.ed, LA, LB)}" y="${T}" width="${Math.max(0, gap)}" height="${B - T}" fill="${C.sage}" opacity="${narrow ? 0.2 : 0.13}"/>
          <path d="${eff}" fill="none" stroke="${C.teal}" stroke-width="3" stroke-linecap="round" class="vz-line" pathLength="1"/><path d="${tox}" fill="none" stroke="${C.coral}" stroke-width="3" stroke-linecap="round" class="vz-line" pathLength="1"/>
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
    let shown = [100, 100, 100], raf = 0, modeNow = "both";
    const w = shell(host, {
      label: "Interactive CYP450 inhibitor and inducer bar chart", hint: "Pick an interaction and set its strength",
      point: "Inhibitors slow metabolism, so levels rise toward toxicity. Inducers speed it up, so levels fall toward therapeutic failure.",
      legend: [["teal", "Normal"], ["coral", "+ Inhibitor"], ["blue", "+ Inducer"], ["sage", "Therapeutic window (illustrative)"]],
      steps: [{ label: "Add an inhibitor", state: { mode: "inh", s: 1 } }, { label: "A weak inhibitor", state: { mode: "inh", s: 0.3 } }, { label: "Add an inducer", state: { mode: "ind", s: 1 } }, { label: "Compare both", state: { mode: "both", s: 1 } }],
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
        modeNow = S.mode;
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
        v.map((p, i) => { const cx = L + 70 + i * 135; return `<g opacity="${(modeNow === "inh" && i === 2) || (modeNow === "ind" && i === 1) ? 0.25 : 1}">${bar(cx - 46, y(p), 92, B - y(p), cols[i])}</g>${tag(cx, y(p) - 9, pct(p), C.deep)}<text x="${cx}" y="${B + 19}" text-anchor="middle" class="vz-tk">${names[i]}</text>`; }).join("");
    }
    function paint() { const svg = w.el.querySelector("svg"); svg.innerHTML = scope(svg, DEFS() + bars(shown)); }
    return w;
  };

  // Figure 7 · exponential decay over half-lives
  V.S20 = (host) => shell(host, {
    label: "Interactive half-life decay", hint: "Drag through time",
    point: "Each half-life removes half of what's left, so about 97% is gone after five.",
    legend: [["teal", "Plasma concentration"]],
    steps: [{ label: "1 half-life", state: { n: 1 } }, { label: "3 half-lives", state: { n: 3 } }, { label: "5 half-lives ≈ 97% gone", state: { n: 5 } }],
    state: { n: 2, th: 6 },
    controls: range("n", "Time", 0, 6, 0.05) + range("th", "Half-life", 1, 48, 1),
    fmt: { n: (v) => `${f1(v)} half-lives`, th: (v) => `${v} h` },
    drag: (S, x) => { S.n = clamp(((x - L) / (R - L)) * 6, 0, 6); },
    draw(S) {
      const c = 100 * 0.5 ** S.n, curve = path((t) => [sx(t, 0, 6), sy(100 * 0.5 ** t, 0, 110)], 0, 6);
      const marks = [1, 2, 3, 4, 5].map((k) => `<circle cx="${sx(k, 0, 6)}" cy="${sy(100 * 0.5 ** k, 0, 110)}" r="3.5" fill="${C.teal}"/>${tag(sx(k, 0, 6) + 4, sy(100 * 0.5 ** k, 0, 110) - 9, f1(100 * 0.5 ** k) + "%", C.ink, "start")}`).join("");
      return {
        svg: axes("Time (half-lives)", "Concentration (% of start)", [0, 1, 2, 3, 4, 5, 6].map((v) => [v, sx(v, 0, 6)]), [0, 25, 50, 75, 100].map((v) => [v, sy(v, 0, 110)])) +
          `${area(curve, "teal")}<path d="${curve}" fill="none" stroke="${C.teal}" stroke-width="3" stroke-linecap="round" class="vz-line" pathLength="1"/>${marks}${dot(sx(S.n, 0, 6), sy(c, 0, 110), C.teal)}`,
        read: `After <b>${f1(S.n)} half-lives</b> (${f1(S.n * S.th)} h if t½ = ${S.th} h): <b>${f1(c)}% remains</b>, ${f1(100 - c)}% eliminated. Each half-life removes half of what's left, so after ~5 half-lives about 97% is gone.`,
      };
    },
  });

  // Figure 8 · steady state with and without a loading dose
  V.S24 = (host) => shell(host, {
    label: "Interactive steady state and loading dose", hint: "Drag through time; toggle the loading dose",
    point: "Steady state takes about 4–5 half-lives no matter the dose. A loading dose gets you to the target from the first dose.",
    legend: [["teal", "Maintenance doses only"], ["amber", "Loading dose + maintenance", 1], ["ink", "Average at steady state", 1]],
    steps: [{ label: "Maintenance only", state: { load: 0, t: 2 } }, { label: "Reach steady state", state: { load: 0, t: 5 } }, { label: "Add a loading dose", state: { load: 1, t: 1 } }, { label: "Dose less often", state: { load: 0, tau: 2, t: 7 } }],
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
          <path d="${line(0)}" fill="none" stroke="${C.teal}" stroke-width="3" opacity="${S.load ? 0.35 : 1}"/>${`<path opacity="${S.load ? 1 : 0}" d="${line(1)}" fill="none" stroke="${C.amber}" stroke-width="3" stroke-linecap="round" class="vz-dash" stroke-dasharray="9 5"/>`}
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
    point: "Same math both ways: about 4–5 half-lives to reach steady state, and about 4–5 to clear the drug.",
    legend: [["teal", "Filling: regular dosing"], ["coral", "Emptying: after the last dose"]],
    steps: [{ label: "Start dosing: 1 t½", state: { mode: "fill", n: 1 } }, { label: "Steady state at ~5 t½", state: { mode: "fill", n: 5 } }, { label: "Stop dosing: 5 t½", state: { mode: "empty", n: 5 } }],
    state: { n: 3, mode: "fill" },
    controls: seg("mode", [["fill", "Start dosing (fill)"], ["empty", "Stop dosing (empty)"]]) + range("n", "Half-lives", 0, 6, 0.05),
    fmt: { n: f1 },
    drag: (S, x) => { S.n = clamp(((x - L) / (R - L)) * 6, 0, 6); },
    draw(S) {
      const fill = S.mode === "fill", v = (t) => (fill ? 100 * (1 - 0.5 ** t) : 100 * 0.5 ** t), c = v(S.n);
      const steps = [1, 2, 3, 4, 5].map((k) => `<line x1="${sx(k, 0, 6)}" x2="${sx(k, 0, 6)}" y1="${B}" y2="${sy(v(k), 0, 110)}" stroke="${C.grid}"/>${tag(sx(k, 0, 6), sy(v(k), 0, 110) + (fill ? -10 : -10), f1(v(k)) + "%", C.ink)}`).join("");
      return {
        svg: axes("Time (half-lives)", fill ? "% of steady state" : "% of drug remaining", [0, 1, 2, 3, 4, 5, 6].map((t) => [t, sx(t, 0, 6)]), [0, 25, 50, 75, 100].map((t) => [t, sy(t, 0, 110)])) +
          steps + `${area(path((t) => [sx(t, 0, 6), sy(v(t), 0, 110)], 0, 6), fill ? "teal" : "coral")}<path d="${path((t) => [sx(t, 0, 6), sy(v(t), 0, 110)], 0, 6)}" fill="none" stroke="${fill ? C.teal : C.coral}" stroke-width="3" stroke-linecap="round" class="vz-line" pathLength="1"/>${dot(sx(S.n, 0, 6), sy(c, 0, 110), fill ? C.teal : C.coral)}`,
        read: fill ? `After <b>${f1(S.n)} half-lives</b> of regular dosing you're at <b>${f1(c)}%</b> of steady state. Each half-life closes half the remaining gap: 50 → 75 → 87.5 → 93.75 → ~97%.`
          : `<b>${f1(S.n)} half-lives</b> after the last dose, <b>${f1(c)}%</b> remains. Same math in reverse: after ~5 half-lives about 97% is gone.`,
      };
    },
  });

  // Figure 5 · ADME: where an oral dose goes vs an IV dose
  V.S46 = (host) => shell(host, {
    label: "Interactive ADME pathway", h: 266, hint: "Switch the route and change first-pass loss",
    point: "Swallowed drugs pass the liver before reaching the body (first pass). IV and sublingual skip it, which is why their doses differ.",
    steps: [{ label: "IV: all of it arrives", state: { route: "iv" } }, { label: "Oral, large first pass", state: { route: "oral", fp: 80 } }, { label: "Sublingual skips the liver", state: { route: "sl" } }],
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
          `<g opacity="${oral ? 1 : 0}">${arrow(130, 60, 172, 36, 5, C.amber) + arrow(245, 58, 245, 97, 5, C.amber) + arrow(315, 125, 377, 84, Math.max(1.5, 5 * F / 100), C.teal)}</g>` +
          `<g opacity="${oral ? 0 : 1}">${arrow(130, 69, 377, 69, 5, C.teal)}</g>` +
          arrow(420, 98, 380, 197, 3, C.blue) + arrow(460, 98, 476, 197, 3, C.coral) + arrow(500, 98, 572, 197, 3, C.sage),
        read: S.route === "iv" ? "IV goes straight into systemic blood: <b>bioavailability 100%</b>, no first pass."
          : S.route === "sl" ? "Sublingual drug enters systemic veins directly, <b>bypassing the portal vein and liver</b>: no first-pass loss."
          : `Oral drug is absorbed into the portal vein and passes the liver first: <b>${pct(lost)}</b> is lost, so <b>bioavailability is ${pct(F)}</b>. ${lost >= 60 ? "A large first-pass effect is why the oral dose must be much higher than the IV dose." : ""}`,
      };
    },
  });

  // ---- reusable types: a new lecture's figure names one of these in its "viz" field and gets the same hands-on version
  Object.assign(V, { "dose-response": V.S31, antagonist: V.S23, "potency-efficacy": V.S35, "therapeutic-index": V.S39, "cyp-interaction": V.S7,
    "half-life": V.S20, "steady-state": V.S24, "fill-empty": V.TB_fill_empty, adme: V.S46 });
  // generic comparison bars: {"type": "bars", "unit": "%", "point": "...", "ref": 100, "bars": [{"label", "value", "note"}], "steps": [{"label", "pick": index}]}
  V.bars = (host, cfg = {}) => {
    const bars = cfg.bars || [], top = Math.max(1, ...bars.map((b) => b.value), cfg.ref || 0);
    // round ticks (0, 20, 40…): step from 1/2/2.5/5 × 10^k, axis a little above the tallest bar
    const mag = 10 ** Math.floor(Math.log10(top / 4)), tick = [1, 2, 2.5, 5, 10].map((m) => m * mag).find((t) => top / t <= 4.5);
    const max = Math.ceil((top * 1.08) / tick) * tick, cols = [C.teal, C.coral, C.blue, C.amber, C.sage];
    const colOf = (b, i) => (b.col && C[b.col]) || cols[i % cols.length];
    const allSteps = (cfg.steps || []).length >= bars.length;
    const step = (R - L) / Math.max(1, bars.length), bw = Math.min(110, step * 0.62);
    return shell(host, {
      label: `Interactive ${cfg.title || "comparison"}`, hint: "Tap a bar to see what it means", point: cfg.point, steps: (cfg.steps || []).map((st) => ({ label: st.label, state: { sel: st.pick } })),
      legend: cfg.legend, state: { sel: -1 },
      controls: allSteps ? "" : `<div class="seg" data-k="sel">${bars.map((b, i) => `<button type="button" data-v="${i}">${b.label}</button>`).join("")}</div>`,
      drag: (S, x) => { S.sel = clamp(Math.floor((x - L) / step), 0, bars.length - 1); },
      draw(S) {
        const y = (v) => sy(v, 0, max), sel = Math.round(S.sel);
        const ticks = Array.from({ length: Math.round(max / tick) + 1 }, (_, k) => k * tick).map((v) => [f1(v) + (cfg.unit === "%" ? "%" : ""), y(v)]);
        return {
          svg: axes("", cfg.yLabel || "", [], ticks) + (cfg.ref != null ? `<line x1="${L}" x2="${R}" y1="${y(cfg.ref)}" y2="${y(cfg.ref)}" stroke="${C.ink}" stroke-dasharray="2 4"/>` : "") +
            bars.map((b, i) => { const cx = L + step * (i + 0.5); return `<g opacity="${sel < 0 || sel === i ? 1 : 0.35}">${bar(cx - bw / 2, y(b.value), bw, B - y(b.value), colOf(b, i))}${tag(cx, y(b.value) - 9, `${f1(b.value)}${cfg.unit || ""}`, C.deep)}</g><text x="${cx}" y="${B + 19}" text-anchor="middle" class="vz-tk">${(step < 170 ? b.label.split(" · ") : [b.label]).map((t, k) => `<tspan x="${cx}" dy="${k ? 1.15 : 0}em">${t}</tspan>`).join("")}</text>`; }).join(""),
          read: sel >= 0 && bars[sel] ? `<b>${bars[sel].label}: ${f1(bars[sel].value)}${cfg.unit || ""}.</b> ${bars[sel].note || ""}` : (cfg.read || "Tap a bar, or use the buttons, to see what each value means."),
        };
      },
    });
  };

  // generic mechanism pathway: boxes joined by arrows; pick a drug to see where it cuts in and what goes quiet downstream.
  // {"type": "pathway", "h": 300, "nodes": [{id, label ("\n" breaks), x, y, w, col}], "edges": [["a", "b"]],
  //  "drugs": [{label, at: "a>b" (an arrow) or "a" (a box), off: [ids dimmed], less: [ids partly dimmed], note}], "point", "read"}
  V.pathway = (host, cfg = {}) => {
    const N = cfg.nodes || [], E = cfg.edges || [], Dg = cfg.drugs || [];
    // narrow cards (phones, the home column) re-stack the boxes top to bottom by step, so labels can be large
    const narrow = (host.clientWidth || 640) < 560, NH = narrow ? 82 : 58, R0 = narrow ? 17 : 13;
    let h = cfg.h || 300, by = Object.fromEntries(N.map((n) => [n.id, { w: 130, col: "teal", ...n }]));
    if (narrow) {
      const rank = Object.fromEntries(N.map((n) => [n.id, 0]));
      for (let k = 0; k < N.length; k++) E.forEach(([a, b]) => (rank[b] = Math.max(rank[b], rank[a] + 1)));
      const rows = [];
      N.forEach((n) => (rows[rank[n.id]] ||= []).push(n.id));
      const GAP = 74, PAD = 14;
      rows.forEach((ids, r) => {
        const w = (W - 2 * PAD - (ids.length - 1) * 24) / ids.length;
        ids.forEach((id, j) => Object.assign(by[id], { x: PAD + j * (w + 24), y: PAD + r * (NH + GAP), w }));
      });
      h = 2 * PAD + rows.length * (NH + GAP) - GAP;
    }
    const ctr = (n) => [n.x + n.w / 2, n.y + NH / 2], gs = narrow ? 1.6 : 1;
    // small line-art glyphs, drawn in the node's color: what kind of thing each step is
    const GLYPH = {
      cell: (x, y, c) => `<circle cx="${x}" cy="${y}" r="${11 * gs}" fill="${c}" fill-opacity=".18" stroke="${c}" stroke-width="${1.5 * gs}"/><circle cx="${x + 3 * gs}" cy="${y - 2 * gs}" r="${4 * gs}" fill="${c}" fill-opacity=".7"/>`,
      membrane: (x, y, c) => [-8, -4, 0, 4, 8].map((k) => `<circle cx="${x + k * gs}" cy="${y - 6 * gs}" r="${2.1 * gs}" fill="${c}"/><circle cx="${x + k * gs}" cy="${y + 6 * gs}" r="${2.1 * gs}" fill="${c}"/><path d="M${x + k * gs},${y - 4 * gs}v${2.6 * gs}M${x + k * gs},${y + 4 * gs}v${-2.6 * gs}" stroke="${c}" stroke-width="${1.1 * gs}" stroke-linecap="round"/>`).join(""),
      enzyme: (x, y, c) => { const r = 11 * gs; return `<path d="M${x},${y}L${x + r * 0.87},${y - r * 0.5}A${r},${r} 0 1 0 ${x + r * 0.87},${y + r * 0.5}Z" fill="${c}" fill-opacity=".22" stroke="${c}" stroke-width="${1.5 * gs}" stroke-linejoin="round"/>`; },
      molecule: (x, y, c) => `<path d="M${x - 7 * gs},${y + 4 * gs}L${x},${y - 5 * gs}L${x + 7 * gs},${y + 4 * gs}" fill="none" stroke="${c}" stroke-width="${1.3 * gs}"/>` + [[-7, 4], [0, -5], [7, 4]].map(([a, b2]) => `<circle cx="${x + a * gs}" cy="${y + b2 * gs}" r="${3.2 * gs}" fill="${C.bg}" stroke="${c}" stroke-width="${1.5 * gs}"/>`).join(""),
      signal: (x, y, c) => [[-6, -5, 2.6], [5, -6, 2], [7, 4, 2.8], [-4, 6, 2.2], [0, 0, 3]].map(([a, b2, r]) => `<circle cx="${x + a * gs}" cy="${y + b2 * gs}" r="${r * gs}" fill="${c}" fill-opacity=".75"/>`).join(""),
      effect: (x, y, c) => `<circle cx="${x}" cy="${y}" r="${12 * gs}" fill="${c}" fill-opacity=".10"/><circle cx="${x}" cy="${y}" r="${8 * gs}" fill="${c}" fill-opacity=".2"/><circle cx="${x}" cy="${y}" r="${4.2 * gs}" fill="${c}"/>`,
    };
    // connectors leave from the facing side and bend smoothly when boxes don't line up
    const link = (A, B2) => {
      const [ax, ay] = ctr(A), [bx, by2] = ctr(B2), g = 7;
      if (Math.abs(by2 - ay) < NH) {  // same row: across; different rows: down
        const s1 = Math.sign(bx - ax), x1 = ax + s1 * (A.w / 2 + g), x2 = bx - s1 * (B2.w / 2 + g), m = (x1 + x2) / 2;
        return [`M${x1},${ay}C${m},${ay} ${m},${by2} ${x2},${by2}`, [x1, ay], [m, ay], [m, by2], [x2, by2]];
      }
      const s1 = Math.sign(by2 - ay), y1 = ay + s1 * (NH / 2 + g), y2 = by2 - s1 * (NH / 2 + g), m = (y1 + y2) / 2;
      return [`M${ax},${y1}C${ax},${m} ${bx},${m} ${bx},${y2}`, [ax, y1], [ax, m], [bx, m], [bx, y2]];
    };
    const mid = (p0, p1, p2, p3) => [(p0[0] + 3 * p1[0] + 3 * p2[0] + p3[0]) / 8, (p0[1] + 3 * p1[1] + 3 * p2[1] + p3[1]) / 8];
    const cross = (x, y) => { const k = R0 * 0.36; return `<circle cx="${x}" cy="${y}" r="${R0}" fill="${C.coral}" filter="url(#vzSh)"/><path d="M${x - k},${y - k}L${x + k},${y + k}M${x + k},${y - k}L${x - k},${y + k}" stroke="${C.bg}" stroke-width="${R0 / 5}" stroke-linecap="round"/>`; };
    return shell(host, {
      label: `Interactive ${cfg.title || "pathway"}`, hint: "Pick a drug to see where it acts", point: cfg.point, h,
      steps: Dg.map((d, i) => ({ label: d.label, state: { sel: i } })), state: { sel: -1 },
      controls: "",
      draw(S) {
        const d = Dg[Math.round(S.sel)], off = new Set(d?.off || []), less = new Set(d?.less || []);
        const op = (id) => (off.has(id) ? 0.28 : less.has(id) ? 0.6 : 1);
        const lines = E.map(([a, b], i) => {
          const A = by[a], B2 = by[b], [path, ...pts] = link(A, B2), cut = d?.at === `${a}>${b}`, quiet = cut || off.has(a) || off.has(b);
          const col = C[A.col] || C.teal, [mx, my] = mid(...pts);
          // molecules drifting along the arrow: they stop where a drug cuts the pathway
          const flow = [0, 1, 2].map((k) => `<circle r="${(narrow ? 4.2 : 2.8)}" fill="${col}"><animateMotion dur="2.7s" begin="${(-k * 0.9 - i * 0.37).toFixed(2)}s" repeatCount="indefinite" path="${path}"/></circle>`).join("");
          return `<path d="${path}" fill="none" stroke="${C.ink}" stroke-width="${narrow ? 2.6 : 1.9}" stroke-linecap="round" marker-end="url(#vzA)" opacity="${quiet ? 0.28 : 0.55}" stroke-dasharray="${cut ? "3 6" : "none"}"/>` +
            `<g class="vz-flow" opacity="${quiet ? 0 : 0.85}">${flow}</g>` + (cut ? cross(mx, my) : "");
        }).join("");
        const boxes = N.map((n0) => {
          const n = by[n0.id], ls = String(n.label).split("\n"), col = C[n.col] || C.teal, rx = NH / 2;
          const gw = n.glyph && GLYPH[n.glyph] ? 30 * gs : 0, tx = n.x + gw + (n.w - gw) / 2 + (gw ? 2 * gs : 0), cy = n.y + NH / 2;
          return `<g opacity="${op(n.id)}"><rect x="${n.x}" y="${n.y}" width="${n.w}" height="${NH}" rx="${rx}" fill="${C.bg}" filter="url(#vzSoft)"/>
            <rect x="${n.x}" y="${n.y}" width="${n.w}" height="${NH}" rx="${rx}" fill="${col}" fill-opacity=".12" stroke="${col}" stroke-opacity=".38" stroke-width="1"/>
            <rect x="${n.x + 1}" y="${n.y + 1}" width="${n.w - 2}" height="${NH / 2}" rx="${rx - 1}" fill="url(#vzGloss)" opacity=".7"/>
            ${gw ? GLYPH[n.glyph](n.x + 12 * gs + 11 * gs, cy, col) : ""}
            <text x="${tx}" y="${cy}" text-anchor="middle" class="vz-node${narrow ? " vz-node-lg" : ""}" fill="${C.deep}">${ls.map((l, i) => `<tspan x="${tx}" dy="${i ? 1.2 : 0.35 - (ls.length - 1) * 0.6}em">${l}</tspan>`).join("")}</text></g>` +
            (d?.at === n.id ? cross(n.x + n.w - rx * 0.35, n.y + 4) : "");
        }).join("");
        return { svg: lines + boxes, read: d ? `<b>${d.label}.</b> ${d.note || ""}` : (cfg.read || "Pick a drug to see where it interrupts the pathway.") };
      },
    });
  };

  // Rumack-Matthew nomogram (illustrative schematic, single acute ingestion): drag the level to a time and concentration.
  // Treatment line: 150 mcg/mL at 4 h, halving every 4 h to 4.7 at 24 h. {"type": "nomogram", "point", "steps": [{label, t, c}]}
  V.nomogram = (host, cfg = {}) => {
    const T0 = 0, T1 = 32, LO = Math.log10(3), HI = Math.log10(300);
    const X = (t) => sx(t, T0, T1), Y = (c) => sy(Math.log10(clamp(c, 3, 300)), LO, HI);
    const line = (t) => 150 * 2 ** (-(t - 4) / 4);
    return shell(host, {
      label: "Interactive Rumack-Matthew nomogram", hint: "Drag the point to a time and level", point: cfg.point,
      legend: [["coral", "Above the line: give NAC"], ["sage", "Below the line: toxicity unlikely"], ["ink", "Treatment line (illustrative)"]],
      steps: (cfg.steps || []).map((st) => ({ label: st.label, state: { t: st.t, c: Math.log10(st.c) } })),
      state: { t: 8, c: Math.log10(120) },
      controls: range("t", "Hours since a single acute ingestion", 1, 32, 0.25) + range("c", "Acetaminophen level", LO, HI, 0.01),
      fmt: { t: (v) => `${f1(v)} h`, c: (v) => `${f1(10 ** v)} mcg/mL` },
      drag: (S, x, y) => { S.t = clamp(T0 + ((x - L) / (R - L)) * (T1 - T0), 1, 32); S.c = clamp(LO + ((B - y) / (B - T)) * (HI - LO), LO, HI); },
      draw(S) {
        const c = 10 ** S.c, t = S.t, on = t >= 4 && t <= 24, lv = on ? line(t) : null;
        const lp = path((u) => [X(u), Y(line(u))], 4, 24, 40);
        const above = `${lp}L${X(24)},${T}L${X(4)},${T}Z`, below = `${lp}L${X(24)},${B}L${X(4)},${B}Z`;
        const yt = [3, 5, 10, 20, 50, 100, 150, 300].map((v) => [v, Y(v)]), xt = [0, 4, 8, 12, 16, 20, 24, 28, 32].map((v) => [v, X(v)]);
        const zone = !on ? C.ink : c >= lv ? C.coral : C.sage;
        const read = t < 4 ? `<b>Too early.</b> Levels drawn before 4 hours can't be plotted: draw the level at 4 hours or later.`
          : t > 24 ? `<b>Beyond 24 hours the nomogram is not used.</b> 4.7 mcg/mL is only where the line ends, not a safe cutoff: get AST/ALT; a detectable level or raised AST/ALT guides NAC, per protocol or poison control.`
          : c >= lv ? `<b>Above the treatment line</b> (the line is ${f1(lv)} mcg/mL at ${f1(t)} h): <b>give NAC</b>.`
          : `<b>Below the line</b> (${f1(lv)} mcg/mL at ${f1(t)} h): toxicity unlikely, for a single acute ingestion with a known time.`;
        return {
          svg: axes("Hours after single acute ingestion", "Acetaminophen (mcg/mL, log)", xt, yt) +
            `<path d="${above}" fill="${C.coral}" opacity=".10"/><path d="${below}" fill="${C.sage}" opacity=".12"/>
            <rect x="${X(24)}" y="${T}" width="${X(32) - X(24)}" height="${B - T}" fill="${C.ink}" opacity=".08"/><rect x="${X(0)}" y="${T}" width="${X(4) - X(0)}" height="${B - T}" fill="${C.ink}" opacity=".08"/>
            ${tag(X(28), T + 18, "not used > 24 h", C.ink)}${tag(X(2), T + 18, "< 4 h", C.ink)}
            <path d="${lp}" fill="none" stroke="${C.deep}" stroke-width="2.6" stroke-linecap="round" class="vz-line" pathLength="1"/>
            ${[[4, 150], [8, 75], [12, 37.5], [16, 18.75], [20, 9.4], [24, 4.7]].map(([u, v]) => `<circle cx="${X(u)}" cy="${Y(v)}" r="3.2" fill="${C.deep}"/>`).join("")}
            <line x1="${X(t)}" x2="${X(t)}" y1="${Y(c)}" y2="${B}" stroke="${zone}" stroke-dasharray="3 4" opacity=".7"/>${dot(X(t), Y(c), zone)}`,
          read,
        };
      },
    });
  };

  // fast symptom relief (NSAIDs) vs slow structural protection (DMARDs) over time: a schematic, not data
  V.onset = (host, cfg = {}) => {
    const relief = (t) => 1 - Math.exp(-t / 0.3), prot = (t) => 0.18 + 0.55 * (1 - Math.exp(-t / 3.6));
    const X = (t) => sx(t, 0, 12), Y = (v) => sy(v, 0, 1.1);
    return shell(host, {
      label: "Interactive NSAID vs DMARD timeline", hint: "Drag along the timeline", point: cfg.point,
      legend: [["teal", "Symptom relief (NSAIDs)"], ["sage", "Joint damage slowed (DMARDs)"]],
      steps: (cfg.steps || []).map((st) => ({ label: st.label, state: { t: st.t } })), state: { t: 0.5 },
      controls: range("t", "Time on treatment (weeks to months)", 0, 12, 0.05), fmt: { t: (v) => f1(v) },
      drag: (S, x) => { S.t = clamp(((x - L) / (R - L)) * 12, 0, 12); },
      draw(S) {
        const a = path((u) => [X(u), Y(relief(u))], 0, 12), b = path((u) => [X(u), Y(prot(u))], 0, 12), t = S.t;
        const read = t < 1.5 ? `<b>Early:</b> NSAID relief of pain and swelling comes within days; the DMARD is barely working yet — don't judge it at the first visit.`
          : t < 6 ? `<b>Weeks in:</b> symptom relief has long plateaued, while the DMARD's protection is still building.`
          : `<b>Months in:</b> the DMARD now slows cartilage and bone destruction — something the NSAID never does. Relief now with NSAIDs, protection later with DMARDs.`;
        return {
          svg: axes("Time on treatment (weeks to months)", "Effect (schematic)", [0, 2, 4, 6, 8, 10, 12].map((v) => [v, X(v)]), []) +
            `<path d="${a}" fill="none" stroke="${C.teal}" stroke-width="3" stroke-linecap="round" class="vz-line" pathLength="1"/>
            <path d="${b}" fill="none" stroke="${C.sage}" stroke-width="3" stroke-linecap="round" class="vz-line" pathLength="1"/>
            <line x1="${X(t)}" x2="${X(t)}" y1="${T}" y2="${B}" stroke="${C.ink}" stroke-dasharray="3 4" opacity=".6"/>
            ${dot(X(t), Y(relief(t)), C.teal, 6)}${dot(X(t), Y(prot(t)), C.sage, 6)}`,
          read,
        };
      },
    });
  };

  // ---- enhance every figure that has an interactive twin; the original image stays one tap away
  function enhance(fig) {
    const key = fig.dataset.viz, make = V[key];
    if (!make || fig.dataset.vizOn) return;
    fig.dataset.vizOn = 1;
    let cfg = {}; try { cfg = JSON.parse(fig.dataset.vizCfg || "{}"); } catch { /* bad config: defaults */ }
    make(fig, cfg);
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
