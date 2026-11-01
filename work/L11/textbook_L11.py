"""Textbook (Katzung 16e Ch. 40, gonadal hormones; Ch. 41 biguanides and GLP-1 agonists for PCOS) additions for L11.
The rest of Ch. 41 (insulin and diabetes) is taught in Endocrine Session 2 (L08)."""

EP = "Estrogens, Progestins & Contraception"
SA = "SERMs, Aromatase Inhibitors & Androgens"
PC = "PCOS & the Reproductive-Metabolic Overlap"

ADD = {
    EP: {
        "moa": [
            ("Estrogens raise hepatic clotting factors II, VII, IX and X and lower antithrombin III — the basis of the clotting risk; transdermal or vaginal routes avoid first-pass liver exposure.", "p. 761; p. 762"),
        ],
        "indications": [
            ("Postmenopausal hormonal therapy: vasomotor symptoms, genital atrophy and bone loss; after hysterectomy estrogen alone is fine because no progestin is needed.", "p. 762; p. 763"),
            ("An implantable progestin preparation (subdermal implant) provides long-acting progestin-only contraception.", "p. 768"),
            ("Contraception with progestins alone suits patients with hepatic disease, hypertension, or prior thromboembolism.", "p. 773"),
        ],
        "adverse": [
            ("Oral contraceptive VTE risk tracks the estrogen, not the progestin; factor V Leiden and other inherited clotting disorders markedly raise it.", "p. 772"),
            ("Estrogen therapy also increases migraine, cholestasis, gallbladder disease and hypertension; oral contraceptives raise hepatic adenoma risk.", "p. 764; p. 772"),
        ],
        "contra": [
            ("Contraindications & cautions: thrombophlebitis or past thromboembolism, cardiovascular or cerebrovascular disease, estrogen-dependent cancer, undiagnosed genital bleeding, liver disease.", "p. 764; p. 773"),
        ],
        "interactions": [
            ("Rifampin and phenytoin speed estrogen/progestin metabolism, and antibiotics that disturb gut flora may cut enterohepatic recycling — both can cause contraceptive failure.", "p. 771; p. 773"),
        ],
        "pearls": [
            ("Beneficial effects of oral contraceptives: lower risk of endometrial and ovarian cancer, ovarian cysts and benign breast disease; lifetime breast cancer risk unchanged.", "p. 773; p. 774"),
            ("Mifepristone (RU-486) blocks progesterone and glucocorticoid receptors; 600 mg with misoprostol ends early pregnancy in over 95%.", "p. 775"),
        ],
    },
    SA: {
        "indications": [
            ("Tamoxifen as adjuvant therapy cuts contralateral breast cancer by 35%; benefit does not grow beyond 5 years.", "p. 774"),
            ("Clomiphene, a partial estrogen agonist, blocks hypothalamic feedback to trigger ovulation (mostly in PCOS); multiple pregnancy about 10%.", "p. 776; p. 777"),
            ("Other inhibitors: danazol suppresses the midcycle LH/FSH surge (endometriosis; hepatic caution); exemestane is an irreversible aromatase inhibitor.", "p. 775; p. 776"),
        ],
        "adverse": [
            ("Androgens & anabolic steroids: masculinization in women, polycythemia; 17-alkylated oral androgens cause cholestasis, peliosis hepatis and liver tumors.", "p. 779; p. 780"),
            ("Flutamide causes gynecomastia and occasional reversible hepatotoxicity; bicalutamide is given once daily with a GnRH analog to prevent tumor flare.", "p. 782"),
        ],
        "contra": [
            ("Androgens are contraindicated in pregnant women or women who may become pregnant (fetal masculinization).", "p. 780"),
        ],
        "pk": [
            ("Androgen suppression: continuous (not pulsatile) GnRH analogs such as leuprolide suppress the gonads; dutasteride has a much longer half-life than finasteride.", "p. 781"),
        ],
    },
    PC: {
        "indications": [
            ("Polycystic ovary syndrome affects about 7% of women of reproductive age.", "p. 776"),
        ],
    },
}

CONFLICTS = {}
DISCREPANCIES = []
CRAM = [
    ("OC VTE driver", "Estrogen dose, not progestin; factor V Leiden ↑ risk", "p. 772"),
    ("OC benefits", "↓ Endometrial and ovarian cancer", "p. 773"),
    ("Clomiphene", "Ovulation induction; ~10% multiple pregnancy", "p. 776; p. 777"),
    ("Oral 17-alkyl androgens", "Cholestasis, peliosis hepatis, liver tumors", "p. 780"),
]
QUESTIONS = [
    dict(topic=EP, kind="vignette",
         stem="A 30-year-old with factor V Leiden asks for contraception. Which feature of combined pills drives her main risk?",
         correct="The estrogen component (VTE)",
         why_correct="VTE risk relates to the estrogen, not the progestin, and inherited clotting disorders markedly increase it (p. 772).",
         distractors=[("The progestin component", "VTE tracks estrogen (p. 772)."),
                      ("Neither; pills lower VTE risk", "They raise it (p. 772)."),
                      ("Only her age, not the pill", "Genetic risk matters (p. 772)."),
                      ("Only if she also smokes", "Genetic risk alone raises it (p. 772).")],
         src="p. 772"),
]
COMPARISONS = {}
DEEPER = {
    EP: (40, 758, 775, "Estrogens, progestins, contraception and postmenopausal therapy"),
    SA: (40, 774, 783, "SERMs, aromatase inhibitors, ovulation agents, androgens and antiandrogens"),
}

# Ch. 41 sections other than biguanides and GLP-1 agonists are taught in L08
_CH41_L08 = ["THE ENDOCRINE PANCREAS", "Insulin Secretion", "Insulin Degradation", "Circulating Insulin", "The Insulin Receptor", "Effects of Insulin on Its Targets",
             "Chemistry & Metabolism", "Pharmacologic Effects of Glucagon", "DIABETES MELLITUS", "Other Specific Types of Diabetes Mellitus", "Gestational Diabetes Mellitus",
             "Insulin Preparations", "Immunopathology of Insulin Therapy", "MEDICATIONS FOR TREATMENT OF TYPE 2 DIABETES", "Mechanism of Action",
             "Efficacy & Safety of the Sulfonylureas", "FIRST-GENERATION SULFONYLUREAS", "SECOND-GENERATION SULFONYLUREAS", "MEGLITINIDE ANALOGS", "BIGUANIDES",
             "THIAZOLIDINEDIONES", "DRUGS THAT AFFECT ABSORPTION OF GLUCOSE", "GLUCAGON-LIKE PEPTIDE-1 (GLP-1) RECEPTOR AGONISTS", "DIPEPTIDYL PEPTIDASE 4 (DPP-4) INHIBITORS",
             "SODIUM-GLUCOSE CO-TRANSPORTER 2 (SGL T2) INHIBITORS", "OTHER GLUCOSE-LOWERING DRUGS", "Glycemic Targets", "Prebreakfast Prelunch Predinner Bedtime",
             "Benefits of Tight Glycemic Control in Diabetes", "Chronic Complications of Diabetes", "Islet Mass Secretory Products"]
_LISTS = ["Azurette, Kariva, Mircette, Viorele", "Enpresse, Levonest, Myzilra, Triphasil, Tri-Levlen, Trivora", "Casiant, Cyclessa, Cesia, Velivet", "Toremifene Fareston"]

READING_SKIP = (
    [{"heading": h, "reason": "Taught in L08 (Endocrine Session 2: insulin and glucose-lowering drugs, Ch. 41); metformin and GLP-1 agonists in PCOS are taught here"} for h in _CH41_L08]
    + [{"heading": h, "reason": "Preparations list (brand names only, no teaching content)"} for h in _LISTS]
    + [{"heading": "Preparations & Dosages", "reason": "Preparations and dosing table; the doses are in the drug profiles"}]
    + [{"heading": "CHEMICAL CONTRACEPTION IN MEN", "reason": "Beyond PA scope: investigational male contraceptives, none approved"},
       {"heading": "GOSSYPOL", "reason": "Beyond PA scope: experimental male contraceptive, not in use"}]
)
