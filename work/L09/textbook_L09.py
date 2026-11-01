"""Textbook (Katzung 16e — Ch. 15 Diuretic Agents and Ch. 3 rational dosing) additions for L09.
Ch. 3 time-course and absorption sections were taught in Unit 1 (L02); Session 2 (L10) builds on this chapter for RAAS and CKD."""

DOSE = "Renal Dosing & Diuretic Sites"
LT = "Loop & Thiazide Diuretics"
KS = "Potassium-Sparing, CAI & Osmotic Diuretics"

ADD = {
    DOSE: {
        "moa": [
            ("Renal tubule transport mechanisms: the proximal tubule reabsorbs about 66% of Na⁺ and 85% of NaHCO₃; organic acid secretion there delivers most diuretics to their luminal site.", "p. 262; p. 263"),
            ("Collecting tubule system: only 2–5% of NaCl, but where aldosterone acts and K⁺ is secreted; upstream diuretics deliver more Na⁺ here — the basis of diuretic K⁺ wasting.", "p. 264; p. 265"),
            ("Renal autacoids: adenosine (A1) lowers GFR; prostaglandins (PGE2) aid loop action; natriuretic peptides (nesiritide) and urodilatin cause natriuresis but have a limited clinical role.", "p. 266"),
        ],
        "pk": [
            ("Pharmacokinetics in two numbers: volume of distribution links amount in the body to concentration; clearance links elimination rate to concentration.", "p. 43"),
            ("Maintenance dose = clearance × target concentration (steady state depends only on clearance); loading dose = volume of distribution × target concentration, given slowly IV.", "p. 51; p. 52"),
            ("Drug accumulation: doses repeated more often than every four half-lives accumulate; steady state takes about four half-lives.", "p. 47; p. 48"),
        ],
        "monitoring": [
            ("Distribution & clearance: adjust a renally cleared drug in proportion to creatinine clearance (Cockcroft-Gault; women 85% of the calculated value).", "p. 55"),
            ("The target concentration strategy: choose a target, predict V and CL from weight and renal function, dose, measure the response, revise, repeat.", "p. 53"),
            ("Dosing history: without it a drug level loses its predictive value; draw digoxin at least 6 hours after a dose.", "p. 54; p. 55"),
        ],
        "pearls": [
            ("Textbook case: 85-year-old, 60 kg, CrCl 22 mL/min — digoxin clearance falls to 3.7 L/h, so about 127 mcg/day: two 62.5-mcg tablets.", "p. 42; p. 56"),
        ],
    },
    LT: {
        "moa": [
            ("Loops work from the lumen, so their effect tracks proximal secretion; NSAIDs and probenecid compete and reduce it. NSAIDs also blunt the PGE2 contribution.", "p. 269; p. 270"),
        ],
        "pk": [
            ("Furosemide lasts 2–3 hours; torsemide 4–6 hours and absorbs in 1 hour, nearly as completely as IV. Torsemide is mainly cleared by the liver.", "p. 269"),
            ("Chemistry & pharmacokinetics: all thiazides are sulfonamides given orally; chlorothiazide is the only parenteral thiazide.", "p. 271"),
        ],
        "indications": [
            ("Hypercalcemia: normal saline plus IV furosemide (80–120 mg) — a loop alone causes volume contraction and stops working.", "p. 280"),
            ("Nephrolithiasis: thiazide plus more fluid and less salt; do not restrict dietary calcium.", "p. 280"),
            ("Diabetes insipidus (nephrogenic, including lithium-induced): thiazides reduce polyuria; amiloride blocks lithium entry; monitor lithium levels.", "p. 280"),
            ("Nonedematous states, hypertension: chlorthalidone lowers BP more than HCTZ but has more adverse effects; loops reserved for GFR < 30–40 mL/min or heart failure.", "p. 280"),
        ],
        "adverse": [
            ("Thiazide hyperglycemia occurs at HCTZ > 50 mg/d, not at 12.5 mg/d or less; correcting hypokalemia partly reverses it.", "p. 272"),
            ("Thiazides are the diuretics most associated with gout and cause hypomagnesemia more than loops; loop ototoxicity is usually reversible.", "p. 271; p. 272; p. 273"),
            ("Risk of hyponatremia with different diuretic classes: thiazides highest (elderly women); loops protective (odds ratio 0.61).", "p. 272; p. 281"),
        ],
        "interactions": [
            ("Diuretic combinations: loop agents and thiazides (often metolazone) are synergistic in loop resistance — but cause large fluid shifts and K⁺ wasting.", "p. 277"),
        ],
        "pearls": [
            ("Edematous states, heart failure: loops are standard, but overdiuresis cuts preload and cardiac output; hypokalemia worsens arrhythmias and digitalis toxicity.", "p. 278"),
            ("Kidney disease and renal failure: little benefit below GFR 5 mL/min; high-dose loops or loop plus metolazone treat overload; avoid acetazolamide.", "p. 278; p. 279"),
            ("Textbook case: HCTZ added to chronic furosemide in CKD → 15 kg lost, BP 91/58, creatinine 10.8 — hypovolemic AKI; monitor closely, ideally inpatient.", "p. 261; p. 285"),
        ],
    },
    KS: {
        "indications": [
            ("Potassium-sparing diuretics fit mineralocorticoid excess: primary (Conn syndrome) or secondary hyperaldosteronism (heart failure, cirrhosis, nephrotic syndrome).", "p. 274"),
            ("Hepatic cirrhosis: resistant to loops but unusually responsive to spironolactone; aggressive diuresis risks hepatorenal syndrome and encephalopathy.", "p. 279"),
            ("Renal & cardiac protection: aldosterone antagonists are cardioprotective and lower albuminuria; finerenone slowed CKD in type 2 diabetes.", "p. 281"),
            ("Idiopathic edema (women 20–30): rule out surreptitious diuretic use; prefer moderate salt restriction.", "p. 279"),
        ],
        "adverse": [
            ("K⁺-sparing agents can cause hyperchloremic metabolic acidosis (like type IV RTA); triamterene can cause kidney stones and, with indomethacin, acute renal failure.", "p. 275"),
            ("Acetazolamide: drowsiness, paresthesias, calcium phosphate stones, hyperammonemia in cirrhosis; monitor potassium and phosphorus.", "p. 268"),
            ("Mannitol: early ECF expansion and hyponatremia, later dehydration, hypernatremia and hyperkalemia; AKI in 6–7% of patients.", "p. 276"),
        ],
        "interactions": [
            ("Strong CYP3A4 inhibitors (erythromycin, fluconazole, diltiazem, grapefruit juice) raise eplerenone but not spironolactone levels.", "p. 275"),
            ("RALES showed spironolactone helps severe heart failure on an ACE inhibitor — afterward hyperkalemia admissions and deaths rose.", "p. 275"),
        ],
        "pk": [
            ("Acetazolamide diuresis fades within 2–3 days (reduce dose in renal insufficiency); mannitol must be given IV — orally it causes osmotic diarrhea.", "p. 268; p. 275"),
        ],
        "pearls": [
            ("SGLT2 inhibitors block proximal glucose and Na⁺ reabsorption; main indication now cardiorenal protection. Adverse reactions: sixfold genital fungal infections in women, initial GFR dip.", "p. 268; p. 269"),
            ("Antidiuretic hormone antagonists (vaptans): oral tolvaptan (V2), IV conivaptan (V1a and V2) for SIADH when water restriction fails; watch sodium and liver tests.", "p. 276; p. 277"),
        ],
    },
}

CONFLICTS = {
    LT: [
        {"topic": "Thiazide efficacy in advanced CKD",
         "slides": {"text": "Thiazides lose efficacy below GFR ~30 mL/min; switch to a loop.", "src": "S12; S15"},
         "textbook": {"text": "The exact GFR cutoff is debated; chlorthalidone still lowered BP in stage 4 CKD.", "src": "p. 279; p. 280"}},
        {"topic": "Hypomagnesemia",
         "slides": {"text": "Listed as a loop adverse effect.", "src": "S10"},
         "textbook": {"text": "More likely with thiazides than with loops.", "src": "p. 273"}},
    ],
    KS: [
        {"topic": "Mannitol dose for raised ICP/IOP",
         "slides": {"text": "0.25–1 g/kg IV over 30–60 minutes.", "src": "S37"},
         "textbook": {"text": "1–2 g/kg IV.", "src": "p. 275"}},
    ],
}

DISCREPANCIES = [
    ("**Thiazide GFR cutoff:** slides teach about 30 mL/min (switch to a loop); the textbook says the exact cutoff is debated. For the exam, use 30.", "S15; p. 279"),
    ("**Hypomagnesemia:** slides list it under loops; the textbook says it is more likely with thiazides. Both classes can cause it.", "S10; p. 273"),
    ("**Chlorthalidone half-life:** profile says 40–60 hours; textbook table says 50–60 hours. Either way, the longest-acting thiazide.", "S31; p. 281"),
    ("**Mannitol dose:** profile 0.25–1 g/kg; textbook 1–2 g/kg. Use the slide dose.", "S37; p. 275"),
]

CRAM = [
    ("Maintenance vs. loading dose", "Maintenance = CL × target · loading = V × target", "p. 51; p. 52"),
    ("Steady state", "About four half-lives", "p. 47"),
    ("Hypercalcemia regimen", "Normal saline + IV furosemide 80–120 mg", "p. 280"),
    ("Loop resistance", "Add metolazone (loop + thiazide synergy); watch K⁺", "p. 277"),
    ("Cirrhotic ascites", "Spironolactone (loops resisted)", "p. 279"),
    ("Eplerenone + CYP3A4 inhibitors", "Levels rise; spironolactone unaffected", "p. 275"),
    ("SIADH, water restriction failed", "Tolvaptan (oral V2) or conivaptan (IV)", "p. 276"),
    ("SGLT2 inhibitors", "Cardiorenal protection; genital fungal infections", "p. 268; p. 269"),
]

QUESTIONS = [
    dict(topic=LT, kind="vignette",
         stem="A patient with CKD on furosemide 80 mg twice daily has hydrochlorothiazide 25 mg added. Two weeks later he has lost 15 kg, BP is 91/58 and creatinine is 10.8. What happened?",
         correct="Loop–thiazide synergy caused hypovolemic AKI",
         why_correct="Adding a thiazide to chronic loop therapy can cause dramatic diuresis, hypovolemia and AKI; monitor very closely, ideally inpatient (p. 277; p. 285).",
         distractors=[("Thiazide failed, so fluid built up", "He lost 15 kg (p. 285)."),
                      ("Hyperkalemia from the thiazide", "Thiazides waste K⁺ (p. 272)."),
                      ("Ototoxicity from the furosemide", "Not the picture (p. 285)."),
                      ("Thiazide-induced hypercalcemia", "Not the cause of AKI here (p. 285).")],
         src="p. 261; p. 277; p. 285"),
    dict(topic=LT, kind="mechanism",
         stem="Why must saline be given with furosemide to treat hypercalcemia?",
         correct="Volume loss boosts proximal Ca²⁺ reabsorption",
         why_correct="A loop alone causes volume contraction, which enhances proximal Ca²⁺ reabsorption and stops the calcium diuresis; give saline with it (p. 280).",
         distractors=[("Saline blocks NKCC2 with the loop", "Saline replaces volume (p. 280)."),
                      ("Furosemide raises calcium without saline", "It lowers calcium (p. 280)."),
                      ("Saline prevents loop ototoxicity in the ear", "Not the reason (p. 280)."),
                      ("Saline lowers PTH secretion directly", "Not the reason (p. 280).")],
         src="p. 280"),
    dict(topic=KS, kind="vignette",
         stem="A patient with SIADH stays hyponatremic despite fluid restriction at home. Which drug does the textbook use next?",
         correct="Tolvaptan (oral V2 blocker)",
         why_correct="ADH antagonists are used for SIADH when water restriction fails; tolvaptan is oral, conivaptan IV (p. 276).",
         distractors=[("Hydrochlorothiazide (thiazide)", "Thiazides cause hyponatremia (p. 272)."),
                      ("Spironolactone (MR blocker)", "Not an ADH antagonist (p. 273)."),
                      ("Desmopressin (ADH agonist)", "An ADH agonist (p. 280)."),
                      ("Mannitol (given orally)", "Oral mannitol causes diarrhea (p. 275).")],
         src="p. 276"),
]

COMPARISONS = {
    KS: [
        {"title": "Other renal agents in the reading (textbook)", "columns": ["Drug / group", "Mechanism", "Point"],
         "rows": [["SGLT2 inhibitors (dapagliflozin, empagliflozin, canagliflozin)", "Block proximal Na⁺/glucose cotransport", "Cardio- and renoprotective; genital fungal infections"],
                  ["Finerenone", "Nonsteroidal mineralocorticoid antagonist", "Less hyperkalemia (2.8%); slows diabetic CKD"],
                  ["Metolazone", "Thiazide-like", "Added to loops for synergy; start 2.5 mg weekly"],
                  ["Ethacrynic acid", "Loop, not a sulfonamide", "Option for true sulfa allergy"],
                  ["Tolvaptan / conivaptan", "V2 / V1a+V2 ADH antagonists", "SIADH, heart-failure hyponatremia; liver tests"],
                  ["Dorzolamide, brinzolamide", "Topical carbonic anhydrase inhibitors", "Glaucoma without systemic effects"]],
         "src": "p. 267; p. 268; p. 273; p. 276; p. 277; p. 281"},
    ],
}

DEEPER = {
    DOSE: (3, 51, 56, "Maintenance and loading dose maths, target concentration, and the digoxin case"),
    LT: (15, 269, 273, "Loop and thiazide pharmacology in full"),
    KS: (15, 273, 282, "Potassium-sparing, osmotic and ADH-antagonist agents, and diuretics by disease"),
}

_L02 = ["Rate of Absorption", "Extraction Ratio & the First-Pass Effect", "THE TIME COURSE OF DRUG EFFECT", "Immediate Effects",
        "Delayed Effects", "Schedule-Dependent Effects", "Conc Effect", "Cumulative Effects"]

READING_SKIP = (
    [{"heading": h, "reason": "Taught in L02 (Unit 1 pharmacokinetics, Ch. 3); not part of renal dose adjustment"} for h in _L02]
    + [{"heading": "Drug Usual Oral Dosage", "reason": "Table column heading (dosage table); the doses are in the drug profiles"},
       {"heading": "UREARETICS", "reason": "Beyond PA scope: investigational urea-transport blockers still in preclinical studies, no prescribing decision"}]
)
