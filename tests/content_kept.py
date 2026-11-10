"""Nothing lost: every fact the authors wrote for a lecture must appear, word for word, on that lecture's built page.
The page layout can be reorganised freely; this check fails the moment a fact, table cell, flow step or callout goes missing."""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "pipeline"))
from build_site import md  # noqa: E402  (the same text-to-HTML step the page uses)


def texts(cl):
    for facts in cl.get("sections", {}).values():
        for f in facts:
            yield f["text"]
    for f in cl.get("high_yield", []):
        yield f["text"]
    for h in cl.get("hooks", []):
        yield h["text"]
    for fl in cl.get("flows", []):
        yield fl["title"]
        yield from fl["steps"]
    for t in cl.get("comparisons", []):
        yield t["title"]
        yield from t["columns"]
        for r in t["rows"]:
            yield from r
    for fig in cl.get("figures", []):
        yield fig["caption"]
    for cf in cl.get("conflicts", []):
        yield cf["topic"]
        yield cf["slides"]["text"]
        yield cf["textbook"]["text"]


def main():
    total, missing = 0, []
    for f in sorted((ROOT / "work").glob("L*/content.json")):
        L = f.parent.name
        page = ROOT / "docs" / L / "index.html"
        if not page.exists():
            continue
        h = page.read_text()
        for cl in json.loads(f.read_text())["classes"]:
            for t in texts(cl):
                total += 1
                if md(str(t)) not in h:
                    missing.append(f"{L} · {cl['name']}: {str(t)[:90]}")
    for m in missing[:25]:
        print(f"  ✗ missing from the page — {m}")
    print(f"  content: {total} facts, table cells, steps and captions checked, {len(missing)} missing from their page")
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main())
