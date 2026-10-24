// Drug of the day: one drug a day from those already taught, a 1-minute study card, then up to 5 questions.
// Same drug for everyone on a given date; your score and streak stay in this browser.
(function () {
  const el = document.getElementById("dotd");
  if (!el) return;
  const root = document.documentElement.dataset.root || "", v = document.documentElement.dataset.v || "";
  const esc = (s) => String(s ?? "").replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const md = (s) => esc(s).replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>");
  const store = {
    get(k, d) { try { const x = localStorage.getItem(k); return x === null ? d : JSON.parse(x); } catch { return d; } },
    set(k, x) { try { localStorage.setItem(k, JSON.stringify(x)); } catch { /* private mode */ } },
  };
  const iso = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  const now = new Date(), today = iso(now), yesterday = iso(new Date(now.getFullYear(), now.getMonth(), now.getDate() - 1));
  const hash = (s) => [...s].reduce((h, c) => (Math.imul(h, 31) + c.charCodeAt(0)) | 0, 7);

  fetch(`${root}drugs/dotd.json?v=${v}`).then((r) => r.json()).then((all) => {
    const pool = all.filter((d) => d.taught <= today).sort((a, b) => hash(a.name) - hash(b.name));
    if (!pool.length) return;
    const day = Math.floor(Date.UTC(now.getFullYear(), now.getMonth(), now.getDate()) / 864e5);
    const d = pool[day % pool.length];
    const qs = d.qs.map((q) => ({ ...q, link: q.link ? { ...q.link, href: root + q.link.href } : null }));
    const cls = d.cls === "Not covered in materials" ? "Drug class: covered in a later unit" : d.cls;

    function paint() {
      const s = store.get("dotd", {}), done = s.last === today, streak = s.last === today || s.last === yesterday ? s.streak || 0 : 0;
      el.innerHTML = `<div class="dotd-sky"></div><div class="dotd-body">
        <div class="tile-k">Drug of the day · ${now.toLocaleDateString(undefined, { weekday: "long", month: "short", day: "numeric" })}</div>
        <h3 class="dotd-name">${esc(d.name)}</h3><p class="dotd-cls">${esc(cls)}</p>
        ${done ? `<p class="dotd-meta"><strong>Done today · ${s.score}/${s.total}</strong>${streak > 1 ? ` · ${streak}-day streak` : ""}. A new drug tomorrow.</p>
          <button class="btn ghost small" data-go>Go again</button>`
        : `<p class="dotd-meta">5 minutes · a quick read, then ${qs.length} questions${streak ? ` · keep your ${streak}-day streak` : ""}</p>
          <button class="btn small" data-go>Start</button>`}</div>`;
      el.hidden = false;
      el.querySelector("[data-go]").onclick = () => study(done);
      window.dpasMolData?.(root).then((M) => { if (M[d.name] && !el.querySelector(".mol3d-wrap")) window.dpasMol3d(el.querySelector(".dotd-sky"), window, M[d.name], { size: 220, recede: false }); });
    }

    function study(again) {
      const o = document.createElement("div");
      o.className = "qm"; o.setAttribute("role", "dialog"); o.setAttribute("aria-label", `Drug of the day: ${d.name}`);
      o.innerHTML = `<div class="qm-top"><button class="qm-x" data-x aria-label="Close">✕</button><div class="qm-title">Drug of the day</div><span></span></div>
        <div class="qm-scroll"><div class="qm-card dotd-study"><div class="small muted">Read it once, then close your eyes and say it back.</div>
        <h2>${esc(d.name)}</h2><p class="muted">${esc(cls)}</p>
        <ul>${d.facts.map((f) => `<li>${f.tb ? '<span class="tag tb">TB</span>' : ""}${md(f.text)} <span class="cite">${esc(f.src)}</span></li>`).join("")}</ul>
        ${d.lectures?.length ? `<div class="small muted">In your lectures</div><ul class="dotd-lec">${d.lectures.map((m) => `<li>${md(m.text)} <span class="cite">${esc(m.src)}</span></li>`).join("")}</ul>` : ""}
        <div class="sk-row"><button class="btn" data-q>I've got it · ${qs.length} questions →</button><a class="btn ghost" href="${root}drugs/index.html#${d.name.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "")}">Full drug sheet</a></div></div></div>`;
      document.body.append(o); document.documentElement.style.overflow = "hidden";
      const end = () => { o.remove(); document.documentElement.style.overflow = ""; removeEventListener("keydown", key, true); };
      const key = (e) => { if (e.key === "Escape") end(); };
      addEventListener("keydown", key, true);
      o.querySelector("[data-x]").onclick = end;
      o.querySelector("[data-q]").onclick = () => {
        end();
        window.dpasQuiz?.start(qs, {
          title: `Drug of the day · ${d.name}`,
          // misses on lecture questions show up in Progress like any other
          onAnswer: (q, L, ok) => { if (!q.lid) return; const m = new Set(store.get(`miss:${q.lid}`, [])); ok ? m.delete(q.raw) : m.add(q.raw); store.set(`miss:${q.lid}`, [...m]); },
          onFinish: (r) => {
            if (again) return;  // the first run of the day is the one that counts
            const s = store.get("dotd", {});
            store.set("dotd", { last: today, score: r.correct, total: r.total, streak: s.last === yesterday ? (s.streak || 0) + 1 : 1 });
            paint();
          },
        });
      };
    }
    paint();
  }).catch(() => {});
})();
