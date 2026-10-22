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
let index;
function buildIndex() {
  const docs = kb.chunks.map((c) => terms(c.text + " " + c.where));
  const df = new Map();
  docs.forEach((d) => new Set(d).forEach((t) => df.set(t, (df.get(t) || 0) + 1)));
  const avg = docs.reduce((n, d) => n + d.length, 0) / docs.length;
  index = { docs, df, avg, N: docs.length };
}
function search(q, k = 6) {
  const qt = [...new Set(terms(q))];
  if (!qt.length) return [];
  const { docs, df, avg, N } = index;
  return docs.map((d, i) => {
    let s = 0;
    for (const t of qt) {
      const tf = d.filter((w) => w === t || (t.length > 3 && w.startsWith(t))).length;
      if (!tf) continue;
      const idf = Math.log(1 + (N - (df.get(t) || 0) + 0.5) / ((df.get(t) || 0) + 0.5));
      s += idf * (tf * 2.2) / (tf + 1.2 * (0.25 + 0.75 * d.length / avg));
    }
    return [s, i];
  }).filter(([s]) => s > 0).sort((a, b) => b[0] - a[0]).slice(0, k).map(([, i]) => kb.chunks[i]);
}

// ---------------------------------------------------------------- panel shell
const TABS = [["ask", "Ask"], ["listen", "Listen"], ["cards", "Flashcards"], ["quiz", "Quiz"], ["map", "Mind map"], ["brief", "Briefing"], ["faq", "FAQ"]];
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
  if (store.get("sk:open", false)) open();
}
function open() { panel.classList.add("open"); document.body.classList.add("sk-on"); store.set("sk:open", true); show(tab); }
function close() { panel.classList.remove("open"); document.body.classList.remove("sk-on"); store.set("sk:open", false); speechSynthesis?.cancel(); }
function show(id, arg) {
  tab = id; store.set("sk:tab", id);
  panel.querySelectorAll("[data-tab]").forEach((b) => b.setAttribute("aria-selected", b.dataset.tab === id));
  if (id !== "listen") speechSynthesis?.cancel();
  ({ ask: askTab, listen: listenTab, cards: cardsTab, quiz: quizTab, map: mapTab, brief: briefTab, faq: faqTab })[id](arg);
  body.scrollTop = 0;
}

// ---------------------------------------------------------------- Ask: search + optional AI chat
const chat = { history: [], busy: false };
function askTab(prefill) {
  const key = store.get("sk:key", "");
  body.innerHTML = `<form class="sk-ask"><input name="q" placeholder="Ask about this lecture…" autocomplete="off" value="${esc(prefill || "")}"><button class="btn">Ask</button></form>
    <div class="sk-ai-line small">${key ? `AI chat <strong>on</strong> · ${esc(MODELS.find((m) => m[0] === store.get("sk:model", MODELS[0][0]))?.[1].split(" —")[0])} · <a href="#" data-ai>settings</a>${chat.history.length ? ' · <a href="#" data-clear>new chat</a>' : ""}`
      : `Searching your study materials. <a href="#" data-ai>Turn on AI chat</a> (optional, uses your own Claude API key).`}</div>
    <div class="sk-thread"></div><div class="sk-results"></div>`;
  const form = body.querySelector("form");
  body.querySelector("[data-ai]").addEventListener("click", (e) => { e.preventDefault(); aiSettings(); });
  body.querySelector("[data-clear]")?.addEventListener("click", (e) => { e.preventDefault(); chat.history = []; askTab(); });
  renderThread();
  form.addEventListener("submit", (e) => { e.preventDefault(); const q = form.q.value.trim(); if (q) ask(q); form.q.value = ""; });
  if (prefill) ask(prefill);
  else form.q.focus();
}
function renderThread() {
  const t = body.querySelector(".sk-thread");
  if (!t) return;
  t.innerHTML = chat.history.map((m) => m.role === "user" ? `<div class="sk-msg me">${esc(m.content)}</div>`
    : `<div class="sk-msg ai">${md(m.content).replace(/\n/g, "<br>")}</div>`).join("");
}
function ask(q) {
  const hits = search(q);
  body.querySelector(".sk-results").innerHTML = `<h4>From your study materials</h4>` + (hits.length ? hits.map((h) =>
    `<div class="sk-hit"><div class="small muted">${esc(h.where)}</div><div>${tags(h)}${md(h.text)}${cite(h.src)}</div>
     <a href="#${esc(h.anchor)}" data-go="${esc(h.anchor)}" class="small">Go to section →</a></div>`).join("")
    : `<p class="muted">Nothing matched. Try different words (e.g., a drug name or term) — or it may be <strong>not covered in materials</strong>.</p>`);
  body.querySelectorAll("[data-go]").forEach((a) => a.addEventListener("click", (e) => { e.preventDefault(); goTo(a.dataset.go); }));
  if (store.get("sk:key", "")) aiAnswer(q);
}
async function loadSource() {
  if (!sourceText && kb.source) sourceText = await fetch(kb.source).then((r) => r.text()).catch(() => "");
  return sourceText;
}
async function aiAnswer(q) {
  if (chat.busy) return;
  chat.busy = true;
  chat.history.push({ role: "user", content: q });
  renderThread();
  const t = body.querySelector(".sk-thread");
  const out = document.createElement("div");
  out.className = "sk-msg ai";
  out.innerHTML = '<span class="muted">Thinking…</span>';
  t.append(out);
  let text = "";
  try {
    Anthropic ||= (await import(SDK_URL)).default;
    const client = new Anthropic({ apiKey: store.get("sk:key", ""), dangerouslyAllowBrowser: true });
    const source = await loadSource();
    const model = store.get("sk:model", MODELS[0][0]);
    const stream = client.beta.messages.stream({
      model,
      max_tokens: 4000,
      ...(model === "claude-haiku-5-5" ? {} : { betas: ["server-side-fallback-2026-07-01"], fallbacks: "default" }),
      output_config: { effort: "low" },
      system: [
        { type: "text", text: "You are Sidekick, a study assistant for a physician assistant student in clinical pharmacology. Answer only from the lecture source below. Cite every fact the way the source does, e.g. (S12), (S12 notes), (p. 17), (SG U1-R3). If the source does not cover something, say \"Not covered in materials\" rather than using outside knowledge. Keep answers short and scannable: a direct answer first, then up to 5 bullets. Use **bold** for the single most testable point. When asked to quiz, ask one PANCE-style question at a time and wait for the answer." },
        { type: "text", text: `LECTURE SOURCE (${kb.title}):\n\n${source}`, cache_control: { type: "ephemeral" } },
      ],
      messages: chat.history.map(({ role, content }) => ({ role, content })),
    });
    stream.on("text", (d) => { text += d; out.innerHTML = md(text).replace(/\n/g, "<br>"); });
    const msg = await stream.finalMessage();
    if (msg.stop_reason === "refusal") text = text || "Claude declined to answer this one. Try rephrasing the question.";
    if (msg.stop_reason === "max_tokens") text += "\n\n(Answer cut off — ask me to continue.)";
    chat.history.push({ role: "assistant", content: text });
    renderThread();
  } catch (err) {
    console.error("Sidekick chat:", err);
    chat.history.pop();
    const is = (cls) => Anthropic && err instanceof Anthropic[cls];
    const why = is("AuthenticationError") ? "Your API key was rejected — check it in settings."
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
      <li>Uses <strong>your own</strong> Anthropic API key (get one at console.anthropic.com). Usage is billed to your key.</li>
      <li>The key is saved only in this browser and sent only to Anthropic — never to this site or anyone else.</li>
      <li>Don't use this on a shared or public computer. Click "Forget key" when done.</li></ul></div>
    <label class="sk-field">API key<input type="password" name="key" placeholder="sk-ant-…" value="${esc(key)}" autocomplete="off"></label>
    <label class="sk-field">Model<select name="model">${MODELS.map(([id, l]) => `<option value="${id}" ${id === model ? "selected" : ""}>${l}</option>`).join("")}</select></label>
    <div class="btns"><button class="btn" data-save>Save</button>${key ? '<button class="btn ghost" data-forget>Forget key</button>' : ""}<button class="btn ghost" data-back>Back</button></div>`;
  body.querySelector("[data-save]").addEventListener("click", () => {
    const k = body.querySelector("[name=key]").value.trim();
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
function cardsTab() {
  const key = `sk:fc:${kb.lecture}`, boxes = store.get(key, {});
  const queue = shuffle(kb.cards.map((c, i) => i)).sort((a, b) => (boxes[a] || 1) - (boxes[b] || 1));
  let n = 0;
  const counts = () => [1, 2, 3, 4, 5].map((b) => kb.cards.filter((_, i) => (boxes[i] || 1) === b).length);
  const draw = () => {
    const i = queue[n % queue.length], c = kb.cards[i], cs = counts();
    body.innerHTML = `<div class="sk-boxes">${cs.map((k, b) => `<div><strong>${k}</strong><span>${["New", "Learning", "Familiar", "Strong", "Mastered"][b]}</span></div>`).join("")}</div>
      <div class="sk-card" tabindex="0"><div class="sk-face"><div class="small muted">Card ${(n % queue.length) + 1} of ${queue.length} · tap to flip</div><div class="sk-q">${tags(c)}${md(c.q)}</div></div>
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
  if (!kb.cards.length) { body.innerHTML = '<p class="muted">No flashcards for this lecture yet.</p>'; return; }
  draw();
}

// ---------------------------------------------------------------- Quiz: 10 random questions
function quizTab() {
  const qs = shuffle([...kb.quiz]).slice(0, 10);
  let n = 0, score = 0;
  const draw = () => {
    if (n >= qs.length) {
      body.innerHTML = `<div class="sk-done"><div class="sk-score">${score}/${qs.length}</div><p>${score >= 8 ? "Strong — you're ready for this lecture." : score >= 6 ? "Close. Review the parts you missed, then go again." : "Worth another pass through the guide first."}</p><button class="btn" data-again>New quiz</button></div>`;
      body.querySelector("[data-again]").addEventListener("click", quizTab);
      return;
    }
    const q = qs[n];
    body.innerHTML = `<div class="small muted">Question ${n + 1} of ${qs.length} · ${esc(q.label)} · score ${score}</div><div class="sk-stem">${md(q.stem)}</div>
      <div class="opts">${Object.entries(q.options).map(([L, t]) => `<button class="opt" data-l="${L}"><span class="L">${L}</span><span>${md(t)}</span></button>`).join("")}</div><div class="sk-why"></div>`;
    body.querySelectorAll(".opt").forEach((b) => b.addEventListener("click", () => {
      if (body.querySelector(".opt.right")) return;
      const ok = b.dataset.l === q.answer;
      if (ok) score++;
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

// ---------------------------------------------------------------- start
fetch("kb.json").then((r) => r.json()).then((data) => { kb = data; buildIndex(); mount(); }).catch(() => { /* no Sidekick data on this page */ });
