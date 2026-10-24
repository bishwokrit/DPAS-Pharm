// Turn a lecture's resolved content (work/<LEC>/content.resolved.json) into the study deck.
// Usage: node build_deck.js <content.resolved.json> <out.pptx> <light|dark>
// Every visual choice lives in templates/deck_style.json so all lectures look the same.
const fs = require("fs");
const path = require("path");
const pptxgen = require("pptxgenjs");
const React = require("react");
const ReactDOMServer = require("react-dom/server");
const sharp = require("sharp");
const Fa = require("react-icons/fa");
const { applyTheme } = require("./apply_theme.js");

const [, , contentPath, outPath, themeName = "light"] = process.argv;
const content = JSON.parse(fs.readFileSync(contentPath, "utf8"));
const STYLE = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "templates", "deck_style.json"), "utf8"));
const T = STYLE.themes[themeName];
if (!T) throw new Error(`Unknown theme "${themeName}" — use light or dark`);
const F = STYLE.fonts;

const W = 13.333, H = 7.5, MX = 0.6;
const TOP = 1.45, BOTTOM = 6.85; // content band
// Must match TEMPLATES in content.py
const TEMPLATES = {
  drug_class: [
    ["overview", "Class", "FaLayerGroup"],
    ["prototype", "Prototype + other drugs named", "FaPills"],
    ["moa", "Mechanism of action", "FaCogs"],
    ["indications", "Indications", "FaCheckCircle"],
    ["adverse", "Adverse effects (boxed warnings first)", "FaExclamationTriangle"],
    ["contra", "Contraindications", "FaBan"],
    ["interactions", "Drug interactions", "FaExchangeAlt"],
    ["pk", "Pharmacokinetics", "FaRoute"],
    ["monitoring", "Monitoring", "FaHeartbeat"],
    ["pearls", "Clinical pearls / \"why\" hook", "FaLightbulb"],
  ],
  concept: [
    ["definitions", "Key definitions", "FaBookOpen"],
    ["how", "How it works", "FaCogs"],
    ["clinical", "Clinical relevance", "FaUserMd"],
    ["examples", "Drugs named as examples", "FaPills"],
    ["traps", "Exam traps", "FaExclamationTriangle"],
  ],
};
const sectionsFor = (c) => TEMPLATES[c.template || "drug_class"];
const unitName = (c) => (c.template === "concept" ? "Topic" : "Drug class");
const allConcept = content.classes.every((c) => c.template === "concept");
const figDir = path.join(path.dirname(contentPath), "figures");
const textbookPending = content.textbook_status !== "included";

// ---------- helpers ----------
const iconCache = {};
async function icon(name, color) {
  const key = name + color;
  if (!iconCache[key]) {
    const svg = ReactDOMServer.renderToStaticMarkup(React.createElement(Fa[name], { color: "#" + color, size: 256 }));
    const png = await sharp(Buffer.from(svg)).png().toBuffer();
    iconCache[key] = "image/png;base64," + png.toString("base64");
  }
  return iconCache[key];
}

// Exact word-wrap using real Calibri character widths (from measure.py), so text never
// depends on "shrink to fit" (PowerPoint ignores it until you edit the box).
const WIDTHS = JSON.parse(fs.readFileSync(path.join(path.dirname(contentPath), "char_widths.json"), "utf8"));
function textWidth(str, pt, bold) {
  const table = bold ? WIDTHS.bold : WIDTHS.regular;
  let em = 0;
  for (const ch of str) em += table[ch] ?? 0.6;
  return (em * pt) / 72;
}
// Lines needed for text with **bold** parts, wrapped at word boundaries within widthIn.
function lines(text, widthIn, pt, allBold = false) {
  let total = 0;
  for (const para of String(text).split("\n")) {
    const words = [];
    para.split(/(\*\*[^*]+\*\*)/).forEach((part) => {
      if (!part) return;
      const bold = allBold || (part.startsWith("**") && part.endsWith("**"));
      const clean = bold && part.startsWith("**") ? part.slice(2, -2) : part;
      clean.split(/(?<= )/).forEach((w) => w && words.push({ w, bold }));
    });
    let n = 1, cur = 0;
    for (const { w, bold } of words) {
      const ww = textWidth(w, pt, bold);
      if (cur > 0 && cur + textWidth(w.trimEnd(), pt, bold) > widthIn) { n++; cur = 0; }
      cur += ww;
      while (cur > widthIn) { n++; cur -= widthIn; } // a single word longer than the line
    }
    total += n;
  }
  return total;
}
const lineH = (pt) => (pt * 1.22) / 72;
// Largest font size (maxPt..minPt) that keeps text within maxLines.
function fitPt(text, widthIn, maxPt, minPt, bold, maxLines = 1) {
  for (let pt = maxPt; pt >= minPt; pt--) if (lines(text, widthIn, pt, bold) <= maxLines) return pt;
  return null;
}
function factLine(f) {
  return (f.tb ? "TB  " : "") + (f.sg ? "SG  " : "") + (typeof f === "string" ? f : f.text || "") + "  " + (f.src || "");
}
function bulletsHeight(facts, widthIn, pt) {
  return facts.reduce((h, f) => h + lines(factLine(f), widthIn - 0.3, pt) * lineH(pt) + 0.12, 0);
}
const plain = (f) => (typeof f === "string" ? f : f.text || "").replace(/\*\*/g, "");

// "**bold**" -> text runs. Bold in content = emphasized in the lecture.
function richRuns(text, base) {
  const runs = [];
  String(text).split(/(\*\*[^*]+\*\*)/).forEach((part) => {
    if (!part) return;
    const bold = part.startsWith("**") && part.endsWith("**");
    runs.push({ text: bold ? part.slice(2, -2) : part, options: { ...base, bold: bold || base.bold } });
  });
  return runs;
}
function tbTag(pt) {
  return { text: " TB ", options: { fontSize: Math.max(10, pt - 4), bold: true, color: T.tbText, highlight: T.tb } };
}
function sgTag(pt) {
  return { text: " SG ", options: { fontSize: Math.max(10, pt - 4), bold: true, color: T.sgText, highlight: T.sg } };
}
function citeRun(src, pt) {
  return { text: `  ${src}`, options: { fontSize: Math.max(10, pt - 5), color: T.muted } };
}
// One bullet paragraph: [TB] text [citation]
function factRuns(f, pt, last) {
  const runs = [];
  if (f.tb) runs.push(tbTag(pt), { text: " ", options: { fontSize: pt } });
  if (f.sg) runs.push(sgTag(pt), { text: " ", options: { fontSize: pt } });
  runs.push(...richRuns(f.text, { fontSize: pt, color: T.text }));
  if (f.src) runs.push(citeRun(f.src, pt));
  runs[0].options = { ...runs[0].options, bullet: { indent: 18 }, paraSpaceAfter: 8 };
  if (!last) runs[runs.length - 1].options.breakLine = true;
  return runs;
}
function factsToRuns(facts, pt) {
  return facts.flatMap((f, i) => factRuns(f, pt, i === facts.length - 1));
}
function notCovered() {
  return [{ text: textbookPending ? "Not covered in slides · textbook pending" : "Not covered in materials", tb: false, src: "", _empty: true }];
}

// ---------- deck ----------
const pres = new pptxgen();
pres.layout = "LAYOUT_WIDE";
pres.theme = { headFontFace: F.head, bodyFontFace: F.body };
pres.title = `${content.lecture.id} ${content.lecture.title}`;
let slideNo = 0;

function base(kicker, title, objectives) {
  const s = pres.addSlide();
  slideNo++;
  s.background = { color: T.bg };
  const titleW = objectives ? W - 2 * MX - 3.3 : W - 2 * MX;
  let kick = kicker ? kicker.toUpperCase() : "";
  const kickPt = kick ? fitPt(kick, titleW, 12, 9, true) || 9 : 12;
  while (kick && lines(kick, titleW, kickPt, true) > 1) kick = kick.slice(0, -2).trimEnd() + "…";
  if (kick) s.addText(kick, { x: MX, y: 0.32, w: titleW, h: 0.3, fontSize: kickPt, bold: true, color: T.accent, charSpacing: 1, margin: 0, isTextBox: true, objectName: "Kicker" });
  // one line from 30pt down to 20pt; otherwise two lines at up to 22pt (box holds both)
  const titlePt = fitPt(title, titleW, 30, 20, true) || fitPt(title, titleW, 22, 16, true, 2) || 16;
  s.addText(title, { x: MX, y: 0.62, w: titleW, h: 0.78, fontSize: titlePt, bold: true, color: T.text, fontFace: F.head, margin: 0, valign: "top", isTextBox: true, objectName: "Title" });
  if (objectives && objectives.length) {
    const chip = "Objectives: " + objectives.join(" · ");
    s.addText(chip, { shape: pres.shapes.ROUNDED_RECTANGLE, rectRadius: 0.15, x: W - MX - 3.0, y: 0.4, w: 3.0, h: 0.42, fontSize: fitPt(chip, 2.8, 12, 8, true) || 8, bold: true, color: T.chipText, fill: { color: T.chip }, align: "center", valign: "middle", margin: 2, objectName: "Objective chip" });
  }
  s.addText(`${content.lecture.id} · ${content.lecture.title}`, { x: MX, y: 7.02, w: 8, h: 0.3, fontSize: 10, color: T.muted, margin: 0, isTextBox: true, objectName: "Footer" });
  s.addText(String(slideNo), { x: W - MX - 1, y: 7.02, w: 1, h: 0.3, fontSize: 10, color: T.muted, align: "right", margin: 0, isTextBox: true, objectName: "Slide number" });
  return s;
}

async function card(s, { x, y, w, h, label, iconName, color, facts, pt = F.bodyPt }) {
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w, h, rectRadius: 0.12, fill: { color: T.card }, line: { color: T.card }, objectName: `${label} card` });
  s.addShape(pres.shapes.OVAL, { x: x + 0.25, y: y + 0.2, w: 0.48, h: 0.48, fill: { color }, line: { color }, objectName: `${label} icon circle` });
  s.addImage({ data: await icon(iconName, "FFFFFF"), x: x + 0.36, y: y + 0.31, w: 0.26, h: 0.26, objectName: `${label} icon` });
  s.addText(label, { x: x + 0.88, y: y + 0.2, w: w - 1.1, h: 0.48, fontSize: 18, bold: true, color, valign: "middle", margin: 0, isTextBox: true, objectName: `${label} heading` });
  const empty = facts.length === 1 && facts[0]._empty;
  s.addText(empty ? [{ text: facts[0].text, options: { fontSize: pt, italic: true, color: T.muted } }] : factsToRuns(facts, pt),
    { x: x + 0.25, y: y + 0.82, w: w - 0.5, h: h - 0.95, valign: "top", margin: 0, isTextBox: true, objectName: `${label} body` });
}

// Split a list into chunks that fit a given height.
function paginate(items, fits) {
  const pages = [];
  let cur = [];
  for (const it of items) {
    if (cur.length && !fits([...cur, it])) { pages.push(cur); cur = []; }
    cur.push(it);
  }
  if (cur.length) pages.push(cur);
  if (pages.length < 2) return pages;
  // even out the split (e.g., 5+5 instead of 8+2) when the evened pages still fit
  const per = Math.ceil(items.length / pages.length);
  const even = [];
  for (let i = 0; i < items.length; i += per) even.push(items.slice(i, i + per));
  return even.length === pages.length && even.every((pg) => fits(pg)) ? even : pages;
}

// ---------- slide builders ----------
async function titleSlide() {
  const s = pres.addSlide();
  slideNo++;
  s.background = { color: T.bg };
  s.addText(content.lecture.id + (content.lecture.date ? ` · ${content.lecture.date}` : ""), { x: MX, y: 1.5, w: 10, h: 0.4, fontSize: 16, bold: true, color: T.accent, margin: 0, isTextBox: true });
  s.addText(content.lecture.title, { x: MX, y: 1.95, w: W - 2 * MX, h: 1.4, fontSize: fitPt(content.lecture.title, W - 2 * MX, 44, 32, true) || fitPt(content.lecture.title, W - 2 * MX, 38, 24, true, 2) || 24, bold: true, color: T.text, fontFace: F.head, margin: 0, valign: "top", isTextBox: true, objectName: "Title" });
  s.addText(`Pharmacology study deck · organized by ${allConcept ? "topic" : "drug class"}`, { x: MX, y: 3.35, w: 10, h: 0.4, fontSize: 18, color: T.muted, margin: 0, isTextBox: true });
  // legend
  const ly = 4.2;
  s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: MX, y: ly, w: W - 2 * MX, h: 2.3, rectRadius: 0.12, fill: { color: T.card }, line: { color: T.card }, objectName: "Legend card" });
  s.addText("How to read this deck", { x: MX + 0.3, y: ly + 0.2, w: 6, h: 0.4, fontSize: 16, bold: true, color: T.text, margin: 0, isTextBox: true });
  const legend = [
    [{ text: " TB ", options: { bold: true, color: T.tbText, highlight: T.tb, fontSize: 14 } }, { text: "  = textbook only (not on the lecture slides)", options: { fontSize: 14, color: T.text } }],
    [{ text: " SG ", options: { bold: true, color: T.sgText, highlight: T.sg, fontSize: 14 } }, { text: "  = course study guide only (not on the lecture slides)", options: { fontSize: 14, color: T.text } }],
    [{ text: "Bold", options: { bold: true, fontSize: 14, color: T.text } }, { text: " = emphasized on the lecture slides", options: { fontSize: 14, color: T.text } }],
    [{ text: "S12", options: { fontSize: 14, color: T.muted } }, { text: " = lecture slide 12   ·   ", options: { fontSize: 14, color: T.text } }, { text: "p. 245", options: { fontSize: 14, color: T.muted } }, { text: " = textbook page 245   ·   ", options: { fontSize: 14, color: T.text } }, { text: "SG U1-R3", options: { fontSize: 14, color: T.muted } }, { text: " = study guide item", options: { fontSize: 14, color: T.text } }],
  ];
  if (textbookPending) legend.push([{ text: "Textbook not added yet — this deck is built from the slides only.", options: { fontSize: 14, italic: true, color: T.warn } }]);
  const runs = legend.flatMap((row, i) => { row[row.length - 1].options.breakLine = i < legend.length - 1; row[0].options.paraSpaceAfter = 4; return row; });
  s.addText(runs, { x: MX + 0.3, y: ly + 0.6, w: W - 2 * MX - 0.6, h: 1.6, valign: "top", margin: 0, isTextBox: true, objectName: "Legend" });
}

function objectiveCoverage() {
  return content.objectives.map((o) => {
    const classes = content.classes.filter((c) => (c.objectives || []).includes(o.id));
    const facts = classes.reduce((n, c) => n + Object.values(c.sections).flat().length, 0);
    const thin = classes.length === 0 || facts < STYLE.thin_coverage_min_facts || !!o.thin_note;
    return { ...o, classes, thin };
  });
}

async function objectivesSlides() {
  const cov = objectiveCoverage();
  const note = (o) => (o.thin ? "⚠ Thin coverage: " : "") + (o.thin_note ? o.thin_note + " · " : "") + (o.classes.length ? o.classes.map((c) => c.name).join(", ") : "No section covers this");
  const rowH = (o) => Math.max(0.62, lines(o.text, 6.8, 16) * lineH(16) + 0.3, lines(note(o), 3.9, 12) * lineH(12) + 0.25);
  const pages = paginate(cov, (arr) => arr.reduce((h, o) => h + rowH(o) + 0.12, 0) <= BOTTOM - TOP);
  for (const [pi, page] of pages.entries()) {
    const s = base("Start here", "Learning objectives" + (pi ? " (cont.)" : ""));
    let y = TOP;
    for (const o of page) {
      const h = rowH(o);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: MX, y, w: W - 2 * MX, h, rectRadius: 0.1, fill: { color: o.thin ? T.warnBg : T.card }, line: { color: o.thin ? T.warnBg : T.card }, objectName: `Objective ${o.id}` });
      s.addText(o.id, { x: MX + 0.2, y, w: 0.8, h, fontSize: 16, bold: true, color: T.accent, valign: "middle", margin: 0, isTextBox: true });
      s.addText(richRuns(o.text, { fontSize: 16, color: T.text }), { x: MX + 1.0, y, w: 6.8, h, valign: "middle", margin: 0, isTextBox: true });
      s.addText([{ text: o.thin ? "⚠ Thin coverage\n" : "", options: { bold: true, color: T.warn, fontSize: 12 } }, { text: note(o).replace("⚠ Thin coverage: ", ""), options: { color: T.muted, fontSize: 12 } }],
        { x: MX + 8.0, y, w: W - 2 * MX - 8.2, h, valign: "middle", margin: 0, isTextBox: true });
      y += h + 0.12;
    }
  }
}

async function roadmapSlide() {
  const s = base("Roadmap", allConcept ? "Topics in this lecture" : "Drug classes in this lecture");
  const n = content.classes.length, cols = n > 4 ? 2 : 1;
  const per = Math.ceil(n / cols), colW = (W - 2 * MX - (cols - 1) * 0.4) / cols;
  const rowH = Math.min(1.0, (BOTTOM - TOP - (per - 1) * 0.15) / per);
  content.classes.forEach((c, i) => {
    const x = MX + Math.floor(i / per) * (colW + 0.4), y = TOP + (i % per) * (rowH + 0.15);
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x, y, w: colW, h: rowH, rectRadius: 0.1, fill: { color: T.card }, line: { color: T.card } });
    s.addShape(pres.shapes.OVAL, { x: x + 0.2, y: y + rowH / 2 - 0.25, w: 0.5, h: 0.5, fill: { color: T.accent }, line: { color: T.accent } });
    s.addText(String(i + 1), { x: x + 0.2, y: y + rowH / 2 - 0.25, w: 0.5, h: 0.5, fontSize: 16, bold: true, color: "FFFFFF", align: "center", valign: "middle", margin: 0, isTextBox: true });
    s.addText([{ text: c.name, options: { fontSize: fitPt(c.name, colW - 1.1, 18, 13, true, 2) || 13, bold: true, color: T.text, breakLine: true } }, { text: "Objectives: " + ((c.objectives || []).join(", ") || "—"), options: { fontSize: 12, color: T.muted } }],
      { x: x + 0.9, y, w: colW - 1.1, h: rowH, valign: "middle", margin: 0, isTextBox: true });
  });
}

async function aboutSlides() {
  const facts = content.about || [];
  if (!facts.length) return;
  const full = W - 2 * MX;
  const pages = paginate(facts, (arr) => cardH(arr, full) <= BOTTOM - TOP);
  for (const [pi, page] of pages.entries()) {
    const s = base("Start here", "About this lecture" + (pi ? " (cont.)" : ""));
    await card(s, { x: MX, y: TOP, w: full, h: Math.max(cardH(page, full), 2.2), label: "Scope, readings & sources", iconName: "FaInfoCircle", color: T.accent, facts: page });
  }
}

async function dividerSlide(c, idx) {
  const s = pres.addSlide();
  slideNo++;
  s.background = { color: T.accentDark };
  s.addText(`${unitName(c)} ${idx + 1} of ${content.classes.length}`, { x: MX, y: 1.6, w: 8, h: 0.4, fontSize: 16, bold: true, color: T.onAccentMuted, margin: 0, isTextBox: true });
  s.addText(c.name, { x: MX, y: 2.05, w: W - 2 * MX, h: 1.3, fontSize: fitPt(c.name, W - 2 * MX, 44, 32, true) || fitPt(c.name, W - 2 * MX, 36, 24, true, 2) || 24, bold: true, color: "FFFFFF", fontFace: F.head, margin: 0, valign: "top", isTextBox: true, objectName: "Title" });
  s.addText("Covers objectives: " + ((c.objectives || []).join(" · ") || "—"), { x: MX, y: 3.4, w: 10, h: 0.4, fontSize: 18, color: T.onAccentMuted, margin: 0, isTextBox: true });
  // the 8-step template as an icon row: same order in every class
  const SECTIONS = sectionsFor(c);
  const step = (W - 2 * MX) / SECTIONS.length;
  for (const [i, [, label, ic]] of SECTIONS.entries()) {
    const x = MX + i * step;
    s.addShape(pres.shapes.OVAL, { x: x + step / 2 - 0.35, y: 4.7, w: 0.7, h: 0.7, fill: { color: T.section[SECTIONS[i][0]] }, line: { color: "FFFFFF", width: 1.5 } });
    s.addImage({ data: await icon(ic, "FFFFFF"), x: x + step / 2 - 0.18, y: 4.87, w: 0.36, h: 0.36 });
    s.addText(label.replace(/ \(.*\)| \/ .*| \+ .*/, ""), { x: x + 0.05, y: 5.5, w: step - 0.1, h: 0.7, fontSize: SECTIONS.length > 8 ? 10 : 12, color: "FFFFFF", align: "center", valign: "top", margin: 0, isTextBox: true });
  }
  s.addText(String(slideNo), { x: W - MX - 1, y: 7.02, w: 1, h: 0.3, fontSize: 10, color: T.onAccentMuted, align: "right", margin: 0, isTextBox: true });
}

const CARD_HEAD = 0.95;
const cardH = (facts, w) => CARD_HEAD + bulletsHeight(facts, w - 0.5, F.bodyPt) + 0.2;

async function sectionSlides(c) {
  const band = BOTTOM - TOP, gap = 0.3;
  const full = W - 2 * MX, half = (full - gap) / 2;
  const secs = sectionsFor(c).map(([key, label, ic]) => {
    const facts = (c.sections[key] || []).length ? c.sections[key] : notCovered();
    return { key, label, ic, facts, color: T.section[key] };
  });
  const place = async (s, sec, x, y, w, h) => card(s, { x, y, w, h, label: sec.label, iconName: sec.ic, color: sec.color, facts: sec.facts });
  let i = 0;
  while (i < secs.length) {
    const four = secs.slice(i, i + 4);
    const rowH = (pair) => Math.max(...pair.map((sec) => cardH(sec.facts, half)));
    if (four.length === 4 && rowH(four.slice(0, 2)) + rowH(four.slice(2)) + gap <= band) {
      const s = base(c.name, `${four[0].label} → ${four[3].label}`, c.objectives);
      const h1 = rowH(four.slice(0, 2)), h2 = rowH(four.slice(2));
      for (const [k, sec] of four.entries()) await place(s, sec, MX + (k % 2) * (half + gap), k < 2 ? TOP : TOP + h1 + gap, half, k < 2 ? h1 : h2);
      i += 4;
      continue;
    }
    const two = secs.slice(i, i + 2);
    if (two.length === 2 && rowH(two) <= band) {
      const s = base(c.name, `${two[0].label} · ${two[1].label}`, c.objectives);
      const h = Math.max(rowH(two), 2.2);
      for (const [k, sec] of two.entries()) await place(s, sec, MX + k * (half + gap), TOP, half, h);
      i += 2;
      continue;
    }
    const a = secs[i];
    const pages = paginate(a.facts, (arr) => cardH(arr, full) <= band);
    for (const [pi, page] of pages.entries()) {
      const s = base(c.name, a.label + (pi ? " (cont.)" : ""), c.objectives);
      await card(s, { x: MX, y: TOP, w: full, h: Math.max(cardH(page, full), 2.2), label: a.label + (pages.length > 1 ? ` (${pi + 1}/${pages.length})` : ""), iconName: a.ic, color: a.color, facts: page });
    }
    i += 1;
  }
}

async function figureSlides(c) {
  for (const fig of c.figures || []) {
    const file = path.join(figDir, fig.image);
    if (!fs.existsSync(file)) throw new Error(`figure not found: ${file}`);
    const meta = await sharp(file).metadata();
    const s = base(c.name, fig.title || "Figure", c.objectives);
    const capH = lines(fig.caption + " " + (fig.src || ""), W - 2 * MX, 16) * lineH(16) + 0.1;
    const boxW = W - 2 * MX, boxH = BOTTOM - TOP - capH - 0.2;
    const scale = Math.min(boxW / meta.width, boxH / meta.height);
    const w = meta.width * scale, h = meta.height * scale;
    s.addImage({ path: file, x: (W - w) / 2, y: TOP, w, h, objectName: `Figure ${fig.image}` });
    s.addText([...richRuns(fig.caption, { fontSize: 16, color: T.text }), citeRun(fig.src || "", 16)],
      { x: MX, y: TOP + h + 0.2, w: boxW, h: capH, valign: "top", margin: 0, isTextBox: true, objectName: "Figure caption" });
  }
}

async function conflictSlides(c) {
  if (!(c.conflicts || []).length) return;
  for (const cf of c.conflicts) {
    const s = base(c.name, "⚠ Sources disagree: " + cf.topic, c.objectives);
    const colW = (W - 2 * MX - 0.4) / 2;
    const ch = Math.max(2.2, cardH([{ text: cf.slides.text, src: cf.slides.src }], colW), cardH([{ text: cf.textbook.text, src: cf.textbook.src, tb: true }], colW));
    await card(s, { x: MX, y: TOP, w: colW, h: ch, label: "Lecture slides say", iconName: "FaChalkboardTeacher", color: T.accent, facts: [{ text: cf.slides.text, src: cf.slides.src }] });
    await card(s, { x: MX + colW + 0.4, y: TOP, w: colW, h: ch, label: "Textbook says", iconName: "FaBook", color: T.tbHeading, facts: [{ text: cf.textbook.text, src: cf.textbook.src, tb: true }] });
  }
}

const TPT = 16;
async function comparisonSlides(c) {
  for (const tbl of c.comparisons || []) {
    const full = W - 2 * MX;
    const nCol = tbl.columns.length;
    const firstW = Math.min(2.6, full / nCol), restW = (full - firstW) / (nCol - 1);
    const colW = [firstW, ...Array(nCol - 1).fill(restW)];
    // 16pt by default; drop to 14pt if that keeps the table on one slide
    let pt, rowH, headH, pages;
    for (pt of [TPT, 14]) {
      rowH = (row, head = false) => Math.max(...row.map((cell, j) => lines(String(cell), colW[j] - 0.25, pt, head || j === 0))) * lineH(pt) + 0.14;
      headH = rowH(tbl.columns, true);
      pages = paginate(tbl.rows, (rows) => headH + rows.reduce((h, r) => h + rowH(r), 0) <= BOTTOM - TOP - 0.45);
      if (pages.length === 1) break;
    }
    for (const [pi, rows] of pages.entries()) {
      const s = base(c.name, "Compare: " + tbl.title + (pi ? " (cont.)" : ""), c.objectives);
      const header = tbl.columns.map((h) => ({ text: h, options: { bold: true, color: "FFFFFF", fill: { color: T.accent }, fontSize: pt } }));
      const body = rows.map((r, ri) => r.map((cell, j) => ({ text: richRuns(String(cell), { fontSize: pt, color: T.text, ...(j === 0 ? { bold: true } : {}) }), options: { fill: { color: ri % 2 ? T.bg : T.card } } })));
      s.addTable([header, ...body], { x: MX, y: TOP, w: full, colW, border: { type: "solid", pt: 0.75, color: T.rule }, valign: "middle", margin: [4, 6, 4, 6], objectName: "Comparison table" });
      const cap = [];
      if (tbl.tb) cap.push(tbTag(14), { text: "  ", options: {} });
      cap.push({ text: "Focus: what tells these apart.  Sources: " + (tbl.src || ""), options: { fontSize: 11, color: T.muted } });
      const tblH = headH + rows.reduce((h, r) => h + rowH(r), 0);
      s.addText(cap, { x: MX, y: Math.min(TOP + tblH + 0.15, BOTTOM - 0.3), w: full, h: 0.3, margin: 0, isTextBox: true, objectName: "Table sources" });
    }
  }
}

async function hookSlides(c) {
  const hooks = c.hooks || [];
  if (!hooks.length) return;
  const colW = (W - 2 * MX - 0.4) / 2;
  const hookH = (h) => cardH([h], colW);
  // fill two columns per slide
  const pages = [];
  let cur = [[], []], colHeights = [0, 0];
  for (const h of hooks) {
    const need = hookH(h) + 0.25;
    let col = colHeights[0] <= colHeights[1] ? 0 : 1;
    if (colHeights[col] + need > BOTTOM - TOP + 0.25) col = 1 - col;
    if (colHeights[col] + need > BOTTOM - TOP + 0.25) { pages.push(cur); cur = [[], []]; colHeights = [0, 0]; col = 0; }
    cur[col].push(h); colHeights[col] += need;
  }
  pages.push(cur);
  for (const [pi, cols] of pages.entries()) {
    const s = base(c.name, "Memory hooks" + (pi ? " (cont.)" : ""), c.objectives);
    for (const [ci, col] of cols.entries()) {
      let y = TOP;
      for (const h of col) {
        const hh = hookH(h), mn = h.kind === "mnemonic";
        await card(s, { x: MX + ci * (colW + 0.4), y, w: colW, h: hh, label: mn ? "Mnemonic (memory aid)" : "Why it happens", iconName: mn ? "FaBrain" : "FaLightbulb", color: mn ? T.mnemonic : T.why, facts: [{ text: h.text, src: h.src, tb: h.tb }] });
        y += hh + 0.25;
      }
    }
  }
}

async function highYieldSlides(c) {
  const facts = c.high_yield || [];
  if (!facts.length) return;
  const full = W - 2 * MX;
  const pages = paginate(facts, (arr) => cardH(arr, full) <= BOTTOM - TOP);
  for (const [pi, page] of pages.entries()) {
    const s = base(c.name, "High-yield summary" + (pi ? " (cont.)" : ""), c.objectives);
    await card(s, { x: MX, y: TOP, w: full, h: Math.max(cardH(page, full), 2.2), label: "If you remember nothing else", iconName: "FaStar", color: T.highYield, facts: page });
  }
}

// The deck stays lean: every lecture quick check, plus one new question per part (a vignette when there is one).
// The full question set lives in the web guide's self-test and the practice exams.
function deckQuestions(c) {
  const qs = c.questions || [];
  const extra = qs.filter((q) => !q.from_slides).sort((a, b) => (b.kind === "vignette") - (a.kind === "vignette"))[0];
  return qs.filter((q) => q.from_slides || q === extra);
}

async function questionSlides(c) {
  for (const q of deckQuestions(c)) {
    const kind = q.kind === "vignette" ? "Clinical vignette" : "Mechanism";
    const full = W - 2 * MX;
    // --- question ---
    let pt = F.bodyPt;
    const qHeight = (p) => lines(q.stem, full - 0.5, p) * lineH(p) + 0.4 + Object.values(q.options).reduce((h, o) => h + Math.max(0.5, lines(o.text, full - 1.2, p) * lineH(p) + 0.14) + 0.1, 0);
    if (qHeight(pt) > BOTTOM - TOP) pt = 16;
    const origin = q.from_slides ? ` · lecture quick check ${q.from_slides}` : "";
    let s = base(`${kind}${origin}`, `Question ${q.number}`, c.objectives);
    const stemH = lines(q.stem, full - 0.5, pt) * lineH(pt) + 0.4;
    s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: MX, y: TOP, w: full, h: stemH, rectRadius: 0.1, fill: { color: T.card }, line: { color: T.card }, objectName: "Question stem card" });
    s.addText(richRuns(q.stem, { fontSize: pt, color: T.text }), { x: MX + 0.25, y: TOP, w: full - 0.5, h: stemH, valign: "middle", margin: 0, isTextBox: true, objectName: "Question stem" });
    let y = TOP + stemH + 0.2;
    for (const [L, o] of Object.entries(q.options)) {
      const oh = Math.max(0.5, lines(o.text, full - 1.2, pt) * lineH(pt) + 0.14);
      s.addShape(pres.shapes.OVAL, { x: MX, y: y + oh / 2 - 0.22, w: 0.44, h: 0.44, fill: { color: T.bg }, line: { color: T.accent, width: 1.5 } });
      s.addText(L, { x: MX, y: y + oh / 2 - 0.22, w: 0.44, h: 0.44, fontSize: 14, bold: true, color: T.accent, align: "center", valign: "middle", margin: 0, isTextBox: true });
      s.addText(o.text, { x: MX + 0.7, y, w: full - 0.9, h: oh, fontSize: pt, color: T.text, valign: "middle", margin: 0, isTextBox: true, objectName: `Option ${L}` });
      y += oh + 0.1;
    }
    s.addNotes(`Answer on the next slide. Source: ${q.src || ""}`);
    // --- answer + explanation ---
    const ans = q.options[q.answer];
    const wrong = Object.entries(q.options).filter(([, o]) => !o.correct);
    const apt = 16;
    const ansH = Math.max(0.6, lines(`${q.answer}. ${ans.text}`, full - 1.0, 16, true) * lineH(16) + 0.2);
    const whyH = lines(ans.why + "  " + (q.src || ""), full - 0.5, apt) * lineH(apt) + 0.25;
    const wrongH = (arr) => arr.reduce((h, [L, o]) => h + lines(`**${L}. ${o.text} — **${o.why}`, full - 0.5, apt) * lineH(apt) + 0.07, 0) + 0.5;
    const roomFirst = BOTTOM - TOP - ansH - whyH - 0.3;
    const wrongPages = paginate(wrong, (arr) => wrongH(arr) <= roomFirst);
    const later = wrongPages.length > 1 ? paginate(wrongPages.slice(1).flat(), (arr) => wrongH(arr) <= BOTTOM - TOP) : [];
    const allPages = [wrongPages[0] || [], ...later];
    for (const [pi, pageWrong] of allPages.entries()) {
      s = base(`${kind} · answer`, `Answer ${q.number}: ${q.answer}` + (pi ? " (cont.)" : ""), c.objectives);
      let yy = TOP;
      if (pi === 0) {
        s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: MX, y: yy, w: full, h: ansH, rectRadius: 0.1, fill: { color: T.correctBg }, line: { color: T.correct, width: 1.5 }, objectName: "Correct answer" });
        s.addImage({ data: await icon("FaCheckCircle", T.correct), x: MX + 0.2, y: yy + ansH / 2 - 0.18, w: 0.36, h: 0.36 });
        s.addText([{ text: `${q.answer}. `, options: { bold: true } }, ...richRuns(ans.text, { fontSize: 16, color: T.text, bold: true })], { x: MX + 0.75, y: yy, w: full - 1.0, h: ansH, fontSize: 16, color: T.text, valign: "middle", margin: 0, isTextBox: true });
        yy += ansH + 0.15;
        s.addText([...richRuns(ans.why, { fontSize: apt, color: T.text }), citeRun(q.src || "", apt)], { x: MX + 0.25, y: yy, w: full - 0.5, h: whyH, valign: "top", margin: 0, isTextBox: true, objectName: "Why correct" });
        yy += whyH + 0.15;
      }
      const h = wrongH(pageWrong);
      s.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: MX, y: yy, w: full, h: Math.min(h, BOTTOM - yy), rectRadius: 0.1, fill: { color: T.card }, line: { color: T.card }, objectName: "Why others wrong card" });
      const runs = [{ text: "Why the other choices are wrong", options: { bold: true, fontSize: apt, color: T.wrong, breakLine: true, paraSpaceAfter: 4 } }];
      pageWrong.forEach(([L, o], i) => {
        runs.push({ text: `${L}. ${o.text} — `, options: { bold: true, fontSize: apt, color: T.text } });
        runs.push(...richRuns(o.why, { fontSize: apt, color: T.text }));
        runs[runs.length - 1].options.paraSpaceAfter = 4;
        if (i < pageWrong.length - 1) runs[runs.length - 1].options.breakLine = true;
      });
      s.addText(runs, { x: MX + 0.25, y: yy + 0.12, w: full - 0.5, h: Math.min(h, BOTTOM - yy) - 0.2, valign: "top", margin: 0, isTextBox: true, objectName: "Why others wrong" });
    }
  }
}

// pptxgenjs writes a paragraph-settings tag before every run of a multi-run paragraph; viewers
// then apply the last one (no bullet). Keep only the first, which is where it belongs.
async function fixParagraphs(file) {
  const JSZip = require(require.resolve("jszip", { paths: [require.resolve("pptxgenjs")] }));
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  for (const name of Object.keys(zip.files).filter((n) => /^ppt\/slides\/slide\d+\.xml$/.test(n))) {
    const xml = await zip.file(name).async("string");
    const fixed = xml.replace(/<a:p>([\s\S]*?)<\/a:p>/g, (para, inner) => {
      let seen = false;
      return "<a:p>" + inner.replace(/<a:pPr\b[^>]*\/>|<a:pPr\b[\s\S]*?<\/a:pPr>/g, (m) => (seen ? "" : ((seen = true), m))) + "</a:p>";
    });
    zip.file(name, fixed);
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: "nodebuffer", compression: "DEFLATE" }));
}

(async () => {
  await titleSlide();
  await objectivesSlides();
  await aboutSlides();
  await roadmapSlide();
  for (const [i, c] of content.classes.entries()) {
    await dividerSlide(c, i);
    await sectionSlides(c);
    await figureSlides(c);
    await conflictSlides(c);
    await comparisonSlides(c);
    await hookSlides(c);
    await highYieldSlides(c);
    await questionSlides(c);
  }
  await pres.writeFile({ fileName: outPath });
  await fixParagraphs(outPath);
  await applyTheme(outPath, { name: `Study deck ${themeName}`, colors: T.officeTheme });
  console.log(`  deck: ${slideNo} slides -> ${outPath}`);
})().catch((e) => { console.error(e); process.exit(1); });
