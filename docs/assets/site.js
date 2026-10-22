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

  // self-test: first tap answers the question and reveals the explanation
  document.querySelectorAll(".q").forEach((q) => {
    q.querySelectorAll(".opt").forEach((opt) => opt.addEventListener("click", () => {
      if (q.classList.contains("answered")) return;
      q.classList.add("answered");
      q.querySelectorAll(".opt").forEach((o) => { if (o.dataset.correct === "1") o.classList.add("right"); });
      if (opt.dataset.correct !== "1") opt.classList.add("wrong");
    }));
  });

  // objectives checklist, remembered per page
  document.querySelectorAll("input[data-check]").forEach((box) => {
    const key = "check:" + location.pathname + ":" + box.dataset.check;
    box.checked = store.get(key, false);
    box.addEventListener("change", () => store.set(key, box.checked));
  });
})();
