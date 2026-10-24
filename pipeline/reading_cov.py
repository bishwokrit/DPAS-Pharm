"""Assigned-reading coverage: every section heading in the lecture's textbook pages must be taught somewhere in the guide
(or skipped on purpose with a reason in content.json "reading_skip"). The syllabus makes assigned reading testable."""
import re

from audit import toks

NOISE = re.compile(r"^Term Definition$|Approach and Goals|Adverse Effect$|Katzung|Vanderah|PhD|\bMD\b|Figure|FIGURE|TABLE|Table|CHAPTER|SECTION|Basic Principles|Case Study|REFERENCES|SUMMARY")


def headings(textbook):
    """Section headings from the extracted page text: short title-like lines (OCR fragments and labels filtered out)."""
    out, seen = [], set()
    for p in textbook:
        lines = [l.strip() for l in p["text"].split("\n")]
        for i, s in enumerate(lines):
            words = s.split()
            if not (2 <= len(words) <= 8) or s.endswith((".", ",", ";", ":")) or NOISE.search(s):
                continue
            if not re.match(r"^[A-Z][A-Za-z0-9 ,&\-–'’()/]+$", s):
                continue
            longw = [w for w in words if len(re.sub(r"\W", "", w)) >= 4]
            if len(longw) < 2 or not any(len(w) >= 6 for w in longw):
                continue  # drug-structure labels, axis labels, broken OCR
            if not (s.isupper() or all(w[0].isupper() or w.lower() in {"and", "of", "the", "in", "for", "to", "&", "with", "by", "on"} for w in words)):
                continue
            if re.search(r"[A-Z]{2,}\d|\d[A-Z]|[a-z]\d|\*", s) or len({w.lower() for w in words}) < len(words):
                continue  # chemical formulas, gene codes, repeated table cells
            # an ALL-CAPS heading that wraps onto the next line is one heading
            j = i + 1
            if s.isupper() and j < len(lines) and lines[j].isupper() and len(lines[j].split()) <= 6:
                s, j = s + " " + lines[j], j + 1
            while j < len(lines) and not lines[j]:
                j += 1
            nxt = lines[j] if j < len(lines) else ""
            if len(nxt) < 35 or nxt.count(" ") < 5:
                continue  # a real heading is followed by a paragraph, not by more short labels (table rows, figure text)
            key = s.lower()
            if key in seen:
                continue
            seen.add(key)
            out.append({"page": p["page"], "heading": s})
    return out


def uncovered(textbook, content_text, skips=()):
    have = toks(content_text)
    skipped = {s["heading"].lower(): s["reason"] for s in skips}
    miss, skip = [], []
    for h in headings(textbook):
        t = toks(h["heading"])
        if not t:
            continue
        if h["heading"].lower() in skipped:
            skip.append({**h, "reason": skipped[h["heading"].lower()]})
        elif len(t & have) / len(t) < 0.5:
            miss.append(h)
    return miss, skip
