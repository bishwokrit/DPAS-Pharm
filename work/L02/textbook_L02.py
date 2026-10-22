"""Textbook (Katzung 16e, Ch. 3–5) additions for L02. Imported by author_L02.py.
Only details that sharpen what the lecture teaches; every fact is TB-tagged and cited to a printed page."""

ADD = {
    "Drug Metabolism & CYP450 Interactions": {
        "how": [
            ("CYP3A4 alone metabolizes over 50% of the prescription drugs metabolized by the liver.", "p. 60"),
            ("Acetaminophen is mostly conjugated (glucuronide/sulfate); in overdose glutathione is depleted and the toxic metabolite (NAPQI) injures the liver — **N-acetylcysteine** given within 8–16 hours protects against fulminant hepatotoxicity.", "p. 66"),
        ],
        "examples": [
            ("**Inducers:** rifampin, carbamazepine, phenytoin, barbiturates, St. John's wort; **inhibitors:** ketoconazole, clarithromycin/erythromycin, ritonavir, grapefruit juice.", "p. 63; p. 64"),
            ("St. John's wort induces CYP3A4 and speeds metabolism of oral contraceptives, warfarin, cyclosporine, and others.", "p. 72"),
        ],
        "clinical": [
            ("Liver disease (e.g., cirrhosis, hepatitis) slows metabolism of some drugs enough that ordinary doses can cause coma.", "p. 73"),
            ("Severe ADRs contribute to about 100,000 US deaths a year and about 7% of hospital admissions.", "p. 71"),
        ],
    },
    "PK Calculations: Half-Life, Steady State & Clearance": {
        "definitions": [
            ("**t½ = 0.7 × Vd / CL** — half-life rises when Vd rises or clearance falls.", "p. 56"),
            ("**Loading dose = Vd × target concentration** (e.g., theophylline: 35 L × 10 mg/L = 350 mg for a 70-kg adult).", "p. 52"),
        ],
        "how": [
            ("During regular dosing: 50% of steady state after 1 half-life, 75% after 2, and over 90% after 4 — the textbook's \"four half-lives\" rule of thumb.", "p. 47"),
            ("If the dosing interval is shorter than four half-lives, accumulation will be detectable.", "p. 48"),
            ("**Capacity-limited (saturable) elimination:** clearance falls as concentration rises — important for phenytoin, ethanol, and aspirin.", "p. 47"),
        ],
    },
    "Pharmacogenomics": {
        "how": [
            ("Codeine is converted to morphine (200× more potent) by CYP2D6; CPIC recommends an alternative analgesic for CYP2D6 poor **and** ultrarapid metabolizers.", "p. 81; p. 83"),
            ("Clopidogrel: about 85% of a dose is inactivated by esterases; CYP2C19 activates the rest. CYP2C19 poor/intermediate metabolizers → prasugrel or ticagrelor.", "p. 81; p. 82"),
            ("TPMT intermediate activity: start thiopurines at 30–70% of the target dose; deficient: use a drastically reduced dose or an alternative.", "p. 83"),
            ("Warfarin dose varies up to 20-fold between patients; CYP2C9 and VKORC1 genotypes explain much of it.", "p. 90"),
        ],
        "examples": [
            ("CYP2D6 metabolizes up to one-quarter of clinically used drugs (β blockers, antidepressants, antipsychotics, opioids).", "p. 78"),
            ("CYP2D6 ultrarapid metabolizers: up to one-third of Ethiopians and Saudi Arabians; CYP2C19 poor metabolizers: 3–5% of Caucasians, 18–23% of Japanese.", "p. 67"),
            ("**HLA-B*57:01** → abacavir hypersensitivity; **G6PD deficiency** → rasburicase contraindicated; slow NAT2 acetylators (~50% in the USA) → isoniazid toxicity.", "p. 70; p. 83; p. 88"),
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
