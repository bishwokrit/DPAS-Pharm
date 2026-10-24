"""Anki generator: every lecture broken into card-ready items (docs/anki/data.json) and the page that turns a
selection of them into a deck in the browser (.apkg, Anki text, CSV, Quizlet, or a printable sheet).

Each item carries what a card needs — a front/back pair, a cloze sentence, or a multiple-choice question — plus
where it came from (unit, lecture, part, section, slide/page) and a depth level:
  1 essentials     high-yield points and the cram sheet
  2 standard       + definitions, clinical pearls, exam traps, memory hooks, practice questions
  3 comprehensive  + how-it-works, examples, comparison tables, step-by-step flows, textbook-only detail, drug facts
Everything comes from the study guides' own content; nothing new is written here."""
import hashlib
import html
import json
import re
import sys

from build_site import DOCS, ROOT, SITE_NAME, page, slug

SECTION = {"definitions": ("Definition", 2), "clinical": ("Clinical pearl", 2), "traps": ("Exam trap", 2),
           "how": ("How it works", 3), "examples": ("Example", 3)}
NOT = "Not covered in materials"


def _plain(t):
    return re.sub(r"\s+", " ", re.sub(r"\*\*(.+?)\*\*", r"\1", t)).strip()


def _md(t):
    return re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", html.escape(t, quote=False))


def _pair(t):
    """A statement that already reads as prompt → answer: 'Term: …', 'Why X? …', 'A = B', 'A — B'."""
    p = _plain(t)
    m = re.match(r"^(.{3,80}?\?)\s+(.{3,})$", p)  # question-led
    if m:
        return m.group(1), m.group(2)
    for sep in (": ", " = ", " — ", " → "):
        i = p.find(sep)
        if 1 < i <= 70 and len(p) - i > 6:
            a, b = p[:i].strip(), p[i + len(sep):].strip()
            if sep in (" — ", " → ") and len(a) > 30:
                a += " …"  # a statement to finish, not a term to define
            return None if NOT in a or NOT in b else (a, b)
    return None


def _cloze(t, drugs):
    """Hide what's worth recalling, in this order of preference:
    1. the bold terms (unless the bold is the whole sentence), trailing colons kept outside the blank;
    2. the answer side of each 'A = B' / 'A: B' sentence (one blank per sentence);
    3. numbers with units and drug names.
    Returns the text with {{cN::…}} blanks, or None when nothing is worth blanking."""
    spans = re.findall(r"\*\*(.+?)\*\*", t)
    if spans and sum(len(s) for s in spans) < 0.6 * len(_plain(t)):
        n = [0]
        def rep(m):
            n[0] += 1
            body, tail = re.match(r"^(.*?)([:;,.]?)$", m.group(1)).groups()
            return "{{c%d::%s}}%s" % (n[0], body, tail)
        return re.sub(r"\*\*(.+?)\*\*", rep, html.escape(t, quote=False))
    sents = [x for x in re.split(r"(?<=[.;])\s+", _plain(t)) if x]
    out, n = [], 0
    for x in sents:
        pr = _pair(x)
        if pr and 2 <= len(pr[1]) < 110:
            n += 1
            sep = x[len(pr[0]):len(x) - len(pr[1])]
            out.append(html.escape(pr[0] + sep, quote=False) + "{{c%d::%s}}" % (n, html.escape(pr[1].rstrip(".;"), quote=False)) + (x[-1] if x[-1] in ".;" and not pr[1].endswith(("…",)) and x.rstrip(".;") != x else ""))
        else:
            out.append(html.escape(x, quote=False))
    if n:
        return " ".join(out)
    p = html.escape(_plain(t), quote=False)
    targets = re.findall(r"(?<![\w.])(\d+(?:[.,]\d+)?\s?(?:%|×|-fold|mg/L|mg|ng/mL|mEq/L|L|h|hours|half-lives|days|minutes)(?![\w]))", p)
    targets += [d for d in drugs if re.search(rf"\b{re.escape(d)}\b", p)]
    seen, n = set(), 0
    for tg in targets:
        if tg in seen or len(tg) < 2:
            continue
        seen.add(tg)
        n += 1
        k = n
        p = re.sub((rf"\b{re.escape(tg)}(?![\w}}])" if tg[0].isalnum() else re.escape(tg)), lambda m: "{{c%d::%s}}" % (k, m.group(0)), p, count=1)
        if n >= 3:
            break
    return p if n else None


def anki_data(built, exams):
    sys.path.insert(0, str(ROOT / "work"))
    import drugs as DR
    drug_names = sorted({n for d in DR.DRUGS for n in [d["name"], *d["aliases"]] if len(n) > 3}, key=len, reverse=True)
    syl = json.loads((ROOT / "work" / "syllabus.json").read_text())
    items, lectures = [], []
    uid = lambda *p: hashlib.sha1("|".join(map(str, p)).encode()).hexdigest()[:12]

    def add(**it):
        it.setdefault("tb", False)
        items.append(it)

    exam_qs = []
    for e in exams:
        exam_qs += [(e["id"], q) for q in json.loads((DOCS / "exams" / e["id"] / "quiz.json").read_text())]
    for lec in syl["lectures"]:
        lid = lec["id"]
        if lid not in built:
            continue
        c = json.loads((ROOT / "work" / lid / "content.resolved.json").read_text())
        parts = [{"n": i, "name": cl["name"], "anchor": slug(cl["name"])} for i, cl in enumerate(c["classes"], 1)]
        lectures.append({"id": lid, "unit": int(lec["unit"]), "title": c["lecture"]["title"], "date": lec["date"], "parts": parts})
        base = dict(lid=lid, unit=int(lec["unit"]))
        for i, cl in enumerate(c["classes"], 1):
            at = dict(base, part=i)
            for f in cl.get("high_yield", []):
                pr = _pair(f["text"])
                add(id=uid(lid, "hy", f["text"]), kind="fact", label="High-yield", depth=1, src=f.get("src", ""), tb=f.get("tb", False),
                    text=_md(f["text"]), front=pr[0] if pr else None, back=pr[1] if pr else None, cloze=_cloze(f["text"], drug_names), **at)
            for key, (label, depth) in SECTION.items():
                for f in cl["sections"].get(key, []):
                    pr = _pair(f["text"])
                    add(id=uid(lid, key, f["text"]), kind="fact", label=label, depth=3 if f.get("tb") else depth, src=f.get("src", ""), tb=f.get("tb", False),
                        text=_md(f["text"]), front=pr[0] if pr else None, back=pr[1] if pr else None, rev=key == "definitions" and bool(pr) and len(pr[0]) <= 50,
                        cloze=_cloze(f["text"], drug_names), **at)
            for h in cl.get("hooks", []):
                pr = _pair(h["text"])
                add(id=uid(lid, "hook", h["text"]), kind="fact", label="Memory hook", depth=2, src=h.get("src", ""), text=_md(h["text"]),
                    front=pr[0] if pr else None, back=pr[1] if pr else None, cloze=None, **at)
            for t in cl.get("comparisons", []):
                cols = t["columns"]
                for r in t["rows"]:
                    for j in range(1, len(cols)):
                        cell = r[j] if j < len(r) else ""
                        if not cell or NOT in cell:
                            continue
                        add(id=uid(lid, "tbl", t["title"], r[0], cols[j]), kind="table", label="Comparison table", depth=3, src=t.get("src", ""),
                            table=t["title"], front=f"{_plain(r[0])} · {_plain(cols[j])}", back=_plain(cell), text=_md(f"**{_plain(r[0])}**, {cols[j].lower()}: {cell}"), cloze=None, **at)
            for fl in cl.get("flows", []):
                steps = [_plain(s) for s in fl["steps"]]
                add(id=uid(lid, "flow", fl["title"]), kind="flow", label="Step by step", depth=3, src=fl.get("src", ""), front=f"In order: {_plain(fl['title'])}",
                    back=" → ".join(steps), steps=steps, text=html.escape(" → ".join(steps)),
                    cloze=" → ".join("{{c%d::%s}}" % (k, html.escape(s)) for k, s in enumerate(steps, 1)), **at)
        for r in c["guide"].get("cram", []):
            add(id=uid(lid, "cram", r["prompt"]), kind="pair", label="Cram sheet", depth=1, src=r.get("src", ""), front=_plain(r["prompt"]), back=_plain(r["answer"]),
                rev=len(_plain(r["prompt"])) <= 50, text=_md(f"**{r['prompt']}**: {r['answer']}"), cloze=None, part=0, **base)
        kb = json.loads((DOCS / lid / "kb.json").read_text())
        for q in kb["quiz"]:
            add(id=uid(lid, "q", q["id"]), kind="mcq", label="Self-test question", depth=2, src=q.get("src", ""), stem=_md(q["stem"]),
                options={k: _md(v) for k, v in q["options"].items()}, answer=q["answer"], why=_md(q.get("why", "")), part=0, cloze=None, raw=q["id"], **base)
        for ex, q in exam_qs:
            if (q.get("link") or {}).get("href", "").split("/")[2:3] == [lid]:
                add(id=uid(ex, q["id"]), kind="mcq", label="Practice-exam question", depth=2, src=q.get("src", ""), stem=_md(q["stem"]),
                    options={k: _md(v) for k, v in q["options"].items()}, answer=q["answer"], why=_md(q.get("why", "")), part=0, cloze=None, exam=ex, raw=q["id"], **base)
    # drugs: class + each cited fact, filed under the lectures that mention them
    kbs = {lid: json.loads((DOCS / lid / "kb.json").read_text()) for lid in built}
    for d in DR.DRUGS:
        pat = re.compile(r"\b(" + "|".join(re.escape(n) for n in [d["name"], *d["aliases"]]) + r")\b", re.I)
        lids = [lid for lid, kb in kbs.items() if any(pat.search(ch["text"]) for ch in kb["chunks"])]
        if not lids:
            continue
        base = dict(lid=lids[0], lids=lids, unit=int(d["unit"]), part=0, drug=d["name"])
        if d["cls"] != NOT:
            add(id=uid("drug", d["name"], "cls"), kind="pair", label="Drug class", depth=1, src=d.get("cls_src", ""), front=d["name"], back=d["cls"], rev=False,
                text=_md(f"**{d['name']}**: {d['cls']}"), cloze=None, **base)
        for f in d["facts"]:
            blank = pat.sub("_____", _plain(f["text"]))
            named = "_____" in blank
            add(id=uid("drug", d["name"], f["text"]), kind="fact", label="Drug fact", depth=3 if f.get("tb") else 2, src=f.get("src", ""), tb=f.get("tb", False),
                text=_md(f"**{d['name']}**: {f['text']}"), front=f"Which drug? {blank if named else _plain(f['text'])}", back=d["name"],
                cloze=pat.sub(lambda m: "{{c1::" + m.group(0) + "}}", html.escape(_plain(f["text"]), quote=False)) if named
                else "{{c1::" + html.escape(d["name"]) + "}}: " + html.escape(_plain(f["text"]), quote=False), **base)
    return {"lectures": lectures, "units": syl["units"], "items": items}


def anki_page(built, exams):
    data = anki_data(built, exams)
    out = DOCS / "anki"
    out.mkdir(exist_ok=True)
    (out / "data.json").write_text(json.dumps(data, ensure_ascii=False))
    body = f"""<header class="hero wrap ak-hero"><p class="eyebrow appear">Anki</p><h1 class="appear" style="--d:.05s">Your deck, built from the course.</h1>
<p class="lede appear" style="--d:.12s">Pick the lectures, how deep to go and the kinds of cards you like. Every card cites its slide or textbook page, and the deck downloads ready to import into Anki.</p></header>
<section class="section ak-sec"><div class="wrap ak-wrap"><div id="ak-app" class="ak-app"><p class="muted">Loading {len(data["items"]):,} card-ready items…</p></div></div></section>
<div id="ak-print" class="ak-print" aria-hidden="true"></div>
<script src="../assets/vendor/sql-wasm.js"></script><script src="../assets/anki.js"></script>"""
    (out / "index.html").write_text(page(f"Anki · {SITE_NAME}", body, depth=1, active="anki"))
    print(f"  anki: {len(data['items'])} card-ready items from {len(data['lectures'])} lectures")
