// Small shared behaviors: theme toggle, cram-sheet hide/reveal, tap-to-answer self-tests,
// objective checklist. Saved settings live in this browser only.
(function () {
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* private mode: just don't save */ } },
  };

  // theme: auto (follow device) -> light -> dark
  const root = document.documentElement;
  const applyTheme = (t) => { if (t === "auto") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", t); };
  let theme = store.get("theme", "auto");
  applyTheme(theme);
  document.querySelectorAll(".theme-btn").forEach((b) => {
    const svg = {
      auto: '<svg viewBox="0 0 16 16"><circle cx="8" cy="8" r="6.5" fill="none" stroke="currentColor" stroke-width="1.5"/><path d="M8 1.5a6.5 6.5 0 0 1 0 13z" fill="currentColor"/></svg>',
      light: '<svg viewBox="0 0 16 16"><circle cx="8" cy="8" r="3.2" fill="currentColor"/><g stroke="currentColor" stroke-width="1.5" stroke-linecap="round"><path d="M8 1v1.6M8 13.4V15M1 8h1.6M13.4 8H15M3 3l1.1 1.1M11.9 11.9 13 13M3 13l1.1-1.1M11.9 4.1 13 3"/></g></svg>',
      dark: '<svg viewBox="0 0 16 16"><path d="M13.5 10.2A6 6 0 0 1 5.8 2.5a6 6 0 1 0 7.7 7.7z" fill="currentColor"/></svg>',
    };
    const icon = () => (b.innerHTML = svg[theme]);
    icon();
    b.title = "Theme: follow device / light / dark";
    b.addEventListener("click", () => { theme = theme === "auto" ? "light" : theme === "light" ? "dark" : "auto"; store.set("theme", theme); applyTheme(theme); icon(); });
  });

  // reading progress bar
  const bar = document.querySelector(".progress-bar");
  if (bar) {
    const upd = () => { document.body.classList.toggle("at-top", scrollY < 240); const h = document.documentElement.scrollHeight - innerHeight; bar.style.width = (h > 0 ? (scrollY / h) * 100 : 0) + "%"; };
    addEventListener("scroll", upd, { passive: true }); upd();
  }

  // focus mode: the section you're reading stays bright, the rest fades back (long pages only)
  const sections = document.querySelectorAll(".section");
  if (sections.length > 4 && "IntersectionObserver" in window) {
    const io = new IntersectionObserver((es) => es.forEach((e) => e.target.classList.toggle("in-view", e.isIntersecting)), { rootMargin: "-35% 0px -45% 0px" });
    sections.forEach((s) => io.observe(s));
    const btn = document.createElement("button");
    btn.className = "focus-btn";
    btn.textContent = "Focus";
    btn.title = "Focus mode: fade everything except the section you're reading";
    const set = (on) => { document.body.classList.toggle("focus", on); btn.setAttribute("aria-pressed", on); };
    set(store.get("focus", true));
    btn.addEventListener("click", () => { const on = !document.body.classList.contains("focus"); store.set("focus", on); set(on); });
    document.querySelector(".theme-btn")?.before(btn);
  }

  // nav highlights the section you're in
  const navLinks = [...document.querySelectorAll(".nav-links a[href^='#']")];
  if (navLinks.length && "IntersectionObserver" in window) {
    const byId = new Map(navLinks.map((a) => [a.getAttribute("href").slice(1), a]));
    const spy = new IntersectionObserver((es) => es.forEach((e) => {
      if (!e.isIntersecting) return;
      navLinks.forEach((a) => a.classList.remove("active"));
      const a = byId.get(e.target.id);
      if (a) {  // keep the active link visible in the nav without scrolling the page
        a.classList.add("active");
        const bar = a.parentElement;
        bar.scrollTo({ left: a.offsetLeft - bar.clientWidth / 2 + a.offsetWidth / 2, behavior: "smooth" });
      }
    }), { rootMargin: "-45% 0px -50% 0px" });
    byId.forEach((_, id) => { const el = document.getElementById(id); if (el) spy.observe(el); });
  }

  // Textbook: open your own Katzung PDF at a printed page (the file stays on this device), or AccessMedicine.
  // Shared with Sidekick through window.dpasTextbook.
  const db = () => new Promise((ok, bad) => { const r = indexedDB.open("dpas", 1); r.onupgradeneeded = () => r.result.createObjectStore("files"); r.onsuccess = () => ok(r.result); r.onerror = () => bad(r.error); });
  const idb = async (mode, fn) => { const d = await db(); return new Promise((ok, bad) => { const t = d.transaction("files", mode); const q = fn(t.objectStore("files")); t.oncomplete = () => ok(q?.result); t.onerror = () => bad(t.error); }); };
  const textbook = {
    get: () => idb("readonly", (st) => st.get("katzung")).catch(() => null),
    pick: () => new Promise((ok) => {
      const input = Object.assign(document.createElement("input"), { type: "file", accept: "application/pdf" });
      input.addEventListener("change", async () => { const f = input.files[0]; if (f) await idb("readwrite", (st) => st.put(f, "katzung")).catch(() => {}); ok(f || null); });
      input.click();
    }),
    async open(page, offset, file) {
      file = file || (await textbook.get()) || (await textbook.pick());
      if (!file) return;
      if (!window.open(URL.createObjectURL(file) + "#page=" + (page + offset), "_blank")) alert("Allow pop-ups to open the textbook.");
    },
  };
  window.dpasTextbook = textbook;
  let pop;
  const closePop = () => { pop?.remove(); pop = null; };
  document.addEventListener("click", (e) => { if (pop && !pop.contains(e.target) && !e.target.closest(".deeper-btn")) closePop(); });
  document.addEventListener("keydown", (e) => { if (e.key === "Escape") closePop(); });
  document.querySelectorAll(".deeper-btn").forEach((btn) => btn.addEventListener("click", async () => {
    if (pop) { closePop(); return; }
    const page = +btn.dataset.page, offset = +btn.dataset.offset, have = await textbook.get();
    pop = document.createElement("div");
    pop.className = "deeper-pop";
    pop.innerHTML = `<div class="small muted">${btn.dataset.label}</div>
      <button data-open>${have ? "Open in my textbook PDF" : "Choose my Katzung PDF…"}<span>${have ? `Jumps to page ${page}` : "Pick it once; it stays on this device only"}</span></button>
      <a href="${btn.dataset.am}" target="_blank" rel="noopener">Find on AccessMedicine<span>School library login · Chapter ${btn.dataset.label.match(/Ch\. (\d+)/)[1]}</span></a>
      ${have ? '<button data-change class="small-link">Use a different PDF</button>' : ""}`;
    btn.after(pop);
    pop.querySelector("[data-open]").addEventListener("click", () => { closePop(); textbook.open(page, offset, have); });
    pop.querySelector("[data-change]")?.addEventListener("click", async () => { closePop(); const f = await textbook.pick(); if (f) textbook.open(page, offset, f); });
  }));

  // cram sheet: hide answers for active recall; tap a cell to peek
  document.querySelectorAll("[data-cram-toggle]").forEach((btn) => {
    const table = document.getElementById(btn.dataset.cramToggle);
    btn.addEventListener("click", () => {
      table.classList.toggle("hide");
      table.querySelectorAll("td.show").forEach((td) => td.classList.remove("show"));
      btn.textContent = table.classList.contains("hide") ? "Show all answers" : "Hide answers (quiz yourself)";
    });
    table.addEventListener("click", (e) => { const td = e.target.closest("td:last-child"); if (td && table.classList.contains("hide")) td.classList.toggle("show"); });
  });

  // self-test misses: a question stays "missed" until you get it right (inline or in focus mode)
  const qdata = (() => { try { return JSON.parse(document.getElementById("quiz-data")?.textContent || "null"); } catch { return null; } })();
  const missKey = qdata ? "miss:" + qdata.lecture : null;
  const record = (id, ok) => {
    if (!missKey) return;
    const m = new Set(store.get(missKey, []));
    ok ? m.delete(id) : m.add(id);
    store.set(missKey, [...m]);
    if (ok) store.set("done:" + qdata.lecture, [...new Set([...store.get("done:" + qdata.lecture, []), id])]);
    renderMisses();
  };
  function renderMisses() {
    const box = document.getElementById("misses");
    if (!box || !qdata) return;
    const ids = store.get(missKey, []), items = qdata.items.filter((q) => ids.includes(q.id));
    box.hidden = !items.length;
    if (!items.length) return;
    box.innerHTML = `<div class="callout trap"><div class="label">Review your misses (${items.length})</div><ul>${items.map((q) =>
      `<li><a href="#${q.id}">${q.stem.length > 110 ? q.stem.slice(0, 108) + "…" : q.stem}</a> ${q.link ? `<a class="jump" href="${q.link.href}">${q.link.label.replace("Study this: ", "")}</a>` : ""}</li>`).join("")}</ul>
      <button class="btn" data-retry-misses style="margin-top:10px">Retry these in focus mode →</button></div>`;
    box.querySelector("[data-retry-misses]").addEventListener("click", () => window.dpasQuiz?.start(items, { title: "Retry: misses", onAnswer: (q, L, ok) => record(q.id, ok) }));
  }
  renderMisses();
  document.querySelectorAll("[data-focus-quiz]").forEach((b) => b.addEventListener("click", () => {
    if (!qdata || !window.dpasQuiz) return;
    window.dpasQuiz.setup(qdata.items, { title: "Self-test", missed: store.get(missKey, []), onAnswer: (q, L, ok) => record(q.id, ok) });
  }));

  // self-test: first tap answers the question and reveals the explanation
  document.querySelectorAll(".q").forEach((q) => {
    q.querySelectorAll(".opt").forEach((opt) => opt.addEventListener("click", () => {
      if (q.classList.contains("answered")) return;
      q.classList.add("answered");
      q.querySelectorAll(".opt").forEach((o) => { if (o.dataset.correct === "1") o.classList.add("right"); });
      if (opt.dataset.correct !== "1") opt.classList.add("wrong");
      if (q.dataset.qid) record(q.dataset.qid, opt.dataset.correct === "1");
    }));
  });

  // objectives checklist, remembered per lecture (older saves were keyed by page path)
  document.querySelectorAll("input[data-check]").forEach((box) => {
    const key = "check:" + (qdata?.lecture || location.pathname) + ":" + box.dataset.check;
    box.checked = store.get(key, store.get("check:" + location.pathname + ":" + box.dataset.check, false));
    box.addEventListener("change", () => store.set(key, box.checked));
  });

  // home page: progress rings per lecture and exam (all from this browser's saved progress)
  const ring = (n, d, label) => { const p = d ? Math.round((100 * n) / d) : 0;
    return `<div class="pring" title="${label}: ${n} of ${d}"><div class="pring-c" style="--p:${p}"><span>${p}%</span></div><div><strong>${n}/${d}</strong><span>${label}</span></div></div>`; };
  document.querySelectorAll("[data-progress]").forEach((card) => {
    const d = card.dataset, lid = d.lid, out = card.querySelector(".progress");
    if (d.progress === "exam") {
      const st = store.get("exam:" + d.slug + ":v1", null), ans = st ? Object.keys(st.answers).length : 0;
      if (ans) out.innerHTML = ring(ans, +d.total, "answered");
      return;
    }
    const objs = d.objs.split(","), checked = objs.filter((o) => store.get("check:" + lid + ":" + o, false)).length;
    const boxes = store.get("sk:fc:" + lid, {}), mine = store.get("sk:mycards:" + lid, []).length;
    const strong = Object.values(boxes).filter((b) => b >= 4).length;
    const done = store.get("done:" + lid, []).length;
    if (checked + strong + done === 0) return;
    out.innerHTML = ring(checked, objs.length, "objectives") + ring(strong, +d.cards + mine, "flashcards strong") + ring(done, +d.qs, "questions right");
  });
})();
