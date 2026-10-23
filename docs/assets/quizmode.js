// Focus quiz mode: one full-screen question at a time, nothing else on screen.
// Shared by study-guide self-tests, Sidekick quizzes, and practice exams (window.dpasQuiz.start).
// Works with keyboards and Bluetooth page-turner / "Anki remote" rings:
//   ↑ ↓ (or PageUp/PageDown, W/S, mouse wheel) move the highlight · Enter / Space / click lock it in
//   → / Enter / Space go to the next question · ← goes back · A–E or 1–5 answer directly · F flag · Esc exit
// Ends with a debrief: score, time, by-topic breakdown, every miss with a link to study it, and suggestions.
(function () {
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const md = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  const fmt = (s) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;
  const L5 = "ABCDE";

  // q: {id, stem, options:{A:text,...}, answer, why, whys?:{L:why}, takeaway?, discriminator?, src?, topic?, kind?, link?:{href,label}}
  // opts: {title, timed:false, secondsPer:60, feedback:"each"|"end", onAnswer(q, letter, ok, secs), onFinish(result), onExit()}
  function start(questions, opts = {}) {
    if (!questions.length) return;
    const feedback = opts.feedback || (opts.timed ? "end" : "each");
    const st = { i: 0, hi: 0, chosen: {}, secs: {}, flags: new Set(), t0: Date.now(), qStart: Date.now(), done: false };
    const total = opts.timed ? questions.length * (opts.secondsPer || 60) : 0;
    const prevOverflow = document.documentElement.style.overflow;
    document.documentElement.style.overflow = "hidden";
    const el = document.createElement("div");
    el.className = "qm";
    el.setAttribute("role", "dialog");
    el.setAttribute("aria-label", opts.title || "Quiz");
    document.body.append(el);
    el.requestFullscreen?.().catch(() => {});
    let timer = null;
    if (opts.timed) timer = setInterval(tick, 1000);

    function elapsed() { return (Date.now() - st.t0) / 1000; }
    function tick() {
      const left = total - elapsed(), t = el.querySelector(".qm-time");
      if (t) {
        t.textContent = fmt(Math.max(0, left));
        const pace = (st.i + 1) * (opts.secondsPer || 60) - elapsed();  // ahead (+) or behind (−) pace for this question
        t.classList.toggle("warn", left < 300 || pace < 0);
      }
      if (left <= 0) finish(true);
    }
    function q() { return questions[st.i]; }
    function answered(x) { return st.chosen[x.id] !== undefined; }
    function reveal(x) { return answered(x) && (feedback === "each" || st.done); }

    function draw() {
      const x = q(), letters = Object.keys(x.options), ch = st.chosen[x.id], show = reveal(x);
      const dots = questions.map((y, k) => `<span class="${k === st.i ? "cur" : ""} ${answered(y) ? (feedback === "each" ? (st.chosen[y.id] === y.answer ? "ok" : "no") : "ans") : ""} ${st.flags.has(y.id) ? "flag" : ""}"></span>`).join("");
      el.innerHTML = `
        <div class="qm-top"><button class="qm-x" data-exit aria-label="Exit">✕</button>
          <div class="qm-count">${st.i + 1} <span>/ ${questions.length}</span></div>
          ${opts.timed ? `<div class="qm-time" title="Time left">${fmt(Math.max(0, total - elapsed()))}</div>` : `<div class="qm-title">${esc(opts.title || "")}</div>`}
          <button class="qm-flag ${st.flags.has(x.id) ? "on" : ""}" data-flag title="Flag (F)">⚑</button></div>
        <div class="qm-dots">${dots}</div>
        <div class="qm-scroll"><div class="qm-card">
          <div class="qm-meta">${x.topic ? `<span class="chip">${md(x.topic)}</span>` : ""}${x.kind ? `<span class="chip ${x.kind === "vignette" ? "warn" : ""}">${x.kind === "vignette" ? "Patient case" : "Recall"}</span>` : ""}</div>
          <div class="qm-stem">${md(x.stem)}</div>
          <div class="qm-opts">${letters.map((L, k) => {
            let c = "qm-opt";
            if (show) c += L === x.answer ? " right" : L === ch ? " wrong" : " dim";
            else if (ch === L) c += " picked";
            if (!show && k === st.hi) c += " hi";
            return `<button class="${c}" data-l="${L}"><span class="L">${L}</span><span>${md(x.options[L])}</span></button>`;
          }).join("")}</div>
          ${show ? explain(x, ch) : ""}
        </div></div>
        <div class="qm-bottom"><button class="qm-nav" data-prev ${st.i === 0 ? "disabled" : ""}>←</button>
          <div class="qm-hint">${show || (ch && feedback === "end") ? "<kbd>Enter</kbd> / <kbd>→</kbd> next" : "<kbd>↑</kbd><kbd>↓</kbd> choose · <kbd>Enter</kbd> lock in · or <kbd>A</kbd>–<kbd>E</kbd>"}</div>
          <button class="qm-nav primary" data-next>${st.i === questions.length - 1 ? (st.done ? "Debrief" : "Finish") : "→"}</button></div>`;
      el.querySelectorAll("[data-l]").forEach((b) => b.addEventListener("click", () => pick(b.dataset.l)));
      el.querySelector("[data-exit]").addEventListener("click", exit);
      el.querySelector("[data-flag]").addEventListener("click", flag);
      el.querySelector("[data-prev]").addEventListener("click", () => move(-1));
      el.querySelector("[data-next]").addEventListener("click", () => move(1));
      el.querySelectorAll("[data-jump]").forEach((a) => a.addEventListener("click", () => exit(true)));
      el.querySelector(".qm-opt.hi")?.scrollIntoView({ block: "nearest" });
    }
    function explain(x, ch) {
      const ok = ch === x.answer;
      const whys = x.whys ? Object.entries(x.whys).filter(([L]) => L !== x.answer).map(([L, w]) => `<li><strong>${L}.</strong> ${md(w)}</li>`).join("") : "";
      return `<div class="qm-res ${ok ? "ok" : "no"}">${ok ? "Correct" : ch ? `Not quite — the answer is ${x.answer}` : `Unanswered — the answer is ${x.answer}`}</div>
        <div class="callout clin"><div class="label">Why ${x.answer}</div>${md(x.why)}${x.src ? ` <span class="cite">${esc(x.src)}</span>` : ""}${whys ? `<ul class="why-list">${whys}</ul>` : ""}</div>
        ${x.takeaway ? `<div class="callout hy"><div class="label">High-yield takeaway</div>${md(x.takeaway)}</div>` : ""}
        ${x.discriminator ? `<div class="callout why"><div class="label">How to tell it apart</div>${md(x.discriminator)}</div>` : ""}
        ${x.link ? `<a class="jump" data-jump href="${esc(x.link.href)}">${esc(x.link.label)}</a>` : ""}`;
    }
    function pick(L) {
      const x = q();
      if (st.done || (answered(x) && feedback === "each")) return;
      st.chosen[x.id] = L;
      st.secs[x.id] = (st.secs[x.id] || 0) + (Date.now() - st.qStart) / 1000;
      st.qStart = Date.now();
      if (feedback === "each") opts.onAnswer?.(x, L, L === x.answer, st.secs[x.id]);  // timed mode reports at the end (answers can change)
      st.hi = Object.keys(x.options).indexOf(L);
      if (feedback === "end" && st.i < questions.length - 1) { move(1); return; }
      draw();
    }
    function move(d) {
      if (d > 0 && st.i === questions.length - 1) { st.done ? debrief() : finish(false); return; }
      st.i = Math.max(0, Math.min(questions.length - 1, st.i + d));
      st.hi = Math.max(0, Object.keys(q().options).indexOf(st.chosen[q().id]));
      st.qStart = Date.now();
      draw();
      el.querySelector(".qm-scroll").scrollTop = 0;
    }
    function flag() { const id = q().id; st.flags.has(id) ? st.flags.delete(id) : st.flags.add(id); draw(); }
    function finish(timeUp) {
      if (!st.done) {
        const left = questions.filter((x) => !answered(x)).length;
        if (!timeUp && left && !confirm(`${left} question${left > 1 ? "s" : ""} unanswered. Finish anyway?`)) return;
        st.done = true;
        st.time = Math.min(elapsed(), total || Infinity);
        clearInterval(timer);
        if (feedback === "end") questions.forEach((x) => { if (answered(x)) opts.onAnswer?.(x, st.chosen[x.id], st.chosen[x.id] === x.answer, st.secs[x.id] || 0); });
        opts.onFinish?.(result());
      }
      debrief(timeUp);
    }
    function result() {
      const rows = questions.map((x) => ({ q: x, chose: st.chosen[x.id], ok: st.chosen[x.id] === x.answer, secs: st.secs[x.id] || 0 }));
      return { rows, correct: rows.filter((r) => r.ok).length, total: rows.length, time: st.time ?? elapsed(), flags: [...st.flags] };
    }

    function debrief(timeUp) {
      const r = result(), pct = Math.round((100 * r.correct) / r.total);
      const topics = {};
      r.rows.forEach((x) => { const t = x.q.topic || "General"; (topics[t] ||= { n: 0, ok: 0, link: x.q.link }).n++; if (x.ok) topics[t].ok++; });
      const trows = Object.entries(topics).map(([t, v]) => ({ t, ...v, pct: Math.round((100 * v.ok) / v.n) })).sort((a, b) => a.pct - b.pct);
      const misses = r.rows.filter((x) => !x.ok);
      const answeredRows = r.rows.filter((x) => x.chose);
      const avg = answeredRows.length ? answeredRows.reduce((s, x) => s + x.secs, 0) / answeredRows.length : 0;
      const fastWrong = misses.filter((x) => x.chose && x.secs < 20).length;
      const slowRight = r.rows.filter((x) => x.ok && x.secs > 120).length;
      const byKind = (k) => { const xs = r.rows.filter((x) => x.q.kind === k); return xs.length ? Math.round((100 * xs.filter((x) => x.ok).length) / xs.length) : null; };
      const vig = byKind("vignette"), rec = byKind("mechanism");
      const tips = [];
      trows.filter((t) => t.pct < 70).slice(0, 3).forEach((t) => tips.push(`<strong>${md(t.t)}</strong> is your weakest area (${t.ok}/${t.n}). ${t.link ? `<a href="${esc(t.link.href)}" data-jump>Re-read it →</a>` : "Re-read that part of the guide,"} then retry your misses.`));
      if (fastWrong >= 2) tips.push(`${fastWrong} misses took under 20 seconds — you may be rushing. Read the last line of the stem first, then predict the answer before looking at options.`);
      if (avg > 75) tips.push(`You averaged ${Math.round(avg)} s per question; the PANCE allows about 64 s. Practice timed mode to build pace.`);
      if (slowRight >= 2) tips.push(`${slowRight} correct answers took over 2 minutes — you know it, but not automatically yet. Drill those topics with flashcards.`);
      if (vig !== null && rec !== null && Math.abs(vig - rec) >= 15) tips.push(vig < rec ? `Patient cases (${vig}%) lag recall questions (${rec}%): practice turning each fact into "what would this look like in a patient?".` : `Recall questions (${rec}%) lag patient cases (${vig}%): drill the cram sheet for exact definitions and numbers.`);
      if (r.flags.length) tips.push(`You flagged ${r.flags.length} question${r.flags.length > 1 ? "s" : ""} — review those explanations even if you got them right.`);
      if (!tips.length) tips.push(pct >= 85 ? "Excellent — move on to a timed mixed set, then revisit in 2–3 days to lock it in." : "Retry your misses now, then do a fresh set tomorrow.");
      el.innerHTML = `<div class="qm-top"><button class="qm-x" data-exit aria-label="Exit">✕</button><div class="qm-title">Debrief${timeUp ? " · time's up" : ""}</div><span></span></div>
        <div class="qm-scroll"><div class="qm-card qm-debrief">
          <div class="qm-big"><div class="qm-ring" style="--p:${pct}"><span>${pct}%</span></div>
            <div><div class="qm-score">${r.correct} of ${r.total} correct</div><div class="muted">${fmt(r.time)} total · ${Math.round(avg)} s per question${vig !== null && rec !== null ? ` · patient cases ${vig}% · recall ${rec}%` : ""}</div></div></div>
          <h3>What to do next</h3><ul class="qm-tips">${tips.map((t) => `<li>${t}</li>`).join("")}</ul>
          <h3>By topic</h3><div class="table-wrap"><table><tbody>${trows.map((t) => `<tr><td>${md(t.t)}</td><td>${t.ok}/${t.n}</td><td><div class="qm-meter"><div style="width:${t.pct}%;background:${t.pct >= 80 ? "var(--good)" : t.pct >= 60 ? "var(--warn)" : "var(--bad)"}"></div></div></td><td>${t.link ? `<a href="${esc(t.link.href)}" data-jump>Study →</a>` : ""}</td></tr>`).join("")}</tbody></table></div>
          <h3>Your misses (${misses.length})</h3>${misses.length ? misses.map((x) => `<div class="qm-miss"><div class="qm-miss-stem">${md(x.q.stem)}</div>
            <div class="small">${x.chose ? `You chose <strong>${x.chose}</strong> · ` : "Unanswered · "}answer <strong>${x.q.answer}</strong>: ${md(x.q.options[x.q.answer])}</div>
            <div class="small muted">${md(x.q.why)}</div>${x.q.link ? `<a class="jump" data-jump href="${esc(x.q.link.href)}">${esc(x.q.link.label)}</a>` : ""}</div>`).join("") : '<p class="muted">None — clean sweep.</p>'}
          <div class="btns">${misses.length ? '<button class="btn" data-retry>Retry my misses</button>' : ""}<button class="btn ghost" data-review>Review all answers</button><button class="btn ghost" data-exit2>Done</button></div>
        </div></div>`;
      el.querySelector("[data-exit]").addEventListener("click", () => exit(true));
      el.querySelector("[data-exit2]").addEventListener("click", () => exit(true));
      el.querySelector("[data-review]").addEventListener("click", () => { st.i = 0; draw(); });
      el.querySelector("[data-retry]")?.addEventListener("click", () => { teardown(); start(misses.map((x) => x.q), { ...opts, title: "Retry: misses", timed: false, feedback: "each" }); });
      el.querySelectorAll("[data-jump]").forEach((a) => a.addEventListener("click", () => exit(true)));
    }
    function teardown() {
      clearInterval(timer);
      document.removeEventListener("keydown", key, true);
      el.removeEventListener("wheel", wheel);
      if (document.fullscreenElement) document.exitFullscreen?.().catch(() => {});
      document.documentElement.style.overflow = prevOverflow;
      el.remove();
    }
    function exit(force) {
      if (force !== true && !st.done && Object.keys(st.chosen).length && !confirm("Leave this quiz? Your answers so far are kept in your history.")) return;
      teardown();
      opts.onExit?.();
    }

    function key(e) {
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      if (!el.querySelector(".qm-opts") && !["Escape"].includes(e.key)) return;  // debrief: let the page scroll normally
      const x = q(), n = Object.keys(x.options).length, locked = reveal(x) || (st.done);
      const k = e.key, up = k.toUpperCase();
      let handled = true;
      if (k === "Escape") exit();
      else if (["ArrowDown", "PageDown", "s", "S", "j", "J"].includes(k)) { if (locked) el.querySelector(".qm-scroll").scrollBy({ top: 160, behavior: "smooth" }); else { st.hi = (st.hi + 1) % n; draw(); } }
      else if (["ArrowUp", "PageUp", "w", "W", "k", "K"].includes(k)) { if (locked) el.querySelector(".qm-scroll").scrollBy({ top: -160, behavior: "smooth" }); else { st.hi = (st.hi - 1 + n) % n; draw(); } }
      else if (k === "Enter" || k === " ") { if (locked || (answered(x) && feedback === "end")) move(1); else pick(Object.keys(x.options)[st.hi]); }
      else if (k === "ArrowRight") move(1);
      else if (k === "ArrowLeft") move(-1);
      else if (L5.includes(up) && up.length === 1 && x.options[up]) pick(up);
      else if ("12345".includes(k) && k.length === 1 && x.options[L5[+k - 1]]) pick(L5[+k - 1]);
      else if (up === "F") flag();
      else handled = false;
      if (handled) { e.preventDefault(); e.stopPropagation(); }
    }
    let wheelLock = 0;
    function wheel(e) {  // scroll-wheel rings: step the highlight before answering; scroll normally after
      const x = q();
      if (!el.querySelector(".qm-opts") || reveal(x) || Math.abs(e.deltaY) < 8) return;
      e.preventDefault();
      if (Date.now() < wheelLock) return;
      wheelLock = Date.now() + 220;
      const n = Object.keys(x.options).length;
      st.hi = (st.hi + (e.deltaY > 0 ? 1 : -1) + n) % n;
      draw();
    }
    document.addEventListener("keydown", key, true);
    el.addEventListener("wheel", wheel, { passive: false });
    draw();
  }

  // Small setup sheet: how many, which, timed or not
  function setup(all, base = {}) {
    const el = document.createElement("div");
    el.className = "qm qm-setup";
    const topics = [...new Set(all.map((q) => q.topic).filter(Boolean))];
    el.innerHTML = `<div class="qm-scroll"><div class="qm-card">
      <h2>${esc(base.title || "Focus quiz")}</h2><p class="muted">Full screen, one question at a time. Works with a keyboard or a Bluetooth remote ring.</p>
      <label class="qm-field">Questions<select name="n">${[10, 20, 40, all.length].filter((v, i, a) => v <= all.length && a.indexOf(v) === i).map((v) => `<option value="${v}">${v === all.length ? `All ${v}` : v}</option>`).join("")}</select></label>
      ${topics.length > 1 ? `<div class="qm-field"><span>Topics <small class="muted">pick one or more · none = all</small></span><div class="qm-topics">${topics.map((t) => `<label class="qm-topic"><input type="checkbox" name="topic" value="${esc(t)}"><span>${esc(t)} <small>${all.filter((q) => q.topic === t).length}</small></span></label>`).join("")}</div><div class="small muted" data-avail></div></div>` : ""}
      ${base.missed?.length ? `<label class="qm-check"><input type="checkbox" name="missed"> Only questions I've missed (${base.missed.length})</label>` : ""}
      <div class="qm-modes">
        <label><input type="radio" name="mode" value="study" ${base.minutes ? "" : "checked"}><span><strong>Study</strong>Explanation after every question</span></label>
        ${base.minutes ? `<label><input type="radio" name="mode" value="exam" checked><span><strong>Exam conditions</strong>All ${all.length} questions in ${base.minutes} minutes, results at the end</span></label>` : ""}
        <label><input type="radio" name="mode" value="timed"><span><strong>Timed (PANCE pace)</strong>1 min per question, results at the end</span></label>
      </div>
      <div class="btns"><button class="btn" data-go>Start</button><button class="btn ghost" data-cancel>Cancel</button></div>
      <p class="small muted">Remote / keys: ↑ ↓ choose · Enter lock in · → next · ← back · F flag · Esc exit. A–E also work.</p></div></div>`;
    document.body.append(el);
    const val = (n) => el.querySelector(`[name=${n}]`);
    el.querySelector("[data-cancel]").addEventListener("click", () => el.remove());
    // chosen topics (any combination) and the "only missed" filter, with a live count of what's available
    const pick = (qs) => {
      const chosen = [...el.querySelectorAll("[name=topic]:checked")].map((c) => c.value);
      if (chosen.length) qs = qs.filter((q) => chosen.includes(q.topic));
      if (val("missed")?.checked) qs = qs.filter((q) => base.missed.includes(q.id));
      return qs;
    };
    const avail = () => { const a = el.querySelector("[data-avail]"); if (a) { const n = pick(all).length; a.textContent = `${n} question${n === 1 ? "" : "s"} match`; } };
    el.querySelectorAll("[name=topic], [name=missed]").forEach((c) => c.addEventListener("change", avail)); avail();
    el.querySelector("[data-go]").addEventListener("click", () => {
      let qs = all.slice();
      qs = pick(qs);
      if (!qs.length) { el.querySelector("[data-avail]").textContent = "No questions match — pick other topics or untick “only missed”."; return; }
      if (base.shuffle !== false) for (let i = qs.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [qs[i], qs[j]] = [qs[j], qs[i]]; }
      qs = qs.slice(0, +val("n").value);
      const mode = el.querySelector("[name=mode]:checked").value, timed = mode !== "study";
      if (mode === "exam") qs = all.slice();  // the full exam, in its built order
      el.remove();
      start(qs, { ...base, timed, feedback: timed ? "end" : "each", secondsPer: mode === "exam" ? (base.minutes * 60) / qs.length : 60 });
    });
    el.querySelector("[data-go]").focus();
  }

  window.dpasQuiz = { start, setup };
})();
