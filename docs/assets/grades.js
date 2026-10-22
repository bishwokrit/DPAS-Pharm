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
          <div class="gs-in gs-cp" style="--n:${D.bonus.count}">${Array.from({ length: D.bonus.count }, (_, i) => `<label title="Checkpoint ${i + 1}: ≥90%"><input type="checkbox" data-cp="${i}"><i>${i + 1}</i></label>`).join("")}</div></div></div>
      <div class="gs-chart">
        <div class="gs-sum"><div><div class="gs-big" id="pd-big">—</div><div class="gs-lbl">Projected grade</div></div><div class="gs-pct" id="pd-pct">—</div></div>
        <div class="gs-plot"><div class="gs-grid"><div class="gs-line base" style="bottom:0"><span>50</span></div>${ticks.map(([L, min]) => `<div class="gs-line" style="bottom:${(min / 10 - 50) * 2}%"><span>${L} ${min / 10}</span></div>`).join("")}</div>
          ${cats.map((it) => `<div class="gs-col" style="--c:var(--c-${it.key})"><div class="gs-bar" data-bar="${it.key}"><span class="gs-val" data-avg="${it.key}"></span></div></div>`).join("")}</div>
        <div class="gs-axis"><span>100</span><span>50</span></div><div class="gs-x">${cats.map((it) => `<span>${SHORT[it.key] || it.label}</span>`).join("")}</div>
        <div class="gs-foot"><span>Ungraded work at</span><div class="seg" id="assume">${ASSUME.map((v) => `<button data-v="${v}">${v}%</button>`).join("")}</div><button class="pc-clear" data-clear>Clear</button></div>
      </div></div>`;
    if (froot) froot.innerHTML = `<div class="fs">
      <div class="fs-top"><div><div class="fs-lbl">Final exam score</div><div class="fs-num" id="fn-score">—</div></div>
        <div class="fs-right"><div class="fs-lbl">Course grade</div><div class="fs-num"><span id="fn-letter">—</span><small id="fn-total"></small></div></div></div>
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
    // focusing a section highlights its column
    root.querySelectorAll(".gs-sec").forEach((sec, i) => {
      const on = (v) => { root.querySelectorAll(".gs-col").forEach((c, j) => c.classList.toggle("dim", v && j !== i)); };
      sec.addEventListener("mouseenter", () => on(i < cats.length)); sec.addEventListener("mouseleave", () => on(false));
    });

    const LC = { A: "var(--good)", B: "var(--accent)", C: "var(--warn)", F: "var(--bad)" };
    function calc() {
      const assume = S.assume ?? 85, finalScore = S.final?.[0], hasFinal = finalScore != null && finalScore !== "";
      root.querySelectorAll("#assume button").forEach((b) => b.classList.toggle("on", +b.dataset.v === assume));
      let projNoFinal = 0;
      for (const it of D.items) {
        let n = 0, sum = 0;
        for (let i = 0; i < it.count; i++) {
          const v = S[it.key]?.[i], has = v !== null && v !== undefined && v !== "";
          if (has) { n++; sum += v; }
          if (it.key !== "final") projNoFinal += ((has ? v : assume) / 100) * it.points_each;
        }
        const bar = root.querySelector(`[data-bar="${it.key}"]`);
        if (bar) {
          bar.style.height = `${Math.max(2, ((n ? sum / n : assume) - 50) * 2)}%`;  // axis runs 50–100% bar.classList.toggle("est", !n);
          bar.querySelector(".gs-val").textContent = n ? `${Math.round(sum / n)}` : "";
        }
      }
      const bonus = Math.min(D.bonus.max, (S.cp || []).filter(Boolean).length * D.bonus.points_each);
      root.querySelector("#bonus-pts").textContent = `+${+bonus.toFixed(2)}`;
      const total = (f) => Math.min(1000, projNoFinal + (f / 100) * final.points_each + bonus);
      const letter = (f) => (f < 75 || total(f) < 750 ? "F" : letterOf(total(f))[0]);
      const projF = hasFinal ? finalScore : assume, pl = letter(projF);
      const big = root.querySelector("#pd-big"); big.textContent = pl; big.style.color = LC[pl];
      root.querySelector("#pd-pct").textContent = `${trunc1(total(projF) / 10)}%`;

      if (!froot) return;
      const tryF = hasFinal ? finalScore : +fin.value, fl = letter(tryF);
      fin.disabled = hasFinal; fin.value = tryF;
      froot.querySelector("#fn-score").textContent = `${Math.round(tryF * 10) / 10}%`;
      const le = froot.querySelector("#fn-letter"); le.textContent = fl; le.style.color = LC[fl];
      froot.querySelector("#fn-total").textContent = `${trunc1(total(tryF) / 10)}%`;
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
