"""Lecture-level standard checks that the coverage audit doesn't do: home teaser, drug index, interactive figures,
textbook folded in, figure captions, and a length budget (PA students are short on time: PA-level depth, no more).
Returns a list of problems (empty = meets the standard)."""
import importlib.util
import glob
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
            for f in cl["sections"].get("prototype", [])[:1]:
                first = re.split(r"[\s(,:;—–-]+", re.sub(r"\*", "", f["text"]).strip())[0].lower()
                if first and len(first) > 3 and first not in names:
                    bad.append(f"{cl['name']}: prototype \"{first}\" is not in work/drugs.py")
    # length budget: the deck may not grow past ~2x the lecture, the textbook may not outweigh the slides, bullets stay short
    facts = [x for cl in c["classes"] for v in cl["sections"].values() for x in v]
    tb = sum(bool(x.get("tb")) for x in facts)
    if facts and tb / len(facts) > MAX_TB_SHARE:
        bad.append(f"textbook facts are {tb / len(facts):.0%} of the guide (limit {MAX_TB_SHARE:.0%}): keep only what a PA needs, merge repeats")
    for x in facts:
        if len(x["text"].replace("**", "").split()) > MAX_WORDS:
            bad.append(f"bullet over {MAX_WORDS} words ({x['src']}): split or tighten it — {x['text'][:60]}…")
    deck = glob.glob(str(ROOT / "outputs" / lid / "*_study_deck.pptx"))
    n_lec = len(json.loads((work / "slides.json").read_text()))
    if deck:
        from pptx import Presentation
        n = len(Presentation(deck[0]).slides)
        if n > MAX_DECK_RATIO * n_lec:
            bad.append(f"deck has {n} slides for a {n_lec}-slide lecture (limit {int(MAX_DECK_RATIO * n_lec)}): cut beyond-PA detail and repeats")
    return bad


MAX_TB_SHARE = 0.30   # textbook-only bullets as a share of all guide bullets
MAX_WORDS = 40        # words per bullet
MAX_DECK_RATIO = 2.25 # deck slides per lecture slide (deck includes tables, figures and quick-check Q/A slides)
