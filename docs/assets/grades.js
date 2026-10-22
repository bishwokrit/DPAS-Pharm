// Syllabus page: interactive grade breakdown (donut), a live 100-square grade grid + calculator,
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

  // ---------------------------------------------------------------- calculator + live grade grid
  const root = document.getElementById("calcapp");
  if (root) {
    root.innerHTML = `<div class="calc-grid"><div class="calc-inputs">${D.items.map((it) => `
        <div class="calc-group" style="--c:var(--c-${it.key})"><div class="calc-head"><span class="cg-dot"></span><strong>${it.label}</strong><span class="cg-avg" data-avg="${it.key}">—</span><span class="muted small">${it.weight}%</span></div>
        <div class="calc-row">${Array.from({ length: it.count }, (_, i) => `<label class="cin"><span>${NAMES[it.key](i)}</span><input type="number" inputmode="decimal" min="0" max="100" step="0.1" placeholder="—" data-k="${it.key}" data-i="${i}"><i class="cin-bar"></i></label>`).join("")}</div></div>`).join("")}
        <div class="calc-group" style="--c:var(--c-bonus)"><div class="calc-head"><span class="cg-dot"></span><strong>Bonus checkpoints</strong><span class="muted small">≥90% on either attempt · +${D.bonus.points_each} each</span></div>
        <div class="calc-row cp">${Array.from({ length: D.bonus.count }, (_, i) => `<label class="cpbox"><input type="checkbox" data-cp="${i}"><span>CP ${i + 1}</span></label>`).join("")}</div></div>
        <button class="btn ghost small" data-clear>Clear all</button></div>
      <div class="calc-out">
        <div class="calc-card gg-card"><div class="gg-head"><div><div class="small muted">Projected final grade</div><div class="gg-big"><span id="proj-num">0.0</span>%<span class="gg-letter" id="proj-letter">—</span></div></div>
          <div class="gg-cur"><div class="small muted">Graded so far</div><div><strong id="cur-num">—</strong></div></div></div>
          <div class="gg" id="gg" aria-label="Each square is 1% of your grade"></div>
          <div class="gg-key"><span><i class="k-earned"></i>Earned</span><span><i class="k-lost"></i>Lost</span><span><i class="k-proj"></i>Projected</span><span><i class="k-bonus"></i>Bonus</span></div>
          <div class="track"><div class="track-zones"><span style="left:75%"></span><span style="left:80%"></span><span style="left:90%"></span></div>
            <div class="track-lbl"><b style="left:75%">C</b><b style="left:80%">B</b><b style="left:90%">A</b></div>
            <div class="track-mark cur" id="mk-cur" title="Graded so far"></div><div class="track-mark proj" id="mk-proj" title="Projected"></div></div>
          <label class="calc-assume">If I average <strong id="as-v">85%</strong> on everything left<input type="range" min="50" max="100" step="1" data-assume></label></div>
        <div class="calc-card"><div class="small muted" id="need-h">What you need on the final</div><div id="need"></div></div>
      </div></div>`;

    // 100 squares: one per 1% of the grade, grouped by category in syllabus order (+ up to 3 bonus squares)
    const gg = root.querySelector("#gg"), cells = [];
    D.items.forEach((it) => { for (let i = 0; i < it.weight; i++) cells.push(it.key); });
    gg.innerHTML = cells.map((k, i) => `<i data-k="${k}" style="--c:var(--c-${k});--i:${i}"></i>`).join("") +
      `<span class="gg-plus">+</span>` + [0, 1, 2].map((i) => `<i class="b" style="--c:var(--c-bonus);--i:${100 + i}"></i>`).join("");
    const sq = [...gg.querySelectorAll("i:not(.b)")], bsq = [...gg.querySelectorAll("i.b")];

    root.querySelectorAll("input[data-k]").forEach((inp) => {
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
    const slider = root.querySelector("[data-assume]");
    slider.value = S.assume ?? 85;
    slider.addEventListener("input", () => { S.assume = +slider.value; saveAll(S); calc(); });
    root.querySelector("[data-clear]").addEventListener("click", () => {
      if (!confirm("Clear all scores?")) return;
      S = { assume: S.assume }; saveAll(S);
      root.querySelectorAll("input[data-k]").forEach((i) => (i.value = "")); root.querySelectorAll("input[data-cp]").forEach((c) => (c.checked = false));
      calc();
    });

    // smooth number tweening
    const tweens = new Map();
    const tween = (el, to, fmt) => {
      const from = +(el.dataset.v ?? to); el.dataset.v = to;
      if (calm || from === to) { el.textContent = fmt(to); return; }
      cancelAnimationFrame(tweens.get(el));
      const t0 = performance.now(), dur = 550;
      const step = (t) => { const k = Math.min(1, (t - t0) / dur), e = 1 - Math.pow(1 - k, 3); el.textContent = fmt(from + (to - from) * e); if (k < 1) tweens.set(el, requestAnimationFrame(step)); };
      tweens.set(el, requestAnimationFrame(step));
    };
    const LCOL = { A: "var(--good)", B: "var(--accent)", C: "var(--warn)", F: "var(--bad)" };

    function calc() {
      const assume = S.assume ?? 85;
      root.querySelector("#as-v").textContent = assume + "%";
      let earned = 0, possible = 0, projNoFinal = 0, projected = 0;
      const final = D.items.find((i) => i.key === "final");
      // per-category points: earned / lost (graded) and projected earned / lost (ungraded at the slider value)
      const cat = {};
      for (const it of D.items) {
        const c = (cat[it.key] = { e: 0, l: 0, pe: 0, pl: 0, n: 0, sum: 0 });
        for (let i = 0; i < it.count; i++) {
          const v = S[it.key]?.[i], has = v !== null && v !== undefined && v !== "";
          if (has) { c.e += (v / 100) * it.points_each; c.l += (1 - v / 100) * it.points_each; c.n++; c.sum += v; earned += (v / 100) * it.points_each; possible += it.points_each; }
          else { c.pe += (assume / 100) * it.points_each; c.pl += (1 - assume / 100) * it.points_each; }
          if (it.key !== "final") projNoFinal += ((has ? v : assume) / 100) * it.points_each;
          projected += ((has ? v : assume) / 100) * it.points_each;
        }
        const avg = root.querySelector(`[data-avg="${it.key}"]`);
        avg.textContent = c.n ? `${trunc1(c.sum / c.n)}% avg` : "—";
        avg.classList.toggle("has", !!c.n);
      }
      // inputs: little fill bar under each score
      root.querySelectorAll("label.cin").forEach((l) => { const v = +l.querySelector("input").value; l.style.setProperty("--v", l.querySelector("input").value === "" ? 0 : Math.max(0, Math.min(100, v))); });

      // paint the grid: within each category, earned → lost → projected-earned → (projected-lost stays empty)
      let idx = 0;
      for (const it of D.items) {
        const c = cat[it.key], per = 10;  // 1 square = 10 points
        let e = Math.round(c.e / per), l = Math.round((c.e + c.l) / per) - e, pe = Math.round((c.e + c.l + c.pe) / per) - e - l;
        for (let i = 0; i < it.weight; i++, idx++) {
          const st = i < e ? "earned" : i < e + l ? "lost" : i < e + l + pe ? "proj" : "";
          if (sq[idx].dataset.s !== st) { sq[idx].dataset.s = st; sq[idx].style.setProperty("--dl", `${(i % 20) * 12}ms`); }
        }
      }
      const bonus = Math.min(D.bonus.max, (S.cp || []).filter(Boolean).length * D.bonus.points_each);
      bsq.forEach((b, i) => (b.dataset.s = bonus >= (i + 1) * 10 - 0.01 ? "earned" : bonus > i * 10 ? "half" : ""));

      const projTotal = Math.min(1000, projected + bonus), [pl] = letterOf(projTotal);
      const cur = possible ? (100 * earned) / possible : null;
      tween(root.querySelector("#proj-num"), projTotal / 10, (x) => trunc1(x));
      const le = root.querySelector("#proj-letter");
      if (le.textContent !== pl) { le.textContent = pl; le.style.background = LCOL[pl]; le.classList.remove("pop"); void le.offsetWidth; le.classList.add("pop"); }
      root.querySelector("#cur-num").textContent = cur === null ? "—" : `${trunc1(cur)}% ${letterOf(cur * 10)[0]}`;
      const pos = (pct) => `${Math.max(0, Math.min(100, (pct - 50) * 2))}%`;  // track shows 50–100%
      root.querySelector("#mk-proj").style.left = pos(projTotal / 10);
      root.querySelector("#mk-proj").style.background = LCOL[pl];
      const mc = root.querySelector("#mk-cur");
      mc.hidden = cur === null; if (cur !== null) mc.style.left = pos(cur);

      // what you need on the final, as three mini gauges
      const finalScore = S.final?.[0], need = root.querySelector("#need");
      if (finalScore != null && finalScore !== "") {
        root.querySelector("#need-h").textContent = "Final exam";
        need.innerHTML = `<p class="small">${finalScore >= 75 ? "✓ At least 75% on the final — passing requirement met." : "⚠ Below 75% on the final means not passing the course, whatever the total."}</p>`;
        return;
      }
      root.querySelector("#need-h").textContent = "What you need on the final";
      need.innerHTML = D.scale.filter(([, min]) => min > 0).map(([L, min]) => {
        const req = Math.max(((min - projNoFinal - bonus) / final.points_each) * 100, 75), out = req > 100;
        return `<div class="need-row"><span class="gg-letter" style="background:${LCOL[L]}">${L}</span><div class="need-bar"><i style="width:${out ? 100 : req}%;background:${out ? "var(--hair)" : LCOL[L]}"></i></div>
          <strong>${out ? "—" : trunc1(req) + "%"}</strong></div><div class="need-sub small muted">${out ? "Out of reach with these assumptions" : req === 75 ? "The 75% minimum" : "on the final"}</div>`;
      }).join("") + '<p class="small muted" style="margin-top:8px">Assumes your other remaining work matches the slider. ≥75% on the final is required to pass.</p>';
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
