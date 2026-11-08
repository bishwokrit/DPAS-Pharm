// Class performance (syllabus page). One viewer with switchable views, a short summary under it, and the detail in
// collapsed boxes. Reported numbers come from #class-stats-data; curves, counts and percentiles are modeled, never real
// grades. Exams are only compared with exams, quizzes with quizzes. Scores typed into the grade calculator
// ("grades:v1") show up on the curves as "You".
(() => {
  const root = document.getElementById("csapp"), src = document.getElementById("class-stats-data");
  if (!root || !src) return;
  const D = JSON.parse(src.textContent), N = D.cohort;
  const ALL = D.assessments, NUM = ALL.filter((a) => a.mean !== null);
  const byId = Object.fromEntries(ALL.map((a) => [a.id, a]));
  const COLOR = { u1: "var(--accent)", u2: "var(--violet)", q1: "var(--text-2)", q2: "var(--warn)" };
  const GROUPS = { exam: { label: "Exams", ids: ALL.filter((a) => a.type === "exam").map((a) => a.id) }, quiz: { label: "Quizzes", ids: ALL.filter((a) => a.type === "quiz").map((a) => a.id) } };
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const f = (x, d = 2) => (Math.round(x * 10 ** d) / 10 ** d).toFixed(d);
  const pct = (x) => `${f(x)}%`;
  const sgn = (x, d = 1) => `${x >= 0 ? "+" : "−"}${f(Math.abs(x), d)}`;
  const ord = (n) => { const r = Math.round(n), t = r % 100; return `${r}${t > 10 && t < 14 ? "th" : ["th", "st", "nd", "rd"][r % 10] || "th"}`; };

  // ---- normal-model math ----
  const SQ2PI = Math.sqrt(2 * Math.PI), phi = (z) => Math.exp(-z * z / 2) / SQ2PI;
  function erf(x) {  // Abramowitz & Stegun 7.1.26 (|error| < 1.5e-7)
    const s = Math.sign(x), t = 1 / (1 + 0.3275911 * Math.abs(x));
    return s * (1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x));
  }
  const Phi = (z) => 0.5 * (1 + erf(z / Math.SQRT2));
  const MODELS = {
    range: { name: "Normal, cut off at each reported min and max", short: "Reported range", bounds: (a) => [a.min, a.max] },
    scale: { name: "Normal, cut off at 0% and 100%", short: "0–100% scale", bounds: () => [0, 100] },
    normal: { name: "Plain normal curve, not cut off (reference only)", short: "Not cut off", bounds: () => [-Infinity, Infinity] },
  };
  let model = "range";
  function M(a) {
    const [lo, hi] = MODELS[model].bounds(a), al = (lo - a.mean) / a.sd, be = (hi - a.mean) / a.sd, Z = Phi(be) - Phi(al);
    return {
      pdf: (x) => (x < lo || x > hi ? 0 : phi((x - a.mean) / a.sd) / a.sd / Z),
      cdf: (x) => (x <= lo ? 0 : x >= hi ? 1 : (Phi((x - a.mean) / a.sd) - Phi(al)) / Z),
      moments() {  // the cut-off curve's own mean and SD drift away from the reported ones
        const pa = isFinite(al) ? phi(al) : 0, pb = isFinite(be) ? phi(be) : 0, aa = isFinite(al) ? al * pa : 0, bb = isFinite(be) ? be * pb : 0;
        return { mean: a.mean + a.sd * (pa - pb) / Z, sd: a.sd * Math.sqrt(1 + (aa - bb) / Z - ((pa - pb) / Z) ** 2) };
      },
    };
  }

  // ---- your scores from the grade calculator ----
  const mine = () => {
    let S = {}; try { S = JSON.parse(localStorage.getItem("grades:v1")) || {}; } catch { /* private mode */ }
    const out = {};
    ALL.forEach((a) => { const v = S[a.calc?.[0]]?.[a.calc?.[1]]; if (v !== null && v !== undefined && v !== "" && isFinite(+v)) out[a.id] = +v; });
    return out;
  };

  // ---- shared UI bits ----
  const TAG = { rep: ["Reported", "Announced by the course"], calc: ["Calculated", "Arithmetic on the reported numbers"], mod: ["Model", "An estimate from a normal curve, not real grades"], fb: ["Feedback", "Instructor's words, no numbers"] };
  const tag = (k) => `<span class="cs-tag cs-${k}" title="${TAG[k][1]}">${TAG[k][0]}</span>`;
  const typeBadge = (a) => `<span class="cs-type ${a.type}">${a.type === "exam" ? "Exam" : "Quiz"}</span>`;
  const seg = (name, opts, on, label) => `<div class="seg cs-seg" role="group" aria-label="${label}" data-seg="${name}">${opts.map(([v, l]) => `<button type="button" data-v="${v}" class="${v === on ? "on" : ""}" aria-pressed="${v === on}">${l}</button>`).join("")}</div>`;
  const W = (el) => Math.max(300, Math.min(1000, el.clientWidth || 700));
  const tip = Object.assign(document.createElement("div"), { className: "cs-tip", role: "status" });
  tip.hidden = true; document.body.append(tip);
  const showTip = (h, x, y) => { tip.innerHTML = h; tip.hidden = false; const r = tip.getBoundingClientRect(); tip.style.left = `${Math.min(innerWidth - r.width - 8, Math.max(8, x + 14))}px`; tip.style.top = `${Math.max(8, y - r.height - 12)}px`; };
  const hideTip = () => (tip.hidden = true);
  const exams = GROUPS.exam.ids.map((i) => byId[i]);
  const examHi = exams.reduce((a, b) => (b.mean > a.mean ? b : a)), examLo = exams.reduce((a, b) => (b.mean < a.mean ? b : a));

  root.innerHTML = `
<div class="cs-viewer card">
  <div class="cs-vtabs" role="tablist" aria-label="Choose a view">${[["curve", "Curves"], ["bands", "Score bands"], ["compare", "Compare"], ["table", "All stats"]].map(([v, l], i) => `<button type="button" role="tab" data-view="${v}" aria-selected="${!i}">${l}</button>`).join("")}</div>

  <div class="cs-view" data-view="curve">
    <div class="cs-ctl">${seg("group", [["exam", "Exams"], ["quiz", "Quizzes"]], "exam", "Assessment group")}
      <div class="cs-ctl-r">${seg("zoom", [["all", "Full"], ["mid", "85–100"], ["top", "90–100"]], "all", "Zoom")}</div></div>
    <div class="cs-chart" id="cs-dist"></div>
    <div class="cs-slide"><label for="cs-score">Try a score</label><input type="range" id="cs-score" min="0" max="100" step="0.5" value="90"><output id="cs-score-out">90%</output></div>
    <div class="cs-presets">${[60, 70, 80, 85, 90, 95, 98, 100].map((s) => `<button type="button" class="sch-chip" data-s="${s}">${s}</button>`).join("")}</div>
    <div class="cs-ex" id="cs-ex"></div>
    <p class="cs-foot small muted" id="cs-foot"></p>
  </div>

  <div class="cs-view" data-view="bands" hidden>
    <div class="cs-ctl">${seg("hist", NUM.map((a) => [a.id, a.label]), "u1", "Assessment")}</div>
    <div class="cs-chart" id="cs-hist"></div>
    <p class="cs-foot small muted">${tag("mod")} About how many of ${N} students land in each band if scores followed the curve. Decimals on purpose: these are estimates, not head counts.</p>
  </div>

  <div class="cs-view" data-view="compare" hidden>
    <div class="cs-ctl">${seg("cmp", [["mean", "Average"], ["sd", "Spread (SD)"], ["range", "Low – high"], ["cv", "Relative spread"]], "mean", "Statistic")}</div>
    <div class="cs-chart" id="cs-cmp"></div>
    <p class="cs-foot small muted">Exams are compared only with exams, quizzes only with quizzes — they differ in length and difficulty.</p>
  </div>

  <div class="cs-view" data-view="table" hidden>
    <div class="table-wrap"><table class="cs-table"><thead><tr><th></th>${ALL.map((a) => `<th>${a.label}</th>`).join("")}<th></th></tr></thead><tbody>
    ${[["Average", (a) => pct(a.mean), "rep"], ["Standard deviation", (a) => f(a.sd), "rep"], ["Lowest grade", (a) => `${a.min}%`, "rep"], ["Highest grade", (a) => `${a.max}%`, "rep"],
       ["Class size", () => `${N}*`, "rep"], ["Range width", (a) => `${a.max - a.min} pts`, "calc"], ["Mean − 2 SD", (a) => pct(a.mean - 2 * a.sd), "calc"], ["Mean − 1 SD", (a) => pct(a.mean - a.sd), "calc"],
       ["Mean + 1 SD", (a) => pct(a.mean + a.sd) + (a.mean + a.sd > 100 ? "†" : ""), "calc"], ["Mean + 2 SD", (a) => pct(a.mean + 2 * a.sd) + (a.mean + 2 * a.sd > 100 ? "†" : ""), "calc"],
       ["Relative spread (SD ÷ mean)", (a) => pct(100 * a.sd / a.mean), "calc"]]
      .map(([n, fn, k]) => `<tr><td>${n}</td>${ALL.map((a) => `<td>${a.mean === null && n !== "Class size" ? '<span class="muted">—</span>' : fn(a)}</td>`).join("")}<td>${tag(k)}</td></tr>`).join("")}
    </tbody></table></div>
    <p class="small muted">* Assumed, not confirmed for each assessment. † A math threshold above 100%, not a grade anyone can earn. — Not released.</p>
  </div>
</div>

<div class="cs-kpis">
  <div class="cs-kpi"><span class="cs-k">Class size</span><strong>${N}<sup>*</sup></strong><span class="small muted">assumed</span></div>
  <div class="cs-kpi"><span class="cs-k">Exam averages</span><strong>${f(examLo.mean, 0)}–${f(examHi.mean, 0)}%</strong><span class="small muted">${exams.map((a) => a.short).join(" & ")}</span></div>
  <div class="cs-kpi"><span class="cs-k">${byId.q2.label} average</span><strong>${f(byId.q2.mean, 0)}%</strong><span class="small muted">widest spread · SD ${f(byId.q2.sd, 1)}</span></div>
  <div class="cs-kpi"><span class="cs-k">${byId.q1.label}</span><strong class="cs-kpi-w">On track</strong><span class="small muted">everyone still at an A overall</span></div>
</div>
<div class="cs-cards">${ALL.map((a) => `<div class="cs-card${a.mean === null ? " na" : ""}" style="--c:${COLOR[a.id]}"><div class="cs-ch"><strong>${a.label}</strong>${typeBadge(a)}</div>
  ${a.mean === null ? `<div class="cs-big">—</div><p class="small muted">No numbers released</p>` : `<div class="cs-big">${pct(a.mean)}</div><p class="small muted">SD ${f(a.sd, 1)} · ${a.min}–${a.max}%</p>`}</div>`).join("")}</div>

<details class="cs-more"><summary>About the model</summary><div class="cs-more-in">
  <p class="small">Each curve is a normal (bell) curve built from the reported average and SD. Real grades stop at 100% and pile up near the top, so the curves are sketches, not the real shape. ${tag("mod")}</p>
  <div class="cs-ctl"><span class="small muted">Cut the curve off at</span>${seg("model", Object.entries(MODELS).map(([k, m]) => [k, m.short]), model, "Model")}</div>
  <div id="cs-moments"></div>
</div></details>
<details class="cs-more"><summary>${byId.q1.label}: what the feedback means</summary><div class="cs-more-in">
  <blockquote class="cs-quote">“${esc(byId.q1.quote)}” ${tag("fb")}</blockquote>
  <p class="small"><strong>It tells us</strong> every student's <em>overall course grade</em> was still on an A track after Quiz 1.</p>
  <p class="small"><strong>It doesn't tell us</strong> that everyone scored an A on Quiz 1 itself, or any average, spread or lowest score — so Quiz 1 is left out of every chart.</p>
</div></details>
<details class="cs-more"><summary>What the numbers mean</summary><div class="cs-more-in cs-interp">
  <div><h4>Exams</h4><p class="small">Both exam averages were above 93% with small spreads: most of the class sat near the top. ${examHi.label} averaged ${f(examHi.mean - examLo.mean)} points higher than ${examLo.label}; ${byId.u2.sd < byId.u1.sd ? `${byId.u2.label} scores were slightly more bunched (SD ${f(byId.u2.sd)} vs ${f(byId.u1.sd)})` : ""}.</p></div>
  <div><h4>Quizzes</h4><p class="small">${byId.q2.label} averaged ${pct(byId.q2.mean)} with an SD of ${f(byId.q2.sd)} — scores were spread widely, from ${byId.q2.min}% to ${byId.q2.max}%. ${byId.q1.label} released no numbers, so there is nothing to compare it with.</p></div>
  <div><h4>Standard deviation, plainly</h4><p class="small">The typical distance from the average. On ${byId.u2.label} most scores sat within about ${f(byId.u2.sd, 0)} points of ${f(byId.u2.mean, 0)}%; on ${byId.q2.label}, within about ${f(byId.q2.sd, 0)} points of ${f(byId.q2.mean, 0)}%.</p></div>
  <div><h4>Ceiling effect</h4><p class="small">With an average near ${f(byId.u1.mean, 0)}%, many scores are pressed against 100% and the exam can't spread them out further. "Average + 1 SD" on ${byId.u1.label} is ${pct(byId.u1.mean + byId.u1.sd)}, a score nobody can earn — a sign the scores are lopsided toward the top, not bell-shaped.</p></div>
  <div><h4>Why the curves are only sketches</h4><p class="small">A bell curve runs forever both ways; grades stop at 0 and 100. Cutting the curve off keeps it in bounds but shifts its own average and SD away from the reported ones (see "About the model").</p></div>
  <div><h4>A lower average ≠ a harder test</h4><p class="small">A lower average can come from harder questions, but also from fewer questions (each miss costs more), different content, or less prep time. The averages alone can't tell these apart.</p></div>
  <div><h4>Why no one's rank can be known</h4><p class="small">Many different sets of ${N} scores share the same average, SD, low and high. Without the raw scores there's no true median, percentile or rank — only estimates, and ties at 100% make "top of the class" meaningless.</p></div>
</div></details>`;

  // ---- "About the model" table ----
  function moments() {
    root.querySelector("#cs-moments").innerHTML = model === "normal"
      ? `<p class="small muted">Not cut off: the curve keeps the reported average and SD exactly, but puts some chance above 100%, which no one can score.</p>`
      : `<table class="cs-mini"><thead><tr><th></th>${NUM.map((a) => `<th>${a.short}</th>`).join("")}</tr></thead><tbody>
        <tr><td>Reported average / SD</td>${NUM.map((a) => `<td>${f(a.mean, 1)} / ${f(a.sd, 1)}</td>`).join("")}</tr>
        <tr><td>Cut-off curve's own</td>${NUM.map((a) => { const m = M(a).moments(); return `<td>${f(m.mean, 1)} / ${f(m.sd, 1)}</td>`; }).join("")}</tr></tbody></table>
        <p class="small muted">Cutting the curve off keeps every score possible, but its own average and SD no longer match the reported ones: the reported values are its starting settings, not its results.</p>`;
  }

  // ---- Curves view: curves + score line + "You" dots ----
  let group = "exam", zoom = "all", sdFor = null;
  const slider = root.querySelector("#cs-score");
  const ZOOM = { exam: { mid: [85, "85–100"], top: [90, "90–100"] }, quiz: { mid: [70, "70–100"], top: [85, "85–100"] } };
  const domain = () => (zoom !== "all" ? [ZOOM[group][zoom][0], model === "normal" ? 105 : 100] : model === "normal" ? [group === "quiz" ? 40 : 60, 112] : group === "quiz" ? [50, 100] : [70, 100]);
  function dist() {
    const box = root.querySelector("#cs-dist"), w = W(box), h = Math.round(Math.min(340, Math.max(230, w * 0.38)));
    const P = { l: 14, r: 14, t: 30, b: 30 }, [x0, x1] = domain(), score = +slider.value, me = mine();
    const vis = GROUPS[group].ids.map((i) => byId[i]).filter((a) => a.mean !== null);
    const series = vis.map((a) => { const m = M(a), pts = []; for (let i = 0; i <= 260; i++) { const x = x0 + (x1 - x0) * i / 260; pts.push([x, m.pdf(x)]); } return { a, m, pts }; });
    const ymax = Math.max(0.02, ...series.flatMap((s) => s.pts.map((p) => p[1]))) * 1.18;
    const X = (x) => P.l + (x - x0) / (x1 - x0) * (w - P.l - P.r), Y = (y) => h - P.b - y / ymax * (h - P.t - P.b);
    const step = x1 - x0 > 40 ? 10 : 5;
    let s = `<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" aria-label="Modeled score curves for ${vis.map((a) => a.label).join(" and ")}, with a marker at ${score}%">`;
    if (x1 > 100) s += `<rect x="${X(100)}" y="${P.t}" width="${X(x1) - X(100)}" height="${h - P.t - P.b}" class="cs-unatt"/><text x="${X(100) + 6}" y="${P.t + 12}" class="cs-ax">over 100% · impossible</text>`;
    for (let x = Math.ceil(x0 / step) * step; x <= Math.min(x1, 100); x += step) s += `<line x1="${X(x)}" x2="${X(x)}" y1="${P.t}" y2="${h - P.b}" class="cs-grid"/><text x="${X(x)}" y="${h - P.b + 18}" text-anchor="middle" class="cs-ax">${x}%</text>`;
    const g = sdFor && vis.find((a) => a.id === sdFor);
    if (g) [-2, -1, 1, 2].forEach((k) => { const x = g.mean + k * g.sd; if (x >= x0 && x <= x1) s += `<line x1="${X(x)}" x2="${X(x)}" y1="${P.t + 14}" y2="${h - P.b}" style="stroke:${COLOR[g.id]}" class="cs-sdl"/><text x="${X(x)}" y="${h - P.b - 4}" text-anchor="middle" class="cs-sdt" style="fill:${COLOR[g.id]}">${k > 0 ? "+" : "−"}${Math.abs(k)}SD</text>`; });
    series.forEach(({ a, pts }, si) => {
      const c = COLOR[a.id], d = pts.map((p, i) => `${i ? "L" : "M"}${X(p[0]).toFixed(1)},${Y(p[1]).toFixed(1)}`).join("");
      s += `<path d="${d}L${X(x1)},${Y(0)}L${X(x0)},${Y(0)}Z" style="fill:${c}" class="cs-area"/><path d="${d}" style="stroke:${c}" class="cs-line"/>`;
      if (a.mean >= x0 && a.mean <= x1) s += `<line x1="${X(a.mean)}" x2="${X(a.mean)}" y1="${Y(0)}" y2="${P.t + 6 + si * 14}" style="stroke:${c}" class="cs-mean"/>${w > 520 ? `<text x="${X(a.mean) - 5}" y="${P.t + 10 + si * 14}" text-anchor="end" class="cs-ml" style="fill:${c}">avg ${f(a.mean, 1)}</text>` : ""}`;
    });
    s += `<line x1="${P.l}" x2="${w - P.r}" y1="${Y(0)}" y2="${Y(0)}" class="cs-axis"/>`;
    // your calculator scores, on their own curve
    series.forEach(({ a, m }) => { const v = me[a.id]; if (v === undefined || v < x0 || v > x1) return; s += `<g class="cs-you"><circle cx="${X(v)}" cy="${Y(m.pdf(v))}" r="7" style="stroke:${COLOR[a.id]}"/><text x="${X(v)}" y="${Y(m.pdf(v)) - 12}" text-anchor="middle">You ${f(v, 0)}</text></g>`; });
    // the hypothetical score line
    if (score >= x0 && score <= x1) s += `<g class="cs-pin"><line x1="${X(score)}" x2="${X(score)}" y1="${P.t - 6}" y2="${h - P.b}"/><rect x="${X(score) - 22}" y="${P.t - 24}" width="44" height="20" rx="10"/><text x="${X(score)}" y="${P.t - 10}" text-anchor="middle">${f(score, score % 1 ? 1 : 0)}%</text>${series.map(({ a, m }) => `<circle cx="${X(score)}" cy="${Y(m.pdf(score))}" r="4.5" style="fill:${COLOR[a.id]}"/>`).join("")}</g>`;
    s += `<rect x="${P.l}" y="${P.t - 26}" width="${w - P.l - P.r}" height="${h - P.t - P.b + 26}" fill="transparent" class="cs-hit"/></svg>`;
    s += `<div class="cs-legend">${series.map(({ a }) => `<button type="button" class="cs-lg${sdFor === a.id ? " on" : ""}" data-sd="${a.id}" style="--c:${COLOR[a.id]}" title="Show ±1 and ±2 SD for ${a.label}"><i></i>${a.label}<span>avg ${f(a.mean, 1)} · ±SD</span></button>`).join("")}${group === "quiz" ? `<span class="cs-lg na"><i></i>${byId.q1.label} · no numbers</span>` : ""}<span class="cs-lg-note">${tag("mod")} curves, not real grades</span></div>`;
    box.innerHTML = s;
    box.querySelectorAll("[data-sd]").forEach((b) => b.addEventListener("click", () => { sdFor = sdFor === b.dataset.sd ? null : b.dataset.sd; dist(); }));
    const svg = box.querySelector("svg"), hit = svg.querySelector(".cs-hit");
    const xAt = (e) => { const r = svg.getBoundingClientRect(); return x0 + (Math.min(w - P.r, Math.max(P.l, (e.clientX - r.left) * w / r.width)) - P.l) / (w - P.l - P.r) * (x1 - x0); };
    let drag = false;
    const setScore = (x) => { slider.value = Math.max(0, Math.min(100, Math.round(x * 2) / 2)); update(); };
    hit.addEventListener("pointerdown", (e) => { drag = true; hit.setPointerCapture(e.pointerId); setScore(xAt(e)); hideTip(); });
    hit.addEventListener("pointermove", (e) => {
      const x = xAt(e);
      if (drag) return setScore(x);
      if (e.pointerType !== "mouse") return;
      showTip(`<strong>${f(x, 1)}%</strong>${x > 100 ? " · impossible" : ""}<br>${series.map(({ a, m }) => `<span class="cs-dot" style="background:${COLOR[a.id]}"></span>${a.short}: about ${f(100 * m.pdf(x), 1)}% of the class per point <span class="muted">(density ${m.pdf(x).toFixed(3)})</span>`).join("<br>")}<br><span class="muted">Click or drag to move your score.</span>`, e.clientX, e.clientY);
    });
    const stop = () => (drag = false);
    hit.addEventListener("pointerup", stop); hit.addEventListener("pointercancel", stop);
    hit.addEventListener("pointerleave", hideTip);
  }
  function results() {
    const s = +slider.value, me = mine();
    root.querySelector("#cs-score-out").textContent = `${s}%`;
    root.querySelectorAll(".cs-presets button").forEach((b) => b.classList.toggle("on", +b.dataset.s === s));
    const ids = GROUPS[group].ids;
    root.querySelector("#cs-ex").innerHTML = ids.map((id) => {
      const a = byId[id];
      if (a.mean === null) return `<div class="cs-exc na" style="--c:${COLOR[id]}"><strong>${a.label}</strong><p class="small muted">No numbers released — can't estimate.</p></div>`;
      const m = M(a), p = m.cdf(s), z = (s - a.mean) / a.sd, you = me[id];
      const edge = s < a.min ? "below the lowest reported score" : s >= a.max ? "top score — likely shared, not a rank" : "";
      return `<div class="cs-exc" style="--c:${COLOR[id]}"><div class="cs-ch"><strong>${a.label}</strong></div>
        <div class="cs-pv"><span class="cs-pn">${ord(100 * p)}</span><span class="small muted">est. percentile</span></div>
        <div class="cs-pbar" aria-hidden="true"><span style="width:${(100 * p).toFixed(1)}%"></span></div>
        <p class="cs-sub"><span title="Difference from the class average">${sgn(s - a.mean)} vs avg</span><span title="Z-score: (score − average) ÷ SD">z ${sgn(z, 2)}</span><span title="Estimated students scoring below / above (of ${N} assumed)">≈${f(N * p, 0)} below · ≈${f(N * (1 - p), 0)} above</span></p>
        ${edge ? `<p class="small muted cs-edge">${edge}</p>` : ""}
        ${you !== undefined ? `<p class="cs-yours"><span>Your ${f(you, 1).replace(/\.0$/, "")}%</span> ≈ ${ord(100 * m.cdf(you))} percentile</p>` : ""}</div>`;
    }).join("");
    const any = ALL.some((a) => me[a.id] !== undefined);
    const ex = GROUPS[group].ids.map((i) => byId[i]).filter((a) => a.mean !== null);
    let rel = "";
    if (ex.length > 1) { const zs = ex.map((a) => [a, (s - a.mean) / a.sd]).sort((x, y) => y[1] - x[1]); rel = `Against each exam's own class, ${s}% stands higher on ${zs[0][0].short} than on ${zs[1][0].short}. `; }
    root.querySelector("#cs-foot").innerHTML = `${rel}${tag("mod")} Estimates from the ${MODELS[model].short.toLowerCase()} curve, ${N} students assumed — not real ranks.${any ? "" : ` <a href="#calc">Enter your scores in the calculator</a> to see where you sit.`}`;
  }
  const update = () => { dist(); results(); hist(); };
  slider.addEventListener("input", update);
  root.querySelectorAll(".cs-presets button").forEach((b) => b.addEventListener("click", () => { slider.value = b.dataset.s; update(); }));

  // ---- Score bands view ----
  let histA = "u1";
  function hist() {
    const a = byId[histA], m = M(a), box = root.querySelector("#cs-hist");
    if (!box.offsetParent) return;
    const w = W(box), h = 250, s0 = +slider.value;
    const bins = [["Under 60", -Infinity, 60], ["60–69.99", 60, 70], ["70–79.99", 70, 80], ["80–89.99", 80, 90], ["90–100", 90, 100], ["Over 100†", 100, Infinity]];
    const rows = bins.map(([l, x, y]) => [l, N * (m.cdf(y) - m.cdf(x)), x, y]).filter(([, v], i) => (i > 0 && i < 5) || v >= 0.05);
    const P = { l: 8, r: 8, t: 26, b: 34 }, bw = (w - P.l - P.r) / rows.length, ymax = Math.max(1, ...rows.map((r) => r[1])) * 1.2;
    const Y = (v) => h - P.b - v / ymax * (h - P.t - P.b), c = COLOR[a.id];
    let s = `<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" aria-label="Estimated students per score band for ${a.label}"><defs><pattern id="cs-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" class="cs-hatch"/></pattern></defs>`;
    rows.forEach(([l, v, lo, hi]) => {
      const i = rows.findIndex((r) => r[0] === l), x = P.l + i * bw + bw * 0.16, bwi = bw * 0.68, here = s0 >= lo && (s0 < hi || (hi === 100 && s0 === 100));
      s += `<g class="cs-bar${here ? " here" : ""}" data-tip="<strong>${l}%</strong><br>≈ ${f(v, 1)} of ${N} students (estimate)">`
        + `<rect x="${x}" y="${Y(v)}" width="${bwi}" height="${Math.max(0, h - P.b - Y(v))}" rx="8" style="fill:${c}" class="cs-hb"/><rect x="${x}" y="${Y(v)}" width="${bwi}" height="${Math.max(0, h - P.b - Y(v))}" rx="8" fill="url(#cs-hatch)"/>`
        + `<text x="${x + bwi / 2}" y="${Y(v) - 7}" text-anchor="middle" class="cs-val${v < 0.05 ? " zero" : ""}">${v < 0.05 ? "0" : `≈${f(v, 1)}`}</text>`
        + `<text x="${x + bwi / 2}" y="${h - P.b + 18}" text-anchor="middle" class="cs-ax">${l}${here ? " ◂" : ""}</text></g>`;
    });
    s += `<line x1="${P.l}" x2="${w - P.r}" y1="${h - P.b}" y2="${h - P.b}" class="cs-axis"/></svg>`;
    box.innerHTML = s;
    box.querySelectorAll(".cs-bar").forEach((gg) => { gg.addEventListener("pointermove", (e) => showTip(gg.dataset.tip, e.clientX, e.clientY)); gg.addEventListener("pointerleave", hideTip); });
  }

  // ---- Compare view: exams with exams, quizzes with quizzes ----
  let cmp = "mean";
  const CMP = {
    mean: { t: "Class average", v: (a) => a.mean, fmt: (v) => pct(v), lo: 0, hi: 100 },
    sd: { t: "Standard deviation (points)", v: (a) => a.sd, fmt: (v) => f(v), lo: 0, hi: 14 },
    range: { t: "Lowest to highest grade · tick = average", v: (a) => a.max, fmt: (v, a) => `${a.min}–${a.max}%`, lo: 50, hi: 100 },
    cv: { t: "Relative spread (SD ÷ average)", v: (a) => 100 * a.sd / a.mean, fmt: (v) => pct(v), lo: 0, hi: 16 },
  };
  function compare() {
    const C = CMP[cmp], box = root.querySelector("#cs-cmp");
    if (!box.offsetParent) return;
    const w = W(box), rowH = 40, P = { l: Math.min(150, w * 0.32), r: 74 };
    const X = (v) => P.l + (v - C.lo) / (C.hi - C.lo) * (w - P.l - P.r);
    let html = `<p class="cs-ax-t">${C.t}</p>`;
    Object.values(GROUPS).forEach((G) => {
      const list = G.ids.map((i) => byId[i]), h = list.length * rowH + 6;
      let s = `<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" aria-label="${C.t}: ${G.label}">`;
      list.forEach((a, i) => {
        const y = i * rowH + 6, bh = rowH - 16, c = COLOR[a.id];
        s += `<text x="${P.l - 10}" y="${y + bh / 2 + 4}" text-anchor="end" class="cs-rowl">${a.label}</text>`;
        if (a.mean === null) { s += `<rect x="${P.l}" y="${y}" width="${w - P.l - P.r}" height="${bh}" rx="7" class="cs-nabar"/><text x="${P.l + 10}" y="${y + bh / 2 + 4}" class="cs-ax">no numbers released</text>`; return; }
        const v = C.v(a), xa = cmp === "range" ? X(a.min) : X(C.lo);
        s += `<g class="cs-cbar" data-tip="<strong>${a.label}</strong><br>${C.t.split(" · ")[0]}: ${C.fmt(v, a)}"><rect x="${xa}" y="${y}" width="${Math.max(2, X(v) - xa)}" height="${bh}" rx="7" style="fill:${c}" class="cs-cb"/>`
          + (cmp === "range" ? `<line x1="${X(a.mean)}" x2="${X(a.mean)}" y1="${y - 3}" y2="${y + bh + 3}" class="cs-meanmark"/>` : "")
          + `<text x="${X(v) + 8}" y="${y + bh / 2 + 4}" class="cs-val">${C.fmt(v, a)}</text></g>`;
      });
      s += `</svg>`;
      let diff = "";
      const nums = list.filter((a) => a.mean !== null);
      if (nums.length === 2) {
        const [p, q] = nums, d = C.v(p) - C.v(q);
        diff = cmp === "range" ? `${p.short} ${p.max - p.min} pts wide vs ${q.short} ${q.max - q.min} pts` : `${p.short} − ${q.short}: <strong>${sgn(d, 2)}${cmp === "sd" ? " pts" : cmp === "mean" ? " pts" : " points of %"}</strong>`;
      }
      html += `<div class="cs-grp"><div class="cs-grp-h"><span class="cs-type ${G.ids[0] && byId[G.ids[0]].type}">${G.label}</span>${diff ? `<span class="small">${diff} ${tag("calc")}</span>` : `<span class="small muted">only one with numbers — nothing to compare yet</span>`}</div>${s}</div>`;
    });
    box.innerHTML = html;
    box.querySelectorAll(".cs-cbar").forEach((gg) => { gg.addEventListener("pointermove", (e) => showTip(gg.dataset.tip, e.clientX, e.clientY)); gg.addEventListener("pointerleave", hideTip); });
  }

  // ---- wiring ----
  const tabs = [...root.querySelectorAll(".cs-vtabs [data-view]")];
  const showView = (v) => {
    tabs.forEach((t) => t.setAttribute("aria-selected", t.dataset.view === v));
    root.querySelectorAll(".cs-view").forEach((p) => { const on = p.dataset.view === v; p.hidden = !on; if (on) { p.classList.remove("cs-in"); void p.offsetWidth; p.classList.add("cs-in"); } });
    if (v === "bands") hist(); if (v === "compare") compare(); if (v === "curve") dist();
  };
  tabs.forEach((t) => t.addEventListener("click", () => showView(t.dataset.view)));
  root.querySelector(".cs-vtabs").addEventListener("keydown", (e) => {
    const i = tabs.findIndex((t) => t.getAttribute("aria-selected") === "true"), d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
    if (d) { const n = tabs[(i + d + tabs.length) % tabs.length]; n.focus(); showView(n.dataset.view); }
  });
  root.querySelectorAll("[data-seg]").forEach((sg) => sg.addEventListener("click", (e) => {
    const b = e.target.closest("button[data-v]");
    if (!b) return;
    sg.querySelectorAll("button").forEach((x) => { x.classList.toggle("on", x === b); x.setAttribute("aria-pressed", x === b); });
    const v = b.dataset.v, k = sg.dataset.seg;
    if (k === "model") { model = v; moments(); update(); compare(); }
    if (k === "group") { group = v; sdFor = null; zoom = "all"; root.querySelectorAll('[data-seg="zoom"] button').forEach((x) => { x.classList.toggle("on", x.dataset.v === "all"); x.setAttribute("aria-pressed", x.dataset.v === "all"); if (x.dataset.v !== "all") x.textContent = ZOOM[v][x.dataset.v][1]; }); dist(); results(); }
    if (k === "zoom") { zoom = v; dist(); }
    if (k === "hist") { histA = v; hist(); }
    if (k === "cmp") { cmp = v; compare(); }
  }));
  // scores typed into the grade calculator appear here right away
  const calc = document.getElementById("calcapp");
  const refresh = () => { dist(); results(); };
  calc?.addEventListener("input", () => setTimeout(refresh, 0));
  calc?.addEventListener("click", () => setTimeout(refresh, 0));
  addEventListener("storage", (e) => { if (e.key === "grades:v1") refresh(); });
  moments(); dist(); results();
  let rt = 0, lastW = root.clientWidth;
  addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => { if (root.clientWidth !== lastW) { lastW = root.clientWidth; dist(); hist(); compare(); } }, 150); });
})();
