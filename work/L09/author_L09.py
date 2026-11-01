"""Authoring source for L09 content.json. Run: python3 author_L09.py"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import profiles as PR  # noqa: E402


def F(text, src, tb=False, sg=False):
    d = {"text": text, "src": src}
    if tb:
        d["tb"] = True
    if sg:
        d["sg"] = True
    return d


def Q(kind, stem, correct, why_correct, distractors, src, from_slides=None):
    q = {"kind": kind, "stem": stem, "correct": correct, "why_correct": why_correct,
         "distractors": [{"text": t, "why": w} for t, w in distractors], "src": src}
    if from_slides:
        q["from_slides"] = from_slides
    return q


PROF = {p["slide"]: p for p in PR.read("L09")}


def prof(*slides):
    return [PROF[s] for s in slides]


objectives = [
    {"id": "IO5.1", "src": "Syllabus", "text": "Identify major pharmacologic classes used in the management of renal conditions and describe their mechanisms of action."},
    {"id": "IO5.2", "src": "Syllabus", "text": "Describe the indications, contraindications, adverse effects, and clinically significant interactions associated with medications used to treat renal conditions."},
    {"id": "IO5.3", "src": "Syllabus", "text": "Compare pharmacologic agents within and across therapeutic classes to distinguish clinically relevant differences in efficacy, safety, and use."},
    {"id": "IO5.4", "src": "Syllabus", "text": "Select appropriate pharmacologic therapy for common renal conditions based on clinical presentation and patient-specific factors."},
    {"id": "IO5.5", "src": "Syllabus", "text": "Identify appropriate dosing, administration, and monitoring considerations for medications used in renal conditions."},
    {"id": "IO5.6", "src": "Syllabus", "text": "Explain important medication-use and safety information to patients receiving pharmacotherapy for renal."},
    {"id": "SO1", "src": "S2", "text": "Identify the major pharmacologic classes used in the management of renal conditions — diuretics — and describe their mechanisms of action at specific nephron sites."},
    {"id": "SO2", "src": "S2", "text": "Apply basic pharmacokinetic principles to drug dosing in renal impairment, including creatinine clearance/GFR-based dose and interval adjustment."},
    {"id": "SO3", "src": "S2", "text": "Describe the indications, contraindications, adverse effects, and clinically significant interactions of loop, thiazide, potassium-sparing, carbonic anhydrase inhibitor, and osmotic diuretics."},
    {"id": "SO4", "src": "S2", "text": "Compare diuretic classes to distinguish clinically relevant differences in efficacy, electrolyte effects, and clinical use."},
    {"id": "SO5", "src": "S2", "text": "Identify dosing, administration, and monitoring considerations, and explain key medication-safety counseling points for patients on diuretic therapy."},
]

about = [
    F("**PA PHARMACOLOGY COURSE · LECTURE 5 · SESSION 1 OF 2** — Renal Pharmacotherapeutics. **Session 1: Renal Physiology, Dosing Principles, and Diuretic Pharmacology  |  Tuesday, November 17  |  8:30–11:00 AM**", "S1"),
    F("Two ideas run through this unit. First, the kidney clears many drugs, so renal function changes dosing. Second, every diuretic works at one specific nephron segment, and that location predicts its effects, its adverse effects and its interactions.", "S1 (notes); S2 (notes)"),
    F("Arc of the session: renal physiology and dosing principles first, then the five diuretic classes organized by where they act along the nephron. Preview: antihypertensive therapy in chronic kidney disease and the cardiovascular-renal overlap continue in Session 2 (Thursday, November 19).", "S2; S2 (notes)"),
    F("Session 2 builds directly on this foundation — RAAS-blocking antihypertensives are, mechanistically, the natural next step after today’s diuretic content.", "S2 (notes)"),
    F("Readings: Katzung chapters 15 (Diuretic Agents) and 3 (Pharmacokinetics & Pharmacodynamics: Rational Dosing and the Time Course of Drug Action) for today; chapters 11 (Antihypertensive Agents) and 12 (Vasodilators & the Treatment of Angina Pectoris) are supplemental for Session 2, not today.", "S3; S3 (notes)"),
    F("Chapter 11 (Antihypertensive Agents) frames hypertension management in chronic kidney disease; Chapter 12 the cardiovascular-renal overlap with angina pharmacology. Both supplemental chapters are covered in Session 2 (Thursday, November 19), not today.", "S3; S3 (notes)"),
    F("Required text: Katzung’s Basic and Clinical Pharmacology, 16th Edition (Todd W. Vanderah, 2024/2025, McGraw-Hill Education; ISBN 1260463303 eBook; AccessMedicine). Pharmacotherapy Principles and Practice (Chisholm-Burns et al., 2022) remains additional support alongside all four chapters.", "S3"),
    F("**Appendix** 1 abbreviation key: PO = by mouth; IV = intravenous; IM = intramuscular; SL = sublingual; BID / TID / QID = two / three / four times daily; ER = extended-release; ICP = intracranial pressure; IOP = intraocular pressure.", "S26; S26 (notes)"),
    F("CKD = chronic kidney disease; AKI = acute kidney injury; GFR = glomerular filtration rate; CrCl = creatinine clearance; ENaC = epithelial sodium channel; ACE = angiotensin-converting enzyme; ARB = angiotensin receptor blocker.", "S26; S26 (notes)"),
    F("MI = myocardial infarction; HF = heart failure; CYP = cytochrome P450; NSAID = nonsteroidal anti-inflammatory drug; CBC = complete blood count. Use these as a study reference.", "S26; S26 (notes)"),
    F("**Appendix** **2: DRUG PROFILE · SUPPORTING** — supporting drugs at a glance, listed for context to explain interactions, not doses.", "S38; S38 (notes)"),
    F("The appendix gives **Formulation, dose, indications, adverse effects, contraindications and toxicity** for each drug. For each, know the dose logic, the key adverse effect, the contraindication that changes decisions and the toxicity you would need to recognize. **Standard adult dosing for teaching; verify against current prescribing information.**", "S26; S26 (notes); S27-37"),
    F("**Original figures in this deck:** Figures 1–7 (Renal Dose Adjustment: Dose, Interval, or Both; Diuretic Sites of Action Along the Nephron; The Na-K-2Cl Cotransporter (NKCC2): Loop Diuretic Target; Thiazides: Distal Tubule NCC Block and Calcium Reabsorption;", "S39"),
    F("Collecting Duct: Aldosterone Blockers vs. ENaC Blockers; Proximal Tubule: Acetazolamide and Mannitol; Diuretic Class Comparison: Natriuretic Potency).", "S39"),
    F("Figures 2, 3 and 7 were generated by the course director using the AI tool Claude to illustrate standard, non-copyrighted pharmacologic concepts; they are original diagrams, not reproduced from Katzung’s Basic and Clinical Pharmacology or any other copyrighted source.", "S39; S39 (notes)"),
    F("Figures 1, 4, 5 and 6 are illustrative AI-generated schematics of standard mechanisms, not reproduced from any copyrighted source. **Reference:** Anthropic. (2026). Claude (Sonnet 5) [Large language model]. https://claude.ai", "S39; S39 (notes)"),
]

# ---------------------------------------------------------------- Part 1: renal dosing & nephron sites
t1 = {
    "name": "Renal Dosing & Diuretic Sites", "template": "drug_class", "objectives": ["SO1", "SO2", "IO5.1", "IO5.5"],
    "sections": {
        "overview": [
            F("**Where diuretics act, and why renal function changes how every drug is dosed.** Renal physiology and pharmacokinetic principles set the dosing logic for everything that follows.", "S4; S4 (notes)"),
            F("**The kidney is a major route of elimination for many drugs and active metabolites — renal function directly determines how long a drug stays in the body.**", "S5"),
            F("Glomerular filtration rate (GFR) and creatinine clearance (CrCl) are the standard measures used to estimate renal drug-elimination capacity.", "S5; S5 (notes)"),
            F("This is foundational Chapter 3 content applied specifically to the renal unit: renal dosing is not a separate topic but the lens through which every drug in this unit (and this course) should be viewed.", "S5 (notes)"),
        ],
        "prototype": [
            F("Digoxin, most antibiotics (e.g., vancomycin, many beta-lactams), many direct oral anticoagulants, metformin, and the diuretics covered later in this session are examples of drugs requiring renal dose adjustment.", "S5; S5 (notes)"),
        ],
        "moa": [
            F("Flow (Figure 1): GFR falls → renally cleared drug or active metabolite accumulates → toxicity.", "S6; S6 (notes)"),
            F("**Figure 2. Original illustrative diagram (not from Katzung): filtrate flows through the proximal tubule, thick ascending limb, distal convoluted tubule, and collecting duct — each diuretic class blocks sodium reabsorption at a different, specific segment.**", "S7"),
            F("Share of filtered sodium reabsorbed: proximal tubule about 65%, thick ascending limb about 25%, distal tubule 5-8%, collecting duct 2-3% — this previews the potency ranking in Figure 7.", "S7 (notes)"),
            F("This nephron map is the conceptual spine of the session — every diuretic class is anchored back to its segment.", "S7 (notes)"),
            F("Match each diuretic class to the nephron segment where it acts: loop diuretics (furosemide) — thick ascending limb; thiazide diuretics (hydrochlorothiazide) — distal convoluted tubule.", "SG U5-R2; SG U5-M"),
            F("Potassium-sparing — aldosterone antagonists (spironolactone) and ENaC blockers (amiloride) — collecting duct; carbonic anhydrase inhibitors (acetazolamide) — proximal tubule; osmotic diuretics (mannitol) — throughout.", "SG U5-R2; SG U5-M"),
            F("CAI — proximal tubule; osmotic — acts osmotically throughout the filtrate-containing segments, mainly the proximal tubule and descending limb.", "SG U5-R2; SG U5-M"),
        ],
        "indications": [
            F("Three levers: reduce the dose, extend the dosing interval, or both — the specific approach depends on the drug. Reduced GFR makes a renally cleared drug accumulate if unadjusted.", "S6; S8; SG U5-R1"),
            F("Reduce the maintenance dose when the drug’s effect is concentration-dependent; extend the dosing interval when the drug has a long half-life; monitor for toxicity after each dose change.", "S6"),
            F("Loading doses are often unchanged; maintenance doses are what get adjusted.", "S6 (notes); S8"),
        ],
        "adverse": [
            F("As GFR falls, renally cleared drugs accumulate — dosing must be adjusted by reducing the dose, extending the interval, or both.", "S5"),
            F("Active or toxic metabolites that are renally cleared matter just as much as the parent drug.", "S8"),
        ],
        "contra": [],
        "interactions": [
            F("**Renal impairment also raises drug-interaction risk — drugs that are individually safe can become dangerous in combination when renal clearance is already reduced (a theme that returns explicitly in Session 2's \"triple whammy\" discussion).**", "S5"),
        ],
        "pk": [],
        "monitoring": [
            F("Check creatinine clearance before dosing any renally cleared drug (lower maintenance dose, extend the interval, or check CrCl) — especially in older adults.", "S6; S8"),
            F("Reassess as renal function changes — acute illness, dehydration, or new nephrotoxic drugs can drop GFR quickly.", "S8; S8 (notes)"),
            F("When in doubt, consult dosing references or clinical pharmacy — this is not a \"memorize every number\" exercise; the point is the habit of checking renal function before dosing.", "S8; S8 (notes)"),
        ],
        "pearls": [
            F("Renal function determines drug dosing broadly, not just for diuretics — GFR/creatinine clearance should be checked before dosing any renally cleared drug (Chapter 3).", "S25"),
        ],
    },
    "figures": [
        {"image": "S6_1.png", "title": "Figure 1 · Renal dose adjustment: dose, interval, or both", "src": "S6; S6 (notes)",
         "caption": "**Schematic (illustrative)** — Figure 1. Reduced GFR slows clearance, so a renally cleared drug accumulates to higher levels (illustrative schematic). Fixes: lower the maintenance dose, extend the interval, or both; loading doses are often unchanged.",
         "viz": {"type": "pathway", "title": "renal dose adjustment", "h": 170,
                 "point": "Falling GFR means the same dose builds up — pull the dose lever, the interval lever, or both.",
                 "nodes": [{"id": "gfr", "label": "GFR falls", "glyph": "cell", "x": 10, "y": 55, "w": 130, "col": "blue"},
                           {"id": "acc", "label": "Drug or active\nmetabolite builds up", "glyph": "molecule", "x": 165, "y": 55, "w": 170, "col": "amber"},
                           {"id": "tox", "label": "Toxicity", "glyph": "effect", "x": 360, "y": 55, "w": 120, "col": "coral"},
                           {"id": "ok", "label": "Safe level", "glyph": "effect", "x": 505, "y": 55, "w": 125, "col": "sage"}],
                 "edges": [["gfr", "acc"], ["acc", "tox"]],
                 "drugs": [{"label": "Lower the maintenance dose", "at": "acc", "off": ["tox"], "less": [], "note": "Concentration-dependent drugs; loading dose often unchanged (S6; S8)."},
                           {"label": "Extend the interval", "at": "acc", "off": ["tox"], "less": [], "note": "Long half-life drugs; monitor after each change (S6)."},
                           {"label": "Check CrCl first", "at": "gfr", "off": [], "less": ["tox"], "note": "Before any renally cleared drug, especially in older adults (S8)."}],
                 "read": "Pick a lever to see what it prevents."}},
        {"image": "S7_1.jpg", "title": "Figure 2 · Diuretic sites of action along the nephron", "src": "S7; S7 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): filtrate flows left to right through the proximal tubule (~65% of filtered Na⁺), thick ascending limb (~25%), distal convoluted tubule (~5–8%) and collecting duct (~2–3%); each class blocks sodium reabsorption at its own segment, and the share reabsorbed there predicts its potency.",
         "viz": {"type": "pathway", "title": "nephron sites", "h": 170,
                 "point": "Where a diuretic acts predicts how strong it is and which electrolytes it moves.",
                 "nodes": [{"id": "pt", "label": "Proximal tubule\n~65% Na⁺", "glyph": "membrane", "x": 10, "y": 55, "w": 140, "col": "teal"},
                           {"id": "tal", "label": "Thick ascending\nlimb ~25%", "glyph": "membrane", "x": 170, "y": 55, "w": 140, "col": "deep"},
                           {"id": "dct", "label": "Distal tubule\n~5–8%", "glyph": "membrane", "x": 330, "y": 55, "w": 140, "col": "blue"},
                           {"id": "cd", "label": "Collecting duct\n~2–3%", "glyph": "membrane", "x": 490, "y": 55, "w": 140, "col": "coral"}],
                 "edges": [["pt", "tal"], ["tal", "dct"], ["dct", "cd"]],
                 "drugs": [{"label": "Acetazolamide", "at": "pt", "off": [], "less": [], "note": "Blocks Na⁺/HCO₃⁻ reabsorption; weak diuretic (S7; S19)."},
                           {"label": "Mannitol", "at": "pt", "off": [], "less": [], "note": "Osmotic; acts throughout, most prominently here (S7)."},
                           {"label": "Furosemide (loop)", "at": "tal", "off": [], "less": [], "note": "Blocks NKCC2 — the most potent class (S7; S10)."},
                           {"label": "Hydrochlorothiazide", "at": "dct", "off": [], "less": [], "note": "Blocks the Na-Cl cotransporter (S7; S12)."},
                           {"label": "Spironolactone / amiloride", "at": "cd", "off": [], "less": [], "note": "Potassium-sparing (S7; S17)."}],
                 "read": "Pick a drug to see its segment."}},
    ],
    "comparisons": [
        {"title": "Renal dosing: what changes (S8)", "columns": ["What changes", "Practical consideration"],
         "rows": [["Dose, interval, or both — depends on the drug", "Estimate CrCl or eGFR before dosing, especially in older adults"],
                  ["Loading dose often unchanged; maintenance dose adjusted", "Reassess when illness, dehydration or nephrotoxins drop GFR"],
                  ["Renally cleared active/toxic metabolites count too", "Use dosing references or clinical pharmacy"]],
         "src": "S8"},
    ],
    "hooks": [
        {"kind": "why", "text": "Why is the loading dose often unchanged? It fills the volume of distribution, which kidney failure doesn’t shrink much; clearance sets the maintenance dose.", "src": "S8; p. 51; p. 52"},
    ],
    "high_yield": [
        F("Falling GFR → accumulation → toxicity: cut the maintenance dose, stretch the interval, or both; check CrCl first.", "S6; S8; SG U5-R1"),
        F("Sodium reabsorbed: proximal ~65%, loop ~25%, distal 5–8%, collecting duct 2–3%.", "S7 (notes)"),
    ],
    "questions": [
        Q("mechanism", "Why does a falling GFR change how a renally cleared drug must be dosed?",
          "The drug accumulates unless dose or interval is adjusted",
          "Reduced GFR causes a renally cleared drug to accumulate if unadjusted; reduce the dose, extend the interval, or both (S5; SG U5-R1).",
          [("Absorption from the gut falls with GFR", "GFR affects elimination, not absorption (S5)."),
           ("The loading dose must always be doubled", "Loading doses are often unchanged (S8)."),
           ("The drug is cleared faster, so doses rise", "Clearance falls, not rises (S5)."),
           ("Only the parent drug matters, not metabolites", "Active metabolites matter too (S8).")], "S5; S8; SG U5-R1"),
        Q("vignette", "An 80-year-old has pneumonia and dehydration. She takes metformin and a DOAC. What is the best dosing habit?",
          "Re-estimate CrCl now and adjust renally cleared drugs",
          "Acute illness and dehydration can drop GFR quickly; estimate CrCl or eGFR and reassess renally cleared drugs (S8).",
          [("Keep last year’s doses since CrCl is stable", "GFR can fall quickly (S8)."),
           ("Double the loading dose of both drugs", "Loading doses are often unchanged (S8)."),
           ("Stop checking renal function in older adults", "Older adults are the priority (S8)."),
           ("Adjust only the drugs with toxic metabolites", "Parent drugs count too (S8).")], "S5; S8"),
        Q("mechanism", "Roughly what share of filtered sodium does each segment reabsorb, from proximal tubule to collecting duct?",
          "About 65%, 25%, 5–8%, and 2–3%",
          "Proximal tubule ~65%, thick ascending limb ~25%, distal tubule 5–8%, collecting duct 2–3% (S7 notes).",
          [("About 25%, 65%, 2–3%, and 5–8%", "Proximal and loop are swapped (S7)."),
           ("About 5–8%, 25%, 65%, and 2–3%", "The proximal tubule reabsorbs most (S7)."),
           ("About equal at 25% in every segment", "Shares differ by segment (S7)."),
           ("About 2–3%, 5–8%, 25%, and 65%", "Reversed (S7).")], "S7; S7 (notes)"),
    ],
}

# ---------------------------------------------------------------- Part 2: loop & thiazide diuretics
t2 = {
    "name": "Loop & Thiazide Diuretics", "template": "drug_class", "objectives": ["SO1", "SO3", "SO4", "SO5", "IO5.1", "IO5.2", "IO5.3", "IO5.4"],
    "sections": {
        "overview": [
            F("**The two workhorse classes — one for potent natriuresis, one for everyday hypertension control.** They act on the thick ascending limb and the distal tubule.", "S9; S9 (notes)"),
            F("Loops are the most potent class; thiazides are first-line for hypertension.", "S10; S12"),
        ],
        "prototype": [
            F("Furosemide, bumetanide, torsemide: loop diuretics. Hydrochlorothiazide: thiazide; chlorthalidone: thiazide-like.", "S10; S12"),
        ],
        "moa": [
            F("**Mechanism: block the Na-K-2Cl cotransporter (NKCC2) in the thick ascending limb — the site responsible for ~25% of filtered sodium reabsorption.**", "S10"),
            F("**Figure 3. Original illustrative diagram (not from Katzung): loop diuretics block NKCC2 in the thick ascending limb, reducing Na+/Cl-/K+ reabsorption and collapsing the lumen-positive potential that normally drives paracellular calcium and magnesium reabsorption —**", "S11"),
            F("**explaining the increased calcium and magnesium excretion seen with this class.** The lumen-positive potential (from K⁺ recycling) is the link students skip when they memorize “loops cause hypocalcemia” without the why.", "S11; S11 (notes); SG U5-R3"),
            F("**Mechanism: block the Na-Cl cotransporter in the distal convoluted tubule — a less potent natriuretic site (~5–8% of filtered sodium) than the loop.**", "S12"),
            F("Follow the thiazide chain step by step (Figure 4): NCC block in the DCT → sodium and water loss → lower intracellular sodium → calcium retained through the NCX exchanger → falling urinary calcium.", "S13; S13 (notes); SG U5-R3"),
            F("Contrast this with loop diuretics, which raise urinary calcium (Figure 3).", "S13 (notes)"),
            F("In one line: loop diuretics collapse the lumen-positive potential driving paracellular Ca²⁺/Mg²⁺ reabsorption (↑ excretion); thiazides increase distal calcium reabsorption through a separate mechanism (↓ excretion).", "SG U5-R3"),
        ],
        "indications": [
            F("Loops: edema (heart failure, cirrhosis, renal disease) and, at times, hypertension when a thiazide alone is insufficient (e.g., significant renal impairment).", "S10"),
            F("Loop diuretics increase calcium excretion — useful in hypercalcemia, and the opposite effect of thiazides.", "S10; S10 (notes)"),
            F("Hydrochlorothiazide, chlorthalidone — first-line agents for essential hypertension; chlorthalidone has a longer half-life and is often preferred for 24-hour BP control.", "S12"),
            F("Thiazides decrease calcium excretion — can be therapeutically useful in patients with osteoporosis and recurrent calcium-containing kidney stones.", "S12; S13"),
        ],
        "adverse": [
            F("**Adverse effects: hypokalemia, hypomagnesemia, metabolic alkalosis, ototoxicity (especially with rapid IV administration or high doses), and hyperuricemia.**", "S10"),
            F("**Adverse effects: hyponatremia (can be significant, especially in older adults), hypokalemia, hyperglycemia, hyperuricemia (can precipitate gout), and hypercalcemia.**", "S12"),
            F("Loops carry greater risk of ototoxicity and more pronounced electrolyte shifts than thiazides.", "S14"),
            F("Thiazides: hyponatremia, gout, and hypokalemia are common adverse effects.", "S13"),
        ],
        "contra": [
            F("Furosemide carries a sulfonamide-related structure — historical cross-reactivity concern with sulfa allergy, though the clinical risk is now considered low; still worth a careful allergy history.", "S10; S10 (notes)"),
            F("Thiazides lose efficacy as GFR falls below approximately 30 mL/min — loop diuretics are generally preferred once renal function is significantly reduced.", "S12; S13"),
        ],
        "interactions": [
            F("Digoxin: hypokalemia from loops increases toxicity. Aminoglycosides: additive ototoxicity with loops.", "S38; S38 (notes)"),
            F("Lithium: levels rise with thiazides. NSAIDs blunt the diuretic effect and raise AKI risk.", "S38; S38 (notes)"),
        ],
        "pk": [
            F("Chlorthalidone: long half-life of 40-60 hours.", "S31"),
            F("Torsemide: longer half-life and more predictable absorption than furosemide. Bumetanide is about 40 times more potent than furosemide mg for mg.", "S28; S29"),
        ],
        "monitoring": [
            F("Loops: monitor potassium, magnesium, creatinine. Thiazides: monitor sodium, potassium, calcium, glucose.", "S27; S30"),
            F("IV furosemide slowly (no faster than 4 mg/min) — ototoxicity with rapid IV or high doses.", "S27"),
        ],
        "pearls": [
            F("The calcium-handling difference between loops and thiazides is one of the highest-yield comparison points in this whole unit: loops increase Ca2+ excretion, thiazides decrease it — state it both ways.", "S10 (notes); S25; SG U5-R3"),
            F("Case: hypertension and worsening CKD (eGFR now 25 mL/min), well controlled on chlorthalidone for years, but blood pressure has crept up. **What is the most likely explanation, and what change in therapy would you consider?**", "S15"),
            F("**Thiazide diuretics lose much of their natriuretic efficacy once GFR falls below roughly 30 mL/min, because there is too little filtered sodium reaching the distal tubule for the drug to act on meaningfully.**", "S15"),
            F("**A loop diuretic, which acts upstream at the thick ascending limb, remains effective even in advanced CKD and is the more appropriate choice here.**", "S15; S15 (notes)"),
            F("The “thiazides lose efficacy in advanced CKD” point bridges directly to Session 2’s hypertension-in-CKD content.", "S12 (notes)"),
        ],
    },
    "figures": [
        {"image": "S11_1.jpg", "title": "Figure 3 · NKCC2: the loop diuretic target", "src": "S11; S11 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): blocking NKCC2 in the thick ascending limb cuts Na⁺/K⁺/2Cl⁻ reabsorption and collapses the lumen-positive potential (from K⁺ recycling) that drives paracellular Ca²⁺ and Mg²⁺ reabsorption — so loops raise urinary calcium and magnesium.",
         "viz": {"type": "pathway", "title": "loop mechanism", "h": 180,
                 "point": "No lumen-positive potential, no paracellular Ca²⁺/Mg²⁺ pull — so loops waste calcium.",
                 "nodes": [{"id": "nk", "label": "NKCC2 takes up\nNa⁺, K⁺, 2Cl⁻", "glyph": "membrane", "x": 10, "y": 60, "w": 150, "col": "deep"},
                           {"id": "k", "label": "K⁺ recycles\nto lumen", "glyph": "signal", "x": 180, "y": 60, "w": 130, "col": "amber"},
                           {"id": "pot", "label": "Lumen-positive\npotential", "glyph": "signal", "x": 330, "y": 60, "w": 140, "col": "blue"},
                           {"id": "ca", "label": "Ca²⁺, Mg²⁺\nreabsorbed", "glyph": "effect", "x": 490, "y": 60, "w": 140, "col": "sage"}],
                 "edges": [["nk", "k"], ["k", "pot"], ["pot", "ca"]],
                 "drugs": [{"label": "Furosemide", "at": "nk", "off": ["k", "pot", "ca"], "less": [], "note": "↑ Ca²⁺ and Mg²⁺ excretion; useful in hypercalcemia (S10–S11)."},
                           {"label": "Bumetanide / torsemide", "at": "nk", "off": ["k", "pot", "ca"], "less": [], "note": "Same target; bumetanide ~40× furosemide mg for mg (S28)."}],
                 "read": "Pick a loop diuretic to switch NKCC2 off."}},
        {"image": "S13_1.png", "title": "Figure 4 · Thiazides: NCC block and calcium reabsorption", "src": "S13; S13 (notes)",
         "caption": "**Schematic (illustrative)** — Figure 4. Distal convoluted tubule: thiazide block of NCC lowers intracellular sodium, which favors Na⁺/Ca²⁺ exchange (NCX), so more calcium is reabsorbed and urinary calcium falls (illustrative schematic).",
         "viz": {"type": "pathway", "title": "thiazide mechanism", "h": 180,
                 "point": "Lower cell sodium drives the exchanger to pull calcium back — the opposite of loops.",
                 "nodes": [{"id": "ncc", "label": "NCC in the DCT", "glyph": "membrane", "x": 10, "y": 60, "w": 140, "col": "blue"},
                           {"id": "na", "label": "Cell Na⁺ falls", "glyph": "molecule", "x": 170, "y": 60, "w": 140, "col": "amber"},
                           {"id": "ncx", "label": "NCX pulls\nmore Ca²⁺ in", "glyph": "membrane", "x": 330, "y": 60, "w": 140, "col": "teal"},
                           {"id": "uca", "label": "Urinary Ca²⁺\nfalls", "glyph": "effect", "x": 490, "y": 60, "w": 140, "col": "sage"}],
                 "edges": [["ncc", "na"], ["na", "ncx"], ["ncx", "uca"]],
                 "drugs": [{"label": "Hydrochlorothiazide", "at": "ncc", "off": [], "less": [], "note": "Calcium stones, osteoporosis; loses efficacy at GFR < 30 (S12–S13)."},
                           {"label": "Chlorthalidone", "at": "ncc", "off": [], "less": [], "note": "Same site, longer action (40–60 h) (S24; S31)."}],
                 "read": "Pick a thiazide to follow the calcium chain."}},
    ],
    "comparisons": [
        {"title": "Loop vs. thiazide diuretics (S14)", "columns": ["", "Loop diuretics", "Thiazide diuretics"],
         "rows": [["Site, potency", "Thick ascending limb — most potent natriuresis (~25%)", "Distal convoluted tubule — modest natriuresis (~5–8%)"],
                  ["Calcium", "Increase Ca²⁺ excretion", "Decrease Ca²⁺ excretion"],
                  ["Best use", "Preferred in edematous states and advanced CKD", "First-line for essential hypertension with preserved renal function"],
                  ["Watch for", "Greater risk of ototoxicity, more pronounced electrolyte shifts", "Lose efficacy as GFR falls below ~30 mL/min"]],
         "src": "S14; SG U5-R4"},
        *PR.table(prof(27, 28, 29), "Loop diuretic profiles"),
        *PR.table(prof(30, 31), "Thiazide profiles"),
    ],
    "hooks": [
        {"kind": "why", "text": "Why do thiazides fail at eGFR 25? Too little filtered sodium reaches the distal tubule; a loop acts upstream where the sodium still is.", "src": "S15"},
        {"kind": "mnemonic", "text": "Loops Lose calcium; Thiazides Take it back.", "src": "S10; S12; SG U5-R3"},
    ],
    "high_yield": [
        F("Loop = NKCC2, thick ascending limb, most potent, ↑ Ca²⁺ excretion, ototoxicity. Thiazide = NCC, DCT, first-line HTN, ↓ Ca²⁺ excretion.", "S14; SG U5-R3; SG U5-R4"),
        F("Thiazides fade below GFR ~30 → switch to a loop.", "S15; SG U5-R4"),
    ],
    "questions": [
        Q("vignette", "A patient with hypertension and eGFR now 25 mL/min has crept up in BP despite years on chlorthalidone. What is the best change?",
          "Switch to a loop diuretic",
          "Thiazides lose much of their efficacy below GFR ~30 because too little sodium reaches the distal tubule; a loop acts upstream and still works (S15).",
          [("Double the chlorthalidone dose", "The site has too little filtered sodium (S15)."),
           ("Add hydrochlorothiazide to chlorthalidone", "Same failing site (S15)."),
           ("Switch to acetazolamide", "Weak; avoided in kidney disease (S19; p. 279)."),
           ("Stop diuretics altogether", "A loop remains effective (S15).")], "S15; SG U5-R4", from_slides="S15"),
        Q("mechanism", "Why do loop diuretics increase calcium excretion while thiazides decrease it?",
          "Loops collapse lumen potential; thiazides aid NCX",
          "Loops collapse the lumen-positive potential driving paracellular Ca²⁺/Mg²⁺ reabsorption; thiazides lower cell Na⁺ so NCX reabsorbs more Ca²⁺ (S11; S13; SG U5-R3).",
          [("Loops block calcium channels; thiazides open them", "Not the mechanism (S11; S13)."),
           ("Both raise calcium excretion equally", "Effects are opposite (S14)."),
           ("Loops raise PTH; thiazides suppress PTH", "Not the taught mechanism (S11)."),
           ("Thiazides act on NKCC2; loops act on NCC", "Sites are swapped (S10; S12).")], "S11; S13; SG U5-R3"),
        Q("vignette", "A patient has recurrent calcium kidney stones and hypertension with normal renal function. Which diuretic fits best?",
          "Hydrochlorothiazide (thiazide)",
          "Thiazides decrease calcium excretion, useful in recurrent calcium stones; first-line HTN with preserved renal function (S12; S30).",
          [("Furosemide (loop diuretic)", "Increases calcium excretion (S10)."),
           ("Acetazolamide (CA inhibitor)", "Kidney stones are an adverse effect (S36)."),
           ("Mannitol (osmotic diuretic)", "IV osmotic agent for ICP/IOP (S37)."),
           ("Bumetanide (loop diuretic)", "Loop; raises urinary calcium (S10).")], "S12; S30"),
        Q("vignette", "A patient with heart failure on digoxin starts high-dose furosemide. Which lab change most raises digoxin toxicity risk?",
          "Hypokalemia",
          "Hypokalemia from loops increases digoxin toxicity (S38).",
          [("Hyperkalemia", "Loops lower potassium (S10)."),
           ("Hypercalcemia", "Loops increase calcium excretion (S10)."),
           ("Hyponatremia", "Not the digoxin link (S38)."),
           ("Metabolic acidosis", "Loops cause alkalosis (S10).")], "S10; S38"),
        Q("mechanism", "Which adverse effect is most characteristic of loop diuretics given rapidly IV at high doses?",
          "Ototoxicity",
          "Ototoxicity, especially with rapid IV administration or high doses; give IV furosemide no faster than 4 mg/min (S10; S27).",
          [("Gynecomastia", "Spironolactone (S17)."),
           ("Hyperkalemia", "Potassium-sparing class (S17)."),
           ("Metabolic acidosis", "Acetazolamide (S19)."),
           ("Hypercalcemia", "Thiazides (S12).")], "S10; S27"),
        Q("vignette", "An older woman on hydrochlorothiazide is confused, with sodium 122 mEq/L. Which statement fits?",
          "Thiazide hyponatremia, especially in older adults",
          "Hyponatremia can be significant with thiazides, especially in older adults (S12).",
          [("Loop diuretics cause more hyponatremia than thiazides", "Thiazides do (S12; p. 271)."),
           ("Thiazides raise sodium by blocking ADH", "They lower sodium (S12)."),
           ("Hyperkalemia explains the confusion", "Thiazides lower potassium (S12)."),
           ("This is mannitol-type osmotic diuresis", "Not an osmotic agent (S19).")], "S12; S30"),
    ],
}

# ---------------------------------------------------------------- Part 3: K-sparing, CAI, osmotic
t3 = {
    "name": "Potassium-Sparing, CAI & Osmotic Diuretics", "template": "drug_class", "objectives": ["SO1", "SO3", "SO4", "SO5", "IO5.1", "IO5.2", "IO5.3", "IO5.4", "IO5.6"],
    "sections": {
        "overview": [
            F("**Smaller in potency, but each with a distinct and important clinical niche.** Potassium-sparing, carbonic anhydrase inhibitor and osmotic diuretics act on the collecting duct and the proximal tubule.", "S16; S16 (notes)"),
            F("**Two mechanistically distinct subgroups acting at the collecting duct, both reducing potassium and hydrogen ion secretion.**", "S17"),
        ],
        "prototype": [
            F("Spironolactone, eplerenone: aldosterone receptor antagonists. Amiloride, triamterene: epithelial sodium channel (ENaC) blockers.", "S17"),
            F("Carbonic anhydrase inhibitor: acetazolamide. Osmotic diuretic: mannitol.", "S19"),
        ],
        "moa": [
            F("Aldosterone binds the mineralocorticoid receptor → increases ENaC and Na/K pump activity → K+ and H+ secreted into the tubule. Blocking either step reduces potassium and hydrogen secretion.", "S18; S18 (notes)"),
            F("Spironolactone and eplerenone block the receptor (block aldosterone’s effect directly); amiloride and triamterene block ENaC directly, independent of aldosterone.", "S17; S18; S18 (notes)"),
            F("**Acetazolamide (carbonic anhydrase inhibitor):** blocks Na+/HCO3- reabsorption in the proximal tubule → less HCO3- reabsorbed → bicarbonate diuresis, metabolic acidosis; weak diuretic effect.", "S19; S20; SG U5-R6"),
            F("**Mannitol (osmotic diuretic):** an inert, filtered but poorly reabsorbed solute that holds water in the tubule lumen osmotically — osmotic diuresis.", "S19; S20"),
            F("Side by side: acetazolamide removes bicarbonate reabsorption; mannitol removes water reabsorption by staying in the lumen. Both act before the loop, so their natriuretic potency is modest.", "S20 (notes)"),
            F("Figure 6 (**Schematic (illustrative)**): proximal tubule — carbonic anhydrase inhibition and osmotic holding of water (illustrative schematic).", "S20"),
            F("**Figure 7. Original illustrative comparison (illustrative values, not from Katzung): loop diuretics block roughly 25% of filtered sodium reabsorption, substantially more than thiazides, carbonic anhydrase inhibitors, or potassium-sparing diuretics —**", "S21"),
            F("**directly reflecting the percentage normally reabsorbed at each nephron segment in Figure 2.** This is why loops are reached for first when potent natriuresis is the goal.", "S21; S21 (notes)"),
        ],
        "indications": [
            F("Potassium-sparing agents are often used in combination with a loop or thiazide diuretic specifically to offset potassium loss from the more potent class.", "S17"),
            F("Acetazolamide: valued for non-diuretic uses — glaucoma (reduces aqueous humor production), altitude sickness prophylaxis, and metabolic alkalosis correction; also raised intracranial pressure.", "S19; S20"),
            F("Mannitol: used to reduce elevated intracranial or intraocular pressure and in certain cases of rhabdomyolysis-associated kidney injury prevention.", "S19"),
            F("Know the niche, not an everyday use: acetazolamide = glaucoma/altitude sickness; mannitol = ICP/IOP reduction.", "S19 (notes)"),
        ],
        "adverse": [
            F("**Primary adverse effect across the class: hyperkalemia — the risk rises sharply when combined with ACE inhibitors, ARBs, or in renal impairment (a direct preview of Session 2's cardiorenal drug-interaction content).**", "S17; SG U5-R5"),
            F("Spironolactone also has antiandrogen effects (gynecomastia, menstrual irregularities) that eplerenone largely avoids.", "S17"),
            F("Acetazolamide causes a mild metabolic acidosis as a predictable adverse effect, plus potassium loss; watch for kidney stones.", "S19; S20"),
            F("Mannitol expands extracellular volume — can worsen volume overload if used inappropriately; avoid it in heart failure and volume depletion.", "S19; S20"),
        ],
        "contra": [
            F("Mannitol requires intact renal perfusion to be effective.", "S19; S20 (notes)"),
            F("Eplerenone: avoid with potassium above 5.5 mEq/L, CrCl below 30 mL/min, or strong CYP3A4 inhibitors (such as ketoconazole).", "S33"),
        ],
        "interactions": [
            F("Hyperkalemia risk rises with ACE inhibitors, ARBs, or CKD — both block aldosterone’s effect, so the classes are combined carefully.", "S18; S18 (notes)"),
            F("Flag the hyperkalemia-with-ACEi/ARB interaction as a preview: this exact combination becomes a major theme in Session 2 when RAAS blockers are introduced.", "S17 (notes)"),
            F("Potassium supplements and trimethoprim: hyperkalemia with potassium-sparing diuretics.", "S38; S38 (notes)"),
            F("Sulfonamide allergy: caution with loops, thiazides, acetazolamide. Metformin, vancomycin, DOACs: renally cleared; need dose adjustment.", "S38; S38 (notes)"),
        ],
        "monitoring": [
            F("Spironolactone: monitor potassium and creatinine within 1 week; life-threatening hyperkalemia, especially in CKD or with ACE inhibitor/ARB.", "S32"),
            F("Mannitol: monitor osmolality and electrolytes.", "S37"),
        ],
        "pearls": [
            F("Case: a patient with stage 3 chronic kidney disease and heart failure is taking an ACE inhibitor and is started on spironolactone for additional heart-failure benefit; two weeks later a routine basic metabolic panel shows potassium 6.1 mEq/L.", "S23"),
            F("**What is the mechanistic explanation for this finding, and what does it suggest about future drug combinations in this unit?**", "S23; S23 (notes)"),
            F("**Both the ACE inhibitor (by reducing aldosterone) and spironolactone (by directly blocking the aldosterone receptor) independently reduce potassium excretion — combined, and in the setting of CKD (which already impairs potassium excretion), the hyperkalemia risk compounds.**", "S23"),
            F("**This is the same additive-risk logic that will reappear as the \"triple whammy\" in Session 2.** The ACEi/aldosterone-antagonist pair is one of three “whammies” formalized next session.", "S23; S23 (notes)"),
        ],
    },
    "figures": [
        {"image": "S18_1.png", "title": "Figure 5 · Collecting duct: aldosterone blockers vs. ENaC blockers", "src": "S18; S18 (notes)",
         "caption": "Schematic (illustrative) — Figure 5. Collecting duct: aldosterone-receptor blockers and ENaC blockers act at different steps (illustrative schematic). One blocks the hormone’s receptor, the other blocks the channel the hormone turns on; both raise potassium.",
         "viz": {"type": "pathway", "title": "collecting duct", "h": 180,
                 "point": "Block the hormone or block the channel — either way, less K⁺ and H⁺ secreted.",
                 "nodes": [{"id": "ald", "label": "Aldosterone binds\nmineralocorticoid R", "glyph": "signal", "x": 10, "y": 60, "w": 170, "col": "amber"},
                           {"id": "enac", "label": "More ENaC and\nNa/K pump", "glyph": "membrane", "x": 200, "y": 60, "w": 150, "col": "blue"},
                           {"id": "k", "label": "K⁺ and H⁺\nsecreted", "glyph": "effect", "x": 370, "y": 60, "w": 130, "col": "coral"},
                           {"id": "hk", "label": "Kept: risk of\nhyperkalemia", "glyph": "effect", "x": 515, "y": 60, "w": 120, "col": "sage"}],
                 "edges": [["ald", "enac"], ["enac", "k"]],
                 "drugs": [{"label": "Spironolactone", "at": "ald", "off": ["enac", "k"], "less": [], "note": "Receptor blocker; antiandrogen effects (gynecomastia) (S17–S18)."},
                           {"label": "Eplerenone", "at": "ald", "off": ["enac", "k"], "less": [], "note": "Selective; fewer antiandrogen effects; CYP3A4 inhibitors raise levels (S17; S33)."},
                           {"label": "Amiloride / triamterene", "at": "enac", "off": ["k"], "less": [], "note": "Block ENaC independent of aldosterone (S17–S18)."}],
                 "read": "Pick a drug to see which step it blocks."}},
        {"image": "S21_1.jpg", "title": "Figure 7 · Diuretic class comparison: natriuretic potency", "src": "S21; S21 (notes)",
         "caption": "Original illustrative comparison (illustrative values, not from Katzung): loops block about 25% of filtered sodium reabsorption, thiazides about 6%, carbonic anhydrase inhibitors about 4%, potassium-sparing diuretics about 2% — the same nephron-segment logic as Figure 2, now quantified.",
         "viz": {"type": "bars", "title": "Natriuretic potency", "yLabel": "Illustrative % of filtered Na⁺ reabsorption blocked",
                 "point": "Need potent natriuresis? Reach for a loop.",
                 "bars": [{"label": "Loop", "value": 25, "col": "deep", "note": "Thick ascending limb — most potent."},
                          {"label": "Thiazide", "value": 6, "col": "blue", "note": "Distal tubule — modest."},
                          {"label": "CAI", "value": 4, "col": "teal", "note": "Proximal, but the rest of the nephron compensates."},
                          {"label": "K⁺-sparing", "value": 2, "col": "sage", "note": "Collecting duct — weakest; spares K⁺."}],
                 "steps": [{"label": "Loop", "pick": 0}, {"label": "Thiazide", "pick": 1}, {"label": "Carbonic anhydrase inhibitor", "pick": 2}, {"label": "Potassium-sparing", "pick": 3}]}},
    ],
    "comparisons": [
        {"title": "Diuretic classes at a glance (Table 1)", "columns": ["Class", "Example agent(s)", "Key teaching point"],
         "rows": [["Loop", "Furosemide, bumetanide, torsemide", "Most potent; blocks NKCC2; ↑ Ca²⁺ excretion; ototoxicity risk"],
                  ["Thiazide", "Hydrochlorothiazide, chlorthalidone", "First-line for HTN; ↓ Ca²⁺ excretion; loses efficacy at low GFR"],
                  ["K⁺-sparing", "Spironolactone, eplerenone, amiloride, triamterene", "Hyperkalemia risk, especially with ACEi/ARB"],
                  ["CAI / Osmotic", "Acetazolamide / mannitol", "Niche uses: glaucoma, altitude sickness / ↑ ICP, ↑ IOP"]],
         "src": "S22; S22 (notes)"},
        {"title": "Figure 6 · Proximal tubule: carbonic anhydrase inhibition and osmotic holding of water (Schematic (illustrative))", "columns": ["", "Acetazolamide", "Mannitol"],
         "rows": [["How", "Blocks carbonic anhydrase → less HCO₃⁻ reabsorbed", "Filtered, not reabsorbed → water held in lumen"],
                  ["Result", "Bicarbonate diuresis, metabolic acidosis", "Osmotic diuresis"],
                  ["Uses", "Glaucoma, altitude sickness, raised intracranial pressure", "Raised ICP or IOP"],
                  ["Watch for", "Metabolic acidosis, potassium loss, kidney stones", "Expands extracellular volume; avoid in heart failure and volume depletion"]],
         "src": "S20; S20 (notes)"},
        {"title": "Drug names reveal the class (S24)", "columns": ["Stem", "Class", "Examples", "Memory aid"],
         "rows": [["-semide", "Loop", "Furosemide, torsemide", "Works at the thick ascending limb; strongest class"],
                  ["-tanide", "Loop", "Bumetanide", "About 40× furosemide potency, mg for mg"],
                  ["-thiazide", "Thiazide", "Hydrochlorothiazide", "Acts at the distal convoluted tubule"],
                  ["-thalidone", "Thiazide-like", "Chlorthalidone", "Same site, longer action"],
                  ["-onolactone / -erenone", "Aldosterone antagonist", "Spironolactone, eplerenone", "Blocks the mineralocorticoid receptor"],
                  ["-ride", "ENaC blocker", "Amiloride", "Blocks the sodium channel directly"],
                  ["-zolamide", "Carbonic anhydrase inhibitor", "Acetazolamide", "Proximal tubule; bicarbonate diuresis"],
                  ["mannitol / -itol", "Osmotic diuretic", "Mannitol", "Filtered, holds water in the lumen"]],
         "src": "S24; S24 (notes)"},
        {"title": "Supporting drugs at a glance (S38)", "columns": ["Drug(s)", "Why it matters here"],
         "rows": [["ACE inhibitors and ARBs", "Hyperkalemia with potassium-sparing diuretics"],
                  ["NSAIDs", "Blunt diuretic effect; raise AKI risk"],
                  ["Lithium", "Levels rise with thiazides"],
                  ["Digoxin", "Hypokalemia from loops increases toxicity"],
                  ["Aminoglycosides", "Additive ototoxicity with loops"],
                  ["Potassium supplements and trimethoprim", "Hyperkalemia with potassium-sparing diuretics"],
                  ["Sulfonamide allergy", "Caution with loops, thiazides, acetazolamide"],
                  ["Metformin, vancomycin, DOACs", "Renally cleared; need dose adjustment"]],
         "src": "S38; S38 (notes)"},
        *PR.table(prof(32, 33, 34, 35), "Potassium-sparing profiles"),
        *PR.table(prof(36, 37), "Acetazolamide and mannitol profiles"),
    ],
    "hooks": [
        {"kind": "why", "text": "Why does ACE inhibitor + spironolactone raise potassium so much? Both cut aldosterone’s effect — one lowers the hormone, the other blocks its receptor — and CKD already limits K⁺ excretion.", "src": "S23"},
        {"kind": "mnemonic", "text": "Stems: **-semide**, **-tanide** loop · **-thiazide**, **-thalidone** distal · **-onolactone / -erenone**, **-ride** collecting duct · **-zolamide** proximal · **mannitol / -itol** osmotic. Read the **Stem**, name the **Class**, recall the **Examples** and the **Memory aid**.", "src": "S24; S24 (notes)"},
    ],
    "high_yield": [
        F("Potassium-sparing: aldosterone antagonists (spironolactone, eplerenone) and ENaC blockers (amiloride, triamterene); hyperkalemia worsens with ACEi/ARB or CKD.", "S17; SG U5-R5"),
        F("Acetazolamide = glaucoma, altitude sickness, alkalosis; mannitol = ICP/IOP.", "S19; SG U5-R6"),
    ],
    "questions": [
        Q("vignette", "A stage 3 CKD patient with heart failure on an ACE inhibitor starts spironolactone. Two weeks later K⁺ is 6.1 mEq/L. What explains this?",
          "Both drugs cut aldosterone’s effect, compounded by CKD",
          "The ACE inhibitor lowers aldosterone and spironolactone blocks its receptor; both reduce K⁺ excretion, and CKD compounds it (S23).",
          [("Spironolactone blocks NKCC2 in the loop", "It blocks the mineralocorticoid receptor (S18)."),
           ("ACE inhibitors raise aldosterone and potassium", "They reduce aldosterone (S23)."),
           ("The rise is from acetazolamide-like acidosis", "Not acetazolamide (S23)."),
           ("CKD increases renal potassium excretion", "CKD impairs it (S23).")], "S23; SG U5-R5", from_slides="S23"),
        Q("mechanism", "Which pairing correctly matches a potassium-sparing diuretic to its mechanism?",
          "Amiloride — blocks ENaC directly",
          "Amiloride and triamterene block ENaC; spironolactone and eplerenone block the mineralocorticoid receptor (S17–S18).",
          [("Spironolactone — blocks ENaC directly", "Receptor antagonist (S18)."),
           ("Eplerenone — blocks NKCC2", "Receptor antagonist (S17)."),
           ("Triamterene — blocks aldosterone receptor", "ENaC blocker (S17)."),
           ("Amiloride — inhibits carbonic anhydrase", "That is acetazolamide (S19).")], "S17; S18; SG U5-R5"),
        Q("vignette", "A man needs an aldosterone antagonist for heart failure but developed painful gynecomastia on one before. Which fits?",
          "Eplerenone (selective blocker)",
          "Spironolactone has antiandrogen effects (gynecomastia) that eplerenone largely avoids (S17; S33).",
          [("Spironolactone (higher dose)", "Causes the gynecomastia (S17)."),
           ("Amiloride (ENaC blocker)", "Not an aldosterone receptor blocker (S17)."),
           ("Acetazolamide (CA inhibitor)", "Carbonic anhydrase inhibitor (S19)."),
           ("Hydrochlorothiazide (thiazide)", "Not an aldosterone antagonist (S12).")], "S17; S33"),
        Q("vignette", "A hiker plans a rapid ascent to high altitude next week. Which diuretic is used for prophylaxis?",
          "Acetazolamide, from a day before",
          "Acetazolamide is used for altitude sickness prophylaxis, 125–250 mg BID starting a day before ascent (S19; S36).",
          [("Mannitol, IV at the summit", "IV for raised ICP/IOP (S19)."),
           ("Furosemide, daily during ascent", "Edema, not altitude (S10)."),
           ("Spironolactone, daily for a week", "Heart failure, hyperaldosteronism (S32)."),
           ("Hydrochlorothiazide, once daily", "Hypertension (S12).")], "S19; S36; SG U5-R6"),
        Q("mechanism", "How does mannitol produce diuresis?",
          "It is filtered but not reabsorbed, holding water in the lumen",
          "Mannitol is an inert, filtered but poorly reabsorbed solute that holds water in the tubule lumen osmotically (S19–S20).",
          [("It blocks NKCC2 in the thick ascending limb", "That is a loop (S10)."),
           ("It inhibits carbonic anhydrase in the proximal tubule", "That is acetazolamide (S19)."),
           ("It blocks ENaC in the collecting duct", "That is amiloride (S17)."),
           ("It antagonizes aldosterone at its receptor", "That is spironolactone (S18).")], "S19; S20"),
        Q("vignette", "A patient with decompensated heart failure and raised intracranial pressure is being considered for mannitol. What is the concern?",
          "Mannitol expands ECF volume and can worsen heart failure",
          "Mannitol expands extracellular volume; avoid it in heart failure and volume depletion; needs intact renal perfusion (S19–S20; S37).",
          [("Mannitol causes severe hyperkalemia via ENaC", "Not its mechanism (S20)."),
           ("Mannitol has no effect on fluid status", "It shifts fluid (S20)."),
           ("Mannitol causes ototoxicity like loops", "That is loops (S10)."),
           ("Mannitol is safe because it is inert", "Inert, but volume overload (S19).")], "S19; S20; S37"),
        Q("mechanism", "Which acid–base change is a predictable adverse effect of acetazolamide?",
          "Metabolic acidosis",
          "Blocking carbonic anhydrase causes bicarbonate diuresis and a mild metabolic acidosis (S19–S20).",
          [("Metabolic alkalosis", "Loops and thiazides (S10)."),
           ("Respiratory acidosis", "Not the drug effect (S20)."),
           ("Respiratory alkalosis", "Acetazolamide counters it at altitude (p. 267)."),
           ("No acid–base change", "Acidosis is predictable (S19).")], "S19; S20"),
    ],
}

content = {
    "lecture": {"id": "L09", "title": "Renal Pharmacotherapeutics — Session 1", "date": "Tue, Nov 17, 2026"},
    "textbook_status": "included",
    "objectives": objectives,
    "about": about,
    "classes": [t1, t2, t3],
    "notebooklm": {
        "patient": "a patient with worsening CKD (eGFR 25) whose blood pressure has crept up on chlorthalidone, and a CKD/heart-failure patient on an ACE inhibitor whose potassium reaches 6.1 after spironolactone (the lecture’s cases)",
        "suggested_questions": [
            "Why does falling GFR change dosing, and which lever do you pull?",
            "Walk the nephron from proximal tubule to collecting duct and name the diuretic at each site.",
            "Why do loops raise urinary calcium while thiazides lower it?",
            "Why switch from a thiazide to a loop at eGFR 25?",
            "Compare spironolactone, eplerenone, amiloride and triamterene.",
            "What are the niche uses of acetazolamide and mannitol?",
        ],
    },
    "audit_skip": [
        {"ref": "S1", "starts_with": "Diane", "reason": "instructor name (no names on the site)"},
        {"ref": "S3", "starts_with": "AccessMedicine", "reason": "access link for the textbook"},
        *[{"ref": r, "starts_with": "Section transition", "reason": "section divider"} for r in ("S4", "S9", "S16")],
        {"ref": "S6", "starts_with": "Walk the flow from falling", "reason": "teaching instruction; the flow is Figure 1"},
        {"ref": "S14", "starts_with": "Use this slide", "reason": "teaching instruction"},
        {"ref": "S14", "starts_with": "Students should reproduce", "reason": "teaching instruction"},
        {"ref": "S15", "starts_with": "This case makes", "reason": "teaching instruction"},
        {"ref": "S22", "starts_with": "Use this table", "reason": "teaching instruction"},
        {"ref": "S22", "starts_with": "Close the loop", "reason": "teaching instruction"},
        {"ref": "S21", "starts_with": "Close the loop", "reason": "teaching instruction"},
        {"ref": "S25", "starts_with": "Close Session 1", "reason": "teaching instruction"},
        {"ref": "S26", "starts_with": "Class activity", "reason": "teaching instruction"},
        {"ref": "S26", "starts_with": "Teaching points", "reason": "teaching instruction; the drugs are listed in the profiles"},
        {"ref": "S26", "starts_with": "Bloom", "reason": "teaching instruction; the prompts are rebuilt as practice questions"},
        {"ref": "S6", "starts_with": "This sets up", "reason": "teaching instruction"},
        {"ref": "S11", "starts_with": "Left to right", "reason": "teaching instruction; the walk-through is the Figure 3 interactive"},
        *[{"ref": "S26", "starts_with": w, "reason": "Bloom's teaching prompt; rebuilt as practice questions"} for w in ("Remember", "Understand", "Apply", "Analyze", "Evaluate")],
        {"ref": "S38", "starts_with": "Listed for context", "reason": "slide label (the supporting drugs are in the table)"},
        {"ref": "S39", "starts_with": "This slide documents", "reason": "administrative note on AI-tool citation"},
    ],
}

# Session 1 recap (S25) lives in the last part's pearls
t3["sections"]["pearls"] += [
    F("Recap: diuretic classes are organized by nephron site (Figure 2): loop diuretics (thick ascending limb) are most potent, followed by thiazides (distal tubule), then potassium-sparing and carbonic anhydrase inhibitors.", "S25"),
    F("Recap: loop and thiazide diuretics have opposite effects on calcium excretion (Figure 3); potassium-sparing diuretics carry a hyperkalemia risk that compounds with ACE inhibitors or ARBs.", "S25"),
    F("Session 2 (Thursday, November 19) continues with antihypertensive therapy in chronic kidney disease and the cardiovascular-renal overlap, including vasodilators and angina pharmacology — RAAS blockers and the triple whammy first.", "S25; S25 (notes)"),
]

sys.path.insert(0, str(Path(__file__).parent))
import guide_L09 as G  # noqa: E402
content["guide"] = {"summary": [{"text": t, "src": s} for t, s in G.SUMMARY], "teaser": getattr(G, "TEASER", ""),
                    "cram": [{"prompt": p, "answer": a, "src": s} for p, a, s in G.CRAM], "discrepancies": []}
for _cl in content["classes"]:
    _cl["flows"] = G.FLOWS.get(_cl["name"], [])

import textbook_L09 as TBK  # noqa: E402
_by_name = {cl["name"]: cl for cl in content["classes"]}
for _name, _secs in TBK.ADD.items():
    for _key, _facts in _secs.items():
        _by_name[_name]["sections"].setdefault(_key, [])
        _by_name[_name]["sections"][_key] += [F(t, s, tb=True) for t, s in _facts]
for _cl in [c for c in content["classes"] if "adverse" in c["sections"]]:
    _adv = _cl["sections"]["adverse"]
    _box = lambda f: "boxed" in f["text"].lower()  # noqa: E731
    _cl["sections"]["adverse"] = [f for f in _adv if _box(f)] + [f for f in _adv if not _box(f)]
for _name, _cfs in TBK.CONFLICTS.items():
    _by_name[_name].setdefault("conflicts", []).extend(_cfs)
for _q in TBK.QUESTIONS:
    _q = dict(_q)
    _topic = _q.pop("topic")
    _by_name[_topic]["questions"].append({**Q(**_q), "tb": True})
for _name, _tbls in TBK.COMPARISONS.items():
    _by_name[_name].setdefault("comparisons", []).extend(_tbls)
for _name, (_ch, _a, _b, _why) in TBK.DEEPER.items():
    _by_name[_name]["deeper"] = {"chapter": _ch, "first": _a, "last": _b, "why": _why}
content["guide"]["discrepancies"] = [{"text": t, "src": s} for t, s in TBK.DISCREPANCIES]
content["guide"]["cram"] += [{"prompt": p, "answer": a, "src": s, "tb": True} for p, a, s in TBK.CRAM]

out = Path(__file__).with_name("content.json")
out.write_text(json.dumps(content, indent=1, ensure_ascii=False))
print(f"wrote {out}")
