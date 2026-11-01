# Authoring brief — L12: Unit 6: GU & Reproductive — Session 2 (2026-12-01)

Tell Claude: **"author L12"**. Claude writes `work/L12/author_L12.py`, `guide_L12.py` and `textbook_L12.py` (copy the shape of the L02 files), adds the lecture's drugs to `work/drugs.py`, then runs `./run.sh new L12` until every gate says PASS.

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
- **Drugs:** every drug named gets a card (or new facts) in `work/drugs.py`, citing `L12 S#` or `p. N`, filled field by field: class, mechanism, indications, contraindications, adverse effects, interactions, distinguishing / patient-specific factors, extra.
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

## Slides (51) — every one must be covered
- [ ] S1: Genitourinary & Reproductive Pharmacology
- [ ] S2: Learning Objectives — Session 2
- [ ] S3: 04
- [ ] S4: Autonomic & Somatic Receptors of the Lower Urinary Tract
- [ ] S5: Cholinergic (Muscarinic) Control of the Detrusor
- [ ] S6: M3 Receptor Signaling and Detrusor Contraction
- [ ] S7: Adrenergic Control of the Bladder Neck and Detrusor
- [ ] S8: Alpha-1 vs. Beta-3: Outlet Closed, Reservoir Relaxed
- [ ] S9: Storage Phase vs. Voiding Phase
- [ ] S10: 05
- [ ] S11: Antimuscarinic Agents
- [ ] S12: Antimuscarinics: Bladder Benefit and Anticholinergic Burden
- [ ] S13: Beta-3 Agonists
- [ ] S14: Antimuscarinics vs. Beta-3 Agonists: Two Mechanisms for Bladder Storage
- [ ] S15: Anticholinergic Burden in an Older Adult
- [ ] S16: 06
- [ ] S17: Alpha1 Blockers for BPH
- [ ] S18: Alpha1 Blockade at the Bladder Neck and Prostate
- [ ] S19: 5-Alpha-Reductase Inhibitors
- [ ] S20: 5-ARIs: Shrinking the Prostate Slowly
- [ ] S21: NANC Neurotransmission and the NO-cGMP Pathway in Erectile Function
- [ ] S22: PDE5 Inhibitors
- [ ] S23: PDE5 Inhibitors: NO, cGMP and Erection
- [ ] S24: A Dangerous Combination
- [ ] S25: Nitrate plus PDE5 Inhibitor: A Double Hit on cGMP
- [ ] S26: Drug Names Reveal the Class: Urologic Agents
- [ ] S27: 07
- [ ] S28: Autonomic Receptor Map Across the Genitourinary Tract
- [ ] S29: Which Approach Would You Choose?
- [ ] S30: Key Takeaways
- [ ] S31: 08
- [ ] S32: Lecture Recall Quiz (1 of 2)
- [ ] S33: Lecture Recall Quiz (2 of 2)
- [ ] S34: Lecture Recall Quiz — Answer Key
- [ ] S35: Drug Profiles
- [ ] S36: Oxybutynin (Ditropan, Oxytrol)
- [ ] S37: Tolterodine (Detrol)
- [ ] S38: Solifenacin (Vesicare)
- [ ] S39: Darifenacin (Enablex)
- [ ] S40: Mirabegron (Myrbetriq)
- [ ] S41: Tamsulosin (Flomax)
- [ ] S42: Silodosin (Rapaflo)
- [ ] S43: Doxazosin (Cardura)
- [ ] S44: Terazosin (Hytrin)
- [ ] S45: Finasteride (Proscar, Propecia)
- [ ] S46: Dutasteride (Avodart)
- [ ] S47: Sildenafil (Viagra, Revatio)
- [ ] S48: Tadalafil (Cialis, Adcirca)
- [ ] S49: Vardenafil (Levitra, Staxyn)
- [ ] S50: Supporting Drugs at a Glance
- [ ] S51: Image Attribution

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
- [ ] `S14_1.jpg` — caption + viz type
- [ ] `S18_1.jpg` — caption + viz type
- [ ] `S20_1.jpg` — caption + viz type
- [ ] `S21_1.jpg` — caption + viz type
- [ ] `S23_1.jpg` — caption + viz type
- [ ] `S25_1.png` — caption + viz type
- [ ] `S28_1.jpg` — caption + viz type
- [ ] `S4_1.jpg` — caption + viz type
- [ ] `S6_1.png` — caption + viz type
- [ ] `S8_1.png` — caption + viz type

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
