// Grade calculator for the syllabus page. Weights and rules come from the syllabus (grade-data JSON).
// Scores are saved only in this browser.
(function () {
  const root = document.getElementById("calcapp"), D = JSON.parse(document.getElementById("grade-data")?.textContent || "null");
  if (!root || !D) return;
  const KEY = "grades:v1";
  const load = () => { try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch { return {}; } };
  const saveAll = (v) => { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch { /* private mode */ } };
  let S = load();
  const NAMES = { exam: (i) => `Unit ${i + 1} exam`, final: () => "Final", quiz: (i) => `Quiz ${i + 1}`, db: (i) => `DB ${i + 1}`, case: (i) => `Case ${i + 1}` };
  const letter = (pts) => (D.scale.find(([, min]) => pts >= min) || D.scale[D.scale.length - 1]);
  const fmt = (x) => (Math.floor(x * 10) / 10).toFixed(1);  // the syllabus never rounds up

  root.innerHTML = `<div class="calc-grid"><div class="calc-inputs">${D.items.map((it) => `
      <div class="calc-group"><div class="calc-head"><strong>${it.label}</strong><span class="muted small">${it.weight}% · ${+it.points_each.toFixed(2)} pts each</span></div>
      <div class="calc-row">${Array.from({ length: it.count }, (_, i) => `<label><span>${NAMES[it.key](i)}</span><input type="number" inputmode="decimal" min="0" max="100" step="0.1" placeholder="—" data-k="${it.key}" data-i="${i}"></label>`).join("")}</div></div>`).join("")}
      <div class="calc-group"><div class="calc-head"><strong>Bonus checkpoints</strong><span class="muted small">≥90% on either attempt · +${D.bonus.points_each} pts each, max ${D.bonus.max}</span></div>
      <div class="calc-row cp">${Array.from({ length: D.bonus.count }, (_, i) => `<label class="cpbox"><input type="checkbox" data-cp="${i}"><span>CP ${i + 1}</span></label>`).join("")}</div></div>
      <button class="btn ghost small" data-clear>Clear all</button></div>
    <div class="calc-out" id="calcout"></div></div>`;

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
  root.querySelector("[data-clear]").addEventListener("click", () => { if (confirm("Clear all scores?")) { S = { assume: S.assume }; saveAll(S); location.reload(); } });

  function calc() {
    const assume = S.assume ?? 85;
    let earned = 0, possible = 0, projected = 0, projNoFinal = 0;
    const final = D.items.find((i) => i.key === "final");
    for (const it of D.items) for (let i = 0; i < it.count; i++) {
      const v = S[it.key]?.[i], has = v !== null && v !== undefined && v !== "";
      if (has) { earned += (v / 100) * it.points_each; possible += it.points_each; }
      projected += ((has ? v : assume) / 100) * it.points_each;
      if (it.key !== "final") projNoFinal += ((has ? v : assume) / 100) * it.points_each;
    }
    const bonus = Math.min(D.bonus.max, (S.cp || []).filter(Boolean).length * D.bonus.points_each);
    const cur = possible ? (100 * earned) / possible : null;
    const projTotal = Math.min(1000, projected + bonus), [pl, , pst] = letter(projTotal);
    const finalScore = S.final?.[0];
    const need = D.scale.filter(([, min]) => min > 0).map(([L, min]) => {
      const pct = ((min - projNoFinal - bonus) / final.points_each) * 100;
      const req = Math.max(pct, 75);  // must also score ≥75% on the final to pass
      return { L, min, req, impossible: req > 100 };
    });
    const out = document.getElementById("calcout");
    out.innerHTML = `
      <div class="calc-card"><div class="small muted">Current grade (graded work only)</div>
        <div class="calc-big">${cur === null ? "—" : fmt(cur) + "%"}</div>
        <div class="small">${cur === null ? "Enter a score to start." : `${letter(cur * 10)[0]} so far · ${fmt(earned)} of ${fmt(possible)} points graded`}${bonus ? ` · +${bonus} bonus` : ""}</div></div>
      <div class="calc-card"><div class="small muted">Projected final grade</div>
        <label class="calc-assume">If I average <strong>${assume}%</strong> on everything left<input type="range" min="50" max="100" value="${assume}" data-assume></label>
        <div class="calc-big ${projTotal >= 750 ? "" : "bad"}">${fmt(projTotal / 10)}% <span class="calc-letter">${pl}</span></div>
        <div class="small">${fmt(projTotal)} / 1,000 points · ${pst}</div></div>
      <div class="calc-card"><div class="small muted">${finalScore != null ? "Final already entered" : "What you need on the final"}</div>
        ${finalScore != null ? `<div class="small">${finalScore >= 75 ? "✓ Final is at least 75% — passing requirement met." : "⚠ Below 75% on the final means not passing the course, whatever the total."}</div>` :
          need.map((n) => `<div class="calc-need"><span class="calc-letter">${n.L}</span>${n.impossible ? '<span class="muted">Out of reach with these assumptions</span>' : `<strong>${fmt(n.req)}%</strong>${n.req === 75 ? '<span class="muted small"> (the 75% minimum)</span>' : ""}`}</div>`).join("") +
          '<div class="small muted" style="margin-top:6px">Assumes your other remaining work matches the slider above. You need ≥75% on the final to pass no matter what.</div>'}</div>`;
    out.querySelector("[data-assume]")?.addEventListener("input", (e) => { S.assume = +e.target.value; saveAll(S); calc(); });
  }
  calc();

  // "Coming up": the next deadlines with a countdown
  const up = document.getElementById("upnext");
  if (up) {
    const today = new Date(); today.setHours(0, 0, 0, 0);
    const next = D.due.filter((d) => new Date(d.date + "T00:00") >= today).slice(0, 6);
    up.innerHTML = next.length ? next.map((d) => {
      const days = Math.round((new Date(d.date + "T00:00") - today) / 864e5);
      return `<div class="card up k-${d.kind}"><div class="up-days"><strong>${days === 0 ? "Today" : days === 1 ? "Tomorrow" : days}</strong>${days > 1 ? "<span>days</span>" : ""}</div>
        <div><div class="small muted">${new Date(d.date + "T00:00").toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" })}</div><div>${d.label}</div></div></div>`;
    }).join("") : '<p class="muted">Nothing left — the course is done.</p>';
    const iso = `${today.getFullYear()}-${String(today.getMonth() + 1).padStart(2, "0")}-${String(today.getDate()).padStart(2, "0")}`;
    document.querySelectorAll(".sched tr[data-date]").forEach((tr) => {
      if (tr.dataset.date < iso) tr.classList.add("past");
      if (tr.dataset.date === iso) tr.classList.add("today");
    });
    const nextRow = [...document.querySelectorAll(".sched tr[data-date]")].find((tr) => tr.dataset.date >= iso);
    nextRow?.classList.add("upcoming");
  }
})();
