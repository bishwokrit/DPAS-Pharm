"""Textbook (Katzung 16e, Ch. 3–5) additions for L02. Imported by author_L02.py.
Only details that sharpen what the lecture teaches; every fact is TB-tagged and cited to a printed page."""

ADD = {
    "Drug Metabolism & CYP450 Interactions": {
        "how": [
            ("Acetaminophen is mostly conjugated (glucuronide/sulfate); in overdose glutathione is depleted and the toxic metabolite (NAPQI) injures the liver — **N-acetylcysteine** given within 8–16 hours protects against fulminant hepatotoxicity.", "p. 66"),
        ],
        "examples": [
            ("**Inducers:** rifampin, carbamazepine, phenytoin, barbiturates, St. John's wort; **inhibitors:** ketoconazole, clarithromycin/erythromycin, ritonavir, grapefruit juice.", "p. 63; p. 64"),
            ("St. John's wort induces CYP3A4 and speeds metabolism of oral contraceptives, warfarin, cyclosporine, and others.", "p. 72"),
        ],
        "clinical": [
            ("Liver disease (cirrhosis, hepatitis) slows metabolism enough that ordinary doses can cause coma. CYP3A4 handles over 50% of liver-metabolized prescriptions.", "p. 60; p. 73"),
        ],
    },
    "PK Calculations: Half-Life, Steady State & Clearance": {
        "definitions": [
            ("**t½ = 0.7 × Vd / CL** — half-life rises when Vd rises or clearance falls.", "p. 56"),
            ("**Loading dose = Vd × target concentration** (e.g., theophylline: 35 L × 10 mg/L = 350 mg for a 70-kg adult).", "p. 52"),
        ],
        "how": [
            ("During regular dosing: 50% of steady state after 1 half-life, 75% after 2, and over 90% after 4 — the textbook's \"four half-lives\" rule of thumb.", "p. 47"),
            ("**Capacity-limited (saturable) elimination:** clearance falls as concentration rises — important for phenytoin, ethanol, and aspirin.", "p. 47"),
        ],
    },
    "Pharmacogenomics": {
        "definitions": [
            ("**PM, IM, EM, UM:** poor, intermediate, extensive (normal) and ultrarapid metabolizer.", "p. 78"),
        ],
        "how": [
            ("Codeine is converted to morphine (200× more potent) by CYP2D6; CPIC recommends an alternative analgesic for CYP2D6 poor **and** ultrarapid metabolizers.", "p. 81; p. 83"),
            ("Clopidogrel: about 85% of a dose is inactivated by esterases; CYP2C19 activates the rest. CYP2C19 poor/intermediate metabolizers → prasugrel or ticagrelor.", "p. 81; p. 82"),
            ("TPMT intermediate activity: start thiopurines at 30–70% of the target dose; deficient: use a drastically reduced dose or an alternative.", "p. 83"),
            ("Warfarin dose varies up to 20-fold between patients; CYP2C9 and VKORC1 genotypes explain much of it.", "p. 90"),
        ],
        "examples": [
            ("CYP2D6 metabolizes up to one-quarter of clinically used drugs (β blockers, antidepressants, antipsychotics, opioids).", "p. 78"),
            ("CYP2D6 ultrarapid metabolizers: up to one-third of Ethiopians and Saudi Arabians; CYP2C19 poor metabolizers: 3–5% of Caucasians, 18–23% of Japanese.", "p. 67"),
            ("Immune system genes: **HLA-B*57:01** → abacavir hypersensitivity; **G6PD deficiency** → rasburicase contraindicated; slow NAT2 acetylators (~50% in the USA) → isoniazid toxicity.", "p. 70; p. 83; p. 88"),
        ],
    },
}

CONFLICTS = {}

DISCREPANCIES = [
    ("**Time to steady state:** slides say ~4–5 half-lives; the textbook's rule of thumb is four half-lives (over 90% of steady state). These agree — the textbook just rounds down.", "S23; p. 47"),
]

CRAM = [
    ("t½ formula", "t½ = 0.7 × Vd / CL", "p. 56"),
    ("Loading dose formula", "Vd × target concentration", "p. 52"),
    ("% of steady state", "1 t½ = 50% · 2 = 75% · 4 = >90%", "p. 47"),
    ("Saturable elimination", "Phenytoin, ethanol, aspirin", "p. 47"),
    ("CYP3A4 share", ">50% of liver-metabolized prescription drugs", "p. 60"),
    ("Acetaminophen antidote", "N-acetylcysteine within 8–16 h", "p. 66"),
    ("CYP2C19 PM on clopidogrel", "Switch to prasugrel or ticagrelor", "p. 82"),
    ("HLA-B*57:01", "Abacavir hypersensitivity", "p. 88"),
]

QUESTIONS = [
    {"topic": "Drug Metabolism & CYP450 Interactions", "kind": "vignette",
     "stem": "A 19-year-old arrives 6 hours after a large intentional acetaminophen ingestion. Labs are pending. Which treatment best protects against fulminant liver injury?",
     "correct": "N-acetylcysteine, started within the 8–16 hour window",
     "why_correct": "N-acetylcysteine given within 8–16 hours protects against acetaminophen hepatotoxicity by replacing depleted glutathione (p. 66).",
     "distractors": [
         ("Sodium bicarbonate to alkalinize the urine and speed excretion", "Urine alkalinization is used for aspirin overdose, a weak acid (p. 20)."),
         ("Rifampin to induce CYP enzymes and clear the drug faster", "Induction would increase toxic metabolite formation, not protect the liver (p. 66)."),
         ("Protamine to bind and neutralize the circulating drug", "Protamine neutralizes heparin (p. 26), not acetaminophen."),
         ("Waiting for levels before giving any treatment at all", "The protective window is 8–16 hours, so delay risks liver failure (p. 66)."),
     ],
     "src": "p. 66"},
    {"topic": "Pharmacogenomics", "kind": "vignette",
     "stem": "A 62-year-old has a coronary stent placed. Genotyping shows he is a CYP2C19 poor metabolizer. Which antiplatelet choice does CPIC guidance support?",
     "correct": "Prasugrel or ticagrelor instead of clopidogrel",
     "why_correct": "Clopidogrel needs CYP2C19 activation; poor metabolizers make little active drug, so prasugrel or ticagrelor is recommended (p. 81; p. 82).",
     "distractors": [
         ("Clopidogrel at the standard dose with routine follow-up", "Standard clopidogrel risks stent thrombosis in poor metabolizers (p. 81)."),
         ("Clopidogrel plus a CYP2C19 inhibitor to raise its level", "Inhibiting CYP2C19 would reduce clopidogrel activation further (p. 81)."),
         ("Codeine-free analgesia plus standard-dose clopidogrel", "Codeine relates to CYP2D6, not antiplatelet choice (p. 81)."),
         ("Azathioprine at 30–70% of the usual starting dose", "That dose rule is for TPMT-intermediate thiopurine use (p. 83)."),
     ],
     "src": "p. 81-82"},
]

COMPARISONS = {}
FLOWS = {
    "Drug Metabolism & CYP450 Interactions": [
        {"title": "Acetaminophen: normal dose vs. overdose (textbook)", "tb": True, "src": "p. 66",
         "steps": ["Acetaminophen", "Mostly glucuronide/sulfate conjugates → excreted", "Small fraction → CYP → NAPQI, detoxified by glutathione", "Overdose: glutathione depleted → NAPQI injures the liver", "N-acetylcysteine within 8–16 h protects"]},
    ],
    "Pharmacogenomics": [
        {"title": "Codeine and CYP2D6 (textbook)", "tb": True, "src": "p. 81; p. 82",
         "steps": ["Codeine (prodrug)", "CYP2D6 → morphine (200× more potent)", "Poor metabolizer: little morphine → poor pain relief", "Ultrarapid: too much morphine → toxicity", "CPIC: alternative analgesic for PM and UM"]},
        {"title": "Clopidogrel and CYP2C19 (textbook)", "tb": True, "src": "p. 81; p. 82",
         "steps": ["Clopidogrel (prodrug)", "~85% inactivated by esterases", "CYP2C19 makes the active metabolite", "Poor/intermediate metabolizer: less active drug → more stent thrombosis after PCI", "CPIC: prasugrel or ticagrelor instead"]},
    ],
}
FIGURES = {
    "PK Calculations: Half-Life, Steady State & Clearance": [
        {"image": "TB_fill_empty.png", "title": "Textbook concept · Five to fill, five to empty", "tb": True, "src": "S19; S23; p. 47",
         "caption": "Original diagram: starting regular dosing, each half-life closes half of the remaining gap to steady state (50 → 75 → 87.5 → 93.75 → ~97%); after stopping, each half-life removes half of what remains (50 → 25 → 12.5 → 6.25 → 3.125%). The same 4–5 half-lives govern both."},
    ],
}

# One "Go deeper" textbook link per part, only where the chapter adds real depth: (chapter, first page, last page, why)
DEEPER = {
    "Drug Metabolism & CYP450 Interactions": (4, 60, 67, "CYP families, the inducer/inhibitor tables, and acetaminophen toxicity step by step"),
    "PK Calculations: Half-Life, Steady State & Clearance": (3, 46, 52, "Worked dosing math: steady state, loading and maintenance doses"),
    "Pharmacogenomics": (5, 78, 83, "CPIC dosing tables for CYP2D6, CYP2C19, and TPMT"),
}


# ---- Assigned-reading coverage (QC pass): major sections of Ch. 3–5 the slides did not teach, summarized in our own words
# and cited to printed pages, so the guide alone covers the testable reading. Merged into the lists above.
_READ = {
    "Drug Metabolism & CYP450 Interactions": {
        "definitions": [
            ("**Cytochrome P450** (in the liver’s smooth endoplasmic reticulum) does most Phase I work and has low substrate specificity: lipid-soluble drugs are its common thread.", "p. 59; p. 60"),
        ],
        "how": [
            ("Share of liver P450: CYP3A4 about 30%, CYP2C9 about 20%, CYP1A2 about 15%, CYP2D6 about 5%.", "p. 60"),
            ("**Commensal gut microbiota** (gut bacteria) metabolize drugs too: they inactivate digoxin, so antibiotics such as erythromycin can double digoxin levels.", "p. 71"),
            ("An inducer can speed up its own metabolism (**pharmacokinetic tolerance**): the same dose works less over time.", "p. 72"),
        ],
        "clinical": [
            ("**Diet and environment:** smoking, charcoal-broiled food and cruciferous vegetables induce CYP1A; grapefruit juice inhibits CYP3A.", "p. 60; p. 71"),
            ("Stopping an inducer is as risky as starting one: when the inducer stops, warfarin metabolism slows, levels rise and bleeding can follow.", "p. 72"),
        ],
        "examples": [
            ("Terfenadine plus CYP3A4 inhibitors (ketoconazole, erythromycin, grapefruit juice) caused fatal torsades de pointes; terfenadine was withdrawn.", "p. 72"),
            ("Allopurinol inhibits xanthine oxidase, so the mercaptopurine dose must be reduced when both are given.", "p. 72"),
        ],
    },
    "PK Calculations: Half-Life, Steady State & Clearance": {
        "definitions": [
            ("**Extraction ratio:** the share of drug the liver removes in one pass. High-ER drugs have low oral bioavailability (morphine ER 0.67 → about 33%).", "p. 49"),
            ("**Target concentration approach** (the rational way to design a dosage regimen): pick the level that gives the desired effect, then dose from the patient’s clearance and Vd.", "p. 51"),
            ("**Zero-order absorption** runs at a constant rate (controlled-release forms); **first-order** is proportional to the amount left.", "p. 49"),
        ],
        "how": [
            ("**Maintenance dosing rate = clearance × target concentration** (÷ F if oral). The dosing interval changes only peaks and troughs, not the average level.", "p. 51"),
            ("Half-life can change without clearance changing: diazepam’s half-life lengthens with age because its Vd grows.", "p. 54"),
            ("Effects can outlast plasma levels (delayed effects): warfarin acts only as clotting factors turn over.", "p. 50"),
        ],
        "clinical": [
            ("High-extraction drugs (morphine, propranolol, verapamil) vary widely between patients, and far more drug gets through in cirrhosis.", "p. 49"),
            ("**Schedule matters:** gentamicin is more nephrotoxic as a constant infusion than as intermittent doses at the same average level.", "p. 50"),
            ("Give IV loading doses slowly (over an hour): a fast bolus can overshoot into toxicity, e.g., phenytoin.", "p. 52"),
            ("Timing drug levels: digoxin at least 6 hours after the dose; lithium just before the next dose.", "p. 55"),
            ("In obesity, dose drugs that stay out of fat (gentamicin, digoxin) on fat-free mass.", "p. 53; p. 55"),
            ("Displacing a drug from plasma proteins raises free drug only briefly; the body eliminates the extra, so binding changes rarely matter clinically.", "p. 55"),
        ],
    },
    "Pharmacogenomics": {
        "how": [
            ("**G6PD deficiency** (X-linked): red cells cannot make enough NADPH, so they hemolyze under oxidative stress (infection, fava beans, certain drugs).", "p. 86"),
            ("NUDT15 variants, like TPMT, cause thiopurine intolerance.", "p. 86"),
        ],
        "examples": [
            ("**ABCG2 (BCRP)** variant, common in East Asians, raises rosuvastatin levels; the label suggests half the dose.", "p. 87"),
            ("**SLCO1B1** (the OATP1B1 organic anion transporter) reduced-function variants raise simvastatin levels and myopathy risk: use a lower dose or another statin.", "p. 87"),
        ],
    },
}
for _n, _secs in _READ.items():
    for _k, _v in _secs.items():
        ADD.setdefault(_n, {}).setdefault(_k, []).extend(_v)

COMPARISONS.setdefault("PK Calculations: Half-Life, Steady State & Clearance", []).append(
    {"title": "Dosing from the target concentration (textbook Ch. 3)", "tb": True, "src": "p. 51; p. 52",
     "columns": ["Goal", "Formula", "Depends on"],
     "rows": [["Keep the level steady", "Maintenance dosing rate = CL × target concentration (÷ F if oral)", "Clearance"],
              ["Reach the target now", "Loading dose = Vd × target concentration", "Volume of distribution"],
              ["Match the peak at steady state", "Loading dose = maintenance dose × accumulation factor", "Dosing interval and half-life"]]})
COMPARISONS.setdefault("Drug Metabolism & CYP450 Interactions", []).append(
    {"title": "Which inducers switch on which enzyme (textbook Ch. 4)", "tb": True, "src": "p. 60",
     "columns": ["Inducers", "Enzyme induced"],
     "rows": [["Tobacco smoke, charcoal-broiled meat, cruciferous vegetables, omeprazole", "CYP1A"],
              ["Rifampin, St. John’s wort, dexamethasone, phenobarbital", "CYP3A"]]})

CRAM += [
    ("Extraction ratio", "High ER → low oral bioavailability (first pass)", "p. 49"),
    ("Maintenance dosing rate", "CL × target concentration (÷ F orally)", "p. 51"),
    ("Average steady-state level", "Set by clearance alone", "p. 51"),
    ("Smoking", "Induces CYP1A", "p. 60"),
    ("Digoxin level timing", "At least 6 h after the dose", "p. 55"),
    ("SLCO1B1 variant", "Simvastatin myopathy: lower dose or another statin", "p. 87"),
]

QUESTIONS += [
    {"topic": "PK Calculations: Half-Life, Steady State & Clearance", "kind": "vignette",
     "stem": "A drug is given every 8 hours instead of every 24 hours, keeping the same total daily dose. What happens to its average steady-state concentration?",
     "correct": "It stays the same; only peaks and troughs change",
     "why_correct": "The average steady-state level depends only on dosing rate and clearance; the interval changes only the swings (p. 51).",
     "distractors": [
         ("It triples because doses come more often", "Total dose per day is unchanged, so the average is unchanged (p. 51)."),
         ("It falls because each dose is smaller", "Smaller, more frequent doses narrow the swings, not the average (p. 51)."),
         ("It doubles because half-life gets longer", "Dosing interval does not change half-life (p. 51)."),
         ("It depends on Vd, which now changes", "Vd sets the loading dose, not the average level (p. 51; p. 52)."),
     ],
     "src": "p. 51"},
    {"topic": "Drug Metabolism & CYP450 Interactions", "kind": "vignette",
     "stem": "A heavy smoker on a CYP1A2-metabolized drug quits smoking abruptly. What should the PA anticipate?",
     "correct": "Drug levels may rise as CYP1A induction fades",
     "why_correct": "Tobacco smoke induces CYP1A; when the inducer stops, metabolism slows and levels can rise (p. 60; p. 72).",
     "distractors": [
         ("Drug levels will fall because metabolism speeds up", "Quitting removes induction, so metabolism slows (p. 60)."),
         ("No change, since smoking affects only the lungs", "Smoke chemicals induce liver CYP1A enzymes (p. 60)."),
         ("Renal clearance will double right away", "The effect is on hepatic metabolism, not renal clearance (p. 60)."),
         ("The drug becomes a prodrug that needs activation", "Quitting does not change how the drug is activated (p. 60)."),
     ],
     "src": "p. 60; p. 72"},
]

# Reading headings left out on purpose: beyond PA-level scope (no prescribing decision attached; the Go deeper link opens the pages)
READING_SKIP = [
    {"heading": "ORGANIC CATION TRANSPORTER 1 (OCT1, SLC22A1)", "reason": "Beyond PA scope: transporter genetics with no routine prescribing change"},
]
