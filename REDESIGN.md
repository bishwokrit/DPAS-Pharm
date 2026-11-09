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

## Next (highest value first)
1. Teriparatide (L04 S43) still shows no downstream change: needs a formation step in the figure's nodes.
2. Emesis, hormone-axis and seesaw scenes: redraw on anatomy, add the same causal chain.
3. Three figures still on the generic layout: L06 S15 step therapy, L03 S57 screening, L08 S24 parathyroid.
4. Home page: tighten the first screen (three status cards + this week's lecture above the fold).
5. Harder practice sets for Units 4–6.

## Rules of the road
- Diagram facts come only from the slide the figure cites. Never infer a downstream effect: list it in `work/scenes.py`.
- `./run.sh site`, then `./run.sh check` before every commit.
