// Syllabus page: interactive grade breakdown (donut), a grade calculator,
// "coming up" deadlines, and a filterable week-by-week schedule. Weights come from the syllabus (grade-data JSON).
// Scores are saved only in this browser.
(function () {
  const D = JSON.parse(document.getElementById("grade-data")?.textContent || "null");
  if (!D) return;
  const KEY = "grades:v1";
  const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; } };
  const saveAll = (v) => { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch { /* private mode */ } };
  const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const NAMES = { exam: (i) => `Exam ${i + 1}`, final: () => "Final", quiz: (i) => `Quiz ${i + 1}`, db: (i) => `DB ${i + 1}`, case: (i) => `Case ${i + 1}` };
  const letterOf = (pts) => (D.scale.find(([, min]) => pts >= min) || D.scale[D.scale.length - 1]);
  const trunc1 = (x) => (Math.floor(x * 10) / 10).toFixed(1);  // the syllabus never rounds up
  let S = load();

  // ---------------------------------------------------------------- donut: where the points come from
  const donut = document.getElementById("donut"), legend = document.getElementById("legend"), center = document.getElementById("donut-center");
  if (donut) {
    const R = 78, C = 2 * Math.PI * R;
    let off = 0;
    donut.innerHTML = `<circle cx="100" cy="100" r="${R}" class="donut-track"/>` + D.items.map((it) => {
      const len = (it.weight / 100) * C, gap = 2.5;
      const seg = `<circle cx="100" cy="100" r="${R}" class="donut-seg" data-key="${it.key}" style="--c:var(--c-${it.key});stroke-dasharray:${Math.max(0, len - gap)} ${C};stroke-dashoffset:${-off};--len:${len}"/>`;
      off += len;
      return seg;
    }).join("");
    const show = (key) => {
      const it = D.items.find((x) => x.key === key);
      donut.classList.toggle("focus", !!key);
      donut.querySelectorAll(".donut-seg").forEach((s) => s.classList.toggle("on", s.dataset.key === key));
      legend.querySelectorAll("li").forEach((li) => li.classList.toggle("on", li.dataset.key === key));
      center.innerHTML = it ? `<strong>${it.weight}%</strong><span>${it.label}<br>${Math.round(it.weight * 10)} pts</span>`
        : key === "bonus" ? `<strong>+30</strong><span>bonus points<br>max</span>` : `<strong>1,000</strong><span>points</span>`;
    };
    donut.querySelectorAll(".donut-seg").forEach((s) => { s.addEventListener("mouseenter", () => show(s.dataset.key)); s.addEventListener("mouseleave", () => show(null)); });
    legend.querySelectorAll("li").forEach((li) => { li.addEventListener("mouseenter", () => show(li.dataset.key)); li.addEventListener("mouseleave", () => show(null)); li.addEventListener("click", () => show(li.dataset.key)); });
    // draw-in animation when the donut scrolls into view
    if (!calm && "IntersectionObserver" in window) {
      donut.classList.add("pre");
      new IntersectionObserver((es, o) => es.forEach((e) => { if (e.isIntersecting) { donut.classList.remove("pre"); o.disconnect(); } }), { threshold: .3 }).observe(donut);
    }
  }

  // ---------------------------------------------------------------- calculator: a progress donut (same language as the weights donut),
  // category cards with tap-to-type score circles, and a separate "what you need on the final" section
  const root = document.getElementById("calcapp"), froot = document.getElementById("finalapp");
  if (root) {
    const ticks = D.scale.filter(([, min]) => min > 0), final = D.items.find((i) => i.key === "final");
    const R = 78, C = 2 * Math.PI * R, ASSUME = [70, 75, 80, 85, 90, 95, 100];
    let off = 0;
    const arcs = D.items.map((it) => { const len = (it.weight / 100) * C, o = off; off += len;
      return `<circle cx="100" cy="100" r="${R}" class="pd-bg" style="--c:var(--c-${it.key});stroke-dasharray:${len - 2.5} ${C};stroke-dashoffset:${-o}"/>
        <circle cx="100" cy="100" r="${R}" class="pd-proj" data-key="${it.key}" style="--c:var(--c-${it.key});stroke-dashoffset:${-o}"/>
        <circle cx="100" cy="100" r="${R}" class="pd-seg" data-key="${it.key}" style="--c:var(--c-${it.key});stroke-dashoffset:${-o}"/>`; }).join("");
    root.innerHTML = `<div class="grade-split pd-split"><div class="donut-wrap"><svg class="donut pd" viewBox="0 0 200 200" id="pd">${arcs}</svg>
        <div class="donut-center"><strong id="pd-big">—</strong><span id="pd-sub">projected</span></div></div>
      <div class="pc-list">${D.items.filter((it) => it.key !== "final").map((it) => `<div class="pc" data-key="${it.key}" style="--c:var(--c-${it.key})">
          <div class="pc-top"><span class="lg-dot"></span><span class="pc-name">${it.label}</span><span class="pc-avg" data-avg="${it.key}">—</span></div>
          <div class="pc-dots">${Array.from({ length: it.count }, (_, i) => `<label class="pc-dot" title="${NAMES[it.key](i)}"><input type="number" inputmode="decimal" min="0" max="100" step="0.1" placeholder="${it.count > 1 ? i + 1 : "—"}" aria-label="${NAMES[it.key](i)} percent" data-k="${it.key}" data-i="${i}"></label>`).join("")}</div></div>`).join("")}
        <div class="pc" data-key="bonus" style="--c:var(--c-bonus)"><div class="pc-top"><span class="lg-dot"></span><span class="pc-name">Bonus checkpoints</span><span class="pc-avg" id="bonus-pts">—</span></div>
          <div class="pc-dots">${Array.from({ length: D.bonus.count }, (_, i) => `<label class="pc-cp" title="Checkpoint ${i + 1} (≥90%)"><input type="checkbox" data-cp="${i}"><i>${i + 1}</i></label>`).join("")}</div></div>
      </div></div>
      <div class="pc-assume"><span>Not graded yet? Assume</span><div class="seg" id="assume">${ASSUME.map((v) => `<button data-v="${v}">${v}</button>`).join("")}</div>
        <button class="pc-clear" data-clear>Clear</button></div>`;
    if (froot) froot.innerHTML = `<div class="fn-cards" id="fn-cards"></div>
      <div class="fn-try"><div class="fn-res"><span class="fn-score" id="fn-score">—</span><span class="fn-arrow">→</span><span class="fn-letter" id="fn-letter">—</span></div>
        <div class="fn-range"><div class="fn-fill" id="fn-fill"></div><div class="fn-min" title="75% minimum to pass"></div><input type="range" min="0" max="100" step="1" id="fn-in" aria-label="Try a final exam score"></div>
        <div class="fn-scale"><span>0</span><span style="left:75%">75 min</span><span>100</span></div>
        <label class="fn-real">Already took it?<input type="number" inputmode="decimal" min="0" max="100" step="0.1" placeholder="Score" aria-label="Final exam percent" data-k="final" data-i="0"></label></div>`;

    const all = document.querySelectorAll("#calcapp input[data-k], #finalapp input[data-k]");
    all.forEach((inp) => {
      const v = S[inp.dataset.k]?.[inp.dataset.i];
      if (v !== undefined && v !== null && v !== "") inp.value = v;
      inp.addEventListener("input", () => {
        (S[inp.dataset.k] ||= [])[inp.dataset.i] = inp.value === "" ? null : Math.max(0, Math.min(100, +inp.value));
        saveAll(S); calc();
      });
    });
    root.querySelectorAll("input[data-cp]").forEach((cb) => {
      cb.checked = !!S.cp?.[cb.dataset.cp];
      cb.addEventListener("change", () => { (S.cp ||= [])[cb.dataset.cp] = cb.checked; saveAll(S); calc(); });
    });
    root.querySelectorAll("#assume button").forEach((b) => b.addEventListener("click", () => { S.assume = +b.dataset.v; saveAll(S); calc(); }));
    const fin = froot?.querySelector("#fn-in");
    if (fin) { fin.value = S.fxTry ?? 85; fin.addEventListener("input", () => { S.fxTry = +fin.value; saveAll(S); calc(); }); }
    root.querySelector("[data-clear]").addEventListener("click", () => {
      if (!confirm("Clear all scores?")) return;
      S = { assume: S.assume, fxTry: S.fxTry }; saveAll(S);
      all.forEach((i) => (i.value = "")); root.querySelectorAll("input[data-cp]").forEach((c) => (c.checked = false));
      calc();
    });
    // hover a category: the donut focuses on it, the center shows its average
    const pd = root.querySelector("#pd");
    let focusKey = null;
    const focus = (k) => { focusKey = k; pd.classList.toggle("focus", !!k);
      pd.querySelectorAll("[data-key]").forEach((s) => s.classList.toggle("on", s.dataset.key === k));
      root.querySelectorAll(".pc").forEach((c) => c.classList.toggle("on", c.dataset.key === k)); calc(); };
    root.querySelectorAll(".pc").forEach((c) => { c.addEventListener("mouseenter", () => focus(c.dataset.key)); c.addEventListener("mouseleave", () => focus(null)); c.addEventListener("focusin", () => focus(c.dataset.key)); });
    pd.querySelectorAll(".pd-seg, .pd-proj").forEach((s) => { s.addEventListener("mouseenter", () => focus(s.dataset.key)); s.addEventListener("mouseleave", () => focus(null)); });

    const LC = { A: "var(--good)", B: "var(--accent)", C: "var(--warn)", F: "var(--bad)" };
    function calc() {
      const assume = S.assume ?? 85, finalScore = S.final?.[0], hasFinal = finalScore != null && finalScore !== "";
      root.querySelectorAll("#assume button").forEach((b) => b.classList.toggle("on", +b.dataset.v === assume));
      let earned = 0, possible = 0, projNoFinal = 0;
      const avg = {};
      for (const it of D.items) {
        let n = 0, sum = 0, e = 0, p = 0;
        for (let i = 0; i < it.count; i++) {
          const v = S[it.key]?.[i], has = v !== null && v !== undefined && v !== "";
          if (has) { n++; sum += v; e += (v / 100) * it.points_each; earned += (v / 100) * it.points_each; possible += it.points_each; }
          p += ((has ? v : assume) / 100) * it.points_each;
          if (it.key !== "final") projNoFinal += ((has ? v : assume) / 100) * it.points_each;
        }
        avg[it.key] = n ? sum / n : null;
        const el = root.querySelector(`[data-avg="${it.key}"]`); if (el) el.textContent = n ? `${trunc1(sum / n)}%` : "—";
        // donut: solid = points earned, tint = projected, per category (1,000 points around the ring)
        pd.querySelector(`.pd-seg[data-key="${it.key}"]`).style.strokeDasharray = `${Math.max(0, (e / 1000) * C - (e ? 2.5 : 0))} ${C}`;
        pd.querySelector(`.pd-proj[data-key="${it.key}"]`).style.strokeDasharray = `${Math.max(0, (p / 1000) * C - 2.5)} ${C}`;
      }
      root.querySelectorAll(".pc-dot").forEach((d) => { const inp = d.querySelector("input"), has = inp.value !== ""; d.classList.toggle("has", has); d.style.setProperty("--v", has ? Math.max(0, Math.min(100, +inp.value)) : 0); });
      const bonus = Math.min(D.bonus.max, (S.cp || []).filter(Boolean).length * D.bonus.points_each);
      root.querySelector("#bonus-pts").textContent = bonus ? `+${+bonus.toFixed(2)}` : "—";
      const tryF = hasFinal ? finalScore : fin ? +fin.value : assume;
      const total = (f) => Math.min(1000, projNoFinal + (f / 100) * final.points_each + bonus);
      const projTotal = total(hasFinal ? finalScore : assume), [pl] = letterOf(projTotal), cur = possible ? (100 * earned) / possible : null;
      const big = root.querySelector("#pd-big"), sub = root.querySelector("#pd-sub");
      const fit = focusKey && D.items.find((i) => i.key === focusKey);
      if (fit) { big.textContent = avg[fit.key] == null ? "—" : `${trunc1(avg[fit.key])}%`; big.style.color = `var(--c-${fit.key})`; sub.textContent = `${fit.label} average`; }
      else if (focusKey === "bonus") { big.textContent = `+${+bonus.toFixed(2)}`; big.style.color = "var(--c-bonus)"; sub.textContent = "bonus points"; }
      else { big.innerHTML = `${pl}<small>${trunc1(projTotal / 10)}%</small>`; big.style.color = LC[pl]; sub.textContent = cur === null ? "projected" : `projected · ${trunc1(cur)}% so far`; }

      if (!froot) return;
      // final: one ring per letter showing the score you'd need; tap a ring to try that score
      froot.querySelector("#fn-cards").innerHTML = ticks.map(([L, min]) => {
        const req = Math.max(75, ((min - projNoFinal - bonus) / final.points_each) * 100), out = req > 100, rc = 2 * Math.PI * 40;
        return `<button class="fn-card${out ? " out" : ""}" style="--lc:${LC[L]}" ${out ? "disabled" : `data-try="${Math.ceil(req)}"`}>
          <span class="fn-ring"><svg viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" class="fn-bg"/><circle cx="50" cy="50" r="40" class="fn-arc" style="stroke-dasharray:${out ? 0 : (req / 100) * rc} ${rc}"/></svg>
          <span class="fn-need">${out ? "—" : Math.ceil(req) + "<small>%</small>"}</span></span><span class="fn-for">${out ? `<b>${L}</b> out of reach` : `for <b>${L}</b>`}</span></button>`;
      }).join("");
      froot.querySelectorAll("[data-try]").forEach((b) => b.addEventListener("click", () => { if (hasFinal) return; fin.value = S.fxTry = +b.dataset.try; saveAll(S); calc(); }));
      const fl = (() => { const t = total(tryF); return tryF < 75 || t < 750 ? "F" : letterOf(t)[0]; })();
      fin.disabled = hasFinal; fin.value = tryF;
      froot.querySelector("#fn-score").textContent = `${Math.round(tryF * 10) / 10}%`;
      const le = froot.querySelector("#fn-letter"); le.textContent = fl; le.style.color = LC[fl];
      const fill = froot.querySelector("#fn-fill"); fill.style.width = `${tryF}%`; fill.style.background = LC[fl];
      froot.querySelector(".fn-try").style.setProperty("--lc", LC[fl]);
    }
    calc();
  }

  // ---------------------------------------------------------------- coming up
  const today = new Date(); today.setHours(0, 0, 0, 0);
  const iso = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;
  const up = document.getElementById("upnext");
  if (up) {
    const next = D.due.filter((d) => new Date(d.date + "T00:00") >= today).slice(0, 5);
    up.innerHTML = next.length ? next.map((d, i) => {
      const days = Math.round((new Date(d.date + "T00:00") - today) / 864e5), [t, ...rest] = d.label.split(" · ");
      return `<div class="card up k-${d.kind} appear in" style="--d:${i * 0.06}s"><div class="up-days"><strong>${days === 0 ? "Today" : days === 1 ? "1" : days}</strong><span>${days === 0 ? "" : days === 1 ? "day" : "days"}</span></div>
        <div><div class="small muted">${new Date(d.date + "T00:00").toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" })}</div><div class="up-title">${t}</div>${rest.length ? `<div class="small muted">${rest.join(" · ")}</div>` : ""}</div></div>`;
    }).join("") : '<p class="muted">Nothing left — the course is done.</p>';
  }

  // ---------------------------------------------------------------- schedule: today marker, past weeks folded, filters
  const list = document.getElementById("sch-list");
  if (list) {
    const past = [...list.querySelectorAll(".sch-week")].filter((w) => w.dataset.end < iso);
    if (past.length) {
      const box = document.getElementById("sch-past");
      box.hidden = false;
      box.querySelector("summary").textContent = `Show ${past.length} past week${past.length > 1 ? "s" : ""}`;
      past.forEach((w) => document.getElementById("sch-past-list").append(w));
    }
    document.querySelectorAll(".sch-item").forEach((li) => {
      if (li.dataset.date < iso) li.classList.add("past");
      if (li.dataset.date === iso) li.classList.add("today");
    });
    document.querySelectorAll(".sch-week").forEach((w) => { if (w.dataset.week <= iso && iso <= w.dataset.end) w.classList.add("this-week"); });
    document.querySelectorAll(".sch-chip").forEach((b) => b.addEventListener("click", () => {
      document.querySelectorAll(".sch-chip").forEach((x) => x.classList.toggle("on", x === b));
      const f = b.dataset.filter;
      document.querySelectorAll(".sch-item").forEach((li) => li.classList.toggle("hide", f !== "all" && !(li.dataset.kind === f || (f === "exam" && li.dataset.kind === "final"))));
      document.querySelectorAll(".sch-week").forEach((w) => w.classList.toggle("hide", !w.querySelector(".sch-item:not(.hide)")));
    }));
  }
})();
