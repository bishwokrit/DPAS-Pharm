"""Textbook (Katzung 16e Ch. 41, pancreatic hormones and glucose-lowering drugs) additions for L08.
Ch. 37–39 are taught in Endocrine Session 1 (L07); Ch. 40 gonadal hormones in GU Session 1 (L11); Ch. 42 bone mineral homeostasis in L04."""

INS = "Insulin"
NIG = "Non-Insulin Glucose-Lowering Drugs"

ADD = {
    INS: {
        "overview": [
            ("Diabetes mellitus has four categories: type 1 (beta-cell destruction, absolute insulin deficiency), type 2, other specific types, and gestational diabetes (about 7% of US pregnancies).", "p. 789; p. 790"),
            ("Diagnosis: fasting plasma glucose ≥126 mg/dL or HbA1c ≥6.5%, confirmed by repeat testing.", "p. 790"),
        ],
        "pk": [
            ("Insulin preparations: lispro/aspart onset 5–15 min, 3–4 h duration; regular 30–60 min, 6–8 h; NPH 2–4 h, peak 6–7 h; glargine about 24 h, peakless.", "p. 791; p. 793"),
            ("Glargine is acidic (pH 4.0) — never mix it in the same syringe with other insulins.", "p. 793; p. 794"),
        ],
        "adverse": [
            ("Rotate injection sites to avoid lipohypertrophy; insulin allergy (IgE) is rare.", "p. 794; p. 795"),
        ],
        "indications": [
            ("Glucagon (IM, SC, IV, or 3-mg nasal powder) treats severe hypoglycemia when oral glucose is impossible; place the patient on their side (vomiting).", "p. 789"),
        ],
    },
    NIG: {
        "contra": [
            ("Metformin: full dose at eGFR 45–60, cautious at 30–45, contraindicated below 30; avoid in decompensated liver failure; check renal function at least annually.", "p. 798"),
            ("Thiazolidinediones are contraindicated in NYHA class III and IV heart failure.", "p. 799"),
        ],
        "adverse": [
            ("Sulfonylureas: hypoglycemia and weight gain; elderly patients are at particular risk.", "p. 796; p. 797"),
            ("Acarbose (an alpha-glucosidase inhibitor, a drug that affects absorption of glucose): treat hypoglycemia with glucose, not sucrose.", "p. 799"),
        ],
        "indications": [
            ("Semaglutide lowers HbA1c 1.5–1.8%; liraglutide 3 mg and semaglutide 2.4 mg are approved for weight loss without diabetes.", "p. 800"),
            ("SGLT2 inhibitors lower HbA1c 0.5–1%, cause 2–5 kg weight loss, and reduce heart-failure events (dapagliflozin hazard ratio 0.74).", "p. 801; p. 802"),
        ],
        "pk": [
            ("Sitagliptin: reduce dose in renal impairment (50 mg at eGFR 30–50, 25 mg below 30). Exenatide is not approved below eGFR 30.", "p. 800; p. 801"),
        ],
        "pearls": [
            ("SGLT2 inhibitors: not recommended for glycemic control below eGFR 45, contraindicated below 30 (for glucose).", "p. 802"),
        ],
    },
}

CONFLICTS = {
    NIG: [
        {"topic": "Metformin and eGFR",
         "slides": {"text": "Avoid when eGFR is below 30.", "src": "S15"},
         "textbook": {"text": "Full use at 45–60, cautious at 30–45 (lower doses), contraindicated below 30.", "src": "p. 798"}},
    ],
}

DISCREPANCIES = [
    ("**Rapid-acting insulin onset:** slides say about 15 minutes; the textbook gives 5–15 minutes. Same practical rule: dose with the meal.", "S12; p. 791"),
]

CRAM = [
    ("Diabetes diagnosis", "FPG ≥ 126 or HbA1c ≥ 6.5%, repeated", "p. 790"),
    ("Glargine", "pH 4.0 — never mix", "p. 793"),
    ("Metformin by eGFR", "45–60 full · 30–45 caution · < 30 contraindicated", "p. 798"),
    ("TZD contraindication", "NYHA III–IV heart failure", "p. 799"),
    ("Acarbose hypoglycemia", "Treat with glucose, not sucrose", "p. 799"),
]

QUESTIONS = [
    dict(topic=NIG, kind="vignette",
         stem="A patient with type 2 diabetes has NYHA class III heart failure. Which drug is contraindicated?",
         correct="Pioglitazone",
         why_correct="Thiazolidinediones cause fluid retention and are contraindicated in NYHA class III and IV heart failure (p. 799).",
         distractors=[("Empagliflozin", "Reduces heart-failure events (p. 802)."),
                      ("Metformin", "Not the HF contraindication (p. 798)."),
                      ("Sitagliptin", "Not contraindicated here (p. 801)."),
                      ("Semaglutide", "Not contraindicated here (p. 800).")],
         src="p. 799"),
]

COMPARISONS = {}

DEEPER = {
    INS: (41, 789, 795, "Diabetes types, diagnosis and every insulin preparation"),
    NIG: (41, 795, 806, "Every oral and injectable glucose-lowering class, targets and complications"),
}

_CH37_39 = ['ANTERIOR PITUITARY HORMONES & THEIR HYPOTHALAMIC REGULATORS', 'ANTERIOR PITUITARY & HYPOTHALAMIC HORMONE RECEPTORS', 'GROWTH HORMONE (SOMATOTROPIN)', 'Short Stature', 'Other Uses of Growth Hormone', 'Objective Clinical Condition', 'Toxicity & Contraindications', 'MECASERMIN', 'GROWTH HORMONE ANTAGONISTS', 'Somatostatin Analogs', 'Chemistry & Pharmacokinetics', 'GONADOTROPIN-RELEASING HORMONE & ITS ANALOGS', 'Clinical Pharmacology', 'GnRH RECEPTOR ANTAGONISTS', 'PROLACTIN', 'DOPAMINE AGONISTS', 'POSTERIOR PITUITARY HORMONES', 'OXYTOCIN', 'OXYTOCIN ANTAGONIST', 'VASOPRESSIN (ANTIDIURETIC HORMONE, ADH)', 'VASOPRESSIN RECEPTOR ANTAGONISTS', 'GH RECEPTOR ANTAGONIST', 'OXYTOCIN RECEPTOR ANTAGONIST', 'Conivaptan HCl Vaprisol', 'Somapacitan Sogroya', 'THYROID PHYSIOLOGY', 'Iodide Metabolism', 'Biosynthesis of Thyroid Hormones', 'Transport of Thyroid Hormones', 'Evaluation of Thyroid Function', 'Mechanism of Action', 'Effects of Thyroid Hormones', 'Thyroid Preparations', 'ANTITHYROID AGENTS', 'THIOAMIDES', 'System Thyrotoxicosis Hypothyroidism', 'ANION INHIBITORS', 'IODIDES', 'Clinical Use of Iodide', 'RADIOACTIVE IODINE', 'ADRENOCEPTOR-BLOCKING AGENTS', 'CLINICAL PHARMACOLOGY OF THYROID & ANTITHYROID DRUGS HYPOTHYROIDISM', 'Cause Pathogenesis Goiter Degree of Hypothyroidism', 'MANAGEMENT OF HYPOTHYROIDISM', 'HYPERTHYROIDISM', 'Laboratory Diagnosis', 'Management of Graves Disease', 'SUBACUTE THYROIDITIS', 'Thyroid Storm', 'Neonatal Graves Disease', 'SUBCLINICAL HYPERTHYROIDISM', 'Amiodarone-Induced Thyrotoxicosis', 'NONTOXIC GOITER', 'THYROID NEOPLASMS', 'Subclinical Hypothyroidism and Hyperthyroidism', 'Antithyroid Agents and Management of Hyperthyroidism', 'The Effects of Drugs on Thyroid Function', 'GENERIC NAME AVAILABLE AS THYROID AGENTS', 'Tirosint, Tirosint-SOL, Unithroid', 'Thyroid Hormone Action', 'ADRENOCORTICOSTEROIDS', 'SYNTHETIC CORTICOSTEROIDS', 'PHARMACOKINETICS', 'Equivalent Oral', 'PHARMACODYNAMICS', 'Disorder Examples', 'Selection of Drug & Dosage Schedule', 'MINERALOCORTICOIDS (ALDOSTERONE, DEOXYCORTICOSTERONE, FLUDROCORTISONE)', 'ADRENAL ANDROGENS', 'SYNTHESIS INHIBITORS & GLUCOCORTICOID ANTAGONISTS', 'AMINOGLUTETHIMIDE', 'KETOCONAZOLE', 'METYRAPONE', 'TRILOSTANE', 'ABIRATERONE', 'MIFEPRISTONE (RU-486)', 'MITOTANE', 'MINERALOCORTICOID ANTAGONISTS', 'GENERIC NAME AVAILABLE AS', 'Betamethasone Celestone', 'Mitotane Lysodren']
_CH40 = ['Disturbances in Ovarian Function', 'Natural Estrogens', 'Synthetic Estrogens', 'Adverse Effects', 'Preparations & Dosages', 'Synthetic Progestins', 'Azurette, Kariva, Mircette, Viorele', 'Enpresse, Levonest, Myzilra, Triphasil, Tri-Levlen, Trivora', 'Casiant, Cyclessa, Cesia, Velivet', 'Implantable Progestin Preparation', 'OTHER OVARIAN HORMONES', 'HORMONAL CONTRACEPTION (ORAL, PARENTERAL, & IMPLANTED CONTRACEPTIVES)', 'Clinical Uses', 'Contraindications & Cautions', 'Contraception with Progestins Alone', 'Beneficial Effects of Oral Contraceptives', 'TAMOXIFEN & RELATED PARTIAL AGONIST ESTROGENS', 'DANAZOL', 'OTHER INHIBITORS', 'OVULATION-INDUCING AGENTS CLOMIPHENE', 'OTHER DRUGS USED IN OVULATORY DISORDERS', 'ANDROGENS & ANABOLIC STEROIDS', 'Physiologic Effects', 'Anabolic Action', 'ANDROGEN SUPPRESSION & ANTIANDROGENS ANDROGEN SUPPRESSION', 'ANTIANDROGENS', 'Steroid Synthesis Inhibitors', 'Precursors to Androgens', 'Receptor Inhibitors', 'CHEMICAL CONTRACEPTION IN MEN', 'GOSSYPOL', 'Toremifene Fareston']
_CH42 = ['BASIC PHARMACOLOGY', 'PRINCIPAL HORMONAL REGULATORS OF BONE MINERAL HOMEOSTASIS PARATHYROID HORMONE', 'FIBROBLAST GROWTH FACTOR 23', 'SECONDARY HORMONAL REGULATORS OF BONE MINERAL HOMEOSTASIS', 'CALCITONIN', 'GLUCOCORTICOIDS', 'ESTROGENS', 'Therapies for Osteoporosis', 'NONHORMONAL AGENTS AFFECTING BONE MINERAL HOMEOSTASIS BISPHOSPHONATES', 'DENOSUMAB', 'SCLEROSTIN ANTIBODIES', 'CALCIMIMETICS', 'THIAZIDE DIURETICS', 'FLUORIDE', 'STRONTIUM RANELATE', 'ABNORMAL SERUM CALCIUM & PHOSPHATE LEVELS HYPERCALCEMIA', 'Saline Diuresis', 'Gallium Nitrate', 'HYPOCALCEMIA', 'HYPERPHOSPHATEMIA', 'HYPOPHOSPHATEMIA', 'SPECIFIC DISORDERS INVOLVING BONE MINERAL–REGULATING HORMONES PRIMARY HYPERPARATHYROIDISM', 'HYPOPARATHYROIDISM', 'NUTRITIONAL VITAMIN D DEFICIENCY OR INSUFFICIENCY', 'CHRONIC KIDNEY DISEASE', 'Vitamin D Preparations', 'INTESTINAL OSTEODYSTROPHY', 'OSTEOPOROSIS', 'IDIOPATHIC INFANTILE HYPERCALCEMIA', 'NEPHROTIC SYNDROME', 'IDIOPATHIC HYPERCALCIURIA', 'OTHER DISORDERS OF BONE MINERAL HOMEOSTASIS PAGET DISEASE OF BONE', 'ENTERIC OXALURIA', 'SCLEROSTIN ANTIBODY', 'CALCIUM']

READING_SKIP = (
    [{"heading": h, "reason": "Taught in L07 (Endocrine Session 1: pituitary, thyroid and adrenal, Ch. 37–39)"} for h in _CH37_39]
    + [{"heading": h, "reason": "Taught in L11 (GU & Reproductive Session 1: gonadal hormones, Ch. 40)"} for h in _CH40]
    + [{"heading": h, "reason": "Taught in L04 (Musculoskeletal Session 2: bone mineral homeostasis, Ch. 42)"} for h in _CH42]
    + [{"heading": "Islet Mass Secretory Products", "reason": "Beyond PA scope: islet cell-type table (physiology, no prescribing decision)"},
       {"heading": "Prebreakfast Prelunch Predinner Bedtime", "reason": "Table column heading (glucose targets table); targets are taught under Glycemic Targets"}]
)
