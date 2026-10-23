// Small shared behaviors: theme toggle, cram-sheet hide/reveal, tap-to-answer self-tests,
// objective checklist. Saved settings live in this browser only.
(function () {
  const store = {
    get(k, d) { try { const v = localStorage.getItem(k); return v === null ? d : JSON.parse(v); } catch { return d; } },
    set(k, v) { try { localStorage.setItem(k, JSON.stringify(v)); } catch { /* private mode: just don't save */ } },
  };

  // ---- settings (gear in the top bar): theme, accent, text size, motion, and hiding clutter. Saved in this browser.
  const root = document.documentElement;
  const applyTheme = (t) => { if (t === "auto") root.removeAttribute("data-theme"); else root.setAttribute("data-theme", t); };
  let theme = store.get("theme", "auto");
  applyTheme(theme);
  const prefs = store.get("prefs", {});
  const setPref = (k, v, def) => { if (v === def) delete prefs[k]; else prefs[k] = v; store.set("prefs", prefs); if (v === def) root.removeAttribute("data-p" + k); else root.setAttribute("data-p" + k, v); };
  const gear = document.querySelector(".set-btn");
  if (gear) {
    const pop = document.createElement("div");
    pop.className = "set-pop"; pop.setAttribute("role", "dialog"); pop.setAttribute("aria-label", "Settings");
    const seg = (k, opts, cur) => `<div class="seg set-seg" data-k="${k}">${opts.map(([v, l]) => `<button data-v="${v}" class="${v === cur ? "on" : ""}">${l}</button>`).join("")}</div>`;
    const tog = (k, label, on) => `<label class="set-tog"><span>${label}</span><input type="checkbox" data-t="${k}" ${on ? "checked" : ""}><i></i></label>`;
    const draw = () => {
      pop.innerHTML = `<div class="set-h">Settings</div>
        <div class="set-g"><div class="set-l">Appearance</div>${seg("theme", [["auto", "Auto"], ["light", "Light"], ["dark", "Dark"]], theme)}
          <div class="set-row"><span>Accent</span><div class="set-sw">${[["blue", "#0a84ff"], ["purple", "#8a5cf6"], ["teal", "#14a3b8"], ["graphite", "#8e8e93"]].map(([v, c]) => `<button data-acc="${v}" style="--sw:${c}" class="${(prefs.accent || "blue") === v ? "on" : ""}" aria-label="${v}"></button>`).join("")}</div></div>
          <div class="set-row"><span>Text size</span>${seg("text", [["s", "A"], ["m", "A"], ["l", "A"], ["xl", "A"]], prefs.text || "m")}</div></div>
        <div class="set-g"><div class="set-l">Comfort</div>${tog("motion", "Animations", prefs.motion !== "off")}${tog("glow", "Background glow", prefs.glow !== "off")}${tog("density", "Compact spacing", prefs.density === "compact")}</div>
        <div class="set-g"><div class="set-l">Show on pages</div>${tog("sk", "Sidekick button", prefs.sk !== "off")}${tog("cites", "Slide & page citations", prefs.cites !== "off")}${tog("prog", "Reading progress bar", prefs.prog !== "off")}</div>
        <div class="set-g set-data"><button data-backup>Back up</button><button data-restore>Restore</button><button data-reset>Reset progress</button></div>
        <div class="set-foot">Saved only in this browser · <kbd>/</kbd> Sidekick · <kbd>Esc</kbd> close</div>`;
      pop.querySelectorAll(".set-seg").forEach((g) => g.querySelectorAll("button").forEach((b) => b.onclick = () => {
        if (g.dataset.k === "theme") { theme = b.dataset.v; store.set("theme", theme); applyTheme(theme); } else setPref(g.dataset.k, b.dataset.v, "m");
        draw();
      }));
      pop.querySelectorAll("[data-acc]").forEach((b) => b.onclick = () => { setPref("accent", b.dataset.acc, "blue"); draw(); });
      const OFF = { motion: "off", glow: "off", sk: "off", cites: "off", prog: "off" };
      pop.querySelectorAll("[data-t]").forEach((c) => c.onchange = () => {
        const k = c.dataset.t;
        if (k === "density") setPref(k, c.checked ? "compact" : "normal", "normal"); else setPref(k, c.checked ? "on" : OFF[k], "on");
      });
      pop.querySelector("[data-backup]").onclick = () => document.querySelector(".site-foot [data-backup]")?.click();
      pop.querySelector("[data-restore]").onclick = () => document.querySelector(".site-foot [data-restore]")?.click();
      pop.querySelector("[data-reset]").onclick = () => {
        if (!confirm("Erase all your saved progress on this device (scores, misses, flashcards, notes, grades)? Settings and your AI key stay. Back up first if you might want it.")) return;
        try { Object.keys(localStorage).filter((k) => !["theme", "prefs", "sk:key", "sk:model"].includes(k)).forEach((k) => localStorage.removeItem(k)); } catch { /* blocked */ }
        location.reload();
      };
    };
    document.body.append(pop);
    pop.addEventListener("click", (e) => e.stopPropagation());  // clicks inside redraw the panel; don't treat them as "outside"
    const openPop = (on) => { if (on) draw(); pop.classList.toggle("open", on); gear.setAttribute("aria-expanded", on); };
    gear.addEventListener("click", (e) => { e.stopPropagation(); openPop(!pop.classList.contains("open")); });
    document.addEventListener("click", (e) => { if (pop.classList.contains("open") && !pop.contains(e.target)) openPop(false); });
    document.addEventListener("keydown", (e) => { if (e.key === "Escape" && pop.classList.contains("open")) { openPop(false); gear.focus(); } });
  }

  // reading progress bar
  const bar = document.querySelector(".progress-bar");
  if (bar) {
    const upd = () => { document.body.classList.toggle("at-top", scrollY < 240); const h = document.documentElement.scrollHeight - innerHeight; bar.style.width = (h > 0 ? (scrollY / h) * 100 : 0) + "%"; };
    addEventListener("scroll", upd, { passive: true }); upd();
  }

  // ask the browser to keep this site's saved progress (not clear it to free space)
  navigator.storage?.persist?.().catch(() => {});

  // back up / restore: a private file of your progress that you keep (the AI key is never included)
  document.querySelector("[data-backup]")?.addEventListener("click", () => {
    const data = {};
    try { for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k !== "sk:key") data[k] = localStorage.getItem(k); } } catch { /* storage blocked */ }
    const a = document.createElement("a");
    a.href = URL.createObjectURL(new Blob([JSON.stringify({ app: "clinical-pharmacology", saved: new Date().toISOString(), data }, null, 1)], { type: "application/json" }));
    a.download = `my-study-progress-${new Date().toISOString().slice(0, 10)}.json`;
    document.body.append(a); a.click(); a.remove();
  });
  document.querySelector("[data-restore]")?.addEventListener("click", () => {
    const inp = Object.assign(document.createElement("input"), { type: "file", accept: "application/json,.json" });
    inp.onchange = async () => {
      try {
        const f = JSON.parse(await inp.files[0].text());
        if (f.app !== "clinical-pharmacology" || typeof f.data !== "object") throw 0;
        if (!confirm(`Restore progress saved ${new Date(f.saved).toLocaleString()}? This replaces what's saved in this browser.`)) return;
        Object.entries(f.data).forEach(([k, v]) => { if (k !== "sk:key" && typeof v === "string") localStorage.setItem(k, v); });
        location.reload();
      } catch { alert("That file isn't a progress backup from this site."); }
    };
    inp.click();
  });

  // focus mode: hides navigation, sidebars, and decoration; only the section you're reading stays lit.
  // A slim bar shows where you are, a session timer, and an exit. Esc leaves.
  const sections = document.querySelectorAll(".section");
  if (sections.length > 4 && document.querySelector(".subnav") && "IntersectionObserver" in window) {
    let current = null;
    const bar = document.createElement("div");
    bar.className = "fbar"; bar.setAttribute("role", "status");
    bar.innerHTML = `<span class="fbar-dot" aria-hidden="true"></span><span class="fbar-sec"></span><span class="fbar-time" title="Time in this focus session">0:00</span>
      <span class="fbar-prog" aria-hidden="true"><i></i></span><button class="fbar-x" type="button">Exit <kbd>Esc</kbd></button>`;
    document.body.append(bar);
    const name = (sec) => (sec.querySelector("h2")?.textContent || sec.querySelector(".kicker")?.textContent || "").trim();
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      e.target.classList.toggle("in-view", e.isIntersecting);
      if (e.isIntersecting) { current = e.target; bar.querySelector(".fbar-sec").textContent = name(current); }
    }), { rootMargin: "-35% 0px -45% 0px" });
    sections.forEach((s) => io.observe(s));
    let t0 = 0, tick = null;
    const clock = () => { const sec = Math.floor((Date.now() - t0) / 1000); bar.querySelector(".fbar-time").textContent = `${Math.floor(sec / 60)}:${String(sec % 60).padStart(2, "0")}`; };
    const prog = () => { const h = document.documentElement; bar.querySelector(".fbar-prog i").style.width = `${Math.min(100, (100 * h.scrollTop) / Math.max(1, h.scrollHeight - h.clientHeight))}%`; };
    const btn = document.createElement("button");
    btn.className = "focus-btn"; btn.textContent = "Focus";
    btn.title = "Focus mode: hide everything except what you're reading";
    const set = (on) => {
      const y = current?.getBoundingClientRect().top;
      document.body.classList.toggle("focus", on); btn.setAttribute("aria-pressed", on);
      clearInterval(tick);
      if (on) { t0 = Date.now(); clock(); tick = setInterval(clock, 1000); prog(); }
      if (current && y !== undefined) scrollBy(0, current.getBoundingClientRect().top - y);  // keep your place when chrome hides
    };
    set(store.get("focus:v2", false));
    // cross-fade the whole page when focus turns on/off (where the browser supports it)
    const toggle = (on) => { store.set("focus:v2", on); document.startViewTransition && !matchMedia("(prefers-reduced-motion: reduce)").matches ? document.startViewTransition(() => set(on)) : set(on); };
    btn.addEventListener("click", () => toggle(!document.body.classList.contains("focus")));
    bar.querySelector(".fbar-x").addEventListener("click", () => toggle(false));
    addEventListener("keydown", (e) => { if (e.key === "Escape" && document.body.classList.contains("focus") && !document.querySelector(".qm, .sr-box.open, .sk-panel.open")) toggle(false); });
    addEventListener("scroll", () => { if (document.body.classList.contains("focus")) prog(); }, { passive: true });
    document.querySelector(".subnav-tools")?.append(btn);
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

  // scroll reveal + count-up numbers (skipped for reduced motion)
  const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
  const countUp = (el) => {
    const to = +el.dataset.count; if (calm || !to) return;
    const t0 = performance.now(), dur = 1100;
    const step = (t) => { const k = Math.min(1, (t - t0) / dur); el.textContent = Math.round(to * (1 - Math.pow(1 - k, 3))); if (k < 1) requestAnimationFrame(step); };
    requestAnimationFrame(step);
  };
  if ("IntersectionObserver" in window) {
    const ro = new IntersectionObserver((es) => es.forEach((e) => {
      if (!e.isIntersecting) return;
      e.target.classList.add("in");
      e.target.querySelectorAll("[data-count]").forEach(countUp);
      ro.unobserve(e.target);
    }), { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    document.querySelectorAll(".appear").forEach((el) => ro.observe(el));
  } else document.querySelectorAll(".appear").forEach((el) => el.classList.add("in"));

  // home: show the current lecture (latest one on or before today) and label it Today / This week / Last lecture
  const panels = [...document.querySelectorAll(".now-panel")];
  if (panels.length) {
    const t0 = new Date(); t0.setHours(0, 0, 0, 0);
    const past = panels.filter((p) => new Date(p.dataset.date + "T00:00") <= t0);
    const cur = past.pop() || panels[0], d = Math.round((t0 - new Date(cur.dataset.date + "T00:00")) / 864e5);
    cur.hidden = false;
    const k = cur.querySelector("[data-now-kicker]");
    if (k) k.textContent = d === 0 ? "Today's lecture" : d < 0 ? "Next lecture" : d <= 6 ? "This week's lecture" : "Latest lecture";
    if (cur.querySelector(".progress")?.innerHTML.trim()) cur.querySelector(".now-empty")?.remove();
  }

  // home teaser: the most recent lecture's two-sentence pitch (switches on each class day, no rebuild needed)
  const td = document.getElementById("teaser-data"), tp = document.getElementById("home-teaser");
  if (td && tp) {
    const list = JSON.parse(td.textContent), t = new Date(); t.setHours(23, 59, 59, 0);
    const pick = list.filter((x) => new Date(x.date + "T00:00") <= t).pop() || list[0];
    if (pick) tp.textContent = pick.text;
  }

  // home: "coming up" cards, computed in the browser so they stay current without a rebuild
  const hd = document.getElementById("home-data"), hu = document.getElementById("home-up");
  if (hd && hu) {
    const D = JSON.parse(hd.textContent), now = new Date(); now.setHours(0, 0, 0, 0);
    const day = (s) => new Date(s + "T00:00"), days = (s) => Math.round((day(s) - now) / 864e5);
    const fmt = (s) => day(s).toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" });
    const ex = D.exams.find((e) => day(e.date) >= now);
    const due = D.due.find((d) => day(d.date) >= now && !["exam", "final"].includes(d.kind));
    const dl = store.get("daily:log", {});
    const ymd = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
    let streak = 0;
    const d = new Date(now);
    if (!dl[ymd(d)]) d.setDate(d.getDate() - 1);  // today not done yet: count back from yesterday
    while (dl[ymd(d)] && streak < 366) { streak++; d.setDate(d.getDate() - 1); }
    const num = (n, unit) => `<div class="up-num"><strong>${n}</strong><span>${unit}</span></div>`;
    const card = (href, n, unit, k, t, sub, kc) => `<a class="upcard appear" href="${href}" style="--kc:${kc}">${num(n, unit)}<div><div class="up-k">${k}</div><div class="up-t">${t}</div><div class="up-s">${sub}</div></div></a>`;
    const out = [];
    if (ex) { const d = days(ex.date); out.push(card("syllabus/index.html#schedule", d === 0 ? "Today" : d, d === 0 ? "" : d === 1 ? "day" : "days", "Next exam", ex.label, `${fmt(ex.date)} · ${ex.time}`, "var(--bad)")); }
    if (due) { const d = days(due.date); out.push(card("syllabus/index.html#schedule", d === 0 ? "Today" : d, d === 0 ? "" : d === 1 ? "day" : "days", "Next deadline", due.label.split(" · ")[0], fmt(due.date), "var(--warn)")); }
    const done = dl[ymd(now)];
    out.push(card("review/index.html", done ? "✓" : "10", done ? "done" : "questions", "Today", done ? `Daily 10: ${done.score}/${done.of}` : "Daily 10", streak ? `${streak}-day streak — keep it going` : "A quick, weighted daily set", "var(--good)"));
    hu.innerHTML = out.join("");
    hu.querySelectorAll(".appear").forEach((el, i) => { el.style.setProperty("--d", `${0.45 + i * 0.08}s`); requestAnimationFrame(() => el.classList.add("in")); });
  }

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

  if (qdata && new URLSearchParams(location.search).get("quiz")) {  // ?quiz=1 from the home page
    addEventListener("load", () => window.dpasQuiz?.setup(qdata.items, { title: "Self-test", missed: store.get(missKey, []), onAnswer: (q, L, ok) => record(q.id, ok) }));
  }

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

// Site-wide search (⌘K / Ctrl+K or the Search button): every fact, cram row, question, objective,
// deadline and page. Results open at the right section with the words highlighted.
(function () {
  const root = document.documentElement.dataset.root ?? "";
  let index = null, box, input, list, sel = 0, hits = [];
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const norm = (s) => String(s).toLowerCase().normalize("NFKD").replace(/[̀-ͯ]/g, "").replace(/\*\*/g, "");
  const GROUP_RANK = (g) => (g === "Pages" ? 0 : /Objectives|Summary/.test(g) ? 1 : /Part|Sources|Why|Mnemonic/.test(g) ? 2 : /Cram/.test(g) ? 3 : /Self-test|Exam/.test(g) ? 4 : 5);

  async function load() {
    if (!index) index = await fetch(root + "search.json").then((r) => r.json()).catch(() => []);
    index.forEach((e) => (e._n ||= norm(e.t + " " + e.g + " " + (e.s || ""))));
  }
  function run(q) {
    const terms = norm(q).split(/[^a-z0-9.]+/).filter((t) => t.length > 0);
    if (!terms.length) return [];
    const here = location.pathname.split("/").slice(-2).join("/");
    return index.map((e) => {
      let score = 0;
      for (const t of terms) {
        const re = new RegExp("(^|[^a-z0-9])" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
        if (!re.test(e._n)) return null;
        score += norm(e.t).includes(t) ? 3 : 1;
      }
      if (terms.length > 1 && e._n.includes(terms.join(" "))) score += 4;
      if (e.u.split("#")[0].endsWith(here)) score += 1.5;  // this page first
      return { e, score: score - GROUP_RANK(e.g) * 0.4 - e.t.length / 900 };
    }).filter(Boolean).sort((a, b) => b.score - a.score).slice(0, 40).map((x) => x.e);
  }
  const mark = (text, q) => {
    let h = esc(text.replace(/\*\*/g, ""));
    norm(q).split(/[^a-z0-9.]+/).filter((t) => t.length > 1).forEach((t) => { h = h.replace(new RegExp("(" + t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&") + ")", "ig"), "<mark>$1</mark>"); });
    return h;
  };
  function draw() {
    const q = input.value;
    hits = q.trim() ? run(q) : [];
    sel = 0;
    if (!q.trim()) { list.innerHTML = '<div class="sr-empty">Search every lecture, cram row, question, objective, and deadline. Try <em>CYP3A4</em>, <em>half-life</em>, <em>quiz 2</em>, or <em>loading dose</em>.</div>'; return; }
    if (!hits.length) { list.innerHTML = '<div class="sr-empty">No matches. Not covered in materials — or try fewer words.</div>'; return; }
    let last = "";
    list.innerHTML = hits.map((h, i) => {
      const head = h.g !== last ? `<div class="sr-g">${esc(h.g)}</div>` : "";
      last = h.g;
      const t = h.t.length > 220 ? h.t.slice(0, 218) + "…" : h.t;
      return `${head}<a class="sr" href="${root + h.u + (h.u.includes("#") && h.g !== "Pages" ? "" : "")}" data-i="${i}">${mark(t, q)}${h.s ? ` <span class="cite">${esc(h.s)}</span>` : ""}</a>`;
    }).join("");
    list.querySelectorAll(".sr").forEach((a) => a.addEventListener("click", (e) => { e.preventDefault(); go(+a.dataset.i); }));
    paint();
  }
  function paint() { list.querySelectorAll(".sr").forEach((a, i) => a.classList.toggle("on", i === sel)); list.querySelector(".sr.on")?.scrollIntoView({ block: "nearest" }); }
  function go(i) {
    const h = hits[i]; if (!h) return;
    try { sessionStorage.setItem("find", input.value); } catch { /* ignore */ }
    const [path, hash] = (root + h.u).split("#");
    const samePage = new URL(path, location.href).pathname === location.pathname;
    close();
    if (samePage) { if (hash) location.hash = hash; highlight(input.value, hash); }
    else location.href = root + h.u;
  }
  async function open() {
    if (!box) {
      box = document.createElement("div");
      box.className = "sr-box";
      box.innerHTML = `<div class="sr-panel" role="dialog" aria-label="Search"><div class="sr-in"><svg viewBox="0 0 16 16" width="18" height="18"><circle cx="7" cy="7" r="5" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M11 11l3.5 3.5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
        <input type="search" placeholder="Search…" autocomplete="off" spellcheck="false"><kbd>Esc</kbd></div><div class="sr-list"></div>
        <div class="sr-foot"><span><kbd>↑</kbd><kbd>↓</kbd> move</span><span><kbd>Enter</kbd> open</span><span>Results open at the spot, highlighted</span></div></div>`;
      document.body.append(box);
      input = box.querySelector("input"); list = box.querySelector(".sr-list");
      box.addEventListener("mousedown", (e) => { if (e.target === box) close(); });
      input.addEventListener("input", () => index && draw());
      input.addEventListener("keydown", (e) => {
        if (e.key === "ArrowDown") { sel = Math.min(hits.length - 1, sel + 1); paint(); e.preventDefault(); }
        else if (e.key === "ArrowUp") { sel = Math.max(0, sel - 1); paint(); e.preventDefault(); }
        else if (e.key === "Enter") { go(sel); e.preventDefault(); }
        else if (e.key === "Escape") close();
      });
    }
    requestAnimationFrame(() => box.classList.add("open"));
    document.documentElement.style.overflow = "hidden";
    input.focus(); input.select();  // focus first so fast typing isn't lost while the index loads
    await load();
    draw();
  }
  function close() { box?.classList.remove("open"); document.documentElement.style.overflow = ""; }
  document.querySelectorAll(".search-btn").forEach((b) => b.addEventListener("click", open));
  document.addEventListener("keydown", (e) => {
    if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") { e.preventDefault(); box?.classList.contains("open") ? close() : open(); }
  });

  // Arriving from a search: highlight the words inside the target section and scroll to them
  function highlight(q, hash) {
    const terms = norm(q || "").split(/[^a-z0-9.]+/).filter((t) => t.length > 2);
    if (!terms.length) return;
    const scope = (hash && document.getElementById(hash)) || document.querySelector("main, body");
    document.querySelectorAll("mark.find").forEach((m) => m.replaceWith(...m.childNodes));
    const walk = document.createTreeWalker(scope, NodeFilter.SHOW_TEXT, { acceptNode: (n) => n.parentElement.closest("script, style, .sr-box, .sk-panel") ? NodeFilter.FILTER_REJECT : NodeFilter.FILTER_ACCEPT });
    const re = new RegExp(terms.map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")).join("|"), "i");
    const nodes = [];
    for (let n; (n = walk.nextNode());) if (re.test(n.data)) nodes.push(n);
    let first = null;
    nodes.slice(0, 60).forEach((n) => {
      const parts = n.data.split(new RegExp("(" + re.source + ")", "ig"));
      const frag = document.createDocumentFragment();
      parts.forEach((p, i) => { if (i % 2) { const m = Object.assign(document.createElement("mark"), { className: "find", textContent: p }); first ||= m; frag.append(m); } else if (p) frag.append(p); });
      n.replaceWith(frag);
    });
    if (first) setTimeout(() => first.scrollIntoView({ behavior: "smooth", block: "center" }), 150);
    setTimeout(() => document.querySelectorAll("mark.find").forEach((m) => m.classList.add("fade")), 6000);
  }
  let pending = null;
  try { pending = sessionStorage.getItem("find"); sessionStorage.removeItem("find"); } catch { /* ignore */ }
  if (pending) addEventListener("load", () => highlight(pending, location.hash.slice(1)));
})();
