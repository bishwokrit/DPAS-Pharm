// Quiz prep (Prepare page): the next in-class quiz, and a rehearsal in the same format as the real one
// (10 questions, 10 minutes, results at the end), drawn from that unit's self-tests and practice exams and weighted
// toward what you've missed or haven't seen. Rehearsal scores stay in this browser.
(function () {
  const host = document.getElementById("qp-app"), dataEl = document.getElementById("qp-data");
  if (!host || !dataEl) return;
  const D = JSON.parse(dataEl.textContent);
  const root = document.documentElement.dataset.root || "", v = document.documentElement.dataset.v || "";
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const store = {
    get(k, d) { try { const x = localStorage.getItem(k); return x === null ? d : JSON.parse(x); } catch { return d; } },
    set(k, x) { try { localStorage.setItem(k, JSON.stringify(x)); } catch { /* private mode */ } },
  };
  const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  const today = iso(new Date());
  const days = (s) => Math.round((new Date(s + "T00:00") - new Date(today + "T00:00")) / 864e5);
  const when = (s) => new Date(s + "T00:00").toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" });
  const N = 10, MIN = 10;  // the syllabus format: 10 questions, 10 minutes

  const quiz = D.quizzes.find((q) => q.date >= today) || D.quizzes[D.quizzes.length - 1];
  if (!quiz) return;
  const lecs = D.lectures.filter((l) => l.unit === quiz.unit), exams = D.exams.filter((e) => e.unit === quiz.unit);
  const logKey = `quizprep:${quiz.unit}`;

  async function bank() {
    const out = [];
    await Promise.all(lecs.map(async (l) => {
      const kb = await fetch(`${root}${l.id}/kb.json?v=${v}`).then((r) => r.json()).catch(() => null);
      kb?.quiz.forEach((q) => out.push({ ...q, id: `${l.id}:${q.id}`, raw: q.id, lid: l.id }));
    }));
    await Promise.all(exams.map(async (e) => {
      const qs = await fetch(`${root}exams/${e.slug}/quiz.json?v=${v}`).then((r) => r.json()).catch(() => []);
      qs.forEach((q) => out.push({ ...q, exam: e.slug }));
    }));
    return out;
  }
  // missed first, then never seen, then the rest; shuffled within each group so every rehearsal differs
  function pick(all) {
    const key = (q) => String(q.stem).replace(/<[^>]+>|\*\*/g, "").slice(0, 90);  // how the site's answer log names a question
    const seen = new Set(store.get("act:log", []).map((a) => a.k)), shuffle = (a) => a.sort(() => Math.random() - 0.5);
    const missed = all.filter((q) => q.lid && store.get(`miss:${q.lid}`, []).includes(q.raw));
    const fresh = all.filter((q) => !missed.includes(q) && !seen.has(key(q)));
    const rest = all.filter((q) => !missed.includes(q) && !fresh.includes(q));
    const qs = [...shuffle(missed).slice(0, 4), ...shuffle(fresh), ...shuffle(rest)];
    return [...new Map(qs.map((q) => [q.stem, q])).values()].slice(0, N);
  }

  function paint() {
    const d = days(quiz.date), log = store.get(logKey, []);
    const status = d > 1 ? `in ${d} days` : d === 1 ? "tomorrow" : d === 0 ? "today" : "done";
    const best = log.length ? Math.max(...log.map((r) => r.correct)) : null;
    host.innerHTML = `<div class="qp">
      <div class="qp-next card">
        <div class="qp-when"><strong>${d >= 0 ? d : "✓"}</strong><span>${d >= 0 ? (d === 1 ? "day" : "days") : "past"}</span></div>
        <div class="qp-info"><div class="tile-k">Next in-class quiz · ${esc(status)}</div><h3>${esc(quiz.label)}</h3>
          <p class="muted">${esc(when(quiz.date))}${quiz.time ? " · " + esc(quiz.time) : ""}</p>
          <div class="qp-chips"><span>${N} questions</span><span>${MIN} minutes</span><span>Lockdown Browser</span></div></div>
      </div>
      <div class="qp-go card">
        <div class="tile-k">Rehearsal</div><h3>Same format, from Unit ${quiz.unit}</h3>
        <p class="muted">${N} questions in ${MIN} minutes, results at the end. Leans toward questions you've missed or haven't seen yet.</p>
        <div class="qp-row"><button class="btn" data-go ${lecs.length || exams.length ? "" : "disabled"}>Start a rehearsal →</button>
          ${log.length ? `<span class="small muted">Last: <b>${log[0].correct}/${log[0].total}</b> · best ${best}/${N} · ${log.length} done</span>` : `<span class="small muted">${lecs.length || exams.length ? "Takes ten minutes." : "Questions appear once this unit's lectures are up."}</span>`}</div>
        ${log.length > 1 ? `<div class="qp-spark" aria-label="Your recent rehearsal scores">${log.slice(0, 8).reverse().map((r) => `<i style="--h:${Math.max(0.08, r.correct / r.total)}" title="${r.correct}/${r.total} · ${esc(r.date)}"></i>`).join("")}</div>` : ""}
      </div></div>`;
    host.querySelector("[data-go]").onclick = async () => {
      const qs = pick(await bank());
      if (!qs.length) return;
      window.dpasQuiz?.start(qs, {
        title: `${quiz.label} · rehearsal`, timed: true, feedback: "end", secondsPer: (MIN * 60) / qs.length,
        onAnswer: (q, L, ok) => { if (!q.lid) return; const m = new Set(store.get(`miss:${q.lid}`, [])); ok ? m.delete(q.raw) : m.add(q.raw); store.set(`miss:${q.lid}`, [...m]); },
        onFinish: (r) => { store.set(logKey, [{ correct: r.correct, total: r.total, date: today }, ...store.get(logKey, [])].slice(0, 20)); paint(); },
      });
    };
  }
  paint();
})();
