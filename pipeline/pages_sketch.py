"""Sketch mode (hidden): Kahoot spreadsheets built from each unit's practice-exam questions, and a map of
Sketchy Pharm videos to our lectures and drugs. The tab only appears after Ctrl+Alt+S and the password.

Sketchy itself is paid, copyrighted material: the raw docs stay in the private repo (dpas-textbook/sketchy/).
Only work/sketchy.json is published — video titles and which of our drugs/lectures they cover, plus notes
written in our own words — never Sketchy's scenes, symbols or text."""
import hashlib, html, json, re
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
TEMPLATE = ROOT / "pipeline" / "templates" / "kahoot_template.xlsx"
SHORT = json.loads((ROOT / "pipeline" / "kahoot_stems.json").read_text())  # hand-shortened stems (Kahoot caps at 120 chars)
SET_SIZE = 25  # about a 12-minute game


def _h(s):
    return int(hashlib.sha1(s.encode()).hexdigest(), 16)


def kahoot_rows(q):
    """One exam question as a Kahoot row: stem ≤120, the answer plus 3 of the distractors (≤75 each), shuffled."""
    stem = SHORT.get(q["id"], q["stem"])
    wrong = sorted((k for k in q["options"] if k != q["answer"]), key=lambda k: _h(q["id"] + k))[:3]
    opts = sorted([q["answer"], *wrong], key=lambda k: _h(q["id"] + "pos" + k))
    texts = [q["options"][k] for k in opts]
    if len(stem) > 120 or any(len(t) > 75 for t in texts):
        return None
    calc = bool(re.search(r"\d", stem)) and len(stem) >= 90
    secs = 60 if calc else 20 if len(stem) < 80 and max(map(len, texts)) < 40 else 30
    return [stem, *texts, secs, str(opts.index(q["answer"]) + 1)]


def build_kahoots():
    """docs/sketch/kahoot/unit<N>_set<k>.xlsx for every unit that has a practice exam. Returns the page's listing."""
    out_dir = DOCS / "sketch" / "kahoot"
    out_dir.mkdir(parents=True, exist_ok=True)
    keep = set()
    units = {}
    for meta in sorted((DOCS / "exams").glob("*/meta.json")):
        m = json.loads(meta.read_text())
        units.setdefault(m["unit"], []).extend(json.loads((meta.parent / "quiz.json").read_text()))
    listing, skipped = [], 0
    for unit, qs in sorted(units.items()):
        rows = []
        for q in sorted(qs, key=lambda q: _h("mix" + q["id"])):  # mix topics and both exams across sets
            r = kahoot_rows(q)
            (rows.append(r) if r else None)
            skipped += r is None
        sets = [rows[i:i + SET_SIZE] for i in range(0, len(rows), SET_SIZE)]
        files = []
        for k, chunk in enumerate(sets, 1):
            wb = openpyxl.load_workbook(TEMPLATE)
            ws = wb["Sheet1"]
            for i in range(9, ws.max_row + 1):  # row 8 is the header;
                for col in "BCDEFGH":
                    ws[f"{col}{i}"] = None
            for i, r in enumerate(chunk):
                ws[f"A{9 + i}"] = i + 1
                for col, v in zip("BCDEFGH", r):
                    ws[f"{col}{9 + i}"] = v
            name = f"unit{unit}_set{k}.xlsx"
            keep.add(name)
            if (out_dir / name).exists():  # xlsx files carry a save time; only rewrite when the questions changed
                old = openpyxl.load_workbook(out_dir / name)["Sheet1"]
                if [[old[f"{c}{9 + i}"].value for c in "BCDEFGH"] for i in range(len(chunk) + 1)] == [*chunk, [None] * 7]:
                    files.append({"name": name, "n": len(chunk)})
                    continue
            wb.save(out_dir / name)
            files.append({"name": name, "n": len(chunk)})
        listing.append({"unit": unit, "total": len(rows), "files": files})
    for old in out_dir.glob("*.xlsx"):
        (old.unlink() if old.name not in keep else None)
    if skipped:
        print(f"  sketch: {skipped} questions skipped (too long for Kahoot; add a short stem in pipeline/kahoot_stems.json)")
    return listing


def sketch_page(page, SITE_NAME):
    kahoots = build_kahoots()
    sk_file = ROOT / "work" / "sketchy.json"
    sk = json.loads(sk_file.read_text()) if sk_file.exists() else {"videos": []}
    cards = "".join(
        f'<div class="sx-unit"><div class="sx-unit-h"><strong>Unit {u["unit"]}</strong><span>{u["total"]} questions · {len(u["files"])} games</span></div>'
        f'<div class="sx-files">' + "".join(
            f'<a class="sx-file" href="kahoot/{f["name"]}" download><span>Set {i}</span><small>{f["n"]} Q · .xlsx</small></a>'
            for i, f in enumerate(u["files"], 1)) + "</div></div>" for u in kahoots)
    vids = sk.get("videos", [])
    if vids:
        sketchy = '<input class="sx-find" id="sx-find" type="search" placeholder="Filter by drug, video or lecture" aria-label="Filter Sketchy videos"><div class="sx-vids" id="sx-vids">' + "".join(
            f'<div class="sx-vid" data-q="{html.escape((v["title"] + " " + " ".join(v.get("drugs", [])) + " " + " ".join(v.get("lectures", []))).lower())}">'
            f'<div class="sx-vid-h"><strong>{html.escape(v["title"])}</strong><span>{html.escape(v.get("section", ""))}</span></div>'
            + (f'<div class="sx-chips">' + "".join(f'<a href="../drugs/index.html#{re.sub(r'[^a-z0-9]+', '-', d.lower()).strip('-')}">{html.escape(d)}</a>' for d in v.get("drugs", [])) + "</div>" if v.get("drugs") else "")
            + (f'<p>{html.escape(v["note"])}</p>' if v.get("note") else "")
            + (f'<small>{" · ".join(html.escape(l) for l in v["lectures"])}</small>' if v.get("lectures") else "")
            + "</div>" for v in vids) + "</div>"
    else:
        sketchy = '<div class="sx-empty"><strong>Waiting for your Sketchy docs</strong><span>Once they are uploaded, every Sketchy Pharm video is matched to the lectures and drugs it covers, right here.</span></div>'
    body = f"""<header class="hero wrap"><p class="eyebrow">Sketch</p><h1>Sketch mode</h1>
<p class="lede">Game-night Kahoots for every unit, and Sketchy Pharm matched to the lectures. Only you can see this tab.</p>
<p><button class="btn ghost small" id="sx-lock" type="button">Lock Sketch mode</button></p></header>
<section class="section" id="kahoot"><div class="wrap"><p class="kicker">1 · Kahoot</p><h2>Play a unit</h2>
<p class="sx-how">In Kahoot: <b>Create</b> → <b>Kahoot</b> → <b>Add question</b> → <b>Import spreadsheet</b>, then drop in a set. Each set is 25 mixed questions from that unit's practice exams.</p>
<div class="sx-units">{cards}</div></div></section>
<section class="section" id="sketchy"><div class="wrap"><p class="kicker">2 · Sketchy Pharm</p><h2>Watch the right sketch</h2>{sketchy}</div></section>
<script>if(!(function(){{try{{return JSON.parse(localStorage.getItem("sketch"))}}catch(e){{}}}})())location.replace("../index.html");
document.getElementById("sx-lock").onclick=function(){{try{{localStorage.removeItem("sketch")}}catch(e){{}}location.href="../index.html"}};
var f=document.getElementById("sx-find");f&&f.addEventListener("input",function(){{var q=f.value.toLowerCase().trim();document.querySelectorAll(".sx-vid").forEach(function(v){{v.hidden=q&&v.dataset.q.indexOf(q)<0}})}});</script>"""
    out = DOCS / "sketch"
    out.mkdir(exist_ok=True)
    (out / "index.html").write_text(page(f"Sketch · {SITE_NAME}", body, depth=1, active="sketch"))
    print(f"  sketch: {sum(len(u['files']) for u in kahoots)} Kahoot sets, {len(vids)} Sketchy videos mapped")
