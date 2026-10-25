"""Assigned-reading coverage: every section heading in the lecture's textbook pages must be taught somewhere in the guide
(or skipped on purpose with a reason in content.json "reading_skip"). The syllabus makes assigned reading testable."""
import re

from audit import toks

NOISE = re.compile(r"^Term Definition$|Approach and Goals|Adverse Effect$|Katzung|Vanderah|PhD|\bMD\b|Figure|FIGURE|TABLE|Table|CHAPTER|SECTION|Basic Principles|"
                   r"Case Study|CASE STUDY|REFERENCES|SUMMARY|PREPARATIONS|\bGeneric\b|Neutra-")


def headings(textbook):
    """Section headings from the extracted page text: short title-like lines (OCR fragments and labels filtered out)."""
    out, seen = [], set()
    for p in textbook:
        raw = p["text"].split("\n")
        lines = [re.sub(r"^[■•▪]\s*", "", l.strip()) for l in raw]
        # rejoin a capitals heading that wraps over several lines ("OF PHARMACOKINETICS &" / "PHARMACODYNAMICS TO DOSE" /
        # "INDIVIDUALIZATION"): a wrapped line ends in a space or a joining word, and the next line is capitals too
        for j in range(len(lines) - 1):
            if lines[j].isupper() and lines[j + 1].isupper() and (raw[j].endswith(" ") or re.search(r"(&|\b(AND|OF|TO|THE|FOR|IN))$", lines[j])):
                lines[j], lines[j + 1] = "", lines[j] + " " + lines[j + 1]
        for i, s in enumerate(lines):
            words = s.split()
            if s.endswith((".", ",", ";", ":")) or NOISE.search(s) or s.count("(") != s.count(")"):
                continue  # sentences, labels, and fragments of a wrapped heading
            if len(words) == 1:
                # a one-word ALL-CAPS heading is usually a drug section (COLCHICINE, ALLOPURINOL): keep it if prose follows
                if not (s.isupper() and len(s) >= 5 and s.isalpha()):
                    continue
                nxt = next((l for l in lines[i + 1:] if l), "")
                if len(nxt) >= 35 and nxt.count(" ") >= 5 and s.lower() not in seen:
                    seen.add(s.lower()); out.append({"page": p["page"], "heading": s})
                continue
            if not (2 <= len(words) <= 8):
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
    # drop a heading that is only the tail of a longer heading on the same page (a wrapped line seen twice)
    return [h for h in out if not any(o is not h and o["page"] == h["page"] and len(o["heading"]) > len(h["heading"])
                                      and o["heading"].lower().endswith(h["heading"].lower()) for o in out)]


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
