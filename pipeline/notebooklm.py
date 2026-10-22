"""Build the NotebookLM pack for one lecture from its resolved content.

  outputs/<LEC>/notebooklm/<LEC>_source[_partN].md   -> upload these as sources
  outputs/<LEC>/notebooklm/<LEC>_instructions.md     -> copy-paste prompts
"""
import json
import sys
from pathlib import Path

from content import sections_for


def fact_line(f):
    tag = ("[TB] " if f.get("tb") else "") + ("[SG] " if f.get("sg") else "")
    src = f" ({f['src']})" if f.get("src") else ""
    return f"- {tag}{f['text']}{src}"


def class_block(c, pending):
    kind = "Topic" if c.get("template") == "concept" else "Drug class"
    out = [f"\n## {kind}: {c['name']}", f"Learning objectives covered: {', '.join(c.get('objectives', [])) or 'none listed'}"]
    for key, label in sections_for(c):
        out.append(f"\n### {c['name']} — {label}")
        facts = c["sections"].get(key, [])
        if facts:
            out += [fact_line(f) for f in facts]
        else:
            out.append("- Not covered in slides (textbook pending)." if pending else "- Not covered in materials.")
    for fig in c.get("figures", []):
        out.append(f"\n### Figure: {fig.get('title', '')}\n- {fig['caption']} ({fig.get('src', '')})")
    for cf in c.get("conflicts", []):
        out.append(f"\n### Conflict between sources: {cf['topic']}")
        out.append(f"- Lecture slides: {cf['slides']['text']} ({cf['slides']['src']})")
        out.append(f"- Textbook: {cf['textbook']['text']} ({cf['textbook']['src']})")
    for t in c.get("comparisons", []):
        out.append(f"\n### Comparison: {t['title']} ({'[TB] ' if t.get('tb') else ''}{t.get('src', '')})")
        out.append("| " + " | ".join(t["columns"]) + " |")
        out.append("|" + "---|" * len(t["columns"]))
        out += ["| " + " | ".join(str(x) for x in r) + " |" for r in t["rows"]]
    if c.get("hooks"):
        out.append(f"\n### {c['name']} — Memory hooks")
        for h in c["hooks"]:
            label = "Mnemonic (memory aid)" if h["kind"] == "mnemonic" else "Why it happens"
            out.append(f"- {label}: {h['text']} ({h.get('src', '')})")
    if c.get("high_yield"):
        out.append(f"\n### {c['name']} — High-yield summary")
        out += [fact_line(f) for f in c["high_yield"]]
    return "\n".join(out)


def header(c, part=None):
    lec = c["lecture"]
    lines = [f"# {lec['id']}: {lec['title']}" + (f" — part {part}" if part else ""),
             "",
             "Pharmacology study source. Built ONLY from the lecture slides, the assigned textbook pages, the course syllabus, and the course study guide.",
             "Citation key: S12 = lecture slide 12; p. 245 = textbook page 245; SG U1-R3 = course study guide, Unit 1 item R3.",
             "[TB] = from the textbook, not on the lecture slides. [SG] = from the course study guide, not on the lecture slides.",
             "Bold text = emphasized on the lecture slides.",
             ]
    if c.get("textbook_status") != "included":
        lines.append("NOTE: The textbook has not been added yet; this source covers the lecture slides only.")
    lines += ["", "## Learning objectives"]
    lines += [f"- {o['id']}: {o['text']}" + (f" ({o['src']})" if o.get("src") else "") for o in c["objectives"]]
    if c.get("about"):
        lines += ["", "## About this lecture"] + [fact_line(f) for f in c["about"]]
    return "\n".join(lines)


def split_by_words(blocks, limit):
    parts, cur, n = [], [], 0
    for b in blocks:
        w = len(b.split())
        if cur and n + w > limit:
            parts.append(cur)
            cur, n = [], 0
        cur.append(b)
        n += w
    parts.append(cur)
    return parts


def instructions(c):
    lec = c["lecture"]
    nb = c.get("notebooklm", {})
    classes = ", ".join(cl["name"] for cl in c["classes"])
    objectives = "\n".join(f"- {o['id']}: {o['text']}" for o in c["objectives"])
    qs = nb.get("suggested_questions", [])
    patient = nb.get("patient", "a single patient whose care touches each topic in order")
    concept = all(cl.get("template") == "concept" for cl in c["classes"])
    path = ("For each topic follow the same path: key definitions, how it works, clinical relevance, drugs named as examples, exam traps."
            if concept else
            "For each class follow the same path: class, prototype and other drugs named, mechanism of action, indications, adverse effects (boxed warnings first), contraindications, drug interactions, pharmacokinetics, monitoring, clinical pearls.")
    story_steps = ("At each step, show how the concept explains something that happens to this patient's medicines, using the drugs named in the source."
                   if concept else
                   "At each step, show why this patient would get (or must avoid) a drug in that class, its mechanism, what side effects to watch for in this patient, and what to monitor.")
    return f"""# NotebookLM instructions — {lec['id']}: {lec['title']}

## How to use
1. In NotebookLM, create a new notebook named "{lec['id']} {lec['title']}".
2. Add sources: upload every `{lec['id']}_source*.md` file in this folder (nothing else).
3. For each feature below, click its **Customize** (pencil) option and paste the box under it.

---

## 1. Audio overview (podcast)
```
Audience: a physician assistant student preparing for exams and the PANCE.
Use ONLY the uploaded source. Do not add outside facts. If something is not in the source, say it is not covered.
Go topic by topic in this order: {classes}.
{path}
Spend the most time on bolded (lecture-emphasized) points. Say when a point is textbook-only ([TB]) or study-guide-only ([SG]).
Explain WHY adverse effects follow from the mechanism, using the "Why it happens" hooks.
Point out how to tell similar drugs apart, using the comparison tables.
Call out any place the slides and textbook disagree.
End with the high-yield summary for each class.
```

## 2. Video overview — single-patient story
```
Use ONLY the uploaded source. No outside facts.
Tell the whole lecture as one continuous story following ONE patient: {patient}.
Move through the topics in this order: {classes}. {story_steps}
Keep the same patient the entire video; let their story connect each class to the next.
Use simple visuals: mechanism diagrams, side-by-side drug comparisons, and a recap of high-yield points at the end.
Audience: physician assistant students.
```

## 3. Quiz and flashcards
```
Use ONLY the uploaded source.
Quiz: PANCE-style. Mix about half clinical vignettes and half mechanism questions. Five answer choices (A–E), one best answer, all choices similar in length and detail. Explain why the right answer is right and why each wrong choice is wrong. Cover every topic and every learning objective; weight lecture-emphasized (bold) facts more heavily.
Flashcards: one fact per card. Front = a question or cue (drug, class, effect, or "how do you tell X from Y"). Back = the answer with its citation (slide or page). Include mechanism-to-side-effect "why" cards and discriminator cards.
```

## 4. Questions to ask the notebook
{chr(10).join(f'{i}. {q}' for i, q in enumerate(qs, 1)) if qs else '(add suggested_questions in content.json)'}

---
Learning objectives for reference:
{objectives}
"""


def main(content_path, out_dir, max_words):
    c = json.loads(Path(content_path).read_text())
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for old in out.glob("*_source*.md"):
        old.unlink()
    pending = c.get("textbook_status") != "included"
    blocks = [class_block(cl, pending) for cl in c["classes"]]
    parts = split_by_words(blocks, int(max_words))
    lid = c["lecture"]["id"]
    for i, p in enumerate(parts, 1):
        name = f"{lid}_source.md" if len(parts) == 1 else f"{lid}_source_part{i}.md"
        (out / name).write_text(header(c, i if len(parts) > 1 else None) + "\n" + "\n".join(p) + "\n")
    (out / f"{lid}_instructions.md").write_text(instructions(c))
    print(f"  notebooklm: {len(parts)} source file(s) + instructions -> {out}")


if __name__ == "__main__":
    main(*sys.argv[1:4])
