"""Textbook (Katzung 16e Ch. 37 pituitary, Ch. 38 thyroid, Ch. 39 adrenal) additions for L07.
Ch. 40 is taught in L11, Ch. 41 in L08, Ch. 42 in L04."""

PIT = "Pituitary: GH, Prolactin & ADH"
THY = "Thyroid & Antithyroid Drugs"
ADR = "Adrenocorticosteroids & Antagonists"

ADD = {
    PIT: {
        "moa": [
            ("Anterior pituitary hormones & their hypothalamic regulators: continuous (not pulsatile) GnRH analogs down-regulate GnRH receptors and suppress LH and FSH.", "p. 705"),
        ],
        "adverse": [
            ("Short stature from GH deficiency, Turner syndrome and other growth disorders is the main somatropin use; long-acting weekly forms (somapacitan) exist.", "p. 707; p. 721"),
            ("Growth hormone (somatropin) adverse effects are rare: pseudotumor cerebri, slipped capital femoral epiphysis, scoliosis progression, edema, hyperglycemia.", "p. 708"),
            ("Mecasermin (recombinant IGF-I for GH-unresponsive growth failure) causes hypoglycemia — give with a carbohydrate meal within 20 minutes.", "p. 708"),
            ("Octreotide: nausea, cramps, steatorrhea, gallstones, and vitamin B12 deficiency with long-term use.", "p. 709"),
        ],
        "pk": [
            ("Octreotide is 45 times more potent than somatostatin at inhibiting GH; somatostatin analogs come as long-acting monthly depots. Cabergoline’s half-life is about 65 hours.", "p. 709; p. 716"),
        ],
        "monitoring": [
            ("Pegvisomant does not lower GH secretion and may let the adenoma grow — monitor IGF-I and yearly pituitary MRI.", "p. 709"),
        ],
        "pearls": [
            ("Hyperprolactinemia causes hypogonadism — infertility, amenorrhea, galactorrhea in women; low libido and ED in men; macroadenomas can compress the optic nerves.", "p. 715"),
            ("Oxytocin (posterior pituitary) is given IV to start or augment labor; it also triggers milk letdown. Its half-life is about 5 minutes.", "p. 717"),
        ],
    },
    THY: {
        "moa": [
            ("Thyroid physiology: large doses of iodine inhibit organification (Wolff-Chaikoff block); amiodarone, contrast, β blockers and corticosteroids inhibit T4-to-T3 conversion.", "p. 724; p. 725"),
        ],
        "pk": [
            ("T4 has a 7-day half-life (allows once-daily dosing); T3 about 1 day. Enzyme inducers (rifampin, phenytoin, carbamazepine) speed thyroid hormone metabolism.", "p. 725; p. 726; p. 733"),
        ],
        "adverse": [
            ("Thioamide agranulocytosis occurs in 0.1–0.5%, usually within the first 90 days; PTU’s severe hepatitis (boxed warning) restricts it to the first trimester, thyroid storm, or methimazole reactions.", "p. 730; p. 731"),
            ("Iodides given alone can escape in 2–8 weeks and worsen thyrotoxicosis; avoid chronic iodide in pregnancy (fetal goiter).", "p. 732"),
        ],
        "contra": [
            ("Radioactive iodine (131I) is avoided in pregnancy and breastfeeding — it destroys the fetal thyroid.", "p. 732"),
        ],
        "indications": [
            ("Laboratory diagnosis of Graves disease: suppressed TSH with high free thyroid hormone. Management of Graves disease: antithyroid drugs, radioactive iodine, or thyroidectomy; methimazole preferred except in pregnancy and storm.", "p. 734"),
            ("Pregnant hypothyroid patients often need about 25–30% more levothyroxine; add two extra doses a week as soon as pregnancy is confirmed.", "p. 734"),
        ],
        "pearls": [
            ("Subclinical hypothyroidism (high TSH, normal hormones) affects 4–10%; amiodarone causes hypo- or hyperthyroidism (about 3% thyrotoxicosis) that persists after stopping.", "p. 734; p. 736"),
            ("Subacute thyroiditis releases stored hormone transiently; nontoxic goiter in the US is most often Hashimoto thyroiditis; neonatal Graves comes from maternal antibodies.", "p. 735; p. 736"),
        ],
    },
    ADR: {
        "adverse": [
            ("Adrenal suppression can occur after more than 2 weeks of corticosteroids; ACTH does not speed recovery.", "p. 750"),
            ("Long-term steroids: Cushingoid changes, myopathy, osteoporosis, peptic ulcer, masked infection, hypomania or psychosis, posterior subcapsular cataracts.", "p. 745; p. 750"),
        ],
        "indications": [
            ("Addison disease: hydrocortisone 20–30 mg daily (more during stress) plus fludrocortisone 0.05–0.2 mg/d.", "p. 747"),
            ("Dexamethasone suppression test diagnoses Cushing syndrome; antenatal glucocorticoids reduce neonatal respiratory distress.", "p. 748"),
        ],
        "pk": [
            ("Synthetic corticosteroids — pharmacokinetics & pharmacodynamics: potency and salt-retaining activity differ by agent (equivalent-dose table).", "p. 746; p. 747"),
            ("Selection of drug & dosage schedule: give steroids as a single morning dose; alternate-day dosing lessens suppression when disease control allows.", "p. 750; p. 751"),
        ],
        "pearls": [
            ("Older synthesis inhibitors — aminoglutethimide and trilostane — and the adrenolytic mitotane are rarely used; mifepristone (RU-486) is the receptor antagonist.", "p. 752; p. 753; p. 754"),
            ("Synthesis inhibitors & glucocorticoid antagonists: metyrapone is the only adrenal inhibitor usable in pregnancy; abiraterone treats refractory prostate cancer; mifepristone half-life about 20 hours.", "p. 754"),
        ],
    },
}

CONFLICTS = {}
DISCREPANCIES = [
    ("**Iodine timing in thyroid storm:** slides say at least 1 hour after PTU; the textbook only says not until thioamides have begun. Use the slide timing.", "S17; p. 732"),
]
CRAM = [
    ("T4 half-life", "7 days → once daily", "p. 733"),
    ("Agranulocytosis", "0.1–0.5%, first 90 days", "p. 731"),
    ("Iodide escape", "2–8 weeks if given alone", "p. 732"),
    ("Adrenal suppression", "After > 2 weeks of steroids", "p. 750"),
]
QUESTIONS = [
    dict(topic=THY, kind="vignette",
         stem="A hypothyroid woman on levothyroxine learns she is pregnant. What dose change does the textbook advise?",
         correct="Increase by about 25–30%",
         why_correct="Many pregnant hypothyroid patients need about 25–30% more thyroxine; add two extra doses a week as soon as pregnancy is confirmed (p. 734).",
         distractors=[("Stop it until delivery", "Fetal brain needs it (p. 733)."),
                      ("Halve the dose", "Needs rise (p. 734)."),
                      ("Switch to methimazole", "Wrong direction (p. 734)."),
                      ("No change; recheck after birth", "Monitor closely (p. 734).")],
         src="p. 733; p. 734"),
]
COMPARISONS = {}
DEEPER = {
    PIT: (37, 703, 721, "Hypothalamic and pituitary hormones in full"),
    THY: (38, 723, 738, "Thyroid physiology, replacement, antithyroid drugs and special problems"),
    ADR: (39, 740, 756, "Corticosteroids, mineralocorticoids and adrenal antagonists"),
}

_CH40 = ['Disturbances in Ovarian Function', 'Natural Estrogens', 'Synthetic Estrogens', 'Adverse Effects', 'Preparations & Dosages', 'Synthetic Progestins', 'Azurette, Kariva, Mircette, Viorele', 'Enpresse, Levonest, Myzilra, Triphasil, Tri-Levlen, Trivora', 'Casiant, Cyclessa, Cesia, Velivet', 'Implantable Progestin Preparation', 'OTHER OVARIAN HORMONES', 'HORMONAL CONTRACEPTION (ORAL, PARENTERAL, & IMPLANTED CONTRACEPTIVES)', 'Clinical Uses', 'Contraindications & Cautions', 'Contraception with Progestins Alone', 'Beneficial Effects of Oral Contraceptives', 'TAMOXIFEN & RELATED PARTIAL AGONIST ESTROGENS', 'DANAZOL', 'OTHER INHIBITORS', 'OVULATION-INDUCING AGENTS CLOMIPHENE', 'OTHER DRUGS USED IN OVULATORY DISORDERS', 'ANDROGENS & ANABOLIC STEROIDS', 'Physiologic Effects', 'Anabolic Action', 'ANDROGEN SUPPRESSION & ANTIANDROGENS ANDROGEN SUPPRESSION', 'ANTIANDROGENS', 'Steroid Synthesis Inhibitors', 'Precursors to Androgens', 'Receptor Inhibitors', 'CHEMICAL CONTRACEPTION IN MEN', 'GOSSYPOL', 'Toremifene Fareston']
_CH41 = ['THE ENDOCRINE PANCREAS', 'Insulin Secretion', 'Insulin Degradation', 'Circulating Insulin', 'The Insulin Receptor', 'Islet Mass Secretory Products', 'Effects of Insulin on Its Targets', 'Chemistry & Metabolism', 'Pharmacologic Effects of Glucagon', 'DIABETES MELLITUS', 'Other Specific Types of Diabetes Mellitus', 'Gestational Diabetes Mellitus', 'Insulin Preparations', 'Immunopathology of Insulin Therapy', 'MEDICATIONS FOR TREATMENT OF TYPE 2 DIABETES', 'Efficacy & Safety of the Sulfonylureas', 'FIRST-GENERATION SULFONYLUREAS', 'SECOND-GENERATION SULFONYLUREAS', 'MEGLITINIDE ANALOGS', 'BIGUANIDES', 'THIAZOLIDINEDIONES', 'DRUGS THAT AFFECT ABSORPTION OF GLUCOSE', 'GLUCAGON-LIKE PEPTIDE-1 (GLP-1) RECEPTOR AGONISTS', 'DIPEPTIDYL PEPTIDASE 4 (DPP-4) INHIBITORS', 'SODIUM-GLUCOSE CO-TRANSPORTER 2 (SGL T2) INHIBITORS', 'OTHER GLUCOSE-LOWERING DRUGS', 'Glycemic Targets', 'Prebreakfast Prelunch Predinner Bedtime', 'Benefits of Tight Glycemic Control in Diabetes', 'Chronic Complications of Diabetes']
_CH42 = ['BASIC PHARMACOLOGY', 'PRINCIPAL HORMONAL REGULATORS OF BONE MINERAL HOMEOSTASIS PARATHYROID HORMONE', 'FIBROBLAST GROWTH FACTOR 23', 'SECONDARY HORMONAL REGULATORS OF BONE MINERAL HOMEOSTASIS', 'CALCITONIN', 'GLUCOCORTICOIDS', 'ESTROGENS', 'Therapies for Osteoporosis', 'NONHORMONAL AGENTS AFFECTING BONE MINERAL HOMEOSTASIS BISPHOSPHONATES', 'DENOSUMAB', 'SCLEROSTIN ANTIBODIES', 'CALCIMIMETICS', 'THIAZIDE DIURETICS', 'FLUORIDE', 'STRONTIUM RANELATE', 'ABNORMAL SERUM CALCIUM & PHOSPHATE LEVELS HYPERCALCEMIA', 'Saline Diuresis', 'Gallium Nitrate', 'HYPOCALCEMIA', 'HYPERPHOSPHATEMIA', 'HYPOPHOSPHATEMIA', 'SPECIFIC DISORDERS INVOLVING BONE MINERAL–REGULATING HORMONES PRIMARY HYPERPARATHYROIDISM', 'HYPOPARATHYROIDISM', 'NUTRITIONAL VITAMIN D DEFICIENCY OR INSUFFICIENCY', 'CHRONIC KIDNEY DISEASE', 'Vitamin D Preparations', 'INTESTINAL OSTEODYSTROPHY', 'OSTEOPOROSIS', 'IDIOPATHIC INFANTILE HYPERCALCEMIA', 'NEPHROTIC SYNDROME', 'IDIOPATHIC HYPERCALCIURIA', 'OTHER DISORDERS OF BONE MINERAL HOMEOSTASIS PAGET DISEASE OF BONE', 'ENTERIC OXALURIA', 'SCLEROSTIN ANTIBODY', 'CALCIUM']
_LISTS = ["Conivaptan HCl Vaprisol", "Somapacitan Sogroya", "Tirosint, Tirosint-SOL, Unithroid", "GENERIC NAME AVAILABLE AS", "Betamethasone Celestone", "Mitotane Lysodren"]
READING_SKIP = (
    [{"heading": h, "reason": "Preparations list (brand names only, no teaching content)"} for h in _LISTS]
    + [{"heading": "Chemistry & Pharmacokinetics", "reason": "Beyond PA scope: gonadotropin and GnRH-analog chemistry for specialist fertility protocols"}]
    +
    [{"heading": h, "reason": "Taught in L11 (GU & Reproductive Session 1: gonadal hormones, Ch. 40)"} for h in _CH40]
    + [{"heading": h, "reason": "Taught in L08 (Endocrine Session 2: insulin and glucose-lowering drugs, Ch. 41)"} for h in _CH41]
    + [{"heading": h, "reason": "Taught in L04 (Musculoskeletal Session 2: bone mineral homeostasis, Ch. 42)"} for h in _CH42]
)
