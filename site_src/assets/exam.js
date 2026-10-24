// Practice-exam app (shared by every exam page). The exam itself is embedded in the page as JSON.
const EXAM = JSON.parse(document.getElementById("exam-data").textContent);
const KEY = "exam:" + EXAM.slug + ":v1", LOG = "exam:" + EXAM.slug + ":log";
const store = { get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch { return d; } },
                set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch {} } };
let S = store.get(KEY, null) || fresh();
if (!S.order || S.order.length !== EXAM.questions.length) S.order = fresh().order;  // progress saved from other pages may lack the order
S.answers ||= {}; S.flags ||= [];
let log = store.get(LOG, []);
let mode = "all", view = [], pos = 0;
const byId = Object.fromEntries(EXAM.questions.map((q) => [q.id, q]));
const $ = (s) => document.querySelector(s);

function fresh() { return { order: EXAM.questions.map((q) => q.id), answers: {}, flags: [], last: 0 }; }
function save() { store.set(KEY, S); }
function md(t) { return String(t).replace(/[&<>]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[c])).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>"); }
function missedEver() { return new Set(log.map((e) => e.id)); }

function buildView() {
  const missed = missedEver();
  view = S.order.filter((id) => {
    const q = byId[id];
    if (mode === "all") return true;
    if (mode === "missed") return missed.has(id);
    if (mode === "flagged") return S.flags.includes(id);
    return q.topic === mode;
  });
  pos = Math.min(pos, Math.max(0, view.length - 1));
}

function render() {
  const answered = Object.keys(S.answers).length, correct = Object.entries(S.answers).filter(([id, L]) => byId[id].answer === L).length;
  $("#score").textContent = `${correct} / ${answered} correct` + (answered ? ` · ${Math.round((100 * correct) / answered)}%` : "");
  $("#bar").style.width = `${(100 * answered) / EXAM.questions.length}%`;
  $("#progress").textContent = `${answered} of ${EXAM.questions.length} answered`;
  const card = $("#card");
  if (!view.length) { card.innerHTML = `<p class="muted">${mode === "missed" ? "No missed questions yet — nice." : mode === "flagged" ? "No flagged questions. Press F on any question to flag it." : "Nothing here."}</p>`; $("#counter").textContent = ""; return; }
  const q = byId[view[pos]], chosen = S.answers[q.id], flagged = S.flags.includes(q.id);
  $("#counter").textContent = `Question ${pos + 1} of ${view.length}`;
  let h = `<div class="qmeta"><span class="chip">${md(q.topic)}</span><span class="chip ${q.kind === "vignette" ? "warn" : ""}">${q.kind === "vignette" ? "Patient case" : "Recall"}</span>${flagged ? '<span class="chip flagchip">Flagged</span>' : ""}</div>`;
  h += `<div class="stem">${md(q.stem)}</div><div class="opts">`;
  for (const L of "ABCDE") {
    const o = q.options[L];
    let cls = "opt";
    if (chosen) { if (o.correct) cls += " right"; else if (L === chosen) cls += " wrong"; else cls += " dim"; }
    h += `<button class="${cls}" data-l="${L}" ${chosen ? "disabled" : ""}><span class="L">${L}</span><span>${md(o.text)}</span></button>`;
  }
  h += "</div>";
  if (chosen) {
    const right = chosen === q.answer;
    h += `<div class="result ${right ? "ok" : "no"}">${right ? "Correct" : `Not quite — the answer is ${q.answer}`}</div><div class="rationales">`;
    for (const L of "ABCDE") {
      const o = q.options[L];
      h += `<div class="rat ${o.correct ? "is-right" : ""}"><span class="L">${L}</span><div><div class="rat-opt">${md(o.text)}</div><div class="rat-why">${o.correct ? "<strong>Why it's right:</strong> " : "<strong>Why it's wrong:</strong> "}${md(o.why)}</div></div></div>`;
    }
    h += `</div><div class="callout hy"><div class="label">High-yield takeaway</div>${md(q.takeaway)}</div>`;
    h += `<div class="callout why"><div class="label">How to tell it apart</div>${md(q.discriminator)}</div>`;
    h += `<p class="small muted">Source: ${md(q.src)}</p>`;
    if (q.link) h += `<a class="jump" href="${q.link.href}">${md(q.link.label)}</a>`;
  }
  card.innerHTML = h;
  card.querySelectorAll(".opt").forEach((b) => b.addEventListener("click", () => answer(b.dataset.l)));
  $("#flag").textContent = flagged ? "Unflag (F)" : "Flag (F)";
  S.last = pos; save();
}

function answer(L) {
  const q = byId[view[pos]];
  if (S.answers[q.id]) return;
  S.answers[q.id] = L;
  window.dpasLog?.(q, L === q.answer, null);
  if (L !== q.answer) { log.push({ id: q.id, topic: q.topic, chose: L, at: new Date().toISOString() }); store.set(LOG, log); }
  save(); render(); renderScorecard();
}

function go(d) { if (!view.length) return; pos = Math.max(0, Math.min(view.length - 1, pos + d)); render(); window.scrollTo({ top: 0, behavior: "smooth" }); }
function toggleFlag() { const id = view[pos]; if (!id) return; S.flags = S.flags.includes(id) ? S.flags.filter((x) => x !== id) : [...S.flags, id]; save(); render(); }

function renderScorecard() {
  const rows = EXAM.topics.map((t) => {
    const qs = EXAM.questions.filter((q) => q.topic === t);
    const ans = qs.filter((q) => S.answers[q.id]);
    const ok = ans.filter((q) => S.answers[q.id] === q.answer).length;
    const misses = log.filter((e) => e.topic === t).length;
    const pct = ans.length ? Math.round((100 * ok) / ans.length) : null;
    return { t, n: qs.length, done: ans.length, ok, pct, misses };
  });
  $("#scorecard").innerHTML = rows.map((r) => `<tr><td>${md(r.t)}</td><td>${r.done}/${r.n}</td><td>${r.pct === null ? "—" : r.pct + "%"}</td><td>${r.misses}</td></tr>`).join("");
  const weak = rows.filter((r) => r.misses > 0).sort((a, b) => b.misses - a.misses).slice(0, 3);
  $("#studynext").innerHTML = weak.length ? "Study next: " + weak.map((r) => `<strong>${md(r.t)}</strong> (${r.misses} missed)`).join(", ") + ". Use the topic filter or “Missed” to drill them." : "Answer some questions to see where to focus.";
  const recent = log.slice(-12).reverse();
  $("#log").innerHTML = recent.length ? recent.map((e) => `<li><a href="#" data-id="${e.id}">${md(byId[e.id].stem.slice(0, 90))}…</a> <span class="muted small">· ${md(e.topic)} · chose ${e.chose} · ${new Date(e.at).toLocaleDateString()}</span></li>`).join("") : '<li class="muted">No misses recorded yet.</li>';
  $("#log").querySelectorAll("a").forEach((a) => a.addEventListener("click", (ev) => { ev.preventDefault(); mode = "all"; $("#mode").value = "all"; buildView(); pos = view.indexOf(a.dataset.id); render(); window.scrollTo({ top: 0, behavior: "smooth" }); }));
  $("#logcount").textContent = `${log.length} miss${log.length === 1 ? "" : "es"} recorded (kept even when you reset)`;
}

function asQuiz(q) {
  const opts = {}, whys = {};
  for (const L of "ABCDE") { opts[L] = q.options[L].text; if (L !== q.answer) whys[L] = q.options[L].why; }
  return { id: q.id, stem: q.stem, options: opts, answer: q.answer, why: q.options[q.answer].why, whys, takeaway: q.takeaway,
           discriminator: q.discriminator, src: q.src, topic: q.topic, kind: q.kind, link: q.link };
}
function focusSession() {
  window.dpasQuiz.setup(EXAM.questions.map(asQuiz), {
    title: EXAM.title || "Practice exam", missed: [...missedEver()], minutes: EXAM.minutes || 0,
    onAnswer: (q, L, ok) => {
      S.answers[q.id] = L;
      if (!ok) { log.push({ id: q.id, topic: q.topic, chose: L, at: new Date().toISOString() }); store.set(LOG, log); }
      save();
    },
    onExit: () => { buildView(); render(); renderScorecard(); },
  });
}

function init() {
  $("#focus").addEventListener("click", focusSession);
  const sel = $("#mode");
  sel.innerHTML = `<option value="all">All questions</option><option value="missed">Missed (ever)</option><option value="flagged">Flagged</option><optgroup label="Topic">` +
    EXAM.topics.map((t) => `<option value="${md(t)}">${md(t)}</option>`).join("") + "</optgroup>";
  sel.addEventListener("change", () => { mode = sel.value; pos = 0; buildView(); render(); });
  $("#prev").addEventListener("click", () => go(-1));
  $("#next").addEventListener("click", () => go(1));
  $("#flag").addEventListener("click", toggleFlag);
  $("#shuffle").addEventListener("click", () => { const o = S.order.slice(); for (let i = o.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [o[i], o[j]] = [o[j], o[i]]; } S.order = o; pos = 0; save(); buildView(); render(); });
  $("#reset").addEventListener("click", () => { if (confirm("Reset your answers and flags? Your missed-question history stays.")) { S = fresh(); pos = 0; save(); buildView(); render(); renderScorecard(); } });
  document.addEventListener("keydown", (e) => {
    if (e.target.tagName === "SELECT" || e.metaKey || e.ctrlKey || e.altKey) return;
    const k = e.key.toUpperCase();
    if ("ABCDE".includes(k) && k.length === 1) answer(k);
    else if ("12345".includes(k) && k.length === 1) answer("ABCDE"[+k - 1]);
    else if (e.key === "ArrowRight") go(1);
    else if (e.key === "ArrowLeft") go(-1);
    else if (k === "F") toggleFlag();
  });
  buildView(); pos = Math.min(S.last || 0, view.length - 1);
  const deep = location.hash.match(/^#q-(.+)$/);  // links from site search
  if (deep && byId[deep[1]]) { mode = "all"; buildView(); pos = view.indexOf(deep[1]); }
  render(); renderScorecard();
}
init();
