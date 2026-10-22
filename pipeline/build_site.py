"""Build the study website into docs/ (served by GitHub Pages).

  docs/index.html                 home: next exam, units, lectures, practice exams
  docs/<LEC>/index.html           study guide (web) + <LEC>_study_guide.pdf + deck + NotebookLM files
  docs/exams/<id>/index.html      practice exam apps (built by build_exam.py)
Everything comes from work/<LEC>/content.resolved.json — the same data as the decks.
"""
import html
import json
import math
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path

import lecture_checks
from content import sections_for

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
SRC = ROOT / "site_src"
STYLE = json.loads((ROOT / "templates" / "deck_style.json").read_text())["themes"]["light"]["section"]
SITE_NAME = "DPAS Pharm"


# ---------------------------------------------------------------- helpers
def md(text):
    """Escape, then **bold** -> <strong>."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html.escape(str(text), quote=False))


def cite(src):
    return f'<span class="cite">{html.escape(src)}</span>' if src else ""


def fact(f):
    tags = ('<span class="tag tb">TB</span>' if f.get("tb") else "") + ('<span class="tag sg">SG</span>' if f.get("sg") else "")
    return f"<li>{tags}{md(f['text'])}{cite(f.get('src', ''))}</li>"


def slug(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def page(title, body, depth=0, nav_links=""):
    up = "../" * depth
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<title>{html.escape(title)}</title>
<link rel="stylesheet" href="{up}assets/site.css">
</head>
<body>
<nav class="nav"><div class="nav-in">
  <a class="brand" href="{up}index.html">{SITE_NAME}</a>
  <div class="nav-links">{nav_links}</div>
  <button class="theme-btn" aria-label="Change theme"></button>
</div></nav>
{body}
<footer class="wrap">Built only from DPAS 625 course materials (lecture slides, syllabus, study guide). TB = textbook only · SG = study guide only · S12 = slide 12.</footer>
<script src="{up}assets/site.js"></script>
</body>
</html>
"""


# ---------------------------------------------------------------- study guide
def study_plan(c, checks):
    words = sum(len(f["text"].split()) for cl in c["classes"] for fs in cl["sections"].values() for f in fs)
    read = max(10, 5 * math.ceil(words / 150 / 5))
    visuals = sum(len(cl.get("comparisons", [])) + len(cl.get("flows", [])) + len(cl.get("figures", [])) for cl in c["classes"])
    cram = len(c.get("guide", {}).get("cram", []))
    qs = len(checks) + sum(1 for cl in c["classes"] for q in cl.get("questions", []) if not q.get("from_slides"))
    return [("Read the guide", read, "One pass, top to bottom. Bold = what the lecture emphasized."),
            ("Diagrams & tables", max(5, 5 * math.ceil(visuals * 2 / 5)), "Redraw each flow from memory; cover a table column and recall it."),
            ("Cram sheet", max(5, 5 * math.ceil(cram * 0.5 / 5)), "Hide answers and quiz yourself. Repeat until it's automatic."),
            ("Self-test", max(5, 5 * math.ceil(qs * 1.5 / 5)), "Answer before you look. Read every explanation, even when right."),
            ("Objectives check", 5, "Tick each objective only if you can teach it out loud.")]


def flows_html(flows):
    out = []
    for fl in flows:
        steps = '<span class="arrow">→</span>'.join(f'<span class="step">{md(s)}</span>' for s in fl["steps"])
        out.append(f'<div class="card" style="margin:12px 0"><h3>{md(fl["title"])}{cite(fl.get("src", ""))}</h3><div class="flow">{steps}</div></div>')
    return "".join(out)


def table_html(t, i):
    head = "".join(f"<th>{md(h)}</th>" for h in t["columns"])
    rows = "".join("<tr>" + "".join(f"<td>{md(x)}</td>" for x in r) + "</tr>" for r in t["rows"])
    tb = '<span class="tag tb">TB</span>' if t.get("tb") else ""
    return (f'<h3 style="margin-top:22px">{md(t["title"])}</h3><div class="table-wrap"><table>'
            f'<thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table></div>'
            f'<p class="table-cap">{tb}How to tell them apart. Sources: {html.escape(t.get("src", ""))}</p>')


def callout(kind, label, items):
    if not items:
        return ""
    return f'<div class="callout {kind}"><div class="label">{label}</div><ul>{"".join(items)}</ul></div>'


def part_html(c, cl, n, lec_dir, pending):
    secs = dict((k, lbl) for k, lbl in sections_for(cl))
    kind = "Topic" if cl.get("template") == "concept" else "Drug class"
    empty = "Not covered in slides · textbook pending" if pending else "Not covered in materials"
    callout_keys = {"clinical": ("clin", "Clinical"), "traps": ("trap", "Trap"), "pearls": ("why", "Clinical pearl / why")}
    cards = []
    for key, label in secs.items():
        if key in callout_keys:
            continue
        facts = cl["sections"].get(key, [])
        body = f"<ul>{''.join(fact(f) for f in facts)}</ul>" if facts else f'<p class="empty">{empty}</p>'
        cards.append(f'<div class="card"><h3><span class="dot" style="background:#{STYLE.get(key, "4472C4")}"></span>{html.escape(label)}</h3>{body}</div>')
    out = [f'<section class="section part-start" id="{slug(cl["name"])}"><div class="wrap">',
           f'<div class="part">Part {n} · {kind}</div><h2>{md(cl["name"])}</h2>',
           '<div class="chips">' + "".join(f'<span class="chip">{o}</span>' for o in cl.get("objectives", [])) + "</div>",
           f'<div class="grid two">{"".join(cards)}</div>']
    for key, (cls, label) in callout_keys.items():
        if key in secs:
            facts = cl["sections"].get(key, [])
            out.append(callout(cls, label, [fact(f) for f in facts]) if facts else f'<div class="callout {cls}"><div class="label">{label}</div><p class="empty" style="margin:0">{empty}</p></div>')
    if cl.get("flows"):
        out.append("<h3 style='margin-top:26px'>Step by step</h3>" + flows_html(cl["flows"]))
    for fig in cl.get("figures", []):
        shutil.copy(ROOT / "work" / c["lecture"]["id"] / "figures" / fig["image"], lec_dir / fig["image"])
        out.append(f'<figure><img src="{fig["image"]}" alt="{html.escape(fig.get("title", ""))}" loading="lazy">'
                   f'<figcaption><strong>{md(fig.get("title", ""))}.</strong> {md(fig["caption"])}{cite(fig.get("src", ""))}</figcaption></figure>')
    for i, t in enumerate(cl.get("comparisons", [])):
        out.append(table_html(t, i))
    for cf in cl.get("conflicts", []):
        out.append(callout("disc", "Slide discrepancy", [f"<li><strong>{md(cf['topic'])}</strong></li>",
                                                        f"<li>Slides: {md(cf['slides']['text'])}{cite(cf['slides']['src'])}</li>",
                                                        f"<li>Textbook: {md(cf['textbook']['text'])}{cite(cf['textbook']['src'])}</li>"]))
    whys = [f"<li>{md(h['text'])}{cite(h.get('src', ''))}</li>" for h in cl.get("hooks", []) if h["kind"] == "why"]
    mnems = [f"<li>{md(h['text'])}{cite(h.get('src', ''))}</li>" for h in cl.get("hooks", []) if h["kind"] == "mnemonic"]
    out.append(callout("why", "Why it happens", whys))
    out.append(callout("mnem", "Mnemonic (memory aid)", mnems))
    out.append(callout("hy", "High-yield", [fact(f) for f in cl.get("high_yield", [])]))
    out.append("</div></section>")
    return "".join(out)


def question_html(stem, options, answer, why_correct, src, whys=None, label=""):
    opts = "".join(f'<button class="opt" data-correct="{1 if L == answer else 0}"><span class="L">{L}</span><span>{md(t)}</span></button>'
                   for L, t in options.items())
    why_list = ""
    if whys:
        why_list = '<ul class="why-list">' + "".join(f"<li><strong>{L}.</strong> {md(w)}</li>" for L, w in whys.items() if L != answer) + "</ul>"
    return (f'<div class="card q"><div class="small muted">{html.escape(label)}</div><div class="stem">{md(stem)}</div><div class="opts">{opts}</div>'
            f'<div class="reveal"><div class="callout clin" style="margin-bottom:0"><div class="label">Answer: {answer}</div>'
            f'{md(why_correct)}{cite(src)}{why_list}</div></div></div>')


def guide_page(lec, c, slides, lec_dir, files):
    lid = lec["id"]
    pending = c.get("textbook_status") != "included"
    checks = lecture_checks.extract(slides)
    g = c.get("guide", {})
    plan = study_plan(c, checks)
    total = sum(m for _, m, _ in plan)
    nav = "".join(f'<a href="#{a}">{t}</a>' for a, t in [("plan", "Plan"), ("summary", "Summary"), ("objectives", "Objectives")] +
                  [(slug(cl["name"]), f"Part {i}") for i, cl in enumerate(c["classes"], 1)] + [("cram", "Cram sheet"), ("selftest", "Self-test"), ("checklist", "Checklist")])
    dl = "".join(f'<a class="btn {"" if i == 0 else "ghost"}" href="{href}">{label}</a>' for i, (label, href) in enumerate(files))
    body = [f'<header class="hero wrap"><p class="eyebrow">Unit {lec["unit"]} · Session {lec["session"]} · {html.escape(c["lecture"].get("date", ""))}</p>',
            f'<h1>{md(c["lecture"]["title"])}</h1>',
            f'<p class="lede">{len(c["classes"])} parts · every fact cited to its slide. About {total} minutes of focused study.</p>',
            f'<div class="btns noprint">{dl}</div></header>']
    # plan
    body.append('<section class="section" id="plan"><div class="wrap"><h2>Study plan</h2><div class="plan">' +
                "".join(f'<div class="card"><div class="mins">{m}<span class="small muted"> min</span></div><h3 style="margin:6px 0 4px">{t}</h3><div class="small muted">{d}</div></div>' for t, m, d in plan) +
                "</div>" + ('<p class="small muted" style="margin-top:14px">Textbook not added yet — this guide is built from the slides and study guide only.</p>' if pending else "") +
                '<div class="callout why" style="margin-top:18px"><div class="label">How to read this guide</div><ul>'
                '<li><strong>Bold</strong> = emphasized on the lecture slides</li>'
                '<li><span class="tag tb">TB</span>textbook only · <span class="tag sg">SG</span>course study guide only</li>'
                '<li><span class="cite">S12</span> = slide 12 · <span class="cite">S12 (notes)</span> = speaker notes · <span class="cite">SG U1-R3</span> = study guide item</li></ul></div></div></section>')
    # summary
    body.append('<section class="section" id="summary"><div class="wrap narrow"><h2>The whole lecture in 6 sentences</h2><ol class="summary">' +
                "".join(f"<li>{md(s['text'])}{cite(s['src'])}</li>" for s in g.get("summary", [])) + "</ol></div></section>")
    # objectives
    rows = []
    for o in c["objectives"]:
        where = [cl["name"] for cl in c["classes"] if o["id"] in cl.get("objectives", [])]
        note = f'<div class="small" style="color:var(--warn)">⚠ {html.escape(o["thin_note"])}</div>' if o.get("thin_note") else ""
        rows.append(f'<tr><td>{o["id"]}</td><td>{md(o["text"])}{note}</td><td class="small muted">{html.escape(", ".join(where) or "—")}</td></tr>')
    body.append('<section class="section" id="objectives"><div class="wrap"><h2>Learning objectives</h2><p class="muted">IO = syllabus unit objective · SO = this session\'s objectives slide.</p>'
                '<div class="table-wrap"><table><thead><tr><th>ID</th><th>Objective</th><th>Covered in</th></tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>")
    if c.get("about"):
        body.append(callout("why", "About this lecture", [fact(f) for f in c["about"]]))
    disc = g.get("discrepancies", [])
    body.append(callout("disc", "Slide discrepancies", [f"<li>{md(d['text'])}{cite(d.get('src', ''))}</li>" for d in disc]) if disc else
                '<p class="small muted">Slide discrepancies: none found (slides, speaker notes, and study guide agree).</p>')
    body.append("</div></section>")
    # parts
    for i, cl in enumerate(c["classes"], 1):
        body.append(part_html(c, cl, i, lec_dir, pending))
    # cram sheet
    cram = g.get("cram", [])
    body.append(f'<section class="section part-start" id="cram"><div class="wrap"><h2>Cram sheet</h2><p class="muted">Every term, mechanism, drug, and number. '
                f'Hide the answers and quiz yourself; tap a blurred answer to peek.</p><button class="btn ghost noprint" data-cram-toggle="cram-t" style="margin-bottom:14px">Hide answers (quiz yourself)</button>'
                f'<div class="table-wrap"><table class="cram" id="cram-t"><thead><tr><th>Prompt</th><th>Answer</th></tr></thead><tbody>' +
                "".join(f"<tr><td>{md(r['prompt'])}</td><td>{md(r['answer'])}{cite(r['src'])}</td></tr>" for r in cram) + "</tbody></table></div></div></section>")
    # self-test
    st = ['<section class="section part-start" id="selftest"><div class="wrap narrow"><h2>Self-test</h2>',
          f'<p class="muted">First, the lecture\'s own {len(checks)} knowledge checks — exactly as written. Then original PANCE-style questions. Tap an answer to reveal the explanation.</p>',
          '<h3 style="margin-top:26px">From the lecture</h3>']
    for k, q in enumerate(checks, 1):
        st.append(question_html(q["stem"], q["options"], q["answer"], q["why"], q["src"], label=f"Lecture check {k} · {q['src']}"))
    st.append('<h3 style="margin-top:30px">Original questions</h3>')
    k = 0
    for cl in c["classes"]:
        for q in cl.get("questions", []):
            if q.get("from_slides"):
                continue
            k += 1
            opts = {L: o["text"] for L, o in q["options"].items()}
            whys = {L: o["why"] for L, o in q["options"].items()}
            st.append(question_html(q["stem"], opts, q["answer"], q.get("why_correct", ""), q.get("src", ""), whys,
                                    label=f"Q{k} · {'Clinical vignette' if q['kind'] == 'vignette' else 'Mechanism'} · {cl['name']}"))
    st.append("</div></section>")
    body.append("".join(st))
    # checklist
    body.append('<section class="section" id="checklist"><div class="wrap narrow"><h2>Objectives checklist</h2><p class="muted">Tick only what you could teach out loud. Saved on this device.</p>' +
                "".join(f'<label class="check"><input type="checkbox" data-check="{o["id"]}"><span><strong>{o["id"]}</strong> {md(o["text"])}</span></label>' for o in c["objectives"]) +
                "</div></section>")
    return page(f"{lid} · {c['lecture']['title']}", "".join(body), depth=1, nav_links=nav)


def make_pdf(html_path, pdf_path):
    """Print the study-guide page to PDF with headless Chromium (print styles show all answers)."""
    script = f"""
const pw = (() => {{ try {{ return require('playwright'); }} catch {{ return require('/opt/node22/lib/node_modules/playwright'); }} }})();
(async () => {{
  const b = await pw.chromium.launch();
  const p = await b.newPage();
  await p.goto('file://{html_path}', {{ waitUntil: 'load' }});
  await p.emulateMedia({{ media: 'print', colorScheme: 'light' }});
  await p.pdf({{ path: '{pdf_path}', format: 'Letter', printBackground: true, margin: {{ top: '0.6in', bottom: '0.6in', left: '0.6in', right: '0.6in' }},
    displayHeaderFooter: true, headerTemplate: '<span></span>',
    footerTemplate: '<div style="font-size:8px;width:100%;text-align:center;color:#888"><span class="pageNumber"></span> / <span class="totalPages"></span></div>' }});
  await b.close();
}})();
"""
    subprocess.run(["node", "-e", script], check=True, cwd=ROOT)


# ---------------------------------------------------------------- home
def home_page(syl, built, exams_built):
    today = date.today().isoformat()
    nxt = next((e for e in syl.get("exams", []) if e["date"] >= today), None)
    hero = ['<header class="hero wrap"><p class="eyebrow">DPAS 625 · Clinical Pharmacology I · Fall 2026</p>',
            "<h1>Study smarter.<br>Remember longer.</h1>",
            '<p class="lede">Study guides, decks, and practice exams for every lecture — built only from your course materials, with every fact cited to its slide.</p>']
    if nxt:
        days = (date.fromisoformat(nxt["date"]) - date.today()).days
        when = "today" if days == 0 else f"in {days} day{'s' if days != 1 else ''}"
        hero.append(f'<div class="card" style="margin-top:28px;max-width:520px"><div class="small muted">Next exam</div>'
                    f'<h3 style="margin:4px 0">{html.escape(nxt["label"])} — {when}</h3>'
                    f'<div class="small muted">{date.fromisoformat(nxt["date"]).strftime("%a, %b %-d")} · {html.escape(nxt["time"])} · {html.escape(nxt["where"])}</div></div>')
    hero.append("</header>")
    body = ["".join(hero)]
    # practice exams
    cards = []
    for ex in exams_built:
        cards.append(f'<a class="card lec" href="exams/{ex["id"]}/index.html" style="color:inherit"><div class="small muted">Practice exam</div>'
                     f'<h3 style="margin:2px 0">{html.escape(ex["title"])}</h3><div class="meta">{ex["count"]} questions · one at a time · instant explanations · tracks what you miss</div>'
                     f'<div class="links"><span style="color:var(--accent)">Start →</span></div></a>')
    if cards:
        body.append(f'<section class="section" id="exams"><div class="wrap"><h2>Practice exams</h2><div class="grid">{"".join(cards)}</div></div></section>')
    # units
    for u, name in syl.get("units", {}).items():
        lecs = [l for l in syl["lectures"] if str(l["unit"]) == u]
        exam = next((e for e in syl.get("exams", []) if str(e["unit"]) == u), None)
        items = []
        for l in lecs:
            if l["id"] in built:
                b = built[l["id"]]
                links = "".join(f'<a href="{href}">{label}</a>' for label, href in b["links"])
                items.append(f'<div class="card lec"><div class="small muted">Session {l["session"]} · {date.fromisoformat(l["date"]).strftime("%a, %b %-d")}</div>'
                             f'<h3 style="margin:2px 0"><a href="{l["id"]}/index.html" style="color:inherit">{html.escape(b["title"])}</a></h3>'
                             f'<div class="meta">{b["meta"]}</div><div class="links">{links}</div></div>')
            else:
                items.append(f'<div class="card lec soon"><div class="small muted">Session {l["session"]} · {date.fromisoformat(l["date"]).strftime("%a, %b %-d")}</div>'
                             f'<h3 style="margin:2px 0">{html.escape(name)} — Session {l["session"]}</h3><div class="meta">Coming after the lecture</div></div>')
        exam_line = (f'<p class="muted">{html.escape(exam["label"])}: {date.fromisoformat(exam["date"]).strftime("%a, %b %-d")} · {html.escape(exam["time"])}</p>' if exam else "")
        body.append(f'<section class="section" id="unit{u}"><div class="wrap"><div class="part">Unit {u}</div><h2>{html.escape(name)}</h2>{exam_line}<div class="grid">{"".join(items)}</div></div></section>')
    nav = '<a href="#exams">Practice exams</a>' + "".join(f'<a href="#unit{u}">Unit {u}</a>' for u in syl.get("units", {}))
    return page(SITE_NAME, "".join(body), nav_links=nav)


# ---------------------------------------------------------------- main
def main(pdf=True):
    syl = json.loads((ROOT / "work" / "syllabus.json").read_text())
    DOCS.mkdir(exist_ok=True)
    shutil.copytree(SRC / "assets", DOCS / "assets", dirs_exist_ok=True)
    (DOCS / ".nojekyll").write_text("")
    built = {}
    for lec in syl["lectures"]:
        lid = lec["id"]
        resolved = ROOT / "work" / lid / "content.resolved.json"
        if not resolved.exists():
            continue
        c = json.loads(resolved.read_text())
        slides = json.loads((ROOT / "work" / lid / "slides.json").read_text())
        lec_dir = DOCS / lid
        lec_dir.mkdir(parents=True, exist_ok=True)
        files = []
        pdf_name = f"{lid}_study_guide.pdf"
        files.append(("Download PDF", pdf_name))
        for deck in (ROOT / "outputs" / lid).glob("*_study_deck.pptx"):
            shutil.copy(deck, lec_dir / deck.name)
            files.append(("Slide deck (.pptx)", deck.name))
        for f in (ROOT / "outputs" / lid / "notebooklm").glob("*.md"):
            shutil.copy(f, lec_dir / f.name)
        src_md = sorted(lec_dir.glob(f"{lid}_source*.md"))
        files.append(("NotebookLM source", src_md[0].name))
        files.append(("NotebookLM prompts", f"{lid}_instructions.md"))
        (lec_dir / "index.html").write_text(guide_page(lec, c, slides, lec_dir, files))
        if pdf:
            make_pdf(lec_dir / "index.html", lec_dir / pdf_name)
        n_q = sum(len(cl.get("questions", [])) for cl in c["classes"]) + len(lecture_checks.extract(slides))
        built[lid] = {"title": c["lecture"]["title"],
                      "meta": f'{len(c["classes"])} parts · {len(c.get("guide", {}).get("cram", []))}-row cram sheet · {n_q} practice questions',
                      "links": [("Study guide", f"{lid}/index.html"), ("PDF", f"{lid}/{pdf_name}"), ("Deck", f"{lid}/" + next((n for l, n in files if l.startswith("Slide")), ""))]}
        print(f"  site: {lid} study guide" + (" + PDF" if pdf else ""))
    exams = []
    for ex_dir in sorted((DOCS / "exams").glob("*/meta.json")) if (DOCS / "exams").exists() else []:
        exams.append(json.loads(ex_dir.read_text()))
    (DOCS / "index.html").write_text(home_page(syl, built, exams))
    print(f"  site: home page ({len(built)} lectures, {len(exams)} practice exams) -> docs/")


if __name__ == "__main__":
    import sys
    main(pdf="--no-pdf" not in sys.argv)
