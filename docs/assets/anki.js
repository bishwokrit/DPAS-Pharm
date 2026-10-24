// Anki generator: choose content, depth and card styles; preview; export as an Anki package (.apkg), Anki text,
// CSV, Quizlet, or a printable sheet. Everything runs in this browser from the study guides' own content.
(function () {
  const app = document.getElementById("ak-app");
  if (!app) return;
  const v = document.documentElement.dataset.v || "";
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const strip = (h) => String(h ?? "").replace(/<[^>]+>/g, "").replace(/&nbsp;/g, " ").replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').trim();
  const store = {
    get(k, d) { try { const x = localStorage.getItem(k); return x === null ? d : JSON.parse(x); } catch { return d; } },
    set(k, x) { try { localStorage.setItem(k, JSON.stringify(x)); } catch { /* private mode */ } },
  };
  const hash = (s) => { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return h >>> 0; };

  // ---- what each source is, in the order a student thinks about them
  const SRC = [
    ["hy", "High-yield", "The points the lecture stressed", 1], ["cram", "Cram sheet", "Prompt → answer pairs", 1], ["drug", "Drugs", "Class and every cited fact", 1],
    ["def", "Definitions", "Key terms, both directions", 2], ["pearl", "Clinical pearls", "What it means for the patient", 2], ["trap", "Exam traps", "Where students slip", 2],
    ["hook", "Memory hooks", "The why behind a fact", 2], ["selftest", "Self-test questions", "Lecture vignettes", 2], ["exam", "Practice-exam questions", "Board-style, with explanations", 2],
    ["how", "How it works", "Mechanisms and processes", 3], ["example", "Examples", "Drugs and cases named in lecture", 3], ["table", "Comparison tables", "One card per cell", 3],
    ["flow", "Step-by-step flows", "Sequences in order", 3],
  ];
  const SRC_OF = { "High-yield": "hy", "Cram sheet": "cram", "Drug class": "drug", "Drug fact": "drug", Definition: "def", "Clinical pearl": "pearl", "Exam trap": "trap",
    "Memory hook": "hook", "Self-test question": "selftest", "Practice-exam question": "exam", "How it works": "how", Example: "example", "Comparison table": "table", "Step by step": "flow" };
  const DEPTH = [[1, "Essentials", "High-yield, cram sheet and drug classes. The fastest review."],
    [2, "Standard", "Adds definitions, pearls, traps, hooks and practice questions. The exam-ready deck."],
    [3, "Comprehensive", "Everything: mechanisms, examples, tables, flows and textbook detail."]];
  const TYPES = [
    ["cloze", "Cloze", "Fill in the blank inside the real sentence", "Steady state is reached in about <span class=ak-blank>[…]</span> half-lives."],
    ["basic", "Basic", "Question on the front, answer on the back", "<b>Pharmacokinetics</b><hr>What the body does to the drug (ADME)"],
    ["reversed", "Basic + reversed", "Term → definition and definition → term", "Term ⇄ definition, two cards"],
    ["typein", "Type the answer", "Short answers you type, checked by Anki", "Antidote for acetaminophen? <span class=ak-input>N-acetylcysteine</span>"],
    ["mcq", "Multiple choice", "Exam-style stem with A–E and the explanation", "A 68-year-old… <span class=ak-ch>A</span><span class=ak-ch>B</span><span class=ak-ch>C</span>"],
  ];
  const FORMATS = [
    ["apkg", "Anki package", ".apkg · styled cards, decks, tags. Double-click to import.", "apkg"],
    ["txt", "Anki text", ".txt · imports into your own note types (File → Import)", "txt"],
    ["csv", "CSV", ".csv · Front, Back, Tags for any flashcard app", "csv"],
    ["quizlet", "Quizlet", ".txt · paste into Quizlet's import box", "txt"],
    ["print", "Print", "A two-column sheet: fold down the middle to self-test", null],
  ];

  const DEF = { lids: null, parts: {}, depth: 2, src: null, tb: true, types: ["cloze", "basic", "mcq"], every: false, clozeMode: "separate",
    extra: { source: true, where: true, explain: true }, tags: { unit: true, lecture: true, part: true, kind: true }, deck: "PA–S Rx::Clinical Pharmacology I",
    split: "lecture", order: "course", q: "", missed: false, format: "apkg" };
  let S = { ...DEF, ...store.get("ak:cfg", {}) };
  const save = () => store.set("ak:cfg", { ...S, q: "" });
  const srcForDepth = (d) => Object.fromEntries(SRC.map(([k, , , lv]) => [k, lv <= d]));
  let D = null, preview = 0, flipped = new Set(), open = new Set();

  fetch(`data.json?v=${v}`).then((r) => r.json()).then((data) => {
    D = data;
    if (!S.lids) S.lids = D.lectures.map((l) => l.id);
    if (!S.src) S.src = srcForDepth(S.depth);
    D.lectures.forEach((l) => { if (!S.parts[l.id]) S.parts[l.id] = l.parts.map((p) => p.n); });
    draw();
  }).catch(() => (app.innerHTML = '<p class="muted">Couldn\'t load the course content. Refresh to try again.</p>'));

  // ---------------------------------------------------------------- selection → items → notes
  const missed = (it) => {
    if (it.kind !== "mcq") return false;
    if (it.exam) return store.get(`exam:${it.exam}:log`, []).some((e) => e.id === it.raw) && store.get(`exam:${it.exam}:v1`, { answers: {} }).answers[it.raw] !== it.answer;
    return store.get(`miss:${it.lid}`, []).includes(it.raw);
  };
  function chosen() {
    const lids = new Set(S.lids), q = S.q.toLowerCase().trim();
    return D.items.filter((it) => {
      const src = SRC_OF[it.label];
      if (!S.src[src] || it.depth > S.depth || (it.tb && !S.tb)) return false;
      const inLec = it.lids ? it.lids.some((l) => lids.has(l)) : lids.has(it.lid);
      if (!inLec) return false;
      if (it.part && !(S.parts[it.lid] || []).includes(it.part)) return false;
      if (S.missed && !missed(it)) return false;
      if (q && !strip((it.text || "") + " " + (it.front || "") + " " + (it.back || "") + " " + (it.stem || "") + " " + (it.drug || "") + " " + (it.table || "")).toLowerCase().includes(q)) return false;
      return true;
    });
  }
  const lecOf = (id) => D.lectures.find((l) => l.id === id);
  const partName = (it) => (it.part ? lecOf(it.lid)?.parts.find((p) => p.n === it.part)?.name : "");
  const tagOf = (s) => s.replace(/[^\w:-]+/g, "_").replace(/_+/g, "_").replace(/^_|_$/g, "");
  function meta(it) {
    const l = lecOf(it.lid), where = [it.drug ? `Drug: ${it.drug}` : null, l ? `${l.id} ${l.title.replace(/^.*—\s*/, "")}` : null, partName(it) ? `Part ${it.part}: ${partName(it)}` : null, it.label].filter(Boolean).join(" · ");
    const src = [S.extra.where ? where : null, S.extra.source && it.src ? `Source: ${it.src}${it.tb ? " (textbook)" : ""}` : null].filter(Boolean).join("<br>");
    const tags = ["PAS_Rx"];
    if (S.tags.unit) tags.push(`PAS_Rx::Unit_${it.unit}`);
    if (S.tags.lecture && l) tags.push(`PAS_Rx::${l.id}`);
    if (S.tags.part && it.part && partName(it)) tags.push(tagOf(`PAS_Rx::${l.id}::Part_${it.part}_${partName(it)}`));
    if (S.tags.kind) tags.push(tagOf(`type::${it.label}`));
    if (it.tb) tags.push("textbook");
    if (it.drug) tags.push(tagOf(`drug::${it.drug}`));
    let deck = S.deck.trim() || "PA–S Rx";
    if (S.split !== "none" && l) deck += `::${l.id} · ${l.title.replace(/^.*—\s*/, "")}`;
    if (S.split === "part" && l) deck += `::${it.part ? `Part ${it.part} · ${partName(it)}` : it.kind === "mcq" ? "Questions" : it.drug ? "Drugs" : "Cram sheet"}`;
    return { src, tags, deck };
  }
  const renum = (c) => { if (S.clozeMode !== "together") return c; return c.replace(/\{\{c\d+::/g, "{{c1::"); };
  function notesFor(it) {
    const m = meta(it), out = [], T = new Set(S.types), base = { id: it.id, tags: m.tags, deck: m.deck, src: m.src };
    if (it.kind === "mcq") {
      const choices = Object.entries(it.options).map(([k, t]) => `<li><b>${k}</b> ${t}</li>`).join("");
      const ans = `${it.answer} — ${it.options[it.answer]}`, why = S.extra.explain ? it.why : "";
      if (T.has("mcq")) out.push({ ...base, model: "mcq", f: { Question: it.stem, Choices: choices, Answer: ans, Explanation: why } });
      else if (T.has("basic")) out.push({ ...base, model: "basic", f: { Front: `${it.stem}<ol class="choices" type="A">${choices}</ol>`, Back: ans, Extra: why } });
      return out;
    }
    const fullText = it.kind === "table" ? `${it.table}` : it.kind === "flow" ? "" : it.text;
    const back = it.kind === "flow" ? `<ol>${it.steps.map((s) => `<li>${esc(s)}</li>`).join("")}</ol>` : esc(it.back || "");
    const can = { cloze: !!it.cloze, reversed: !!(it.rev && it.front), typein: !!(it.front && it.back && it.back.length <= 45 && it.kind !== "flow"), basic: !!(it.front && it.back) };
    const make = {
      cloze: () => ({ ...base, model: "cloze", f: { Text: renum(it.cloze), Extra: "" } }),
      reversed: () => ({ ...base, model: "reversed", f: { Front: esc(it.front), Back: back, Extra: "" } }),
      typein: () => ({ ...base, model: "typein", f: { Front: esc(it.front), Back: esc(it.back), Extra: S.extra.explain && fullText && strip(fullText) !== `${it.front}: ${it.back}` ? fullText : "" } }),
      basic: () => ({ ...base, model: "basic", f: { Front: esc(it.front), Back: back, Extra: S.extra.explain && fullText && it.kind !== "pair" ? fullText : "" } }),
    };
    for (const k of ["cloze", "reversed", "typein", "basic"]) {
      if (T.has(k) && can[k]) { out.push(make[k]()); if (!S.every) break; }
    }
    return out;
  }
  const cardsIn = (n) => n.model === "reversed" ? 2 : n.model === "cloze" ? new Set([...n.f.Text.matchAll(/\{\{c(\d+)::/g)].map((x) => x[1])).size || 1 : 1;
  function build() {
    let items = chosen();
    if (S.order === "shuffle") items = items.map((x) => [hash(x.id + "s" + Date.now() % 997), x]).sort((a, b) => a[0] - b[0]).map((x) => x[1]);
    const notes = items.flatMap(notesFor);
    return { items, notes, cards: notes.reduce((a, n) => a + cardsIn(n), 0), skipped: items.filter((it) => !notesFor(it).length).length };
  }

  // ---------------------------------------------------------------- page
  const chk = (on) => `<span class="ak-chk${on ? " on" : ""}"></span>`;
  function draw() {
    const B = build(), lids = new Set(S.lids), units = [...new Set(D.lectures.map((l) => l.unit))];
    const countSrc = (k) => D.items.filter((it) => SRC_OF[it.label] === k && (it.lids ? it.lids.some((l) => lids.has(l)) : lids.has(it.lid))).length;
    const byType = B.notes.reduce((a, n) => ((a[n.model] = (a[n.model] || 0) + 1), a), {});
    const TN = { cloze: "Cloze", basic: "Basic", reversed: "Reversed", typein: "Type-in", mcq: "Multiple choice" };
    app.innerHTML = `<div class="ak-main">
      <section class="ak-step"><div class="ak-sh"><span class="ak-n">1</span><div><h3>What to cover</h3><p>Whole lectures or single parts. Everything stays cited.</p></div>
        <div class="ak-quick"><button data-all>All</button><button data-none>None</button></div></div>
        ${units.map((u) => `<div class="ak-unit"><div class="ak-uh">Unit ${u} · ${esc(D.units[u] || "")}</div>${D.lectures.filter((l) => l.unit === u).map((l) => {
          const on = lids.has(l.id), ps = S.parts[l.id] || [];
          return `<div class="ak-lec${on ? " on" : ""}"><button class="ak-lrow" data-lec="${l.id}">${chk(on)}<span><strong>${l.id} · ${esc(l.title.replace(/^.*—\s*/, ""))}</strong><small>${esc(l.title.split(" — ")[0])} · ${l.parts.length} parts</small></span></button>
            <button class="ak-exp${open.has(l.id) ? " open" : ""}" data-exp="${l.id}" aria-label="Choose parts of ${l.id}">${ps.length < l.parts.length ? `${ps.length}/${l.parts.length} parts` : "All parts"}<i></i></button>
            ${open.has(l.id) ? `<div class="ak-parts">${l.parts.map((p) => `<button data-part="${l.id}:${p.n}" ${on ? "" : "disabled"}>${chk(ps.includes(p.n))}<span>Part ${p.n} · ${esc(p.name)}</span></button>`).join("")}</div>` : ""}</div>`;
        }).join("")}</div>`).join("")}
        <div class="ak-filter"><input type="search" id="ak-q" placeholder="Only cards about… (e.g. CYP3A4, half-life, warfarin)" value="${esc(S.q)}" aria-label="Filter by keyword">
        <button class="ak-tog${S.missed ? " on" : ""}" data-missed>${chk(S.missed)}Only questions I've missed</button></div></section>

      <section class="ak-step"><div class="ak-sh"><span class="ak-n">2</span><div><h3>How deep</h3><p>Pick a level, then fine-tune the sources.</p></div></div>
        <div class="ak-depth">${DEPTH.map(([d, t, s]) => `<button class="${S.depth === d ? "on" : ""}" data-depth="${d}"><strong>${t}</strong><span>${s}</span><i class="ak-bars">${"<b></b>".repeat(d)}${"<b class=off></b>".repeat(3 - d)}</i></button>`).join("")}</div>
        <div class="ak-srcs">${SRC.map(([k, t, s, lv]) => { const off = lv > S.depth; return `<button class="ak-src${S.src[k] && !off ? " on" : ""}" data-src="${k}" ${off ? "disabled title=\"Raise the depth to include\"" : ""}>${chk(S.src[k] && !off)}<span><strong>${t}</strong><small>${s} · ${countSrc(k)}</small></span></button>`; }).join("")}</div>
        <button class="ak-tog${S.tb ? " on" : ""}" data-tb>${chk(S.tb)}Include textbook-only detail (marked TB in the guides)</button></section>

      <section class="ak-step"><div class="ak-sh"><span class="ak-n">3</span><div><h3>Card styles</h3><p>Each fact becomes the best style you allow, in this order.</p></div></div>
        <div class="ak-types">${TYPES.map(([k, t, s, ex]) => `<button class="ak-type${S.types.includes(k) ? " on" : ""}" data-type="${k}">${chk(S.types.includes(k))}<span><strong>${t}</strong><small>${s}</small><em class="ak-ex">${ex}</em></span></button>`).join("")}</div>
        <div class="ak-row"><button class="ak-tog${S.every ? " on" : ""}" data-every>${chk(S.every)}Make every allowed style for each fact (more cards)</button>
        <div class="seg ak-seg" data-k="clozeMode"><button data-v="separate" class="${S.clozeMode === "separate" ? "on" : ""}">Cloze: one card per blank</button><button data-v="together" class="${S.clozeMode === "together" ? "on" : ""}">All blanks on one card</button></div></div></section>

      <section class="ak-step"><div class="ak-sh"><span class="ak-n">4</span><div><h3>On the back, and how it's filed</h3><p>Context makes cards stick; tags make them findable.</p></div></div>
        <div class="ak-row">${[["source", "Slide / page citation"], ["where", "Lecture and part"], ["explain", "Explanations and full sentence"]].map(([k, t]) => `<button class="ak-tog${S.extra[k] ? " on" : ""}" data-extra="${k}">${chk(S.extra[k])}${t}</button>`).join("")}</div>
        <div class="ak-row"><span class="ak-lab">Tags</span>${[["unit", "Unit"], ["lecture", "Lecture"], ["part", "Part"], ["kind", "Card source"]].map(([k, t]) => `<button class="ak-tog${S.tags[k] ? " on" : ""}" data-tag="${k}">${chk(S.tags[k])}${t}</button>`).join("")}</div>
        <div class="ak-row"><label class="ak-deck"><span class="ak-lab">Deck</span><input id="ak-deck" value="${esc(S.deck)}" aria-label="Deck name"></label>
        <div class="seg ak-seg" data-k="split"><button data-v="none" class="${S.split === "none" ? "on" : ""}">One deck</button><button data-v="lecture" class="${S.split === "lecture" ? "on" : ""}">Subdeck per lecture</button><button data-v="part" class="${S.split === "part" ? "on" : ""}">…and per part</button></div>
        <div class="seg ak-seg" data-k="order"><button data-v="course" class="${S.order === "course" ? "on" : ""}">Course order</button><button data-v="shuffle" class="${S.order === "shuffle" ? "on" : ""}">Shuffled</button></div></div></section>
    </div>

    <aside class="ak-side"><div class="ak-sum">
      <div class="ak-big"><strong>${B.notes.length.toLocaleString()}</strong><span>notes</span><strong>${B.cards.toLocaleString()}</strong><span>cards</span></div>
      <div class="ak-mix">${Object.entries(byType).map(([k, n]) => `<span class="ak-pill t-${k}">${TN[k]} ${n}</span>`).join("") || '<span class="muted small">Nothing selected yet.</span>'}</div>
      ${B.skipped ? `<p class="ak-note">${B.skipped} item${B.skipped === 1 ? "" : "s"} only fit a style you've turned off.${S.types.includes("cloze") ? "" : " Turning on Cloze includes most of them."}</p>` : ""}
      <div class="ak-fmts">${FORMATS.map(([k, t, s]) => `<button class="${S.format === k ? "on" : ""}" data-fmt="${k}"><strong>${t}</strong><small>${s}</small></button>`).join("")}</div>
      <button class="btn ak-go" data-go ${B.notes.length ? "" : "disabled"}>${S.format === "print" ? "Open printable sheet" : `Download ${B.cards.toLocaleString()} cards`}</button>
      <details class="ak-help"><summary>How to import</summary>${S.format === "apkg" ? "<p>Double-click the file, or in Anki: <b>File → Import</b>. Decks, tags and card styling come with it. Re-importing an updated deck updates the same notes instead of duplicating them.</p>"
        : S.format === "txt" ? "<p>Anki: <b>File → Import</b>, pick the file. It uses Anki's built-in Basic, Basic (and reversed card), Basic (type in the answer) and Cloze note types, and fills deck and tags automatically.</p>"
        : S.format === "csv" ? "<p>Columns: Front, Back, Tags. Cloze cards show the blanks as […] on the front and the full sentence on the back.</p>"
        : S.format === "quizlet" ? "<p>Quizlet: <b>Create → Import</b>, paste the file's contents, choose <b>Tab</b> between term and definition and <b>New line</b> between cards.</p>" : "<p>Prints front and back side by side. Fold the page down the middle and quiz yourself.</p>"}</details>
    </div>
    <div class="ak-prev"><div class="ak-ph"><strong>Preview</strong><span>${B.notes.length ? `${Math.min(B.notes.length, preview + 1)} of ${B.notes.length} · tap to flip` : ""}</span>
      <span class="ak-nav"><button data-pv="-1" aria-label="Previous card" ${preview <= 0 ? "disabled" : ""}>‹</button><button data-pv="1" aria-label="Next card" ${preview >= B.notes.length - 1 ? "disabled" : ""}>›</button></span></div>
      ${B.notes.length ? cardHTML(B.notes[Math.min(preview, B.notes.length - 1)]) : '<div class="ak-card empty">Your cards appear here.</div>'}</div></aside>`;
    wire(B);
  }
  function cardHTML(n) {
    const flip = flipped.has(n.id + n.model), src = n.src ? `<div class="ak-c-src">${n.src}</div>` : "";
    const tags = `<div class="ak-c-tags">${n.tags.slice(1).map((t) => `<i>${esc(t.replace(/^PAS_Rx::/, ""))}</i>`).join("")}</div>`;
    let front = "", back = "";
    if (n.model === "cloze") {
      const first = (n.f.Text.match(/\{\{c(\d+)::/) || [, "1"])[1];
      front = n.f.Text.replace(/\{\{c(\d+)::(.+?)\}\}/g, (m, k, t) => (k === first ? '<span class="ak-blank">[…]</span>' : t));
      back = n.f.Text.replace(/\{\{c(\d+)::(.+?)\}\}/g, (m, k, t) => (k === first ? `<span class="ak-cl">${t}</span>` : t));
    } else if (n.model === "mcq") { front = `${n.f.Question}<ol class="choices" type="A">${n.f.Choices}</ol>`; back = `<div class="ak-ans">${n.f.Answer}</div>${n.f.Explanation ? `<div class="ak-c-ex">${n.f.Explanation}</div>` : ""}`; }
    else if (n.model === "typein") { front = `${n.f.Front}<div class="ak-input">Type your answer</div>`; back = `<div class="ak-ans">${n.f.Back}</div>${n.f.Extra ? `<div class="ak-c-ex">${n.f.Extra}</div>` : ""}`; }
    else { front = n.f.Front; back = `${n.f.Back}${n.f.Extra ? `<div class="ak-c-ex">${n.f.Extra}</div>` : ""}`; }
    return `<button class="ak-card${flip ? " flip" : ""}" data-flip="${esc(n.id + n.model)}"><div class="ak-face">${front}</div>${flip ? `<hr><div class="ak-face back">${back}</div>${src}` : '<div class="ak-tap">Show answer</div>'}${tags}</button>`;
  }
  function wire(B) {
    const on = (sel, fn) => app.querySelectorAll(sel).forEach((b) => b.addEventListener("click", (e) => { fn(b, e); save(); draw(); }));
    on("[data-all]", () => (S.lids = D.lectures.map((l) => l.id)));
    on("[data-none]", () => (S.lids = []));
    on("[data-lec]", (b) => { const id = b.dataset.lec; S.lids = S.lids.includes(id) ? S.lids.filter((x) => x !== id) : [...S.lids, id]; preview = 0; });
    on("[data-exp]", (b) => (open.has(b.dataset.exp) ? open.delete(b.dataset.exp) : open.add(b.dataset.exp)));
    on("[data-part]", (b) => { const [l, n] = b.dataset.part.split(":"), p = S.parts[l] || []; S.parts[l] = p.includes(+n) ? p.filter((x) => x !== +n) : [...p, +n].sort((a, c) => a - c); preview = 0; });
    on("[data-missed]", () => (S.missed = !S.missed));
    on("[data-depth]", (b) => { S.depth = +b.dataset.depth; S.src = { ...srcForDepth(S.depth) }; preview = 0; });
    on("[data-src]", (b) => (S.src[b.dataset.src] = !S.src[b.dataset.src]));
    on("[data-tb]", () => (S.tb = !S.tb));
    on("[data-type]", (b) => { const k = b.dataset.type; S.types = S.types.includes(k) ? S.types.filter((x) => x !== k) : [...S.types, k]; preview = 0; });
    on("[data-every]", () => (S.every = !S.every));
    on("[data-extra]", (b) => (S.extra[b.dataset.extra] = !S.extra[b.dataset.extra]));
    on("[data-tag]", (b) => (S.tags[b.dataset.tag] = !S.tags[b.dataset.tag]));
    on(".ak-seg[data-k] button", (b) => (S[b.parentElement.dataset.k] = b.dataset.v));
    on("[data-fmt]", (b) => (S.format = b.dataset.fmt));
    on("[data-pv]", (b) => (preview = Math.max(0, preview + +b.dataset.pv)));
    on("[data-flip]", (b) => (flipped.has(b.dataset.flip) ? flipped.delete(b.dataset.flip) : flipped.add(b.dataset.flip)));
    const q = app.querySelector("#ak-q"); let qt = 0;
    q.addEventListener("input", () => { clearTimeout(qt); qt = setTimeout(() => { S.q = q.value; preview = 0; draw(); const g = app.querySelector("#ak-q"); g.focus(); g.setSelectionRange(g.value.length, g.value.length); }, 220); });
    const dk = app.querySelector("#ak-deck"); dk.addEventListener("change", () => { S.deck = dk.value; save(); draw(); });
    app.querySelector("[data-go]")?.addEventListener("click", (e) => { e.stopPropagation(); exportDeck(build()); });
  }

  // ---------------------------------------------------------------- exports
  const download = (blob, name) => { const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(blob), download: name }); document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 5000); };
  const fileBase = () => `${(S.deck.split("::").pop() || "deck").replace(/[^\w\- ]+/g, "").trim().replace(/\s+/g, "_") || "deck"}_${new Date().toISOString().slice(0, 10)}`;
  const flat = (h) => strip(String(h).replace(/<br\s*\/?>|<\/li>|<\/p>/gi, " ").replace(/<li>/gi, "• ")).replace(/\s+/g, " ").trim();
  const clozePlain = (t, reveal) => t.replace(/\{\{c\d+::(.+?)\}\}/g, (m, x) => (reveal ? x : "[…]"));
  function frontBack(n) {
    if (n.model === "cloze") return [clozePlain(n.f.Text, false), clozePlain(n.f.Text, true) + (n.f.Extra ? `<br>${n.f.Extra}` : "")];
    if (n.model === "mcq") return [`${n.f.Question}<ol type="A">${n.f.Choices}</ol>`, `${n.f.Answer}${n.f.Explanation ? `<br><br>${n.f.Explanation}` : ""}`];
    return [n.f.Front, `${n.f.Back}${n.f.Extra ? `<br><br>${n.f.Extra}` : ""}`];
  }
  async function exportDeck(B) {
    const btn = app.querySelector("[data-go]"), label = btn.textContent;
    btn.disabled = true; btn.textContent = "Building…";
    try {
      if (S.format === "apkg") download(await apkg(B.notes), `${fileBase()}.apkg`);
      else if (S.format === "txt") download(new Blob([ankiText(B.notes)], { type: "text/plain" }), `${fileBase()}_anki.txt`);
      else if (S.format === "csv") download(new Blob(["\ufeff" + csv(B.notes)], { type: "text/csv" }), `${fileBase()}.csv`);
      else if (S.format === "quizlet") download(new Blob([B.notes.map((n) => frontBack(n).map((x) => flat(x).replace(/\t/g, " ")).join("\t")).join("\n")], { type: "text/plain" }), `${fileBase()}_quizlet.txt`);
      else printSheet(B.notes);
      btn.textContent = S.format === "print" ? label : "Downloaded ✓";
    } catch (e) { console.error(e); btn.textContent = "Couldn't build it. Try again"; }
    setTimeout(() => { btn.disabled = false; btn.textContent = label; }, 1800);
  }
  function ankiText(notes) {
    const NT = { basic: "Basic", reversed: "Basic (and reversed card)", typein: "Basic (type in the answer)", cloze: "Cloze", mcq: "Basic" };
    const cell = (s) => String(s).replace(/\t/g, " ").replace(/\r?\n/g, "<br>").replace(/"/g, "&quot;");
    const rows = notes.map((n) => {
      let a, b;
      if (n.model === "cloze") { a = n.f.Text; b = [n.f.Extra, n.src].filter(Boolean).join("<br>"); }
      else { [a, b] = frontBack(n); if (n.src) b += `<br><br><small>${n.src}</small>`; }
      if (n.model === "typein") b = n.f.Back;  // type-in compares against the Back field exactly
      return [NT[n.model], n.deck, a, b, n.tags.join(" ")].map(cell).join("\t");
    });
    return ["#separator:tab", "#html:true", "#notetype column:1", "#deck column:2", "#tags column:5", ...rows].join("\n");
  }
  function csv(notes) {
    const q = (s) => `"${String(s).replace(/"/g, '""')}"`;
    return ["Front,Back,Tags", ...notes.map((n) => { const [a, b] = frontBack(n); return [q(flat(a)), q(flat(b) + (n.src ? ` (${flat(n.src)})` : "")), q(n.tags.join(" "))].join(","); })].join("\r\n");
  }
  function printSheet(notes) {
    const box = document.getElementById("ak-print");
    box.innerHTML = `<h1>${esc(S.deck.split("::").pop())}</h1><p>${notes.length} cards · fold along the line, front on the left</p><table>${notes.map((n) => { const [a, b] = frontBack(n); return `<tr><td>${a}</td><td>${b}${n.src ? `<div class="ak-psrc">${n.src}</div>` : ""}</td></tr>`; }).join("")}</table>`;
    document.body.classList.add("ak-printing");
    const done = () => { document.body.classList.remove("ak-printing"); removeEventListener("afterprint", done); };
    addEventListener("afterprint", done); setTimeout(() => print(), 60);
  }

  // ---------------------------------------------------------------- .apkg (Anki's own format: a SQLite collection in a zip)
  const CSS = `.card{font-family:-apple-system,"SF Pro Text",Inter,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;font-size:20px;line-height:1.5;color:#1d1d1f;background:#fbfbfd;text-align:left;padding:28px 24px;max-width:700px;margin:0 auto}
.nightMode.card,.nightMode .card,.card.nightMode{color:#f5f5f7;background:#141416}
.front{font-weight:600}.back{}b{font-weight:650}hr#answer{border:0;border-top:1px solid rgba(128,128,128,.3);margin:20px 0}
.cloze{font-weight:700;color:#0a84ff}.nightMode .cloze{color:#64d2ff}
.extra{margin-top:16px;font-size:16px;color:#6e6e73}.nightMode .extra{color:#a1a1a6}
.src{margin-top:18px;font-size:12px;letter-spacing:.02em;color:#86868b}
.choices{list-style:none;padding:0;margin:14px 0 0}.choices li{padding:9px 13px;border-radius:12px;background:rgba(127,127,127,.1);margin:7px 0}.choices li b{color:#86868b;margin-right:6px}
.ans{font-weight:700;color:#248a3d}.nightMode .ans{color:#30d158}
input#typeans{font-size:18px;padding:8px 10px;border-radius:10px;border:1px solid rgba(128,128,128,.4);width:100%;box-sizing:border-box;margin-top:14px}
ol{padding-left:22px}`;
  const tail = `{{#Extra}}<div class="extra">{{Extra}}</div>{{/Extra}}{{#Source}}<div class="src">{{Source}}</div>{{/Source}}`;
  const fld = (names) => names.map((name, ord) => ({ font: "Arial", media: [], name, ord, rtl: false, size: 20, sticky: false }));
  const tmpl = (name, ord, qfmt, afmt) => ({ afmt, bafmt: "", bqfmt: "", did: null, name, ord, qfmt });
  const MODELS = {
    basic: { id: 1729500000001, name: "PA–S Rx · Basic", type: 0, flds: ["Front", "Back", "Extra", "Source"], req: [[0, "any", [0]]],
      tmpls: [tmpl("Card 1", 0, '<div class="front">{{Front}}</div>', `{{FrontSide}}<hr id="answer"><div class="back">{{Back}}</div>${tail}`)] },
    reversed: { id: 1729500000002, name: "PA–S Rx · Basic + reversed", type: 0, flds: ["Front", "Back", "Extra", "Source"], req: [[0, "any", [0]], [1, "any", [1]]],
      tmpls: [tmpl("Forward", 0, '<div class="front">{{Front}}</div>', `{{FrontSide}}<hr id="answer"><div class="back">{{Back}}</div>${tail}`),
        tmpl("Reverse", 1, '<div class="front">{{Back}}</div>', `{{FrontSide}}<hr id="answer"><div class="back">{{Front}}</div>${tail}`)] },
    cloze: { id: 1729500000003, name: "PA–S Rx · Cloze", type: 1, flds: ["Text", "Extra", "Source"], req: [[0, "any", [0]]],
      tmpls: [tmpl("Cloze", 0, "{{cloze:Text}}", `{{cloze:Text}}${tail}`)] },
    typein: { id: 1729500000004, name: "PA–S Rx · Type the answer", type: 0, flds: ["Front", "Back", "Extra", "Source"], req: [[0, "any", [0]]],
      tmpls: [tmpl("Card 1", 0, '<div class="front">{{Front}}</div>{{type:Back}}', `<div class="front">{{Front}}</div><hr id="answer">{{type:Back}}${tail}`)] },
    mcq: { id: 1729500000005, name: "PA–S Rx · Multiple choice", type: 0, flds: ["Question", "Choices", "Answer", "Explanation", "Source"], req: [[0, "any", [0]]],
      tmpls: [tmpl("Card 1", 0, '<div class="front">{{Question}}</div><ol class="choices">{{Choices}}</ol>',
        '{{FrontSide}}<hr id="answer"><div class="ans">{{Answer}}</div>{{#Explanation}}<div class="extra">{{Explanation}}</div>{{/Explanation}}{{#Source}}<div class="src">{{Source}}</div>{{/Source}}')] },
  };
  let sqlP = null;
  const sql = () => (sqlP ||= window.initSqlJs({ locateFile: (f) => `../assets/vendor/${f}?v=${v}` }));
  const sha1 = async (s) => [...new Uint8Array(await crypto.subtle.digest("SHA-1", new TextEncoder().encode(s)))].map((b) => b.toString(16).padStart(2, "0")).join("");
  const B91 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!#$%&()*+,-./:;<=>?@[]^_`{|}~";
  const guidOf = (s) => { let h1 = hash(s), h2 = hash(s + "#"), out = ""; for (let i = 0; i < 10; i++) { const x = i < 5 ? h1 : h2; out += B91[x % 91]; i < 5 ? (h1 = Math.floor(h1 / 91) + hash(out)) : (h2 = Math.floor(h2 / 91) + hash(out)); } return out; };
  async function apkg(notes) {
    const SQL = await sql(), db = new SQL.Database(), now = Math.floor(Date.now() / 1000), ms = Date.now();
    db.run(`CREATE TABLE col (id integer primary key, crt integer not null, mod integer not null, scm integer not null, ver integer not null, dty integer not null, usn integer not null, ls integer not null, conf text not null, models text not null, decks text not null, dconf text not null, tags text not null);
      CREATE TABLE notes (id integer primary key, guid text not null, mid integer not null, mod integer not null, usn integer not null, tags text not null, flds text not null, sfld integer not null, csum integer not null, flags integer not null, data text not null);
      CREATE TABLE cards (id integer primary key, nid integer not null, did integer not null, ord integer not null, mod integer not null, usn integer not null, type integer not null, queue integer not null, due integer not null, ivl integer not null, factor integer not null, reps integer not null, lapses integer not null, left integer not null, odue integer not null, odid integer not null, flags integer not null, data text not null);
      CREATE TABLE revlog (id integer primary key, cid integer not null, usn integer not null, ease integer not null, ivl integer not null, lastIvl integer not null, factor integer not null, time integer not null, type integer not null);
      CREATE TABLE graves (usn integer not null, oid integer not null, type integer not null);
      CREATE INDEX ix_notes_usn on notes (usn); CREATE INDEX ix_cards_usn on cards (usn); CREATE INDEX ix_revlog_usn on revlog (usn); CREATE INDEX ix_cards_nid on cards (nid);
      CREATE INDEX ix_cards_sched on cards (did, queue, due); CREATE INDEX ix_revlog_cid on revlog (cid); CREATE INDEX ix_notes_csum on notes (csum);`);
    // decks: every "A::B::C" level needs its own entry
    const deckIds = {}, decks = { 1: deckJSON(1, "Default", now) };
    const ensure = (name) => { const parts = name.split("::"); for (let i = 1; i <= parts.length; i++) { const nm = parts.slice(0, i).join("::"); if (!deckIds[nm]) { deckIds[nm] = 1500000000000 + (hash(nm) % 99999999); decks[deckIds[nm]] = deckJSON(deckIds[nm], nm, now); } } return deckIds[name]; };
    const used = [...new Set(notes.map((n) => n.model))], models = {};
    used.forEach((k) => { const m = MODELS[k]; models[m.id] = { css: CSS, did: 1, flds: fld(m.flds), id: m.id, latexPost: "\\end{document}", latexPre: "\\documentclass[12pt]{article}\n\\special{papersize=3in,5in}\n\\usepackage{amssymb,amsmath}\n\\pagestyle{empty}\n\\setlength{\\parindent}{0in}\n\\begin{document}\n", latexsvg: false, mod: now, name: m.name, req: m.req, sortf: 0, tags: [], tmpls: m.tmpls, type: m.type, usn: -1, vers: [] }; });
    const dconf = { 1: { autoplay: true, id: 1, lapse: { delays: [10], leechAction: 0, leechFails: 8, minInt: 1, mult: 0 }, maxTaken: 60, mod: 0, name: "Default", new: { bury: true, delays: [1, 10], initialFactor: 2500, ints: [1, 4, 7], order: 1, perDay: 20, separate: true }, replayq: true, rev: { bury: true, ease4: 1.3, fuzz: 0.05, ivlFct: 1, maxIvl: 36500, minSpace: 1, perDay: 200 }, timer: 0, usn: 0 } };
    const conf = { activeDecks: [1], curDeck: 1, newSpread: 0, collapseTime: 1200, timeLim: 0, estTimes: true, dueCounts: true, curModel: null, nextPos: notes.length + 1, sortType: "noteFld", sortBackwards: false, addToCur: true };
    notes.forEach((n) => ensure(n.deck));
    db.run("INSERT INTO col VALUES (1, ?, ?, ?, 11, 0, 0, 0, ?, ?, ?, ?, '{}')", [now, ms, ms, JSON.stringify(conf), JSON.stringify(models), JSON.stringify(decks), JSON.stringify(dconf)]);
    const nIns = db.prepare("INSERT INTO notes VALUES (?, ?, ?, ?, -1, ?, ?, ?, ?, 0, '')"), cIns = db.prepare("INSERT INTO cards VALUES (?, ?, ?, ?, ?, -1, 0, 0, ?, 0, 0, 0, 0, 0, 0, 0, 0, '')");
    let cid = ms * 10, due = 0;
    for (let i = 0; i < notes.length; i++) {
      const n = notes[i], m = MODELS[n.model], vals = m.flds.map((f) => (f === "Source" ? n.src || "" : n.f[f] || "")), first = strip(vals[0]);
      const nid = ms + i, csum = parseInt((await sha1(first)).slice(0, 8), 16), did = deckIds[n.deck];
      nIns.run([nid, guidOf(n.id + "|" + n.model), m.id, now, " " + n.tags.join(" ") + " ", vals.join("\x1f"), first, csum]);
      const ords = n.model === "reversed" ? [0, 1] : n.model === "cloze" ? [...new Set([...n.f.Text.matchAll(/\{\{c(\d+)::/g)].map((x) => +x[1] - 1))] : [0];
      due++;
      for (const o of ords) cIns.run([cid++, nid, did, o, now, due]);
    }
    nIns.free(); cIns.free();
    const bytes = db.export(); db.close();
    return zip([["collection.anki2", bytes], ["media", new TextEncoder().encode("{}")]]);
  }
  function deckJSON(id, name, now) { return { collapsed: false, conf: 1, desc: "Built with PA–S Rx from the course study guides. Every card cites its slide or textbook page.", dyn: 0, extendNew: 10, extendRev: 50, id, lrnToday: [0, 0], mod: now, name, newToday: [0, 0], revToday: [0, 0], timeToday: [0, 0], usn: -1 }; }
  const CRC = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
  const crc32 = (b) => { let c = 0xffffffff; for (let i = 0; i < b.length; i++) c = CRC[(c ^ b[i]) & 255] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; };
  function zip(files) {
    const enc = new TextEncoder(), parts = [], central = []; let off = 0;
    for (const [name, data] of files) {
      const nm = enc.encode(name), crc = crc32(data), h = new DataView(new ArrayBuffer(30));
      h.setUint32(0, 0x04034b50, true); h.setUint16(4, 20, true); h.setUint32(14, crc, true); h.setUint32(18, data.length, true); h.setUint32(22, data.length, true); h.setUint16(26, nm.length, true);
      parts.push(new Uint8Array(h.buffer), nm, data);
      const c = new DataView(new ArrayBuffer(46));
      c.setUint32(0, 0x02014b50, true); c.setUint16(4, 20, true); c.setUint16(6, 20, true); c.setUint32(16, crc, true); c.setUint32(20, data.length, true); c.setUint32(24, data.length, true); c.setUint16(28, nm.length, true); c.setUint32(42, off, true);
      central.push(new Uint8Array(c.buffer), nm); off += 30 + nm.length + data.length;
    }
    const size = central.reduce((a, b) => a + b.length, 0), end = new DataView(new ArrayBuffer(22));
    end.setUint32(0, 0x06054b50, true); end.setUint16(8, files.length, true); end.setUint16(10, files.length, true); end.setUint32(12, size, true); end.setUint32(16, off, true);
    return new Blob([...parts, ...central, new Uint8Array(end.buffer)], { type: "application/octet-stream" });
  }
})();
