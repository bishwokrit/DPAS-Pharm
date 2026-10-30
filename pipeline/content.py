"""Load a lecture's content.json, check it follows the template, and assign answer letters.

Answer letters are assigned here (not by the author) so they're balanced across A–E,
never repeat back-to-back, and follow no pattern. Same lecture -> same letters every run.
"""
import json
import random
from pathlib import Path

# Two fixed templates: drug-class lectures (Units 2-6) and concept lectures (e.g., Unit 1).
TEMPLATES = {
    "drug_class": [
        ("overview", "Class"),
        ("prototype", "Prototype + other drugs named"),
        ("moa", "Mechanism of action"),
        ("indications", "Indications"),
        ("adverse", "Adverse effects (boxed warnings first)"),
        ("contra", "Contraindications"),
        ("interactions", "Drug interactions"),
        ("pk", "Pharmacokinetics"),
        ("monitoring", "Monitoring"),
        ("pearls", "Clinical pearls / \"why\" hook"),
    ],
    "concept": [
        ("definitions", "Key definitions"),
        ("how", "How it works"),
        ("clinical", "Clinical relevance"),
        ("examples", "Drugs named as examples"),
        ("traps", "Exam traps"),
    ],
}
SECTIONS = TEMPLATES["drug_class"]


def sections_for(cl):
    return TEMPLATES[cl.get("template", "drug_class")]


LETTERS = "ABCDE"


def load(path):
    return json.loads(Path(path).read_text())


def validate(c):
    """Return a list of problems (empty = OK)."""
    errs = []
    for key in ("lecture", "objectives", "classes"):
        if key not in c:
            errs.append(f"missing top-level '{key}'")
    obj_ids = {o["id"] for o in c.get("objectives", [])}
    for cl in c.get("classes", []):
        name = cl.get("name", "?")
        for o in cl.get("objectives", []):
            if o not in obj_ids:
                errs.append(f"{name}: unknown objective id {o}")
        if cl.get("template", "drug_class") not in TEMPLATES:
            errs.append(f"{name}: template must be one of {list(TEMPLATES)}")
            continue
        for key, _ in sections_for(cl):
            if key not in cl.get("sections", {}):
                errs.append(f"{name}: section '{key}' missing (use [] if not covered)")
        for key, facts in cl.get("sections", {}).items():
            for f in facts:
                if not f.get("src"):
                    errs.append(f"{name}/{key}: fact without citation: {f.get('text', '')[:60]}")
        for f in cl.get("high_yield", []):
            if not f.get("src"):
                errs.append(f"{name}/high_yield: fact without citation: {f.get('text', '')[:60]}")
        for h in cl.get("hooks", []):
            if h.get("kind") not in ("why", "mnemonic"):
                errs.append(f"{name}: hook kind must be 'why' or 'mnemonic'")
            if not h.get("src"):
                errs.append(f"{name}: hook without citation: {h.get('text', '')[:60]}")
        for q in cl.get("questions", []):
            if len(q.get("distractors", [])) != 4:
                errs.append(f"{name}: question needs exactly 4 distractors: {q.get('stem', '')[:50]}")
            if q.get("kind") not in ("vignette", "mechanism"):
                errs.append(f"{name}: question kind must be 'vignette' or 'mechanism'")
            for d in q.get("distractors", []):
                if not d.get("why"):
                    errs.append(f"{name}: distractor missing 'why' explanation: {d.get('text', '')[:50]}")
    return errs


def answer_sequence(n, seed):
    """Balanced A–E letters, shuffled, with no letter twice in a row."""
    rng = random.Random(seed)
    for _ in range(1000):
        bag = list(LETTERS * (n // 5)) + rng.sample(LETTERS, n % 5)
        rng.shuffle(bag)
        if all(bag[i] != bag[i + 1] for i in range(n - 1)):
            return bag
    # random shuffles rarely succeed for long lectures: build it greedily (most-remaining letter that differs from the last)
    left = {l: bag.count(l) for l in LETTERS}
    out = []
    for _ in range(n):
        pool = [l for l in LETTERS if left[l] and (not out or l != out[-1])]
        top = max(left[l] for l in pool)
        pick = rng.choice([l for l in pool if left[l] == top])
        out.append(pick)
        left[pick] -= 1
    return out


def resolve(c):
    """Give each question its lettered options; number them across the lecture."""
    qs = [q for cl in c["classes"] for q in cl.get("questions", [])]
    letters = answer_sequence(len(qs), c["lecture"]["id"])
    rng = random.Random(c["lecture"]["id"] + "-opts")
    for num, (q, ans) in enumerate(zip(qs, letters), start=1):
        others = [l for l in LETTERS if l != ans]
        ds = q["distractors"][:]
        rng.shuffle(ds)
        opts = {ans: {"text": q["correct"], "why": q.get("why_correct", ""), "correct": True}}
        for l, d in zip(others, ds):
            opts[l] = {"text": d["text"], "why": d["why"], "correct": False}
        q["number"] = num
        q["answer"] = ans
        q["options"] = {l: opts[l] for l in LETTERS}
    return c
