"""Study-guide extras for L09 (summary, flows, cram sheet). Imported by author_L09.py."""

TEASER = "Today: why falling kidney function changes the dose of almost any drug, and the five diuretic classes mapped to the nephron segment where each acts. Loops versus thiazides, the potassium-sparing pair, and the niche uses of acetazolamide and mannitol."

SUMMARY = [
    ("Falling **GFR** makes renally cleared drugs **accumulate**: check CrCl first, then lower the maintenance dose, extend the interval, or both (loading doses often unchanged).", "S5; S6; S8; SG U5-R1"),
    ("Each diuretic acts at one segment: **CAI/osmotic** proximal tubule, **loop** thick ascending limb, **thiazide** distal tubule, **K⁺-sparing** collecting duct.", "S7; SG U5-R2; SG U5-M"),
    ("**Loops** (NKCC2, ~25%) are most potent and **raise** urinary calcium; **thiazides** (NCC, ~5–8%) are first-line for hypertension and **lower** it.", "S10; S12; S14; SG U5-R3"),
    ("Thiazides fade below **GFR ~30** — switch to a loop.", "S15; SG U5-R4"),
    ("**Spironolactone/eplerenone** block the aldosterone receptor; **amiloride/triamterene** block ENaC; all risk **hyperkalemia**, worse with ACEi/ARB or CKD.", "S17; S23; SG U5-R5"),
    ("**Acetazolamide**: glaucoma, altitude sickness, alkalosis (causes acidosis). **Mannitol**: raised ICP/IOP; avoid in heart failure.", "S19; S20; SG U5-R6"),
]

FLOWS = {
    "Renal Dosing & Diuretic Sites": [
        {"title": "Dosing a renally cleared drug", "steps": ["Estimate CrCl or eGFR", "Is the drug (or active metabolite) renally cleared?", "Concentration-dependent → lower the maintenance dose", "Long half-life → extend the interval", "Reassess when illness, dehydration or nephrotoxins change GFR"], "src": "S6; S8"},
    ],
    "Loop & Thiazide Diuretics": [
        {"title": "Loop or thiazide?", "steps": ["Edema or advanced CKD (GFR < 30)?", "Yes → loop (furosemide, bumetanide, torsemide)", "Essential hypertension, preserved renal function → thiazide", "Calcium stones or osteoporosis → thiazide helps", "Hypercalcemia → loop (with saline)"], "src": "S10; S12; S14; S15; p. 280"},
    ],
    "Potassium-Sparing, CAI & Osmotic Diuretics": [
        {"title": "The hyperkalemia setup", "steps": ["CKD already limits K⁺ excretion", "ACE inhibitor lowers aldosterone", "Spironolactone blocks its receptor", "K⁺ rises (6.1 mEq/L)", "Check K⁺ and creatinine within 1 week"], "src": "S23; S32"},
    ],
}

CRAM = [
    ("Falling GFR", "Accumulation → reduce dose, extend interval, or both", "S5; S6; SG U5-R1"),
    ("Loading vs. maintenance", "Loading often unchanged; maintenance adjusted", "S8"),
    ("Na⁺ reabsorbed by segment", "PT ~65% · TAL ~25% · DCT 5–8% · CD 2–3%", "S7 (notes)"),
    ("Loop target", "NKCC2, thick ascending limb", "S10"),
    ("Loop AEs", "↓K, ↓Mg, alkalosis, ototoxicity, hyperuricemia", "S10"),
    ("Thiazide target", "NCC, distal convoluted tubule", "S12"),
    ("Thiazide AEs", "↓Na (older adults), ↓K, ↑glucose, ↑uric acid, ↑Ca", "S12"),
    ("Calcium", "Loops ↑ excretion · thiazides ↓ excretion", "S14; SG U5-R3"),
    ("Thiazide cutoff", "GFR < ~30 → switch to a loop", "S15; SG U5-R4"),
    ("Chlorthalidone", "Longer half-life (40–60 h), 24-hour BP control", "S12; S31"),
    ("Bumetanide", "About 40× furosemide mg for mg", "S28"),
    ("K⁺-sparing subgroups", "Spironolactone, eplerenone (receptor) · amiloride, triamterene (ENaC)", "S17; SG U5-R5"),
    ("Spironolactone vs. eplerenone", "Gynecomastia vs. fewer antiandrogen effects; eplerenone + CYP3A4 inhibitors", "S17; S33"),
    ("Hyperkalemia setup", "K⁺-sparing + ACEi/ARB + CKD", "S17; S23"),
    ("Acetazolamide", "Glaucoma, altitude sickness, alkalosis; causes acidosis", "S19; SG U5-R6"),
    ("Mannitol", "Raised ICP/IOP; avoid in heart failure", "S19; S20"),
    ("Digoxin + loop", "Hypokalemia → digoxin toxicity", "S38"),
    ("Lithium + thiazide", "Lithium levels rise", "S38"),
]
