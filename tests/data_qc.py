"""Cross-file consistency of the built site: every lecture has all its outputs, every stored link and anchor resolves,
and the generated data (drug of the day, structures, Anki, Kahoot, search) all point at things that exist.
Used by ./run.sh check. Exit code 1 = problems found."""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
sys.path.insert(0, str(ROOT / "work"))
import drugs as DR  # noqa: E402

problems = []
bad = problems.append
ids_cache = {}


def ids(page):
    if page not in ids_cache:
        ids_cache[page] = set(re.findall(r'id="([^"]+)"', page.read_text())) if page.exists() else None
    return ids_cache[page]


def resolve(href, here):
    """A site-relative href from page `here` → (file exists, anchor exists)."""
    file, _, hash_ = href.partition("#")
    target = (here.parent / file.split("?")[0]).resolve() if file else here
    if target.is_dir():
        target = target / "index.html"
    if not target.exists():
        return f"missing file {href}"
    if target.parent.name == "drugs" and hash_:  # the drug index opens a drug sheet from its slug (drugs.js)
        return None if hash_ in {re.sub(r"[^a-z0-9]+", "-", d["name"].lower()).strip("-") for d in DR.DRUGS} else f"unknown drug {href}"
    if hash_.startswith("q-") and (target.parent / "quiz.json").exists():  # exam pages open a question by its id (exam.js)
        return None if any(q["id"] == hash_[2:] for q in json.loads((target.parent / "quiz.json").read_text())) else f"unknown question {href}"
    if hash_ and target.suffix == ".html" and hash_ not in (ids(target) or set()):
        return f"missing anchor {href}"
    return None


syl = json.loads((ROOT / "work" / "syllabus.json").read_text())
built = [l for l in syl["lectures"] if (DOCS / l["id"] / "kb.json").exists()]

# 1. every built lecture has its full set of outputs
for l in built:
    d, lid = DOCS / l["id"], l["id"]
    need = [d / "index.html", d / f"{lid}_study_guide.pdf", d / "kb.json"]
    need += list(d.glob("*_study_deck.pptx"))[:1] or [d / "(study deck .pptx)"]
    need += [DOCS / "sketch" / "kahoot" / f"unit{l['unit']}_{lid}.xlsx"]
    for f in need:
        if not f.exists():
            bad(f"{lid}: missing {f.relative_to(DOCS) if f.is_relative_to(DOCS) else f.name}")
    audit = ROOT / "work" / lid / "audit.json"
    if not audit.exists() or not json.loads(audit.read_text())["passed"]:
        bad(f"{lid}: coverage audit has not passed (run ./run.sh {lid})")
    # every figure has an interactive twin (a dedicated one or a generic "viz" type)
    c = json.loads((ROOT / "work" / lid / "content.resolved.json").read_text())
    vjs = (ROOT / "site_src" / "assets" / "viz.js").read_text()
    for cl in c["classes"]:
        for fig in cl.get("figures", []):
            key = re.sub(r"_1$", "", fig["image"].rsplit(".", 1)[0])
            vt = (fig.get("viz") or {}).get("type")
            if vt and f'"{vt}"' not in vjs and f"V.{vt} " not in vjs and f" {vt}:" not in vjs:
                bad(f"{lid}: figure {fig['image']} names an unknown interactive type \"{vt}\"")
            elif not vt and f"V.{key} " not in vjs and f"V.{key}=" not in vjs:
                bad(f"{lid}: figure {fig['image']} has no interactive version (add \"viz\" to it in the author script)")

# 2. stored links in question banks and lecture data resolve
for l in built:
    kb = json.loads((DOCS / l["id"] / "kb.json").read_text())
    here = DOCS / l["id"] / "index.html"
    for q in kb["quiz"]:
        if q.get("link") and (err := resolve(q["link"]["href"], here)):
            bad(f"{l['id']} self-test {q['id']}: {err}")
for qf in sorted((DOCS / "exams").glob("*/quiz.json")):
    here = qf.parent / "index.html"
    for q in json.loads(qf.read_text()):
        if q.get("link") and (err := resolve(q["link"]["href"], here)):
            bad(f"{qf.parent.name} {q['id']}: {err}")
for e in json.loads((DOCS / "search.json").read_text()):
    if (err := resolve(e["u"], DOCS / "index.html")):
        bad(f"search: {err}")

# 3. generated data agrees with the drug list and the lectures
names = {d["name"] for d in DR.DRUGS}
for d in json.loads((DOCS / "drugs" / "dotd.json").read_text()):
    if d["name"] not in names:
        bad(f"drug of the day: unknown drug {d['name']}")
    if len(d["qs"]) < 3:
        bad(f"drug of the day: {d['name']} has only {len(d['qs'])} questions")
for n in json.loads((DOCS / "drugs" / "mol3d.json").read_text()):
    if n not in names:
        bad(f"3D structure for unknown drug {n}")
anki = json.loads((DOCS / "anki" / "data.json").read_text())
lids = {l["id"]: l for l in anki["lectures"]}
for it in anki["items"]:
    if it["lid"] not in lids:
        bad(f"anki item for unknown lecture {it['lid']}")
    elif it.get("part") and it["part"] not in {p["n"] for p in lids[it["lid"]]["parts"]}:
        bad(f"anki item {it['id']}: part {it['part']} not in {it['lid']}")
    if it["kind"] == "mcq" and it["answer"] not in it["options"]:
        bad(f"anki item {it['id']}: answer {it['answer']} not among options")
    if it.get("cloze") and "{{c1::" not in it["cloze"]:
        bad(f"anki item {it['id']}: cloze without a first blank")
if set(lids) != {l["id"] for l in built}:
    bad("anki data does not cover exactly the built lectures")

for p in problems[:60]:
    print("  ✗ " + p)
print(f"  data: {len(built)} lectures, {len(anki['items'])} Anki items, {len(names)} drugs checked, {len(problems)} problems")
sys.exit(1 if problems else 0)
