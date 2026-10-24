# Authoring guide (the rules for writing `work/<LEC>/content.json`)

This is the step an AI does: read the extracted lecture + textbook pages and write the
organized study content. Everything after this step (deck, NotebookLM pack, audit) is automatic.
Today Claude does this step in a chat session. Later it can be sent to the Claude or ChatGPT
API with this file as the instructions — the format is plain JSON on purpose.

**Update this file after pilot feedback** so every lecture is built the same way.

## Inputs to read
- `work/<LEC>/slides.md` — every slide's text, tables, speaker notes. `**bold**` = emphasized on the slide.
- `work/<LEC>/slide_images/` (if present) — check pictures/diagrams for text that extraction can't see.
- `work/<LEC>/textbook.md` — assigned pages (only once the textbook PDF is added).
- `work/syllabus.json` — this lecture's unit objectives (IOx.y) and its assigned study-guide items.
- `work/study_guide.md` — course study guide items (questions + answer key). Only the items listed
  for this lecture in `work/syllabus.json`. For Units 2–6, split each unit's items between its two sessions
  by topic when authoring, and update `study_guide` in `work/syllabus.json`.
- `work/<LEC>/figures/` — big pictures saved from the slides (e.g., `S23_1.png`).

## Source rules (strict)
1. Use ONLY the slides (incl. speaker notes), the assigned textbook pages, the syllabus, and the
   course study guide. No outside knowledge.
2. Mnemonics may be invented but must only encode facts already in the materials. Put them in
   `hooks` with `"kind": "mnemonic"` (the deck labels them "Mnemonic (memory aid)").
3. If a template section isn't covered, leave it as `[]`. The deck prints
   "Not covered in materials". Never fill gaps.
4. Slides vs textbook disagree → add to that class's `conflicts` (show both, both cited).
5. Every fact has `src`: `S12`, `S12-14`, `S12 (notes)`, `p. 245`, `SG U1-R3`, or combined `S12; p. 245`.
6. `"tb": true` on anything that is in the textbook but NOT on the slides.
   `"sg": true` on anything that is in the study guide but NOT on the slides.
7. Wrap anything the slides emphasize (bold/highlight/underlined body text — see `**` in slides.md) in
   `**double asterisks**`. Don't bold for decoration: bold must mean "the lecture emphasized this".

## Structure
- One entry in `classes` per drug class (or per topic), in lecture order. Each has a `"template"`:
  - `"drug_class"` (Units 2–6): `overview` (Class), `prototype` (Prototype + other drugs named), `moa`,
    `indications`, `adverse` (BOXED WARNINGS FIRST), `contra`, `interactions`, `pk`, `monitoring`,
    `pearls` (clinical pearls / "why" hook)
  - `"concept"` (principles lectures like Unit 1): `definitions, how, clinical, examples, traps`
    (Key definitions → How it works → Clinical relevance → Drugs named as examples → Exam traps)
- Every class/topic has all of its template's sections (use `[]` if not covered).
- `objectives` (top level): the syllabus unit objectives (`IO1.1`…, `"src": "Syllabus"`) PLUS the
  session objectives from the lecture's objectives slide (`SO1`…, `"src": "S2"`). Add `"thin_note"`
  when this session barely covers an objective (e.g., "taught in Session 2 (L02)").
- `about` (top level): readings, session scope, what continues next session, figure attribution.
- `figures`: `{image, title, caption, src}` for each saved figure — caption explains what the picture shows.
- Short facts: one idea per bullet, ~25 words max. Split long sentences. No walls of text.
- Include ALL content: every slide line, table row, speaker-note point, and assigned textbook fact
  must land somewhere. If it fits no section, put it in `overview`.

## Extras per class
- `comparisons`: tables focused on **discriminators** — the column "How to tell apart" is encouraged.
- `hooks`: `"why"` = mechanism-based explanation that appears in or follows directly from the
  materials (e.g., why a side effect follows from the mechanism); `"mnemonic"` = labeled memory aid.
- `high_yield`: 3–8 must-know facts (repeat of the most emphasized points, with citations).
- `questions`: ~50/50 `"vignette"` and `"mechanism"` across the lecture.
  - Rebuild EVERY lecture quick-check question as a 5-option question: keep its stem, options and
    "Why" explanation, add one more distractor, and set `"from_slides": "S8-9"`.
  - Then add new questions (mostly vignettes) until the mix is ~50/50.
  - PANCE-style, detail-heavy, single best answer.
  - Write `correct` + exactly 4 `distractors` (each with `why` it's wrong) + `why_correct`.
  - Do NOT pick letters — the pipeline shuffles and balances A–E automatically.
  - All 5 options similar in length, grammar, and specificity; the right one must not stand out.
  - Distractors must be plausible and drawn from the same lecture (other drugs, other mechanisms).

## NotebookLM extras
- `notebooklm.patient`: one patient (age, sex, situation) whose story can plausibly pass through every
  drug class in the lecture, using only conditions mentioned in the materials.
- `notebooklm.suggested_questions`: 5–10 questions the student should ask the notebook.

## Format
See `templates/content_example.json` (made-up drugs — format reference only).
Top level: `lecture {id,title,date}`, `textbook_status` (`"pending"` or `"included"`),
`objectives [{id,text}]`, `classes [...]`, `notebooklm {...}`.

## Things the audit should skip
Speaker notes that are only teaching instructions ("Point students to…", "Trace the arrows…") go in
`audit_skip`: `{"ref": "S31", "starts_with": "Point to EC50", "reason": "teaching instruction"}`.
Never skip anything that contains a fact.

## Pilot lessons (L01)
- Build from an authoring script (`work/<LEC>/author_<LEC>.py`) that writes content.json — easier to fix.
- Keep option lengths balanced: the audit flags a correct answer >30% longer than every distractor.

## Depth and length (gated)
PA-student depth: no more, no less. PA students are short on time, so the guide is lean, never dense.
- Teach what a PA needs to prescribe safely and answer exam/PANCE questions. Leave out chemistry, molecular-biology and
  drug-industry detail with no prescribing decision attached.
- Textbook additions only where they sharpen what the slides teach or are likely to be tested; merge repeats.
- Gates (`pipeline/standards.py`): textbook-only bullets ≤30% of all bullets, bullets ≤40 words, deck ≤2.25× the lecture's
  slides. The deck shows every lecture quick check plus one new question per part; all questions stay on the site.

## Assigned reading (gated)
The syllabus makes the assigned pages testable, so every section heading on those pages must be taught.
`work/<LEC>/AUTHOR_BRIEF.md` lists them; the audit fails on any that the guide doesn't cover.
A section that belongs to another session, or is beyond PA scope, goes in `READING_SKIP` in `textbook_<LEC>.py`:
`{"heading": "DOSAGE REGIMEN", "reason": "Taught in L02 (PK Calculations)"}`,
`{"heading": "Rational Drug Design", "reason": "Beyond PA scope: how chemists design molecules"}`.

## Figures (gated)
Every figure needs a `caption` and an interactive twin. Either a dedicated diagram exists in
`site_src/assets/viz.js`, or give the figure `"viz": {"type": "dose-response"}` (types are listed in the brief;
`"bars"` takes your own numbers: `{"type": "bars", "title": …, "unit": "%", "bars": [{"label", "value", "note"}]}`).

## After writing
Run `./run.sh new <LEC>`. It builds the deck, NotebookLM pack, audit, standard checks, practice exam,
website and site checks, and ends with a PASS/FAIL report card. Read `outputs/<LEC>/<LEC>_audit.md`
for anything missing; fix the content and re-run until every line says PASS.

## Home-page teaser (every lecture)
In `work/<ID>/guide_<ID>.py`, set `TEASER` to two professional sentences: sentence 1 names what that
session teaches (start "Today:" for the class day's lecture); sentence 2 is the value line ("One cited
guide and exam-style practice — no more hours lost rereading the textbook."). Keep it under ~35 words,
no hype words or exclamation marks. The home page shows the latest lecture's teaser automatically.
