"""Cut a lecture's assigned reading out of the full textbook PDF.

Uses the syllabus readings for that lecture:
  {"chapter": "12", "pages": "233-260"}  -> printed page numbers (preferred)
  {"chapter": "12"}                      -> finds the chapter in the PDF's bookmarks
Writes work/<LEC>/textbook.json + textbook.md, citing PRINTED page numbers.
"""
import json
import re
import sys
from pathlib import Path

from pypdf import PdfReader


def page_labels(reader):
    try:
        labels = reader.page_labels
        if labels and len(labels) == len(reader.pages):
            return list(labels)
    except Exception:
        pass
    return [str(i + 1) for i in range(len(reader.pages))]


def label_range(labels, pages):
    a, _, b = pages.partition("-")
    b = b or a
    try:
        return labels.index(a.strip()), labels.index(b.strip())
    except ValueError:
        raise SystemExit(f"  ! page '{pages}' not found in the PDF's page numbers")


def chapter_range(reader, chapter):
    """Find chapter start/end from bookmarks: the entry mentioning 'Chapter N' or starting with 'N'."""
    flat = []

    def walk(items):
        for it in items:
            if isinstance(it, list):
                walk(it)
            else:
                try:
                    flat.append((it.title.strip(), reader.get_destination_page_number(it)))
                except Exception:
                    pass
    walk(reader.outline)
    pat = re.compile(rf"^(chapter\s+)?{re.escape(str(chapter))}\b", re.I)
    for i, (title, start) in enumerate(flat):
        if pat.search(title):
            later = [p for _, p in flat[i + 1:] if p > start]
            end = (min(later) - 1) if later else len(reader.pages) - 1
            return start, end
    raise SystemExit(f"  ! chapter {chapter} not found in the PDF bookmarks — add page numbers to the syllabus reading instead")


def clean(text):
    text = re.sub(r"-\n(\w)", r"\1", text)  # re-join hyphenated words
    return re.sub(r"[ \t]+", " ", text).strip()


def main(pdf_path, readings_json, out_dir):
    readings = json.loads(readings_json)
    reader = PdfReader(pdf_path)
    labels = page_labels(reader)
    pages = []
    for rd in readings:
        a, b = label_range(labels, rd["pages"]) if rd.get("pages") else chapter_range(reader, rd["chapter"])
        for idx in range(a, b + 1):
            pages.append({"page": labels[idx], "chapter": rd.get("chapter", ""),
                          "text": clean(reader.pages[idx].extract_text() or "")})
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "textbook.json").write_text(json.dumps(pages, indent=1, ensure_ascii=False))
    md = ["# Assigned textbook pages\n"] + [f"\n## p. {p['page']} (Ch. {p['chapter']})\n\n{p['text']}" for p in pages]
    (out_dir / "textbook.md").write_text("\n".join(md) + "\n")
    print(f"  extracted {len(pages)} textbook pages")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
