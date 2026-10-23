"""Build a practice-exam app from a question bank, with anti-guessing checks.

  python3 build_exam.py U1     -> docs/exams/unit1/index.html + outputs/exams/U1_exam_audit.md

Steps: validate → interleave topics → assign answer letters under constraints → audit → app.
Letter rules: equal A–E overall, balanced within every topic and every 50-question block, and no
3-in-a-row, ascending/descending runs (ABCD), alternating pairs (ABAB), or repeating cycles (ABCABC).
"""
import html
import json
import random
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LETTERS = "ABCDE"
EXAMS = {"U1": {"slug": "unit1", "title": "Unit 1 Practice Exam — Introduction to Pharmacology",
                "short": "Unit 1 Practice Exam", "lectures": ["L01", "L02"], "seed": 625, "unit": 1,
                "about": "Built only from the Unit 1 slides and study guide."},
         "U1B": {"slug": "unit1b", "title": "Unit 1 Practice Exam B — Exam Conditions",
                 "short": "Unit 1 Practice Exam B (50 Q · 60 min)", "lectures": ["L01", "L02"], "seed": 1030, "unit": 1, "minutes": 60,
                 "about": "50 new questions at real exam length — slides, study guide, and the assigned Katzung chapters (textbook questions are cited by page). Best taken timed: 60 minutes."}}


def load_bank(exam_id):
    """Every BANK_* list from work/exams/<id>/bank*.py, in file order (loaded under unique names so exams don't collide)."""
    import importlib.util
    d = ROOT / "work" / "exams" / exam_id
    sys.path.insert(0, str(d))
    bank = []
    for f in sorted(d.glob("bank*.py")):
        spec = importlib.util.spec_from_file_location(f"{exam_id}_{f.stem}", f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        bank += [q for name in sorted(vars(mod)) if name.startswith("BANK_") for q in getattr(mod, name)]
    sys.path.remove(str(d))
    for i, q in enumerate(bank, 1):
        q["id"] = f"{exam_id}-{i:03d}"
    return bank


def validate(bank):
    errs = []
    for q in bank:
        opts = [q["correct"]] + [d["text"] for d in q["distractors"]]
        if len(q["distractors"]) != 4:
            errs.append(f"{q['id']}: needs 4 distractors")
        if len({o.strip().lower() for o in opts}) != 5:
            errs.append(f"{q['id']}: duplicate options")
        for k in ("why_correct", "takeaway", "discriminator", "src"):
            if not q.get(k):
                errs.append(f"{q['id']}: missing {k}")
        if any(not d["why"] for d in q["distractors"]):
            errs.append(f"{q['id']}: distractor without explanation")
    return errs


# ---------------------------------------------------------------- order + letters
def interleave(bank, rng):
    """Order questions so the same topic never appears twice in a row (topics spread evenly)."""
    for _ in range(2000):
        pools = defaultdict(list)
        for q in bank:
            pools[q["topic"]].append(q)
        for p in pools.values():
            rng.shuffle(p)
        order, last = [], None
        while any(pools.values()):
            # pick among the topics with the most remaining (keeps spread even), never repeating the last
            choices = [t for t, p in pools.items() if p and t != last]
            if not choices:
                break
            most = max(len(pools[t]) for t in choices)
            t = rng.choice([t for t in choices if len(pools[t]) >= most - 1])
            order.append(pools[t].pop())
            last = t
        if len(order) == len(bank):
            return order
    raise RuntimeError("could not interleave topics")


def pattern_problems(seq):
    """List the forbidden patterns found in a letter sequence."""
    probs = []
    idx = [LETTERS.index(c) for c in seq]
    for i in range(len(seq)):
        if i >= 2 and seq[i] == seq[i - 1] == seq[i - 2]:
            probs.append(f"3 identical at {i - 1}")
        if i >= 3:
            w = idx[i - 3:i + 1]
            diffs = {w[k + 1] - w[k] for k in range(3)}
            if diffs in ({1}, {-1}):
                probs.append(f"run {seq[i - 3:i + 1]} at {i - 2}")
            if seq[i] == seq[i - 2] and seq[i - 1] == seq[i - 3] and seq[i] != seq[i - 1]:
                probs.append(f"alternating {seq[i - 3:i + 1]} at {i - 2}")
        if i >= 5:
            w = seq[i - 5:i + 1]
            if w[:3] == w[3:] and len(set(w[:3])) == 3:
                probs.append(f"cycle {w} at {i - 4}")
    return probs


def score(seq, topics, blocks):
    s = 3 * len(pattern_problems(seq))
    for b in blocks:
        c = Counter(seq[i] for i in b)
        want = len(b) / 5
        s += sum(abs(c[L] - want) for L in LETTERS)
    return s


def assign_letters(order, rng):
    """Balanced letter bags per topic, then local search (swaps within a topic) to clear every rule."""
    n = len(order)
    topics = defaultdict(list)
    for i, q in enumerate(order):
        topics[q["topic"]].append(i)
    blocks = [list(range(k, min(k + 50, n))) for k in range(0, n, 50)]
    for attempt in range(200):
        # extras: the remainder letters each topic needs, chosen so overall counts are equal
        need = Counter({L: n // 5 for L in LETTERS})
        bags = {}
        extras_left = Counter()
        for t, pos in topics.items():
            bags[t] = [L for L in LETTERS for _ in range(len(pos) // 5)]
            need.subtract(Counter(bags[t]))
        ok = True
        for t, pos in sorted(topics.items(), key=lambda kv: -(len(kv[1]) % 5)):
            k = len(pos) % 5
            cands = sorted(LETTERS, key=lambda L: (-need[L], rng.random()))[:k]
            if len(cands) < k or any(need[L] <= 0 for L in cands):
                ok = False
                break
            bags[t] += cands
            need.subtract(Counter(cands))
        if not ok or any(v != 0 for v in need.values()):
            continue
        seq = [""] * n
        for t, pos in topics.items():
            bag = bags[t][:]
            rng.shuffle(bag)
            for i, L in zip(pos, bag):
                seq[i] = L
        cur = score("".join(seq), topics, blocks)
        for _ in range(60000):
            if cur == 0:
                return "".join(seq)
            t = rng.choice(list(topics))
            i, j = rng.sample(topics[t], 2)
            if seq[i] == seq[j]:
                continue
            seq[i], seq[j] = seq[j], seq[i]
            new = score("".join(seq), topics, blocks)
            if new <= cur or rng.random() < 0.002:
                cur = new
            else:
                seq[i], seq[j] = seq[j], seq[i]
    raise RuntimeError("could not satisfy letter constraints")


def place_options(q, letter, rng):
    ds = q["distractors"][:]
    rng.shuffle(ds)
    others = [L for L in LETTERS if L != letter]
    opts = {letter: {"text": q["correct"], "why": q["why_correct"], "correct": True}}
    for L, d in zip(others, ds):
        opts[L] = {"text": d["text"], "why": d["why"], "correct": False}
    return {L: opts[L] for L in LETTERS}


def length_rank(q):
    """1 = shortest ... 5 = longest (by words, then characters)."""
    items = sorted(q["options"].items(), key=lambda kv: (len(kv[1]["text"].split()), len(kv[1]["text"])))
    return [L for L, _ in items].index(q["answer"]) + 1


# ---------------------------------------------------------------- source checks
DRUG_SUFFIX = re.compile(r"\b[a-z]+(?:ol|ine|in|ide|pril|sartan|statin|mab|cillin|cycline|azole|prazole|olol|pam|lam|mycin|one|ate|ase)\b", re.I)


def source_text(lectures):
    parts = []
    for lid in lectures:
        for s in json.loads((ROOT / "work" / lid / "slides.json").read_text()):
            parts += [it["text"] for it in s["items"]] + [s.get("notes", "")] + [" ".join(map(str, r)) for t in s["tables"] for r in t]
    for lid in lectures:
        tb = ROOT / "work" / lid / "textbook.json"
        if tb.exists():
            parts += [p["text"] for p in json.loads(tb.read_text())]
    sg = ROOT / "work" / "study_guide.json"
    if sg.exists():
        parts += [v["question"] + " " + v["answer"] for v in json.loads(sg.read_text()).values()]
    return " ".join(parts).lower()


NAMED_DRUGS = ["acetaminophen", "tylenol", "albuterol", "warfarin", "lithium", "digoxin", "phenytoin", "nitroglycerin",
               "propranolol", "morphine", "insulin", "heparin", "codeine", "clopidogrel", "azathioprine", "allopurinol",
               "aspirin", "napqi", "thiopurine", "antiarrhythmic", "antidepressant", "opioid", "antibiotic"]


def drug_audit(bank, src):
    tested = Counter()
    unverified = []
    for q in bank:
        blob = " ".join([q["stem"], q["correct"]] + [d["text"] for d in q["distractors"]]).lower()
        for d in NAMED_DRUGS:
            if d in blob:
                tested[d] += 1
        for w in DRUG_SUFFIX.findall(blob):
            if w.lower() not in src and len(w) > 6:
                unverified.append((q["id"], w))
    return tested, {d: d in src for d in tested}, unverified


def as_quiz(q):
    """The shared focus-quiz format (assets/quizmode.js)."""
    return {"id": q["id"], "stem": q["stem"], "options": {L: o["text"] for L, o in q["options"].items()}, "answer": q["answer"],
            "why": q["options"][q["answer"]]["why"], "whys": {L: o["why"] for L, o in q["options"].items() if not o["correct"]},
            "takeaway": q["takeaway"], "discriminator": q["discriminator"], "src": q["src"], "topic": q["topic"], "kind": q["kind"],
            "link": q.get("link")}


def study_link(src, lectures):
    """'L02 S19; S30; SG U1-R11' -> link to the study-guide part that covers those slides."""
    sys.path.insert(0, str(ROOT / "pipeline"))
    from build_site import part_finder
    m = re.match(r"\s*(L\d+)\s*(.*)", src)
    lid, rest = (m.group(1), m.group(2)) if m else (lectures[0], src)
    resolved = ROOT / "work" / lid / "content.resolved.json"
    if not resolved.exists():
        return None
    part = part_finder(json.loads(resolved.read_text()))(rest)
    return {"href": f"../../{lid}/index.html" + (f"#{part[1]}" if part else ""),
            "label": f"Study this: {lid}" + (f" · Part {part[0]} →" if part else " →")}


# ---------------------------------------------------------------- app
# The exam app lives in site_src/assets/exam.js (one shared copy); each page only embeds its questions as JSON.





def app_html(meta, data):
    sys.path.insert(0, str(ROOT / "pipeline"))
    from build_site import nav_html, SECURITY_META
    up = "../../"
    body = f"""<header class="hero wrap narrow" style="padding-bottom:0"><p class="eyebrow">Practice exam · {len(data['questions'])} questions</p>
<h1 style="font-size:clamp(30px,5vw,44px)">{html.escape(meta['title'])}</h1>
<p class="lede">One question at a time. Tap an answer to see why every option is right or wrong. {html.escape(meta['about'])}</p></header>
<section class="wrap narrow">
  <div class="callout why noprint" style="margin-top:18px"><div class="label">Best way to practice</div>Full screen, one question at a time — study mode or <strong>timed at PANCE pace</strong> (1 min/question), with a debrief at the end. Works with a Bluetooth remote ring.
    <div style="margin-top:12px"><button class="btn" id="focus">Start focus session →</button></div></div>
  <div class="exam-top"><select id="mode" aria-label="Filter"></select><span id="score" class="muted"></span></div>
  <div class="track"><div id="bar"></div></div><div class="small muted" id="progress"></div>
  <div class="card" id="card" style="margin-top:16px"></div>
  <div class="navrow"><button class="btn ghost" id="prev">← Prev</button><span class="small muted" id="counter" style="align-self:center"></span><button class="btn" id="next">Next →</button></div>
  <div class="btns" style="margin-top:0"><button class="btn ghost" id="flag">Flag (F)</button><button class="btn ghost" id="shuffle">Shuffle order</button><button class="btn ghost" id="reset">Reset progress</button></div>
  <p class="kbd" style="margin-top:14px">Keys: <kbd>A</kbd>–<kbd>E</kbd> or <kbd>1</kbd>–<kbd>5</kbd> answer · <kbd>←</kbd> <kbd>→</kbd> move · <kbd>F</kbd> flag</p>
</section>
<section class="section" style="margin-top:30px"><div class="wrap narrow">
  <h2 style="font-size:30px">Scorecard</h2><p id="studynext" class="muted"></p>
  <div class="table-wrap"><table><thead><tr><th>Topic</th><th>Done</th><th>Score</th><th>Misses</th></tr></thead><tbody id="scorecard"></tbody></table></div>
  <h3 style="margin-top:28px">Wrong-answer log</h3><p class="small muted" id="logcount"></p><ul id="log"></ul>
</div></section>
<script type="application/json" id="exam-data">{json.dumps(data, ensure_ascii=False).replace("</", "<\\/")}</script>
<script src="{up}assets/exam.js"></script>"""
    return f"""<!doctype html>
<html lang="en" data-root="{up}" data-sk="global"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">{SECURITY_META}
<title>{html.escape(meta['short'])}</title><link rel="stylesheet" href="{up}assets/site.css"><link rel="icon" type="image/svg+xml" href="{up}assets/logo-mark.svg"><script>(function(d){{d.classList.add("js");try{{var t=JSON.parse(localStorage.getItem("theme")||'"auto"');if(t!=="auto")d.setAttribute("data-theme",t);var p=JSON.parse(localStorage.getItem("prefs")||"{{}}");for(var k in p)d.setAttribute("data-p"+k,p[k])}}catch(e){{}}}})(document.documentElement)</script></head>
<body>{nav_html(up, "practice")}
{body}
<footer class="wrap narrow">Progress and your wrong-answer log are saved in this browser.</footer>
<script src="{up}assets/site.js"></script><script src="{up}assets/quizmode.js"></script><script type="module" src="{up}assets/sidekick.js"></script></body></html>"""


# ---------------------------------------------------------------- main
def main(exam_id):
    meta = EXAMS[exam_id]
    rng = random.Random(meta["seed"])
    bank = load_bank(exam_id)
    errs = validate(bank)
    if errs:
        raise SystemExit("bank problems:\n  " + "\n  ".join(errs))
    order = interleave(bank, rng)
    letters = assign_letters(order, rng)
    for q, L in zip(order, letters):
        q["answer"] = L
        q["options"] = place_options(q, L, rng)
    topics = list(dict.fromkeys(q["topic"] for q in bank))

    # ---- audit
    lines = [f"# {meta['title']} — build audit\n", f"**{len(order)} questions** · built from {', '.join(meta['lectures'])} + course study guide\n"]
    kinds = Counter(q["kind"] for q in order)
    lines.append(f"## Blueprint\n- Patient cases: {kinds['vignette']} · Direct recall: {kinds['mechanism']}")
    lines.append(f"- Questions testing study-guide items: {sum(1 for q in order if q['sg'])} (target ~50)")
    lines.append("\n| Topic | Questions | Letters (A B C D E) |\n|---|---|---|")
    for t in topics:
        c = Counter(q["answer"] for q in order if q["topic"] == t)
        lines.append(f"| {t} | {sum(c.values())} | {' '.join(str(c[L]) for L in LETTERS)} |")
    io = Counter(o for q in order for o in q["objectives"])
    lines.append("\n**By syllabus objective:** " + " · ".join(f"{k}: {io[k]}" for k in sorted(io)))
    sgc = Counter(s for q in order for s in q["sg"])
    lines.append("\n**Study-guide items tested:** " + " · ".join(f"{k}: {sgc[k]}" for k in sorted(sgc)))
    c = Counter(letters)
    lines.append(f"\n## Answer-letter audit\n- Overall: " + " · ".join(f"{L} {c[L]}" for L in LETTERS))
    for b in range(0, len(order), 50):
        cb = Counter(letters[b:b + 50])
        lines.append(f"- Questions {b + 1}–{min(b + 50, len(order))}: " + " · ".join(f"{L} {cb[L]}" for L in LETTERS))
    pp = pattern_problems(letters)
    lines.append(f"- Pattern check (3-in-a-row, ABCD/EDCB runs, ABAB, ABCABC cycles): {'none ✅' if not pp else ', '.join(pp)}")
    lines.append(f"- Sequence: `{letters}`")
    ranks = Counter(length_rank(q) for q in order)
    spreads = Counter(max(len(o["text"].split()) for o in q["options"].values()) - min(len(o["text"].split()) for o in q["options"].values()) for q in order)
    lines.append("\n## Option-length audit (can length give the answer away?)")
    lines.append("- Correct answer's length rank among its 5 options (1 = shortest, 5 = longest): " + " · ".join(f"rank {r}: {ranks[r]}" for r in range(1, 6)))
    lines.append("- Word-count spread within a question (longest − shortest option): " + " · ".join(f"{k} words: {spreads[k]}" for k in sorted(spreads)))
    runs, mx, cur = [], 1, 1
    for a, b in zip(order, order[1:]):
        cur = cur + 1 if a["topic"] == b["topic"] else 1
        mx = max(mx, cur)
    lines.append(f"\n## Interleaving\n- Longest run of same-topic questions back to back: {mx}")
    src = source_text(meta["lectures"])
    tested, verified, unver = drug_audit(order, src)
    lines.append("\n## Drugs tested (each checked against the sources)")
    lines += [f"- {d}: {n} question(s) — {'found in sources ✅' if verified[d] else 'NOT FOUND ❌'}" for d, n in sorted(tested.items())]
    lines.append("- Other drug-like words not found in sources: " + (", ".join(f"{w} ({i})" for i, w in unver) if unver else "none ✅"))
    lines.append("\n## Answer integrity\n- Every question: exactly 5 distinct options, one keyed answer, an explanation for each option, a takeaway, a discriminator, and a source ✅")
    out = ROOT / "outputs" / "exams"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{exam_id}_exam_audit.md").write_text("\n".join(lines) + "\n")

    # ---- app
    for q in order:
        q["link"] = study_link(q["src"], meta["lectures"])
    data = {"slug": meta["slug"], "title": meta["short"], "topics": topics, "minutes": meta.get("minutes"),
            "questions": [{k: q[k] for k in ("id", "topic", "kind", "stem", "options", "answer", "takeaway", "discriminator", "src", "link")} for q in order]}
    d = ROOT / "docs" / "exams" / meta["slug"]
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(app_html(meta, data))
    (d / "questions.json").write_text(json.dumps([{"id": q["id"], "stem": q["stem"], "src": q["src"]} for q in order], ensure_ascii=False))
    (d / "meta.json").write_text(json.dumps({"id": meta["slug"], "title": meta["short"], "count": len(order), "unit": meta.get("unit"), "minutes": meta.get("minutes")}))
    (d / "quiz.json").write_text(json.dumps([as_quiz(q) for q in order], ensure_ascii=False))
    (ROOT / "work" / "exams" / exam_id / "resolved.json").write_text(json.dumps(order, indent=1, ensure_ascii=False))
    print(f"  exam {exam_id}: {len(order)} questions -> docs/exams/{meta['slug']}/ ; audit -> outputs/exams/{exam_id}_exam_audit.md")
    print(f"  letters {dict(c)} | length ranks {dict(sorted(ranks.items()))} | patterns {len(pp)} | max same-topic run {mx}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "U1")
