"""Textbook additions for L12. The syllabus assigns Ch. 40 and Ch. 41 to both GU sessions; they are taught in L11 (Ch. 40, PCOS)
and L08 (Ch. 41, diabetes). The slides name Ch. 6 (autonomic) as supplemental reading, which is not in the assigned page range."""

BPH = "BPH, Erectile Dysfunction & PDE5 Inhibitors"

ADD = {
    BPH: {
        "pk": [
            ("Finasteride lowers DHT within 8 hours, lasting about 24 hours; dutasteride has a slow onset and a much longer half-life.", "p. 781"),
        ],
        "indications": [
            ("Finasteride is moderately effective in reducing prostate size in BPH; 1 mg/d is approved for early male pattern baldness.", "p. 781"),
        ],
    },
}
CONFLICTS = {}
DISCREPANCIES = []
CRAM = [("Finasteride onset", "DHT falls within 8 h; prostate shrinks over months", "p. 781; S19")]
QUESTIONS = []
COMPARISONS = {}
DEEPER = {BPH: (40, 780, 782, "Androgen suppression, 5-alpha-reductase inhibitors and antiandrogens")}

_CH40 = ['Disturbances in Ovarian Function', 'Natural Estrogens', 'Synthetic Estrogens', 'Adverse Effects', 'Preparations & Dosages', 'Synthetic Progestins', 'Azurette, Kariva, Mircette, Viorele', 'Enpresse, Levonest, Myzilra, Triphasil, Tri-Levlen, Trivora', 'Casiant, Cyclessa, Cesia, Velivet', 'Implantable Progestin Preparation', 'OTHER OVARIAN HORMONES', 'HORMONAL CONTRACEPTION (ORAL, PARENTERAL, & IMPLANTED CONTRACEPTIVES)', 'Clinical Uses', 'Contraindications & Cautions', 'Contraception with Progestins Alone', 'Beneficial Effects of Oral Contraceptives', 'TAMOXIFEN & RELATED PARTIAL AGONIST ESTROGENS', 'MIFEPRISTONE (RU-486)', 'DANAZOL', 'OTHER INHIBITORS', 'OVULATION-INDUCING AGENTS CLOMIPHENE', 'OTHER DRUGS USED IN OVULATORY DISORDERS', 'ANDROGENS & ANABOLIC STEROIDS', 'Physiologic Effects', 'Anabolic Action', 'ANDROGEN SUPPRESSION & ANTIANDROGENS ANDROGEN SUPPRESSION', 'ANTIANDROGENS', 'Steroid Synthesis Inhibitors', 'Precursors to Androgens', 'Receptor Inhibitors', 'CHEMICAL CONTRACEPTION IN MEN', 'GOSSYPOL', 'Toremifene Fareston']
_CH41 = ['THE ENDOCRINE PANCREAS', 'Insulin Secretion', 'Insulin Degradation', 'Circulating Insulin', 'The Insulin Receptor', 'Islet Mass Secretory Products', 'Effects of Insulin on Its Targets', 'Chemistry & Metabolism', 'Pharmacologic Effects of Glucagon', 'DIABETES MELLITUS', 'Other Specific Types of Diabetes Mellitus', 'Gestational Diabetes Mellitus', 'Insulin Preparations', 'Immunopathology of Insulin Therapy', 'MEDICATIONS FOR TREATMENT OF TYPE 2 DIABETES', 'Mechanism of Action', 'Efficacy & Safety of the Sulfonylureas', 'FIRST-GENERATION SULFONYLUREAS', 'SECOND-GENERATION SULFONYLUREAS', 'MEGLITINIDE ANALOGS', 'BIGUANIDES', 'THIAZOLIDINEDIONES', 'DRUGS THAT AFFECT ABSORPTION OF GLUCOSE', 'GLUCAGON-LIKE PEPTIDE-1 (GLP-1) RECEPTOR AGONISTS', 'DIPEPTIDYL PEPTIDASE 4 (DPP-4) INHIBITORS', 'SODIUM-GLUCOSE CO-TRANSPORTER 2 (SGL T2) INHIBITORS', 'OTHER GLUCOSE-LOWERING DRUGS', 'Glycemic Targets', 'Prebreakfast Prelunch Predinner Bedtime', 'Benefits of Tight Glycemic Control in Diabetes', 'Chronic Complications of Diabetes']
READING_SKIP = (
    [{"heading": h, "reason": "Taught in L11 (GU Session 1: gonadal hormones, Ch. 40)"} for h in _CH40]
    + [{"heading": h, "reason": "Taught in L08 (Endocrine Session 2: diabetes, Ch. 41); PCOS use taught in L11"} for h in _CH41]
)
