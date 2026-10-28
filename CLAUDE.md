# PA–S Rx — rules for every session

The owner is not a programmer: explain in plain language, keep replies short, and do the work end to end.

## When a new lecture is uploaded ("author L05", "new lecture is up")
1. `./run.sh new L05` — extracts the slides and assigned reading and writes `work/L05/AUTHOR_BRIEF.md`
   (every slide, every reading section, every figure, and the standard). Read it first.
2. Write `work/L05/author_L05.py`, `guide_L05.py`, `textbook_L05.py` following `templates/AUTHORING_GUIDE.md`
   (copy the shape of the L02 files; Units 2–6 use the `drug_class` template). Run `python3 work/L05/author_L05.py`.
3. Add every drug the lecture names to `work/drugs.py` as a full card (class, mechanism, indications, contraindications, adverse
   effects, interactions, distinguishing / patient-specific factors, extra — from the slides and assigned pages). Add the unit's practice questions to `work/exams/U?/`
   (a new unit also needs an entry in `EXAMS` in `pipeline/build_exam.py`).
4. `./run.sh new L05` again until the report card is all PASS. Then commit and push (see Commits below).

Never weaken a gate to make it pass. Fix the content. `audit_skip` / `READING_SKIP` only with a true reason
(teaching instruction, taught in another session, or beyond PA scope — say why).

## The standard
- **Sources only:** slides (with notes), the assigned textbook pages, the syllabus, the course study guide. No internet facts.
  Everything is cited (`S12`, `S12 (notes)`, `p. 245`, `SG U1-R3`). Textbook-only facts are tagged TB.
- **Nothing missed:** every slide line and every assigned-reading section is taught (the audit enforces both).
- **PA-student depth: no more, no less.** PA students are short on time. Teach what a PA needs to prescribe safely and pass
  the exam/PANCE: mechanism → clinical use → adverse effects → interactions → monitoring → traps. Leave out chemistry,
  molecular-biology and drug-industry detail with no prescribing decision attached (skip that reading section as
  "Beyond PA scope"; the guide's Go deeper link opens the pages). Never drop anything the slides teach, and never cut a
  fact that a practice-exam question tests (grep the exam banks for it first; `./run.sh check` also flags exam answers the
  guide doesn't teach).
- **Lean, not dense:** one idea per bullet (≤25 words, gate at 40), merge repeats, prefer one table over five bullets.
  Gates: textbook-only bullets ≤30% of the guide; deck ≤2.25× the lecture's slide count (the deck carries the lecture
  quick checks plus one question per part; the full question set lives on the site).
- **Easier to learn:** a student with only the guide, or only the deck, can answer any exam question on the lecture.
  Make it easier through order, short bullets, discriminator tables, flows, why-hooks and interactive figures.
- Textbook facts are `("text", "p. N")` with ’ for apostrophes so `./run.sh check` can verify every number on its page.
- Questions: ~50/50 vignette/mechanism, 5 balanced options, every slide quick-check rebuilt.
- Every figure has a caption and an interactive version (`"viz": {"type": …}`; types listed in the brief).
- Design: Apple-like, minimal, sleek, professional, smooth motion, never cartoonish. Diagrams rich but readable.
  Interactive figures use the site palette, reset after 30 s idle, and have Try-it steps.

## Never
- Commit the textbook PDF, extracted textbook text, or raw Sketchy material (they live in the private `dpas-textbook` repo).
- Publish the instructor's real quizzes or checkpoints. They live in `dpas-textbook/quizzes/` (private) with `STYLE.md`,
  which describes how she writes questions; use it to shape our own quiz-prep questions, never copy them onto the site.
- Edit the original course files in `inputs/` (they are fingerprinted).
- Put school, course-director or instructor names on the site.
- Use the owner's API key: AI chat runs on each student's own key, in their browser.
- Put model names in commits.

## Commands
`./run.sh status` · `./run.sh new L05` · `./run.sh L05` (lecture only) · `./run.sh site` · `./run.sh exam U1` · `./run.sh check`
(`check` takes a few minutes: run it in the background).

## Commits
Every commit is authored by the owner: `bishwokrit <bishwokrit@gmail.com>` (set in this repo's git config).
No `Co-Authored-By` or session-link lines in commit messages.
