// Class performance dashboard (syllabus page). Reported numbers come from #class-stats-data; everything else is
// calculated from them or modeled. No individual score is ever invented: the curves and counts are statistical models.
(() => {
  const root = document.getElementById("csapp"), src = document.getElementById("class-stats-data");
  if (!root || !src) return;
  const D = JSON.parse(src.textContent), N = D.cohort;
  const ALL = D.assessments, NUM = ALL.filter((a) => a.mean !== null);
  const COLOR = { u1: "var(--accent)", u2: "var(--violet)", q1: "var(--text-2)", q2: "var(--warn)" };
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
  const f = (x, d = 2) => (Math.round(x * 10 ** d) / 10 ** d).toFixed(d);
  const pct = (x) => `${f(x)}%`;

  // ---- normal-model math ----
  const SQ2PI = Math.sqrt(2 * Math.PI);
  const phi = (z) => Math.exp(-z * z / 2) / SQ2PI;
  function erf(x) {  // Abramowitz & Stegun 7.1.26 (|error| < 1.5e-7)
    const s = Math.sign(x), t = 1 / (1 + 0.3275911 * Math.abs(x));
    const y = 1 - ((((1.061405429 * t - 1.453152027) * t + 1.421413741) * t - 0.284496736) * t + 0.254829592) * t * Math.exp(-x * x);
    return s * y;
  }
  const Phi = (z) => 0.5 * (1 + erf(z / Math.SQRT2));
  const MODELS = {
    range: { name: "Truncated to reported range", short: "Reported range", bounds: (a) => [a.min, a.max] },
    scale: { name: "Truncated to 0–100% scale", short: "0–100% scale", bounds: () => [0, 100] },
    normal: { name: "Untruncated normal (reference only)", short: "Untruncated", bounds: () => [-Infinity, Infinity] },
  };
  let model = "range";
  function M(a) {
    const [lo, hi] = MODELS[model].bounds(a), al = (lo - a.mean) / a.sd, be = (hi - a.mean) / a.sd;
    const Z = Phi(be) - Phi(al);
    return {
      lo, hi,
      pdf: (x) => (x < lo || x > hi ? 0 : phi((x - a.mean) / a.sd) / a.sd / Z),
      cdf: (x) => (x <= lo ? 0 : x >= hi ? 1 : (Phi((x - a.mean) / a.sd) - Phi(al)) / Z),
      // the truncated model's own mean and SD: these drift away from the reported parameters
      moments() {
        const pa = isFinite(al) ? phi(al) : 0, pb = isFinite(be) ? phi(be) : 0, aa = isFinite(al) ? al * pa : 0, bb = isFinite(be) ? be * pb : 0;
        const m = a.mean + a.sd * (pa - pb) / Z, v = a.sd * a.sd * (1 + (aa - bb) / Z - ((pa - pb) / Z) ** 2);
        return { mean: m, sd: Math.sqrt(v) };
      },
    };
  }

  // ---- shared bits ----
  const TAG = { rep: ["Reported", "Numbers the course announced"], calc: ["Calculated", "Arithmetic on reported numbers"], mod: ["Modeled", "Estimates from a normal model — not real grades"], fb: ["Instructor feedback", "Words, not numbers"] };
  const tag = (k) => `<span class="cs-tag cs-${k}" title="${TAG[k][1]}">${TAG[k][0]}</span>`;
  const typeBadge = (a) => `<span class="cs-type ${a.type}">${a.type === "exam" ? "Exam" : "Quiz"}</span>`;
  const seg = (name, opts, on) => `<div class="seg cs-seg" role="group" data-seg="${name}">${opts.map(([v, l]) => `<button type="button" data-v="${v}" class="${v === on ? "on" : ""}" aria-pressed="${v === on}">${l}</button>`).join("")}</div>`;
  const NS = "http://www.w3.org/2000/svg";
  const W = (el) => Math.max(300, Math.min(980, el.clientWidth || 700));
  const tip = Object.assign(document.createElement("div"), { className: "cs-tip", role: "status" });
  tip.hidden = true;
  document.body.append(tip);
  const showTip = (html, x, y) => { tip.innerHTML = html; tip.hidden = false; const r = tip.getBoundingClientRect(); tip.style.left = `${Math.min(innerWidth - r.width - 8, Math.max(8, x + 14))}px`; tip.style.top = `${Math.max(8, y - r.height - 12)}px`; };
  const hideTip = () => (tip.hidden = true);

  const hi = NUM.reduce((a, b) => (b.mean > a.mean ? b : a)), lo = NUM.reduce((a, b) => (b.mean < a.mean ? b : a));
  const maxSd = NUM.reduce((a, b) => (b.sd > a.sd ? b : a));
  const byId = Object.fromEntries(ALL.map((a) => [a.id, a]));

  root.innerHTML = `
<div class="cs-legendbar">${Object.keys(TAG).map(tag).join("")}<span class="small muted">Class size is <strong>assumed</strong> to be ${N} on every assessment; participation counts are not confirmed.</span></div>

<h3 class="cs-h">Performance overview</h3>
<div class="cs-kpis">
  <div class="cs-kpi"><span class="cs-k">Class size</span><strong>${N}<sup>*</sup></strong><span class="small muted">assumed for all four</span></div>
  <div class="cs-kpi"><span class="cs-k">Highest average</span><strong>${pct(hi.mean)}</strong><span class="small muted">${hi.label} ${tag("rep")}</span></div>
  <div class="cs-kpi"><span class="cs-k">Lowest reported average</span><strong>${pct(lo.mean)}</strong><span class="small muted">${lo.label} ${tag("rep")}</span></div>
  <div class="cs-kpi"><span class="cs-k">Most spread out</span><strong>SD ${f(maxSd.sd)}</strong><span class="small muted">${maxSd.label} ${tag("rep")}</span></div>
</div>
<div class="cs-cards">${ALL.map((a) => a.mean === null ? `
  <div class="cs-card na" style="--c:${COLOR[a.id]}"><div class="cs-ch"><strong>${a.label}</strong>${typeBadge(a)}</div>
    <div class="cs-big">N/A</div><p class="small muted">No average, SD or range was released. ${tag("fb")}</p>
    <div class="cs-avail"><span class="no">Average</span><span class="no">SD</span><span class="no">Min/Max</span><span class="yes">Feedback</span></div></div>` : `
  <div class="cs-card" style="--c:${COLOR[a.id]}"><div class="cs-ch"><strong>${a.label}</strong>${typeBadge(a)}</div>
    <div class="cs-big">${pct(a.mean)}<span>average</span></div>
    <dl><dt>SD</dt><dd>${f(a.sd)} pts</dd><dt>Min – max</dt><dd>${a.min}–${a.max}%</dd><dt>Range width</dt><dd>${a.max - a.min} pts</dd></dl>
    <div class="cs-avail"><span class="yes">Average</span><span class="yes">SD</span><span class="yes">Min/Max</span><span class="${a.quote ? "yes" : "no"}">Feedback</span></div></div>`).join("")}
</div>

<div class="cs-model card">
  <div><strong>Model used for every estimate below</strong> ${tag("mod")}
  <p class="small muted">A normal curve with the reported mean and SD as its parameters, cut off at the bounds you pick. Real grades are bounded and rarely normal, so treat every curve, count and percentile as an estimate.</p></div>
  ${seg("model", Object.entries(MODELS).map(([k, m]) => [k, m.short]), model)}
  <div class="cs-moments" id="cs-moments"></div>
</div>

<h3 class="cs-h">Modeled grade distributions ${tag("mod")}</h3>
<div class="card cs-panel">
  <div class="cs-ctl"><div class="cs-toggles" id="cs-toggles">${NUM.map((a) => `<label class="cs-tog" style="--c:${COLOR[a.id]}"><input type="checkbox" data-a="${a.id}" checked><span></span>${a.label}</label>`).join("")}</div>
  <div class="cs-ctl-r"><span class="small muted">SD guides</span>${seg("sdg", [...NUM.map((a) => [a.id, a.short]), ["none", "Off"]], "q2")}<button type="button" class="vz-btn" id="cs-unzoom" hidden>Reset zoom</button></div></div>
  <div class="cs-chart" id="cs-dist"></div>
  <p class="small muted cs-note">Statistical model, not observed grades. Drag across the chart to zoom into a score range; hover for the modeled density. Shaded area above 100% is unattainable — it only appears in the untruncated model.</p>
</div>

<h3 class="cs-h">Estimated students per score band ${tag("mod")}</h3>
<div class="card cs-panel">
  <div class="cs-ctl">${seg("hist", NUM.map((a) => [a.id, a.label]), "q2")}<span class="small muted" id="cs-hist-sum"></span></div>
  <div class="cs-chart" id="cs-hist"></div>
  <p class="small muted cs-note">Expected counts = ${N} × modeled probability. Fractions are kept on purpose: 2.4 means "about two or three students under the model," never a real count.</p>
</div>

<h3 class="cs-h">Score explorer ${tag("mod")}</h3>
<div class="card cs-panel">
  <p class="small muted" style="margin-top:0">Pick a <strong>hypothetical</strong> score. The results are model estimates, not anyone's real rank.</p>
  <div class="cs-slide"><input type="range" id="cs-score" min="0" max="100" step="0.5" value="90" aria-label="Hypothetical score"><output id="cs-score-out">90%</output></div>
  <div class="cs-presets">${[60, 70, 80, 85, 90, 95, 98, 100].map((s) => `<button type="button" class="sch-chip" data-s="${s}">${s}%</button>`).join("")}</div>
  <div class="cs-ex" id="cs-ex"></div>
  <p class="cs-rel" id="cs-rel"></p>
</div>

<h3 class="cs-h">Class comparison</h3>
<div class="card cs-panel">
  <div class="cs-ctl">${seg("cmp", [["mean", "Averages"], ["sd", "Standard deviation"], ["range", "Min – max"], ["width", "Range width"], ["cv", "Coefficient of variation"]], "mean")}
  <span class="cs-key small"><i class="exam"></i>Exam <i class="quiz"></i>Quiz</span></div>
  <div class="cs-chart" id="cs-cmp"></div>
  <div class="table-wrap"><table class="cs-table"><thead><tr><th>Statistic</th>${ALL.map((a) => `<th>${a.label} ${typeBadge(a)}</th>`).join("")}<th>Source</th></tr></thead><tbody>
  ${[["Class average", (a) => pct(a.mean), "rep"], ["Standard deviation", (a) => f(a.sd), "rep"], ["Minimum grade", (a) => `${a.min}%`, "rep"], ["Maximum grade", (a) => `${a.max}%`, "rep"],
     ["Class size", () => `${N}*`, "rep"], ["Range width", (a) => a.max - a.min, "calc"], ["Mean − 2 SD", (a) => pct(a.mean - 2 * a.sd), "calc"], ["Mean − 1 SD", (a) => pct(a.mean - a.sd), "calc"],
     ["Mean + 1 SD", (a) => pct(a.mean + a.sd) + (a.mean + a.sd > 100 ? "†" : ""), "calc"], ["Mean + 2 SD", (a) => pct(a.mean + 2 * a.sd) + (a.mean + 2 * a.sd > 100 ? "†" : ""), "calc"],
     ["Coefficient of variation", (a) => pct(100 * a.sd / a.mean), "calc"]]
    .map(([n, fn, k]) => `<tr><td>${n}</td>${ALL.map((a) => `<td>${a.mean === null && n !== "Class size" ? '<span class="muted">N/A</span>' : fn(a)}</td>`).join("")}<td>${tag(k)}</td></tr>`).join("")}
  </tbody></table></div>
  <p class="small muted">* Assumed. † Mathematical SD threshold above 100% — not an attainable grade.</p>
  <div class="cs-diffs">${[["u1", "u2"], ["u2", "q2"], ["u1", "q2"]].map(([x, y]) => `<div><span class="small muted">${byId[x].short} vs ${byId[y].short} average</span><strong>${f(byId[x].mean - byId[y].mean)} pts</strong><span class="small">higher on ${byId[x].short}</span></div>`).join("")}
  ${[["q2", "u2"], ["q2", "u1"]].map(([x, y]) => `<div><span class="small muted">${byId[x].short} SD ÷ ${byId[y].short} SD</span><strong>${f(byId[x].sd / byId[y].sd)}×</strong><span class="small">as spread out</span></div>`).join("")}</div>
  <p class="small muted">${tag("calc")} These are differences, not trends: the four assessments differ in format, content and stakes, so they are not repeated measures of the same skill. No significance test is possible without the raw scores.</p>
</div>

<h3 class="cs-h">In-Class Quiz 1</h3>
<div class="card cs-q1">
  <div class="cs-ch"><strong>Statistics unavailable</strong>${typeBadge(byId.q1)}${tag("fb")}</div>
  <blockquote>“${esc(byId.q1.quote)}”</blockquote>
  <div class="grid two"><div><h4>What it tells us</h4><ul class="small"><li>After Quiz 1, every student's <em>overall course grade</em> was still on an A track.</li><li>Quiz 1 did not knock anyone off that track.</li></ul></div>
  <div><h4>What it does not tell us</h4><ul class="small"><li>That everyone scored an A on Quiz 1 itself — a quiz is a small share of the grade.</li><li>Any average, spread, lowest score or distribution, so Quiz 1 is left out of every chart.</li></ul></div></div>
</div>

<h3 class="cs-h">What the numbers mean</h3>
<div class="cs-interp">
  <div class="card"><h4>How strongly the class did</h4><p class="small">Both exams averaged above 93% with small SDs — most of the class sat near the top. ${byId.q2.label} averaged ${pct(byId.q2.mean)}, still a B-range average, with a much wider spread.</p></div>
  <div class="card"><h4>Highest average · most variability</h4><p class="small">Highest average: <strong>${hi.label}</strong> (${pct(hi.mean)}). Most variable: <strong>${maxSd.label}</strong> (SD ${f(maxSd.sd)}, CV ${pct(100 * maxSd.sd / maxSd.mean)}) — about twice the spread of either exam.</p></div>
  <div class="card"><h4>Standard deviation in plain terms</h4><p class="small">The typical distance of a score from the average. On Unit 2 (SD ${f(byId.u2.sd)}) most scores sat within about 5 points of ${pct(byId.u2.mean)}; on Quiz 2 (SD ${f(byId.q2.sd)}) within about 12 points of ${pct(byId.q2.mean)}.</p></div>
  <div class="card"><h4>Ceiling effects</h4><p class="small">With an average near 97%, many students are pressed against 100% and the test can't separate them further. Mean + 1 SD on Unit 1 is ${pct(byId.u1.mean + byId.u1.sd)}, a score nobody can earn — a sign the scores are piled up and skewed toward the top, not bell-shaped.</p></div>
  <div class="card"><h4>Bounded grades vs. the normal curve</h4><p class="small">A normal curve runs forever in both directions; grades stop at 0 and 100. Cutting the curve at the bounds fixes that but shifts its own mean and SD away from the reported values (see the model check above). The model is a sketch, not the real shape.</p></div>
  <div class="card"><h4>Lower average ≠ harder test</h4><p class="small">A lower average can come from harder questions, but also from less study time, a different format (in-class vs exam), fewer items (one miss costs more), or different content. The averages alone can't tell these apart.</p></div>
  <div class="card"><h4>Why no one's rank can be known</h4><p class="small">Many different sets of 33 scores share the same average, SD, minimum and maximum. Without the raw scores there is no true median, percentile or rank — only modeled estimates, and ties at 100% make "top" meaningless.</p></div>
</div>`;

  // ---- model check (truncated moments) ----
  function moments() {
    root.querySelector("#cs-moments").innerHTML = model === "normal"
      ? `<p class="small muted">Untruncated: the curve keeps the reported mean and SD exactly, but puts some probability above 100% and below 0%, which is impossible for real grades.</p>`
      : `<table class="cs-mini"><thead><tr><th>Model check</th>${NUM.map((a) => `<th>${a.short}</th>`).join("")}</tr></thead><tbody>
        <tr><td>Reported mean / SD</td>${NUM.map((a) => `<td>${f(a.mean)} / ${f(a.sd)}</td>`).join("")}</tr>
        <tr><td>Model's own mean / SD</td>${NUM.map((a) => { const m = M(a).moments(); return `<td>${f(m.mean)} / ${f(m.sd)}</td>`; }).join("")}</tr></tbody></table>
        <p class="small muted">Truncating keeps scores in bounds, but the model's own mean and SD no longer equal the reported ones — the reported values are used as parameters, not preserved.</p>`;
  }

  // ---- distribution chart ----
  const shown = new Set(NUM.map((a) => a.id));
  let sdg = "q2", dom = null;
  const baseDom = () => (model === "normal" ? [40, 115] : model === "scale" ? [40, 100] : [55, 100]);
  function dist() {
    const box = root.querySelector("#cs-dist"), w = W(box), h = Math.round(Math.min(360, Math.max(240, w * 0.42)));
    const P = { l: 46, r: 14, t: 26, b: 38 }, [x0, x1] = dom || baseDom();
    const vis = NUM.filter((a) => shown.has(a.id));
    const step = (x1 - x0) / 300;
    const series = vis.map((a) => { const m = M(a), pts = []; for (let x = x0; x <= x1 + 1e-9; x += step) pts.push([x, m.pdf(x)]); return { a, m, pts }; });
    const ymax = Math.max(0.02, ...series.flatMap((s) => s.pts.map((p) => p[1]))) * 1.12;
    const X = (x) => P.l + (x - x0) / (x1 - x0) * (w - P.l - P.r), Y = (y) => h - P.b - y / ymax * (h - P.t - P.b);
    const xt = []; const xs = (x1 - x0) > 40 ? 10 : (x1 - x0) > 15 ? 5 : (x1 - x0) > 6 ? 2 : 1;
    for (let x = Math.ceil(x0 / xs) * xs; x <= x1; x += xs) xt.push(x);
    const yt = [0, ymax / 3, 2 * ymax / 3].map((y) => +y.toFixed(3));
    let s = `<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" aria-label="Modeled probability density curves for ${vis.map((a) => a.label).join(", ")}">`;
    s += `<text x="${P.l}" y="14" class="cs-ax-t">Modeled density (share of class per 1-point band)</text>`;
    yt.forEach((y) => (s += `<line x1="${P.l}" x2="${w - P.r}" y1="${Y(y)}" y2="${Y(y)}" class="cs-grid"/><text x="${P.l - 6}" y="${Y(y) + 4}" text-anchor="end" class="cs-ax">${y.toFixed(2)}</text>`));
    if (x1 > 100) s += `<rect x="${X(Math.max(100, x0))}" y="${P.t}" width="${X(x1) - X(Math.max(100, x0))}" height="${h - P.t - P.b}" class="cs-unatt"/><text x="${X(Math.max(100, x0)) + 4}" y="${P.t + 12}" class="cs-ax">above 100% — unattainable</text>`;
    const g = NUM.find((a) => a.id === sdg && shown.has(a.id));
    if (g) {
      const c = COLOR[g.id];
      [[2, 0.06], [1, 0.1]].forEach(([k, op]) => { const a = Math.max(x0, g.mean - k * g.sd), b = Math.min(x1, g.mean + k * g.sd); if (b > a) s += `<rect x="${X(a)}" y="${P.t}" width="${X(b) - X(a)}" height="${h - P.t - P.b}" style="fill:${c};opacity:${op}"/>`; });
      [-2, -1, 1, 2].forEach((k) => { const x = g.mean + k * g.sd; if (x >= x0 && x <= x1) s += `<line x1="${X(x)}" x2="${X(x)}" y1="${P.t}" y2="${h - P.b}" style="stroke:${c}" class="cs-sdl"/><text x="${X(x)}" y="${P.t - 4}" text-anchor="middle" class="cs-ax" style="fill:${c}">${k > 0 ? "+" : "−"}${Math.abs(k)} SD${x > 100 ? "†" : ""}</text>`; });
    }
    series.forEach(({ a, pts }, si) => {
      const c = COLOR[a.id], d = pts.map((p, i) => `${i ? "L" : "M"}${X(p[0]).toFixed(1)},${Y(p[1]).toFixed(1)}`).join("");
      s += `<path d="${d}L${X(x1)},${Y(0)}L${X(x0)},${Y(0)}Z" style="fill:${c}" class="cs-area"/><path d="${d}" style="stroke:${c}" class="cs-line"/>`;
      if (a.mean >= x0 && a.mean <= x1) s += `<line x1="${X(a.mean)}" x2="${X(a.mean)}" y1="${Y(0)}" y2="${P.t + 8}" style="stroke:${c}" class="cs-mean"/><circle cx="${X(a.mean)}" cy="${P.t + 8}" r="4" style="fill:${c}"/><text x="${X(a.mean) - 6}" y="${P.t + 22 + si * 14}" text-anchor="end" class="cs-ax cs-ml" style="fill:${c}">x̄ ${f(a.mean, 1)}</text>`;
    });
    s += `<line x1="${P.l}" x2="${w - P.r}" y1="${Y(0)}" y2="${Y(0)}" class="cs-axis"/>`;
    xt.forEach((x) => (s += `<text x="${X(x)}" y="${h - P.b + 16}" text-anchor="middle" class="cs-ax">${x}%</text>`));
    s += `<text x="${(w + P.l) / 2}" y="${h - 4}" text-anchor="middle" class="cs-ax-t">Score (%) · model, not observed grades</text>`;
    s += `<line class="cs-hair" x1="0" x2="0" y1="${P.t}" y2="${h - P.b}" hidden/><rect class="cs-brush" y="${P.t}" height="${h - P.t - P.b}" width="0" hidden/>`;
    s += `<rect x="${P.l}" y="${P.t}" width="${w - P.l - P.r}" height="${h - P.t - P.b}" fill="transparent" class="cs-hit"/></svg>`;
    if (!vis.length) s = `<p class="muted small">Turn on at least one assessment.</p>`;
    box.innerHTML = s;
    root.querySelector("#cs-unzoom").hidden = !dom;
    const svg = box.querySelector("svg");
    if (!svg) return;
    const hair = svg.querySelector(".cs-hair"), brush = svg.querySelector(".cs-brush"), hit = svg.querySelector(".cs-hit");
    const toX = (e) => { const r = svg.getBoundingClientRect(); return Math.min(w - P.r, Math.max(P.l, (e.clientX - r.left) * w / r.width)); };
    const inv = (px) => x0 + (px - P.l) / (w - P.l - P.r) * (x1 - x0);
    let start = null;
    hit.addEventListener("pointerdown", (e) => { start = toX(e); hit.setPointerCapture(e.pointerId); });
    hit.addEventListener("pointermove", (e) => {
      const px = toX(e), x = inv(px);
      hair.removeAttribute("hidden"); hair.setAttribute("x1", px); hair.setAttribute("x2", px);
      if (start !== null) { brush.removeAttribute("hidden"); brush.setAttribute("x", Math.min(start, px)); brush.setAttribute("width", Math.abs(px - start)); }
      showTip(`<strong>Score ${f(x, 1)}%</strong>${x > 100 ? ' <span class="muted">(unattainable)</span>' : ""}<br>${series.map(({ a, m }) => `<span class="cs-dot" style="background:${COLOR[a.id]}"></span>${a.short}: density ${m.pdf(x).toFixed(4)} <span class="muted">≈ ${f(100 * m.pdf(x), 1)}% of class per point</span>`).join("<br>")}<br><span class="muted small">Modeled, not observed.</span>`, e.clientX, e.clientY);
    });
    const end = (e) => {
      if (start === null) return;
      const px = toX(e), a = inv(Math.min(start, px)), b = inv(Math.max(start, px));
      start = null;
      if (b - a >= 2) { dom = [Math.round(a * 2) / 2, Math.round(b * 2) / 2]; dist(); }
      else brush.setAttribute("hidden", "");
    };
    hit.addEventListener("pointerup", end);
    hit.addEventListener("pointercancel", () => { start = null; brush.setAttribute("hidden", ""); });
    hit.addEventListener("pointerleave", () => { hair.setAttribute("hidden", ""); hideTip(); });
    hit.addEventListener("dblclick", () => { dom = null; dist(); });
  }

  // ---- expected-count histogram ----
  let histA = "q2";
  function hist() {
    const a = byId[histA], m = M(a), box = root.querySelector("#cs-hist"), w = W(box), h = 260;
    const bins = [["Below 60%", -Infinity, 60], ["60–69.99%", 60, 70], ["70–79.99%", 70, 80], ["80–89.99%", 80, 90], ["90–100%", 90, 100], ["Above 100%†", 100, Infinity]];
    const rows = bins.map(([l, x, y]) => [l, N * ((y === 100 ? m.cdf(100) : m.cdf(y)) - m.cdf(x))]).filter(([l, v], i) => (i > 0 && i < 5) || v >= 0.005);
    const P = { l: 40, r: 10, t: 28, b: 40 }, bw = (w - P.l - P.r) / rows.length, ymax = Math.max(1, ...rows.map((r) => r[1])) * 1.18;
    const Y = (v) => h - P.b - v / ymax * (h - P.t - P.b), c = COLOR[a.id];
    let s = `<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" aria-label="Modeled expected student counts per score band for ${a.label}"><defs><pattern id="cs-hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" class="cs-hatch"/></pattern></defs>`;
    s += `<text x="${P.l}" y="14" class="cs-ax-t">Expected students (modeled, of ${N} assumed)</text>`;
    rows.forEach(([l, v], i) => {
      const x = P.l + i * bw + bw * 0.14, bwi = bw * 0.72;
      s += `<g class="cs-bar" data-tip="<strong>${l}</strong><br>${a.label}: ≈ ${f(v, 1)} students (modeled)<br><span class='muted'>${f(100 * v / N, 1)}% of the model's probability</span>">`
        + `<rect x="${x}" y="${Y(v)}" width="${bwi}" height="${Math.max(0, h - P.b - Y(v))}" rx="6" style="fill:${c}" class="cs-hb"/><rect x="${x}" y="${Y(v)}" width="${bwi}" height="${Math.max(0, h - P.b - Y(v))}" rx="6" fill="url(#cs-hatch)"/>`
        + `<text x="${x + bwi / 2}" y="${Y(v) - 6}" text-anchor="middle" class="cs-val">≈${f(v, 1)}</text>`
        + `<text x="${x + bwi / 2}" y="${h - P.b + 16}" text-anchor="middle" class="cs-ax">${l}</text></g>`;
    });
    s += `<line x1="${P.l}" x2="${w - P.r}" y1="${h - P.b}" y2="${h - P.b}" class="cs-axis"/></svg>`;
    box.innerHTML = s;
    const total = rows.reduce((t, r) => t + r[1], 0);
    root.querySelector("#cs-hist-sum").textContent = `${MODELS[model].short} model · bars sum to ≈ ${f(total, 1)}${model === "normal" ? " (some modeled probability falls outside 0–100%)" : ""}`;
    box.querySelectorAll(".cs-bar").forEach((g) => { g.addEventListener("pointermove", (e) => showTip(g.dataset.tip, e.clientX, e.clientY)); g.addEventListener("pointerleave", hideTip); });
  }

  // ---- score explorer ----
  const slider = root.querySelector("#cs-score");
  function explore() {
    const s = +slider.value;
    root.querySelector("#cs-score-out").textContent = `${s}%`;
    root.querySelectorAll(".cs-presets button").forEach((b) => b.classList.toggle("on", +b.dataset.s === s));
    const res = NUM.map((a) => { const m = M(a), p = m.cdf(s), z = (s - a.mean) / a.sd; return { a, z, p, d: s - a.mean }; });
    root.querySelector("#cs-ex").innerHTML = res.map(({ a, z, p, d }) => {
      const note = s < a.min ? `Below the lowest reported score (${a.min}%).` : s >= a.max ? `At the reported maximum — several students may share it, so this is not a rank.` : "";
      return `<div class="cs-exc" style="--c:${COLOR[a.id]}"><div class="cs-ch"><strong>${a.label}</strong>${typeBadge(a)}</div>
        <div class="cs-pbar" aria-hidden="true"><span style="width:${(100 * p).toFixed(1)}%"></span></div>
        <dl><dt>vs. class mean</dt><dd class="${d >= 0 ? "up" : "down"}">${d >= 0 ? "+" : "−"}${f(Math.abs(d))} pts</dd>
        <dt title="(score − mean) ÷ SD">Z-score</dt><dd>${z >= 0 ? "+" : "−"}${f(Math.abs(z))}</dd>
        <dt>Est. percentile</dt><dd>${f(100 * p, 1)}<span class="small muted">th</span></dd>
        <dt>Est. students below</dt><dd>≈ ${f(N * p, 1)}</dd><dt>Est. students above</dt><dd>≈ ${f(N * (1 - p), 1)}</dd></dl>
        ${note ? `<p class="small muted cs-exn">${note}</p>` : ""}</div>`;
    }).join("") + `<div class="cs-exc na"><div class="cs-ch"><strong>${byId.q1.label}</strong>${typeBadge(byId.q1)}</div><p class="small muted">No statistics released — this score can't be compared with the Quiz 1 class.</p></div>`;
    const sorted = [...res].sort((x, y) => y.z - x.z), b = sorted[0], w = sorted[sorted.length - 1];
    root.querySelector("#cs-rel").innerHTML = `${tag("mod")} Relative to each class, a hypothetical <strong>${s}%</strong> stands out most on <strong style="color:${COLOR[b.a.id]}">${b.a.label}</strong> (z ${b.z >= 0 ? "+" : "−"}${f(Math.abs(b.z))}) and least on <strong style="color:${COLOR[w.a.id]}">${w.a.label}</strong> (z ${w.z >= 0 ? "+" : "−"}${f(Math.abs(w.z))}). Percentiles use the <em>${MODELS[model].name.toLowerCase()}</em> model; students above + below = ${N} (assumed).`;
  }
  slider.addEventListener("input", explore);
  root.querySelectorAll(".cs-presets button").forEach((b) => b.addEventListener("click", () => { slider.value = b.dataset.s; explore(); }));

  // ---- comparison chart ----
  let cmp = "mean";
  const CMP = {
    mean: { t: "Class average (%)", v: (a) => a.mean, fmt: (v) => pct(v), lo: 0, hi: 100, k: "rep" },
    sd: { t: "Standard deviation (points)", v: (a) => a.sd, fmt: (v) => f(v), lo: 0, hi: 14, k: "rep" },
    range: { t: "Lowest to highest reported grade (%)", v: (a) => a.max, fmt: (v, a) => `${a.min}–${a.max}%`, lo: 50, hi: 100, k: "rep" },
    width: { t: "Range width (max − min, points)", v: (a) => a.max - a.min, fmt: (v) => `${v} pts`, lo: 0, hi: 45, k: "calc" },
    cv: { t: "Coefficient of variation (SD ÷ mean)", v: (a) => 100 * a.sd / a.mean, fmt: (v) => pct(v), lo: 0, hi: 16, k: "calc" },
  };
  function compare() {
    const C = CMP[cmp], box = root.querySelector("#cs-cmp"), w = W(box), rowH = 44, P = { l: Math.min(150, w * 0.3), r: 70, t: 30, b: 10 }, h = P.t + ALL.length * rowH + P.b;
    const X = (v) => P.l + (v - C.lo) / (C.hi - C.lo) * (w - P.l - P.r);
    let s = `<svg viewBox="0 0 ${w} ${h}" width="${w}" height="${h}" role="img" aria-label="${C.t} by assessment"><text x="${P.l}" y="16" class="cs-ax-t">${C.t}</text>`;
    s += `<defs><pattern id="cs-stripe" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" class="cs-stripe"/></pattern></defs>`;
    ALL.forEach((a, i) => {
      const y = P.t + i * rowH + 8, bh = rowH - 18, c = COLOR[a.id];
      s += `<text x="${P.l - 10}" y="${y + bh / 2 + 4}" text-anchor="end" class="cs-rowl">${a.label}</text>`;
      if (a.mean === null) { s += `<rect x="${P.l}" y="${y}" width="${w - P.l - P.r}" height="${bh}" rx="7" class="cs-nabar"/><text x="${P.l + 10}" y="${y + bh / 2 + 4}" class="cs-ax">N/A — no statistics released</text>`; return; }
      const v = C.v(a), x0 = cmp === "range" ? X(a.min) : X(C.lo);
      s += `<g class="cs-cbar" data-tip="<strong>${a.label}</strong> (${a.type})<br>${C.t}: ${C.fmt(v, a)}"><rect x="${x0}" y="${y}" width="${Math.max(2, X(v) - x0)}" height="${bh}" rx="7" style="fill:${c}" class="cs-cb ${a.type}"/>${a.type === "quiz" ? `<rect x="${x0}" y="${y}" width="${Math.max(2, X(v) - x0)}" height="${bh}" rx="7" fill="url(#cs-stripe)"/>` : ""}`;
      if (cmp === "range") s += `<line x1="${X(a.mean)}" x2="${X(a.mean)}" y1="${y - 3}" y2="${y + bh + 3}" class="cs-meanmark"/>`;
      s += `<text x="${X(v) + 8}" y="${y + bh / 2 + 4}" class="cs-val">${C.fmt(v, a)}</text></g>`;
    });
    s += `</svg>`;
    box.innerHTML = s + (cmp === "range" ? `<p class="small muted">Bars run from the lowest to the highest reported grade; the tick marks the average.</p>` : "");
    box.querySelectorAll(".cs-cbar").forEach((g) => { g.addEventListener("pointermove", (e) => showTip(g.dataset.tip, e.clientX, e.clientY)); g.addEventListener("pointerleave", hideTip); });
  }

  // ---- wiring ----
  root.querySelectorAll("[data-seg]").forEach((sg) => sg.addEventListener("click", (e) => {
    const b = e.target.closest("button[data-v]");
    if (!b) return;
    sg.querySelectorAll("button").forEach((x) => { x.classList.toggle("on", x === b); x.setAttribute("aria-pressed", x === b); });
    const v = b.dataset.v, k = sg.dataset.seg;
    if (k === "model") { model = v; dom = null; renderAll(); }
    if (k === "sdg") { sdg = v; dist(); }
    if (k === "hist") { histA = v; hist(); }
    if (k === "cmp") { cmp = v; compare(); }
  }));
  root.querySelectorAll("#cs-toggles input").forEach((i) => i.addEventListener("change", () => { i.checked ? shown.add(i.dataset.a) : shown.delete(i.dataset.a); dist(); }));
  root.querySelector("#cs-unzoom").addEventListener("click", () => { dom = null; dist(); });
  function renderAll() { moments(); dist(); hist(); explore(); compare(); }
  renderAll();
  let rt = 0, lastW = root.clientWidth;
  addEventListener("resize", () => { clearTimeout(rt); rt = setTimeout(() => { if (root.clientWidth !== lastW) { lastW = root.clientWidth; dist(); hist(); compare(); } }, 150); });
})();
