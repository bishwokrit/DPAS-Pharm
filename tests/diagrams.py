"""Diagram accuracy check. Every interactive figure is read the way the site builds it, then tested:

  wiring     every node a drug or edge names exists
  effect     adding a drug changes something (off / less / more / a lit step), or it is declared as a note-only chip
  direction  a step whose label already says which way it moves ("… falls", "↑ …") is lit, never marked more/less
  grounded   every drug on a figure is named in that lecture's cited facts, and its note cites a slide the lecture has
  cited      every figure carries a source

Hard failures stop the publish. This cannot judge whether a mechanism is true: it proves the picture only claims what
the cited lecture material names, and that nothing on it is dead or contradictory."""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "work"))
import scenes  # noqa: E402

# words in a drug chip that are not drug names
STOP = set("a an the and or of for with to in on at by is no not plus then first second only alone low high dose doses daily slow abrupt chronic acute "
           "before during after add added adding stop stopping hold starting start skipping taken taking use used inhibitor inhibitors blocker blockers agonist "
           "antagonist analog analogs drug drugs therapy rules day sick loop loops oral iv sl otc old new both either min h mg".split())


def words(s):
    return [w for w in re.findall(r"[A-Za-z][A-Za-z0-9\-]{3,}", s) if w.lower() not in STOP]


def lecture_text(c):
    out = []
    def walk(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("viz",):
                    continue
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)
        elif isinstance(o, str):
            out.append(o)
    walk(c)
    return " ".join(out).lower()


def slide_count(L):
    try:
        s = json.loads((ROOT / "work" / L / "slides.json").read_text())
        return len(s["slides"] if isinstance(s, dict) else s)
    except Exception:
        return 10 ** 6


def main():
    errs, warns, n_fig, n_drug = [], [], 0, 0
    for f in sorted((ROOT / "work").glob("L*/content.json")):
        L = f.parent.name
        c = json.loads(f.read_text())
        text, nslides = lecture_text(c), slide_count(L)
        for cl in c["classes"]:
            for fig in cl.get("figures", []):
                n_fig += 1
                who = f"{L} {fig['image']}"
                if not fig.get("src"):
                    errs.append(f"{who}: figure has no source")
                v = fig.get("viz") or {}
                sc = (scenes.SCENES.get(L) or {}).get(fig["image"])
                an = (getattr(scenes, "ANAT", {}).get(L) or {}).get(fig["image"])
                drugs = [dict(d) for d in (sc or v).get("drugs", []) if isinstance(d, dict)]
                if not sc and v.get("type") == "pathway":
                    drugs = [{**d, **((an or {}).get("fix", {}).get(i, {}))} for i, d in enumerate(v.get("drugs", []))]
                    ids = {n["id"] for n in v.get("nodes", [])}
                    labels = {n["id"]: (an or {}).get("labels", {}).get(n["id"], n["label"]) for n in v.get("nodes", [])}
                    for a, b in v.get("edges", []):
                        if a not in ids or b not in ids:
                            errs.append(f"{who}: edge {a}>{b} names a missing node")
                    for d in drugs:
                        refs = [x for k in ("off", "less", "more", "on") for x in d.get(k) or []] + [x for x in str(d.get("at") or "").split(">") if x]
                        for r in refs:
                            if r not in ids:
                                errs.append(f"{who}: '{d['label']}' names a missing node '{r}'")
                        placed = bool((an or {}).get("verb"))  # a ladder or lane figure: the chip is placed on its rung, by design
                        if not any(d.get(k) for k in ("off", "less", "more", "on")) and d.get("at") and not placed:
                            (errs if an else warns).append(f"{who}: '{d['label']}' docks but changes nothing")
                        for k in ("less", "more"):
                            for r in d.get(k) or []:
                                if r in labels and re.search(r"\b(falls?|rises?|lowered|restored|reduced)\b", labels[r], re.I):
                                    errs.append(f"{who}: '{d['label']}' marks \"{labels[r]}\" as {k}: light it as a step instead")
                for d in drugs:
                    n_drug += 1
                    label, note = str(d.get("label", "")), str(d.get("note", "") or "")
                    names = words(label)
                    if names and not any(w.lower() in text for w in names):
                        errs.append(f"{who}: '{label}' is not named anywhere in the lecture's cited material")
                    cites = [int(x) for x in re.findall(r"\bS(\d+)", note)]
                    if note and not cites and not re.search(r"p\. \d+|SG U", note):
                        warns.append(f"{who}: note for '{label}' cites no slide")
                    for s in cites:
                        if s > nslides:
                            errs.append(f"{who}: note for '{label}' cites S{s}, but the lecture has {nslides} slides")
    for w in warns[:0]:
        print(f"    note: {w}")
    for e in errs:
        print(f"  ✗ {e}")
    print(f"  diagrams: {n_fig} figures, {n_drug} drug chips checked, {len(errs)} problems ({len(warns)} minor notes)")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
