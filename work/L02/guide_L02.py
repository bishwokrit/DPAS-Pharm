"""Study-guide extras for L02 (6-sentence summary, flow diagrams, cram sheet). Imported by author_L02.py."""

SUMMARY = [
    ("Metabolism inactivates drugs, activates prodrugs, or makes active or **toxic metabolites** (e.g., NAPQI); **Phase I** (CYP450 oxidation, reduction, hydrolysis) functionalizes and **Phase II** conjugates for excretion.", "S4; S4 (notes); S5"),
    ("A **CYP inhibitor raises** a substrate's level (toxicity) and an **inducer lowers** it (therapeutic failure) — always check CYP450 interactions before adding a drug.", "S6; S7 (notes); S40"),
    ("The **kidney** is the main elimination route — filtration of free drug, active secretion, reabsorption of lipophilic un-ionized drug — and less renal function means less clearance and more exposure.", "S13; S14; S15"),
    ("**Half-life** (time for concentration to fall 50%) depends on clearance and Vd: ~**4–5 half-lives** to steady state and ~**97%** eliminated after ~5.", "S19; S23"),
    ("**Loading doses** (based on Vd) reach the target immediately; **maintenance doses** (based on clearance) keep levels in range; in CKD adjust dose and/or interval by eGFR/CrCl.", "S23; S23 (notes); S28"),
    ("**Pharmacogenomic** variants (CYP2D6, CYP2C19, TPMT, HLA-B*5801) change drug response, but genotype is one input in a checklist of indication, contraindications, organ function, interactions, patient factors, and dose/route/monitoring.", "S33; S34; S39"),
]

FLOWS = {
    "Drug Metabolism & CYP450 Interactions": [
        {"title": "Two phases of metabolism", "steps": ["Drug", "Phase I — functionalization (CYP450)", "Phase II — conjugation (adds polar group)", "More water-soluble product", "Renal/biliary excretion"], "src": "S5"},
        {"title": "CYP inhibition", "steps": ["Drug A inhibits CYP3A4", "Drug B (CYP3A4 substrate) cleared more slowly", "Drug B accumulates (Figure 6: 240%)", "Toxicity risk ↑"], "src": "S6; S8"},
        {"title": "CYP induction", "steps": ["Inducer ↑ CYP enzyme production", "Substrate cleared faster", "Level and effect ↓ (Figure 6: 42%)", "Therapeutic-failure risk ↑"], "src": "S6; S7 (notes); S8"},
    ],
    "Drug Excretion & Renal Dosing": [
        {"title": "Renal handling of a drug", "steps": ["Free drug filtered at glomerulus (by size)", "Transporters secrete more into tubule", "Lipophilic, un-ionized drug reabsorbed", "Remainder eliminated in urine"], "src": "S14"},
    ],
    "PK Calculations: Half-Life, Steady State & Clearance": [
        {"title": "Renal impairment logic chain", "steps": ["Clearance ↓", "Half-life ↑", "Time to steady state ↑", "Accumulation risk ↑ (if regimen not adjusted)"], "src": "S28 (notes)"},
        {"title": "Half-life decay (100 mg/L, t½ 6 h)", "steps": ["0 h: 100 mg/L", "6 h: 50", "12 h: 25", "18 h: 12.5", "24 h: 6.25", "30 h: 3.125 (~97% gone)"], "src": "S19"},
    ],
    "Putting It All Together: Clinical Decision-Making": [
        {"title": "One integrated pathway", "steps": ["Dose", "Absorption", "Distribution", "Receptor / target", "Effect", "Metabolism", "Excretion"], "src": "S38"},
    ],
}

CRAM = [
    ("4 purposes of metabolism", "Inactivate drug · activate prodrug · active metabolite · occasionally toxic metabolite", "S4"),
    ("NAPQI", "Toxic metabolite from acetaminophen via normal Phase I metabolism", "S4 (notes)"),
    ("Phase I", "Functionalization: oxidation, reduction, hydrolysis; mainly CYP450; unmasks reactive group", "S5"),
    ("Phase II", "Conjugation: glucuronidation, sulfation, acetylation, methylation, glutathione → water-soluble", "S5"),
    ("Phase order", "Phase I often first — but some drugs go straight to conjugation", "S5 (notes)"),
    ("CYP enzyme inhibition", "Slows CYP → substrate level **↑** → toxicity risk", "S6"),
    ("CYP enzyme induction", "More CYP made → substrate level **↓** → therapeutic failure", "S6; S7 (notes)"),
    ("Figure 6 values", "Inhibitor: 240% of baseline; inducer: 42%", "S8"),
    ("CYP3A4 inhibitor + narrow-TI substrate", "Level ↑ and toxicity risk ↑ — especially dangerous", "S11"),
    ("Main elimination route", "Kidney (most drugs and metabolites)", "S13"),
    ("Bile / feces", "Some large or protein-bound drugs", "S13"),
    ("Lungs", "Volatile agents (anesthetic gases)", "S13"),
    ("Sweat / breast milk", "Minor; breast milk matters in lactation", "S13"),
    ("Glomerular filtration", "Free (unbound) drug, by molecular size", "S14"),
    ("Tubular secretion", "Active transporters move more drug into tubule", "S14"),
    ("Tubular reabsorption", "Lipophilic, un-ionized drug diffuses back → less elimination", "S14"),
    ("Alkalinize urine (aspirin overdose)", "Traps ionized drug in tubule, blocks reabsorption", "S14 (notes)"),
    ("Renal function estimates", "eGFR and creatinine clearance (CrCl)", "S15"),
    ("Renally cleared narrow-TI drugs", "Many antibiotics, digoxin, lithium — adjust dose or interval", "S15"),
    ("CKD dosing", "Decrease dose and/or extend interval, guided by eGFR/CrCl", "S17; S28"),
    ("Half-life (t½)", "Time for plasma concentration to fall 50%; set by clearance + Vd", "S19"),
    ("% remaining formula", "100% x (1/2)^(number of half-lives)", "S19"),
    ("Concentration formula", "C(t) = C₀ x (1/2)^(t/t½)", "S19"),
    ("Remaining after 1/2/3/4/5 t½", "50% / 25% / 12.5% / 6.25% / 3.125%", "S19"),
    ("~97% eliminated", "After about 5 half-lives", "S19; S30"),
    ("Steady state", "Intake = elimination; ~4–5 half-lives, regardless of dose", "S23; S30"),
    ("Time to steady state set by", "Half-life", "S48"),
    ("Loading dose", "Larger first dose → target immediately; based on **Vd**", "S23; S23 (notes); S26"),
    ("Maintenance dose", "Ongoing dose to stay in range; based on **clearance**", "S23; S23 (notes)"),
    ("Clearance", "Plasma volume completely cleared of drug per unit time; total = hepatic + renal", "S27"),
    ("CKD effect on PK", "Clearance ↓ → t½ ↑ → concentration ↑ → time to steady state ↑", "S28; S28 (notes)"),
    ("Pharmacogenomics", "Genetic variation changing drug response (metabolism, transport, target, ADR risk)", "S32"),
    ("CYP2D6 variation", "Antidepressants, opioids — codeine activation", "S33"),
    ("CYP2C19 variation", "Clopidogrel activation; some antidepressant/PPI dosing", "S33"),
    ("TPMT deficiency", "↑ Toxicity with thiopurines (azathioprine)", "S33"),
    ("HLA-B*5801", "Severe hypersensitivity to allopurinol", "S36"),
    ("Personalized therapy inputs", "Genotype + phenotype + disease state + other medications", "S34"),
    ("Prescribing checklist", "Indication · contraindications/allergies · renal/hepatic · interactions (CYP450) · age/pregnancy · dose/route/monitoring", "S39"),
    ("Effect weakened, restored by higher agonist dose", "Competitive (not irreversible) antagonism", "S41"),
    ("Single best check vs. predictable toxicity", "Review CYP450 interactions with current medications", "S43"),
]
