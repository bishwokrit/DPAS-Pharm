// Sketch mode (hidden page): sketch of the day, Sketchy watch tracker + exam-eve playlist, recall drill,
// memory hooks, a Kahoot game-night builder, and head-to-head. Everything you do here stays in this browser.
(function () {
  const CFG = JSON.parse(document.getElementById("sketch-data").textContent);
  const V = CFG.videos || [];
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* private mode */ } },
  };
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const md = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  const now = new Date(), today = iso(now);
  const hash = (s) => [...s].reduce((h, c) => (Math.imul(h, 31) + c.charCodeAt(0)) | 0, 7);
  const shuffle = (a) => { for (let i = a.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [a[i], a[j]] = [a[j], a[i]]; } return a; };
  const $ = (id) => document.getElementById(id);
  const v = document.documentElement.dataset.v || "";
  const fmtDay = (s) => new Date(s + "T00:00").toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" });
  const daysTo = (s) => Math.round((new Date(s + "T00:00") - new Date(today + "T00:00")) / 864e5);

  const unitOfLec = Object.fromEntries(CFG.lectures.map((l) => [l.id, l.unit]));
  const drugByName = Object.fromEntries(CFG.drugs.map((d) => [d.name.toLowerCase(), d]));
  const vidUnit = (x) => Math.min(...(x.lectures || []).map((l) => unitOfLec[l] || 99), ...(x.drugs || []).map((n) => drugByName[n.toLowerCase()]?.unit || 99));
  const vidsFor = (name) => V.filter((x) => (x.drugs || []).some((n) => n.toLowerCase() === name.toLowerCase()));
  const nextUnitExam = CFG.exams.find((e) => e.unit && e.date >= today);
  const curUnit = nextUnitExam ? nextUnitExam.unit : Math.max(1, ...CFG.lectures.map((l) => l.unit));
  const watched = () => store.get("sk:watched", {});
  const setWatched = (t, on) => { const w = watched(); on ? (w[t] = today) : delete w[t]; store.set("sk:watched", w); };

  // the question bank: lecture self-tests + practice exams, each tagged with its lecture and unit
  let bankP = null;
  const bank = () => (bankP ||= (async () => {
    const out = [];
    await Promise.all(CFG.lectures.map(async (l) => {
      const kb = await fetch(`../${l.id}/kb.json?v=${v}`).then((r) => r.json()).catch(() => null);
      kb?.quiz.forEach((q) => out.push({ ...q, id: `${l.id}:${q.id}`, raw: q.id, lid: l.id, unit: l.unit, link: q.link ? { ...q.link, href: `../${l.id}/index.html${q.link.href}` } : null }));
    }));
    await Promise.all(CFG.quizzes.map(async (slugE) => {
      const qs = await fetch(`../exams/${slugE}/quiz.json?v=${v}`).then((r) => r.json()).catch(() => []);
      qs.forEach((q) => { const lid = (q.link?.href || "").split("/")[2]; out.push({ ...q, exam: slugE, lid, unit: unitOfLec[lid] || 1, link: q.link ? { ...q.link, href: q.link.href.replace(/^\.\.\/\.\.\//, "../") } : null }); });
    }));
    return out;
  })());

  const vidChip = (x) => `<span class="sx-vchip${watched()[x.title] ? " on" : ""}">${esc(x.title)}</span>`;

  // ---------------------------------------------------------------- 1 · sketch of the day
  (async () => {
    const host = $("sotd-app");
    const all = await fetch(`../drugs/dotd.json?v=${v}`).then((r) => r.json()).catch(() => []);
    const pool = all.filter((d) => d.taught <= today).sort((a, b) => hash(a.name) - hash(b.name));
    if (!pool.length) { host.innerHTML = '<p class="sx-muted">Nothing taught yet.</p>'; return; }
    const d = pool[Math.floor(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()) / 864e5) % pool.length];
    const qs = d.qs.slice(0, 3).map((q) => ({ ...q, link: q.link ? { ...q.link, href: "../" + q.link.href } : null }));
    const vids = vidsFor(d.name), info = drugByName[d.name.toLowerCase()];
    const paint = () => {
      const s = store.get("sk:sotd", {}), done = s.date === today;
      host.innerHTML = `<div class="sx-panel sx-sotd"><div class="sx-sotd-main"><div class="sx-k">${now.toLocaleDateString(undefined, { weekday: "long", month: "long", day: "numeric" })}</div>
        <h3>${esc(d.name)}</h3><p class="sx-muted">${esc(d.cls === "Not covered in materials" ? "Class: covered in a later unit" : d.cls)}</p>
        <div class="sx-sotd-v">${vids.length ? vids.map((x) => `<button class="sx-vbtn${watched()[x.title] ? " on" : ""}" data-w="${esc(x.title)}"><span class="sx-tick"></span><span><strong>${esc(x.title)}</strong>${x.section ? `<small>${esc(x.section)}</small>` : ""}</span></button>`).join("")
          : `<p class="sx-muted small">${V.length ? "No Sketchy video lists this drug." : "Its Sketchy video appears here once your docs are uploaded."}</p>`}</div>
        <div class="sx-row">${done ? `<span class="sx-done">Done today · ${s.score}/${s.total}</span><button class="btn ghost small" data-q>Again</button>` : `<button class="btn small" data-q>3 questions →</button>`}
        <a class="btn ghost small" href="../drugs/index.html#${slug(d.name)}">Drug sheet</a></div></div>
        <ul class="sx-facts">${(info?.facts || d.facts).slice(0, 3).map((f) => `<li>${md(f.text)} <span class="cite">${esc(f.src)}</span></li>`).join("")}</ul></div>`;
      host.querySelector("[data-q]").onclick = () => window.dpasQuiz?.start(qs, { title: `Sketch of the day · ${d.name}`, onFinish: (r) => { if (!done) store.set("sk:sotd", { date: today, score: r.correct, total: r.total }); paint(); } });
      host.querySelectorAll("[data-w]").forEach((b) => (b.onclick = () => { setWatched(b.dataset.w, !watched()[b.dataset.w]); paint(); tracker(); }));
    };
    paint();
  })();

  // ---------------------------------------------------------------- 2 · watch tracker (+ 7 · exam-eve playlist)
  let q = "";
  function tracker() {
    const host = $("tracker-app");
    if (!host) return;
    const w = watched(), units = [...new Set(V.map(vidUnit))].sort((a, b) => a - b);
    const due = nextUnitExam ? V.filter((x) => vidUnit(x) === nextUnitExam.unit && !w[x.title]) : [];
    const match = (x) => !q || (x.title + " " + (x.section || "") + " " + (x.drugs || []).join(" ") + " " + (x.lectures || []).join(" ")).toLowerCase().includes(q);
    host.innerHTML = (nextUnitExam ? `<div class="sx-banner${due.length ? "" : " ok"}"><strong>${esc(nextUnitExam.label)}</strong> ${fmtDay(nextUnitExam.date)} · ${due.length ? `${due.length} Unit ${nextUnitExam.unit} sketch${due.length === 1 ? "" : "es"} left to watch` : "every Unit " + nextUnitExam.unit + " sketch watched"}</div>` : "") +
      `<input class="sx-find" type="search" placeholder="Filter by drug, video or lecture" aria-label="Filter Sketchy videos" value="${esc(q)}">` +
      units.map((u) => {
        const list = V.filter((x) => vidUnit(x) === u), n = list.filter((x) => w[x.title]).length, shown = list.filter(match);
        if (!shown.length) return "";
        return `<div class="sx-tu"><div class="sx-tu-h"><strong>${u === 99 ? "Other" : `Unit ${u}`}${CFG.units[u] ? ` <span>· ${esc(CFG.units[u])}</span>` : ""}</strong><span>${n}/${list.length} watched</span></div>
          <div class="sx-prog"><i style="width:${(100 * n) / list.length}%"></i></div>
          <div class="sx-vlist">${shown.map((x) => `<button class="sx-vbtn${w[x.title] ? " on" : ""}" data-w="${esc(x.title)}"><span class="sx-tick"></span><span><strong>${esc(x.title)}</strong><small>${esc([x.section, ...(x.lectures || [])].filter(Boolean).join(" · "))}</small>
            ${(x.drugs || []).length ? `<em>${x.drugs.map(esc).join(", ")}</em>` : ""}${x.note ? `<small class="sx-note">${esc(x.note)}</small>` : ""}</span></button>`).join("")}</div></div>`;
      }).join("");
    const f = host.querySelector(".sx-find");
    f.oninput = () => { q = f.value.toLowerCase().trim(); tracker(); const g = $("tracker-app").querySelector(".sx-find"); g.focus(); g.setSelectionRange(g.value.length, g.value.length); };
    host.querySelectorAll("[data-w]").forEach((b) => (b.onclick = () => { setWatched(b.dataset.w, !watched()[b.dataset.w]); tracker(); playlist(); }));
  }
  async function playlist() {
    const host = $("playlist-app");
    if (!host || !V.length) return;
    // what you've missed (self-tests, practice exams, Review) → the drugs those questions are about → their sketches
    const qs = await bank(), missed = qs.filter((x) => (x.exam ? store.get(`exam:${x.exam}:log`, []).some((e) => e.id === x.id) && store.get(`exam:${x.exam}:v1`, { answers: {} }).answers[x.id] !== x.answer : store.get(`miss:${x.lid}`, []).includes(x.raw)));
    const score = {};
    missed.forEach((x) => CFG.drugs.forEach((d) => { if (new RegExp(`\\b(${d.pattern})\\b`, "i").test(x.stem + " " + Object.values(x.options).join(" ") + " " + (x.why || ""))) score[d.name] = (score[d.name] || 0) + 1; }));
    const ranked = V.map((x) => ({ x, s: (x.drugs || []).reduce((a, n) => a + (score[n] || 0), 0) + (nextUnitExam && vidUnit(x) === nextUnitExam.unit && !watched()[x.title] ? 0.5 : 0) }))
      .filter((r) => r.s > 0).sort((a, b) => b.s - a.s).slice(0, 8);
    const ex = CFG.exams.find((e) => e.date >= today), eve = ex && daysTo(ex.date) <= 1;
    host.innerHTML = `<div class="sx-panel sx-play${eve ? " eve" : ""}"><div class="sx-k">${eve ? "Exam eve" : "Before your next exam"}${ex ? ` · ${esc(ex.label)} ${daysTo(ex.date) === 0 ? "today" : daysTo(ex.date) === 1 ? "tomorrow" : "in " + daysTo(ex.date) + " days"}` : ""}</div>
      <h3>${eve ? "Tonight's playlist" : "Your playlist"}</h3>
      ${ranked.length ? `<ol class="sx-pl">${ranked.map(({ x, s }) => `<li><strong>${esc(x.title)}</strong><small>${s >= 1 ? `${Math.floor(s)} missed question${Math.floor(s) === 1 ? "" : "s"} on ${esc((x.drugs || []).filter((n) => score[n]).join(", "))}` : "not watched yet"}</small></li>`).join("")}</ol>`
        : '<p class="sx-muted">Answer questions in Progress or the practice exams, and the sketches for the drugs you miss most line up here, worst first.</p>'}</div>`;
  }
  tracker(); playlist();

  // ---------------------------------------------------------------- 3 · recall drill
  (function recall() {
    const host = $("recall-app"), useVids = V.length > 0;
    const items = useVids ? V.map((x) => ({ key: "v:" + x.title, prompt: x.title, sub: x.section || "Sketchy video", facts: (x.drugs || []).flatMap((n) => (drugByName[n.toLowerCase()]?.facts || []).map((f) => ({ ...f, drug: n }))) })).filter((i) => i.facts.length)
      : CFG.drugs.filter((d) => d.unit <= curUnit && d.facts.length).map((d) => ({ key: "d:" + d.name, prompt: d.name, sub: d.cls === "Not covered in materials" ? "Drug" : d.cls, facts: d.facts }));
    if (!items.length) { host.innerHTML = '<p class="sx-muted">Nothing to drill yet.</p>'; return; }
    const log = () => store.get("sk:recall", {});
    // next prompt: never seen first, then the lowest score, oldest first
    const pick = (skip) => items.filter((i) => i.key !== skip).map((i) => { const r = log()[i.key]; return { i, k: r ? r.score / r.total + (r.date === today ? 1 : 0) + Math.random() * 0.15 : -1 + Math.random() }; }).sort((a, b) => a.k - b.k)[0].i;
    let cur = pick(), t0 = 0, timer = 0;
    function card() {
      clearInterval(timer);
      const r = log()[cur.key];
      host.innerHTML = `<div class="sx-panel sx-recall"><div class="sx-k">${useVids ? "Sketchy video" : "Drug"} · ${esc(cur.sub)}${r ? ` · last time ${r.score}/${r.total}` : ""}</div><h3>${esc(cur.prompt)}</h3>
        <p class="sx-muted">Out loud or typed: everything you remember${useVids ? " from this sketch and its drugs" : ""}. Then reveal and check yourself.</p>
        <textarea rows="3" placeholder="Optional: type what you recall" aria-label="What you recall"></textarea>
        <div class="sx-row"><button class="btn small" data-reveal>Reveal <span class="sx-clock">0:00</span></button><button class="btn ghost small" data-skip>Another</button></div></div>`;
      t0 = Date.now(); const c = host.querySelector(".sx-clock");
      timer = setInterval(() => { const s = Math.floor((Date.now() - t0) / 1000); c.textContent = `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`; }, 1000);
      host.querySelector("[data-skip]").onclick = () => { cur = pick(cur.key); card(); };
      host.querySelector("[data-reveal]").onclick = reveal;
    }
    function reveal() {
      clearInterval(timer);
      const typed = host.querySelector("textarea").value.trim();
      host.querySelector(".sx-recall").innerHTML = `<div class="sx-k">Tap each fact you had</div><h3>${esc(cur.prompt)}</h3>${typed ? `<blockquote class="sx-typed">${esc(typed)}</blockquote>` : ""}
        <div class="sx-checks">${cur.facts.map((f, i) => `<button class="sx-fact" data-i="${i}"><span class="sx-tick"></span><span>${f.drug ? `<b>${esc(f.drug)}:</b> ` : ""}${md(f.text)} <span class="cite">${esc(f.src)}</span></span></button>`).join("")}</div>
        <div class="sx-row"><button class="btn small" data-save>Save · <span data-n>0</span>/${cur.facts.length}</button></div>`;
      const box = host.querySelector(".sx-recall"), n = () => box.querySelectorAll(".sx-fact.on").length;
      box.querySelectorAll(".sx-fact").forEach((b) => (b.onclick = () => { b.classList.toggle("on"); box.querySelector("[data-n]").textContent = n(); }));
      box.querySelector("[data-save]").onclick = () => { const L = log(); L[cur.key] = { score: n(), total: cur.facts.length, date: today }; store.set("sk:recall", L); cur = pick(cur.key); card(); };
    }
    card();
  })();

  // ---------------------------------------------------------------- 4 · memory hooks (also shown on drug sheets while Sketch mode is on)
  (function hooks() {
    const host = $("hooks-app");
    const H = () => store.get("sk:hooks", {});
    let filter = "";
    function paint() {
      const h = H(), list = CFG.drugs.filter((d) => !filter || (d.name + " " + d.cls).toLowerCase().includes(filter));
      host.innerHTML = `<p class="sx-muted">One line per drug, in your own words. ${Object.keys(h).length} written. They show up on each drug's sheet while Sketch mode is on.</p>
        <input class="sx-find" type="search" placeholder="Find a drug" aria-label="Find a drug" value="${esc(filter)}">
        <div class="sx-hooks">${list.map((d) => `<label class="sx-hook"><span><strong>${esc(d.name)}</strong><small>Unit ${d.unit}</small></span><input maxlength="160" data-d="${esc(d.name)}" value="${esc(h[d.name] || "")}" placeholder="Your hook…"></label>`).join("")}</div>`;
      const f = host.querySelector(".sx-find");
      f.oninput = () => { filter = f.value.toLowerCase().trim(); paint(); const g = host.querySelector(".sx-find"); g.focus(); g.setSelectionRange(g.value.length, g.value.length); };
      host.querySelectorAll("[data-d]").forEach((i) => (i.oninput = () => { const x = H(); i.value.trim() ? (x[i.dataset.d] = i.value.trim()) : delete x[i.dataset.d]; store.set("sk:hooks", x); }));
    }
    paint();
  })();

  // ---------------------------------------------------------------- 5 · Kahoot game-night builder (fills the official template in the browser)
  (async function builder() {
    const host = $("kahoot-app");
    const rows = await fetch(`kahoot/rows.json?v=${v}`).then((r) => r.json()).catch(() => ({}));
    const lecs = CFG.lectures.filter((l) => rows[l.id]?.length);
    if (!lecs.length) { host.innerHTML = '<p class="sx-muted">No decks yet.</p>'; return; }
    const sel = new Set(lecs.filter((l) => l.unit === curUnit).map((l) => l.id));
    if (!sel.size) sel.add(lecs[lecs.length - 1].id);
    let n = 30;
    const total = () => [...sel].reduce((a, id) => a + rows[id].length, 0);
    function paint() {
      const max = Math.max(1, total()); n = Math.min(Math.max(5, n), max);
      host.innerHTML = `<div class="sx-panel sx-build"><div class="sx-pick">${[...new Set(lecs.map((l) => l.unit))].map((u) => `<div><div class="sx-k">Unit ${u}</div>${lecs.filter((l) => l.unit === u).map((l) => `<button class="sx-lec${sel.has(l.id) ? " on" : ""}" data-l="${l.id}"><span class="sx-tick"></span><span><strong>${l.id}</strong><small>${esc(l.title)} · ${rows[l.id].length} Q</small></span></button>`).join("")}</div>`).join("")}</div>
        <label class="vz-r sx-count"><span>Questions</span><output>${n}</output><input type="range" min="5" max="${max}" value="${n}" style="--p:${((n - 5) / Math.max(1, max - 5)) * 100}%"></label>
        <div class="sx-row"><button class="btn small" data-build ${sel.size ? "" : "disabled"}>Build deck · ${n} questions</button><span class="sx-muted small">Mixed evenly across the lectures you pick, then shuffled.</span></div></div>`;
      host.querySelectorAll("[data-l]").forEach((b) => (b.onclick = () => { sel.has(b.dataset.l) ? sel.delete(b.dataset.l) : sel.add(b.dataset.l); paint(); }));
      const r = host.querySelector("input[type=range]");
      r.oninput = () => { n = +r.value; r.style.setProperty("--p", `${((n - 5) / Math.max(1, +r.max - 5)) * 100}%`); host.querySelector("output").textContent = n; host.querySelector("[data-build]").textContent = `Build deck · ${n} questions`; };
      host.querySelector("[data-build]").onclick = build;
    }
    async function build() {
      const ids = [...sel], per = Math.ceil(n / ids.length);
      const picked = shuffle(ids.flatMap((id) => shuffle(rows[id].slice()).slice(0, per))).slice(0, n);
      const buf = await fetch(`kahoot/template.xlsx?v=${v}`).then((r) => r.arrayBuffer());
      const blob = await xlsxWithRows(buf, picked);
      const a = Object.assign(document.createElement("a"), { href: URL.createObjectURL(blob), download: `game-night_${ids.join("-")}_${picked.length}q.xlsx` });
      document.body.append(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 4000);
    }
    paint();
  })();

  // a tiny zip reader/writer: inflate the template, swap in our rows, store it back uncompressed
  const CRC = (() => { const t = new Uint32Array(256); for (let n = 0; n < 256; n++) { let c = n; for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1; t[n] = c >>> 0; } return t; })();
  const crc32 = (b) => { let c = 0xffffffff; for (let i = 0; i < b.length; i++) c = CRC[(c ^ b[i]) & 255] ^ (c >>> 8); return (c ^ 0xffffffff) >>> 0; };
  async function inflate(bytes) { return new Uint8Array(await new Response(new Blob([bytes]).stream().pipeThrough(new DecompressionStream("deflate-raw"))).arrayBuffer()); }
  async function xlsxWithRows(buf, rows) {
    const u8 = new Uint8Array(buf), dv = new DataView(buf);
    let e = u8.length - 22; while (dv.getUint32(e, true) !== 0x06054b50) e--;
    const count = dv.getUint16(e + 10, true); let p = dv.getUint32(e + 16, true);
    const files = [];
    for (let i = 0; i < count; i++) {
      const method = dv.getUint16(p + 10, true), csize = dv.getUint32(p + 20, true), nlen = dv.getUint16(p + 28, true), xlen = dv.getUint16(p + 30, true), clen = dv.getUint16(p + 32, true), off = dv.getUint32(p + 42, true);
      const name = new TextDecoder().decode(u8.subarray(p + 46, p + 46 + nlen));
      const lstart = off + 30 + dv.getUint16(off + 26, true) + dv.getUint16(off + 28, true), raw = u8.subarray(lstart, lstart + csize);
      files.push({ name, data: method === 8 ? await inflate(raw) : raw.slice() });
      p += 46 + nlen + xlen + clen;
    }
    const x = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
    const sheet = files.find((f) => f.name === "xl/worksheets/sheet1.xml");
    let xml = new TextDecoder().decode(sheet.data);
    const s0 = xml.indexOf("<sheetData>") + 11, s1 = xml.indexOf("</sheetData>");
    const keep = (xml.slice(s0, s1).match(/<row r="[1-8]"[\s\S]*?<\/row>/g) || []).join("");
    const str = (ref, t) => `<c r="${ref}" s="14" t="inlineStr"><is><t xml:space="preserve">${x(t)}</t></is></c>`;
    const body = rows.map((r, i) => { const n = 9 + i; return `<row r="${n}" spans="1:27" ht="34"><c r="A${n}" s="11"><v>${i + 1}</v></c>${["B", "C", "D", "E", "F"].map((c, k) => str(c + n, r[k])).join("")}<c r="G${n}" s="14"><v>${r[5]}</v></c>${str("H" + n, r[6])}</row>`; }).join("");
    xml = xml.slice(0, s0) + keep + body + xml.slice(s1);
    sheet.data = new TextEncoder().encode(xml);
    // write: local headers + data, then the central directory (method 0 = stored)
    const enc = new TextEncoder(), parts = [], central = []; let offset = 0;
    for (const f of files) {
      const nm = enc.encode(f.name), crc = crc32(f.data), h = new DataView(new ArrayBuffer(30));
      h.setUint32(0, 0x04034b50, true); h.setUint16(4, 20, true); h.setUint32(14, crc, true); h.setUint32(18, f.data.length, true); h.setUint32(22, f.data.length, true); h.setUint16(26, nm.length, true);
      parts.push(new Uint8Array(h.buffer), nm, f.data);
      const c = new DataView(new ArrayBuffer(46));
      c.setUint32(0, 0x02014b50, true); c.setUint16(4, 20, true); c.setUint16(6, 20, true); c.setUint32(16, crc, true); c.setUint32(20, f.data.length, true); c.setUint32(24, f.data.length, true); c.setUint16(28, nm.length, true); c.setUint32(42, offset, true);
      central.push(new Uint8Array(c.buffer), nm);
      offset += 30 + nm.length + f.data.length;
    }
    const csize = central.reduce((a, b) => a + b.length, 0), end = new DataView(new ArrayBuffer(22));
    end.setUint32(0, 0x06054b50, true); end.setUint16(8, files.length, true); end.setUint16(10, files.length, true); end.setUint32(12, csize, true); end.setUint32(16, offset, true);
    return new Blob([...parts, ...central, new Uint8Array(end.buffer)], { type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" });
  }

  // ---------------------------------------------------------------- 6 · head-to-head (pass the device: each player locks in, then both are revealed)
  (function h2h() {
    const host = $("h2h-app");
    const units = [...new Set(CFG.lectures.map((l) => l.unit))];
    let unit = units.includes(curUnit) ? curUnit : units[units.length - 1], names = store.get("sk:h2h:names", ["Player 1", "Player 2"]);
    const rec = () => store.get("sk:h2h:log", []);
    host.innerHTML = `<div class="sx-panel sx-h2h-set"><div class="sx-names"><label><span class="sx-dotp a"></span><input value="${esc(names[0])}" maxlength="20" aria-label="Player 1 name"></label><span class="sx-vs">vs</span><label><span class="sx-dotp b"></span><input value="${esc(names[1])}" maxlength="20" aria-label="Player 2 name"></label></div>
      <div class="sx-row"><div class="seg" role="group" aria-label="Unit">${units.map((u) => `<button data-u="${u}" class="${u === unit ? "on" : ""}">Unit ${u}</button>`).join("")}</div><button class="btn small" data-go>Start · 10 questions</button></div>
      ${rec().length ? `<p class="sx-muted small">Last game: ${esc(rec()[0].text)}</p>` : ""}</div>`;
    host.querySelectorAll("[data-u]").forEach((b) => (b.onclick = () => { unit = +b.dataset.u; host.querySelectorAll("[data-u]").forEach((x) => x.classList.toggle("on", x === b)); }));
    host.querySelector("[data-go]").onclick = async () => {
      names = [...host.querySelectorAll(".sx-names input")].map((i, k) => i.value.trim() || `Player ${k + 1}`); store.set("sk:h2h:names", names);
      const qs = shuffle((await bank()).filter((x) => x.unit === unit && x.stem.length < 260)).slice(0, 10);
      if (qs.length) play(qs);
    };
    function play(qs) {
      const o = document.createElement("div"); o.className = "qm sx-h2h"; o.setAttribute("role", "dialog"); o.setAttribute("aria-label", "Head-to-head");
      document.body.append(o); document.documentElement.style.overflow = "hidden";
      let i = 0, turn = 0, picks = [], score = [0, 0];
      const end = () => { o.remove(); document.documentElement.style.overflow = ""; };
      const top = () => `<div class="qm-top"><button class="qm-x" data-x aria-label="Close">✕</button><div class="qm-count">${Math.min(i + 1, qs.length)} <span>/ ${qs.length}</span></div>
        <div class="sx-score"><span class="a">${esc(names[0])} <b>${score[0]}</b></span><span class="b">${esc(names[1])} <b>${score[1]}</b></span></div><span></span></div>`;
      function draw(reveal) {
        const x = qs[i], L = Object.keys(x.options);
        o.innerHTML = top() + `<div class="qm-scroll"><div class="qm-card">${reveal ? "" : `<div class="sx-turn ${turn ? "b" : "a"}">${esc(names[turn])}'s turn${turn ? " · no peeking at the last pick" : ""}</div>`}
          <div class="qm-stem">${md(x.stem)}</div><div class="sx-opts">${L.map((k) => {
            const who = reveal ? [0, 1].filter((p) => picks[p] === k) : [];
            return `<button class="sx-opt${reveal && k === x.answer ? " right" : ""}${reveal && who.length && k !== x.answer ? " wrong" : ""}" data-k="${k}" ${reveal ? "disabled" : ""}><b>${k}</b><span>${md(x.options[k])}</span>${who.map((p) => `<i class="sx-dotp ${p ? "b" : "a"}" title="${esc(names[p])}"></i>`).join("")}</button>`;
          }).join("")}</div>
          ${reveal ? `<p class="sx-why">${md(x.why || "")}</p><div class="sx-row"><button class="btn" data-next>${i + 1 < qs.length ? "Next question →" : "See the winner →"}</button></div>` : ""}</div></div>`;
        o.querySelector("[data-x]").onclick = end;
        if (!reveal) o.querySelectorAll("[data-k]").forEach((b) => (b.onclick = () => {
          picks[turn] = b.dataset.k;
          if (turn === 0) { turn = 1; o.querySelector(".qm-card").animate([{ opacity: 1 }, { opacity: 0, transform: "translateY(6px)" }, { opacity: 1 }], { duration: 380 }); draw(false); }
          else { [0, 1].forEach((p) => { if (picks[p] === x.answer) score[p]++; }); draw(true); }
        }));
        else o.querySelector("[data-next]").onclick = () => { i++; turn = 0; picks = []; i < qs.length ? draw(false) : win(); };
      }
      function win() {
        const w = score[0] === score[1] ? -1 : score[0] > score[1] ? 0 : 1;
        const text = w < 0 ? `${names[0]} and ${names[1]} tied ${score[0]}–${score[1]}` : `${names[w]} won ${Math.max(...score)}–${Math.min(...score)}`;
        store.set("sk:h2h:log", [{ text, date: today }, ...rec()].slice(0, 20));
        o.innerHTML = `<div class="qm-scroll"><div class="qm-card sx-win"><div class="sx-k">Unit ${unit} · 10 questions</div><h2 class="${w < 0 ? "" : w ? "b" : "a"}">${w < 0 ? "It's a tie." : `${esc(names[w])} wins.`}</h2>
          <div class="sx-final"><span class="a">${esc(names[0])}<b>${score[0]}</b></span><span class="b">${esc(names[1])}<b>${score[1]}</b></span></div>
          <div class="sx-row"><button class="btn" data-again>Rematch</button><button class="btn ghost" data-x>Done</button></div></div></div>`;
        o.querySelector("[data-x]").onclick = end;
        o.querySelector("[data-again]").onclick = async () => { end(); play(shuffle((await bank()).filter((x) => x.unit === unit && x.stem.length < 260)).slice(0, 10)); };
      }
      draw(false);
    }
  })();
})();
