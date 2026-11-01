# Authoring brief — L11: Unit 6: GU & Reproductive — Session 1 (2026-11-24)

Tell Claude: **"author L11"**. Claude writes `work/L11/author_L11.py`, `guide_L11.py` and `textbook_L11.py` (copy the shape of the L02 files), adds the lecture's drugs to `work/drugs.py`, then runs `./run.sh new L11` until every gate says PASS.

## The standard (every lecture, no exceptions)
- **Sources:** slides (with speaker notes), the assigned textbook pages, the syllabus and the course study guide only. No internet facts. Every fact cited (`S12`, `S12 (notes)`, `p. 245`, `SG U1-R3`).
- **Everything taught:** every slide line and every assigned-reading section below lands in the guide (the audit fails otherwise). A section taught in another session, or beyond PA scope, goes in `READING_SKIP` with the reason.
- **PA-student depth, no more, no less:** what a PA needs to prescribe safely and pass the exam. Skip chemistry, molecular-biology and industry detail with no prescribing decision attached. PA students are short on time: lean, never dense.
- **Easier to learn:** order (big idea → mechanism → clinical use → traps), one idea per bullet (≤25 words), discriminator tables, flows, why-hooks. A student with only the guide or only the deck can answer any exam question.
- **Length gates:** textbook-only bullets ≤30% of the guide; bullets ≤40 words; deck ≤2.25× the lecture’s slides.
- **Template:** `drug_class` for every class/topic (overview, prototype, moa, indications, adverse — boxed warnings first, contra, interactions, pk, monitoring, pearls).
- **Textbook facts** in `textbook_<ID>.py` as `("text", "p. N")`; write apostrophes as ’ so `./run.sh check` can verify the numbers on that page.
- **Questions:** ~50/50 vignette and mechanism; 5 options, all similar in length; rebuild every quick-check slide question (`from_slides`).
- **Figures:** each saved figure gets a caption and an interactive version (`"viz": {"type": …}`, list below).
- **Drugs:** every drug named gets a card (or new facts) in `work/drugs.py`, citing `L11 S#` or `p. N`, filled field by field: class, mechanism, indications, contraindications, adverse effects, interactions, distinguishing / patient-specific factors, extra.
- **Home teaser:** `TEASER` in `guide_<ID>.py` — two calm sentences, no hype.
- **No school, course-director or instructor names** anywhere (slide 1 credits are skipped on purpose).
- **Original files are never edited** (they are fingerprinted; the build stops if one changes).

## Objectives to cover
- IO6.1: Identify major pharmacologic classes used in the management of genitourinary and reproductive conditions and describe their mechanisms of action.
- IO6.2: Describe the indications, contraindications, adverse effects, and clinically significant interactions associated with medications used to treat genitourinary and reproductive conditions.
- IO6.3: Compare pharmacologic agents within and across therapeutic classes to distinguish clinically relevant differences in efficacy, safety, and use.
- IO6.4: Select appropriate pharmacologic therapy for common genitourinary & reproductive conditions based on clinical presentation and patient-specific factors.
- IO6.5: Identify appropriate dosing, administration, and monitoring considerations for medications used in genitourinary and reproductive conditions.
- IO6.6: Explain important medication-use and safety information to patients receiving pharmacotherapy for genitourinary & reproductive.

## Slides (46) — every one must be covered
- [ ] S1: Genitourinary & Reproductive Pharmacology
- [ ] S2: Learning Objectives — Session 1
- [ ] S3: Required & Recommended Readings — Unit 6
- [ ] S4: 01
- [ ] S5: Estrogens
- [ ] S6: Progestins
- [ ] S7: Unopposed Estrogen: Why a Progestin Is Added
- [ ] S8: The Hypothalamic-Pituitary-Gonadal (HPG) Axis: Sites of Hormonal Drug Action
- [ ] S9: Combined Hormonal Contraception vs. Progestin-Only Methods
- [ ] S10: 02
- [ ] S11: Selective Estrogen Receptor Modulators (SERMs)
- [ ] S12: SERMs: One Receptor, Different Tissue Effects
- [ ] S13: Two Ways to Reduce Estrogen Signaling: SERMs vs. Aromatase Inhibitors
- [ ] S14: Aromatase Inhibitors: Blocking Estrogen Synthesis
- [ ] S15: Androgens & Antiandrogens
- [ ] S16: Androgen Pathway: Where Each Drug Acts
- [ ] S17: Estrogen-Pathway Drugs vs. Androgen-Pathway Drugs
- [ ] S18: Weighing Tamoxifen's Tissue-Selective Effects
- [ ] S19: 03
- [ ] S20: PCOS: A Reproductive-Metabolic Overlap Condition
- [ ] S21: The PCOS–Insulin Resistance Cycle
- [ ] S22: Antidiabetic Agents in Reproductive-Metabolic Management
- [ ] S23: Metformin in PCOS: Insulin, Androgens and Ovulation
- [ ] S24: Agents Used in PCOS Management at a Glance
- [ ] S25: Choosing Between Metformin and Combined Contraception in PCOS
- [ ] S26: Drug Names Reveal the Class: GU and Reproductive Agents
- [ ] S27: Session 1 Recap — To Be Continued
- [ ] S28: Drug Profiles
- [ ] S29: Combined oral contraceptives (ethinyl estradiol plus a progestin)
- [ ] S30: Norethindrone (progestin-only pill)
- [ ] S31: Medroxyprogesterone depot (Depo-Provera)
- [ ] S32: Levonorgestrel IUD (Mirena)
- [ ] S33: Estradiol (Estrace, Vivelle-Dot)
- [ ] S34: Tamoxifen (Nolvadex)
- [ ] S35: Raloxifene (Evista)
- [ ] S36: Anastrozole (Arimidex)
- [ ] S37: Letrozole (Femara)
- [ ] S38: Testosterone (cypionate, gel, patch)
- [ ] S39: Spironolactone (Aldactone)
- [ ] S40: Flutamide (Eulexin)
- [ ] S41: Bicalutamide (Casodex)
- [ ] S42: Finasteride (Proscar, Propecia)
- [ ] S43: Dutasteride (Avodart)
- [ ] S44: Metformin (Glucophage)
- [ ] S45: Supporting Drugs at a Glance
- [ ] S46: Image Attribution

## Assigned reading — Ch. 40, pp. 757–784; Ch. 41, pp. 785–810 (64 sections to teach)
If this session covers only part of the reading (the unit is split across two sessions), put the other session’s sections in `READING_SKIP` with “Taught in L0x”, and teach them there.
- [ ] p. 758: Disturbances in Ovarian Function
- [ ] p. 759: Natural Estrogens
- [ ] p. 760: Synthetic Estrogens
- [ ] p. 763: Adverse Effects
- [ ] p. 764: Preparations & Dosages
- [ ] p. 765: Synthetic Progestins
- [ ] p. 767: Azurette, Kariva, Mircette, Viorele
- [ ] p. 767: Enpresse, Levonest, Myzilra, Triphasil, Tri-Levlen, Trivora
- [ ] p. 767: Casiant, Cyclessa, Cesia, Velivet
- [ ] p. 768: Implantable Progestin Preparation
- [ ] p. 769: OTHER OVARIAN HORMONES
- [ ] p. 769: HORMONAL CONTRACEPTION (ORAL, PARENTERAL, & IMPLANTED CONTRACEPTIVES)
- [ ] p. 771: Clinical Uses
- [ ] p. 773: Contraindications & Cautions
- [ ] p. 773: Contraception with Progestins Alone
- [ ] p. 774: Beneficial Effects of Oral Contraceptives
- [ ] p. 774: TAMOXIFEN & RELATED PARTIAL AGONIST ESTROGENS
- [ ] p. 775: MIFEPRISTONE (RU-486)
- [ ] p. 775: DANAZOL
- [ ] p. 776: OTHER INHIBITORS
- [ ] p. 776: OVULATION-INDUCING AGENTS CLOMIPHENE
- [ ] p. 777: OTHER DRUGS USED IN OVULATORY DISORDERS
- [ ] p. 777: ANDROGENS & ANABOLIC STEROIDS
- [ ] p. 778: Physiologic Effects
- [ ] p. 778: Anabolic Action
- [ ] p. 780: ANDROGEN SUPPRESSION & ANTIANDROGENS ANDROGEN SUPPRESSION
- [ ] p. 781: ANTIANDROGENS
- [ ] p. 781: Steroid Synthesis Inhibitors
- [ ] p. 781: Precursors to Androgens
- [ ] p. 782: Receptor Inhibitors
- [ ] p. 782: CHEMICAL CONTRACEPTION IN MEN
- [ ] p. 782: GOSSYPOL
- [ ] p. 783: Toremifene Fareston
- [ ] p. 785: THE ENDOCRINE PANCREAS
- [ ] p. 786: Insulin Secretion
- [ ] p. 786: Insulin Degradation
- [ ] p. 786: Circulating Insulin
- [ ] p. 786: The Insulin Receptor
- [ ] p. 786: Islet Mass Secretory Products
- [ ] p. 787: Effects of Insulin on Its Targets
- [ ] p. 787: Chemistry & Metabolism
- [ ] p. 788: Pharmacologic Effects of Glucagon
- [ ] p. 789: DIABETES MELLITUS
- [ ] p. 790: Other Specific Types of Diabetes Mellitus
- [ ] p. 790: Gestational Diabetes Mellitus
- [ ] p. 791: Insulin Preparations
- [ ] p. 795: Immunopathology of Insulin Therapy
- [ ] p. 795: MEDICATIONS FOR TREATMENT OF TYPE 2 DIABETES
- [ ] p. 796: Mechanism of Action
- [ ] p. 796: Efficacy & Safety of the Sulfonylureas
- [ ] p. 796: FIRST-GENERATION SULFONYLUREAS
- [ ] p. 796: SECOND-GENERATION SULFONYLUREAS
- [ ] p. 797: MEGLITINIDE ANALOGS
- [ ] p. 797: BIGUANIDES
- [ ] p. 798: THIAZOLIDINEDIONES
- [ ] p. 799: DRUGS THAT AFFECT ABSORPTION OF GLUCOSE
- [ ] p. 800: GLUCAGON-LIKE PEPTIDE-1 (GLP-1) RECEPTOR AGONISTS
- [ ] p. 801: DIPEPTIDYL PEPTIDASE 4 (DPP-4) INHIBITORS
- [ ] p. 801: SODIUM-GLUCOSE CO-TRANSPORTER 2 (SGL T2) INHIBITORS
- [ ] p. 802: OTHER GLUCOSE-LOWERING DRUGS
- [ ] p. 803: Glycemic Targets
- [ ] p. 804: Prebreakfast Prelunch Predinner Bedtime
- [ ] p. 804: Benefits of Tight Glycemic Control in Diabetes
- [ ] p. 806: Chronic Complications of Diabetes

## Figures saved from the slides
- [ ] `S12_1.png` — caption + viz type
- [ ] `S13_1.jpg` — caption + viz type
- [ ] `S14_1.png` — caption + viz type
- [ ] `S16_1.png` — caption + viz type
- [ ] `S21_1.jpg` — caption + viz type
- [ ] `S23_1.png` — caption + viz type
- [ ] `S7_1.jpg` — caption + viz type
- [ ] `S8_1.jpg` — caption + viz type

## Interactive figure types (`"viz": {"type": "…"}` on a figure)
- `dose-response` — graded dose-response curve (EC50, Emax)
- `antagonist` — agonist curve shifted by a competitive vs noncompetitive antagonist
- `potency-efficacy` — two drugs compared on potency and efficacy
- `therapeutic-index` — ED50 vs TD50, narrow vs wide window
- `cyp-interaction` — substrate level with an inhibitor vs an inducer
- `half-life` — exponential decay over half-lives
- `steady-state` — accumulation to steady state, with/without loading dose
- `fill-empty` — time to fill and time to empty are the same
- `adme` — absorption → distribution → metabolism → excretion map
- `bars` — any bar chart; give {title, unit, bars:[{label, value, note}], steps:[{label, pick}]}
- `nomogram` — Rumack-Matthew nomogram: drag a level to a time; give {point, steps:[{label, t, c}]}
- `onset` — fast symptom relief vs slow disease modification over time (schematic); give {point, steps:[{label, t}]}
- `pathway` — mechanism flow (boxes + arrows) where each drug cuts in; give {title, h, nodes:[{id, label, x, y, w, col}], edges:[[a, b]], drugs:[{label, at, off, less, note}]}

If none fits, ask for a new dedicated diagram in `site_src/assets/viz.js` (same palette, reset after 30 s idle, Try-it steps).
