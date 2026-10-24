"""Lecture-level standard checks that the coverage audit doesn't do: home teaser, drug index, interactive figures,
textbook folded in, figure captions. Returns a list of problems (empty = meets the standard)."""
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _load(path):
    spec = importlib.util.spec_from_file_location(path.stem + "_std", path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def check(lec):
    lid, work = lec["id"], ROOT / "work" / lec["id"]
    bad = []
    c = json.loads((work / "content.resolved.json").read_text())
    g = work / f"guide_{lid}.py"
    if not g.exists():
        bad.append(f"no guide_{lid}.py (home teaser, summary, cram sheet)")
    elif not getattr(_load(g), "TEASER", "").strip():
        bad.append(f"TEASER is empty in guide_{lid}.py")
    if (work / "textbook.json").exists() and c.get("textbook_status") != "included":
        bad.append("assigned textbook pages are extracted but not folded in (textbook_status is not \"included\")")
    vjs = (ROOT / "site_src" / "assets" / "viz.js").read_text()
    for cl in c["classes"]:
        for fig in cl.get("figures", []):
            key = re.sub(r"_1$", "", fig["image"].rsplit(".", 1)[0])
            vt = (fig.get("viz") or {}).get("type")
            if not fig.get("caption"):
                bad.append(f"figure {fig['image']} has no caption")
            if not vt and f"V.{key} " not in vjs and f"V.{key}=" not in vjs:
                bad.append(f"figure {fig['image']} has no interactive version (add \"viz\": {{\"type\": …}})")
    sys.path.insert(0, str(ROOT / "work"))
    import drugs as DR
    cited = [d for d in DR.DRUGS if any(f["src"].startswith(lid + " ") or f" {lid} " in f" {f['src']} " for f in d["facts"])]
    if not cited:
        bad.append(f"no drug in work/drugs.py cites {lid} (add every drug the lecture names)")
    if any(cl.get("template") == "drug_class" for cl in c["classes"]):
        names = " ".join(d["name"].lower() + " " + " ".join(a.lower() for a in d["aliases"]) for d in DR.DRUGS)
        for cl in c["classes"]:
            for f in cl.get("prototype", [])[:1]:
                first = re.split(r"[\s(,:;—–-]+", re.sub(r"\*", "", f["text"]).strip())[0].lower()
                if first and len(first) > 3 and first not in names:
                    bad.append(f"{cl['name']}: prototype \"{first}\" is not in work/drugs.py")
    return bad
