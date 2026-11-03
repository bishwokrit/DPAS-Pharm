// Drug flashcards, Anki-style: choose the drugs and what each card asks, then study with spaced repetition
// (Again / Hard / Good / Easy, learning steps 1 m and 10 m, SM-2 intervals). Remote-ring friendly: page-turn keys,
// scroll / TikTok swipes, taps and media buttons all work, and every ring button can be re-learned in Ring setup.
// Everything stays in this browser (localStorage: fc:cfg, fc:srs, fc:day, fc:ring).
(function () {
  const app = document.getElementById("fc-app");
  if (!app) return;
  const CFG = JSON.parse(document.getElementById("fc-data").textContent), DR = CFG.drugs;
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const md = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  const store = {
    get(k, d) { try { const x = localStorage.getItem(k); return x === null ? d : JSON.parse(x); } catch { return d; } },
    set(k, x) { try { localStorage.setItem(k, JSON.stringify(x)); } catch { /* private mode */ } },
  };
  const hash = (s) => { let h = 2166136261; for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); } return (h >>> 0).toString(36); };
  const NOT = "Not covered in materials";
  const FIELDS = [["cls", "Drug class"], ["brand", "Brand names"], ["moa", "Mechanism of action"], ["ind", "Indications"], ["contra", "Contraindications"],
    ["ae", "Adverse effects"], ["ix", "Interactions"], ["pt", "Patient factors & traps"], ["extra", "Extra information"]];
  const FACT_FIELDS = ["moa", "ind", "contra", "ae", "ix", "pt", "extra"];
  const LABEL = Object.fromEntries(FIELDS);
  const STYLES = [
    ["whole", "Drug → whole card", "Front: the drug. Back: every field you pick. One card per drug."],
    ["field", "Drug → one field", "Front: “Furosemide · adverse effects?” One small card per drug per field, the way Anki decks are built."],
    ["which", "Fact → which drug?", "Front: a cited fact with the name blanked. Back: the drug (or every drug that shares it)."],
    ["class", "Class → drugs", "Front: a drug class. Back: the drugs in it from your selection."],
  ];
  const brands = (d) => d.a.filter((a) => /^[A-Z]/.test(a) && a !== d.n && !/^NAPQI$/.test(a));
  const lecTitle = (id) => CFG.lectures.find((l) => l.id === id)?.title || id;

  const DEF = { units: [], lids: [], tags: [], sgOnly: false, tbDrugs: true, q: "", styles: ["whole", "field"], fields: ["cls", "moa", "ind", "contra", "ae", "ix", "pt"],
    tbFacts: true, per: 3, cites: true, mol: true, newPer: 20, revPer: 200, order: "course", cram: false, reverse: false };
  let S = { ...DEF, ...store.get("fc:cfg", {}) };
  const save = () => store.set("fc:cfg", { ...S, q: "" });

  // ---------------------------------------------------------------- which drugs
  const tbOnlyDrug = (d) => d.f.length > 0 && d.f.every((f) => f[3]);
  function drugsChosen() {
    const q = S.q.toLowerCase().trim();
    return DR.filter((d) => (!S.units.length || S.units.includes(d.u))
      && (!S.lids.length || d.l.some((l) => S.lids.includes(l)))
      && (!S.tags.length || d.t.some((t) => S.tags.includes(t)))
      && (!S.sgOnly || d.sg) && (S.tbDrugs || !tbOnlyDrug(d))
      && (!q || (d.n + " " + d.a.join(" ") + " " + d.c + " " + d.t.join(" ")).toLowerCase().includes(q)));
  }
  const factsOf = (d, k) => d.f.filter((f) => f[0] === k && (S.tbFacts || !f[3]));

  // ---------------------------------------------------------------- cards (front/back html builders are lazy)
  function cards() {
    const ds = drugsChosen(), out = [];
    const fieldOn = (k) => S.fields.includes(k);
    const hasField = (d, k) => (k === "cls" ? d.c !== NOT : k === "brand" ? brands(d).length > 0 : factsOf(d, k).length > 0);
    for (const d of ds) {
      if (S.styles.includes("whole") && S.fields.some((k) => hasField(d, k))) out.push({ id: "w|" + d.n, kind: "whole", d });
      if (S.styles.includes("field")) for (const [k] of FIELDS) if (fieldOn(k) && hasField(d, k)) {
        out.push({ id: "f|" + d.n + "|" + k, kind: "field", d, k });
        if (S.reverse && k === "cls") out.push({ id: "r|" + d.n, kind: "rcls", d });
      }
    }
    if (S.styles.includes("which")) {
      // a fact shared by several drugs (class-level facts) becomes one card whose answer is all of them
      const by = new Map();
      for (const d of ds) for (const k of FACT_FIELDS) if (fieldOn(k)) for (const f of factsOf(d, k)) {
        const key = k + "|" + f[1];
        if (!by.has(key)) by.set(key, { k, f, ds: [] });
        by.get(key).ds.push(d);
      }
      for (const [key, v] of by) out.push({ id: "q|" + hash(key), kind: "which", k: v.k, f: v.f, ds: v.ds, d: v.ds[0] });
    }
    if (S.styles.includes("class")) {
      const by = new Map();
      for (const d of ds) if (d.c !== NOT) { if (!by.has(d.c)) by.set(d.c, []); by.get(d.c).push(d); }
      for (const [c, list] of by) if (list.length >= 2) out.push({ id: "c|" + hash(c + "|" + list.map((d) => d.n).join(",")), kind: "class", c, ds: list, d: list[0] });
    }
    return out;
  }

  const cite = (s) => (S.cites && s ? ` <span class="cite">${esc(s)}</span>` : "");
  const tb = (f) => (f[3] ? '<span class="tag tb">TB</span>' : "");
  const ul = (fs) => `<ul class="fc-ul">${fs.slice(0, S.per || 99).map((f) => `<li>${tb(f)}${md(f[1])}${cite(f[2])}</li>`).join("")}${S.per && fs.length > S.per ? `<li class="fc-more">+${fs.length - S.per} more on the drug card</li>` : ""}</ul>`;
  const fieldHtml = (d, k) => (k === "cls" ? `<p class="fc-p">${md(d.c)}${cite(d.cs)}</p>` : k === "brand" ? `<p class="fc-p">${brands(d).map(esc).join(", ")}</p>` : ul(factsOf(d, k)));
  const blank = (d, s) => { const re = new RegExp(`\\b(${[d.n, ...d.a].map((x) => x.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|")})\\b`, "gi"); return s.replace(re, "_____"); };
  function faces(c) {
    const d = c.d;
    if (c.kind === "whole") return [`<div class="fc-k">What do you know about</div><div class="fc-name">${esc(d.n)}</div><div class="fc-sub">Unit ${d.u}${S.fields.includes("cls") ? "" : d.c !== NOT ? " · " + esc(d.c) : ""}</div>`,
      `<div class="fc-name sm">${esc(d.n)}</div>${S.fields.map((k) => { const h = k === "cls" ? d.c !== NOT : k === "brand" ? brands(d).length : factsOf(d, k).length; return h ? `<div class="fc-f"><div class="fc-fl">${LABEL[k]}</div>${fieldHtml(d, k)}</div>` : ""; }).join("")}`];
    if (c.kind === "field") return [`<div class="fc-k">${LABEL[c.k]}</div><div class="fc-name">${esc(d.n)}</div><div class="fc-sub">${c.k === "cls" ? "Which class?" : c.k === "brand" ? "Brand names?" : "What does the course teach?"}</div>`,
      `<div class="fc-k">${LABEL[c.k]} · ${esc(d.n)}</div>${fieldHtml(d, c.k)}`];
    if (c.kind === "rcls") return [`<div class="fc-k">Name a drug in this class</div><div class="fc-name md">${md(d.c)}</div>`, `<div class="fc-name">${esc(d.n)}</div>${cite(d.cs)}`];
    if (c.kind === "which") {
      const names = c.ds.map((x) => x.n);
      return [`<div class="fc-k">Which drug? · ${LABEL[c.k]}</div><p class="fc-stem">${tb(c.f)}${md(blank(d, c.ds.reduce((s, x) => blank(x, s), c.f[1])))}</p>${c.ds.length > 1 ? `<div class="fc-sub">${c.ds.length} drugs share this fact</div>` : ""}`,
        `<div class="fc-name ${names.length > 2 ? "md" : ""}">${names.map(esc).join(", ")}</div><div class="fc-sub">${esc(d.c !== NOT ? d.c : "")}</div><p class="fc-p">${md(c.f[1])}${cite(c.f[2])}</p>`];
    }
    return [`<div class="fc-k">Drugs in this class</div><div class="fc-name md">${md(c.c)}</div><div class="fc-sub">${c.ds.length} in your selection</div>`,
      `<div class="fc-k">${md(c.c)}</div><ul class="fc-ul">${c.ds.map((x) => `<li><strong>${esc(x.n)}</strong>${brands(x).length ? ` <span class="muted">(${brands(x).slice(0, 2).map(esc).join(", ")})</span>` : ""}</li>`).join("")}</ul>`];
  }

  // ---------------------------------------------------------------- scheduler (Anki defaults)
  const MIN = 60e3, DAY = 864e5, LEARN = [1, 10], RELEARN = [10];
  let SRS = store.get("fc:srs", {});
  const today = () => { const t = new Date(); t.setHours(4, 0, 0, 0); if (Date.now() < t) t.setDate(t.getDate() - 1); return t.getTime(); };  // Anki's day starts at 4 am
  const dayEnd = () => today() + DAY;
  const dayLog = () => { const L = store.get("fc:day", {}); return L.d === today() ? L : { d: today(), n: 0, r: 0 }; };
  function next(st, g, now = Date.now()) {  // g: 1 again, 2 hard, 3 good, 4 easy → new state
    const s = st ? { ...st } : { t: "new", step: 0, ivl: 0, ease: 2.5, reps: 0, lapses: 0 };
    s.reps++;
    const fuzz = (d) => (d < 3 ? d : Math.round(d * (0.95 + Math.random() * 0.1)));
    const toReview = (ivl) => { s.t = "review"; s.ivl = Math.max(1, fuzz(ivl)); s.due = today() + s.ivl * DAY; delete s.step; return s; };
    if (s.t === "new" || s.t === "learn" || s.t === "relearn") {
      const steps = s.t === "relearn" ? RELEARN : LEARN, step = s.step || 0;
      if (s.t === "new") s.t = "learn";
      if (g === 1) { s.step = 0; s.due = now + steps[0] * MIN; return s; }
      if (g === 2) { s.due = now + (step === 0 && steps.length > 1 ? (steps[0] + steps[1]) / 2 : steps[step]) * MIN; return s; }
      if (g === 4) return toReview(s.t === "relearn" ? Math.max(s.ivl + 1, 1) : 4);
      if (step + 1 < steps.length) { s.step = step + 1; s.due = now + steps[s.step] * MIN; return s; }
      return toReview(s.t === "relearn" ? Math.max(s.ivl, 1) : 1);
    }
    // review
    if (g === 1) { s.lapses++; s.ease = Math.max(1.3, s.ease - 0.2); s.t = "relearn"; s.step = 0; s.ivl = 1; s.due = now + RELEARN[0] * MIN; return s; }
    if (g === 2) { s.ease = Math.max(1.3, s.ease - 0.15); return toReview(Math.max(s.ivl + 1, s.ivl * 1.2)); }
    if (g === 3) return toReview(Math.max(s.ivl + 1, s.ivl * s.ease));
    s.ease += 0.15; return toReview(Math.max(s.ivl + 1, s.ivl * s.ease * 1.3));
  }
  const ivlText = (st, now = Date.now()) => {
    const ms = st.due - now;
    if (st.t === "review") { const d = st.ivl; return d < 30 ? `${d}d` : d < 365 ? `${(d / 30).toFixed(1).replace(/\.0$/, "")}mo` : `${(d / 365).toFixed(1).replace(/\.0$/, "")}y`; }
    return ms < 60 * MIN ? `${Math.max(1, Math.round(ms / MIN))}m` : `${Math.round(ms / 3600e3)}h`;
  };
  const isDue = (st) => st && st.t === "review" && st.due < dayEnd();
  const isLearn = (st) => st && (st.t === "learn" || st.t === "relearn");

  // ---------------------------------------------------------------- remote ring / keyboard / tap input
  // Inputs are named: "key:Space", "wheel:down", "swipe:up", "tap:left|right|any", "media:nexttrack"…
  const ACTIONS = [["show", "Show answer / Good", "The main button"], ["again", "Again", "Didn't know it"], ["hard", "Hard", ""], ["easy", "Easy", ""], ["undo", "Undo", "Take back the last grade"]];
  const RDEF = {
    show: ["key:Space", "key:Enter", "key:NumpadEnter", "key:ArrowRight", "key:ArrowDown", "key:PageDown", "key:MediaTrackNext", "key:MediaPlayPause", "key:AudioVolumeUp", "key:Digit3", "key:Numpad3", "wheel:down", "swipe:up", "swipe:left", "media:nexttrack", "media:play", "media:pause"],
    again: ["key:ArrowLeft", "key:ArrowUp", "key:PageUp", "key:MediaTrackPrevious", "key:AudioVolumeDown", "key:Digit1", "key:Numpad1", "wheel:up", "swipe:down", "swipe:right", "media:previoustrack"],
    hard: ["key:Digit2", "key:Numpad2"], easy: ["key:Digit4", "key:Numpad4"], undo: ["key:KeyZ", "key:Backspace"],
  };
  let RING = { ...RDEF, ...store.get("fc:ring", {}) }, ringOpts = { tapZones: true, media: false, ...store.get("fc:ringopt", {}) };
  const actionOf = (inp) => ACTIONS.map((a) => a[0]).find((a) => (RING[a] || []).includes(inp));
  const inputName = (inp) => {
    const [t, v] = inp.split(":");
    const K = { Space: "Space", Enter: "Enter", ArrowRight: "→", ArrowLeft: "←", ArrowUp: "↑", ArrowDown: "↓", PageDown: "Page Down", PageUp: "Page Up", MediaPlayPause: "Play/Pause", MediaTrackNext: "Next track", MediaTrackPrevious: "Previous track", AudioVolumeUp: "Volume +", AudioVolumeDown: "Volume −", Backspace: "Backspace" };
    if (t === "key") return K[v] || v.replace(/^Key|^Digit/, "").replace(/^Numpad/, "Num ");
    if (t === "wheel") return v === "down" ? "Scroll down" : "Scroll up";
    if (t === "swipe") return `Swipe ${v}`;
    if (t === "media") return { nexttrack: "Media next", previoustrack: "Media previous", play: "Media play", pause: "Media pause" }[v] || v;
    return inp;
  };
  let listener = null, learnFor = null, peek = null, coolUntil = 0;
  const gate = () => { if (Date.now() < coolUntil) return false; coolUntil = Date.now() + 320; return true; };  // rings repeat; one press = one action
  // can the card area still scroll that way? Then a wheel or swipe scrolls it instead of acting.
  const scroller = () => document.querySelector(".fc-study .fc-scroll");
  const canScroll = (dir) => { const sc = scroller(); if (!sc) return false; return dir === "down" ? sc.scrollTop + sc.clientHeight < sc.scrollHeight - 2 : sc.scrollTop > 2; };
  function fire(inp, e) {
    if (learnFor) { learnFor(inp); e?.preventDefault?.(); return true; }
    if (peek) { peek(inp); e?.preventDefault?.(); return true; }
    if (!listener) return false;
    const a = actionOf(inp);
    if (!a) return false;
    e?.preventDefault?.();
    if (gate()) listener(a);
    return true;
  }
  document.addEventListener("keydown", (e) => {
    if (!listener && !learnFor) return;
    if (e.target.closest?.("input, select, textarea")) return;
    if (e.key === "Escape") { if (learnFor) learnFor(null); else listener?.("exit"); return; }
    if (e.metaKey || e.ctrlKey || e.altKey || e.key === "Tab") return;
    if (peek && !learnFor && e.target.closest?.("button") && (e.key === "Enter" || e.key === " ")) return;
    if (e.repeat) { if (actionOf("key:" + e.code)) e.preventDefault(); return; }
    fire("key:" + (e.code || e.key), e) || (e.key === " " && fire("key:Space", e));
  }, true);
  let wheelAcc = 0, wheelT = 0;
  addEventListener("wheel", (e) => {
    if (!listener && !learnFor) return;
    if (peek && !learnFor) return;  // let the setup page scroll
    if (!learnFor && canScroll(e.deltaY > 0 ? "down" : "up")) return;
    e.preventDefault();
    if (Date.now() - wheelT > 400) wheelAcc = 0;
    wheelT = Date.now(); wheelAcc += e.deltaY;
    if (Math.abs(wheelAcc) > 40) { const d = wheelAcc > 0 ? "down" : "up"; wheelAcc = 0; fire("wheel:" + d, e); }
  }, { passive: false });
  let t0 = null;
  addEventListener("touchstart", (e) => { if ((listener || learnFor) && e.touches.length === 1) t0 = { x: e.touches[0].clientX, y: e.touches[0].clientY, t: Date.now(), el: e.target, dn: canScroll("down"), up: canScroll("up") }; }, { passive: true });
  addEventListener("touchend", (e) => {
    if (!t0) return;
    const p = e.changedTouches[0], dx = p.clientX - t0.x, dy = p.clientY - t0.y, s = t0; t0 = null;
    if (Math.max(Math.abs(dx), Math.abs(dy)) < 50 || Date.now() - s.t > 900) return;
    if (s.el.closest?.("button, a, input, select")) return;
    const v = Math.abs(dy) > Math.abs(dx);
    if (v && !learnFor && !peek && (dy < 0 ? s.dn : s.up)) return;  // that swipe was scrolling a long answer
    fire("swipe:" + (v ? (dy < 0 ? "up" : "down") : (dx < 0 ? "left" : "right")));
  }, { passive: true });
  // media buttons only reach a page that is playing audio, so this plays silence while you study
  let silent = null;
  function mediaOn(on) {
    if (!("mediaSession" in navigator)) return false;
    if (on) {
      if (!silent) {
        const sr = 8000, n = sr, b = new ArrayBuffer(44 + n * 2), v = new DataView(b), w = (o, s) => [...s].forEach((c, i) => v.setUint8(o + i, c.charCodeAt(0)));
        w(0, "RIFF"); v.setUint32(4, 36 + n * 2, true); w(8, "WAVEfmt "); v.setUint32(16, 16, true); v.setUint16(20, 1, true); v.setUint16(22, 1, true);
        v.setUint32(24, sr, true); v.setUint32(28, sr * 2, true); v.setUint16(32, 2, true); v.setUint16(34, 16, true); w(36, "data"); v.setUint32(40, n * 2, true);
        silent = new Audio(URL.createObjectURL(new Blob([b], { type: "audio/wav" }))); silent.loop = true;
      }
      silent.play().catch(() => {});
      navigator.mediaSession.metadata = new MediaMetadata({ title: "Drug flashcards", artist: "PA–S Rx" });
      for (const a of ["play", "pause", "nexttrack", "previoustrack"]) { try { navigator.mediaSession.setActionHandler(a, () => { fire("media:" + a); if (a === "pause" || a === "play") silent.play().catch(() => {}); }); } catch { /* unsupported action */ } }
    } else if (silent) { silent.pause(); for (const a of ["play", "pause", "nexttrack", "previoustrack"]) { try { navigator.mediaSession.setActionHandler(a, null); } catch { /* */ } } }
    return true;
  }

  // ---------------------------------------------------------------- setup screen
  const tags = [...new Set(DR.flatMap((d) => d.t))].sort();
  const chip = (on, attr, label, title = "") => `<button class="sch-chip${on ? " on" : ""}" ${attr}${title ? ` title="${esc(title)}"` : ""}>${label}</button>`;
  function counts(cs) {
    const now = Date.now(), L = dayLog();
    let n = 0, l = 0, r = 0;
    for (const c of cs) { const st = SRS[c.id]; if (!st) n++; else if (isLearn(st)) l++; else if (isDue(st)) r++; }
    return { n: Math.min(n, Math.max(0, S.newPer - L.n)), nAll: n, l, r: Math.min(r, Math.max(0, S.revPer - L.r)), total: cs.length, now };
  }
  function draw() {
    const ds = drugsChosen(), cs = cards(), k = counts(cs);
    const units = Object.entries(CFG.units).filter(([u]) => DR.some((d) => d.u === +u));
    const lecs = CFG.lectures.filter((l) => !S.units.length || S.units.includes(l.unit));
    app.innerHTML = `
    <div class="fc-grid">
      <div class="fc-panel">
        <h3>1 · Drugs <span class="fc-n">${ds.length} of ${DR.length}</span></h3>
        <div class="fc-lab">Unit</div><div class="fc-chips">${chip(!S.units.length, 'data-unit=""', "All")}${units.map(([u, name]) => chip(S.units.includes(+u), `data-unit="${u}"`, `${u} · ${esc(name)}`)).join("")}</div>
        <div class="fc-lab">Lecture</div><div class="fc-chips">${chip(!S.lids.length, 'data-lid=""', "All")}${lecs.map((l) => chip(S.lids.includes(l.id), `data-lid="${l.id}"`, esc(l.id), l.title)).join("")}</div>
        <details class="fc-det"${S.tags.length ? " open" : ""}><summary>Class / system${S.tags.length ? ` · ${S.tags.length} picked` : ""}</summary><div class="fc-chips">${chip(!S.tags.length, 'data-tag=""', "All")}${tags.map((t) => chip(S.tags.includes(t), `data-tag="${esc(t)}"`, esc(t))).join("")}</div></details>
        <div class="fc-row"><input type="search" id="fc-q" placeholder="Search a drug or class…" value="${esc(S.q)}" aria-label="Search drugs"></div>
        <label class="dx-check"><input type="checkbox" data-opt="sgOnly"${S.sgOnly ? " checked" : ""}><span>Study-guide drugs only</span></label>
        <label class="dx-check"><input type="checkbox" data-opt="tbDrugs"${S.tbDrugs ? " checked" : ""}><span>Include textbook-only drugs</span></label>
      </div>
      <div class="fc-panel">
        <h3>2 · Card style</h3>
        <div class="fc-styles">${STYLES.map(([k2, t, d]) => `<label class="fc-style${S.styles.includes(k2) ? " on" : ""}"><input type="checkbox" data-style="${k2}"${S.styles.includes(k2) ? " checked" : ""}><span><strong>${t}</strong><small>${d}</small></span></label>`).join("")}</div>
        <label class="dx-check"><input type="checkbox" data-opt="reverse"${S.reverse ? " checked" : ""}><span>Also reversed: class → name a drug</span></label>
        <h3 style="margin-top:18px">3 · What the cards cover</h3>
        <div class="fc-chips">${FIELDS.map(([k2, t]) => chip(S.fields.includes(k2), `data-field="${k2}"`, t)).join("")}</div>
        <div class="fc-row2"><label>Facts per field <select data-num="per">${[[1, "1"], [2, "2"], [3, "3"], [0, "All"]].map(([v, t]) => `<option value="${v}"${S.per === v ? " selected" : ""}>${t}</option>`).join("")}</select></label></div>
        <label class="dx-check"><input type="checkbox" data-opt="tbFacts"${S.tbFacts ? " checked" : ""}><span>Textbook-only facts (TB)</span></label>
        <label class="dx-check"><input type="checkbox" data-opt="cites"${S.cites ? " checked" : ""}><span>Show citations</span></label>
        <label class="dx-check"><input type="checkbox" data-opt="mol"${S.mol ? " checked" : ""}><span>3D structure on the answer</span></label>
      </div>
      <div class="fc-panel">
        <h3>4 · Session</h3>
        <div class="fc-row2"><label>New cards a day <select data-num="newPer">${[5, 10, 20, 30, 50, 100, 9999].map((v) => `<option value="${v}"${S.newPer === v ? " selected" : ""}>${v === 9999 ? "No limit" : v}</option>`).join("")}</select></label>
        <label>Reviews a day <select data-num="revPer">${[50, 100, 200, 500, 9999].map((v) => `<option value="${v}"${S.revPer === v ? " selected" : ""}>${v === 9999 ? "No limit" : v}</option>`).join("")}</select></label></div>
        <div class="fc-row2"><label>New card order <select data-sel="order"><option value="course"${S.order === "course" ? " selected" : ""}>Course order</option><option value="random"${S.order === "random" ? " selected" : ""}>Random</option></select></label></div>
        <label class="dx-check"><input type="checkbox" data-opt="cram"${S.cram ? " checked" : ""}><span>Cram: every card now, schedule untouched</span></label>
        <div class="fc-counts"><span class="fc-new" title="New">${k.n}</span><span class="fc-lrn" title="Learning">${k.l}</span><span class="fc-due" title="To review">${k.r}</span><small>${k.total} cards · ${k.nAll} never seen</small></div>
        <button class="btn fc-go" id="fc-go"${(S.cram ? k.total : k.n + k.l + k.r) ? "" : " disabled"}>${S.cram ? `Cram ${k.total} cards` : "Study now"}</button>
        ${!S.cram && !(k.n + k.l + k.r) && k.total ? `<p class="small muted">All caught up for today. Come back tomorrow, raise the new-card limit, or turn on Cram.</p>` : ""}
        <div class="fc-row3"><button class="btn ghost small" id="fc-ring">Remote ring setup</button><button class="btn ghost small" id="fc-reset">Reset progress</button></div>
      </div>
    </div>
    <div class="fc-preview"><div class="fc-lab">Preview</div>${cs.length ? (() => { const f = faces(cs[0]); return `<div class="fc-mini"><div>${f[0]}</div><div class="fc-mini-b" tabindex="0" aria-label="Answer side">${f[1]}</div></div>`; })() : '<p class="muted">No cards: pick at least one drug, one card style and one field.</p>'}</div>`;
    const tog = (arr, v) => (arr.includes(v) ? arr.filter((x) => x !== v) : [...arr, v]);
    const set = (fn) => { fn(); save(); draw(); };
    app.querySelectorAll("[data-unit]").forEach((b) => b.onclick = () => set(() => { S.units = b.dataset.unit ? tog(S.units, +b.dataset.unit) : []; S.lids = S.lids.filter((l) => !S.units.length || S.units.includes(CFG.lectures.find((x) => x.id === l)?.unit)); }));
    app.querySelectorAll("[data-lid]").forEach((b) => b.onclick = () => set(() => (S.lids = b.dataset.lid ? tog(S.lids, b.dataset.lid) : [])));
    app.querySelectorAll("[data-tag]").forEach((b) => b.onclick = () => set(() => (S.tags = b.dataset.tag ? tog(S.tags, b.dataset.tag) : [])));
    app.querySelectorAll("[data-field]").forEach((b) => b.onclick = () => set(() => (S.fields = FIELDS.map((f) => f[0]).filter((f) => (f === b.dataset.field ? !S.fields.includes(f) : S.fields.includes(f))))));
    app.querySelectorAll("[data-style]").forEach((b) => b.onchange = () => set(() => (S.styles = tog(S.styles, b.dataset.style))));
    app.querySelectorAll("[data-opt]").forEach((b) => b.onchange = () => set(() => (S[b.dataset.opt] = b.checked)));
    app.querySelectorAll("[data-num]").forEach((b) => b.onchange = () => set(() => (S[b.dataset.num] = +b.value)));
    app.querySelectorAll("[data-sel]").forEach((b) => b.onchange = () => set(() => (S[b.dataset.sel] = b.value)));
    const q = app.querySelector("#fc-q");
    q.oninput = () => { S.q = q.value; clearTimeout(q._t); q._t = setTimeout(() => { draw(); const n = app.querySelector("#fc-q"); n.focus(); n.setSelectionRange(n.value.length, n.value.length); }, 250); };
    app.querySelector("#fc-go").onclick = () => study(cs);
    app.querySelector("#fc-ring").onclick = ringSetup;
    app.querySelector("#fc-reset").onclick = () => { if (confirm(`Forget your progress on these ${cs.length} cards? They'll all be new again.`)) { cs.forEach((c) => delete SRS[c.id]); store.set("fc:srs", SRS); draw(); } };
  }

  // ---------------------------------------------------------------- study overlay
  let wake = null;
  const keepAwake = async (on) => { try { if (on && "wakeLock" in navigator) wake = await navigator.wakeLock.request("screen"); else { await wake?.release(); wake = null; } } catch { /* not allowed */ } };
  function study(all) {
    const order = S.order === "random" ? [...all].sort(() => Math.random() - 0.5) : all;
    const L = dayLog();
    let newLeft = S.cram ? Infinity : Math.max(0, S.newPer - L.n), revLeft = S.cram ? Infinity : Math.max(0, S.revPer - L.r);
    const cram = S.cram ? [...all].sort(() => Math.random() - 0.5) : null;
    const pending = new Set(order.map((c) => c.id)), byId = Object.fromEntries(order.map((c) => [c.id, c]));
    let cur = null, shown = false, history = [], done = 0, startN = null, again = [];
    const el = document.createElement("div"); el.className = "qm fc-study"; document.body.append(el);
    document.documentElement.style.overflow = "hidden"; keepAwake(true); if (ringOpts.media) mediaOn(true);
    const end = () => { listener = null; el.remove(); document.documentElement.style.overflow = ""; keepAwake(false); mediaOn(false); draw(); };
    function pick() {
      const now = Date.now();
      if (cram) { if (!cram.length && again.length) cram.push(...again.splice(0)); return cram.shift() || null; }
      const learnDue = order.filter((c) => pending.has(c.id) && isLearn(SRS[c.id]) && SRS[c.id].due <= now).sort((a, b) => SRS[a.id].due - SRS[b.id].due);
      if (learnDue.length) return learnDue[0];
      const rev = revLeft > 0 ? order.filter((c) => pending.has(c.id) && isDue(SRS[c.id])).sort((a, b) => SRS[a.id].due - SRS[b.id].due) : [];
      const fresh = newLeft > 0 ? order.filter((c) => pending.has(c.id) && !SRS[c.id]) : [];
      // like Anki: mix new cards in among reviews
      if (rev.length && fresh.length) return done % 4 === 3 ? fresh[0] : rev[0];
      if (rev.length) return rev[0];
      if (fresh.length) return fresh[0];
      const ahead = order.filter((c) => pending.has(c.id) && isLearn(SRS[c.id]) && SRS[c.id].due - now < 20 * MIN).sort((a, b) => SRS[a.id].due - SRS[b.id].due);  // learn ahead 20 min
      return ahead[0] || null;
    }
    function live() {
      if (cram) return { n: cram.length + again.length + (cur ? 1 : 0), l: 0, r: 0 };
      let n = 0, l = 0, r = 0;
      for (const id of pending) { const st = SRS[id]; if (!st) n++; else if (isLearn(st)) l++; else if (isDue(st)) r++; }
      return { n: Math.min(n, newLeft), l, r: Math.min(r, revLeft) };
    }
    function render() {
      if (!cur) cur = pick();
      shown = false;
      const k = live();
      if (!cur) {
        const nextL = order.map((c) => SRS[c.id]).filter(isLearn).sort((a, b) => a.due - b.due)[0];
        el.innerHTML = `<div class="qm-top"><button class="qm-x" data-x aria-label="Close">✕</button><div class="qm-title">Drug flashcards</div><span></span></div>
          <div class="fc-scroll"><div class="fc-done"><div class="fc-done-k">Congratulations!</div><h2>You've finished for now.</h2><p class="muted">${done} card${done === 1 ? "" : "s"} studied${nextL ? ` · next learning card in ${ivlText(nextL)}` : ""}.</p>
          <div class="fc-row3" style="justify-content:center"><button class="btn" data-x>Done</button>${nextL ? '<button class="btn ghost" data-wait>Keep going</button>' : ""}</div></div></div>`;
        el.querySelectorAll("[data-x]").forEach((b) => (b.onclick = end));
        el.querySelector("[data-wait]")?.addEventListener("click", () => { const c = order.find((x) => SRS[x.id] === nextL); if (c) { SRS[c.id] = { ...nextL, due: Date.now() }; render(); } });
        listener = (a) => { if (a === "exit" || a === "show") end(); };
        return;
      }
      if (startN === null) startN = k.n + k.l + k.r;
      const f = faces(cur), st = SRS[cur.id], kind = !st ? "n" : isLearn(st) ? "l" : "r";
      el.innerHTML = `<div class="qm-top"><button class="qm-x" data-x aria-label="Close" title="Close (Esc)">✕</button>
        <div class="fc-counts top"><span class="fc-new${kind === "n" ? " cur" : ""}">${k.n}</span><span class="fc-lrn${kind === "l" ? " cur" : ""}">${k.l}</span><span class="fc-due${kind === "r" ? " cur" : ""}">${k.r}</span></div>
        <button class="qm-x" data-undo aria-label="Undo" title="Undo (Z)"${history.length ? "" : " disabled"}>↶</button></div>
        <div class="fc-scroll"><div class="fc-card" data-tapzone>
          <div class="fc-face front">${f[0]}</div>
          <div class="fc-face back" hidden><div class="fc-back-in">${f[1]}</div></div>
        </div></div>
        <div class="fc-bar"><button class="btn fc-show" data-show>Show answer</button>
        <div class="fc-grades" hidden>${[[1, "Again", "again"], [2, "Hard", "hard"], [3, "Good", "good"], [4, "Easy", "easy"]].map(([g, t, c]) => `<button class="fc-g ${c}" data-g="${g}"><small>${ivlText(next(SRS[cur.id], g))}</small><span>${t}</span></button>`).join("")}</div>
        <div class="fc-hint">${hint()}</div></div>`;
      el.querySelector("[data-x]").onclick = end;
      el.querySelector("[data-undo]").onclick = undo;
      el.querySelector("[data-show]").onclick = reveal;
      el.querySelectorAll("[data-g]").forEach((b) => (b.onclick = (e) => { e.stopPropagation(); grade(+b.dataset.g); }));
      el.querySelector("[data-tapzone]").onclick = (e) => {
        if (e.target.closest("a, button, summary") || !gate()) return;
        if (!shown) return reveal();
        if (!ringOpts.tapZones) return;
        const r = el.querySelector("[data-tapzone]").getBoundingClientRect();
        grade(e.clientX < r.left + r.width / 2 ? 1 : 3);
      };
      listener = (a) => {
        if (a === "exit") return end();
        if (a === "undo") return undo();
        if (!shown) { if (a === "show") reveal(); return; }  // only the main button flips; nothing grades a card you haven't seen
        grade({ show: 3, again: 1, hard: 2, easy: 4 }[a]);
      };
    }
    function hint() {
      const p = (a) => (RING[a] || []).slice(0, 2).map(inputName).join(" / ");
      return `${p("show")} · show &amp; Good &nbsp;·&nbsp; ${p("again")} · Again &nbsp;·&nbsp; 1–4 grade${ringOpts.tapZones ? " &nbsp;·&nbsp; tap left = Again, right = Good" : ""}`;
    }
    function reveal() {
      if (shown) return;
      shown = true;
      const front = el.querySelector(".fc-face.front"), back = el.querySelector(".fc-face.back");
      back.hidden = false; front.classList.add("asked");
      el.querySelector("[data-show]").hidden = true; el.querySelector(".fc-grades").hidden = false;
      back.animate?.([{ opacity: 0, transform: "translateY(10px)" }, { opacity: 1, transform: "none" }], { duration: 260, easing: "cubic-bezier(.2,.8,.2,1)" });
      if (S.mol && cur.d && ["whole", "field", "rcls", "which"].includes(cur.kind) && (cur.kind !== "which" || cur.ds.length === 1)) {
        const host = back, name = cur.d.n;
        window.dpasMolData?.("../").then((M) => { if (M[name] && host.isConnected && !host.querySelector(".mol3d-wrap")) window.dpasMol3d(host, el.querySelector(".fc-scroll"), M[name], { size: innerWidth < 700 ? 150 : 210, cls: "fc-mol", recede: false }); });
      }
    }
    function grade(g) {
      if (!shown || !cur) return;
      shown = false;  // a second press before the next card can't grade twice
      const id = cur.id, before = SRS[id];
      history.push({ id, before, cur, newLeft, revLeft, done, cram: cram ? [...cram] : null, again: [...again] });
      if (history.length > 30) history.shift();
      if (cram) { if (g === 1) again.push(cur); }
      else {
        const L2 = dayLog();
        if (!before) { newLeft--; L2.n++; } else if (isDue(before)) { revLeft--; L2.r++; }
        store.set("fc:day", L2);
        SRS[id] = next(before, g); store.set("fc:srs", SRS);
        if (SRS[id].t === "review") pending.delete(id);
      }
      done++;
      const c = el.querySelector(".fc-card");
      c?.animate?.([{ opacity: 1, transform: "none" }, { opacity: 0, transform: `translateX(${g === 1 ? -24 : 24}px)` }], { duration: 160, easing: "ease-in" });
      setTimeout(() => { cur = null; render(); }, 150);
    }
    function undo() {
      const h = history.pop();
      if (!h) return;
      if (!cram) {
        if (h.before) SRS[h.id] = h.before; else delete SRS[h.id];
        store.set("fc:srs", SRS); pending.add(h.id);
        const L2 = dayLog(); if (!h.before) L2.n = Math.max(0, L2.n - 1); else if (isDue(h.before)) L2.r = Math.max(0, L2.r - 1); store.set("fc:day", L2);
      } else { cram.splice(0, cram.length, ...h.cram); again.splice(0, again.length, ...h.again); }
      newLeft = h.newLeft; revLeft = h.revLeft; done = h.done; cur = byId[h.id] || h.cur;
      render(); reveal();
    }
    render();
  }

  // ---------------------------------------------------------------- remote ring setup
  function ringSetup() {
    const el = document.createElement("div"); el.className = "qm fc-study"; document.body.append(el);
    document.documentElement.style.overflow = "hidden";
    let test = "";
    const close = () => { listener = null; learnFor = null; peek = null; mediaOn(false); el.remove(); document.documentElement.style.overflow = ""; draw(); };
    const paint = () => {
      el.innerHTML = `<div class="qm-top"><button class="qm-x" data-x aria-label="Close">✕</button><div class="qm-title">Remote ring setup</div><span></span></div>
      <div class="fc-scroll"><div class="fc-ring">
        <p class="lede" style="font-size:17px">Pair your ring (Stouchi or any Bluetooth page-turner) with this phone or computer first. It works in any of its modes: <strong>page-turn</strong> (arrow / page keys), <strong>scroll</strong> or TikTok mode (swipes), <strong>tap</strong> (taps the screen), or <strong>media</strong> (play / next / previous).</p>
        <div class="fc-test" aria-live="polite">${test ? `Heard: <strong>${esc(inputName(test))}</strong> → ${actionOf(test) ? `<span class="fc-ok">${esc(ACTIONS.find((a) => a[0] === actionOf(test))[1])}</span>` : '<span class="fc-bad">not assigned</span>'}` : "Press a ring button to test it."}</div>
        ${ACTIONS.map(([a, t, sub]) => `<div class="fc-bind"><div><strong>${t}</strong>${sub ? `<small>${sub}</small>` : ""}</div><div class="fc-keys">${(RING[a] || []).map((i) => `<span>${esc(inputName(i))}<button data-rm="${a}|${esc(i)}" aria-label="Remove">×</button></span>`).join("")}</div><button class="btn ghost small" data-learn="${a}">Learn button</button></div>`).join("")}
        <label class="dx-check"><input type="checkbox" data-o="tapZones"${ringOpts.tapZones ? " checked" : ""}><span>Tap mode: after the answer shows, tapping the left half = Again, right half = Good</span></label>
        <label class="dx-check"><input type="checkbox" data-o="media"${ringOpts.media ? " checked" : ""}><span>Media mode: listen for play / next / previous (plays silence in the background so the buttons reach this page)</span></label>
        <p class="small muted">Volume buttons can't be read by a web page. If your ring is in a volume or camera-shutter mode, switch it to page-turn or scroll mode. Each press counts once, so a ring that repeats won't skip cards. Nothing grades a card before its answer is showing.</p>
        <div class="fc-row3"><button class="btn ghost small" data-reset>Restore defaults</button><button class="btn" data-x>Done</button></div>
      </div></div>`;
      el.querySelectorAll("[data-x]").forEach((b) => (b.onclick = close));
      el.querySelectorAll("[data-rm]").forEach((b) => (b.onclick = () => { const [a, i] = b.dataset.rm.split("|"); RING[a] = RING[a].filter((x) => x !== i); store.set("fc:ring", RING); paint(); }));
      el.querySelectorAll("[data-learn]").forEach((b) => (b.onclick = (e) => {
        e.stopPropagation();
        const a = b.dataset.learn; b.textContent = "Press the ring button…"; b.classList.add("fc-listen");
        setTimeout(() => { learnFor = (inp) => {
          learnFor = null;
          if (inp) { for (const k of Object.keys(RING)) RING[k] = RING[k].filter((x) => x !== inp); RING[a] = [inp, ...(RING[a] || [])]; store.set("fc:ring", RING); test = inp; }
          paint();
        }; }, 250);
      }));
      el.querySelectorAll("[data-o]").forEach((b) => (b.onchange = () => { ringOpts[b.dataset.o] = b.checked; store.set("fc:ringopt", ringOpts); if (b.dataset.o === "media") mediaOn(b.checked); }));
      el.querySelector("[data-reset]").onclick = () => { RING = JSON.parse(JSON.stringify(RDEF)); store.set("fc:ring", RING); paint(); };
    };
    // test mode: every press is echoed ("Heard: …") instead of acting
    peek = (inp) => { test = inp; paint(); };
    listener = (a) => { if (a === "exit") close(); };
    if (ringOpts.media) mediaOn(true);
    paint();
  }
  draw();
})();
