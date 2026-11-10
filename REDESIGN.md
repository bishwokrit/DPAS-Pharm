# Site redesign log

A running record of the design overhaul, so any session can pick it up.

## Done
- **Lecture reader.** Each part is one sheet of labelled rows (same shape as a drug card) instead of uneven three-column
  cards. The label stays in view while its facts scroll; lines keep a readable width; wide screens flow into two columns.
- **Depth switch.** "Everything / Lecture only" on every part folds textbook-only (TB) facts away. Saved per browser
  (`prefs.depth`); print always shows everything.
- **Diagrams: the causal chain in words.** Anatomy figures list the normal pathway, then, once a drug is added, where it
  acts and what changes after it, step by step. Pointing at a step lights its structure.
- **Diagrams: drug-driven steps.** `ON` in `work/scenes.py` names the steps each drug sets in motion (13 figures), so adding
  a drug always shows a consequence. Each list comes from the figure's own slide.
- **Drug cards.** Fields not taught yet fold into one line instead of repeating the same sentence.
- **Accuracy.** ADH figure now shows sodium falling with desmopressin and rising with tolvaptan.

- **Concept figures.** Step therapy (L06) is a ladder, DMARD screening (L03) a checklist and parathyroid strategies (L08)
  two lanes, instead of the generic boxes.
- **Hormone axis.** Stronger feedback, and with an outside hormone the readout separates "hormone + drug" from what the
  gland itself makes.
- **Ulcer balance.** H. pylori alone now tips it toward injury. **PTH loop.** Teriparatide no longer docks on resorption.
- **Home.** Headline, the three status cards and this week's lecture fit on the first screen.
- **Sidekick prompt.** Tutors in a chain (target, change, effect, predicted adverse effect) and explains wrong answers.
- **Rules.** Diagram rules added to `CLAUDE.md` and `templates/AUTHORING_GUIDE.md`.
- **Practice.** Harder B sets for Units 4, 5 and 6 (20 questions, 24 minutes each).

- **B sets** for Units 4–6 are now 30 questions, 36 minutes.
- **Balance, cycle and nausea figures** list the story in words; nausea and hormone-axis figures sit on drawn anatomy.

## Next
See the critique list agreed with the owner (performance, question review, Words mode, progress backup).

## Rules of the road
- Diagram facts come only from the slide the figure cites. Never infer a downstream effect: list it in `work/scenes.py`.
- `./run.sh site`, then `./run.sh check` before every commit.
