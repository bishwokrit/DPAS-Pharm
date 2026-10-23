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
  // Scope: "unit" = the unit whose exam is next; "all" = cumulative, every unit so far (final prep).
  // Practice on the home page is the current unit; this page adds earlier units and the final.
  const unitOf = Object.fromEntries(CFG.lectures.map((l) => [l.id, l.unit]));
  const nextUnitExam = (CFG.upcoming || []).find((e) => e.unit && e.date >= today());
  const cur = nextUnitExam ? nextUnitExam.unit : Math.max(1, ...CFG.lectures.map((l) => l.unit));
  const finalPeriod = !nextUnitExam;
  let scope = (() => {
    const q = new URLSearchParams(location.search).get("scope");
    if (q === "unit" || q === "all") return q;
    const saved = store.get("rv:scope", null);  // a choice sticks until the unit changes
    return saved && saved.unit === cur ? saved.s : finalPeriod ? "all" : "unit";
  })();
  const P = () => (scope === "unit" ? pool.filter((q) => q.unit === cur) : pool);
  const lidIn = (lid) => scope === "all" || unitOf[lid] === cur;
  // One topic list for everything: lecture questions are filed under the practice exams' (finer) topics,
  // so "Distribution" or "Drug development" means the same thing whichever source a question came from.
  const CANON = [[/language/i, "Language & drug names"], [/development|regulation/i, "Drug development & approval"], [/receptor|pharmacodynamic/i, "Receptors & drug targets"],
    [/dose-?response/i, "Dose-response & therapeutic index"], [/metabolism|cyp/i, "Metabolism & CYP450"], [/excretion|renal/i, "Excretion & renal dosing"],
    [/half-life|pk calc|steady state|clearance/i, "Half-life, steady state & clearance"], [/pharmacogenom|decision|putting it all/i, "Pharmacogenomics & decisions"]];
  const canon = (q) => {
    const t = q.topic || "";
    if (/absorption|distribution|adme/i.test(t)) return /distribut|\bvd\b|volume of distribution|protein[- ]bound|barrier|albumin/i.test(q.stem + " " + Object.values(q.options || {}).join(" ")) ? "Distribution" : "Absorption & routes";
    return (CANON.find(([re]) => re.test(t)) || [, t])[1];
  };

  async function load() {
    await Promise.all(CFG.lectures.map(async (l) => {
      const kb = await fetch(`../${l.id}/kb.json${document.documentElement.dataset.v ? "?v=" + document.documentElement.dataset.v : ""}`).then((r) => r.json()).catch(() => null);
      if (!kb) return;
      kbs[l.id] = kb;
      kb.quiz.forEach((q) => pool.push({ ...q, id: `${l.id}:${q.id}`, raw: q.id, unit: l.unit, from: { type: "lec", lid: l.id }, topic: canon(q), label: `${l.id} · ${q.topic}`,
        link: q.link ? { href: `../${l.id}/index.html${q.link.href}`, label: `Study this: ${l.id} · ${q.link.label.replace("Study this: ", "")}` } : null }));
    }));
    await Promise.all(CFG.exams.map(async (e) => {
      const qs = await fetch(`../exams/${e.id}/quiz.json${document.documentElement.dataset.v ? "?v=" + document.documentElement.dataset.v : ""}`).then((r) => r.json()).catch(() => null);
      if (!qs) return;
      exams[e.id] = e;
      qs.forEach((q) => pool.push({ ...q, raw: q.id, unit: e.unit, from: { type: "exam", slug: e.id }, label: `${e.title} · ${q.topic}`,
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
    P().forEach((q) => {
      const s = status(q);
      if (s === "new") return;
      const r = (t[q.topic] ||= { ok: 0, n: 0, link: q.link });
      r.n++; if (s === "right" || s === "fixed") r.ok++;
    });
    return Object.entries(t).map(([topic, r]) => ({ topic, ...r, pct: Math.round((100 * r.ok) / r.n) })).sort((a, b) => a.pct - b.pct);
  }
  function weighted(n, from = P()) {
    const weak = new Set(topicStats().filter((t) => t.pct < 70).map((t) => t.topic));
    const w = (q) => { const s = status(q); return (s === "missed" ? 6 : s === "new" ? 3 : 1) + (flagged(q) ? 3 : 0) + (weak.has(q.topic) ? 2 : 0); };
    // weighted sampling without replacement
    const items = from.map((q) => ({ q, k: Math.pow(Math.random(), 1 / w(q)) }));
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
  // final mock: the same number from every unit so far, weighted toward weak spots within each
  function finalMock(n) {
    const units = [...new Set(pool.map((q) => q.unit))].sort();
    const per = Math.ceil(n / Math.max(1, units.length));
    return shuffle(units.flatMap((u) => weighted(per, pool.filter((q) => q.unit === u)))).slice(0, n);
  }
  function startDaily() {
    // this-unit Daily 10 still spaces in a few questions from earlier units, so they don't fade before the final
    const past = pool.filter((q) => q.unit < cur);
    const mine = weighted(7);  // a brand-new unit with no lectures yet: all ten come from earlier units
    const qs = scope === "unit" && past.length ? shuffle([...mine, ...weighted(10 - mine.length, past)]) : weighted(10);
    window.dpasQuiz.start(qs, opts("Daily 10", {
      onFinish: (r) => { const log = store.get("daily:log", {}); log[today()] = { score: r.correct, of: r.total }; store.set("daily:log", log); },
    }));
  }

  // ---- weak flashcards (boxes 1–2 you've already seen)
  function weakCards() {
    const out = [];
    for (const [lid, kb] of Object.entries(kbs)) {
      if (!lidIn(lid)) continue;
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

  // ---- page: 1 practice · 2 progress · 3 saved collections
  let tab = store.get("rv:tab", "misses");
  function render() {
    const SP = P(), missed = SP.filter((q) => status(q) === "missed"), flags = SP.filter(flagged), cards = weakCards(), topics = topicStats();
    const notes = Object.keys(kbs).filter(lidIn).flatMap((lid) => store.get(`sk:notes:${lid}`, []).map((n) => ({ ...n, lid })));
    const uname = `Unit ${cur}`;
    $("rv-scope").innerHTML = `<button data-s="unit" class="${scope === "unit" ? "on" : ""}">This unit · ${uname}</button><button data-s="all" class="${scope === "all" ? "on" : ""}">Cumulative · final prep</button>`;
    $("rv-scope").querySelectorAll("[data-s]").forEach((b) => (b.onclick = () => { scope = b.dataset.s; store.set("rv:scope", { s: scope, unit: cur }); render(); }));
    $("rv-scope-sub").textContent = scope === "unit" ? `${uname}: ${CFG.units?.[cur] || ""}. Your Daily 10 still mixes in a few questions from earlier units.` : "Every unit so far, for spaced review and the comprehensive final.";
    const daily = store.get("daily:log", {})[today()];
    const answered = SP.filter((q) => status(q) !== "new"), right = answered.filter((q) => ["right", "fixed"].includes(status(q)));

    // countdown to the next exam, computed today (not when the site was built)
    const nxt = (CFG.upcoming || []).find((e) => e.date >= today());
    if (nxt) {
      const days = Math.round((new Date(nxt.date + "T00:00") - new Date(today() + "T00:00")) / 864e5);
      $("rv-count").hidden = false;
      $("rv-count").innerHTML = `<span class="rv-dot"></span><strong>${esc(nxt.label)}</strong> ${days === 0 ? "is today" : `in ${days} day${days === 1 ? "" : "s"}`} · ${new Date(nxt.date + "T00:00").toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" })}`;
    }

    const tile = (k, ic, title, sub, cta, off) => `<button class="rv-act${k === "daily" ? " main" : ""}" data-a="${k}" ${off ? "disabled" : ""}><span class="rv-ic">${ic}</span><span class="rv-t"><strong>${title}</strong><span>${sub}</span></span><span class="rv-cta">${cta}</span></button>`;
    $("act").innerHTML =
      tile("daily", window.dpasIcon("sun"), "Daily 10", daily ? `Done today · ${daily.score}/${daily.of}. Go again anytime.` : "10 questions, about 5 minutes, weighted toward your weak spots", daily ? "Again →" : "Start →") +
      tile("misses", window.dpasIcon("retry"), "Retry misses", missed.length ? `${missed.length} question${missed.length === 1 ? "" : "s"} you got wrong` : "Nothing to retry yet", "Start →", !missed.length) +
      (scope === "unit" ? tile("mixed", window.dpasIcon("timer"), `Timed ${uname} exam`, `40 questions at exam pace, ${uname} only`, "Start →", !SP.length)
        : tile("mixed", window.dpasIcon("timer"), "Final mock", "50 questions, timed, balanced across every unit so far", "Start →")) +
      tile("custom", window.dpasIcon("sliders"), "Build your own", "Pick size, topic, or misses only", "Set up →");
    const A = (k) => $("act").querySelector(`[data-a="${k}"]`);
    A("daily").onclick = startDaily;
    A("misses").onclick = () => missed.length && window.dpasQuiz.start(shuffle(missed.slice()), opts("Retry: all misses"));
    A("mixed").onclick = () => scope === "unit" ? window.dpasQuiz.start(weighted(40), opts(`Timed ${uname} exam`, { timed: true, feedback: "end" }))
      : window.dpasQuiz.start(finalMock(50), opts("Final mock", { timed: true, feedback: "end" }));
    A("custom").onclick = () => window.dpasQuiz.setup(SP, opts(scope === "unit" ? `Build your own · ${uname}` : "Build your own · all units", { missed: missed.map((q) => q.id) }));

    const pct = answered.length ? Math.round((100 * right.length) / answered.length) : null;
    const stat = (n, l, sub = "") => `<div class="rv-stat"><strong>${n}</strong><span>${l}</span>${sub ? `<i style="width:${sub}%"></i>` : ""}</div>`;
    if (!answered.length) $("stats").innerHTML = '<p class="rv-empty" style="grid-column:1/-1">Nothing tracked yet. Start with the <strong>Daily 10</strong> above. Every answer you give here, in self-tests, or in practice exams shows up as progress.</p>';
    else $("stats").innerHTML = stat(`${answered.length}<small>/${SP.length}</small>`, "questions answered", (100 * answered.length) / Math.max(1, pool.length)) +
      stat(pct === null ? "—" : `${pct}%`, "accuracy", pct ?? 0) + stat(missed.length, "to retry") + stat(`${streak()}`, `day streak`);

    const units = [...new Set(pool.map((q) => q.unit))].sort();
    $("units").innerHTML = scope === "all" && units.length ? `<h3 class="rv-h3">By unit</h3><div class="rv-topics">${units.map((u) => {
      const qs = pool.filter((q) => q.unit === u), a = qs.filter((q) => status(q) !== "new"), r = a.filter((q) => ["right", "fixed"].includes(status(q)));
      const pc = a.length ? Math.round((100 * r.length) / a.length) : null;
      return `<div class="rv-topic"><span class="rv-tn">Unit ${u} · ${esc(CFG.units?.[u] || "")}</span><span class="rv-bar"><i style="width:${pc ?? 0}%;background:${pc === null ? "var(--hair)" : pc >= 80 ? "var(--good)" : pc >= 60 ? "var(--warn)" : "var(--bad)"}"></i></span><span class="rv-tp">${pc === null ? "—" : pc + "%"}</span><span class="rv-go small muted">${a.length}/${qs.length}</span></div>`;
    }).join("")}</div>` : "";
    $("topics").innerHTML = topics.length ? `<div class="rv-topics">${topics.slice(0, 8).map((t) => `<a class="rv-topic" ${t.link ? `href="${esc(t.link.href)}"` : ""}>
        <span class="rv-tn">${md(t.topic)}</span><span class="rv-bar"><i style="width:${t.pct}%;background:${t.pct >= 80 ? "var(--good)" : t.pct >= 60 ? "var(--warn)" : "var(--bad)"}"></i></span><span class="rv-tp">${t.pct}%</span><span class="rv-go">${t.link ? "Study →" : ""}</span></a>`).join("")}</div>`
      : '<p class="rv-empty">Answer a few self-test or practice-exam questions and your weakest topics will rank here, each linked to the part of the study guide that covers it.</p>';

    const list = (qs) => `<ul class="rv-list">${qs.slice(0, 40).map((q) => `<li><span class="small muted">${esc(q.label)}</span><div>${md(q.stem.length > 140 ? q.stem.slice(0, 138) + "…" : q.stem)}</div>${q.link ? `<a class="jump" href="${esc(q.link.href)}">${esc(q.link.label)}</a>` : ""}</li>`).join("")}</ul>`;
    const T = {
      misses: ["Missed", missed.length, () => missed.length ? `<button class="btn small" data-go="misses">Retry all ${missed.length} →</button>${list(missed)}` : "Questions you get wrong in self-tests, Sidekick quizzes, or practice exams land here until you get them right."],
      flags: ["Flagged", flags.length, () => flags.length ? list(flags) : "Press F on any practice-exam question to flag it for later. Flagged questions collect here."],
      cards: ["Flashcards", cards.length, () => cards.length ? `<p>${cards.length} card${cards.length === 1 ? "" : "s"} you marked "Again" or haven't learned yet.</p><button class="btn small" data-drill>Drill them →</button>` : `Study flashcards in Sidekick (the ✦ button on any lecture page). Cards you mark "Again" collect here.`],
      notes: ["Notes", notes.length, () => notes.length ? `<ul class="rv-list">${notes.map((n) => `<li><span class="small muted">${esc(n.lid)} · ${esc(n.where)}</span><div><mark class="hl">${esc(n.text)}</mark>${n.src ? ` <span class="cite">${esc(n.src)}</span>` : ""}</div></li>`).join("")}</ul>` : "Highlight any text in a study guide and tap Save. Your highlights collect here."],
    };
    if (!T[tab]) tab = "misses";
    $("rv-tabs").innerHTML = Object.entries(T).map(([k, [l, n]]) => `<button data-t="${k}" class="${k === tab ? "on" : ""}">${l}${n ? ` <b>${n}</b>` : ""}</button>`).join("");
    const body = T[tab][2]();
    $("rv-panel").innerHTML = body.startsWith("<") ? body : `<p class="rv-empty">${body}</p>`;
    $("rv-tabs").querySelectorAll("[data-t]").forEach((b) => b.onclick = () => { tab = b.dataset.t; store.set("rv:tab", tab); render(); });
    $("rv-panel").querySelector("[data-go]")?.addEventListener("click", () => A("misses").click());
    $("rv-panel").querySelector("[data-drill]")?.addEventListener("click", () => drill(shuffle(cards)));
  }

  load().then(() => (document.readyState === "loading" ? addEventListener("DOMContentLoaded", render) : render()));  // icons come from site.js, which loads after this file
})();
