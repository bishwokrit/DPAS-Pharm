"""Pull the lecture's own knowledge-check questions out of slides.json, exactly as written.

Handles two slide styles seen in this course:
  - "Quick Check" slide (stem + A–D options laid out in a grid) followed by an "Answer" slide
  - "Recall Quiz" slides ("1. stem" + "A. option" lines) with an "Answer Key" slide ("1. A — why")
Returns [{src, stem, options: {A: text, ...}, answer, why}].
"""
import re


def body(slide):
    return [it["text"].strip() for it in slide["items"] if not it.get("heading")]


def quick_checks(slides):
    out = []
    for i, s in enumerate(slides[:-1]):
        nxt = slides[i + 1]
        if not re.match(r"quick check", s.get("title", ""), re.I) or not re.match(r"answer", nxt.get("title", ""), re.I):
            continue
        items = body(s)
        stem, opts = items[0], items[1:]
        letters = [it["text"].strip() for it in nxt["items"] if re.fullmatch(r"[A-E]", it["text"].strip())]
        ans_items = body(nxt)
        why = next((t for t in ans_items if t.startswith("Why:")), "")
        out.append({"src": f"S{s['slide']}-{nxt['slide']}", "stem": stem,
                    "options": dict(zip("ABCDE", opts)), "answer": letters[0] if letters else "",
                    "why": why.replace("Why:", "", 1).strip()})
    return out


def recall_quiz(slides):
    qs, key, key_src = {}, {}, ""
    for s in slides:
        title = s.get("title", "")
        if re.search(r"recall quiz.*answer key", title, re.I):
            key_src = f"S{s['slide']}"
            for t in body(s):
                m = re.match(r"(\d+)\.\s*([A-E])\s*—\s*(.+)", t)
                if m:
                    key[m.group(1)] = (m.group(2), m.group(3).strip())
        elif re.search(r"recall quiz", title, re.I):
            cur = None
            for t in body(s):
                m = re.match(r"(\d+)\.\s+(.+)", t)
                o = re.match(r"([A-E])\.\s+(.+)", t)
                if m:
                    cur = m.group(1)
                    qs[cur] = {"src": f"S{s['slide']}", "stem": m.group(2).strip(), "options": {}}
                elif o and cur:
                    qs[cur]["options"][o.group(1)] = o.group(2).strip()
    out = []
    for n, q in qs.items():
        ans, why = key.get(n, ("", ""))
        out.append({**q, "src": f"{q['src']}; {key_src}" if key_src else q["src"], "answer": ans, "why": why})
    return out


def extract(slides):
    return quick_checks(slides) + recall_quiz(slides)


if __name__ == "__main__":
    import json
    import sys
    for q in extract(json.load(open(sys.argv[1]))):
        print(q["src"], "|", q["stem"][:60], "|", list(q["options"].values()), "|", q["answer"], "|", q["why"][:50])
