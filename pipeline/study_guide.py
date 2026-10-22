"""Split the course study guide (.docx) into citable items with their answer-key answers.

Item IDs: U1-R3 = Unit 1, Key Concept Recall question 3; U1-M = matching exercise; U1-S = clinical scenario.
Writes work/study_guide.json and work/study_guide.md.
"""
import json
import re
import sys
from pathlib import Path

import docx
from docx.table import Table
from docx.text.paragraph import Paragraph


def lines_of(path):
    d = docx.Document(path)
    out = []
    for b in d.element.body.iterchildren():
        tag = b.tag.split("}")[1]
        if tag == "p":
            p = Paragraph(b, d)
            if p.text.strip():
                style = p.style.name if p.style is not None else ""
                level = int(style[-1]) if style.startswith("Heading") and style[-1].isdigit() else 0
                out.append(("#" * level + " " if level else "") + p.text.strip())
        elif tag == "tbl":
            for r in Table(b, d).rows:
                out.append("| " + " | ".join(c.text.replace("\n", " ") for c in r.cells) + " |")
    return out


def parse(lines):
    items, unit, part, in_key = {}, None, None, False
    for ln in lines:
        if ln.startswith("## Answer Key"):
            in_key, unit = True, None
            continue
        m = re.match(r"#+\s*Unit (\d+)", ln)
        if m:
            unit, part = m.group(1), None
            continue
        if ln.startswith("### "):
            h = ln.lower()
            part = "R" if "recall" in h else "M" if "matching" in h else "S" if "scenario" in h else None
            continue
        if not unit:
            continue
        if not in_key:
            if part == "R":
                n = sum(1 for k in items if k.startswith(f"U{unit}-R")) + 1
                items[f"U{unit}-R{n}"] = {"unit": unit, "question": ln, "answer": ""}
            elif part in ("M", "S"):
                it = items.setdefault(f"U{unit}-{part}", {"unit": unit, "question": "", "answer": ""})
                it["question"] = (it["question"] + "\n" + ln).strip()
        else:
            if ln.startswith("Recall:"):
                for num, ans in re.findall(r"\((\d+)\)\s*(.+?)(?=\s*\(\d+\)\s|$)", ln[7:]):
                    if f"U{unit}-R{num}" in items:
                        items[f"U{unit}-R{num}"]["answer"] = ans.strip()
            elif ln.startswith("Matching:") and f"U{unit}-M" in items:
                items[f"U{unit}-M"]["answer"] = ln[9:].strip()
            elif ln.startswith("Scenario:") and f"U{unit}-S" in items:
                items[f"U{unit}-S"]["answer"] = ln[9:].strip()
    return items


def main(docx_path, out_dir):
    items = parse(lines_of(docx_path))
    out = Path(out_dir)
    (out / "study_guide.json").write_text(json.dumps(items, indent=1, ensure_ascii=False))
    md = ["# Course study guide items\n"]
    for k, v in items.items():
        md.append(f"\n## {k}\nQ: {v['question']}\n\nA: {v['answer'] or '(no answer key)'}")
    (out / "study_guide.md").write_text("\n".join(md) + "\n")
    print(f"  study guide: {len(items)} items")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
