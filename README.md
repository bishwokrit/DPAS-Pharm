# PA Pharmacology Study System

Turns each lecture's slides + textbook reading + syllabus into:
1. a study deck (.pptx) organized by drug class,
2. a NotebookLM source + copy-paste instructions,
3. a coverage audit (proof nothing was left out).

## Where to put your files

```
dpas-pharm/
  inputs/
    syllabus/      <- your syllabus (PDF, Word, or PowerPoint)
    textbook/      <- the full textbook PDF (when you have it)
    study_guide/   <- the course study guide (.docx)
    lectures/
      L01/         <- Lecture 1's slides (.pptx) — one file per folder
      L02/         <- Lecture 2's slides ...
  outputs/
    L01/           <- your finished deck, NotebookLM pack, and audit report appear here
  templates/       <- the shared look and rules (don't need to touch)
  work/            <- behind-the-scenes files (don't need to touch)
  config.json      <- settings, e.g. "theme": "light" or "dark"
```

Lecture folder names (L01, L02, …) come from the syllabus. Run `./run.sh status` to see them.

## Adding a new lecture (3 steps)

1. Drop the lecture's `.pptx` into `inputs/lectures/<ID>/`.
2. Tell Claude: **"author L05"** (use the lecture's ID). Claude reads the slides and textbook
   pages and organizes the content following `templates/AUTHORING_GUIDE.md`.
3. Run: `./run.sh L05`

Your files appear in `outputs/L05/`. Open `L05_audit.md` first — it should say **PASS**.

## Commands

| Command | What it does |
|---|---|
| `./run.sh status` | Shows every lecture and what's done |
| `./run.sh L05` | Builds one lecture (deck + NotebookLM + audit) |
| `./run.sh all` | Rebuilds every lecture that's ready |
| `./run.sh setup` | Makes a folder for each lecture from the syllabus |
| `./run.sh site` | Rebuilds the website (study guides + PDFs + home page) |
| `./run.sh exam U1` | Rebuilds the Unit 1 practice exam app |

## The website

Everything in `docs/` is the website (GitHub Pages serves it). It has a home page with your next
exam, a study guide per lecture (web + PDF, with cram sheet and self-test), and practice exams.
Progress, flags, and your wrong-answer log are saved in your browser.

## Adding the textbook later

Put the PDF in `inputs/textbook/`. On the next run, each lecture's assigned pages are cut out
automatically (using the syllabus readings). The run will say which lectures need the textbook
folded in — tell Claude **"add textbook to L05"**, then re-run.

## Switching light/dark

Open `config.json`, change `"theme": "light"` to `"dark"`, and run `./run.sh all`.

## Using NotebookLM

In `outputs/<ID>/notebooklm/`: upload the `_source` file(s) to a new notebook, then open
`_instructions.md` and paste each box into the matching NotebookLM **Customize** field.

## What the deck markings mean

- **TB** (gold tag) = textbook only, not on the lecture slides
- **SG** (teal tag) = course study guide only, not on the lecture slides
- **Bold** = emphasized on the lecture slides
- `S12` = lecture slide 12 · `p. 245` = textbook page 245 · `SG U1-R3` = study guide, Unit 1, recall item 3
- ⚠ = thin coverage of an objective, or slides and textbook disagree

## One-time install (only if running on your own computer)

Needs Python 3, Node.js, and: `pip install python-pptx pypdf python-docx` and `npm install` in this folder.
