"""Site-wide pieces: search index, whole-site Sidekick data, version stamping, Review hub, drug index."""
import html
import json
import re
from datetime import date
import sys

from build_site import DOCS, ROOT, SITE_NAME, COURSE, md, cite, slug, page, nav_html, SEARCH_ICON  # shared helpers


# ---------------------------------------------------------------- site-wide search index
def stamp_versions():
    """Cache-busting: every page asks for assets/data with ?v=<content hash>, so a new build is fetched immediately
    instead of browsers reusing yesterday's copy."""
    import hashlib
    h = hashlib.sha1()
    for f in sorted([*(DOCS / "assets").rglob("*.*"), *DOCS.rglob("*.json")]):
        h.update(f.read_bytes())
    v = h.hexdigest()[:10]
    for page_ in DOCS.rglob("*.html"):
        t = page_.read_text()
        t2 = re.sub(r'(assets/[\w\-/]+\.(?:css|js|mjs|svg))(\?v=\w+)?"', rf'\1?v={v}"', t)
        t2 = re.sub(r'<html lang="en"( data-v="\w+")?', f'<html lang="en" data-v="{v}"', t2, count=1)
        if t2 != t:
            page_.write_text(t2)
    return v


def global_kb(syl, sched, built, exams):
    """Sidekick for every non-lecture page: all lectures merged, plus the site's pages and the course calendar,
    so students can ask it things instead of searching. Links are relative to the site root."""
    kbs = {lid: json.loads((DOCS / lid / "kb.json").read_text()) for lid in built}
    g = {"lecture": "ALL", "title": "All lectures · whole site", "chunks": [], "cards": [], "quiz": [], "brief": [], "summary": [], "faq": [],
         "lectures": next(iter(kbs.values()))["lectures"] if kbs else [], "source": None, "global": True}
    for lid, k in kbs.items():
        g["chunks"] += [{**c, "lid": lid, "where": f"{lid} · {c['where']}"} for c in k["chunks"]]
        g["cards"] += [{**c, "lid": lid} for c in k["cards"]]
        g["quiz"] += [{**q, "id": f"{lid}:{q['id']}", "raw": q["id"], "lid": lid,
                       "link": ({**q["link"], "href": f"{lid}/index.html{q['link']['href']}"} if q.get("link") else None)} for q in k["quiz"]]
        g["brief"] += [{**b, "part": f"{lid} · {b['part']}"} for b in k["brief"]]
        g["summary"] += k["summary"][:3]
        g["faq"] += k["faq"][:4]
    g["pages"] = [{"t": x["t"], "u": x["u"]} for x in search_index(syl, sched, built, exams) if x.get("g") == "Pages"] + [
        {"t": "Drug index — every drug, cited, with compare and quiz", "u": "drugs/index.html"},
        {"t": "Review — Daily 10, retry misses, weakest topics, saved notes", "u": "review/index.html"},
        {"t": "What you need on the final", "u": "syllabus/index.html#final"}, {"t": "Week-by-week schedule", "u": "syllabus/index.html#schedule"}]
    cal = [f"{c['date']}: class — {c['topic']}" for c in sched["classes"]] + [f"{d['date']}: {d['kind']} — {d['label']}" + (f" (note: {d['note']})" if d.get("note") else "") for d in sched["due"]]
    gr = sched["grading"]
    g["course"] = ("COURSE CALENDAR (from the syllabus):\n" + "\n".join(sorted(cal)) + "\n\nGRADING: " +
                   "; ".join(f"{i['label']} {i['weight']}% ({i['count']} × {round(i['points_each'], 2)} pts)" for i in gr["items"]) +
                   f"; bonus: {gr['bonus']['rule']}\nSCALE: " + ", ".join(f"{L} ≥ {p / 10:g}%" for L, p, _ in gr["scale"] if p) +
                   "\nRULES: " + " ".join(gr["rules"]))
    return g


def search_index(syl, sched, built, exams):
    """Small entries for the ⌘K search: {t: text, g: group, u: url (from site root), s: citation}."""
    out = [{"t": "Home — next exam, lectures, practice exams", "g": "Pages", "u": "index.html"},
           {"t": "Syllabus — schedule, grading, grade calculator", "g": "Pages", "u": "syllabus/index.html"},
           {"t": "Grade calculator", "g": "Pages", "u": "syllabus/index.html#calc"}]
    for ex in exams:
        out.append({"t": f"{ex['title']} — practice exam", "g": "Pages", "u": f"exams/{ex['id']}/index.html"})
    for lid, b in built.items():
        kb = json.loads((DOCS / lid / "kb.json").read_text())
        out.append({"t": f"{lid} · {b['title']} — study guide", "g": "Pages", "u": f"{lid}/index.html"})
        for ch in kb["chunks"]:
            out.append({"t": ch["text"], "g": f"{lid} · {ch['where']}", "u": f"{lid}/index.html#{ch['anchor']}", "s": ch["src"]})
        for c in kb["cards"]:
            out.append({"t": f"{c['q']} — {c['a']}", "g": f"{lid} · Cram sheet", "u": f"{lid}/index.html#cram", "s": c["src"]})
        for q in kb["quiz"]:
            out.append({"t": q["stem"], "g": f"{lid} · Self-test", "u": f"{lid}/index.html#{q['id']}", "s": q.get("src", "")})
        for s in kb["summary"]:
            out.append({"t": s["text"], "g": f"{lid} · Summary", "u": f"{lid}/index.html#summary", "s": s["src"]})
    for l in syl["lectures"]:
        for o in l["objectives"]:
            if l["id"] in built:
                out.append({"t": f"{o['id']} {o['text']}", "g": f"{l['id']} · Objectives", "u": f"{l['id']}/index.html#objectives"})
    for ex in exams:
        res = DOCS / "exams" / ex["id"] / "questions.json"
        if res.exists():
            for q in json.loads(res.read_text()):
                out.append({"t": q["stem"], "g": f"{ex['title']}", "u": f"exams/{ex['id']}/index.html#q-{q['id']}", "s": q.get("src", "")})
    sys.path.insert(0, str(ROOT / "work"))
    import drugs as DR
    for d in DR.DRUGS:
        out.append({"t": (d['name'] if d['cls'].startswith('Not covered') else f"{d['name']} — {d['cls']}"), "g": "Drug index", "u": f"drugs/index.html#{slug(d['name'])}"})
        for f in d["facts"]:
            out.append({"t": f"{d['name']}: {f['text']}", "g": "Drug index", "u": f"drugs/index.html#{slug(d['name'])}", "s": f["src"]})
    for d in sched["due"]:
        out.append({"t": f"{d['label']} — {date.fromisoformat(d['date']).strftime('%a, %b %-d')}", "g": "Schedule", "u": "syllabus/index.html#schedule"})
    for u, r in sched["readings"].items():
        out.append({"t": f"Unit {u} reading: {r}", "g": "Syllabus", "u": "syllabus/index.html#units"})
    for r in sched["grading"]["rules"]:
        out.append({"t": r, "g": "Syllabus · rules", "u": "syllabus/index.html#grading"})
    return out


# ---------------------------------------------------------------- exam-week review dashboard
def review_page(syl, built, exams):
    cfg = json.dumps({"lectures": [{"id": lid, "title": b["title"]} for lid, b in built.items()],
                      "exams": [{"id": e["id"], "title": e["title"]} for e in exams],
                      "upcoming": [{"label": e["label"], "date": e["date"], "time": e["time"]} for e in syl.get("exams", [])]}).replace("</", "<\\/")
    body = f"""<header class="hero wrap rv-hero"><p class="eyebrow">Review</p><h1>Your study hub</h1>
<p class="lede">Practice that adapts to you. Everything here comes from what you've done on this site: questions you missed, cards you marked, notes you saved.</p>
<div class="rv-count" id="rv-count" hidden></div></header>
<section class="section rv-sec" id="practice"><div class="wrap"><p class="kicker">1 · Practice</p><h2>Start a session</h2>
<div class="rv-acts" id="act"></div></div></section>
<section class="section rv-sec" id="progress"><div class="wrap"><p class="kicker">2 · Your progress</p><h2>How you're doing</h2>
<div class="rv-stats" id="stats"></div><h3 class="rv-h3">Weakest topics</h3><div id="topics"></div></div></section>
<section class="section rv-sec" id="saved"><div class="wrap"><p class="kicker">3 · Saved for later</p><h2>Your collections</h2>
<div class="seg rv-tabs" id="rv-tabs"></div><div class="rv-panel" id="rv-panel"></div></div></section>
<script type="application/json" id="review-data">{cfg}</script>
<script src="../assets/review.js"></script>"""
    return page(f"Review · {SITE_NAME}", body, depth=1, active="review")


# ---------------------------------------------------------------- cumulative drug index
def drug_data(built):
    """work/drugs.py entries + every place each drug is mentioned in the study guides (auto-collected)."""
    sys.path.insert(0, str(ROOT / "work"))
    import drugs as DR
    kbs = {lid: json.loads((DOCS / lid / "kb.json").read_text()) for lid in built}
    out = []
    for d in DR.DRUGS:
        names = [d["name"]] + d["aliases"]
        pat = re.compile(r"\b(" + "|".join(re.escape(n) for n in names) + r")\b", re.I)
        mentions, seen = [], set()
        for lid, kb in kbs.items():
            for ch in kb["chunks"]:
                key = ch["text"][:80]
                if pat.search(ch["text"]) and key not in seen:
                    seen.add(key)
                    mentions.append({"lid": lid, "where": ch["where"], "text": ch["text"], "src": ch["src"], "tb": ch.get("tb", False), "href": f"../{lid}/index.html#{ch['anchor']}"})
        out.append({**d, "mentions": mentions[:12], "n_mentions": len(mentions), "pattern": "|".join(re.escape(n) for n in names)})
    return out


def drugs_page(built, exams):
    data = drug_data(built)
    tags = sorted({t for d in data for t in d["tags"]})
    cfg = json.dumps({"drugs": data, "lectures": list(built), "exams": [e["id"] for e in exams]}, ensure_ascii=False).replace("</", "<\\/")
    body = f"""<header class="hero wrap"><p class="eyebrow appear">Drug index · cumulative</p>
<h1 class="appear" style="--d:.05s">Every drug, <span class="accent-text">one place.</span></h1>
<p class="lede appear" style="--d:.12s">{len(data)} drugs from the lectures and assigned reading so far — each fact cited, every mention linked back to its lecture. It grows with every unit.</p></header>
<section class="section" style="border-top:0;padding-top:0"><div class="wrap">
<div class="dx-bar"><div class="dx-search">{SEARCH_ICON}<input id="dx-q" type="search" placeholder="Search drugs, classes, or facts…" autocomplete="off"></div>
<div class="dx-tools"><button class="btn ghost small" id="dx-drill">Drill drug flashcards</button><button class="btn ghost small" id="dx-cmp" disabled>Compare (0/2)</button></div></div>
<div class="dx-tags" id="dx-tags"><button class="sch-chip on" data-tag="">All</button>{"".join(f'<button class="sch-chip" data-tag="{html.escape(t)}">{html.escape(t)}</button>' for t in tags)}</div>
<div class="dx-grid" id="dx-grid"></div><p class="muted" id="dx-empty" hidden>No drugs match. It may be <strong>not covered in materials</strong> yet.</p>
</div></section>
<aside class="dx-sheet" id="dx-sheet" aria-label="Drug details" hidden><div class="dx-sheet-in" id="dx-sheet-in"></div></aside><div class="dx-scrim" id="dx-scrim" hidden></div>
<script type="application/json" id="drug-data">{cfg}</script>
<script src="../assets/drugs.js"></script>"""
    return page(f"Drug index · {SITE_NAME}", body, depth=1, active="drugs")

