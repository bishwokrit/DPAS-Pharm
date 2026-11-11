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
  const trunc1 = (x) => (Math.floor(x * 10 + 1e-7) / 10).toFixed(1);  // the syllabus never rounds up (the tiny nudge only absorbs floating-point error: 799.99999… is 800)
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

  // ---------------------------------------------------------------- calculator: score panel (left) + column chart (right); final slider
  const root = document.getElementById("calcapp"), froot = document.getElementById("finalapp");
  if (root) {
    const ticks = D.scale.filter(([, min]) => min > 0), final = D.items.find((i) => i.key === "final");
    const cats = D.items.filter((it) => it.key !== "final"), ASSUME = [75, 80, 85, 90, 95];
    const SHORT = { exam: "Exams", quiz: "Quizzes", db: "Discussions", case: "Cases" };
    root.innerHTML = `<div class="gs">
      <div class="gs-panel">${cats.map((it) => `<div class="gs-sec" style="--c:var(--c-${it.key})">
          <div class="gs-h"><span class="gs-dot"></span>${it.label}<span>${it.weight}%</span></div>
          <div class="gs-in" style="--n:${it.count}">${Array.from({ length: it.count }, (_, i) => `<input type="number" inputmode="decimal" min="0" max="100" step="0.1" placeholder="${NAMES[it.key](i).replace(/^(\w+) (\d+)$/, (m, a, n) => (it.key === "db" ? "DB " : a.slice(0, 1) + "") + n)}" aria-label="${NAMES[it.key](i)} percent" data-k="${it.key}" data-i="${i}">`).join("")}</div></div>`).join("")}
        <div class="gs-sec" style="--c:var(--c-bonus)"><div class="gs-h"><span class="gs-dot"></span>Bonus checkpoints<span id="bonus-pts">+0</span></div>
          <div class="gs-in gs-cpin" style="--n:${D.bonus.count}">${Array.from({ length: D.bonus.count }, (_, i) => `<input type="number" inputmode="decimal" min="0" max="100" step="0.1" placeholder="CP${i + 1}" title="Checkpoint ${i + 1}: your highest score (≥90% earns ${D.bonus.points_each})" aria-label="Checkpoint ${i + 1} highest percent" data-cp="${i}">`).join("")}</div></div></div>
      <div class="gs-chart">
        <div class="gs-sum"><div><div class="gs-big" id="pd-big" aria-live="polite">—</div><div class="gs-lbl">Projected grade</div></div><div class="gs-pct" id="pd-pct">—</div></div>
        <div class="gs-math" id="pd-math"></div>
        <div class="gs-prog" id="pd-prog" aria-live="polite"></div>
        <div class="gs-plot"><div class="gs-grid"><div class="gs-line base" style="bottom:0"><span>50</span></div>${ticks.map(([L, min]) => `<div class="gs-line" style="bottom:${(min / 10 - 50) * 2}%"><span>${L} ${min / 10}</span></div>`).join("")}</div>
          ${cats.map((it) => `<div class="gs-col" style="--c:var(--c-${it.key})"><span class="gs-val" data-avg="${it.key}"></span><div class="gs-bar" data-bar="${it.key}"></div></div>`).join("")}</div>
        <div class="gs-axis"><span>100</span><span>50</span></div><div class="gs-x">${cats.map((it) => `<span>${SHORT[it.key] || it.label}</span>`).join("")}</div>
        <p class="gs-hint" id="gs-hint">Enter your first score on the left. Until then, the faded bars show the "ungraded work" setting below.</p>
        <div class="gs-foot"><span id="assume-lbl">Ungraded work at</span><div class="seg" id="assume">${ASSUME.map((v) => `<button data-v="${v}">${v}%</button>`).join("")}</div><button class="pc-clear" data-clear>Clear</button></div>
      </div></div>`;
    if (froot) froot.innerHTML = `<div class="fs">
      <div class="fs-top"><div><div class="fs-lbl">Final exam score</div><div class="fs-num" id="fn-score">—</div></div>
        <div class="fs-right"><div class="fs-lbl">Course grade</div><div class="fs-num"><span id="fn-letter" aria-live="polite">—</span><small id="fn-total"></small></div><div class="fs-verdict" id="fn-verdict"></div></div></div>
      <div class="fs-track"><div class="fs-fill" id="fn-fill"></div><div class="fs-marks" id="fn-marks"></div><input type="range" min="0" max="100" step="1" id="fn-in" aria-label="Final exam score"></div>
      <div class="fs-need" id="fn-need"></div>
      <div class="fs-bottom"><span>Drag to try a score. At least 75% is required to pass.</span><label>Actual score <input type="number" inputmode="decimal" min="0" max="100" step="0.1" placeholder="—" aria-label="Final exam percent" data-k="final" data-i="0"></label></div></div>`;

    const all = document.querySelectorAll("#calcapp input[data-k], #finalapp input[data-k]");
    all.forEach((inp) => {
      const v = S[inp.dataset.k]?.[inp.dataset.i];
      if (v !== undefined && v !== null && v !== "") inp.value = v;
      inp.addEventListener("input", () => {
        (S[inp.dataset.k] ||= [])[inp.dataset.i] = inp.value === "" ? null : Math.max(0, Math.min(100, +inp.value));
        saveAll(S); calc();
      });
    });
    // checkpoints: one box each for your highest score. Earlier saves (checked boxes, or two attempts) carry over.
    if (!S.cpb) {
      S.cpb = S.cps ? S.cps.map((r) => { const a = (r || []).filter((v) => v !== null && v !== undefined); return a.length ? Math.max(...a) : null; })
        : S.cp ? S.cp.map((on) => (on ? 90 : null)) : [];
      delete S.cps; delete S.cp; saveAll(S);
    }
    root.querySelectorAll("input[data-cp]").forEach((inp) => {
      const v = S.cpb[inp.dataset.cp];
      if (v !== undefined && v !== null) inp.value = v;
      inp.addEventListener("input", () => { S.cpb[inp.dataset.cp] = inp.value === "" ? null : Math.max(0, Math.min(100, +inp.value)); saveAll(S); calc(); });
    });
    root.querySelectorAll("#assume button").forEach((b) => b.addEventListener("click", () => { S.assume = S.assume === +b.dataset.v ? "avg" : +b.dataset.v; saveAll(S); calc(); }));
    const fin = froot?.querySelector("#fn-in");
    // while you drag, the page corners glow faintly in the grade's color
    const amb = document.createElement("div"); amb.className = "fs-ambient"; amb.setAttribute("aria-hidden", "true"); document.body.append(amb);
    let ambT = 0;
    const glow = () => { amb.style.setProperty("--lc", froot.querySelector(".fs")?.style.getPropertyValue("--lc") || "var(--accent)"); amb.classList.add("on"); clearTimeout(ambT); ambT = setTimeout(() => amb.classList.remove("on"), 1100); };
    if (fin) { fin.value = S.fxTry ?? 85; fin.addEventListener("input", () => { S.fxTry = +fin.value; saveAll(S); calc(); glow(); }); fin.addEventListener("pointerdown", glow); }
    root.querySelector("[data-clear]").addEventListener("click", () => {
      if (!confirm("Clear all scores?")) return;
      S = { assume: S.assume, fxTry: S.fxTry, cpb: [] }; saveAll(S);
      all.forEach((i) => (i.value = "")); root.querySelectorAll("input[data-cp]").forEach((c) => (c.value = ""));
      calc();
    });
    // focusing a section highlights its column
    root.querySelectorAll(".gs-sec").forEach((sec, i) => {
      const on = (v) => { root.querySelectorAll(".gs-col").forEach((c, j) => c.classList.toggle("dim", v && j !== i)); };
      sec.addEventListener("mouseenter", () => on(i < cats.length)); sec.addEventListener("mouseleave", () => on(false));
    });

    const LC = { A: "var(--good)", B: "var(--accent)", C: "var(--warn)", F: "var(--bad)" };
    function calc() {
      // no pill picked (tap the active one again) → ungraded work counts at your current average
      const entered = D.items.filter((it) => it.key !== "final").flatMap((it) => (S[it.key] || []).filter((v) => v !== null && v !== undefined && v !== ""));
      const useAvg = S.assume === "avg", avg = entered.length ? entered.reduce((a, b) => a + b, 0) / entered.length : 85;
      const assume = useAvg ? avg : S.assume ?? 85, finalScore = S.final?.[0], hasFinal = finalScore != null && finalScore !== "";
      root.querySelectorAll("#assume button").forEach((b) => { const on = !useAvg && +b.dataset.v === assume; b.classList.toggle("on", on); b.setAttribute("aria-pressed", on); });
      root.querySelector("#assume-lbl").textContent = useAvg ? `Ungraded work at your average (${Math.round(avg)}%)` : "Ungraded work at";
      let projNoFinal = 0;
      for (const it of D.items) {
        let n = 0, sum = 0;
        for (let i = 0; i < it.count; i++) {
          const v = S[it.key]?.[i], has = v !== null && v !== undefined && v !== "";
          if (has) { n++; sum += v; }
          if (it.key !== "final") projNoFinal += ((has ? v : assume) / 100) * ((it.weight * 10) / it.count);
        }
        const bar = root.querySelector(`[data-bar="${it.key}"]`);
        if (bar) {
          bar.style.height = `${Math.max(2, ((n ? sum / n : assume) - 50) * 2)}%`;  // axis runs 50–100%
          bar.classList.toggle("est", !n);
          bar.parentElement.querySelector(".gs-val").textContent = n ? `${Math.round(sum / n)}` : "—";
        }
      }
      // semester progress: how much of the course grade is already graded (by weight), and how much is still to come
      {
        const has = (v) => v !== null && v !== undefined && v !== "";
        const rows = D.items.map((it) => { const vs = Array.from({ length: it.count }, (_, i) => S[it.key]?.[i]).filter(has), each = (it.weight * 10) / it.count;
          return { it, n: vs.length, done: vs.length * each, got: vs.reduce((a, v) => a + (v / 100) * each, 0) }; });
        const done = rows.reduce((a, r) => a + r.done, 0), got = rows.reduce((a, r) => a + r.got, 0), pct = done / 10, left = 100 - pct;
        const f1 = (x) => (Math.round(x * 10) / 10).toString();
        root.querySelector("#pd-prog").innerHTML = done ? `<div class="gs-prog-h"><span><strong>${f1(pct)}%</strong> of the semester graded</span><span><strong>${f1(left)}%</strong> still to come</span></div>
          <div class="gs-prog-bar" role="img" aria-label="${f1(pct)} percent of the course grade is graded, ${f1(left)} percent is still to come">${rows.filter((r) => r.done).map((r) => `<i style="width:${r.done / 10}%;--c:var(--c-${r.it.key})" title="${r.it.label}: ${r.n} of ${r.it.count} graded"></i>`).join("")}</div>
          <div class="gs-prog-f">You have earned <strong>${f1(got)}</strong> of the ${f1(done)} points graded so far (${f1((got / done) * 100)}%). ${left > 0 ? `<strong>${f1(1000 - done)}</strong> points are still open: ${rows.filter((r) => r.n < r.it.count).map((r) => r.it.key === "final" ? "the final" : `${r.it.count - r.n} ${r.it.count - r.n === 1 ? (SHORT[r.it.key] || "final").replace(/(zes|s)$/, (m) => (m === "zes" ? "z" : "")).toLowerCase() : (SHORT[r.it.key] || "final").toLowerCase()}`).join(", ")}.` : "Everything is graded."}</div>`
          : `<div class="gs-prog-f">Enter a score and this shows how much of the semester is graded and how much is still to come.</div>`;
      }
      root.querySelector("#gs-hint").hidden = D.items.some((it) => (S[it.key] || []).some((v) => v !== null && v !== undefined && v !== ""));
      // a checkpoint earns its bonus when the better of its two attempts is at least 90%
      // syllabus: 3.75 points for each checkpoint scored ≥90% on either attempt; all 8 → 30 points (3%), capped at 30
      let earned = 0;
      root.querySelectorAll("input[data-cp]").forEach((inp) => {
        const v = S.cpb[inp.dataset.cp], has = v !== null && v !== undefined, ok = has && v >= 90;
        if (ok) earned++;
        inp.classList.toggle("ok", ok); inp.classList.toggle("miss", has && !ok);
      });
      const bonus = Math.min(D.bonus.max, earned * D.bonus.points_each);
      root.querySelector("#bonus-pts").textContent = `+${+bonus.toFixed(2)} (${earned}/${D.bonus.count} at ≥90%)`;
      const required = (f) => Math.round((projNoFinal + (f / 100) * final.points_each) * 1e6) / 1e6;  // drop floating-point noise before any cutoff
      const total = (f) => Math.min(1000, required(f) + bonus);
      const letter = (f) => (f < 75 || total(f) < 750 ? "F" : letterOf(total(f))[0]);
      const projF = hasFinal ? finalScore : assume, pl = letter(projF);
      const big = root.querySelector("#pd-big"); big.textContent = pl; big.style.color = LC[pl];
      root.querySelector("#pd-pct").textContent = `${trunc1(total(projF) / 10)}%`;
      const rq = required(projF), capped = rq + bonus > 1000;
      root.querySelector("#pd-math").textContent = `Required ${trunc1(rq)} + bonus ${bonus.toFixed(2).replace(/\.?0+$/, "")} = ${trunc1(Math.min(1000, rq + bonus))} / 1,000${capped ? " (capped)" : ""}`;

      if (!froot) return;
      const tryF = hasFinal ? finalScore : +fin.value, fl = letter(tryF);
      fin.disabled = hasFinal; fin.value = tryF;
      froot.querySelector("#fn-score").textContent = `${Math.round(tryF * 10) / 10}%`;
      // the whole card takes on the grade's color: glow, fill, knob; the letter springs when it changes
      const card = froot.querySelector(".fs"), le = froot.querySelector("#fn-letter");
      card.style.setProperty("--lc", LC[fl]); card.dataset.l = fl;
      if (le.textContent !== fl) {
        le.textContent = fl; le.style.color = LC[fl];
        if (!calm && le.dataset.seen) { le.classList.remove("pop", "shake"); void le.offsetWidth; le.classList.add(fl === "F" ? "shake" : "pop"); }
        le.dataset.seen = 1;
      }
      froot.querySelector("#fn-total").textContent = `${trunc1(total(tryF) / 10)}%`;
      froot.querySelector("#fn-verdict").textContent = fl === "F" ? (tryF < 75 ? "Below the 75% final minimum" : "Not passing") : (D.scale.find(([L]) => L === fl) || [])[2] || "";
      froot.querySelector("#fn-fill").style.width = `${tryF}%`;
      // marks on the track: the score needed for each letter (letters needing the same score share a mark)
      const need = {};
      ticks.forEach(([L, min]) => { const r = Math.max(75, Math.ceil(((min - projNoFinal - bonus) / final.points_each) * 100)); (need[r > 100 ? "out" : r] ||= []).push(L); });
      froot.querySelector("#fn-marks").innerHTML = Object.entries(need).filter(([k]) => k !== "out").map(([k, Ls]) => `<i style="left:${k}%" class="${tryF >= +k ? "hit" : ""}"></i>`).join("");
      froot.querySelector("#fn-need").innerHTML = ticks.map(([L]) => {
        const k = Object.keys(need).find((x) => need[x].includes(L));
        return `<span class="${k === "out" ? "out" : tryF >= +k ? "hit" : ""}"><b>${L}</b>${k === "out" ? "Out of reach" : `${k}%`}</span>`;
      }).join("");
    }
    calc();
  }

  // ---------------------------------------------------------------- coming up
  const today = new Date(); today.setHours(0, 0, 0, 0);
  const iso = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;
  const up = document.getElementById("upnext");
  if (up) {
    // redrawn every 30 s so a same-day countdown (hours, then minutes) stays live
    const T = window.dpasDue, paintUp = () => {
      const next = D.due.filter((d) => T.upcoming(d.date, d.label)).slice(0, 5);
      up.innerHTML = next.length ? next.map((d, i) => {
        const l = T.left(d.date, d.label), [t, ...rest] = d.label.split(" · "), tm = T.timeOf(d.label);
        return `<div class="card up k-${d.kind} appear in${l.soon ? " soon" : ""}" style="--d:${i * 0.06}s"><div class="up-days"><strong>${l.n}</strong><span>${l.unit}</span></div>
          <div><div class="small muted">${new Date(d.date + "T00:00").toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" })}${tm ? " · " + tm : ""}</div><div class="up-title">${t}</div>${rest.length ? `<div class="small muted">${rest.join(" · ")}</div>` : ""}</div></div>`;
      }).join("") : '<p class="muted">Nothing left — the course is done.</p>';
    };
    paintUp();
    setInterval(() => { if (!document.hidden) paintUp(); }, 30000);
  }

  // ---------------------------------------------------------------- schedule: one card per week; this week opens, past weeks dim; filters
  const list = document.getElementById("sch-list");
  if (list) {
    const weeks = [...list.querySelectorAll(".wk")];
    weeks.forEach((w) => {
      if (w.dataset.end < iso) w.classList.add("past");
      if (w.dataset.week <= iso && iso <= w.dataset.end) { w.classList.add("this-week"); w.open = true; }
    });
    if (!list.querySelector(".wk[open]")) (weeks.find((w) => w.dataset.week > iso) || weeks[0])?.setAttribute("open", "");
    list.querySelectorAll(".wk-day").forEach((d) => { if (d.dataset.date < iso) d.classList.add("past"); if (d.dataset.date === iso) d.classList.add("today"); });
    document.querySelectorAll(".sch-chip[data-filter]").forEach((b) => b.addEventListener("click", () => {
      document.querySelectorAll(".sch-chip[data-filter]").forEach((x) => x.classList.toggle("on", x === b));
      const f = b.dataset.filter, ok = (k) => f === "all" || k === f || (f === "exam" && k === "final");
      list.querySelectorAll("[data-kind]").forEach((el) => el.classList.toggle("hide", !ok(el.dataset.kind)));
      list.querySelectorAll(".wk-day").forEach((d) => d.classList.toggle("hide", !d.querySelector(".wk-items > :not(.hide)")));
      weeks.forEach((w) => w.classList.toggle("hide", f !== "all" && !w.querySelector(".wk-day:not(.hide)")));
    }));
  }
})();
