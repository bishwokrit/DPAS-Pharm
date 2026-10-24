"""One command for everything. See README.md.

  ./run.sh status        what's ready, what's missing
  ./run.sh setup         make a folder per lecture from the syllabus
  ./run.sh new L03       a new lecture, start to finish: extract → author brief (or, once authored: deck, audit,
                         standard checks, practice exam, website, site checks) → one PASS/FAIL report
  ./run.sh L01           build one lecture
  ./run.sh all           build every lecture that has its slides + content, then the website
  ./run.sh site          rebuild the website (study guides, PDFs, home page) into docs/
  ./run.sh exam U1       rebuild a practice exam (bank in work/exams/U1/)
  ./run.sh check         test the built site before publishing (pages, links, answer balance, textbook facts)
"""
import json
import re
import subprocess
import sys
from pathlib import Path

import audit
import content as C
import extract
import notebooklm

ROOT = Path(__file__).resolve().parent.parent
CFG = json.loads((ROOT / "config.json").read_text())
SYLLABUS = ROOT / "work" / "syllabus.json"


def syllabus():
    if not SYLLABUS.exists():
        sys.exit("No syllabus yet. Put your syllabus in inputs/syllabus/ and ask Claude: \"read my syllabus\".")
    return json.loads(SYLLABUS.read_text())


def lecture(lid):
    for lec in syllabus()["lectures"]:
        if lec["id"].lower() == lid.lower():
            return lec
    sys.exit(f"{lid} is not in the syllabus. Run ./run.sh status to see lecture IDs.")


def slides_file(lid):
    files = sorted((ROOT / "inputs" / "lectures" / lid).glob("*.pptx"))
    files = [f for f in files if not f.name.startswith("~$")]
    if len(files) > 1:
        sys.exit(f"{lid}: more than one .pptx in inputs/lectures/{lid}/ — keep only the lecture's slides there.")
    return files[0] if files else None


def textbook_pdf():
    """The textbook lives outside this public repo (config textbook_dir, a private repo); inputs/textbook is a fallback."""
    for d in [ROOT / CFG.get("textbook_dir", ""), ROOT / "inputs" / "textbook"]:
        pdfs = sorted(d.resolve().glob("*.pdf")) if CFG.get("textbook_dir") or d.name == "textbook" else []
        if pdfs:
            return pdfs[0]
    return None


def slug(text):
    return re.sub(r"[^A-Za-z0-9]+", "_", text).strip("_")[:50]


def build(lid):
    lec = lecture(lid)
    lid = lec["id"]
    work, out = ROOT / "work" / lid, ROOT / "outputs" / lid
    work.mkdir(parents=True, exist_ok=True)
    print(f"\n== {lid}: {lec['title']} ==")

    pptx = slides_file(lid)
    if not pptx:
        print(f"  waiting for slides: put the .pptx in inputs/lectures/{lid}/")
        return "no slides"
    sj = work / "slides.json"
    if not sj.exists() or sj.stat().st_mtime < pptx.stat().st_mtime:
        extract.main(pptx, work)

    pdf = textbook_pdf()
    if pdf and lec.get("readings"):
        tj = work / "textbook.json"
        if not tj.exists() or tj.stat().st_mtime < pdf.stat().st_mtime:
            subprocess.run([sys.executable, str(ROOT / "pipeline" / "textbook.py"), str(pdf), json.dumps(lec["readings"]), str(work)], check=True)

    guide_docx = sorted((ROOT / "inputs" / "study_guide").glob("*.docx"))
    sg = ROOT / "work" / "study_guide.json"
    if guide_docx and (not sg.exists() or sg.stat().st_mtime < guide_docx[0].stat().st_mtime):
        import study_guide
        study_guide.main(guide_docx[0], ROOT / "work")

    cj = work / "content.json"
    if not cj.exists():
        import brief
        b = brief.main(lec, work)
        print(f"  slides extracted; checklist written to {b.relative_to(ROOT)}.\n  Next step: ask Claude \"author {lid}\".")
        return "needs authoring"
    c = C.load(cj)
    if (work / "textbook.json").exists() and c.get("textbook_status") != "included":
        print(f"  ! textbook pages are now available — ask Claude \"add textbook to {lid}\" to fold them in.")
    errs = C.validate(c)
    if errs:
        print("  content.json problems:\n   - " + "\n   - ".join(errs))
        return "content errors"
    C.resolve(c)
    (work / "content.resolved.json").write_text(json.dumps(c, indent=1, ensure_ascii=False))

    out.mkdir(parents=True, exist_ok=True)
    deck = out / f"{lid}_{slug(lec['title'])}_study_deck.pptx"
    import measure
    measure.main(work / "content.resolved.json", work / "char_widths.json")
    subprocess.run(["node", str(ROOT / "pipeline" / "build_deck.js"), str(work / "content.resolved.json"), str(deck), CFG.get("theme", "light")], check=True)
    nlm = out / "notebooklm"
    notebooklm.main(work / "content.resolved.json", nlm, CFG["notebooklm_max_words_per_source"])
    code = audit.main(lid, work, out, deck, nlm, CFG["audit_match_threshold"], lec.get("study_guide", []))
    return "built ✅" if code == 0 else "built — audit found gaps"


def new(lid):
    """Everything for one lecture, with every quality gate, ending in a plain PASS/FAIL report card."""
    lec = lecture(lid)
    lid = lec["id"]
    gates = {}
    r = build(lid)
    if r in ("no slides", "needs authoring", "content errors"):
        return r
    gates["Every slide and assigned-reading section taught (audit)"] = r == "built ✅"
    import standards
    bad = standards.check(lec)
    for b in bad:
        print("  ✗ " + b)
    gates["Lecture standard (teaser, drugs, figures, textbook)"] = not bad
    import build_exam
    for eid, meta in build_exam.EXAMS.items():
        if lid in meta["lectures"] and (ROOT / "work" / "exams" / eid).exists():
            build_exam.main(eid)
    import build_site
    build_site.main()
    gates["Website checks (pages, links, a11y, phone, data)"] = subprocess.run([sys.executable, str(ROOT / "pipeline" / "check.py")]).returncode == 0
    print(f"\n{lid} report card")
    for k, ok in gates.items():
        print(f"  {'PASS' if ok else 'FAIL'}  {k}")
    if r != "built ✅":
        print(f"  → open outputs/{lid}/{lid}_audit.md for what is missing")
    ok = all(gates.values())
    print(f"\n{'Ready to publish.' if ok else 'Not ready — fix the FAIL lines, then run ./run.sh new ' + lid + ' again.'}")
    return "ready ✅" if ok else "gaps"


def status():
    syl = syllabus()
    pdf = textbook_pdf()
    print(f"Textbook PDF: {pdf.name if pdf else 'not added yet (decks use slides only)'}   Theme: {CFG.get('theme')}\n")
    print(f"{'ID':6} {'Date':11} {'Slides':7} {'Content':8} {'Audit':6} Title")
    for lec in syl["lectures"]:
        lid = lec["id"]
        work = ROOT / "work" / lid
        a = work / "audit.json"
        audit_s = ("pass" if json.loads(a.read_text())["passed"] else "gaps") if a.exists() else "-"
        print(f"{lid:6} {lec.get('date', ''):11} {'yes' if slides_file(lid) else '-':7} {'yes' if (work / 'content.json').exists() else '-':8} {audit_s:6} {lec['title']}")


LOCK = ROOT / "inputs" / "ORIGINALS.sha256"


def originals():
    """The files the professor gave (lectures, study guide, syllabus) are read-only sources.
    Their fingerprints are recorded once; every run checks nothing has changed them."""
    import hashlib
    files = sorted(p for p in (ROOT / "inputs").rglob("*") if p.is_file() and p != LOCK and not p.name.startswith("."))
    return {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in files}


def check_originals():
    now = originals()
    known = dict(l.split("  ", 1)[::-1] for l in LOCK.read_text().splitlines() if l.strip()) if LOCK.exists() else {}
    changed = [f for f in known if f in now and now[f] != known[f]] + [f for f in known if f not in now]
    if changed:
        sys.exit("STOP: these original course files were changed or removed:\n  " + "\n  ".join(changed) +
                 "\nRestore them from the original upload before building.")
    new = [f for f in now if f not in known]
    if new:  # a newly added lecture/syllabus gets fingerprinted the first time it is seen
        LOCK.write_text("".join(f"{h}  {f}\n" for f, h in sorted({**known, **{f: now[f] for f in new}}.items())))
        print("Recorded fingerprints for new originals:", ", ".join(new))


def setup():
    for lec in syllabus()["lectures"]:
        (ROOT / "inputs" / "lectures" / lec["id"]).mkdir(parents=True, exist_ok=True)
    print("Made a folder for each lecture in inputs/lectures/.")


if __name__ == "__main__":
    arg = (sys.argv[1] if len(sys.argv) > 1 else "status").strip()
    check_originals()
    if arg == "status":
        status()
    elif arg == "setup":
        setup()
    elif arg == "all":
        results = {lec["id"]: build(lec["id"]) for lec in syllabus()["lectures"]}
        print("\nSummary:")
        for k, v in results.items():
            print(f"  {k}: {v}")
        import build_site
        build_site.main()
    elif arg == "new":
        if len(sys.argv) < 3:
            sys.exit("Which lecture? e.g. ./run.sh new L03")
        sys.exit(0 if new(sys.argv[2]) == "ready ✅" else 1)
    elif arg == "check":
        import check
        check.main()
    elif arg == "site":
        import build_site
        build_site.main()
    elif arg == "exam":
        import build_exam
        build_exam.main(sys.argv[2] if len(sys.argv) > 2 else "U1")
        import build_site
        build_site.main(pdf=False)
    else:
        build(arg)
