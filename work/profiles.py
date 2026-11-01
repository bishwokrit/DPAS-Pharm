"""Read the 'Drug Profile' appendix slides (one drug per slide) from a lecture's slides.json.

Each profile slide carries the same fields in its speaker notes (Formulation / Dose / Indications / Adverse effects /
Contraindications / Toxicity); the class is the third heading on the slide (or a 'Class:' note line).
Used by the lecture authoring files (profile tables) and by drugs.py (drug cards), so both stay word-for-word with the slides."""
import json
import re
from pathlib import Path

KEYS = {"drug": "name", "class": "cls", "formulation": "form", "strength/recommended dose": "dose", "dose (adult)": "dose", "adult dose": "dose",
        "indications": "ind", "adverse effects": "ae", "contraindications": "contra", "toxicity": "tox", "toxicity / overdose": "tox"}


def read(lec):
    slides = json.loads((Path(__file__).parent / lec / "slides.json").read_text())
    out = []
    for s in slides:
        heads = [i["text"] for i in s["items"] if i.get("heading")]
        first = s["items"][0]["text"].strip() if s["items"] else ""
        if not ((heads and heads[0] == "DRUG PROFILE") or first == "DRUG PROFILE") or not s.get("notes"):
            continue
        p = {"slide": s["slide"], "title": s["title"].strip()}
        # newer decks: one pipe-separated line, Drug|Class|Formulation|Dose|Indications|Adverse effects|Contraindications|Toxicity
        cells = [c.strip() for c in s["notes"].strip().split("\n")[0].split("|")]
        if len(cells) == 8:
            p.update(dict(zip(("_t", "cls", "form", "dose", "ind", "ae", "contra", "tox"), cells)))
            p.pop("_t")
        one = s["notes"].strip().split("\n")[0]
        if one.startswith("Drug:") and one.count(":") >= 6:
            # one-line form: "Drug: X. Class: Y. Formulation: … Toxicity / overdose: …."
            parts = re.split(r"(?:^|\.\s+)(Drug|Class|Formulation|Dose \(adult\)|Indications|Adverse effects|Contraindications|Toxicity / overdose):\s*", one)
            for k, v in zip(parts[1::2], parts[2::2]):
                p[KEYS[k.lower()]] = v.strip().rstrip(".")
        for line in s["notes"].split("\n"):
            m = re.match(r"^([A-Za-z /()]+):\s*(.+)$", line.strip())
            if m and m.group(1).strip().lower() in KEYS:
                p[KEYS[m.group(1).strip().lower()]] = m.group(2).strip()
        if "cls" not in p:
            body = [i["text"] for i in s["items"]]
            p["cls"] = body[2] if len(body) > 2 else ""
        t = p["title"]
        p["name"] = re.sub(r"\s*\(.*\)$", "", t).strip()
        p["aliases"] = [re.sub(r"\s+combinations?$", "", a.strip()) for a in re.split(r",|;|\band\b", re.findall(r"\(([^)]*)\)", t)[0])] if "(" in t else []
        out.append(p)
    return out


def table(profiles, title, lec_cite="", bold=False):
    """Two compact tables per group: how it is used, and what can go wrong. Cells are the slide's own words."""
    src = "; ".join(f"S{p['slide']}" for p in profiles)
    use = {"title": f"{title}: formulation, dose, indications", "columns": ["Drug", "Class", "Formulation", "Adult dose", "Indications"],
           "rows": [[p["title"], f"**{p.get('cls', '')}**", p.get("form", ""), p.get("dose", ""), p.get("ind", "")] for p in profiles], "src": src}
    safe = {"title": f"{title}: adverse effects, contraindications, toxicity", "columns": ["Drug", "Adverse effects", "Contraindications", "Toxicity / overdose"],
            "rows": [[p["title"], p.get("ae", ""), p.get("contra", ""), p.get("tox", "")] for p in profiles], "src": src}
    if bold:  # decks that bold every profile cell: keep that emphasis
        for t in (use, safe):
            t["rows"] = [[c if (not c or c.startswith("**")) else f"**{c}**" for c in r] for r in t["rows"]]
    return [use, safe]
