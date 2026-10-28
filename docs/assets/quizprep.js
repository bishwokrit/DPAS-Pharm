// Quiz prep (Prepare page): the next in-class quiz, and a rehearsal in the same format as the real one
// (10 questions, 4 options, 10 minutes, results at the end), drawn from that unit's self-tests and practice exams: mostly the
// lectures' quick checks and study-guide points, then what you've missed or haven't seen. Rehearsal scores stay in this browser.
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
  const when = (s) => new Date(s + "T00:00").toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" });
  const N = 10, MIN = 10;  // the syllabus format: 10 questions, 10 minutes

  const T = window.dpasDue;
  const quiz = D.quizzes.find((q) => T.upcoming(q.date, q.time)) || D.quizzes[D.quizzes.length - 1];
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
  // Built like the in-class quizzes: mostly the lecture's own quick checks, then study-guide points, then your misses and
  // what you haven't seen. Within each group: missed first, then never seen; shuffled so every rehearsal differs.
  const shuffle = (a) => a.sort(() => Math.random() - 0.5);
  function pick(all) {
    const key = (q) => String(q.stem).replace(/<[^>]+>|\*\*/g, "").slice(0, 90);  // how the site's answer log names a question
    const seen = new Set(store.get("act:log", []).map((a) => a.k));
    const missed = (q) => q.lid && store.get(`miss:${q.lid}`, []).includes(q.raw);
    const order = (qs) => [...shuffle(qs.filter(missed)), ...shuffle(qs.filter((q) => !missed(q) && !seen.has(key(q)))), ...shuffle(qs.filter((q) => !missed(q) && seen.has(key(q))))];
    const check = all.filter((q) => /^c\d/.test(q.raw || "")), sg = all.filter((q) => !check.includes(q) && /\bSG\b/.test(q.src || ""));
    const other = all.filter((q) => !check.includes(q) && !sg.includes(q));
    const qs = [...order(check).slice(0, 6), ...order(sg).slice(0, 3), ...order(other), ...order(check).slice(6), ...order(sg).slice(3)];
    return shuffle([...new Map(qs.map((q) => [q.stem, q])).values()].slice(0, N)).map(four);
  }
  // the in-class format has 4 options: keep the answer and three of the wrong ones, re-lettered A–D
  function four(q) {
    const ks = Object.keys(q.options || {});
    if (ks.length <= 4) return q;
    const wrong = shuffle(ks.filter((k) => k !== q.answer)).slice(0, 3), keep = ks.filter((k) => k === q.answer || wrong.includes(k));
    const to = Object.fromEntries(keep.map((k, i) => [k, "ABCD"[i]]));
    const re = (o) => o && Object.fromEntries(Object.entries(o).filter(([k]) => to[k]).map(([k, v]) => [to[k], v]));
    return { ...q, options: re(q.options), answer: to[q.answer], whys: re(q.whys) };
  }

  function paint() {
    const l = T.left(quiz.date, quiz.time), log = store.get(logKey, []);
    const status = l.past ? "done" : l.text;
    const best = log.length ? Math.max(...log.map((r) => r.correct)) : null;
    host.innerHTML = `<div class="qp">
      <div class="qp-next card">
        <div class="qp-when"><strong>${l.n}</strong><span>${l.unit}</span></div>
        <div class="qp-info"><div class="tile-k">Next in-class quiz · ${esc(status)}</div><h3>${esc(quiz.label)}</h3>
          <p class="muted">${esc(when(quiz.date))}${quiz.time ? " · " + esc(quiz.time) : ""}</p>
          <div class="qp-chips"><span>${N} questions</span><span>${MIN} minutes</span><span>Lockdown Browser</span></div></div>
      </div>
      <div class="qp-go card">
        <div class="tile-k">Rehearsal</div><h3>Same format, from Unit ${quiz.unit}</h3>
        <p class="muted">${N} questions, 4 options each, ${MIN} minutes, results at the end. Built like the in-class quizzes: mostly the lectures' own quick checks and study-guide points, then what you've missed or haven't seen.</p>
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
  // keep a same-day countdown live (hours, then minutes); skip while a rehearsal is open
  setInterval(() => { if (!document.hidden && !document.querySelector(".qm") && T.left(quiz.date, quiz.time).soon) paint(); }, 30000);
})();
