"""Cumulative drug index — one entry per drug named in the course materials.
Every fact is cited (S = lecture slide as 'L01 S38', p. = Katzung page; tb=True marks textbook-only facts).
The site also auto-collects every place a drug is mentioned in the study guides, so entries stay short.
Add new drugs as each unit is taught (Unit 2+ drug-class lectures add mechanism, adverse effects, monitoring, etc.).
"""


def D(name, cls, tags, facts, aliases=(), unit=1):
    return {"name": name, "cls": cls, "tags": list(tags), "aliases": list(aliases), "unit": unit,
            "facts": [{"text": t, "src": s, "tb": tb} for t, s, tb in facts]}


T = True   # textbook-only
L = False  # lecture / study guide

DRUGS = [
    D("Acetaminophen", "Not covered in materials", ["Naming", "Toxic metabolite", "Antidote"], [
        ("Generic name; sold as Tylenol and many store brands — two brands can hide the same ingredient and cause double-dosing.", "L01 S7; S9; SG U1-R2", L),
        ("Normal Phase I metabolism makes a toxic metabolite, NAPQI.", "L02 S4 (notes)", L),
        ("Mostly conjugated (glucuronide/sulfate); in overdose glutathione is depleted and NAPQI injures the liver.", "p. 66", T),
        ("N-acetylcysteine given within 8–16 hours protects against fulminant hepatotoxicity.", "p. 66", T),
    ], aliases=["Tylenol", "NAPQI"]),
    D("Albuterol", "Selective β2-adrenergic receptor agonist", ["Receptors", "Inhaled"], [
        ("Binds and activates β2 → ↑ intracellular cAMP → bronchial smooth muscle relaxes → bronchodilation.", "L01 S26", L),
        ("The lecture's model for receptor-to-response logic you reuse for every agonist.", "L01 S26", L),
    ]),
    D("Warfarin", "Anticoagulant", ["Narrow TI", "Protein-bound", "Pharmacogenomics", "CYP interactions"], [
        ("Classic narrow-therapeutic-index drug — careful dosing and blood-level monitoring.", "L01 S38; SG U1-R7", L),
        ("99% protein-bound; half-life about 37 h.", "p. 45", T),
        ("Dose requirements vary up to 20-fold; CYP2C9 and VKORC1 genotypes explain much of it.", "p. 90", T),
        ("Inducers (e.g., barbiturates, St. John's wort) lower its level; stopping the inducer raises it and can cause bleeding.", "p. 72", T),
    ]),
    D("Lithium", "Not covered in materials", ["Narrow TI", "Renal dosing"], [
        ("Classic narrow-TI drug requiring blood-level monitoring.", "L01 S38; SG U1-R7", L),
        ("Renally cleared, narrow-TI — needs dose or interval adjustment in renal impairment.", "L02 S15", L),
        ("About 95% excreted unchanged in urine, 0% protein-bound; target ~0.7 mEq/L, toxic above 2 mEq/L; half-life ~22 h.", "p. 44", T),
    ]),
    D("Digoxin", "Not covered in materials", ["Narrow TI", "High Vd", "Renal dosing", "Transporters"], [
        ("Classic narrow-TI drug requiring blood-level monitoring.", "L01 S38; SG U1-R7", L),
        ("Very high Vd — mostly sequestered in tissue, not plasma.", "L01 S52 (notes)", L),
        ("Renally cleared — adjust dose or interval in renal impairment.", "L02 S15", L),
        ("Vd ~500 L, half-life ~39 h; target ~1 ng/mL, toxic above 2 ng/mL.", "p. 44", T),
        ("Inhibiting P-glycoprotein (MDR1) raises digoxin blood levels.", "p. 9", T),
    ]),
    D("Phenytoin", "Not covered in materials", ["Narrow TI", "Saturable elimination", "CYP inducer"], [
        ("Classic narrow-TI drug requiring blood-level monitoring.", "L01 S38; SG U1-R7", L),
        ("Capacity-limited (saturable) elimination — clearance falls as concentration rises.", "p. 47", T),
        ("Target ~10 mg/L, toxic above 20 mg/L; 89% protein-bound.", "p. 45", T),
        ("A CYP inducer.", "p. 63; p. 64", T),
    ]),
    D("Nitroglycerin", "Not covered in materials", ["First-pass", "Routes"], [
        ("Large first-pass effect — needs a higher oral dose or a non-oral route.", "L01 S51; SG U1-R9", L),
        ("Sublingual dosing enters systemic veins directly, bypassing the portal vein and liver.", "L01 S55", L),
    ]),
    D("Propranolol", "Nonselective β-adrenoceptor antagonist (β blocker)", ["First-pass", "Receptors", "Competitive antagonist"], [
        ("Large first-pass effect — much higher oral than IV dose for the same exposure.", "L01 S51; SG U1-R9", L),
        ("Competitive antagonist: exercise or stress catecholamines can overcome a fixed dose.", "p. 25", T),
        ("Slows heart rate markedly in pheochromocytoma but not a trained runner's resting rate.", "p. 39", T),
        ("Can cause bronchoconstriction in asthma (blocks β2) — a β1-selective blocker is an alternative.", "p. 41", T),
    ]),
    D("Metoprolol", "β1-selective adrenoceptor antagonist", ["Receptors"], [
        ("Binds preferentially to β1 (heart) with lower affinity for β2 — an alternative to propranolol in a patient with asthma.", "p. 41", T),
    ]),
    D("Morphine", "Opioid analgesic", ["First-pass", "Pharmacogenomics"], [
        ("Large first-pass effect.", "L01 S51; SG U1-R9", L),
        ("Active metabolite of codeine, about 200× more potent than codeine.", "p. 81", T),
    ]),
    D("Codeine", "Opioid (prodrug)", ["Pharmacogenomics", "Prodrug"], [
        ("Needs CYP2D6 activation; CYP2D6 variation changes its effect.", "L02 S33; SG U1-R12", L),
        ("CYP2D6 converts it to morphine; poor metabolizers get little relief, ultrarapid metabolizers risk toxicity.", "p. 81", T),
        ("CPIC: use an alternative analgesic in CYP2D6 poor and ultrarapid metabolizers.", "p. 81; p. 82", T),
    ]),
    D("Clopidogrel", "Antiplatelet (prodrug)", ["Pharmacogenomics", "Prodrug"], [
        ("CYP2C19 variation affects its activation.", "L02 S33", L),
        ("About 85% of a dose is inactivated by esterases; CYP2C19 forms the active metabolite.", "p. 81", T),
        ("CYP2C19 poor/intermediate metabolizers after PCI: CPIC recommends prasugrel or ticagrelor.", "p. 81; p. 82", T),
    ]),
    D("Azathioprine", "Thiopurine (immunosuppressant)", ["Pharmacogenomics"], [
        ("TPMT deficiency raises thiopurine toxicity risk.", "L02 S33; SG U1-R12", L),
        ("TPMT intermediate activity: start at 30–70% of the target dose; deficient: drastically reduce or use an alternative.", "p. 83", T),
    ]),
    D("Allopurinol", "Not covered in materials", ["Pharmacogenomics", "Hypersensitivity"], [
        ("HLA-B*5801 carriers have a sharply higher risk of severe hypersensitivity.", "L02 S35-36; SG U1-R12", L),
        ("Suggested alternative when rasburicase is contraindicated (G6PD deficiency).", "p. 83", T),
    ]),
    D("Abacavir", "Not covered in materials", ["Pharmacogenomics", "Hypersensitivity"], [
        ("Contraindicated in HLA-B*57:01-positive patients (hypersensitivity).", "p. 83; p. 88", T),
    ]),
    D("Rasburicase", "Not covered in materials", ["Pharmacogenomics"], [
        ("Contraindicated in G6PD deficiency; use an alternative such as allopurinol.", "p. 83", T),
    ]),
    D("Aspirin", "Not covered in materials", ["Urine pH", "Saturable elimination"], [
        ("Overdose: alkalinizing the urine traps ionized drug and blocks reabsorption.", "L02 S14 (notes)", L),
        ("A weak acid; sodium bicarbonate alkalinizes blood and urine, cutting tissue entry and speeding renal clearance.", "p. 20", T),
        ("Capacity-limited (saturable) elimination.", "p. 47", T),
    ]),
    D("Heparin", "Anticoagulant", ["Routes", "Reversal"], [
        ("Commonly given subcutaneously (slower, steady absorption).", "L01 S49", L),
        ("Reversed by protamine, which binds it directly (chemical antagonism).", "p. 26", T),
    ]),
    D("Protamine", "Heparin reversal agent", ["Reversal", "Antagonism"], [
        ("Positively charged protein that binds negatively charged heparin — chemical antagonism, no receptor involved.", "p. 26", T),
    ]),
    D("Insulin", "Not covered in materials", ["Routes"], [
        ("Commonly given subcutaneously (slower, steady absorption).", "L01 S49", L),
    ]),
    D("Theophylline", "Not covered in materials", ["PK math"], [
        ("Loading dose example: Vd 35 L × target 10 mg/L = 350 mg for a 70-kg adult.", "p. 52", T),
    ]),
    D("Phenoxybenzamine", "Irreversible α-adrenoceptor antagonist", ["Antagonism"], [
        ("Irreversible: blockade lasts until new receptors are made — used for pheochromocytoma hypertension.", "p. 25", T),
    ]),
    D("Rifampin", "CYP inducer", ["CYP inducer"], [
        ("Induces CYP enzymes, speeding metabolism of substrates (levels fall).", "p. 63; p. 64", T),
    ]),
    D("St. John's wort", "Herbal product · CYP3A4 inducer", ["CYP inducer"], [
        ("Induces CYP3A4 — lowers levels of oral contraceptives, warfarin, cyclosporine, and others.", "p. 72", T),
    ], aliases=["St John's wort", "St. John’s wort"]),
    D("Grapefruit juice", "CYP3A4 / P-glycoprotein inhibitor", ["CYP inhibitor"], [
        ("Inhibits gut-wall CYP3A4 and P-glycoprotein, raising absorption of some drugs.", "p. 48; p. 64", T),
    ], aliases=["grapefruit"]),
    D("Ketoconazole", "CYP3A4 inhibitor", ["CYP inhibitor"], [
        ("CYP3A4 inhibitor — raises levels of CYP3A4 substrates.", "p. 64", T),
    ]),
    D("Ritonavir", "CYP3A4 inhibitor", ["CYP inhibitor"], [
        ("Potent CYP3A4 inhibitor (acutely).", "p. 64; p. 72", T),
    ]),
    D("N-acetylcysteine", "Antidote", ["Antidote"], [
        ("Acetaminophen overdose antidote — protective when given within 8–16 hours.", "p. 66", T),
    ], aliases=["NAC"]),
    D("Thalidomide", "Not covered in materials", ["Regulation"], [
        ("Caused about 10,000 birth defects; led to the Kefauver-Harris Amendments (1962), which required proof of efficacy.", "p. 16", T),
    ]),
    D("Isoniazid", "Not covered in materials", ["Pharmacogenomics"], [
        ("Slow NAT2 acetylators (~50% of people in the USA) are at higher toxicity risk.", "p. 70", T),
    ]),
]

# where each drug-class label comes from
CLASS_SOURCES = {"Albuterol": "L01 S26", "Warfarin": "p. 72", "Propranolol": "p. 25; p. 41", "Metoprolol": "p. 41", "Morphine": "p. 81",
                 "Codeine": "p. 81", "Clopidogrel": "p. 81", "Azathioprine": "L02 S33; p. 83", "Heparin": "p. 26", "Protamine": "p. 26",
                 "Phenoxybenzamine": "p. 25", "Rifampin": "p. 63", "St. John's wort": "p. 72", "Grapefruit juice": "p. 48; p. 64",
                 "Ketoconazole": "p. 64", "Ritonavir": "p. 64", "N-acetylcysteine": "p. 66"}
for _d in DRUGS:
    _d["cls_src"] = CLASS_SOURCES.get(_d["name"], "")
