"""./run.sh check — run before every update. Fails loudly if something is wrong:
  1. every page loads with no JavaScript errors, missing files, or broken links/anchors (headless browser)
  2. practice-exam answer letters are balanced (no guessable pattern)
  3. every number in a textbook-cited fact appears on the page it cites (needs the private textbook PDF)
"""
import collections, glob, json, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
CFG = json.loads((ROOT / "config.json").read_text())


def answers():
    ok = True
    for f in sorted(DOCS.glob("exams/*/quiz.json")):
        qs = json.loads(f.read_text())
        c = collections.Counter(q["answer"] for q in qs)
        share = {L: c.get(L, 0) / len(qs) for L in "ABCDE"}
        flag = [L for L, v in share.items() if v < .12 or v > .28]
        print(f"  answers {f.parent.name}: " + " ".join(f"{L}{c.get(L, 0)}" for L in "ABCDE") + ("  ✗ unbalanced: " + ",".join(flag) if flag else "  ✓"))
        ok &= not flag
    return ok


def textbook():
    pdf = next(iter(glob.glob(str((ROOT / CFG.get("textbook_dir", "../dpas-textbook")).resolve() / "*.pdf"))), None)
    if not pdf:
        print("  textbook: skipped (private textbook PDF not on this machine)")
        return True
    off = json.loads((ROOT / "work" / "textbook_meta.json").read_text())["pdf_page_offset"]
    cache = {}
    def page(n):
        if n not in cache:
            cache[n] = subprocess.run(["pdftotext", "-f", str(n + off), "-l", str(n + off), "-layout", pdf, "-"], capture_output=True, text=True).stdout
        return cache[n]
    norm = lambda t: re.sub(r"\s+", " ", t.replace("–", "-").replace("−", "-")).lower()
    facts = []
    sys.path.insert(0, str(ROOT / "work"))
    import drugs
    facts += [(d["name"], f["text"], f["src"]) for d in drugs.DRUGS for f in d["facts"] if f["tb"]]
    for f in sorted((ROOT / "work").glob("L*/textbook_L*.py")):
        facts += [(f.parent.name, t, p) for t, p in re.findall(r'["\']([^"\']{25,400}?)["\'],\s*["\'](p\. ?\d+(?:[;,–-] ?p?\.? ?\d+)*)["\']', f.read_text())]
    bad = 0
    for who, txt, src in facts:
        hay = norm(" ".join(page(int(p)) + page(int(p) + 1) for p in re.findall(r"\d+", src)))
        nums = re.findall(r"\d+(?:\.\d+)?", re.sub(r"(CYP\w+|HLA-[\w*:]+|VKORC1|MDR1|NAT2|t½|\w+₅₀|[A-Z]{2,}\d\w*)", "", txt))
        miss = [n for n in nums if not re.search(r"(?<![\d.])" + re.escape(n) + r"(?!\d)", hay)]
        if miss:
            bad += 1
            print(f"  ✗ [{who}] {src}: {miss} not on the page — {txt[:90]}")
    print(f"  textbook: {len(facts)} cited facts checked, {bad} with numbers not found on the cited page")
    return not bad


def main():
    print("Checking the site…")
    ok = answers()
    ok &= textbook()
    ok &= subprocess.run(["node", str(ROOT / "tests" / "pages.mjs")]).returncode == 0
    print("All checks passed." if ok else "Some checks FAILED — fix before publishing.")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
