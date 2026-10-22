// Sidekick: a NotebookLM-style study assistant that lives in a side panel on each lecture page.
// Free tools run entirely in the browser from this lecture's kb.json (our cited study content).
// Optional AI chat calls Claude with the student's OWN API key, kept only in this browser.
const SDK_URL = new URL("vendor/anthropic-sdk.mjs", import.meta.url).href; // official SDK, bundled by pipeline/build_vendor.mjs
const MODELS = [
  ["claude-opus-5-5", "Claude Opus 5.5 — best answers"],
  ["claude-sonnet-5-5", "Claude Sonnet 5.5 — faster, cheaper"],
  ["claude-haiku-5-5", "Claude Haiku 5.5 — fastest, cheapest"],
];

const store = {
  get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch { return d; } },
  set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* private mode */ } },
  del(k) { try { localStorage.removeItem(k); } catch { /* ignore */ } },
};
const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const md = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
const plain = (s) => String(s ?? "").replace(/\*\*/g, "");
const cite = (src) => (src ? `<span class="cite">${esc(src)}</span>` : "");
const tags = (o) => (o.tb ? '<span class="tag tb">TB</span>' : "") + (o.sg ? '<span class="tag sg">SG</span>' : "");
const shuffle = (a) => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
const goTo = (anchor) => { const el = document.getElementById(anchor); if (el) { el.scrollIntoView({ behavior: "smooth" }); if (matchMedia("(max-width: 760px)").matches) close(); } };

let Anthropic, kb, sourceText = "", panel, body, tab = store.get("sk:tab", "ask");

// ---------------------------------------------------------------- search (BM25 over cited chunks)
const STOP = new Set("a an and are as at be by can do does for from has have how i in is it its of on or that the this to was what when which who why will with you your vs versus".split(" "));
const stem = (w) => w.replace(/(ations?|ization|ments?|ness|ically|ical|ally|ing|ed|ies|es|s|ly)$/, "") || w;
const terms = (s) => plain(s).toLowerCase().normalize("NFKC").match(/[a-z0-9₀-₉]+/g)?.filter((w) => !STOP.has(w)).map(stem) || [];
let index, indexAll = null, allSources = "";
function makeIndex(chunks) {
  const docs = chunks.map((c) => terms(c.text + " " + c.where));
  const df = new Map();
  docs.forEach((d) => new Set(d).forEach((t) => df.set(t, (df.get(t) || 0) + 1)));
  const avg = docs.reduce((n, d) => n + d.length, 0) / Math.max(1, docs.length);
  return { docs, df, avg, N: docs.length, chunks };
}
function buildIndex() { index = makeIndex(kb.chunks.map((c) => ({ ...c, lid: kb.lecture }))); }
function search(q, k = 6, idx = index) {
  const qt = [...new Set(terms(q))];
  if (!qt.length) return [];
  const { docs, df, avg, N } = idx;
  return docs.map((d, i) => {
    let s = 0;
    for (const t of qt) {
      const tf = d.filter((w) => w === t || (t.length > 3 && w.startsWith(t))).length;
      if (!tf) continue;
      const idf = Math.log(1 + (N - (df.get(t) || 0) + 0.5) / ((df.get(t) || 0) + 0.5));
      s += idf * (tf * 2.2) / (tf + 1.2 * (0.25 + 0.75 * d.length / avg));
    }
    return [s, i];
  }).filter(([s]) => s > 0).sort((a, b) => b[0] - a[0]).slice(0, k).map(([, i]) => idx.chunks[i]);
}
// Every lecture at once (for cumulative review): loads the other lectures' cited chunks on first use
async function ensureAll() {
  if (indexAll) return indexAll;
  const others = await Promise.all((kb.lectures || []).filter((l) => l.id !== kb.lecture).map((l) =>
    fetch(`../${l.id}/kb.json`).then((r) => r.json()).then((k) => ({ k, l })).catch(() => null)));
  const chunks = kb.chunks.map((c) => ({ ...c, lid: kb.lecture }));
  others.filter(Boolean).forEach(({ k }) => k.chunks.forEach((c) => chunks.push({ ...c, lid: k.lecture, where: `${k.lecture} · ${c.where}` })));
  indexAll = makeIndex(chunks);
  return indexAll;
}
async function loadAllSources() {
  if (allSources) return allSources;
  const parts = await Promise.all((kb.lectures || []).map((l) => fetch(`../${l.id}/${l.source}`).then((r) => r.text()).then((t) => `=== ${l.id}: ${l.title} ===\n${t}`).catch(() => "")));
  return (allSources = parts.filter(Boolean).join("\n\n"));
}
const hitLink = (h) => (h.lid && h.lid !== kb.lecture ? `../${h.lid}/index.html#${h.anchor}` : `#${h.anchor}`);
function wireGo(root) {
  root.querySelectorAll("[data-go]").forEach((a) => a.addEventListener("click", (e) => {
    if (a.getAttribute("href").startsWith("#")) { e.preventDefault(); goTo(a.dataset.go); }
  }));
}

// ---------------------------------------------------------------- panel shell
const TABS = [["ask", "Ask"], ["notes", "Notes"], ["cards", "Flashcards"], ["quiz", "Quiz"], ["listen", "Listen"], ["map", "Mind map"], ["brief", "Briefing"], ["faq", "FAQ"]];
function mount() {
  const fab = document.createElement("button");
  fab.className = "sk-fab noprint";
  fab.innerHTML = '<span aria-hidden="true">✦</span> Sidekick';
  fab.title = "Open Sidekick (press /)";
  fab.addEventListener("click", open);
  panel = document.createElement("aside");
  panel.className = "sk-panel noprint";
  panel.setAttribute("aria-label", "Sidekick study assistant");
  panel.innerHTML = `<div class="sk-head"><div><div class="sk-title">✦ Sidekick</div><div class="small muted">${esc(kb.title)}</div></div>
    <button class="sk-x" aria-label="Close">✕</button></div>
    <div class="sk-tabs" role="tablist">${TABS.map(([id, l]) => `<button role="tab" data-tab="${id}">${l}</button>`).join("")}</div>
    <div class="sk-body"></div>`;
  document.body.append(fab, panel);
  body = panel.querySelector(".sk-body");
  panel.querySelector(".sk-x").addEventListener("click", close);
  panel.querySelectorAll("[data-tab]").forEach((b) => b.addEventListener("click", () => show(b.dataset.tab)));
  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && !/input|textarea|select/i.test(document.activeElement.tagName)) { e.preventDefault(); open(); }
    if (e.key === "Escape" && panel.classList.contains("open")) close();
  });
  const want = new URLSearchParams(location.search).get("sk");  // e.g. ?sk=listen from the home page
  if (want && TABS.some(([id]) => id === want)) { tab = want; open(); }
  else if (store.get("sk:open", false)) open();
}
function open() { panel.classList.add("open"); document.body.classList.add("sk-on"); store.set("sk:open", true); show(tab); }
function close() { panel.classList.remove("open"); document.body.classList.remove("sk-on"); store.set("sk:open", false); speechSynthesis?.cancel(); }
function show(id, arg) {
  tab = id; store.set("sk:tab", id);
  panel.querySelectorAll("[data-tab]").forEach((b) => b.setAttribute("aria-selected", b.dataset.tab === id));
  if (id !== "listen") speechSynthesis?.cancel();
  ({ ask: askTab, listen: listenTab, cards: cardsTab, quiz: quizTab, map: mapTab, brief: briefTab, faq: faqTab, notes: notesTab, source: sourceView, explain: explainFree, card: newCard, compare: compareView })[id](arg);
  body.scrollTop = 0;
}

// ---------------------------------------------------------------- Ask: search + optional AI chat
const chat = { history: [], busy: false };
let scope = store.get("sk:scope", "this");
function askTab(prefill) {
  const key = store.get("sk:key", "");
  body.innerHTML = `<form class="sk-ask"><input name="q" placeholder="Ask about this lecture…" autocomplete="off" value="${esc(prefill || "")}"><button class="btn">Ask</button></form>
    <div class="sk-ai-line small">${key ? `AI chat <strong>on</strong> · ${esc(MODELS.find((m) => m[0] === store.get("sk:model", MODELS[0][0]))?.[1].split(" —")[0])} · <a href="#" data-ai>settings</a>${chat.history.length ? ' · <a href="#" data-clear>new chat</a>' : ""}`
      : `Searching your study materials. <a href="#" data-ai>Turn on AI chat</a> (optional, uses your own Claude API key).`}</div>
    ${(kb.lectures || []).length > 1 ? `<div class="sk-scope small"><button data-scope="this" class="${scope === "this" ? "on" : ""}">This lecture</button><button data-scope="all" class="${scope === "all" ? "on" : ""}">All lectures (${kb.lectures.length})</button></div>` : ""}
    ${chat.history.length ? "" : '<p class="sk-tip small">Tip: <strong>highlight any text</strong> in the guide to Explain it, see its Source slide or textbook page, get quizzed, make a flashcard, or save it to Notes.</p>'}
    <div class="sk-thread"></div><div class="sk-results"></div>`;
  const form = body.querySelector("form");
  body.querySelector("[data-ai]").addEventListener("click", (e) => { e.preventDefault(); aiSettings(); });
  body.querySelector("[data-clear]")?.addEventListener("click", (e) => { e.preventDefault(); chat.history = []; askTab(); });
  body.querySelectorAll("[data-scope]").forEach((b) => b.addEventListener("click", () => { scope = b.dataset.scope; store.set("sk:scope", scope); chat.history = []; askTab(); }));
  renderThread();
  form.addEventListener("submit", (e) => { e.preventDefault(); const q = form.q.value.trim(); if (q) ask(q); form.q.value = ""; });
  if (prefill) ask(prefill);
  else form.q.focus();
}
function renderThread() {
  const t = body.querySelector(".sk-thread");
  if (!t) return;
  t.innerHTML = chat.history.map((m) => m.role === "user" ? `<div class="sk-msg me">${esc(m.label || m.content)}</div>`
    : `<div class="sk-msg ai">${md(m.content).replace(/\n/g, "<br>")}</div>`).join("") +
    (chat.history.length && !chat.busy ? `<div class="sk-follow">${FOLLOW.map(([l]) => `<button data-f="${l}">${l}</button>`).join("")}</div>` : "");
  t.querySelectorAll("[data-f]").forEach((b) => b.addEventListener("click", () => aiAnswer(FOLLOW.find(([l]) => l === b.dataset.f)[1], b.dataset.f)));
}
async function ask(q) {
  const idx = scope === "all" ? await ensureAll() : index;
  const hits = search(q, scope === "all" ? 8 : 6, idx);
  body.querySelector(".sk-results").innerHTML = `<h4>From your study materials${scope === "all" ? " · all lectures" : ""}</h4>` + (hits.length ? hits.map((h) =>
    `<div class="sk-hit"><div class="small muted">${esc(h.where)}</div><div>${tags(h)}${md(h.text)}${cite(h.src)}</div>
     <a href="${esc(hitLink(h))}" data-go="${esc(h.anchor)}" class="small">${h.lid !== kb.lecture ? `Open in ${esc(h.lid)} →` : "Go to section →"}</a></div>`).join("")
    : `<p class="muted">Nothing matched. Try different words (e.g., a drug name or term) — or it may be <strong>not covered in materials</strong>.</p>`);
  wireGo(body);
  if (store.get("sk:key", "")) aiAnswer(q);
}
async function loadSource() {
  if (!sourceText && kb.source) sourceText = await fetch(kb.source).then((r) => r.text()).catch(() => "");
  return sourceText;
}
const FOLLOW = [
  ["Simpler", "Explain that again more simply, like you're talking to a first-year student. Same facts, same citations."],
  ["Clinical example", "Give a short clinical example (a patient scenario) that shows this — using only drugs and facts from the source, with citations."],
  ["Mnemonic", "Give one memory aid for this. Label it \"Mnemonic (memory aid)\" and do not add any fact that isn't in the source."],
  ["Quiz me", "Ask me one PANCE-style question (options A–E) on this, from the source only. Don't give the answer until I reply."],
];
async function askAI(prompt, label) {
  if (!panel.classList.contains("open")) open();
  if (tab !== "ask") show("ask");
  aiAnswer(prompt, label);
}
async function aiAnswer(q, label) {
  if (chat.busy) return;
  chat.busy = true;
  chat.history.push({ role: "user", content: q, label });
  renderThread();
  const t = body.querySelector(".sk-thread");
  const out = document.createElement("div");
  out.className = "sk-msg ai";
  out.innerHTML = '<span class="muted">Thinking…</span>';
  t.append(out);
  let text = "";
  try {
    Anthropic ||= (await import(SDK_URL)).default;
    // Only ever the student's own key from this browser, sent straight to Anthropic — no proxy, no shared key.
    const key = store.get("sk:key", "");
    if (!/^sk-ant-/.test(key)) throw new Error("No personal API key saved");
    const client = new Anthropic({ apiKey: key, authToken: null, baseURL: "https://api.anthropic.com", dangerouslyAllowBrowser: true });
    const source = scope === "all" ? await loadAllSources() : await loadSource();
    const model = store.get("sk:model", MODELS[0][0]);
    const stream = client.beta.messages.stream({
      model,
      max_tokens: 4000,
      ...(model === "claude-haiku-5-5" ? {} : { betas: ["server-side-fallback-2026-07-01"], fallbacks: "default" }),
      output_config: { effort: "low" },
      system: [
        { type: "text", text: "You are Sidekick, a study assistant for a physician assistant student in clinical pharmacology. Answer only from the lecture source below. Cite every fact the way the source does, e.g. (S12), (S12 notes), (p. 17), (SG U1-R3). If the source does not cover something, say \"Not covered in materials\" rather than using outside knowledge. Keep answers short and scannable: a direct answer first, then up to 5 bullets. Use **bold** for the single most testable point. When asked to quiz, ask one PANCE-style question at a time and wait for the answer." },
        { type: "text", text: scope === "all" ? `COURSE SOURCES (every lecture so far):\n\n${source}` : `LECTURE SOURCE (${kb.title}):\n\n${source}`, cache_control: { type: "ephemeral" } },
      ],
      messages: chat.history.map(({ role, content }) => ({ role, content })),
    });
    stream.on("text", (d) => { text += d; out.innerHTML = md(text).replace(/\n/g, "<br>"); });
    const msg = await stream.finalMessage();
    if (msg.stop_reason === "refusal") text = text || "Claude declined to answer this one. Try rephrasing the question.";
    if (msg.stop_reason === "max_tokens") text += "\n\n(Answer cut off — ask me to continue.)";
    chat.history.push({ role: "assistant", content: text });
    chat.busy = false;
    renderThread();
  } catch (err) {
    console.error("Sidekick chat:", err);
    chat.history.pop();
    const is = (cls) => Anthropic && err instanceof Anthropic[cls];
    const why = /No personal API key/.test(err?.message) ? "AI chat needs your own Anthropic API key (it starts with sk-ant-). Add it in settings."
      : is("AuthenticationError") ? "Your API key was rejected — check it in settings."
      : is("RateLimitError") ? "Rate limited — wait a moment and try again."
      : is("PermissionDeniedError") || is("NotFoundError") ? "This key can't use that model — try another model in settings."
      : is("APIConnectionError") || !Anthropic ? "Couldn't reach Claude — check your connection."
      : `Something went wrong (${esc(err?.message || err)}).`;
    out.innerHTML = `<span style="color:var(--bad)">${why}</span>`;
  } finally {
    chat.busy = false;
  }
}
function aiSettings() {
  const key = store.get("sk:key", ""), model = store.get("sk:model", MODELS[0][0]);
  body.innerHTML = `<h3>AI chat (optional)</h3>
    <p class="small">Chat with Claude about <strong>this lecture only</strong>. It answers from the same cited source this page is built from, and says "Not covered in materials" otherwise.</p>
    <div class="callout why small"><div class="label">How it works</div><ul>
      <li>Uses <strong>your own</strong> Anthropic API key (create one at console.anthropic.com → API keys). Any usage is billed to <strong>your</strong> Anthropic account — never to the person who shared this site.</li>
      <li>This site has no key of its own and no server: your key is saved only in this browser and sent only to Anthropic. Nobody else can see or use it, and it gives you no access to anyone else's Claude account.</li>
      <li>API keys are separate from a Claude.ai subscription. Tip: set a monthly spend limit in the Anthropic Console.</li>
      <li>Don't use this on a shared or public computer. Click "Forget key" when done.</li></ul></div>
    <label class="sk-field">API key<input type="password" name="key" placeholder="sk-ant-…" value="${esc(key)}" autocomplete="off"></label>
    <label class="sk-field">Model<select name="model">${MODELS.map(([id, l]) => `<option value="${id}" ${id === model ? "selected" : ""}>${l}</option>`).join("")}</select></label>
    <div class="btns"><button class="btn" data-save>Save</button>${key ? '<button class="btn ghost" data-forget>Forget key</button>' : ""}<button class="btn ghost" data-back>Back</button></div>`;
  body.querySelector("[data-save]").addEventListener("click", () => {
    const k = body.querySelector("[name=key]").value.trim();
    if (k && !/^sk-ant-/.test(k)) { alert("That doesn't look like an Anthropic API key (it should start with sk-ant-)."); return; }
    if (k) store.set("sk:key", k); else store.del("sk:key");
    store.set("sk:model", body.querySelector("[name=model]").value);
    askTab();
  });
  body.querySelector("[data-forget]")?.addEventListener("click", () => { store.del("sk:key"); chat.history = []; askTab(); });
  body.querySelector("[data-back]").addEventListener("click", () => askTab());
}

// ---------------------------------------------------------------- Listen: audio overview read aloud
function script() {
  const lines = [`Audio overview: ${plain(kb.title)}.`, "First, the whole lecture in six sentences."];
  kb.summary.forEach((s) => lines.push(plain(s.text)));
  kb.brief.forEach((b) => {
    if (!b.hy.length) return;
    lines.push(`${b.part.replace("·", ":")}. The high-yield points.`);
    b.hy.forEach((h) => lines.push(plain(h)));
    if (b.traps.length) { lines.push("Watch out for this trap."); lines.push(plain(b.traps[0])); }
  });
  lines.push("That's the overview. Open the flashcards or the quiz to lock it in.");
  return lines;
}
function listenTab() {
  const lines = script(), voices = speechSynthesis?.getVoices().filter((v) => v.lang.startsWith("en")) || [];
  if (!window.speechSynthesis) { body.innerHTML = '<p class="muted">Your browser does not support read-aloud. The script is below.</p>' + lines.map((l) => `<p>${esc(l)}</p>`).join(""); return; }
  body.innerHTML = `<p class="small muted">A spoken walkthrough of the summary and every part's high-yield points (about ${Math.round(lines.join(" ").split(" ").length / 150)} min). Uses your device's voice; nothing leaves your browser.</p>
    <div class="sk-row"><button class="btn" data-play>▶ Play</button><button class="btn ghost" data-stop>■ Stop</button>
    <select data-rate>${[0.9, 1, 1.15, 1.3, 1.5].map((r) => `<option value="${r}" ${r === store.get("sk:rate", 1.15) ? "selected" : ""}>${r}×</option>`).join("")}</select></div>
    ${voices.length ? `<select data-voice class="sk-voice">${voices.map((v, i) => `<option value="${i}" ${v.name === store.get("sk:voice", "") ? "selected" : ""}>${esc(v.name)}</option>`).join("")}</select>` : ""}
    <div class="sk-script">${lines.map((l, i) => `<p data-line="${i}">${esc(l)}</p>`).join("")}</div>`;
  let i = 0, playing = false;
  const playBtn = body.querySelector("[data-play]");
  const say = () => {
    if (i >= lines.length) { playing = false; playBtn.textContent = "▶ Play"; i = 0; return; }
    body.querySelectorAll("[data-line]").forEach((p) => p.classList.toggle("now", +p.dataset.line === i));
    body.querySelector(`[data-line="${i}"]`).scrollIntoView({ block: "center", behavior: "smooth" });
    const u = new SpeechSynthesisUtterance(lines[i]);
    u.rate = +body.querySelector("[data-rate]").value;
    const v = voices[+body.querySelector("[data-voice]")?.value];
    if (v) u.voice = v;
    u.onend = () => { if (playing) { i++; say(); } };
    speechSynthesis.speak(u);
  };
  playBtn.addEventListener("click", () => {
    if (playing && !speechSynthesis.paused) { speechSynthesis.pause(); playBtn.textContent = "▶ Resume"; return; }
    if (playing) { speechSynthesis.resume(); playBtn.textContent = "❚❚ Pause"; return; }
    playing = true; playBtn.textContent = "❚❚ Pause"; say();
  });
  body.querySelector("[data-stop]").addEventListener("click", () => { playing = false; speechSynthesis.cancel(); i = 0; playBtn.textContent = "▶ Play"; });
  body.querySelector("[data-rate]").addEventListener("change", (e) => store.set("sk:rate", +e.target.value));
  body.querySelector("[data-voice]")?.addEventListener("change", (e) => store.set("sk:voice", voices[+e.target.value].name));
  body.querySelectorAll("[data-line]").forEach((p) => p.addEventListener("click", () => { speechSynthesis.cancel(); i = +p.dataset.line; playing = true; playBtn.textContent = "❚❚ Pause"; say(); }));
}

// ---------------------------------------------------------------- Flashcards: Leitner boxes (spaced repetition)
function allCards() {
  return [...kb.cards.map((c, i) => ({ ...c, id: i })), ...store.get(`sk:mycards:${kb.lecture}`, []).map((c, i) => ({ ...c, id: "m" + i, mine: true }))];
}
function cardsTab() {
  const key = `sk:fc:${kb.lecture}`, boxes = store.get(key, {}), cards = allCards();
  const queue = shuffle(cards.map((c, i) => i)).sort((a, b) => (boxes[cards[a].id] || 1) - (boxes[cards[b].id] || 1));
  let n = 0;
  const counts = () => [1, 2, 3, 4, 5].map((b) => cards.filter((c) => (boxes[c.id] || 1) === b).length);
  const draw = () => {
    const c = cards[queue[n % queue.length]], i = c.id, cs = counts();
    body.innerHTML = `<div class="sk-boxes">${cs.map((k, b) => `<div><strong>${k}</strong><span>${["New", "Learning", "Familiar", "Strong", "Mastered"][b]}</span></div>`).join("")}</div>
      <div class="sk-card" tabindex="0"><div class="sk-face"><div class="small muted">Card ${(n % queue.length) + 1} of ${queue.length} · tap to flip</div><div class="sk-q">${c.mine ? '<span class="tag mine">MINE</span>' : ""}${tags(c)}${md(c.q)}</div></div>
      <div class="sk-face back"><div class="sk-a">${md(c.a)}</div>${cite(c.src)}</div></div>
      <div class="sk-row sk-rate" hidden><button class="btn ghost" data-again>Again</button><button class="btn" data-good>Got it</button></div>
      <p class="small muted">"Again" sends a card back to New; "Got it" moves it up a box. Lower boxes come up first. Saved in this browser.</p>`;
    const card = body.querySelector(".sk-card"), rate = body.querySelector(".sk-rate");
    const flip = () => { card.classList.toggle("flipped"); rate.hidden = !card.classList.contains("flipped"); };
    card.addEventListener("click", flip);
    card.addEventListener("keydown", (e) => { if (e.key === " " || e.key === "Enter") { e.preventDefault(); flip(); } });
    const grade = (up) => { boxes[i] = up ? Math.min(5, (boxes[i] || 1) + 1) : 1; store.set(key, boxes); n++; draw(); };
    body.querySelector("[data-again]").addEventListener("click", () => grade(false));
    body.querySelector("[data-good]").addEventListener("click", () => grade(true));
    card.focus();
  };
  if (!cards.length) { body.innerHTML = '<p class="muted">No flashcards for this lecture yet.</p>'; return; }
  draw();
}

// ---------------------------------------------------------------- Quiz: 10 random questions
function quizTab(list) {
  const qs = Array.isArray(list) ? list : shuffle([...kb.quiz]).slice(0, 10);
  let n = 0, score = 0;
  const draw = () => {
    if (n >= qs.length) {
      body.innerHTML = `<div class="sk-done"><div class="sk-score">${score}/${qs.length}</div><p>${score >= 0.8 * qs.length ? "Strong — you're ready for this lecture." : score >= 0.6 * qs.length ? "Close. Review the parts you missed, then go again." : "Worth another pass through the guide first."}</p><button class="btn" data-again>New quiz</button></div>`;
      body.querySelector("[data-again]").addEventListener("click", () => quizTab());
      return;
    }
    const q = qs[n];
    body.innerHTML = `<div class="sk-row small"><span class="muted" style="flex:1">Question ${n + 1} of ${qs.length} · score ${score}</span><a href="#" data-full>⛶ Full screen</a></div><div class="small muted">${esc(q.label)}</div><div class="sk-stem">${md(q.stem)}</div>
      <div class="opts">${Object.entries(q.options).map(([L, t]) => `<button class="opt" data-l="${L}"><span class="L">${L}</span><span>${md(t)}</span></button>`).join("")}</div><div class="sk-why"></div>`;
    body.querySelector("[data-full]").addEventListener("click", (e) => {
      e.preventDefault();
      const key = "miss:" + kb.lecture;
      window.dpasQuiz?.setup(kb.quiz, { title: "Quiz", missed: store.get(key, []), onAnswer: (x, L, ok) => { const m = new Set(store.get(key, [])); ok ? m.delete(x.id) : m.add(x.id); store.set(key, [...m]); if (ok) store.set("done:" + kb.lecture, [...new Set([...store.get("done:" + kb.lecture, []), x.id])]); } });
    });
    body.querySelectorAll(".opt").forEach((b) => b.addEventListener("click", () => {
      if (body.querySelector(".opt.right")) return;
      const ok = b.dataset.l === q.answer;
      if (ok) score++;
      if (q.id) { const key = "miss:" + kb.lecture, m = new Set(store.get(key, [])); ok ? m.delete(q.id) : m.add(q.id); store.set(key, [...m]); if (ok) store.set("done:" + kb.lecture, [...new Set([...store.get("done:" + kb.lecture, []), q.id])]); }
      body.querySelectorAll(".opt").forEach((o) => { if (o.dataset.l === q.answer) o.classList.add("right"); });
      if (!ok) b.classList.add("wrong");
      const whys = q.whys ? Object.entries(q.whys).filter(([L]) => L !== q.answer).map(([L, w]) => `<li><strong>${L}.</strong> ${md(w)}</li>`).join("") : "";
      body.querySelector(".sk-why").innerHTML = `<div class="callout clin"><div class="label">${ok ? "Correct" : "Answer: " + q.answer}</div>${md(q.why)}${cite(q.src)}${whys ? `<ul class="why-list">${whys}</ul>` : ""}</div>
        <button class="btn" data-next>${n + 1 < qs.length ? "Next question" : "See score"}</button>`;
      body.querySelector("[data-next]").addEventListener("click", () => { n++; draw(); body.scrollTop = 0; });
    }));
  };
  draw();
}

// ---------------------------------------------------------------- Mind map: lecture → parts → sections → facts
function mapTab() {
  body.innerHTML = `<p class="small muted">Tap a branch to open it. Tap a part name to jump to it in the guide.</p>
    <div class="sk-map"><div class="sk-root">${esc(kb.title)}</div><ul>${kb.tree.map((p) => `<li><details><summary><a href="#${esc(p.anchor)}" data-go="${esc(p.anchor)}">${esc(p.name)}</a></summary>
      <ul>${p.children.map((s) => `<li><details><summary>${esc(s.name)} <span class="muted small">${s.facts.length}</span></summary><ul>${s.facts.map((f) => `<li>${md(f)}</li>`).join("")}</ul></details></li>`).join("")}</ul></details></li>`).join("")}</ul></div>`;
  body.querySelectorAll("[data-go]").forEach((a) => a.addEventListener("click", (e) => { e.preventDefault(); goTo(a.dataset.go); }));
}

// ---------------------------------------------------------------- Briefing doc
function briefTab() {
  const html = `<h3>Briefing: ${esc(kb.title)}</h3><h4>In six sentences</h4><ol>${kb.summary.map((s) => `<li>${md(s.text)}${cite(s.src)}</li>`).join("")}</ol>` +
    kb.brief.map((b) => `<h4>${esc(b.part)}</h4><ul>${b.hy.map((h) => `<li>${md(h)}</li>`).join("")}${b.traps.map((t) => `<li class="trap">⚠ ${md(t)}</li>`).join("")}</ul>`).join("");
  body.innerHTML = `<div class="sk-row"><button class="btn ghost" data-print>Print / save as PDF</button></div><div class="sk-brief">${html}</div>`;
  body.querySelector("[data-print]").addEventListener("click", () => {
    const w = window.open("", "_blank");
    if (!w) return;
    w.document.write(`<!doctype html><meta charset="utf-8"><title>Briefing</title><style>body{font:14px/1.5 -apple-system,Segoe UI,Roboto,sans-serif;max-width:720px;margin:32px auto;padding:0 16px}.cite{color:#666;font-size:11px;margin-left:4px}h4{margin:18px 0 6px}.trap{color:#a00}</style>${html}`);
    w.document.close(); w.focus(); w.print();
  });
}

// ---------------------------------------------------------------- FAQ: suggested questions → Ask
function faqTab() {
  body.innerHTML = `<p class="small muted">Questions worth being able to answer. Tap one to search your materials${store.get("sk:key", "") ? " and ask Claude" : ""}.</p>` +
    kb.faq.map((q, i) => `<button class="sk-faq" data-i="${i}">${esc(q)}</button>`).join("");
  body.querySelectorAll(".sk-faq").forEach((b) => b.addEventListener("click", () => show("ask", kb.faq[+b.dataset.i])));
}


// ---------------------------------------------------------------- highlight toolbar: act on any selected text
// Select text anywhere in the guide → Explain · Source · Quiz me · Card · Save · Copy
const refsOf = (src) => {
  const out = { slides: [], notes: [], pages: [], sg: [] };
  const sg = String(src || "").match(/SG\s*U\d+-[A-Z]\d*/g) || [];
  out.sg = sg.map((x) => x.replace(/SG\s*/, ""));
  const rest = String(src || "").replace(/SG\s*U\d+-[A-Z]\d*/g, "");
  for (const m of rest.matchAll(/S\s*(\d+)(?:\s*[-–]\s*S?\s*(\d+))?(\s*\(notes\))?/g)) {
    for (let n = +m[1]; n <= +(m[2] || m[1]); n++) (m[3] ? out.notes : out.slides).push(n);
  }
  for (const m of rest.matchAll(/pp?\.\s*(\d+)(?:\s*[-–]\s*(\d+))?/g)) out.pages.push(+m[1]);
  out.slides = [...new Set([...out.slides, ...out.notes])];
  return out;
};
function selectionContext() {
  const sel = getSelection();
  if (!sel || sel.isCollapsed || !sel.rangeCount) return null;
  const text = sel.toString().replace(/\s+/g, " ").trim();
  const node = sel.getRangeAt(0).commonAncestorContainer;
  const el = node.nodeType === 1 ? node : node.parentElement;
  if (!text || text.length < 2 || text.length > 1500 || !el || el.closest(".sk-panel, .nav, .sk-sel, input, textarea, .sk-fab")) return null;
  const block = el.closest("li, tr, .callout, figcaption, .stem, .opt, .flow, p, h2, h3, td") || el;
  const section = el.closest("section[id]");
  let src = [...block.querySelectorAll(".cite")].map((c) => c.textContent).join("; ");
  const clone = block.cloneNode(true);
  clone.querySelectorAll(".cite, .tag, .jump").forEach((x) => x.remove());
  const blockText = clone.textContent.replace(/\s+/g, " ").trim();
  let guessed = false;
  if (!src) { const hit = search(text + " " + blockText, 1)[0]; if (hit) { src = hit.src; guessed = true; } }
  return { text, blockText: blockText.slice(0, 700), src, guessed, anchor: section?.id || "", where: section?.querySelector("h2")?.textContent || kb.title, rect: sel.getRangeAt(0).getBoundingClientRect() };
}
let bar, ctx;
function hideBar() { bar?.classList.remove("show"); }
function showBar() {
  ctx = selectionContext();
  if (!ctx) { hideBar(); return; }
  if (!bar) {
    bar = document.createElement("div");
    bar.className = "sk-sel noprint";
    bar.innerHTML = [["explain", "✦", "Explain"], ["source", "📍", "Source"], ["quiz", "❓", "Quiz me"], ["compare", "⇄", "Compare"], ["card", "🃏", "Card"], ["save", "🖍", "Save"], ["copy", "⧉", "Copy"]]
      .map(([a, i, l]) => `<button data-act="${a}" title="${l}"><span>${i}</span>${l}</button>`).join("");
    bar.addEventListener("mousedown", (e) => e.preventDefault());  // keep the selection while clicking
    bar.addEventListener("click", (e) => { const b = e.target.closest("[data-act]"); if (b && ctx) { act(b.dataset.act, ctx); hideBar(); } });
    document.body.append(bar);
  }
  const r = ctx.rect, w = bar.offsetWidth || 420;
  bar.style.left = Math.max(8, Math.min(innerWidth - w - 8, r.left + r.width / 2 - w / 2)) + "px";
  bar.style.top = (r.top + scrollY - 52 < scrollY + 60 ? r.bottom + scrollY + 10 : r.top + scrollY - 52) + "px";
  bar.classList.add("show");
}
document.addEventListener("mouseup", () => setTimeout(showBar, 10));
document.addEventListener("keyup", (e) => { if (e.shiftKey) setTimeout(showBar, 10); });
document.addEventListener("touchend", () => setTimeout(showBar, 350));
document.addEventListener("selectionchange", () => { if (getSelection()?.isCollapsed) hideBar(); });

function toast(msg) {
  const t = Object.assign(document.createElement("div"), { className: "sk-toast", textContent: msg });
  document.body.append(t);
  setTimeout(() => t.remove(), 2200);
}
const quote = (c) => `“${c.text.length > 90 ? c.text.slice(0, 88) + "…" : c.text}”`;
function act(a, c) {
  if (a === "copy") {
    navigator.clipboard?.writeText(`${c.text} (${c.src || kb.title})`).then(() => toast("Copied with citation"), () => toast("Couldn't copy"));
    return;
  }
  if (a === "save") { saveNote(c); return; }
  if (a === "compare") {
    if (!cmpA || cmpA.text === c.text) { cmpA = c; getSelection()?.removeAllRanges(); toast(`Comparing “${c.text.slice(0, 30)}” — now highlight the second thing`); return; }
    const pair = { a: cmpA, b: c };
    cmpA = null;
    if (!panel.classList.contains("open")) open();
    show("compare", pair);
    return;
  }
  if (!panel.classList.contains("open")) open();
  const ai = !!store.get("sk:key", "");
  const where = `It appears in "${c.where}": "${c.blockText}" (${c.src || "no citation"})`;
  if (a === "explain") {
    if (ai) askAI(`Explain this from the lecture in more depth: why it's true, how it connects to the rest of the lecture, and why it matters clinically. Stay within the source and cite.\n\nHighlighted: "${c.text}"\n${where}`, `Explain ${quote(c)}`);
    else show("explain", c);
  } else if (a === "quiz") {
    if (ai) askAI(`Ask me one PANCE-style question (options A–E) that tests this, from the source only. Don't give the answer until I reply.\n\nHighlighted: "${c.text}"\n${where}`, `Quiz me on ${quote(c)}`);
    else {
      const t = new Set(terms(c.text + " " + c.blockText));
      const scored = kb.quiz.map((q) => [terms(q.stem + " " + Object.values(q.options).join(" ")).filter((w) => t.has(w)).length, q]).filter(([n]) => n >= 2).sort((x, y) => y[0] - x[0]).slice(0, 5).map(([, q]) => q);
      if (scored.length) show("quiz", scored);
      else { show("explain", c); toast("No matching practice questions — turn on AI chat to generate one"); }
    }
  } else if (a === "source") show("source", c);
  else if (a === "card") show("card", c);
}

// Explain without AI: the full fact, its source, and the closest related facts
function explainFree(c) {
  if (!c) { askTab(); return; }
  const related = search(c.text + " " + c.blockText, 7).filter((h) => !c.blockText.includes(plain(h.text).slice(0, 40))).slice(0, 5);
  body.innerHTML = `<h4>You highlighted</h4><blockquote class="sk-quote">${esc(c.text)}</blockquote>
    <h4>In context</h4><div class="sk-hit"><div class="small muted">${esc(c.where)}</div>${esc(c.blockText)}${cite(c.src)}</div>
    <div class="sk-row"><button class="btn ghost" data-src>📍 See the source</button></div>
    <h4>Related in this lecture</h4>${related.map((h) => `<div class="sk-hit"><div class="small muted">${esc(h.where)}</div><div>${tags(h)}${md(h.text)}${cite(h.src)}</div><a href="#${esc(h.anchor)}" data-go="${esc(h.anchor)}" class="small">Go to section →</a></div>`).join("") || '<p class="muted">Nothing closely related.</p>'}
    <p class="small muted">Want a real explanation in your own words? <a href="#" data-ai>Turn on AI chat</a>.</p>`;
  body.querySelector("[data-src]").addEventListener("click", () => show("source", c));
  body.querySelector("[data-ai]").addEventListener("click", (e) => { e.preventDefault(); show("ask"); aiSettings(); });
  body.querySelectorAll("[data-go]").forEach((a) => a.addEventListener("click", (e) => { e.preventDefault(); goTo(a.dataset.go); }));
}

// Source: the actual slide image(s), speaker notes, textbook page, study-guide item
function sourceView(c) {
  if (!c) { askTab(); return; }
  const r = refsOf(c.src);
  const slides = r.slides.slice(0, 4).map((n) => {
    const s = kb.slides[n] || {};
    return `<div class="sk-slide"><div class="small muted">Slide ${n}${s.title ? " · " + esc(s.title) : ""}</div>
      ${s.img ? `<img src="slides/S${n}.jpg" alt="Lecture slide ${n}" loading="lazy" data-zoom>` : ""}
      ${r.notes.includes(n) && s.notes ? `<div class="sk-notes"><strong>Speaker notes:</strong> ${esc(s.notes)}</div>` : ""}</div>`;
  }).join("");
  const pages = r.pages.map((pg) => `<div class="sk-tb"><div><strong>Katzung p. ${pg}</strong><div class="small muted">${esc(kb.textbook.book)}</div></div>
      <button class="btn" data-page="${pg}">Open my PDF</button><a class="btn ghost" href="${esc(kb.textbook.am)}" target="_blank" rel="noopener">AccessMedicine</a></div>`).join("");
  const sg = r.sg.map((id) => kb.sg[id] ? `<div class="sk-hit"><div class="small muted">Course study guide · ${esc(id)}</div><div><strong>Q:</strong> ${esc(kb.sg[id].question)}</div><div><strong>A:</strong> ${esc(kb.sg[id].answer)}</div></div>` : "").join("");
  body.innerHTML = `<h4>Where this comes from</h4><blockquote class="sk-quote">${esc(c.text)}</blockquote>
    ${c.src ? `<p class="small muted">${c.guessed ? "No citation right here — closest match in the lecture: " : "Cited as: "}${cite(c.src)}</p>` : '<p class="muted">Not covered in materials.</p>'}
    ${slides}${pages}${sg}
    ${kb.deck ? `<p class="small muted">Want the whole deck? <a href="${esc(kb.deck)}">Download the slides (.pptx)</a>.</p>` : ""}`;
  body.querySelectorAll("[data-page]").forEach((b) => b.addEventListener("click", () => window.dpasTextbook?.open(+b.dataset.page, kb.textbook.offset)));
  body.querySelectorAll("[data-zoom]").forEach((img) => img.addEventListener("click", () => {
    const z = Object.assign(document.createElement("div"), { className: "sk-zoom" });
    z.innerHTML = `<img src="${img.src}" alt="">`;
    z.addEventListener("click", () => z.remove());
    document.body.append(z);
  }));
}

// Card: turn the highlight into your own flashcard
function newCard(c) {
  if (!c) { cardsTab(); return; }
  const m = c.blockText.match(/^([^:]{2,60}):\s*(.+)$/);
  const front = m && c.blockText.includes(c.text) ? m[1] : c.text;
  const back = m ? m[2] : c.blockText;
  body.innerHTML = `<h4>New flashcard</h4>
    <label class="sk-field">Front<textarea rows="2" name="q">${esc(front)}</textarea></label>
    <label class="sk-field">Back<textarea rows="4" name="a">${esc(back.replace(/\s*(S\d+.*|p\. \d+.*)$/, ""))}</textarea></label>
    <div class="sk-row"><button class="btn" data-save>Add to my flashcards</button><button class="btn ghost" data-cancel>Cancel</button></div>
    <p class="small muted">It joins this lecture's deck as a <span class="tag mine">MINE</span> card. Saved in this browser.</p>`;
  body.querySelector("[data-save]").addEventListener("click", () => {
    const key = `sk:mycards:${kb.lecture}`, mine = store.get(key, []);
    mine.push({ q: body.querySelector("[name=q]").value.trim(), a: body.querySelector("[name=a]").value.trim(), src: c.src });
    store.set(key, mine); toast("Flashcard added"); cardsTab();
  });
  body.querySelector("[data-cancel]").addEventListener("click", () => cardsTab());
}

// Notes: saved highlights, re-highlighted on the page, with your own comments
const notesKey = () => `sk:notes:${kb.lecture}`;
function markOnPage(n) {
  const sec = document.getElementById(n.anchor) || document.body;
  const walk = document.createTreeWalker(sec, NodeFilter.SHOW_TEXT);
  for (let t; (t = walk.nextNode());) {
    const i = t.data.indexOf(n.text);
    if (i >= 0 && !t.parentElement.closest(".hl, .sk-panel")) {
      const r = document.createRange(); r.setStart(t, i); r.setEnd(t, i + n.text.length);
      const mk = Object.assign(document.createElement("mark"), { className: "hl" }); mk.dataset.note = n.id;
      r.surroundContents(mk); return mk;
    }
  }
  const blk = [...sec.querySelectorAll("li, td, p, figcaption")].find((b) => b.textContent.replace(/\s+/g, " ").includes(n.text));
  if (blk) { blk.classList.add("hl-block"); blk.dataset.note = n.id; }
  return blk;
}
function saveNote(c) {
  const notes = store.get(notesKey(), []);
  const n = { id: Date.now().toString(36), text: c.text, src: c.src, anchor: c.anchor, where: c.where, note: "" };
  notes.push(n); store.set(notesKey(), notes);
  getSelection()?.removeAllRanges();
  markOnPage(n);
  toast("Saved to Notes");
  if (tab === "notes" && panel.classList.contains("open")) notesTab();
}
function notesTab() {
  const notes = store.get(notesKey(), []);
  if (!notes.length) { body.innerHTML = '<p class="muted">No notes yet. Highlight text in the guide and tap <strong>🖍 Save</strong>. Your highlights stay on the page and collect here.</p>'; return; }
  body.innerHTML = `<div class="sk-row"><button class="btn ghost" data-export>Copy all as text</button></div>` + notes.map((n) =>
    `<div class="sk-note" data-id="${n.id}"><div class="small muted">${esc(n.where)}</div><mark class="hl">${esc(n.text)}</mark>${cite(n.src)}
     <textarea rows="2" placeholder="Add your own note…">${esc(n.note)}</textarea>
     <div class="sk-row small"><a href="#" data-jump>Show on page</a><a href="#" data-src>Source</a><a href="#" data-del>Delete</a></div></div>`).join("");
  const upd = (id, f) => { const all = store.get(notesKey(), []); const i = all.findIndex((x) => x.id === id); if (i >= 0) { f(all, i); store.set(notesKey(), all); } };
  body.querySelectorAll(".sk-note").forEach((el) => {
    const id = el.dataset.id, n = notes.find((x) => x.id === id);
    el.querySelector("textarea").addEventListener("input", (e) => upd(id, (all, i) => { all[i].note = e.target.value; }));
    el.querySelector("[data-jump]").addEventListener("click", (e) => { e.preventDefault(); const mk = document.querySelector(`[data-note="${id}"]`); if (mk) { mk.scrollIntoView({ behavior: "smooth", block: "center" }); mk.classList.add("flash"); setTimeout(() => mk.classList.remove("flash"), 1600); } else goTo(n.anchor); });
    el.querySelector("[data-src]").addEventListener("click", (e) => { e.preventDefault(); show("source", { ...n, blockText: n.text }); });
    el.querySelector("[data-del]").addEventListener("click", (e) => {
      e.preventDefault(); upd(id, (all, i) => all.splice(i, 1));
      document.querySelectorAll(`[data-note="${id}"]`).forEach((mk) => { if (mk.tagName === "MARK") mk.replaceWith(...mk.childNodes); else mk.classList.remove("hl-block"); });
      notesTab();
    });
  });
  body.querySelector("[data-export]").addEventListener("click", () => {
    const txt = notes.map((n) => `• ${n.text} (${n.src || n.where})${n.note ? "\n  ↳ " + n.note : ""}`).join("\n");
    navigator.clipboard?.writeText(`${kb.title} — my notes\n\n${txt}`).then(() => toast("Notes copied"));
  });
}

// ---------------------------------------------------------------- citation peek: hover S23 / p. 47 to preview, click for the full source
let tip;
function citeTip(c) {
  const r = refsOf(c.textContent);
  if (!r.slides.length && !r.pages.length && !r.sg.length) return;
  tip ||= Object.assign(document.createElement("div"), { className: "cite-tip noprint" });
  const n = r.slides[0], s = kb.slides[n] || {};
  tip.innerHTML = (n ? `${s.img ? `<img src="slides/S${n}.jpg" alt="">` : ""}<div><strong>Slide ${n}</strong>${s.title ? " · " + esc(s.title) : ""}${r.slides.length > 1 ? `<span class="muted"> +${r.slides.length - 1} more</span>` : ""}</div>` : "") +
    (r.pages.length ? `<div>📖 Katzung p. ${r.pages.join(", ")}</div>` : "") +
    (r.sg.length ? `<div>Study guide ${r.sg.join(", ")}</div>` : "") + '<div class="muted small">Click for the full source</div>';
  document.body.append(tip);
  const b = c.getBoundingClientRect(), w = 280;
  tip.style.left = Math.max(8, Math.min(innerWidth - w - 8, b.left + b.width / 2 - w / 2)) + "px";
  tip.style.top = (b.top > 260 ? b.top + scrollY - tip.offsetHeight - 8 : b.bottom + scrollY + 8) + "px";
  tip.classList.add("show");
}
document.addEventListener("mouseover", (e) => { const c = e.target.closest?.(".cite"); if (c && kb) citeTip(c); });
document.addEventListener("mouseout", (e) => { if (e.target.closest?.(".cite")) tip?.classList.remove("show"); });
document.addEventListener("click", (e) => {
  const c = e.target.closest?.(".cite");
  if (!c || !kb || c.closest(".sk-panel")) return;
  const block = c.closest("li, tr, .callout, figcaption, p, td, .q") || c.parentElement;
  const clone = block.cloneNode(true);
  clone.querySelectorAll(".cite, .tag, .jump").forEach((x) => x.remove());
  const text = clone.textContent.replace(/\s+/g, " ").trim().slice(0, 300);
  tip?.classList.remove("show");
  if (!panel.classList.contains("open")) open();
  show("source", { text, blockText: text, src: c.textContent, where: c.closest("section[id]")?.querySelector("h2")?.textContent || kb.title });
});

// Compare: highlight one thing, then another → side by side from every lecture (and a Claude table if AI is on)
let cmpA = null;
async function compareView(pair) {
  if (!pair) { askTab(); return; }
  const { a, b } = pair;
  body.innerHTML = '<p class="muted">Gathering facts from every lecture…</p>';
  const idx = await ensureAll();
  const label = (h) => h.where.split(" · ").slice(-1)[0];
  const side = (x) => search(x.text + " " + x.text, 8, idx);
  const A = side(a), B = side(b);
  // use the words that DIFFER between the two (e.g., "competitive" vs "noncompetitive"), so a shared word doesn't match everything
  const ta0 = new Set(terms(a.text)), tb0 = new Set(terms(b.text));
  const ta = [...ta0].filter((w) => !tb0.has(w)), tb = [...tb0].filter((w) => !ta0.has(w));
  const both = idx.chunks.filter((ch) => { const t = new Set(terms(ch.text)); return (ta.length ? ta : [...ta0]).some((w) => t.has(w)) && (tb.length ? tb : [...tb0]).some((w) => t.has(w)); }).slice(0, 6);
  const groups = [...new Set([...A, ...B].map(label))];
  const cell = (hs, g) => hs.filter((h) => label(h) === g).slice(0, 2).map((h) => `<div class="cmp-fact">${tags(h)}${md(h.text)}${cite(h.src)}</div>`).join("") || '<span class="muted small">—</span>';
  body.innerHTML = `<h4>Compare</h4><div class="cmp-head"><span>${esc(a.text.slice(0, 60))}</span><span>vs</span><span>${esc(b.text.slice(0, 60))}</span></div>
    ${store.get("sk:key", "") ? '<button class="btn" data-ai-cmp style="margin:6px 0 12px">✦ Build a comparison table with Claude</button>' : '<p class="small muted">Turn on AI chat in Ask for a ready-made comparison table.</p>'}
    ${both.length ? `<h4>Mentioned together</h4>${both.map((h) => `<div class="sk-hit"><div class="small muted">${esc(h.where)}</div>${tags(h)}${md(h.text)}${cite(h.src)} <a href="${esc(hitLink(h))}" data-go="${esc(h.anchor)}" class="small">Open →</a></div>`).join("")}` : ""}
    <h4>Side by side</h4><div class="cmp-table">${groups.map((g) => `<div class="cmp-row"><div class="cmp-label">${esc(g)}</div><div>${cell(A, g)}</div><div>${cell(B, g)}</div></div>`).join("") || '<p class="muted">Not covered in materials.</p>'}</div>`;
  wireGo(body);
  body.querySelector("[data-ai-cmp]")?.addEventListener("click", () => {
    scope = "all"; store.set("sk:scope", "all");
    askAI(`Compare "${a.text}" with "${b.text}" in a compact markdown-free table-like list: one line per feature (definition, mechanism, clinical use, examples, key exam trap), "A: … | B: …", using only the course sources and citing each fact. Say "Not covered in materials" for any gap.`, `Compare “${a.text.slice(0, 30)}” vs “${b.text.slice(0, 30)}”`);
  });
}

// ---------------------------------------------------------------- start
fetch("kb.json").then((r) => r.json()).then((data) => { kb = data; buildIndex(); mount(); store.get(notesKey(), []).forEach(markOnPage); }).catch(() => { /* no Sidekick data on this page */ });
