// When things are due, and how long is left. In-class items (quizzes, exams) start at the time in their label;
// everything else (discussion boards, checkpoints, cases) is due 11:59 pm Eastern. On the day itself the count
// switches from days to hours, then minutes in the last hour. Loaded in the head so every page script can use it.
(function () {
  const TZ = "America/New_York";
  const hourET = (t) => +new Intl.DateTimeFormat("en-US", { timeZone: TZ, hour: "numeric", hourCycle: "h23" }).format(t);
  // a wall-clock time in Eastern on a given day, as a real moment (handles daylight saving)
  function et(date, h, m) {
    const [y, mo, d] = date.split("-").map(Number);
    for (const off of [4, 5]) { const t = new Date(Date.UTC(y, mo - 1, d, h + off, m)); if (hourET(t) === h) return t; }
    return new Date(Date.UTC(y, mo - 1, d, h + 5, m));
  }
  // "8:35–8:45 am", "1:00–2:00 pm", "8:30 am": the start time; no time → 11:59 pm
  function at(date, text) {
    const m = String(text || "").match(/(\d{1,2}):(\d{2})\s*(?:[–-]\s*\d{1,2}:\d{2}\s*)?(am|pm)/i);
    if (!m) return et(date, 23, 59);
    const h = (+m[1] % 12) + (m[3].toLowerCase() === "pm" ? 12 : 0);
    return et(date, h, +m[2]);
  }
  const ymd = (d) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  // {n, unit, text, soon, past}: "3 days", "5 hr", "42 min"
  function left(date, text, now = new Date()) {
    const t = at(date, text), ms = t - now;
    if (ms <= 0) return { n: "✓", unit: "past", text: "past", past: true };
    const days = Math.round((new Date(date + "T00:00") - new Date(ymd(now) + "T00:00")) / 864e5);
    if (days > 0) return { n: days, unit: days === 1 ? "day" : "days", text: days === 1 ? "tomorrow" : `in ${days} days` };
    if (ms < 36e5) { const n = Math.max(1, Math.ceil(ms / 6e4)); return { n, unit: "min", text: `in ${n} min`, soon: true }; }
    const n = Math.floor(ms / 36e5);
    return { n, unit: "hr", text: `in ${n} hr`, soon: true };
  }
  // "11:59 pm ET" for take-home work; in-class items already carry their own time
  const timeOf = (text) => (/\d:\d{2}/.test(text || "") ? "" : "11:59 pm ET");
  window.dpasDue = { at, left, timeOf, upcoming: (date, text, now = new Date()) => at(date, text) > now };
})();
