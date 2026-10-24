"""work/<ID>/AUTHOR_BRIEF.md — the checklist Claude authors a new lecture from. It lists every slide, every assigned-reading
section and every saved figure, so nothing can be missed, and restates the standard every lecture is held to.
The audit and ./run.sh new <ID> then check the finished content against the same list."""
import json
import re
from pathlib import Path

import reading_cov

ROOT = Path(__file__).resolve().parent.parent
VIZ_TYPES = {
    "dose-response": "graded dose-response curve (EC50, Emax)",
    "antagonist": "agonist curve shifted by a competitive vs noncompetitive antagonist",
    "potency-efficacy": "two drugs compared on potency and efficacy",
    "therapeutic-index": "ED50 vs TD50, narrow vs wide window",
    "cyp-interaction": "substrate level with an inhibitor vs an inducer",
    "half-life": "exponential decay over half-lives",
    "steady-state": "accumulation to steady state, with/without loading dose",
    "fill-empty": "time to fill and time to empty are the same",
    "adme": "absorption → distribution → metabolism → excretion map",
    "bars": "any bar chart; give {title, unit, bars:[{label, value, note}], steps:[{label, pick}]}",
}


def _first(items):
    for it in items:
        t = it.get("text", "").strip()
        if t:
            return t[:90]
    return "(picture only — look at the slide image)"


def main(lec, work):
    lid = lec["id"]
    slides = json.loads((work / "slides.json").read_text())
    tb = json.loads((work / "textbook.json").read_text()) if (work / "textbook.json").exists() else []
    figs = sorted(p.name for p in (work / "figures").glob("*")) if (work / "figures").exists() else []
    kind = "concept" if lec.get("unit") == 1 else "drug_class"
    L = [f"# Authoring brief — {lid}: {lec['title']} ({lec.get('date', '')})", "",
         f"Tell Claude: **\"author {lid}\"**. Claude writes `work/{lid}/author_{lid}.py`, `guide_{lid}.py` and "
         f"`textbook_{lid}.py` (copy the shape of the L02 files), adds the lecture's drugs to `work/drugs.py`, then runs "
         f"`./run.sh new {lid}` until every gate says PASS.", "",
         "## The standard (every lecture, no exceptions)",
         "- **Sources:** slides (with speaker notes), the assigned textbook pages, the syllabus and the course study guide only. "
         "No internet facts. Every fact cited (`S12`, `S12 (notes)`, `p. 245`, `SG U1-R3`).",
         "- **Everything taught:** every slide line and every assigned-reading section below lands in the guide (the audit fails otherwise). "
         "A section that belongs to another session goes in `READING_SKIP` with the reason.",
         "- **Same level, easier to learn:** keep the textbook’s depth; make it easier with order (big idea → mechanism → "
         "clinical use → traps), short bullets (≤25 words), comparison tables on discriminators, flows, and why-hooks. "
         "A student using only the guide or only the deck should be able to answer any exam question on this lecture.",
         f"- **Template:** `{kind}` for every class/topic"
         + (" (overview, prototype, moa, indications, adverse — boxed warnings first, contra, interactions, pk, monitoring, pearls)."
            if kind == "drug_class" else " (definitions, how, clinical, examples, traps)."),
         "- **Textbook facts** in `textbook_<ID>.py` as `(\"text\", \"p. N\")`; write apostrophes as ’ so `./run.sh check` can verify the numbers on that page.",
         "- **Questions:** ~50/50 vignette and mechanism; 5 options, all similar in length; rebuild every quick-check slide question (`from_slides`).",
         "- **Figures:** each saved figure gets a caption and an interactive version (`\"viz\": {\"type\": …}`, list below).",
         "- **Drugs:** every drug named gets an entry (or new facts) in `work/drugs.py`, citing `" + lid + " S#` or `p. N`.",
         "- **Home teaser:** `TEASER` in `guide_<ID>.py` — two calm sentences, no hype.",
         "- **No school, course-director or instructor names** anywhere (slide 1 credits are skipped on purpose).",
         "- **Original files are never edited** (they are fingerprinted; the build stops if one changes).", "",
         "## Objectives to cover", *[f"- {o['id']}: {o['text']}" for o in lec.get("objectives", [])], "",
         f"## Slides ({len(slides)}) — every one must be covered", *[f"- [ ] S{s['slide']}: {s.get('title') or _first(s.get('items', []))}" for s in slides], ""]
    if tb:
        hs = reading_cov.headings(tb)
        L += [f"## Assigned reading — pages {tb[0]['page']}–{tb[-1]['page']} ({len(hs)} sections to teach)",
              *[f"- [ ] p. {h['page']}: {h['heading']}" for h in hs], ""]
    else:
        L += ["## Assigned reading", "- Textbook pages not extracted (no readings in the syllabus, or the private textbook repo is missing).", ""]
    L += ["## Figures saved from the slides", *([f"- [ ] `{f}` — caption + viz type" for f in figs] or ["- none"]), "",
          "## Interactive figure types (`\"viz\": {\"type\": \"…\"}` on a figure)", *[f"- `{k}` — {v}" for k, v in VIZ_TYPES.items()], "",
          "If none fits, ask for a new dedicated diagram in `site_src/assets/viz.js` (same palette, reset after 30 s idle, Try-it steps)."]
    out = work / "AUTHOR_BRIEF.md"
    out.write_text("\n".join(L) + "\n")
    return out
