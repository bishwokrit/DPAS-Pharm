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

**Sidekick** (the ✦ button on every lecture page, or press `/`) is a built-in study assistant:
Ask (searches the lecture, with citations), Listen (audio overview read aloud), Flashcards (with
spaced repetition), Quiz, Mind map, Briefing (printable), and FAQ. All of these are free and run
in the browser. **AI chat** is optional: each person pastes their own Anthropic API key in
Sidekick → Ask → "Turn on AI chat". The key stays in that browser and goes only to Anthropic.
Claude answers only from the lecture's cited source. The site has no key and no server of its own:
each student's key stays in their browser and goes straight to Anthropic, so nobody can use your
Claude account or credits, and students are billed only on their own Anthropic accounts.

**Highlight anything** in a study guide to get a small toolbar: Explain, Source (shows the actual
slide, speaker notes, textbook page, or study-guide item), Quiz me, Card (make your own flashcard),
Save (keeps the highlight; it collects in Sidekick → Notes), and Copy (copies with its citation).
Hover any citation like `S23` to preview the slide, or click it to see the full source.

**Focus quizzes:** "Start focus quiz" (self-test), "Full screen" (Sidekick quiz), and "Start focus
session" (practice exam) open a distraction-free, full-screen quiz. Study mode shows explanations as
you go; Timed mode gives 1 minute per question (PANCE pace) and shows results at the end. Every
session ends with a debrief: score, time, weakest topics with "Study →" links, every miss, and
suggestions. Remote rings and keyboards: ↑/↓ choose · Enter lock in · → next · ← back · F flag ·
Esc exit (rings that act as a mouse wheel also work).

**Review page** (`Review` in the top bar) for exam week: Daily 10 (a 10-question set each day,
weighted toward what you've missed or haven't seen, with a streak), every missed and flagged question
from all lectures and exams in one list, weakest topics with "Study →" links, a weak-flashcard drill,
all your saved notes, and mixed exams across every lecture (a 40-question timed weak-spot exam, or
a custom one).

**Practice exams:** Exam A (100 questions) and Exam B (50 new questions, real exam length, includes
the assigned Katzung reading). Exam B's focus session defaults to exam conditions: 50 questions in
60 minutes. Build another with `./run.sh exam U1B` (banks live in `work/exams/<ID>/bank*.py`).

**Sidekick extras:** Ask can search *this lecture* or *all lectures*; highlight two things and tap
⇄ Compare for a side-by-side from every lecture.

**Syllabus page** (`Syllabus` in the top bar): what's due next with countdowns, the full schedule
(past rows fade, today is highlighted), grading weights and rules, readings and objectives per unit,
and a **grade calculator** (current grade, projected grade, and "what do I need on the final" for
A/B/C, with the 75%-on-the-final rule and checkpoint bonus built in). The dates and weights live in
`work/schedule.json`; edit that file if the syllabus changes.

**Search** (⌘K / Ctrl+K or the Search button): searches every lecture fact, cram row, self-test and
exam question, objective, deadline, and rule. Opening a result jumps to the spot with your words
highlighted.

**Sharing with classmates:** just send the website link. Everyone's progress is private to their
own browser, and the footer says it's an unofficial student-made aid. The textbook PDF and its
extracted text are never put on the website or in this repo.

(Maintainer note: the chat uses the official Anthropic SDK bundled into
`site_src/assets/vendor/`. To update it: `npm i -D @anthropic-ai/sdk@<version>` then
`node pipeline/build_vendor.mjs`.)

## Adding the textbook later

The textbook PDF lives in your private `dpas-textbook` repo (cloned next to this one), or put it in
`inputs/textbook/`. Neither is ever committed here. On the next run, each lecture's assigned pages are cut out
automatically (using the syllabus readings). The run will say which lectures need the textbook
folded in — tell Claude **"add textbook to L05"**, then re-run. Textbook additions live in
`work/<ID>/textbook_<ID>.py` (tagged TB, cited by printed page).

## Switching light/dark

Open `config.json`, change `"theme": "light"` to `"dark"`, and run `./run.sh all`.

## Using NotebookLM (optional — Sidekick covers this on the website)

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
