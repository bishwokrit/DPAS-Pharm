"""Cumulative drug index — one entry per drug named in the course materials.
Every fact is cited (S = lecture slide as 'L01 S38', p. = Katzung page; tb=True marks textbook-only facts).
The site also auto-collects every place a drug is mentioned in the study guides, so entries stay short.
Add new drugs as each unit is taught (Unit 2+ drug-class lectures add mechanism, adverse effects, monitoring, etc.).
"""


def D(name, cls, tags, facts, aliases=(), unit=1, utd=None):
    # utd: optional exact UpToDate link; otherwise the site links an UpToDate search for the drug's name
    return {"name": name, "cls": cls, "tags": list(tags), "aliases": list(aliases), "unit": unit, **({"utd": utd} if utd else {}),
            "facts": [{"text": t, "src": s, "tb": tb} for t, s, tb in facts]}


T = True   # textbook-only
L = False  # lecture / study guide

DRUGS = [
    D("Acetaminophen", "Analgesic and antipyretic (not an NSAID)", ["Naming", "Toxic metabolite", "Antidote", "Analgesic", "OA"], [
        ("Relieves mild-to-moderate pain (central mechanism incompletely understood) and fever (hypothalamus); minimal peripheral anti-inflammatory effect.", "L03 S10", L),
        ("Reasonable first-line for mild osteoarthritis pain; generally safer first-line than an NSAID when NSAID red flags stack up.", "L03 S21; S24", L),
        ("Overdose: glutathione depleted → NAPQI accumulates → hepatocyte injury; antidote N-acetylcysteine (glutathione precursor).", "L03 S11; SG U2-R3", L),
        ("Combination cold, flu, and sleep products hide acetaminophen — always ask about ALL sources.", "L03 S12", L),
        ("Adults: generally no more than 4 g/day; 15 g may be fatal. Half-life 2–3 h.", "p. 694", T),
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
        ("Conventional DMARD (2 mg/kg/day for RA): becomes 6-thioguanine and suppresses B- and T-cell function; marrow suppression, GI upset, infection.", "p. 682; p. 683", T),
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
    D("Aspirin", "Salicylate NSAID (irreversible COX inhibitor)", ["Urine pH", "Saturable elimination", "Antiplatelet", "NSAID"], [
        ("Irreversibly blocks platelet COX, so the antiplatelet effect lasts 8–10 days; now used mainly at 81–325 mg daily as an antiplatelet.", "p. 677", T),
        ("Taking ibuprofen with it blocks aspirin’s irreversible platelet inhibition, limiting cardioprotection.", "p. 680", T),
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
        ("Acetaminophen overdose antidote: a glutathione precursor that replenishes glutathione to detoxify NAPQI.", "L03 S11; SG U2-R3", L),
        ("Acetaminophen overdose antidote — protective when given within 8–16 hours.", "p. 66", T),
    ], aliases=["NAC"]),
    D("Thalidomide", "Not covered in materials", ["Regulation"], [
        ("Caused about 10,000 birth defects; led to the Kefauver-Harris Amendments (1962), which required proof of efficacy.", "p. 16", T),
    ]),
    D("Isoniazid", "Not covered in materials", ["Pharmacogenomics"], [
        ("Slow NAT2 acetylators (~50% of people in the USA) are at higher toxicity risk.", "p. 70", T),
    ]),

    # ---------------------------------------------------------------- Unit 2 · L03: analgesics, NSAIDs, DMARDs
    D("Ibuprofen", "Nonselective NSAID (COX-1 and COX-2)", ["NSAID", "OA"], [
        ("Common first-line choice for mild-moderate pain.", "L03 S16", L),
        ("NSAID harms: GI (ulcer, bleeding), renal (AKI, fluid retention), cardiovascular (hypertension, events).", "L03 S19", L),
        ("≤1600 mg/day is analgesic but not anti-inflammatory; 2400 mg/day equals 4 g aspirin. Half-life 2 h.", "p. 677; p. 680", T),
        ("Blocks aspirin’s irreversible platelet effect when taken together; relatively contraindicated with nasal polyps or aspirin-induced bronchospasm.", "p. 680", T),
    ], aliases=["Advil", "Motrin"], unit=2),
    D("Naproxen", "Nonselective NSAID", ["NSAID"], [
        ("Longer half-life, twice-daily dosing.", "L03 S16", L),
        ("Half-life 12–17 h; more OTC GI bleeding than ibuprofen but a more favorable cardiovascular profile; avoid in hepatic impairment.", "p. 677; p. 680", T),
    ], aliases=["Aleve"], unit=2),
    D("Diclofenac", "Nonselective NSAID", ["NSAID", "Topical", "OA"], [
        ("Available in oral and topical formulations; topical NSAIDs give local relief with much lower systemic exposure.", "L03 S16; S24", L),
        ("1% gel is sold OTC for OA and muscular pain; raises aminotransferases more often than other NSAIDs.", "p. 679; p. 681", T),
    ], aliases=["Voltaren"], unit=2),
    D("Indomethacin", "Nonselective NSAID", ["NSAID"], [
        ("More potent, with more GI/CNS adverse effects.", "L03 S16", L),
        ("Headache in 11.7%; can aggravate depression, epilepsy, and parkinsonism.", "p. 680", T),
    ], unit=2),
    D("Ketorolac", "Nonselective NSAID (analgesic use)", ["NSAID", "Short-term"], [
        ("Short-term use only — significant GI/renal risk.", "L03 S16", L),
        ("Start IV, IM, or intranasal (not orally); max 120 mg/day; halve doses if over 65, under 50 kg, or with renal impairment; no more than 5 days.", "p. 694", T),
    ], unit=2),
    D("Celecoxib", "COX-2 selective NSAID", ["NSAID", "COX-2", "CV risk"], [
        ("Selectively inhibits COX-2: lower GI ulcer/bleeding risk, but higher cardiovascular event risk — the key trade-off.", "L03 S17-18; SG U2-R5", L),
        ("Renal risk similar to nonselective NSAIDs — selectivity does not protect the kidney.", "L03 S17", L),
        ("About 10–20 times more selective for COX-2; 100–200 mg bid; a CYP2C9 substrate that can interact with warfarin and raise lithium levels.", "p. 677; p. 679", T),
    ], aliases=["Celebrex"], unit=2),
    D("Tramadol", "Centrally acting analgesic (weak μ-opioid + 5-HT/NE reuptake)", ["Analgesic"], [
        ("No significant anti-inflammatory effect; up to 300 mg/day; risks serotonin syndrome and seizures.", "p. 694; p. 695", T),
    ], unit=2),
    D("Methotrexate", "Conventional synthetic DMARD (antifolate)", ["DMARD", "Weekly dosing", "Teratogen"], [
        ("The anchor drug for most RA regimens; inhibits dihydrofolate reductase, reducing immune cell proliferation at low RA doses.", "L03 S26-27; SG U2-M", L),
        ("Dosed WEEKLY, not daily — daily dosing can be fatal. Folate is routinely co-prescribed to reduce toxicity.", "L03 S27; SG U2-R7", L),
        ("Key adverse effects: hepatotoxicity, bone marrow suppression, pulmonary toxicity. Contraindicated in pregnancy (teratogenic).", "L03 S27", L),
        ("Starts at 7.5 mg weekly, rising to 15–25 mg weekly; most common toxicities are nausea and stomatitis.", "p. 688; p. 689", T),
    ], aliases=["MTX"], unit=2),
    D("Hydroxychloroquine", "Conventional synthetic DMARD (antimalarial)", ["DMARD"], [
        ("For milder RA; relatively favorable safety profile.", "L03 S26", L),
        ("Retinopathy risk: baseline eye exam, then annual screening after 5 years; takes 3–6 months to work; relatively safe in pregnancy.", "p. 684", T),
    ], aliases=["HCQ", "Plaquenil"], unit=2),
    D("Sulfasalazine", "Conventional synthetic DMARD", ["DMARD"], [
        ("Often used in combination regimens.", "L03 S26", L),
        ("About 30% stop it for toxicity (nausea, rash, neutropenia); reversible male infertility; relatively safe in pregnancy.", "p. 690", T),
    ], unit=2),
    D("Leflunomide", "Conventional synthetic DMARD (pyrimidine synthesis inhibitor)", ["DMARD"], [
        ("Alternative when methotrexate is not tolerated.", "L03 S26", L),
        ("Inhibits dihydroorotate dehydrogenase; diarrhea in 25%; half-life about 19 days (cholestyramine shortens it).", "p. 687; p. 688", T),
    ], unit=2),
    D("Adalimumab", "Biologic DMARD · TNF inhibitor", ["Biologic", "TNF", "Infection risk"], [
        ("Blocks TNF-α signaling; shared DMARD risk is immunosuppression → infection.", "L03 S28; S30; SG U2-R8", L),
        ("Screen for TB and hepatitis B/C and update vaccines before starting.", "L03 S30", L),
        ("Boxed warning (all TNF inhibitors): malignancy, especially lymphoma; also heart failure, demyelination, lupus-like syndrome.", "p. 690; p. 692", T),
    ], aliases=["Humira"], unit=2),
    D("Etanercept", "Biologic DMARD · TNF inhibitor (receptor fusion protein)", ["Biologic", "TNF"], [
        ("Blocks TNF-α signaling.", "L03 S28; SG U2-R8", L),
        ("Fusion protein of two TNF p75 receptors; latent TB activation is lower than with other TNF blockers.", "p. 691; p. 692", T),
    ], aliases=["Enbrel"], unit=2),
    D("Infliximab", "Biologic DMARD · TNF inhibitor (chimeric antibody)", ["Biologic", "TNF"], [
        ("Blocks TNF-α signaling.", "L03 S28; SG U2-R8", L),
        ("IV infusion at weeks 0, 2, and 6, then every 8 weeks; methotrexate reduces antibodies against it.", "p. 692", T),
    ], aliases=["Remicade"], unit=2),
    D("Tocilizumab", "Biologic DMARD · IL-6 receptor inhibitor", ["Biologic", "IL-6"], [
        ("Blocks interleukin-6 receptor signaling.", "L03 S28; SG U2-R8", L),
        ("Raises liver enzymes and lipids; stimulates CYP450 (watch cyclosporine, warfarin).", "p. 692; p. 693", T),
    ], aliases=["Actemra"], unit=2),
    D("Rituximab", "Biologic DMARD · B-cell (CD20) targeted therapy", ["Biologic", "B cell"], [
        ("Depletes or modulates B lymphocytes.", "L03 S28; SG U2-R8", L),
        ("Rash with the first dose in about 30%; hepatitis B reactivation; two 1000 mg infusions 2 weeks apart for RA.", "p. 689", T),
    ], aliases=["Rituxan"], unit=2),
    D("Abatacept", "Biologic DMARD · T-cell costimulation modulator", ["Biologic", "T cell"], [
        ("Blocks the second signal needed for T-cell activation.", "L03 S28; SG U2-M; SG U2-R8", L),
        ("Fusion protein (CTLA-4 + IgG1 Fc) blocking CD80/CD86–CD28; avoid live vaccines up to 3 months after stopping.", "p. 681; p. 682", T),
    ], aliases=["Orencia"], unit=2),
    D("Tofacitinib", "Targeted synthetic DMARD · JAK inhibitor", ["JAK", "Boxed warning"], [
        ("Oral JAK 1, 2, 3 inhibitor; RA dose 5 mg twice daily. Boxed warning (all JAK inhibitors): VTE, MACE, cancer; more herpes zoster.", "p. 686; p. 687", T),
    ], aliases=["Xeljanz"], unit=2),
]

# where each drug-class label comes from
CLASS_SOURCES = {"Albuterol": "L01 S26", "Warfarin": "p. 72", "Propranolol": "p. 25; p. 41", "Metoprolol": "p. 41", "Morphine": "p. 81",
                 "Codeine": "p. 81", "Clopidogrel": "p. 81", "Azathioprine": "L02 S33; p. 83", "Heparin": "p. 26", "Protamine": "p. 26",
                 "Phenoxybenzamine": "p. 25", "Rifampin": "p. 63", "St. John's wort": "p. 72", "Grapefruit juice": "p. 48; p. 64",
                 "Ketoconazole": "p. 64", "Ritonavir": "p. 64", "N-acetylcysteine": "p. 66",
                 "Acetaminophen": "L03 S10", "Aspirin": "p. 675; p. 677", "Ibuprofen": "L03 S16", "Naproxen": "L03 S16", "Diclofenac": "L03 S16",
                 "Indomethacin": "L03 S16", "Ketorolac": "L03 S16", "Celecoxib": "L03 S17", "Tramadol": "p. 694", "Methotrexate": "L03 S26-27",
                 "Hydroxychloroquine": "L03 S26; p. 684", "Sulfasalazine": "L03 S26", "Leflunomide": "L03 S26; p. 687", "Adalimumab": "L03 S28",
                 "Etanercept": "L03 S28", "Infliximab": "L03 S28", "Tocilizumab": "L03 S28", "Rituximab": "L03 S28", "Abatacept": "L03 S28",
                 "Tofacitinib": "p. 686"}
for _d in DRUGS:
    _d["cls_src"] = CLASS_SOURCES.get(_d["name"], "")
