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

  // ---------------------------------------------------------------- calculator: a grade ruler, score bars you type into, a what-if slider for the final
  const root = document.getElementById("calcapp");
  if (root) {
    const ticks = D.scale.filter(([, min]) => min > 0), LO = 50;  // ruler shows 50–100%
    const at = (pct) => `${Math.max(0, Math.min(100, ((pct - LO) / (100 - LO)) * 100))}%`;
    const bands = D.scale.map(([L, min], i) => { const hi = i ? D.scale[i - 1][1] / 10 : 100, lo = Math.max(LO, min / 10); return `<span class="gr-band" style="left:${at(lo)};width:calc(${at(hi)} - ${at(lo)})"><b>${L}</b></span>`; }).join("");
    const final = D.items.find((i) => i.key === "final");
    root.innerHTML = `<div class="gr-head"><span class="gr-letter" id="proj-letter">—</span><span class="gr-pct" id="proj-num">—</span></div>
      <div class="gr"><div class="gr-track">${bands}</div><i class="gr-mark" id="mk-proj"></i><i class="gr-ghost" id="mk-cur" title="Graded so far"></i></div>
      <div class="gr-scale"><span>50%</span><span>100%</span></div>
      <div class="gr-key"><span><i class="gk-p"></i>Projected</span><span><i class="gk-c"></i>Graded so far <b id="cur-num"></b></span></div>
      <div class="sb">${D.items.filter((it) => it.key !== "final").map((it) => `
        <div class="sb-row"><div class="sb-name">${it.label}<span>${it.weight}%</span></div>
          <div class="sb-cells">${Array.from({ length: it.count }, (_, i) => `<label class="sb-cell" title="${NAMES[it.key](i)}"><input type="number" inputmode="decimal" min="0" max="100" step="0.1" aria-label="${NAMES[it.key](i)} percent" data-k="${it.key}" data-i="${i}"></label>`).join("")}</div></div>`).join("")}
        <div class="sb-row"><div class="sb-name">Bonus<span>+${D.bonus.max} max</span></div>
          <div class="sb-cells sb-cp">${Array.from({ length: D.bonus.count }, (_, i) => `<label title="Checkpoint ${i + 1}: ≥90%"><input type="checkbox" data-cp="${i}"><i></i></label>`).join("")}</div></div></div>
      <label class="sb-assume"><span>Assume <b id="as-v">85%</b> on work not yet graded</span><input type="range" min="50" max="100" step="1" data-assume></label>
      <div class="fx"><div class="fx-h"><h3>The final</h3><span class="muted small" id="fx-sub">${final.weight}% of your grade · 75% required to pass</span></div>
        <div class="fx-bar"><div class="fx-pins" id="fx-pins"></div><input type="range" min="0" max="100" step="1" id="fx-try" aria-label="Try a final exam score"><div class="fx-min" style="left:75%"></div></div>
        <div class="fx-scale"><span>0%</span><span style="left:75%">75%</span><span>100%</span></div>
        <div class="fx-foot"><div class="fx-out" id="fx-out"></div><label class="fx-real-l">Took it? <span class="sb-cell fx-real"><input type="number" inputmode="decimal" min="0" max="100" step="0.1" aria-label="Final exam percent" data-k="final" data-i="0"></span></label></div></div>
      <button class="btn ghost small gc-clear" data-clear>Clear all</button>`;

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
    const slider = root.querySelector("[data-assume]"), fx = root.querySelector("#fx-try");
    slider.value = S.assume ?? 85; fx.value = S.fxTry ?? 85;
    slider.addEventListener("input", () => { S.assume = +slider.value; saveAll(S); calc(); });
    fx.addEventListener("input", () => { S.fxTry = +fx.value; saveAll(S); calc(); });
    root.querySelector("[data-clear]").addEventListener("click", () => {
      if (!confirm("Clear all scores?")) return;
      S = { assume: S.assume }; saveAll(S);
      root.querySelectorAll("input[data-k]").forEach((i) => (i.value = "")); root.querySelectorAll("input[data-cp]").forEach((c) => (c.checked = false));
      calc();
    });

    function calc() {
      const assume = S.assume ?? 85, finalScore = S.final?.[0], hasFinal = finalScore != null && finalScore !== "";
      const tryF = hasFinal ? finalScore : +fx.value;
      root.querySelector("#as-v").textContent = assume + "%";
      let earned = 0, possible = 0, projNoFinal = 0;
      for (const it of D.items) for (let i = 0; i < it.count; i++) {
        const v = S[it.key]?.[i], has = v !== null && v !== undefined && v !== "";
        if (has) { earned += (v / 100) * it.points_each; possible += it.points_each; }
        if (it.key !== "final") projNoFinal += ((has ? v : assume) / 100) * it.points_each;
      }
      // each score cell fills to its score
      root.querySelectorAll(".sb-cells .sb-cell").forEach((c) => { const inp = c.querySelector("input"), has = inp.value !== "";
        c.classList.toggle("has", has); c.style.setProperty("--v", has ? Math.max(0, Math.min(100, +inp.value)) : 0); });
      const bonus = Math.min(D.bonus.max, (S.cp || []).filter(Boolean).length * D.bonus.points_each);
      const total = (f) => Math.min(1000, projNoFinal + (f / 100) * final.points_each + bonus);
      const projTotal = total(tryF), [pl] = letterOf(projTotal), cur = possible ? (100 * earned) / possible : null;
      root.querySelector("#proj-num").textContent = `${trunc1(projTotal / 10)}%`;
      const le = root.querySelector("#proj-letter"); le.textContent = pl; le.dataset.l = pl;
      root.querySelector("#mk-proj").style.left = at(projTotal / 10);
      const mc = root.querySelector("#mk-cur"); mc.hidden = cur === null; if (cur !== null) mc.style.left = at(cur);
      root.querySelector("#cur-num").textContent = cur === null ? "" : `${trunc1(cur)}%`;

      // the final: letter pins sit at the score you'd need; drag the slider to try a score
      fx.disabled = hasFinal; fx.value = tryF;
      const pins = {};  // letters needing the same score share one pin (e.g. "B C" at the 75% minimum)
      ticks.forEach(([L, min]) => { const req = Math.max(75, ((min - projNoFinal - bonus) / final.points_each) * 100), k = req > 100 ? "out" : trunc1(req); (pins[k] ||= []).push(L); });
      root.querySelector("#fx-pins").innerHTML = Object.entries(pins).map(([k, Ls]) => k === "out"
        ? `<span class="fx-pin out" style="left:100%" title="Out of reach">${Ls.join(" ")}</span>`
        : `<span class="fx-pin" style="left:${k}%" title="${Ls.join(", ")}: ${k}% on the final">${Ls.join(" ")}</span>`).join("");
      const pass = tryF >= 75 && projTotal >= 750;
      root.querySelector("#fx-out").innerHTML = `${hasFinal ? "Your final" : "If you score"} <b>${trunc1(tryF)}%</b> → <span class="fx-res" data-l="${pass ? pl : "F"}">${pass ? pl : "F"}</span>${tryF < 75 ? '<span class="muted small"> · below the 75% minimum</span>' : ""}`;
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
