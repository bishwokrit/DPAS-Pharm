"""Textbook (Katzung 16e, Ch. 1–2) additions for L01. Imported by author_L01.py.
Only details that sharpen what the lecture teaches; every fact is TB-tagged and cited to a printed page."""

ADD = {
    "The Language of Pharmacology": {
        "definitions": [
            ("**Prodrug:** an inactive precursor converted to the active drug in the body (usually by metabolism).", "p. 8"),
            ("**Poisons** are drugs with almost exclusively harmful effects — but \"the dose makes the poison\" (Paracelsus): any substance can harm at the wrong dose.", "p. 3"),
        ],
        "clinical": [
            ("More than half of prescriptions in the USA are for generic drugs.", "p. 18"),
        ],
    },
    "Drug Development & Regulation": {
        "how": [
            ("Phase II has the **highest failure rate** — only about 25% of new drugs move on to Phase III.", "p. 17"),
            ("Phase III usually enrolls **thousands** of patients (Figure 1–6: 1000–6000), often double-blind and crossover, in settings like the drug's eventual use.", "p. 12; p. 17"),
            ("Less than one-third of drugs studied in humans survive clinical trials and reach the market.", "p. 14"),
            ("To see one case of a toxicity occurring 1 in 10,000, several hundred thousand patients may need exposure — so rare effects usually surface only in Phase IV, which has **no fixed duration**.", "p. 18"),
            ("Marketing requires a **New Drug Application (NDA)** after Phase III; human testing starts only after an **IND** (Investigational New Drug) application.", "p. 12; p. 17"),
        ],
        "clinical": [
            ("A patent lasts 20 years; after it expires, generics are approved through an **abbreviated new drug application (ANDA)** that requires bioequivalence data.", "p. 16; p. 18"),
            ("Placebo responses can occur in as many as 30–40% of subjects — the reason controlled, blinded trials are needed.", "p. 14"),
            ("Adverse events that are both **serious and unexpected** must be reported to the FDA within 15 days; clinicians can report through MedWatch.", "p. 18; p. 19"),
        ],
        "examples": [
            ("**Thalidomide** (sold in Europe as a \"nontoxic\" hypnotic) caused about 10,000 birth defects and led to the **Kefauver-Harris Amendments (1962)**, which required proof of efficacy as well as safety.", "p. 16"),
            ("The **Orphan Drug Amendment (1983)** gives incentives for drugs treating diseases with fewer than 200,000 US patients.", "p. 16"),
        ],
    },
    "Pharmacodynamics: Targets & Receptors": {
        "how": [
            ("**Spare receptors:** a maximal response can occur without occupying every receptor (e.g., about 90% of cardiac β receptors can be blocked and maximal inotropic response still preserved).", "p. 23"),
            ("**Irreversible antagonist** effects last until new receptors are made — duration depends on receptor turnover, not drug elimination (phenoxybenzamine for pheochromocytoma).", "p. 25"),
            ("A partial agonist's lower maximal effect is **not** due to lower affinity — it can occupy all receptors and still produce less response.", "p. 26"),
            ("**Allosteric modulators** bind a different site from the agonist (e.g., benzodiazepines enhance GABA's effect).", "p. 25"),
            ("Agonist-induced **desensitization** (tachyphylaxis) and downregulation reduce response with continued exposure.", "p. 39"),
        ],
        "examples": [
            ("**Chemical antagonism** needs no receptor: positively charged protamine binds and neutralizes negatively charged heparin.", "p. 26"),
            ("**Physiologic antagonism:** two drugs act on different receptors with opposing effects (e.g., insulin opposes glucocorticoid-induced hyperglycemia).", "p. 27"),
        ],
        "clinical": [
            ("Competitive antagonism is surmountable in real life: exercise or stress raises catecholamines enough to overcome a fixed propranolol dose.", "p. 25"),
            ("Propranolol markedly slows the heart rate in pheochromocytoma (high catecholamines) but not the resting rate of a trained marathon runner.", "p. 39"),
        ],
    },
    "Dose-Response Relationships": {
        "definitions": [
            ("**Quantal dose-response:** ED₅₀ (effective in 50%), TD₅₀ (toxic in 50%), LD₅₀ (lethal in 50% of animals).", "p. 38"),
            ("**Therapeutic window:** the range between the minimum therapeutic dose and the minimum toxic dose — more practical than TI for dosing a patient.", "p. 38"),
        ],
        "clinical": [
            ("No drug causes only a single specific effect — drugs are **selective**, not specific.", "p. 40"),
            ("Asthma + hypertension on propranolol: nonselective β blockade can cause bronchoconstriction; a β₁-selective blocker (metoprolol) is an alternative.", "p. 41"),
        ],
    },
    "Pharmacokinetics: ADME — Absorption & Distribution": {
        "how": [
            ("First-pass loss can happen in the **gut wall** (e.g., intestinal CYP3A4) as well as the liver; grapefruit juice inhibits gut-wall metabolism and P-glycoprotein, raising absorption of some drugs.", "p. 48"),
            ("**P-glycoprotein (MDR1)** pumps drugs out of cells in brain, testes, and gut; inhibiting it raises digoxin blood levels.", "p. 9"),
            ("**Ion trapping:** weak acids are excreted faster in **alkaline** urine; weak bases faster in **acidic** urine.", "p. 10; p. 11"),
        ],
        "clinical": [
            ("Aspirin overdose: sodium bicarbonate alkalinizes blood and urine, reducing aspirin entry into tissues and speeding its renal excretion.", "p. 20"),
        ],
    },
}

CONFLICTS = {
    "Drug Development & Regulation": [
        {"topic": "Phase I population",
         "slides": {"text": "Phase I: a small group of healthy volunteers.", "src": "S13"},
         "textbook": {"text": "Phase I: 20–100 healthy volunteers — but if significant toxicity is expected (cancer, AIDS therapy), volunteer **patients with the disease** are used instead.", "src": "p. 17"}},
        {"topic": "Phase II size",
         "slides": {"text": "Phase II: a few hundred patients with the target condition.", "src": "S13"},
         "textbook": {"text": "Phase II: a modest number of patients (100–200) with the target disease.", "src": "p. 17"}},
    ],
}

DISCREPANCIES = [
    ("**First-pass effect:** slides describe hepatic first-pass and say essentially every route except oral bypasses it. The textbook adds that drug can also be metabolized in the gut wall, and that the rectal route only partly avoids the liver (about 50%).", "S49 (notes); S51; p. 48; p. 49"),
    ("**Therapeutic index:** slides define TI = TD₅₀ ÷ ED₅₀. The textbook notes this is measured in animals; for a patient, the therapeutic window (minimum therapeutic to minimum toxic dose) is more useful.", "S38; p. 38"),
    ("**Phase I population:** slides say healthy volunteers; the textbook adds that patients with the disease are used when significant toxicity is expected (cancer, AIDS).", "S13; p. 17"),
    ("**Phase II size:** slides say a few hundred patients; the textbook says 100–200. Exams may use either — know both.", "S13; p. 17"),
]

CRAM = [
    ("Phase I size (textbook)", "20–100 healthy volunteers; patients if drug is very toxic (cancer, AIDS)", "p. 17"),
    ("Phase with highest failure", "Phase II — only ~25% move to Phase III", "p. 17"),
    ("Kefauver-Harris (1962)", "Required proof of **efficacy** (thalidomide)", "p. 16"),
    ("Generic approval", "ANDA with bioequivalence data; patent life 20 years", "p. 16; p. 18"),
    ("Spare receptors", "Max response without full occupancy (~90% cardiac β can be blocked)", "p. 23"),
    ("Chemical antagonist", "Protamine neutralizes heparin — no receptor", "p. 26"),
    ("Therapeutic window", "Min therapeutic → min toxic dose; more practical than TI", "p. 38"),
    ("Aspirin overdose", "Sodium bicarbonate → alkaline urine → faster excretion", "p. 20"),
]

QUESTIONS = [
    {"topic": "Pharmacodynamics: Targets & Receptors", "kind": "vignette",
     "stem": "A 54-year-old is given phenoxybenzamine before surgery for pheochromocytoma. Blood pressure stays controlled even when the tumor releases large catecholamine surges. What best explains why the blockade persists?",
     "correct": "It binds receptors irreversibly; effect lasts until new receptors are made",
     "why_correct": "An irreversible antagonist's duration depends on receptor turnover, and high agonist levels cannot overcome it (p. 25).",
     "distractors": [
         ("It competes reversibly, so high catecholamine levels easily displace it", "That describes competitive antagonism, which surges CAN overcome (p. 25)."),
         ("It neutralizes catecholamines chemically in plasma before they reach receptors", "That is chemical antagonism, like protamine–heparin (p. 26)."),
         ("It activates opposing receptors, producing a physiologic counter-effect instead", "That is physiologic antagonism, like insulin vs glucocorticoids (p. 27)."),
         ("It is a partial agonist that caps the maximal catecholamine response", "Partial agonists produce a submaximal response; phenoxybenzamine is an irreversible antagonist (p. 25; p. 26)."),
     ],
     "src": "p. 25-27"},
    {"topic": "Drug Development & Regulation", "kind": "mechanism",
     "stem": "According to the textbook, which clinical trial phase has the highest rate of drug failures?",
     "correct": "Phase II",
     "why_correct": "Phase II has the highest failure rate; only about 25% of drugs move on to Phase III (p. 17).",
     "distractors": [
         ("Phase I", "Phase I sets the safe dose range in 20–100 subjects; it is not the main failure point (p. 17)."),
         ("Phase III", "Phase III confirms efficacy in thousands, after most failures have occurred (p. 17)."),
         ("Phase IV", "Phase IV is postmarketing surveillance after approval (p. 17)."),
         ("FDA review", "FDA review is the approval step after Phase III, not a trial phase (p. 17)."),
     ],
     "src": "p. 17"},
]

# Textbook comparison tables, flows, and original diagrams of textbook concepts
COMPARISONS = {
    "Dose-Response Relationships": [
        {"title": "The narrow-TI drugs in numbers (textbook Table 3–1)", "tb": True, "src": "p. 44; p. 45",
         "columns": ["Drug", "Half-life", "Target level", "Toxic above", "Worth knowing"],
         "rows": [["Digoxin", "39 h", "1 ng/mL", "2 ng/mL", "Vd ~500 L (sequestered in tissue); 67% excreted in urine"],
                  ["Lithium", "22 h", "0.7 mEq/L", "2 mEq/L", "95% excreted in urine, 0% protein-bound — renal function rules"],
                  ["Phenytoin", "Concentration-dependent", "10 mg/L", "20 mg/L", "Saturable (capacity-limited) elimination; 89% protein-bound"],
                  ["Warfarin", "37 h", "Not in table", "Not in table", "99% protein-bound"]]},
    ],
    "Pharmacokinetics: ADME — Absorption & Distribution": [
        {"title": "Bioavailability by route (textbook Table 3–3)", "tb": True, "src": "p. 48",
         "columns": ["Route", "Bioavailability (%)", "Note"],
         "rows": [["Intravenous (IV)", "100", "Most rapid onset"],
                  ["Intramuscular (IM)", "75 to ≤100", "Large volumes often feasible; may be painful"],
                  ["Subcutaneous (SC)", "75 to ≤100", "Smaller volumes than IM; may be painful"],
                  ["Oral (PO)", "5 to <100", "Most convenient; first-pass effect may be important"],
                  ["Rectal (PR)", "30 to <100", "Less first-pass effect than oral"],
                  ["Inhalation", "5 to <100", "Often very rapid onset"],
                  ["Transdermal", "80 to ≤100", "Usually very slow absorption; prolonged duration"]]},
    ],
}
FLOWS = {
    "Dose-Response Relationships": [
        {"title": "Asthma + propranolol (textbook case)", "tb": True, "src": "p. 41",
         "steps": ["Nonselective β blocker (propranolol)", "Blocks β2 in the airways", "Bronchoconstriction / no bronchodilation", "Use a β1-selective blocker (metoprolol) or another antihypertensive"]},
    ],
    "Pharmacokinetics: ADME — Absorption & Distribution": [
        {"title": "Aspirin overdose and urine pH (textbook case)", "tb": True, "src": "p. 20",
         "steps": ["Aspirin = weak acid", "Acidosis drives it into tissues and back from urine", "Sodium bicarbonate alkalinizes blood and urine", "Drug ionized → trapped in urine → faster renal clearance"]},
    ],
}
FIGURES = {
    "Dose-Response Relationships": [
        {"image": "TB_quantal.png", "title": "Textbook concept · Quantal dose-response and the therapeutic window", "tb": True, "src": "p. 38",
         "caption": "Original diagram (illustrative values) of a textbook concept: the % of a population showing the therapeutic effect (blue) or a toxic effect (red) as dose rises. ED₅₀ and TD₅₀ give TI = TD₅₀ ÷ ED₅₀ (an animal-study measure); the therapeutic window — minimum therapeutic dose to minimum toxic dose — is the more practical range for dosing a patient."},
    ],
}

# One "Go deeper" textbook link per part, only where the chapter adds real depth: (chapter, first page, last page, why)
DEEPER = {
    "Drug Development & Regulation": (1, 12, 18, "Every trial phase in detail, the FDA laws, and how generics get approved"),
    "Pharmacodynamics: Targets & Receptors": (2, 22, 27, "Spare receptors and each antagonist type, with dose-response curves"),
    "Dose-Response Relationships": (2, 37, 41, "Quantal curves, therapeutic window, and the propranolol–asthma case"),
    "Pharmacokinetics: ADME — Absorption & Distribution": (1, 8, 11, "How drugs cross membranes, ion trapping, and transporters like P-glycoprotein"),
}


# ---- Assigned-reading coverage (QC pass): every major section of Ch. 1–2 that the slides did not teach, so the guide alone
# covers the testable reading. Summarized in our own words, cited to printed pages; merged into the lists above.
_READ = {
    "The Language of Pharmacology": {
        "how": [
            ("Drugs bind receptors by **covalent** bonds (strong, often irreversible), **electrostatic** bonds (most common) or **hydrophobic** bonds (weak).", "p. 4"),
            ("**Chirality:** over half of drugs are mirror-image pairs (enantiomers); one is usually much more potent, yet most are sold as 50:50 mixtures.", "p. 4; p. 5"),
        ],
        "clinical": [
            ("Weak bonds need a precise fit, so they are **more selective**. Aspirin’s covalent bond to platelet cyclooxygenase lasts until new platelets are made.", "p. 4"),
        ],
    },
    "Drug Development & Regulation": {
        "definitions": [
            ("**Double-blind:** neither subjects nor evaluators know who gets drug or placebo. **Crossover:** each subject gets every treatment in turn.", "p. 14; p. 15"),
            ("**IRB:** the committee at each trial site that approves the ethics of the study; participants give informed consent.", "p. 17"),
        ],
        "how": [
            ("Strength of evidence: case reports < cohort and case-control studies < **randomized controlled trials** (the gold standard: randomization balances confounders).", "p. 15"),
        ],
        "clinical": [
            ("Dietary supplements are regulated as food under DSHEA (1994), so they get no full FDA drug review.", "p. 3; p. 16"),
        ],
    },
    "Pharmacodynamics: Targets & Receptors": {
        "definitions": [
            ("**Kd:** the drug concentration that fills half the receptors; a low Kd means high affinity.", "p. 23"),
        ],
        "how": [
            ("Targets beyond receptors: **enzymes** (statins on HMG-CoA reductase), **transporters** (digitalis on Na⁺/K⁺-ATPase; antidepressants) and **structural proteins** (colchicine on tubulin).", "p. 22"),
            ("Five signaling mechanisms carry a drug’s message into the cell: intracellular receptor, receptor tyrosine kinase, cytokine receptor (JAK-STAT), ion channel and G protein (compared in the table).", "p. 28-32"),
        ],
        "clinical": [
            ("Glucocorticoids will not stop an acute asthma attack within minutes: gene-acting drugs need hours to make new proteins.", "p. 28"),
            ("Phosphodiesterase inhibitors prolong second messengers: milrinone (cAMP) and sildenafil (cGMP).", "p. 34; p. 35"),
        ],
    },
    "Pharmacokinetics: ADME — Absorption & Distribution": {
        "definitions": [
            ("**pKa:** the pH at which a drug is half ionized and half nonionized.", "p. 10"),
        ],
        "how": [
            ("Drugs cross membranes by **lipid diffusion** (the main route), aqueous pores, **carriers** (saturable) or endocytosis (vitamin B₁₂, iron).", "p. 8; p. 9"),
            ("Only the **nonionized** form crosses lipid membranes: a weak acid is mostly nonionized when pH < pKa, a weak base when pH > pKa (Henderson-Hasselbalch).", "p. 9; p. 10"),
        ],
        "examples": [
            ("Weak acids: aspirin (pKa 3.5), warfarin (5.0). Weak bases: morphine (7.9), propranolol (9.4).", "p. 10"),
        ],
    },
}
for _n, _secs in _READ.items():
    for _k, _v in _secs.items():
        ADD.setdefault(_n, {}).setdefault(_k, []).extend(_v)

COMPARISONS.setdefault("Pharmacokinetics: ADME — Absorption & Distribution", []).append(
    {"title": "What a drug’s Vd tells you about where it goes (textbook Table 3–2)", "tb": True, "src": "p. 43; p. 44; p. 46",
     "columns": ["Vd (L/kg)", "Where the drug is", "Example"],
     "rows": [["0.04 (about 2.8 L in 70 kg)", "Stays in the plasma (minimum possible Vd)", "Large proteins such as antibodies"],
              ["0.2", "Extracellular water", "Gentamicin"],
              ["0.6", "Total body water", "Ethanol"],
              ["Far above body size", "Sequestered in tissue", "Digoxin"]]})
COMPARISONS.setdefault("Pharmacodynamics: Targets & Receptors", []).extend([
    {"title": "Five ways a signal crosses the membrane (textbook Ch. 2)", "tb": True, "src": "p. 28-32",
     "columns": ["Mechanism", "Examples", "How it signals", "Clinical point"],
     "rows": [["Intracellular receptor", "Corticosteroids, sex steroids, vitamin D, thyroid hormone", "Lipid-soluble ligand enters the cell; receptor changes gene transcription", "Effects lag 30 min to hours and persist after the drug is gone"],
              ["Receptor tyrosine kinase", "Insulin, EGF, PDGF", "Receptors dimerize and phosphorylate tyrosines", "Blocked in cancer (trastuzumab, gefitinib)"],
              ["Cytokine receptor", "Growth hormone, erythropoietin, interferons", "Separate JAK kinase activates STATs, which enter the nucleus", "Same pattern as tyrosine kinases, kinase is a separate protein"],
              ["Ion channel", "Nicotinic ACh, GABA, glutamate; voltage-gated Ca²⁺ and Na⁺ channels", "Opens or blocks ion flow, changing membrane potential", "Fastest signal (milliseconds); verapamil, local anesthetics"],
              ["G protein–coupled receptor", "β and α adrenoceptors, muscarinic ACh, opioids", "G protein (GTP) changes an effector, which changes a second messenger", "Largest family; desensitizes with continued agonist"]]},
    {"title": "G proteins and their second messengers (textbook Table 2–1)", "tb": True, "src": "p. 32",
     "columns": ["G protein", "Receptors for", "Effect"],
     "rows": [["Gs", "β-adrenergic amines, histamine, glucagon", "↑ adenylyl cyclase → ↑ cAMP"],
              ["Gi", "α₂-adrenergic amines, muscarinic ACh, opioids", "↓ cAMP; opens cardiac K⁺ channels → ↓ heart rate"],
              ["Gq", "Muscarinic ACh, serotonin (5-HT₂)", "↑ phospholipase C → IP₃, DAG, ↑ cytoplasmic Ca²⁺"]]},
])
COMPARISONS.setdefault("Drug Development & Regulation", []).append(
    {"title": "Major US drug laws (textbook Table 1–6)", "tb": True, "src": "p. 16",
     "columns": ["Law", "What it did"],
     "rows": [["Food, Drug, and Cosmetic Act (1938)", "New drugs must be safe (not yet proven effective); followed sulfanilamide deaths"],
              ["Durham-Humphrey Act (1952)", "FDA decides which drugs need a prescription"],
              ["Kefauver-Harris Amendments (1962)", "Proof of efficacy as well as safety; adverse-reaction reporting (after thalidomide)"],
              ["Comprehensive Drug Abuse Prevention and Control Act (1970)", "Drug schedules and controls for habit-forming drugs"],
              ["Orphan Drug Amendment (1983)", "Incentives for diseases with fewer than 200,000 US patients"],
              ["Drug Price Competition and Patent Restoration Act (1984)", "Abbreviated applications for generics; bioequivalence data required"],
              ["Dietary Supplement Health and Education Act (1994)", "Supplements treated as food; no full FDA drug review"],
              ["Biologics Price Competition and Innovation Act (2009)", "Abbreviated pathway for biosimilars"]]})

CRAM += [
    ("Weak bonds vs covalent", "Weak = more selective; covalent = long-lasting (aspirin)", "p. 4"),
    ("pKa", "pH where ionized = nonionized", "p. 10"),
    ("Ion trapping", "Acids leave faster in alkaline urine; bases in acidic urine", "p. 10"),
    ("Intracellular receptors", "Steroids, thyroid, vitamin D; lag 30 min–hours, effect persists", "p. 28"),
    ("Gs / Gi / Gq", "↑ cAMP / ↓ cAMP / ↑ IP₃, DAG, Ca²⁺", "p. 32"),
    ("Gold-standard trial", "Randomized controlled trial", "p. 15"),
]

QUESTIONS += [
    {"topic": "Pharmacokinetics: ADME — Absorption & Distribution", "kind": "vignette",
     "stem": "A patient overdoses on a weak-acid drug. To speed its renal excretion, what should be done to the urine?",
     "correct": "Make the urine more alkaline",
     "why_correct": "In alkaline urine a weak acid is mostly ionized, so it cannot diffuse back across the tubule and is trapped in the urine (p. 10).",
     "distractors": [
         ("Make the urine more acidic", "Acidic urine keeps a weak acid nonionized and lipid-soluble, so more is reabsorbed (p. 10)."),
         ("Keep urine pH unchanged and give more fluids only", "Fluids alone do not trap the drug; ionization is the lever (p. 10)."),
         ("Raise plasma protein binding", "Protein binding does not trap drug in the urine (p. 8; p. 10)."),
         ("Slow glomerular filtration", "Less filtration would slow excretion, not speed it (p. 10)."),
     ],
     "src": "p. 10"},
    {"topic": "Pharmacodynamics: Targets & Receptors", "kind": "mechanism",
     "stem": "A patient asks why an inhaled bronchodilator works in minutes but an oral corticosteroid takes hours. What best explains the corticosteroid’s delay?",
     "correct": "It acts on an intracellular receptor that changes gene transcription",
     "why_correct": "Gene-acting drugs need time to make new proteins, so effects lag 30 minutes to several hours (p. 28).",
     "distractors": [
         ("It acts on a ligand-gated ion channel", "Ion channels respond within milliseconds (p. 31)."),
         ("It must first be activated by CYP2D6", "Prodrug activation is not the reason for this lag (p. 28)."),
         ("It binds a G protein–coupled receptor that raises cAMP", "That is how a β₂ agonist bronchodilator works, quickly (p. 31; p. 32)."),
         ("It is a partial agonist with low efficacy", "Efficacy does not explain timing (p. 28)."),
     ],
     "src": "p. 28"},
    {"topic": "Pharmacodynamics: Targets & Receptors", "kind": "mechanism",
     "stem": "A drug activates a receptor coupled to Gq. Which change follows inside the cell?",
     "correct": "Phospholipase C makes IP₃ and DAG; calcium rises",
     "why_correct": "Gq stimulates phospholipase C, producing IP₃ (calcium release) and DAG (protein kinase C) (p. 32; p. 35).",
     "distractors": [
         ("Adenylyl cyclase is stimulated, so cAMP rises", "That is Gs (p. 32)."),
         ("Adenylyl cyclase is inhibited, so cAMP falls", "That is Gi (p. 32)."),
         ("A JAK kinase activates STAT transcription proteins", "That is a cytokine receptor, not a G protein (p. 29)."),
         ("Phosphodiesterase breaks down cGMP in the cell", "That is Gt in the retina (p. 32)."),
     ],
     "src": "p. 32; p. 35"},
]
DEEPER.setdefault("The Language of Pharmacology", (1, 3, 5, "Drug size, bonds, chirality, and how new drugs are designed"))

# Reading headings taught in another lecture (same chapter split across sessions); the reading-coverage gate accepts these.
READING_SKIP = [
    {"heading": "APPROACH TO DESIGNING A RATIONAL DOSAGE REGIMEN", "reason": "Ch. 3 dosing is taught in L02 (PK Calculations)"},
    {"heading": "THE TARGET CONCENTRATION APPROACH TO DESIGNING A RATIONAL DOSAGE REGIMEN", "reason": "Taught in L02 (PK Calculations)"},
    {"heading": "DOSAGE REGIMEN", "reason": "Taught in L02 (PK Calculations)"},
    {"heading": "Initial Predictions of Volume of Distribution & Clearance", "reason": "Taught in L02 (PK Calculations)"},
    # beyond PA-level scope: chemistry and drug-industry detail with no clinical decision attached (Go deeper links to the pages)
    {"heading": "The Physical Nature of Drugs", "reason": "Beyond PA scope: molecular size and shape (the bonds and chirality that matter are taught)"},
    {"heading": "Rational Drug Design", "reason": "Beyond PA scope: how chemists design molecules"},
    {"heading": "Conflicts of Interest", "reason": "Beyond PA scope: drug-industry policy"},
]
