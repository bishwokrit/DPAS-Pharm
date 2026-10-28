// Drug index: search + tag filters, a detail sheet per drug (the drug card — name, class, mechanism, indications,
// contraindications, adverse effects, interactions, patient factors, extra — plus every lecture mention,
// a quiz built from questions that mention it), side-by-side compare, and a drug flashcard drill.
(function () {
  const CFG = JSON.parse(document.getElementById("drug-data").textContent), DR = CFG.drugs;
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const md = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  const slug = (s) => s.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  const cite = (s) => (s ? ` <span class="cite">${esc(s)}</span>` : "");
  const tb = (f) => (f.tb ? '<span class="tag tb">TB</span>' : "");
  const $ = (id) => document.getElementById(id);
  let tag = "", q = "", picked = [];
  // every card has the same fields, in this order (work/drugs.py SECTIONS)
  const SECS = [["moa", "Mechanism of action"], ["ind", "Indications"], ["contra", "Contraindications"], ["ae", "Adverse effects"],
    ["ix", "Clinically significant interactions"], ["pt", "Distinguishing characteristics / patient-specific factors"], ["extra", "Extra information"]];
  const NONE = '<p class="dx-none">Not covered in the lectures or assigned reading yet.</p>';
  const clsLine = (d) => (d.cls === "Not covered in materials" ? '<span class="muted">Not covered yet — taught in a later unit</span>' : `${esc(d.cls)}${cite(d.cls_src)}`);
  const secFacts = (d, k) => d.facts.filter((f) => (f.sec || "extra") === k);
  const lis = (fs) => (fs.length ? `<ul>${fs.map((f) => `<li>${tb(f)}${md(f.text)}${cite(f.src)}</li>`).join("")}</ul>` : NONE);
  // the drug card: generic name (and brand names) · class · then each field
  const card = (d) => `<dl class="dx-card">
      <div class="dx-row"><dt>Generic name</dt><dd><strong>${esc(d.name)}</strong>${d.aliases.filter((a) => /^[A-Z]/.test(a) && a !== d.name && !/^NAPQI$/.test(a)).length ? ` <span class="muted">(${d.aliases.filter((a) => /^[A-Z]/.test(a) && !/^NAPQI$/.test(a)).map(esc).join(", ")})</span>` : ""}</dd></div>
      <div class="dx-row"><dt>Drug class</dt><dd>${clsLine(d)}</dd></div>
      ${SECS.map(([k, label]) => `<div class="dx-row"><dt>${label}</dt><dd>${lis(secFacts(d, k))}</dd></div>`).join("")}
    </dl>`;

  // ---- sorting: A–Z, Z–A, by drug class (grouped), by unit (grouped), most mentioned, most complete card; remembered per browser
  const sto = { get: (k, d) => { try { return localStorage.getItem(k) ?? d; } catch { return d; } }, set: (k, v) => { try { localStorage.setItem(k, v); } catch { /* */ } } };
  let sort = sto.get("dx:sort", "az");
  // a short family name for grouping (the full class stays on each card)
  const family = (d) => {
    const c = d.cls;
    if (c === "Not covered in materials") return "Class taught in a later unit";
    if (/Biologic DMARD/.test(c)) return "Biologic DMARDs";
    if (/DMARD/.test(c)) return "Conventional & targeted DMARDs";
    if (/NSAID/.test(c) && !/not an NSAID/.test(c)) return "NSAIDs";
    if (/analgesic|opioid|antipyretic/i.test(c)) return "Analgesics & opioids";
    if (/CYP|inducer|inhibitor/.test(c)) return "CYP inducers & inhibitors";
    if (/Anticoagulant|Antiplatelet|reversal/i.test(c)) return "Anticoagulants, antiplatelets & reversal";
    if (/agonist|antagonist/i.test(c)) return "Receptor agonists & antagonists";
    if (/Antidote/.test(c)) return "Antidotes";
    return c;
  };
  const filled = (d) => SECS.filter(([k]) => secFacts(d, k).length).length + (d.cls === "Not covered in materials" ? 0 : 1);
  const byName = (a, b) => a.name.localeCompare(b.name);
  const SORTS = {
    az: [byName, null], za: [(a, b) => b.name.localeCompare(a.name), null],
    class: [(a, b) => (family(a) === "Class taught in a later unit") - (family(b) === "Class taught in a later unit") || family(a).localeCompare(family(b)) || byName(a, b), family],
    unit: [(a, b) => a.unit - b.unit || byName(a, b), (d) => `Unit ${d.unit}`],
    mentions: [(a, b) => b.n_mentions - a.n_mentions || byName(a, b), null],
    complete: [(a, b) => filled(b) - filled(a) || byName(a, b), null],
  };
  if (!SORTS[sort]) sort = "az";
  $("dx-sort").value = sort;
  $("dx-sort").addEventListener("change", (e) => { sort = e.target.value; sto.set("dx:sort", sort); draw(); });

  // ---- grid
  function draw() {
    const qq = q.toLowerCase();
    const [cmp, group] = SORTS[sort];
    const list = DR.filter((d) => (!tag || d.tags.includes(tag)) &&
      (!qq || (d.name + " " + d.cls + " " + d.aliases.join(" ") + " " + d.tags.join(" ") + " " + d.facts.map((f) => f.text).join(" ")).toLowerCase().includes(qq))).sort(cmp);
    let last = null;
    $("dx-grid").innerHTML = list.map((d, i) => {
      const g = group ? group(d) : null, head = g && g !== last ? `<h3 class="dx-group">${esc(g)} <span>${list.filter((x) => group(x) === g).length}</span></h3>` : "";
      last = g;
      return head + `<button class="dx-tile appear in" style="--d:${Math.min(i, 12) * 0.025}s" data-name="${esc(d.name)}" id="${slug(d.name)}">
      <span class="dx-pick ${picked.includes(d.name) ? "on" : ""}" data-pick title="Add to compare">${picked.includes(d.name) ? "✓" : "+"}</span>
      <span class="dx-unit">Unit ${d.unit}</span><span class="dx-name">${esc(d.name)}</span><span class="dx-cls">${d.cls === "Not covered in materials" ? "" : esc(d.cls)}</span>
      <span class="dx-tags-mini">${d.tags.slice(0, 3).map((t) => `<i>${esc(t)}</i>`).join("")}</span>
      <span class="dx-meta">${filled(d)} of 8 fields · ${d.n_mentions} mention${d.n_mentions === 1 ? "" : "s"} in lectures</span></button>`;
    }).join("");
    $("dx-empty").hidden = list.length > 0;
    $("dx-grid").querySelectorAll(".dx-tile").forEach((b) => b.addEventListener("click", (e) => {
      if (e.target.closest("[data-pick]")) { togglePick(b.dataset.name); return; }
      open(b.dataset.name, b);
    }));
  }
  $("dx-q").addEventListener("input", (e) => { q = e.target.value; draw(); });
  document.querySelectorAll("#dx-tags [data-tag]").forEach((b) => b.addEventListener("click", () => {
    tag = b.dataset.tag; document.querySelectorAll("#dx-tags [data-tag]").forEach((x) => x.classList.toggle("on", x === b)); draw();
  }));

  // ---- compare (pick two): a floating tray shows your picks
  const tray = document.createElement("div");
  tray.className = "dx-tray"; document.body.append(tray);
  function paintTray() {
    tray.classList.toggle("on", picked.length > 0);
    tray.innerHTML = `<span class="dx-tray-l">Compare</span>${picked.map((n) => `<span class="dx-chip">${esc(n)}<button data-un="${esc(n)}" aria-label="Remove">×</button></span>`).join("")}
      ${picked.length < 2 ? '<span class="dx-tray-hint">Pick one more</span>' : ""}<button class="btn small" data-go ${picked.length < 2 ? "disabled" : ""}>Compare →</button>`;
    tray.querySelectorAll("[data-un]").forEach((x) => x.onclick = () => togglePick(x.dataset.un));
    tray.querySelector("[data-go]").onclick = () => compare();
  }
  function togglePick(name) {
    picked = picked.includes(name) ? picked.filter((n) => n !== name) : [...picked, name].slice(-2);
    const b = $("dx-cmp"); b.disabled = picked.length < 2; b.textContent = `Compare (${picked.length}/2)`;
    paintTray(); draw();
  }
  $("dx-cmp").addEventListener("click", () => compare());
  function compare() {
    const [a, b] = picked.map((n) => DR.find((d) => d.name === n));
    if (!a || !b) return;
    const tags = [...new Set([...a.tags, ...b.tags])].sort((x, y) => (b.tags.includes(y) && a.tags.includes(y)) - (b.tags.includes(x) && a.tags.includes(x)));
    const mark = (d, t) => d.tags.includes(t) ? '<span class="dx-yes">●</span>' : '<span class="dx-no">—</span>';
    // field by field, side by side: the same row for both drugs
    const fieldRows = [["Drug class", (d) => clsLine(d)], ...SECS.map(([k, label]) => [label, (d) => lis(secFacts(d, k))])]
      .map(([label, f]) => `<div class="dx-cmp-row"><div class="dx-cmp-k">${label}</div><div class="dx-cmp-v">${f(a)}</div><div class="dx-cmp-v">${f(b)}</div></div>`).join("");
    sheet(`<div class="dx-sh-top"><div><div class="kicker">Compare</div><h2>${esc(a.name)} <span class="dx-vs">vs</span> ${esc(b.name)}</h2></div><span class="dx-ctl"><button class="sk-x" data-expand aria-label="Expand to full screen" title="Full screen">⤢</button><button class="sk-x" data-close aria-label="Close">✕</button></span></div>
      <div class="dx-swap">${[a, b].map((d, i) => `<label><span class="small muted">${i ? "Against" : "Drug"}</span><select data-swap="${i}" aria-label="${i ? "Second" : "First"} drug in the comparison">${DR.filter((x) => x.name !== (i ? a : b).name).map((x) => `<option ${x.name === d.name ? "selected" : ""}>${esc(x.name)}</option>`).join("")}</select></label>`).join('<span class="dx-vs">vs</span>')}</div>
      <table class="dx-matrix"><thead><tr><th></th><th>${esc(a.name)}</th><th>${esc(b.name)}</th></tr></thead><tbody>
        ${tags.map((t) => `<tr class="${a.tags.includes(t) && b.tags.includes(t) ? "both" : ""}"><td>${esc(t)}</td><td>${mark(a, t)}</td><td>${mark(b, t)}</td></tr>`).join("")}
        <tr><td>Lecture mentions</td><td>${a.n_mentions}</td><td>${b.n_mentions}</td></tr></tbody></table>
      <div class="dx-acts"><button class="btn small" data-qboth>Quiz me on both</button></div>
      <h4>Field by field</h4><div class="dx-cmp-fields"><div class="dx-cmp-row dx-cmp-head"><div></div><div>${esc(a.name)} <a class="dx-utd-s" href="${esc(a.utd)}" target="_blank" rel="noopener noreferrer">UpToDate ↗</a></div><div>${esc(b.name)} <a class="dx-utd-s" href="${esc(b.utd)}" target="_blank" rel="noopener noreferrer">UpToDate ↗</a></div></div>${fieldRows}</div>`);
    $("dx-sheet-in").querySelector("[data-qboth]").onclick = () => quizFor({ name: `${a.name} + ${b.name}`, pattern: `${a.pattern}|${b.pattern}` });
    // swap either drug in place: no need to close the comparison and start over
    $("dx-sheet-in").querySelectorAll("[data-swap]").forEach((sel) => sel.addEventListener("change", () => {
      picked[+sel.dataset.swap] = sel.value; paintTray(); draw(); compare();
    }));
  }

  // ---- detail sheet
  const calm = matchMedia("(prefers-reduced-motion: reduce)").matches;
  let molKill = null;  // the drug's structure, faint in the panel's top-right corner
  function sheet(htmlStr, from) {
    molKill?.(); molKill = null;
    const sh = $("dx-sheet"), wasOpen = sh.classList.contains("open");
    $("dx-sheet-in").innerHTML = htmlStr; sh.hidden = false; $("dx-scrim").hidden = false; sh.scrollTop = 0;
    if (from && !calm && !wasOpen && sh.animate) {
      // the card flips over and grows into the side panel
      sh.style.transition = "none"; sh.classList.add("open");
      const a = from.getBoundingClientRect(), z = sh.getBoundingClientRect();
      const dx = a.left + a.width / 2 - (z.left + z.width / 2), dy = a.top + a.height / 2 - (z.top + z.height / 2);
      sh.animate([
        { transform: `perspective(1400px) translate(${dx}px, ${dy}px) scale(${a.width / z.width}, ${a.height / z.height}) rotateY(-100deg)`, opacity: 0, borderRadius: "18px" },
        { transform: `perspective(1400px) translate(${dx * 0.35}px, ${dy * 0.35}px) scale(${0.6 + 0.4 * a.width / z.width}, ${0.75 + 0.25 * a.height / z.height}) rotateY(-40deg)`, opacity: 1, offset: 0.45 },
        { transform: "none", opacity: 1, borderRadius: "0px" }], { duration: 620, easing: "cubic-bezier(.2,.8,.2,1)" }).onfinish = () => (sh.style.transition = "");
      from.animate([{ transform: "perspective(900px) rotateY(0)" }, { transform: "perspective(900px) rotateY(90deg)", opacity: 0, offset: 0.5 }, { transform: "perspective(900px) rotateY(0)", opacity: 1 }], { duration: 700, easing: "ease-in-out" });
      $("dx-scrim").classList.add("open");
    } else requestAnimationFrame(() => { sh.classList.add("open"); $("dx-scrim").classList.add("open"); });
    document.documentElement.style.overflow = "hidden";
    $("dx-sheet-in").querySelectorAll("[data-close]").forEach((x) => x.addEventListener("click", close));
    // expand: the panel fills the screen (remembered); tap again to go back to the side panel
    const full = (on) => { sh.classList.toggle("full", on); try { localStorage.setItem("dx:full", on ? "1" : ""); } catch { /* */ }
      $("dx-sheet-in").querySelectorAll("[data-expand]").forEach((x) => { x.textContent = on ? "⤡" : "⤢"; x.title = on ? "Back to side panel" : "Full screen"; x.setAttribute("aria-label", x.title); }); };
    $("dx-sheet-in").querySelectorAll("[data-expand]").forEach((x) => x.addEventListener("click", () => full(!sh.classList.contains("full"))));
    full((() => { try { return !!localStorage.getItem("dx:full"); } catch { return false; } })());
  }
  function close() {
    molKill?.(); molKill = null;
    $("dx-sheet").classList.remove("open"); $("dx-scrim").classList.remove("open");
    setTimeout(() => { $("dx-sheet").hidden = true; $("dx-scrim").hidden = true; }, 280);
    document.documentElement.style.overflow = "";
    if (location.hash) history.replaceState(null, "", location.pathname);
  }
  $("dx-scrim").addEventListener("click", close);
  document.addEventListener("keydown", (e) => { if (e.key === "Escape" && !$("dx-sheet").hidden) close(); });

  function open(name, from) {
    const d = DR.find((x) => x.name === name);
    if (!d) return;
    history.replaceState(null, "", "#" + slug(d.name));
    sheet(`<div class="dx-sh-top"><div><div class="kicker">Unit ${d.unit}</div><h2>${esc(d.name)}</h2>
      ${d.cls === "Not covered in materials" ? '<div class="muted small">Drug class: covered in a later unit</div>' : `<div class="muted">${esc(d.cls)}${cite(d.cls_src)}</div>`}</div><span class="dx-ctl"><button class="sk-x" data-expand aria-label="Expand to full screen" title="Full screen">⤢</button><button class="sk-x" data-close aria-label="Close">✕</button></span></div>
      <div class="dx-tags-mini" style="margin:12px 0 4px">${d.tags.map((t) => `<i>${esc(t)}</i>`).join("")}</div>
      <div class="dx-acts"><button class="btn small" data-quiz>Quiz me on ${esc(d.name)}</button><a class="btn ghost small dx-utd" href="${esc(d.utd)}" target="_blank" rel="noopener noreferrer" title="Opens UpToDate in a new tab (needs your school or personal subscription)">UpToDate ↗</a><select data-vs aria-label="Compare with another drug"><option value="">Compare with…</option>${DR.filter((x) => x.name !== d.name).map((x) => `<option>${esc(x.name)}</option>`).join("")}</select></div>
      <h4>Drug card</h4><div class="dx-facts">${card(d)}</div>
      <h4>In your lectures (${d.n_mentions})</h4>${d.mentions.length ? `<ul class="dx-ment">${d.mentions.map((m) => `<li><span class="small muted">${esc(m.lid)} · ${esc(m.where)}</span><div>${m.tb ? '<span class="tag tb">TB</span>' : ""}${md(m.text)}${cite(m.src)}</div><a class="jump" href="${esc(m.href)}">Open →</a></li>`).join("")}</ul>` : '<p class="muted small">Only in the assigned reading so far.</p>'}
      <p class="small muted" style="margin-top:16px">Every field comes from the lecture slides or the assigned textbook pages (<span class="tag tb">TB</span> = textbook only). Fields fill in as later units teach the drug.</p>`, from);
    const s = $("dx-sheet-in");
    window.dpasMolData?.("../").then((M) => { if (M[d.name] && s.querySelector("h2")?.textContent === d.name && !molKill) molKill = window.dpasMol3d($("dx-sheet"), $("dx-sheet"), M[d.name], { size: innerWidth < 700 ? 180 : 260 }); });
    // Sketch mode only: your one-line memory hook for this drug, editable right here
    const sk = (() => { try { return JSON.parse(localStorage.getItem("sketch")) === true; } catch { return false; } })();
    if (sk) {
      const H = (() => { try { return JSON.parse(localStorage.getItem("sk:hooks")) || {}; } catch { return {}; } })();
      s.querySelector(".dx-facts").insertAdjacentHTML("afterend", `<div class="dx-hook"><span class="dx-hook-k">Your hook</span><input maxlength="160" placeholder="One line, your own words…" value="${esc(H[d.name] || "")}" aria-label="Your memory hook for ${esc(d.name)}"></div>`);
      s.querySelector(".dx-hook input").addEventListener("input", (e) => { const h = (() => { try { return JSON.parse(localStorage.getItem("sk:hooks")) || {}; } catch { return {}; } })(); e.target.value.trim() ? (h[d.name] = e.target.value.trim()) : delete h[d.name]; try { localStorage.setItem("sk:hooks", JSON.stringify(h)); } catch { /* */ } });
    }
    s.querySelector("[data-quiz]").addEventListener("click", () => quizFor(d));
    s.querySelector("[data-vs]").addEventListener("change", (e) => { if (e.target.value) { picked = [d.name, e.target.value]; paintTray(); draw(); compare(); } });
  }

  // ---- quiz: every self-test and exam question that mentions this drug
  let bank = null;
  async function loadBank() {
    if (bank) return bank;
    bank = [];
    await Promise.all(CFG.lectures.map((lid) => fetch(`../${lid}/kb.json${document.documentElement.dataset.v ? "?v=" + document.documentElement.dataset.v : ""}`).then((r) => r.json()).then((kb) =>
      kb.quiz.forEach((x) => bank.push({ ...x, id: `${lid}:${x.id}`, link: x.link ? { ...x.link, href: `../${lid}/index.html${x.link.href}` } : null }))).catch(() => {})));
    await Promise.all(CFG.exams.map((e) => fetch(`../exams/${e}/quiz.json${document.documentElement.dataset.v ? "?v=" + document.documentElement.dataset.v : ""}`).then((r) => r.json()).then((qs) =>
      qs.forEach((x) => bank.push({ ...x, link: x.link ? { ...x.link, href: x.link.href.replace(/^\.\.\/\.\.\//, "../") } : null }))).catch(() => {})));
    return bank;
  }
  async function quizFor(d) {
    const re = new RegExp(`\\b(${d.pattern})\\b`, "i");
    const qs = (await loadBank()).filter((x) => re.test(x.stem + " " + Object.values(x.options).join(" ") + " " + (x.why || "")));
    if (!qs.length) { alert(`No practice questions mention ${d.name} yet.`); return; }
    close();
    window.dpasQuiz?.start(qs.sort(() => Math.random() - 0.5).slice(0, 15), { title: `${d.name} · ${qs.length} question${qs.length > 1 ? "s" : ""}` });
  }

  // ---- drug flashcards: name → class + top facts
  $("dx-drill").addEventListener("click", () => {
    const cards = DR.filter((d) => !tag || d.tags.includes(tag)).sort(() => Math.random() - 0.5);
    let i = 0;
    const el = document.createElement("div");
    el.className = "qm"; document.body.append(el); document.documentElement.style.overflow = "hidden";
    const end = () => { el.remove(); document.documentElement.style.overflow = ""; document.removeEventListener("keydown", key, true); };
    const drawCard = () => {
      if (i >= cards.length) { el.innerHTML = `<div class="qm-scroll"><div class="qm-card" style="text-align:center;padding-top:15vh"><div class="qm-score">${cards.length} drugs reviewed</div><button class="btn" data-x style="margin-top:16px">Done</button></div></div>`; el.querySelector("[data-x]").onclick = end; return; }
      const d = cards[i];
      el.innerHTML = `<div class="qm-top"><button class="qm-x" data-x>✕</button><div class="qm-count">${i + 1} <span>/ ${cards.length}</span></div><div class="qm-title">Drug flashcards${tag ? " · " + esc(tag) : ""}</div><span></span></div>
        <div class="qm-scroll"><div class="qm-card"><div class="sk-card" style="min-height:300px"><div class="sk-face"><div class="small muted">What does the course teach about…</div><div class="sk-q" style="font-size:30px">${esc(d.name)}</div><div class="small muted">Tap, Enter, or ↓ to flip</div></div>
        <div class="sk-face back" style="justify-content:flex-start;overflow:auto"><div class="small muted">${d.cls === "Not covered in materials" ? "Class: later unit" : esc(d.cls)}</div><ul style="margin:6px 0 0;padding-left:18px">${["moa", "ind", "ae", "ix", "pt", "contra", "extra"].flatMap((k) => secFacts(d, k).slice(0, 1).map((f) => [k, f])).slice(0, 4).map(([k, f]) => `<li style="margin:6px 0"><span class="small muted">${SECS.find((x) => x[0] === k)[1]}:</span> ${md(f.text)}${cite(f.src)}</li>`).join("")}</ul></div></div>
        <div class="sk-row" style="justify-content:center;margin-top:18px"><button class="btn ghost" data-prev>← Back</button><button class="btn" data-next>Next →</button></div></div></div>`;
      el.querySelector("[data-x]").onclick = end;
      const c = el.querySelector(".sk-card"); c.onclick = () => c.classList.toggle("flipped");
      el.querySelector("[data-next]").onclick = () => { i++; drawCard(); };
      el.querySelector("[data-prev]").onclick = () => { i = Math.max(0, i - 1); drawCard(); };
    };
    const key = (e) => {
      if (e.key === "Escape") end();
      else if (["Enter", " ", "ArrowDown", "ArrowUp"].includes(e.key)) { el.querySelector(".sk-card")?.classList.toggle("flipped"); e.preventDefault(); }
      else if (e.key === "ArrowRight") { i++; drawCard(); } else if (e.key === "ArrowLeft") { i = Math.max(0, i - 1); drawCard(); }
    };
    document.addEventListener("keydown", key, true);
    drawCard();
  });

  draw(); paintTray();
  const want = location.hash.slice(1), hit = DR.find((d) => slug(d.name) === want);
  if (hit) open(hit.name);
  addEventListener("hashchange", () => { const d = DR.find((x) => slug(x.name) === location.hash.slice(1)); if (d) open(d.name); });  // site search jumps here
})();
