"""Study-guide extras for L08 (summary, flows, cram sheet). Imported by author_L08.py."""

TEASER = "Today: how combined contraception switches off the reproductive axis, SERMs and androgen drugs, every glucose-lowering class mapped to where it acts, and the two opposite parathyroid problems. The recall quiz spans both endocrine sessions."

SUMMARY = [
    ("**Combined contraception** suppresses GnRH/FSH/LH; no estrogen with prior VTE/stroke, **smoker ≥ 35**, **migraine with aura**, estrogen-sensitive cancer, uncontrolled hypertension → progestin-only. Inducers (rifampin) need backup.", "S5; S6"),
    ("**Tamoxifen** blocks breast but activates endometrium (report bleeding); **raloxifene** activates bone, blocks endometrium; both raise VTE. **Finasteride** lowers DHT and halves PSA.", "S7; S8; S9"),
    ("**Insulin**: rapid (lispro, aspart), short (regular — the only IV insulin), NPH, basal (glargine, detemir, degludec); main risk **hypoglycemia** (rule of 15; beta-blockers mask it).", "S12; S13"),
    ("**Metformin** first-line (avoid eGFR < 30, hold for contrast, B12); **sulfonylureas** highest oral hypoglycemia; **TZDs** fluid/heart failure; **SGLT2** genital infections, euglycemic DKA, cardiorenal benefit.", "S14; S15; S16"),
    ("**GLP-1 RAs** (weight loss; no MTC/MEN2) and **DPP-4 inhibitors** (weight neutral) work glucose-dependently — low hypoglycemia; older adult who falls → DPP-4 or SGLT2.", "S18; S19; S21"),
    ("**Hyperparathyroidism** → cinacalcet (watch hypocalcemia); **hypoparathyroidism** → calcitriol + calcium (watch hypercalcemia).", "S25; S27"),
]

FLOWS = {
    "Gonadal Hormones & Inhibitors": [
        {"title": "Can this patient take estrogen?", "steps": ["Prior VTE or stroke?", "Smoker aged 35 or older?", "Migraine with aura?", "Estrogen-sensitive cancer, uncontrolled HTN, liver disease?", "Any yes → progestin-only (minipill, DMPA, levonorgestrel IUD)"], "src": "S5; S6"},
    ],
    "Non-Insulin Glucose-Lowering Drugs": [
        {"title": "Add-on after metformin", "steps": ["HbA1c above goal on metformin", "Older, lives alone, falls? → avoid sulfonylurea", "Heart failure or CKD → SGLT2 inhibitor", "Weight loss wanted → GLP-1 RA (no MTC/MEN2)", "Low-risk, weight neutral → DPP-4 inhibitor"], "src": "S16; S18; S21"},
    ],
    "Parathyroid Disorders": [
        {"title": "Which parathyroid drug?", "steps": ["Check PTH and calcium", "High PTH (CKD, dialysis) → cinacalcet; watch hypocalcemia", "Low PTH, low calcium (post-thyroidectomy) → calcitriol + calcium", "Refractory → recombinant PTH 1-84", "Watch hypercalcemia on replacement"], "src": "S25; S27"},
    ],
}

CRAM = [
    ("Estrogen contraindications", "VTE/stroke, smoker ≥ 35, migraine with aura, estrogen-sensitive cancer, uncontrolled HTN, liver disease", "S5"),
    ("Contraception + rifampin", "Backup contraception", "S6; S67"),
    ("Tamoxifen", "Breast antagonist; endometrial agonist; CYP2D6 inhibitors blunt it", "S7; S8"),
    ("Raloxifene", "Bone agonist; endometrium blocked; VTE; not for breast cancer treatment", "S7; S8"),
    ("Finasteride", "↓ DHT; PSA halved → double it; teratogenic tablets", "S9"),
    ("Testosterone", "Monitor hematocrit, PSA, lipids", "S7; S9"),
    ("Insulin buckets", "Rapid lispro/aspart · short regular · NPH · basal glargine/detemir/degludec", "S12"),
    ("Only IV insulin", "Regular", "S12 (notes)"),
    ("Hypoglycemia", "Rule of 15; beta-blockers mask it; glucagon/dextrose rescue", "S13; S67"),
    ("Metformin", "AMPK, ↓ gluconeogenesis; eGFR < 30 avoid; contrast hold; B12", "S15"),
    ("Sulfonylurea risk", "Highest oral hypoglycemia (forced K-ATP closure)", "S14; S35"),
    ("TZD risk", "Fluid retention, heart failure", "S14"),
    ("SGLT2 risks", "Genital yeast, volume depletion, euglycemic DKA, Fournier", "S16"),
    ("GLP-1 RA", "Weight loss; pancreatitis; no MTC/MEN2; never with DPP-4", "S18; S19"),
    ("Cinacalcet", "CaSR activator; hypocalcemia, QT; CYP2D6 inhibitor", "S26"),
    ("Hypoparathyroidism", "Calcitriol + calcium; watch hypercalcemia", "S25; S35"),
]
