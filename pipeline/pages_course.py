"""Home page and syllabus page (schedule, grading, grade calculator)."""
import html
import json
import re
from datetime import date

from build_site import DOCS, ROOT, SITE_NAME, COURSE, md, cite, slug, page, nav_html, SEARCH_ICON  # shared helpers


# ---------------------------------------------------------------- home
ICONS = {  # simple line icons (inherit currentColor)
    "check": '<rect x="3.5" y="3.5" width="17" height="17" rx="4" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M8 12l3 3 5-6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    "review": '<path d="M4 12a8 8 0 1 0 2.3-5.6M4 4v4h4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>',
    "exam": '<rect x="5" y="3" width="14" height="18" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M9 8h6M9 12h6M9 16h3" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "timer": '<circle cx="12" cy="13" r="7.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 9v4l2.5 2M10 2.5h4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15" rx="2.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3.5 10h17M8 3v4M16 3v4" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>',
}


def icon(name):
    return f'<svg viewBox="0 0 24 24" width="22" height="22" aria-hidden="true">{ICONS[name]}</svg>'


def home_page(syl, built, exams_built):
    sched = json.loads((ROOT / "work" / "schedule.json").read_text())
    n_q = sum(b["qs"] for b in built.values()) + sum(e["count"] for e in exams_built)
    n_cards = sum(b["cards"] for b in built.values())
    teasers = [{"date": l["date"], "text": built[l["id"]]["teaser"]} for l in syl["lectures"] if l["id"] in built and built[l["id"]].get("teaser")]
    upnext = json.dumps({"exams": syl.get("exams", []), "due": sched["due"]}).replace("</", "<\\/")
    hero = f"""<section class="first-screen">
<header class="hero home-hero wrap">
<p class="eyebrow appear">Clinical Pharmacology I · Fall 2026</p>
<h1 class="hero-title"><span class="line">Study smarter.</span><span class="line accent-text">Remember longer.</span></h1>
<p class="lede hero-teaser" id="home-teaser">{html.escape(teasers[-1]["text"]) if teasers else ""}</p>
<script type="application/json" id="teaser-data">{json.dumps(teasers).replace("</", "<\\/")}</script>
</header>
<div class="wrap"><div class="up3" id="home-up"></div>
<script type="application/json" id="home-data">{upnext}</script></div>
<div class="wrap stats appear" style="--d:.55s" aria-label="At a glance"><div class="stats-in">
  <div><strong data-count="{len(built)}">{len(built)}</strong><span>lectures ready</span></div>
  <div><strong data-count="{n_q}">{n_q}</strong><span>practice questions</span></div>
  <div><strong data-count="{n_cards}">{n_cards}</strong><span>flashcards</span></div>
  <div><strong>100%</strong><span>facts cited to a source</span></div>
</div></div>
<a class="scroll-cue" href="#practice" aria-label="Scroll to practice"><span></span></a>
</section>"""
    # practice follows the calendar: one bento per unit, and the browser shows the unit whose exam is next
    # (Unit 1 until its exam, then Unit 2, ...). Earlier units and the final live in Review.
    def unit_tiles(u):
        lecs = [(lid, b) for lid, b in built.items() if str(b["unit"]) == u]
        exs = [e for e in exams_built if str(e.get("unit")) == u]
        tiles = []
        if lecs or exs:
            tiles.append(f'<a class="tile tile-wide appear" href="review/index.html?scope=unit"><span class="tile-ic">{icon("review")}</span><div><div class="tile-k">Unit {u} · everything in one place</div>'
                         f'<h3>Unit {u} review</h3><p>Daily 10, your misses, and a timed mix, from Unit {u} only.</p></div><span class="tile-go">Open →</span></a>')
        for i, ex in enumerate(exs):
            timed = f' · {ex["minutes"]} min' if ex.get("minutes") else ""
            tiles.append(f'<a class="tile appear" style="--d:{.06 * (i + 1):.2f}s" href="exams/{ex["id"]}/index.html" data-progress="exam" data-slug="{ex["id"]}" data-total="{ex["count"]}">'
                         f'<span class="tile-ic">{icon("timer" if ex.get("minutes") else "exam")}</span><div><div class="tile-k">Practice exam · {ex["count"]} Q{timed}</div>'
                         f'<h3>{html.escape(ex["title"].split(" (")[0])}</h3><p>Study or timed mode, a debrief at the end, and a log of what you miss.</p><div class="progress"></div></div><span class="tile-go">Start →</span></a>')
        for i, (lid, b) in enumerate(lecs):
            tiles.append(f'<a class="tile appear" style="--d:{.06 * (len(exs) + i + 1):.2f}s" href="{lid}/index.html?quiz=1"><span class="tile-ic">{icon("check")}</span><div><div class="tile-k">{lid} self-test · {b["qs"]} Q</div>'
                         f'<h3>{html.escape(b["title"])}</h3><p>One question at a time, with the why behind every answer.</p></div><span class="tile-go">Start →</span></a>')
        if not tiles:
            tiles.append(f'<div class="tile tile-wide appear"><span class="tile-ic">{icon("calendar")}</span><div><div class="tile-k">Unit {u} · {html.escape(syl["units"][u])}</div>'
                         f'<h3>Practice opens as lectures are posted</h3><p>Questions for Unit {u} appear here after each class. Meanwhile, keep earlier units fresh in Review.</p></div></div>')
        later = "earlier units" if int(u) > 1 else "the whole course"
        tiles.append(f'<a class="tile tile-wide appear" href="review/index.html?scope=all"><span class="tile-ic">{icon("review")}</span><div><div class="tile-k">Cumulative</div>'
                     f'<h3>Review {later} &amp; prep for the final</h3><p>Spaced review across every unit so far, by-unit scores, and a timed final mock.</p></div><span class="tile-go">Open →</span></a>')
        return tiles
    groups = "".join(f'<div class="bento" data-unit="{u}" hidden>{"".join(unit_tiles(u))}</div>' for u in syl["units"])
    groups += (f'<div class="bento" data-unit="final" hidden><a class="tile tile-wide appear" href="review/index.html?scope=all"><span class="tile-ic">{icon("review")}</span><div><div class="tile-k">Comprehensive final</div>'
               '<h3>Final prep</h3><p>Every unit together: by-unit scores, your misses, and a timed final mock.</p></div><span class="tile-go">Open →</span></a></div>')
    practice = (f'<section class="section" id="practice"><div class="wrap"><p class="kicker appear">Practice</p><h2 class="appear">Test yourself. Then test yourself again.</h2>'
                f'<p class="pr-sub appear" id="pr-sub"></p><div class="dotd appear" id="dotd" hidden></div>{groups}</div></section>')
    # course roadmap: one compact row per unit; the current unit opens with its lecture cards
    today = date.today().isoformat()
    exam_of = {str(e["unit"]): e for e in syl.get("exams", [])}
    current = next((u for u in syl["units"] if exam_of.get(u, {}).get("date", "9999") >= today), None)
    rows = []
    for k, (u, name) in enumerate(syl["units"].items()):
        lecs = [l for l in syl["lectures"] if str(l["unit"]) == u]
        ex = exam_of.get(u)
        state = "done" if ex and ex["date"] < today else ("now" if u == current else "later")
        badge = {"done": "Done", "now": "Current unit", "later": ""}[state]
        cards = []
        for l in lecs:
            d = date.fromisoformat(l["date"]).strftime("%a, %b %-d")
            if l["id"] in built:
                b = built[l["id"]]
                links = "".join(f'<a href="{href}">{label}</a>' for label, href in b["links"])
                cards.append(f'<div class="card lec" data-progress="lecture" data-lid="{l["id"]}" data-objs="{b["objs"]}" data-cards="{b["cards"]}" data-qs="{b["qs"]}">'
                             f'<div class="small muted">Session {l["session"]} · {d}</div><h3 style="margin:2px 0"><a class="stretch" href="{l["id"]}/index.html" style="color:inherit">{html.escape(b["title"])}</a></h3>'
                             f'<div class="meta">{b["meta"]}</div><div class="progress"></div><div class="links">{links}</div></div>')
            else:
                cards.append(f'<div class="card lec soon"><div class="small muted">Session {l["session"]} · {d}</div><h3 style="margin:2px 0">Session {l["session"]}</h3><div class="meta">Available after the lecture</div></div>')
        sessions = " · ".join(date.fromisoformat(l["date"]).strftime("%b %-d") for l in lecs)
        rows.append(f'<details class="unit-row {state} appear" data-exam="{ex["date"] if ex else ""}" style="--d:{.05 * k:.2f}s"{" open" if state == "now" else ""}>'
                    f'<summary><span class="unit-num">{u}</span><span class="unit-name"><strong>{html.escape(name)}</strong><span class="small muted">Sessions {sessions}</span></span>'
                    f'<span class="unit-badge"{"" if badge else " hidden"}>{badge}</span><span class="unit-exam small">{("Exam " + date.fromisoformat(ex["date"]).strftime("%a, %b %-d")) if ex else ""}</span><span class="unit-chev" aria-hidden="true"></span></summary>'
                    f'<div class="grid unit-cards">{"".join(cards)}</div></details>')
    study = f'<section class="section" id="study"><div class="wrap"><p class="kicker appear">Study</p><h2 class="appear">Your course, one unit at a time.</h2><p class="appear"><a class="jump" href="drugs/index.html">Open the drug index →</a></p><div class="roadmap">{"".join(rows)}</div></div></section>'
    return page(f"{SITE_NAME} · {COURSE}", hero + now_section(syl, built, sched) + study + practice
                + '<script src="assets/mol3d.js"></script><script src="assets/dotd.js"></script>')



def now_section(syl, built, sched):
    """One panel per built lecture; the browser shows the one matching today's date (latest lecture so far)."""
    exam_of = {e["unit"]: e for e in syl.get("exams", [])}
    panels = []
    for lid, b in built.items():
        d = date.fromisoformat(b["date"])
        week_end = (d.toordinal() + 7)
        due = [x for x in sched["due"] if d.toordinal() <= date.fromisoformat(x["date"]).toordinal() <= week_end and x["kind"] not in ("exam", "final")][:3]
        ex = exam_of.get(b["unit"])
        due_html = "".join(f'<li><span class="small muted">{date.fromisoformat(x["date"]).strftime("%a %b %-d")}</span> {html.escape(x["label"].split(" · ")[0])}</li>' for x in due)
        if ex:
            due_html += f'<li><span class="small muted">{date.fromisoformat(ex["date"]).strftime("%a %b %-d")}</span> <strong>{html.escape(ex["label"])}</strong></li>'
        chips = "".join(f'<a class="topic-chip" href="{lid}/index.html#{a}"><span>{i}</span>{html.escape(n)}</a>' for i, n, a in b["parts"])
        hy = "".join(f'<li><a href="{lid}/index.html#{a}">{md(t)}</a></li>' for i, a, t in b["hy"][:4])
        key = re.sub(r"_1$", "", b["figure"].rsplit("/", 1)[-1].rsplit(".", 1)[0]) if b["figure"] else ""
        fig = (f'<figure class="now-fig" data-viz="{key}"><img src="{b["figure"]}" alt="{html.escape(b["figure_title"])}" loading="lazy">'
               f'<a href="{b["figure_href"]}">{md(b["figure_title"])} →</a></figure>' if b["figure"] else "")
        panels.append(f"""<article class="now-panel" data-date="{b['date']}" hidden>
<div class="now-head"><div><p class="kicker" data-now-kicker>Current lecture</p>
<h2>{html.escape(b['title'])}</h2>
<p class="muted">Unit {b['unit']} · Session {b['session']} · {d.strftime('%A, %B %-d')}{f" · Katzung Ch. {b['readings']}" if b['readings'] else ""}</p></div>
<div class="now-acts"><a class="btn" href="{lid}/index.html">Open study guide</a><a class="btn ghost" href="{lid}/index.html?quiz=1">Focus quiz</a><a class="btn ghost" href="{lid}/index.html?sk=listen">Listen</a></div></div>
<div class="topic-chips">{chips}</div>
<div class="now-grid">
  <div class="card now-hy"><h3>High-yield from this lecture</h3><ul>{hy}</ul></div>
  {fig}
  <div class="card now-side" data-progress="lecture" data-lid="{lid}" data-objs="{b['objs']}" data-cards="{b['cards']}" data-qs="{b['qs']}">
    <h3>Your progress</h3><div class="progress"></div><p class="small muted now-empty">Start the self-test or flashcards and your progress shows here.</p>
    <h3 style="margin-top:14px">Coming up</h3><ul class="now-due">{due_html or '<li class="muted small">Nothing due this week.</li>'}</ul>
    <div class="links"><a href="{b['pdf']}">PDF</a><a href="{b['deck']}">Slide deck</a></div>
  </div>
</div>
</article>""")
    return f'<section class="section now-sec" id="now"><div class="wrap">{"".join(panels)}</div></section>'

# ---------------------------------------------------------------- syllabus + grade calculator
OUTCOMES = ["Explain foundational principles of pharmacology and their relationship to medication effects.",
            "Compare pharmacologic agents based on their therapeutic and pharmacologic characteristics.",
            "Apply pharmacologic knowledge to select safe and effective pharmacotherapy for common medical conditions.",
            "Apply principles of safe medication prescribing and management.",
            "Communicate medication-related information effectively to patients and caregivers."]
KIND = {"exam": ("Exam", "bad"), "final": ("Final", "bad"), "quiz": ("Quiz", "warn"), "db": ("Discussion", "accent"),
        "case": ("Case", "violet"), "checkpoint": ("Bonus", "good")}


def syllabus_page(syl, sched, built):
    g = sched["grading"]
    when = lambda d: date.fromisoformat(d).strftime("%a, %b %-d")
    # schedule grouped by week (Mon–Sun); every class day and every deadline is a row you can filter by kind
    items = [{"date": c["date"], "kind": "class", "label": c["topic"], "lec": c.get("lecture")} for c in sched["classes"]]
    items += [{"date": d["date"], "kind": d["kind"], "label": d["label"], "note": d.get("note")} for d in sched["due"]]
    order = {"class": 0, "final": 1, "exam": 1, "quiz": 2, "case": 3, "db": 4, "checkpoint": 5}
    items.sort(key=lambda x: (x["date"], order[x["kind"]]))
    weeks = {}
    for it in items:
        d = date.fromisoformat(it["date"])
        monday = date.fromordinal(d.toordinal() - d.weekday())
        weeks.setdefault(monday, []).append(it)
    def tag(it):  # short name for a deadline chip
        n = re.search(r"\d+", it["label"].split(" · ")[0])
        n = n.group(0) if n else ""
        return {"exam": f"Exam {n}", "final": "Final", "quiz": f"Quiz {n}", "db": f"DB {n}", "case": f"Case {n}", "checkpoint": f"CP {n}"}[it["kind"]]
    wk_html = []
    for wn, (monday, its) in enumerate(weeks.items(), 1):
        friday = date.fromordinal(monday.toordinal() + 4)
        due = [it for it in its if it["kind"] != "class"]
        chips_ = "".join(f'<span class="wk-tag k-{it["kind"]}" data-kind="{it["kind"]}">{tag(it)}</span>' for it in due)
        days = {}
        for it in its:
            days.setdefault(it["date"], []).append(it)
        rows = []
        for d, day in days.items():
            dd = date.fromisoformat(d)
            lines = []
            for it in day:
                if it["kind"] == "class":
                    t = html.escape(it["label"])
                    if it.get("lec") in built:
                        t = f'<a href="../{it["lec"]}/index.html">{t}</a>'
                    lines.append(f'<div class="wk-class" data-kind="class">{t}</div>')
                else:
                    title, _, detail = it["label"].partition(" · ")
                    note = f'<div class="wk-note">{html.escape(it["note"])}</div>' if it.get("note") else ""
                    lines.append(f'<div class="wk-due k-{it["kind"]}" data-kind="{it["kind"]}"><i></i><div><strong>{html.escape(title)}</strong>'
                                 + (f'<span>{html.escape(detail)}</span>' if detail else "") + f'{note}</div></div>')
            rows.append(f'<div class="wk-day" data-date="{d}"><div class="wk-d"><small>{dd.strftime("%a")}</small>{dd.strftime("%-d")}</div><div class="wk-items">{"".join(lines)}</div></div>')
        span = f'{monday.strftime("%b %-d")} – {friday.strftime("%b %-d") if friday.month != monday.month else friday.strftime("%-d")}'
        wk_html.append(f'<details class="wk sch-week" data-week="{monday.isoformat()}" data-end="{date.fromordinal(monday.toordinal() + 6).isoformat()}">'
                       f'<summary><span class="wk-when"><b>{span}</b><span>{f"{len(due)} due" if due else "Classes only"}</span></span><span class="wk-tags">{chips_}</span><span class="wk-chev" aria-hidden="true"></span></summary>'
                       f'<div class="wk-body">{"".join(rows)}</div></details>')
    chips = "".join(f'<button class="sch-chip{" on" if k == "all" else ""}" data-filter="{k}">{lbl}</button>'
                    for k, lbl in [("all", "All"), ("exam", "Exams"), ("quiz", "Quizzes"), ("db", "Discussions"), ("case", "Cases"), ("checkpoint", "Bonus"), ("class", "Classes")])
    legend = "".join(f'<li data-key="{it["key"]}" style="--c:var(--c-{it["key"]})"><span class="lg-dot"></span><span class="lg-name">{html.escape(it["label"])}</span>'
                     f'<span class="lg-w">{it["weight"]}%</span><span class="lg-pts">{it["count"]} × {round(it["points_each"], 2):g} pts</span></li>' for it in g["items"])
    sc = g["scale"]
    def band(i):
        lo, hi = sc[i][1], (sc[i - 1][1] if i else 1000)
        pct = f"{lo // 10}–100%" if not i else (f"Below {hi // 10}%" if not lo else f"{lo // 10}–{hi / 10 - 0.01:.2f}%")
        pts = f"{lo:,}–1,000" if not i else (f"Below {hi:,}" if not lo else f"{lo:,}–{hi - 0.1:,.1f}")
        return pct, pts
    scale = "".join(f'<div class="scale-row s-{L}"><b>{L}</b><span class="sr-pct">{band(i)[0]}</span><span class="sr-pts">{band(i)[1]} pts</span><em>{st}</em></div>'
                    for i, (L, pts, st) in enumerate(sc))
    units = []
    for u, name in syl["units"].items():
        objs = {o["id"]: o["text"] for l in syl["lectures"] if str(l["unit"]) == u for o in l["objectives"]}
        exam = next((e for e in syl["exams"] if str(e["unit"]) == u), None)
        units.append(f'<details class="card unit"><summary><span class="part">Unit {u}</span><strong>{html.escape(name)}</strong>'
                     f'<span class="muted small">{("Exam " + when(exam["date"])) if exam else ""}</span></summary>'
                     f'<p class="small"><strong>Reading:</strong> {html.escape(sched["readings"].get(u, ""))}</p>'
                     + (f'<ul>{"".join(f"<li><strong>{k}</strong> {html.escape(v)}</li>" for k, v in objs.items())}</ul>' if objs else '<p class="small muted">Objectives listed in the syllabus PDF.</p>') + "</details>")
    data = json.dumps({"items": g["items"], "bonus": g["bonus"], "scale": g["scale"], "due": sched["due"]}, ensure_ascii=False).replace("</", "<\\/")
    facts = [("3", "credit hours"), ("2×", "a week · 2.5 h"), ("1,000", "points"), ("6 + 1", "unit exams + final"), ("75%", "to pass")]
    body = f"""<header class="hero wrap syl-hero"><p class="eyebrow appear">Syllabus · v5 · October 9, 2026</p>
<h1 class="appear" style="--d:.05s">Clinical<br><span class="accent-text">Pharmacology I</span></h1>
<p class="lede appear" style="--d:.12s">Fall 2026 · schedule, grading, and a calculator in one place.</p>
<div class="fact-pills appear" style="--d:.2s">{"".join(f'<div><strong>{a}</strong><span>{b}</span></div>' for a, b in facts)}</div>
<div class="btns noprint appear" style="--d:.28s"><a class="btn" href="#calc">Grade calculator</a><a class="btn ghost" href="#schedule">Schedule</a></div></header>
<section class="section" id="next"><div class="wrap"><p class="kicker">Coming up</p><h2>What's due next</h2><div class="upnext" id="upnext"></div></div></section>
<section class="section" id="grading"><div class="wrap"><p class="kicker">Grading</p><h2>Where your 1,000 points come from</h2>
<p class="muted">Each 1% of the grade is 10 points. Hover a slice or a row.</p>
<div class="grade-split"><div class="donut-wrap"><svg class="donut" viewBox="0 0 200 200" id="donut" aria-label="Grade weights"></svg>
<div class="donut-center" id="donut-center"><strong>1,000</strong><span>points</span></div></div>
<ul class="legend" id="legend">{legend}<li class="lg-bonus" data-key="bonus" style="--c:var(--c-bonus)"><span class="lg-dot"></span><span class="lg-name">Bonus checkpoints</span><span class="lg-w">+3%</span><span class="lg-pts">8 × 3.75 pts, max 30</span></li></ul></div>
<div class="grid two grade-cards" style="margin-top:26px"><div class="card"><h3>Grading scale</h3><div class="scale">{scale}</div><p class="small muted scale-note">Out of 1,000 points. Grades are not rounded — 749.9 is an F.</p></div>
<div class="card"><h3>Rules that matter</h3><ul>{"".join(f"<li>{html.escape(r)}</li>" for r in g["rules"])}<li><strong>Bonus:</strong> {html.escape(g["bonus"]["rule"])}</li></ul></div></div></div></section>
<section class="section" id="calc"><div class="wrap"><p class="kicker">Grade calculator</p><h2>Where your grade stands</h2>
<p class="muted">Enter scores as you get them. Saved only in this browser.</p>
<div id="calcapp"></div>
<script type="application/json" id="grade-data">{data}</script></div></section>
<section class="section" id="final"><div class="wrap"><p class="kicker">The final</p><h2>What you need on the final</h2>
<div id="finalapp"></div></div></section>
<section class="section" id="schedule"><div class="wrap"><p class="kicker">Schedule</p><h2>Week by week</h2><p class="muted">From the course syllabus; subject to revision. Any material covered in lecture or assigned as reading is testable.</p>
<div class="sch-chips noprint">{chips}</div>
<div class="wk-list" id="sch-list">{"".join(wk_html)}</div>
<p class="small muted">DB = discussion board · PTX = pharmacotherapy · Bonus = optional checkpoint quiz (Brightspace, 2 attempts).</p></div></section>
<section class="section" id="units"><div class="wrap"><p class="kicker">Units</p><h2>Readings &amp; objectives</h2><div class="grid two">{"".join(units)}</div></div></section>
<section class="section" id="outcomes"><div class="wrap narrow"><p class="kicker">Outcomes</p><h2>Course goal &amp; outcomes</h2>
<p>By the end of this course, students will integrate foundational pharmacologic principles with therapeutic reasoning to select, evaluate, and communicate safe, effective, evidence-based pharmacotherapy for common conditions encountered in clinical practice.</p>
<ol class="summary">{"".join(f"<li>{html.escape(o)}</li>" for o in OUTCOMES)}</ol>
<h3 style="margin-top:28px">Texts</h3><ul><li><strong>Required:</strong> Katzung's Basic and Clinical Pharmacology, 16th ed. (Vanderah, 2025) — <a href="https://accessmedicine.mhmedical.com/book.aspx?bookid=3382" target="_blank" rel="noopener">AccessMedicine</a></li>
<li><strong>Recommended:</strong> Pharmacotherapy Principles and Practice (Chisholm-Burns et al., 2022)</li></ul>
<h3 style="margin-top:28px">Policies (summary)</h3><ul class="small"><li>Program policies (attendance, grading, progression): PA Studies Student Program Guide.</li>
<li>Religious observances: notify the course in the first week.</li><li>Accommodations: contact your disability services office first, then share your letter with the course.</li>
<li>Grade concerns go to the course first. AI use: follow each assignment's instructions.</li><li>Class cancellations are announced through official email.</li></ul></div></section>
<script src="../assets/grades.js"></script>"""
    nav = '<a href="#next">Coming up</a><a href="#grading">Grading</a><a href="#calc">Calculator</a><a href="#schedule">Schedule</a><a href="#units">Units</a><a href="#outcomes">Outcomes</a>'
    return page(f"Syllabus · {SITE_NAME}", body, depth=1, nav_links=nav, active="syllabus", subtitle="Syllabus")


