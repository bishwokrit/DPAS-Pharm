"""Site-wide pieces: search index, whole-site Sidekick data, version stamping, Review hub, drug index."""
import html
import json
import re
from datetime import date
import sys
from urllib.parse import quote

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
        # UpToDate: a search link built from the name, so every drug (including ones added later) gets one automatically;
        # set "utd" on an entry in work/drugs.py to point at a specific monograph instead.
        utd = d.get("utd") or "https://www.uptodate.com/contents/search?search=" + quote(d["name"]) + "&searchType=PLAIN_TEXT"
        out.append({**d, "utd": utd, "mentions": mentions[:12], "n_mentions": len(mentions), "pattern": "|".join(re.escape(n) for n in names)})
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
<script src="../assets/mol3d.js"></script><script src="../assets/drugs.js"></script>"""
    return page(f"Drug index · {SITE_NAME}", body, depth=1, active="drugs")



# ---------------------------------------------------------------- drug of the day
def dotd_data(built, exams, data):
    """docs/drugs/dotd.json: for every drug already taught in a lecture, a short study card and 5 questions —
    real self-test/exam questions that mention it first, then "which drug?" and "which class?" items built from
    its own cited facts. The page picks one drug per day from the ones taught by that date."""
    import hashlib
    h = lambda s: int(hashlib.sha1(s.encode()).hexdigest(), 16)  # noqa: E731 (stable shuffles, same every build)
    bank = []
    for lid in built:
        for x in json.loads((DOCS / lid / "kb.json").read_text())["quiz"]:
            bank.append({**x, "id": f"{lid}:{x['id']}", "lid": lid, "raw": x["id"], "link": {**x["link"], "href": f"{lid}/index.html{x['link']['href']}"} if x.get("link") else None})
    for e in exams:
        for x in json.loads((DOCS / "exams" / e["id"] / "quiz.json").read_text()):
            bank.append({**x, "link": {**x["link"], "href": x["link"]["href"].replace("../../", "")} if x.get("link") else None})
    pool = [d for d in data if d["mentions"]]
    generic = re.compile(r"first-pass|renal|CYP|P-glycoprotein|protein-bound|narrow|therapeutic index|prodrug|subcutaneous|inhal|sublingual|\bVd\b|half-life|generic name|the lecture", re.I)
    out = []
    for d in pool:
        pat = re.compile(r"\b(" + d["pattern"] + r")\b", re.I)
        # real questions: the drug in the stem or the right answer beats a passing mention in a wrong option
        real = [x for x in bank if pat.search(x["stem"] + " " + " ".join(x["options"].values()) + " " + (x.get("why") or ""))]
        real.sort(key=lambda x: (not pat.search(x["stem"] + " " + x["options"][x["answer"]]), h(d["name"] + x["id"])))
        made = []
        others = [o for o in pool if o["name"] != d["name"]]
        for i, f in enumerate(d["facts"]):
            text = pat.sub("_____", f["text"].replace("**", ""))
            if len(text) < 40 or "_____" in text[:1] or generic.search(f["text"]):
                continue
            # distractors: drugs that share none of its tags (so the fact can't also be true of them) and aren't named in it
            safe = [o for o in others if not set(o["tags"]) & set(d["tags"]) and not re.search(r"\b(" + o["pattern"] + r")\b", f["text"], re.I)] or others
            opts = sorted([d["name"], *sorted((o["name"] for o in safe), key=lambda n: h(d["name"] + n + str(i)))[:3]], key=lambda n: h(n + f["text"]))
            made.append({"id": f"dotd:{slug(d['name'])}:f{i}", "stem": f"Which drug fits this fact? “{text}”", "options": dict(zip("ABCD", opts)),
                         "answer": "ABCD"[opts.index(d["name"])], "why": f"{d['name']}: {f['text'].replace('**', '')}", "src": f["src"], "topic": "Drug of the day"})
        if d["cls"] != "Not covered in materials":
            classes = sorted({o["cls"] for o in others if o["cls"] not in ("Not covered in materials", d["cls"])}, key=lambda c: h(d["name"] + c))[:3]
            if len(classes) == 3:
                opts = sorted([d["cls"], *classes], key=lambda c: h(c + d["name"]))
                made.append({"id": f"dotd:{slug(d['name'])}:cls", "stem": f"Which class does {d['name']} belong to?", "options": dict(zip("ABCD", opts)),
                             "answer": "ABCD"[opts.index(d["cls"])], "why": f"{d['name']} is a {d['cls']}.", "src": d.get("cls_src", ""), "topic": "Drug of the day"})
        # "which statement is true of it?": its own fact against other drugs' facts that name no drug and share no tag
        foreign = [(o, f) for o in others if not set(o["tags"]) & set(d["tags"]) for f in o["facts"]
                   if not re.search(r"\b(" + "|".join(x["pattern"] for x in data) + r")\b", f["text"], re.I) and len(f["text"]) < 160 and not generic.search(f["text"])]
        for i, f in enumerate(d["facts"]):
            if len(made) >= 4 or len(foreign) < 3 or len(f["text"]) > 160:
                break
            wrong, seen = [], {f["text"][:22].lower()}
            for of in sorted(foreign, key=lambda of: h(d["name"] + of[1]["text"] + str(i))):  # no near-duplicate options
                if of[1]["text"][:22].lower() not in seen and len(wrong) < 3:
                    wrong.append(of); seen.add(of[1]["text"][:22].lower())
            if len(wrong) < 3:
                break
            texts = [f["text"].replace("**", ""), *(of[1]["text"].replace("**", "") for of in wrong)]
            opts = sorted(texts, key=lambda t: h(t + d["name"]))
            made.append({"id": f"dotd:{slug(d['name'])}:t{i}", "stem": f"Which statement about {d['name']} is true, per the course?", "options": dict(zip("ABCD", opts)),
                         "answer": "ABCD"[opts.index(texts[0])], "why": f"{d['name']}: {texts[0]}", "src": f["src"], "topic": "Drug of the day",
                         "whys": {"ABCD"[opts.index(of[1]["text"].replace("**", ""))]: f"That describes {of[0]['name']}." for of in wrong}})
        on_topic = [x for x in real if pat.search(x["stem"] + " " + x["options"][x["answer"]])]
        qs = (on_topic[:5] + made + [x for x in real if x not in on_topic])[:5]
        if len(qs) < 3:
            continue
        taught = min(built[m["lid"]]["date"] for m in d["mentions"])
        out.append({"name": d["name"], "cls": d["cls"], "unit": d["unit"], "taught": taught, "facts": d["facts"][:4], "qs": qs,
                    "lectures": [{"text": m["text"], "src": m["src"], "where": f'{m["lid"]} · {m["where"]}'} for m in d["mentions"][:2]]})
    return out
