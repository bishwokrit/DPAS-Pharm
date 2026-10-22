// Exam-week review: everything you've missed, flagged, or saved — across every lecture and practice exam —
// plus Daily 10 and a weak-spot mixed exam. Reads only this browser's saved progress.
(function () {
  const CFG = JSON.parse(document.getElementById("review-data").textContent);
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* private mode */ } },
  };
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const md = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  const today = () => { const d = new Date(); return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`; };
  const shuffle = (a) => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const $ = (id) => document.getElementById(id);

  let pool = [], kbs = {}, exams = {};

  async function load() {
    await Promise.all(CFG.lectures.map(async (l) => {
      const kb = await fetch(`../${l.id}/kb.json`).then((r) => r.json()).catch(() => null);
      if (!kb) return;
      kbs[l.id] = kb;
      kb.quiz.forEach((q) => pool.push({ ...q, id: `${l.id}:${q.id}`, raw: q.id, from: { type: "lec", lid: l.id }, topic: q.topic, label: `${l.id} · ${q.topic}`,
        link: q.link ? { href: `../${l.id}/index.html${q.link.href}`, label: `Study this: ${l.id} · ${q.link.label.replace("Study this: ", "")}` } : null }));
    }));
    await Promise.all(CFG.exams.map(async (e) => {
      const qs = await fetch(`../exams/${e.id}/quiz.json`).then((r) => r.json()).catch(() => null);
      if (!qs) return;
      exams[e.id] = e;
      qs.forEach((q) => pool.push({ ...q, raw: q.id, from: { type: "exam", slug: e.id }, label: `${e.title} · ${q.topic}`,
        link: q.link ? { ...q.link, href: q.link.href.replace(/^\.\.\/\.\.\//, "../") } : null }));
    }));
  }

  // ---- saved progress, read from each feature's own keys
  const examState = (slug) => store.get(`exam:${slug}:v1`, null) || { answers: {}, flags: [] };
  const examLog = (slug) => store.get(`exam:${slug}:log`, []);
  function status(q) {
    if (q.from.type === "lec") {
      if (store.get(`miss:${q.from.lid}`, []).includes(q.raw)) return "missed";
      if (store.get(`done:${q.from.lid}`, []).includes(q.raw)) return "right";
      return "new";
    }
    const st = examState(q.from.slug), a = st.answers[q.raw];
    if (a !== undefined) return a === q.answer ? (examLog(q.from.slug).some((e) => e.id === q.raw) ? "fixed" : "right") : "missed";
    return examLog(q.from.slug).some((e) => e.id === q.raw) ? "missed" : "new";
  }
  const flagged = (q) => q.from.type === "exam" && (examState(q.from.slug).flags || []).includes(q.raw);
  function record(q, L, ok) {
    if (q.from.type === "lec") {
      const lid = q.from.lid, m = new Set(store.get(`miss:${lid}`, []));
      ok ? m.delete(q.raw) : m.add(q.raw);
      store.set(`miss:${lid}`, [...m]);
      if (ok) store.set(`done:${lid}`, [...new Set([...store.get(`done:${lid}`, []), q.raw])]);
    } else {
      const slug = q.from.slug, st = examState(slug);
      st.answers[q.raw] = L; st.order ||= []; st.flags ||= [];
      store.set(`exam:${slug}:v1`, st);
      if (!ok) store.set(`exam:${slug}:log`, [...examLog(slug), { id: q.raw, topic: q.topic, chose: L, at: new Date().toISOString() }]);
    }
  }

  function topicStats() {
    const t = {};
    pool.forEach((q) => {
      const s = status(q);
      if (s === "new") return;
      const r = (t[q.topic] ||= { ok: 0, n: 0, link: q.link });
      r.n++; if (s === "right" || s === "fixed") r.ok++;
    });
    return Object.entries(t).map(([topic, r]) => ({ topic, ...r, pct: Math.round((100 * r.ok) / r.n) })).sort((a, b) => a.pct - b.pct);
  }
  function weighted(n) {
    const weak = new Set(topicStats().filter((t) => t.pct < 70).map((t) => t.topic));
    const w = (q) => { const s = status(q); return (s === "missed" ? 6 : s === "new" ? 3 : 1) + (flagged(q) ? 3 : 0) + (weak.has(q.topic) ? 2 : 0); };
    // weighted sampling without replacement
    const items = pool.map((q) => ({ q, k: Math.pow(Math.random(), 1 / w(q)) }));
    return items.sort((a, b) => b.k - a.k).slice(0, n).map((x) => x.q);
  }
  const refresh = () => render();
  const opts = (title, extra = {}) => ({ title, onAnswer: (q, L, ok) => record(q, L, ok), onExit: refresh, ...extra });

  // ---- Daily 10 with a streak
  function streak() {
    const done = store.get("daily:log", {});
    let n = 0;
    for (let d = new Date(); ; d.setDate(d.getDate() - 1)) {
      const key = `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
      if (done[key]) n++; else if (key !== today()) break;
      if (n > 365) break;
    }
    return n;
  }
  function startDaily() {
    window.dpasQuiz.start(weighted(10), opts("Daily 10", {
      onFinish: (r) => { const log = store.get("daily:log", {}); log[today()] = { score: r.correct, of: r.total }; store.set("daily:log", log); },
    }));
  }

  // ---- weak flashcards (boxes 1–2 you've already seen)
  function weakCards() {
    const out = [];
    for (const [lid, kb] of Object.entries(kbs)) {
      const boxes = store.get(`sk:fc:${lid}`, {});
      kb.cards.forEach((c, i) => { if (boxes[i] !== undefined && boxes[i] <= 2) out.push({ ...c, lid, key: i }); });
      store.get(`sk:mycards:${lid}`, []).forEach((c, i) => { const k = "m" + i; if (boxes[k] !== undefined && boxes[k] <= 2) out.push({ ...c, lid, key: k, mine: true }); });
    }
    return out;
  }
  function drill(cards) {
    let i = 0;
    const el = document.createElement("div");
    el.className = "qm";
    document.body.append(el);
    document.documentElement.style.overflow = "hidden";
    const close = () => { el.remove(); document.documentElement.style.overflow = ""; document.removeEventListener("keydown", key, true); render(); };
    const draw = () => {
      if (i >= cards.length) { el.innerHTML = `<div class="qm-scroll"><div class="qm-card" style="text-align:center;padding-top:15vh"><div class="qm-score">Drill done</div><p class="muted">${cards.length} cards reviewed.</p><button class="btn" data-x>Back to review</button></div></div>`; el.querySelector("[data-x]").onclick = close; return; }
      const c = cards[i];
      el.innerHTML = `<div class="qm-top"><button class="qm-x" data-x>✕</button><div class="qm-count">${i + 1} <span>/ ${cards.length}</span></div><div class="qm-title">Weak flashcards · ${c.lid}</div><span></span></div>
        <div class="qm-scroll"><div class="qm-card"><div class="sk-card" tabindex="0" style="min-height:260px"><div class="sk-face"><div class="small muted">Tap or press Enter to flip</div><div class="sk-q">${md(c.q)}</div></div>
        <div class="sk-face back"><div class="sk-a">${md(c.a)}</div><span class="cite">${esc(c.src || "")}</span></div></div>
        <div class="sk-row" style="justify-content:center;margin-top:18px"><button class="btn ghost" data-again>Again (←)</button><button class="btn" data-good>Got it (→)</button></div></div></div>`;
      el.querySelector("[data-x]").onclick = close;
      const card = el.querySelector(".sk-card");
      card.onclick = () => card.classList.toggle("flipped");
      el.querySelector("[data-again]").onclick = () => grade(false);
      el.querySelector("[data-good]").onclick = () => grade(true);
    };
    const grade = (up) => { const c = cards[i], k = `sk:fc:${c.lid}`, b = store.get(k, {}); b[c.key] = up ? Math.min(5, (b[c.key] || 1) + 1) : 1; store.set(k, b); i++; draw(); };
    const key = (e) => {
      if (e.key === "Escape") close();
      else if (e.key === "Enter" || e.key === " " || e.key === "ArrowDown" || e.key === "ArrowUp") { el.querySelector(".sk-card")?.classList.toggle("flipped"); e.preventDefault(); }
      else if (e.key === "ArrowRight" && i < cards.length) grade(true);
      else if (e.key === "ArrowLeft" && i < cards.length) grade(false);
    };
    document.addEventListener("keydown", key, true);
    draw();
  }

  // ---- page
  function render() {
    const missed = pool.filter((q) => status(q) === "missed"), flags = pool.filter(flagged), cards = weakCards(), topics = topicStats();
    const notes = Object.keys(kbs).flatMap((lid) => store.get(`sk:notes:${lid}`, []).map((n) => ({ ...n, lid })));
    const daily = store.get("daily:log", {})[today()];
    $("act").innerHTML = `
      <button class="card act" data-daily><div class="act-ic">☀︎</div><div><strong>Daily 10</strong><span>${daily ? `Done today: ${daily.score}/${daily.of} · ` : ""}${streak()}-day streak · weighted to your weak spots</span></div></button>
      <button class="card act" data-misses ${missed.length ? "" : "disabled"}><div class="act-ic">↺</div><div><strong>Retry my misses</strong><span>${missed.length} question${missed.length === 1 ? "" : "s"} across all lectures and exams</span></div></button>
      <button class="card act" data-mixed><div class="act-ic">⏱</div><div><strong>Weak-spot mixed exam</strong><span>40 questions, timed at PANCE pace, from every lecture and exam</span></div></button>
      <button class="card act" data-custom><div class="act-ic">⚙︎</div><div><strong>Custom mixed exam</strong><span>Pick the size, a topic, or misses only — study or timed</span></div></button>`;
    $("act").querySelector("[data-daily]").onclick = startDaily;
    $("act").querySelector("[data-misses]").onclick = () => missed.length && window.dpasQuiz.start(shuffle(missed.slice()), opts("Retry: all misses"));
    $("act").querySelector("[data-mixed]").onclick = () => window.dpasQuiz.start(weighted(40), opts("Weak-spot mixed exam", { timed: true, feedback: "end" }));
    $("act").querySelector("[data-custom]").onclick = () => window.dpasQuiz.setup(pool, opts("Mixed exam — all lectures", { missed: missed.map((q) => q.id) }));

    $("topics").innerHTML = topics.length ? `<div class="table-wrap" style="margin:0;box-shadow:none"><table><tbody>${topics.map((t) => `<tr><td>${md(t.topic)}</td><td class="nowrap">${t.ok}/${t.n}</td>
      <td style="width:40%"><div class="qm-meter"><div style="width:${t.pct}%;background:${t.pct >= 80 ? "var(--good)" : t.pct >= 60 ? "var(--warn)" : "var(--bad)"}"></div></div></td>
      <td>${t.link ? `<a href="${esc(t.link.href)}">Study →</a>` : ""}</td></tr>`).join("")}</tbody></table></div>` : '<p class="muted">Answer some self-test or exam questions and your weakest topics show up here.</p>';

    const list = (qs, empty) => qs.length ? `<ul class="rv-list">${qs.slice(0, 40).map((q) => `<li><span class="small muted">${esc(q.label)}</span><div>${md(q.stem.length > 140 ? q.stem.slice(0, 138) + "…" : q.stem)}</div>${q.link ? `<a class="jump" href="${esc(q.link.href)}">${esc(q.link.label)}</a>` : ""}</li>`).join("")}</ul>` : `<p class="muted">${empty}</p>`;
    $("misses").innerHTML = list(missed, "No misses right now. Nice.");
    $("flags").innerHTML = list(flags, "Nothing flagged. Press F on any exam question to flag it.");
    $("cards").innerHTML = cards.length ? `<p>${cards.length} card${cards.length === 1 ? "" : "s"} still in the New/Learning boxes.</p><button class="btn" data-drill>Drill weak cards →</button>` : '<p class="muted">No weak cards yet. Study flashcards in Sidekick; cards you mark "Again" collect here.</p>';
    $("cards").querySelector("[data-drill]")?.addEventListener("click", () => drill(shuffle(cards)));
    $("notes").innerHTML = notes.length ? `<ul class="rv-list">${notes.map((n) => `<li><span class="small muted">${esc(n.lid)} · ${esc(n.where)}</span><div><mark class="hl">${esc(n.text)}</mark>${n.src ? ` <span class="cite">${esc(n.src)}</span>` : ""}</div>${n.note ? `<div class="small">↳ ${esc(n.note)}</div>` : ""}<a class="jump" href="../${esc(n.lid)}/index.html#${esc(n.anchor)}">Open →</a></li>`).join("")}</ul>` : '<p class="muted">Highlight text in any study guide and tap 🖍 Save — your notes collect here.</p>';
    $("counts").textContent = `${pool.length} questions from ${Object.keys(kbs).length} lecture${Object.keys(kbs).length === 1 ? "" : "s"} and ${Object.keys(exams).length} practice exam${Object.keys(exams).length === 1 ? "" : "s"}`;
  }

  load().then(render);
})();
