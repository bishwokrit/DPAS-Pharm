# Authoring brief — L10: Unit 5: Renal — Session 2 (2026-11-19)

Tell Claude: **"author L10"**. Claude writes `work/L10/author_L10.py`, `guide_L10.py` and `textbook_L10.py` (copy the shape of the L02 files), adds the lecture's drugs to `work/drugs.py`, then runs `./run.sh new L10` until every gate says PASS.

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
- **Drugs:** every drug named gets a card (or new facts) in `work/drugs.py`, citing `L10 S#` or `p. N`, filled field by field: class, mechanism, indications, contraindications, adverse effects, interactions, distinguishing / patient-specific factors, extra.
- **Home teaser:** `TEASER` in `guide_<ID>.py` — two calm sentences, no hype.
- **No school, course-director or instructor names** anywhere (slide 1 credits are skipped on purpose).
- **Original files are never edited** (they are fingerprinted; the build stops if one changes).

## Objectives to cover
- IO5.1: Identify major pharmacologic classes used in the management of renal conditions and describe their mechanisms of action.
- IO5.2: Describe the indications, contraindications, adverse effects, and clinically significant interactions associated with medications used to treat renal conditions.
- IO5.3: Compare pharmacologic agents within and across therapeutic classes to distinguish clinically relevant differences in efficacy, safety, and use.
- IO5.4: Select appropriate pharmacologic therapy for common renal conditions based on clinical presentation and patient-specific factors.
- IO5.5: Identify appropriate dosing, administration, and monitoring considerations for medications used in renal conditions.
- IO5.6: Explain important medication-use and safety information to patients receiving pharmacotherapy for renal.

## Slides (56) — every one must be covered
- [ ] S1: Renal Pharmacotherapeutics
- [ ] S2: Learning Objectives — Session 2
- [ ] S3: 04
- [ ] S4: The Renin-Angiotensin-Aldosterone System: Where Antihypertensives Act
- [ ] S5: ACE Inhibitors
- [ ] S6: ACE Inhibitors: Bradykinin, Cough and Angioedema
- [ ] S7: ARBs and Direct Renin Inhibitors
- [ ] S8: RAAS Blockers in Chronic Kidney Disease
- [ ] S9: Efferent Arteriole Dilation: Why Creatinine Rises
- [ ] S10: Interpreting a Creatinine Rise After Starting Lisinopril
- [ ] S11: 05
- [ ] S12: Other Major Antihypertensive Classes
- [ ] S13: Calcium Channel Blockers and Beta-Blockers: Different Targets
- [ ] S14: Antihypertensive Classes: BP-Lowering Efficacy vs. Renoprotection in CKD
- [ ] S15: Resistant Hypertension in CKD
- [ ] S16: Central Agents and Hydralazine: When Others Are Not Enough
- [ ] S17: Resistant Hypertension — Where to Look First
- [ ] S18: 06
- [ ] S19: Nitrates
- [ ] S20: Nitrates: NO, cGMP and Venodilation
- [ ] S21: Angina Pathophysiology: Where Nitrates and Calcium Channel Blockers Act
- [ ] S22: Calcium Channel Blockers for Angina
- [ ] S23: The "Triple Whammy": A Classic Preventable Cause of AKI
- [ ] S24: Triple Whammy: Three Hits on Glomerular Pressure
- [ ] S25: The Cardiorenal-Hypertension Relationship
- [ ] S26: The Cardiorenal-Hypertension Cycle
- [ ] S27: Recognizing the Triple Whammy
- [ ] S28: Drug Names Reveal the Class: Cardiorenal Agents
- [ ] S29: 07
- [ ] S30: Which Approach Would You Choose?
- [ ] S31: Key Takeaways
- [ ] S32: 08
- [ ] S33: Lecture Recall Quiz (1 of 2)
- [ ] S34: Lecture Recall Quiz (2 of 2)
- [ ] S35: Lecture Recall Quiz — Answer Key
- [ ] S36: Drug Profiles
- [ ] S37: Captopril (Capoten)
- [ ] S38: Lisinopril (Zestril, Prinivil)
- [ ] S39: Enalapril (Vasotec)
- [ ] S40: Losartan (Cozaar)
- [ ] S41: Valsartan (Diovan)
- [ ] S42: Aliskiren (Tekturna)
- [ ] S43: Amlodipine (Norvasc)
- [ ] S44: Nifedipine ER (Procardia XL, Adalat CC)
- [ ] S45: Diltiazem (Cardizem)
- [ ] S46: Verapamil (Calan, Isoptin)
- [ ] S47: Metoprolol (Lopressor, Toprol-XL)
- [ ] S48: Atenolol (Tenormin)
- [ ] S49: Clonidine (Catapres)
- [ ] S50: Methyldopa (Aldomet)
- [ ] S51: Hydralazine (Apresoline)
- [ ] S52: Nitroglycerin (Nitrostat, Nitro-Dur)
- [ ] S53: Isosorbide mononitrate (Imdur)
- [ ] S54: Isosorbide dinitrate (Isordil)
- [ ] S55: Supporting Drugs at a Glance
- [ ] S56: Image Attribution

## Assigned reading — Ch. 15, pp. 261–286; Ch. 3, pp. 42–56 (51 sections to teach)
If this session covers only part of the reading (the unit is split across two sessions), put the other session’s sections in `READING_SKIP` with “Taught in L0x”, and teach them there.
- [ ] p. 261: RENAL TUBULE TRANSPORT MECHANISMS PROXIMAL TUBULE
- [ ] p. 264: DISTAL CONVOLUTED TUBULE
- [ ] p. 264: COLLECTING TUBULE SYSTEM
- [ ] p. 266: RENAL AUTACOIDS
- [ ] p. 266: ADENOSINE
- [ ] p. 266: PROSTAGLANDINS
- [ ] p. 266: PEPTIDES
- [ ] p. 266: CARBONIC ANHYDRASE INHIBITORS
- [ ] p. 267: Drug Usual Oral Dosage
- [ ] p. 268: SODIUM GLUCOSE COTRANSPORTER 2 (SGL T2) INHIBITORS
- [ ] p. 268: Clinical Indications
- [ ] p. 269: Adverse Reactions
- [ ] p. 269: LOOP DIURETICS
- [ ] p. 270: Clinical Indications & Dosage
- [ ] p. 271: THIAZIDES
- [ ] p. 271: Chemistry & Pharmacokinetics
- [ ] p. 273: POTASSIUM-SPARING DIURETICS
- [ ] p. 274: Agent Hydrochlorothiazide
- [ ] p. 275: AGENTS THAT AL TER WATER EXCRETION (AQUARETICS) OSMOTIC DIURETICS
- [ ] p. 276: ANTIDIURETIC HORMONE ANTAGONISTS
- [ ] p. 277: UREARETICS
- [ ] p. 277: DIURETIC COMBINATIONS LOOP AGENTS & THIAZIDES
- [ ] p. 278: CLINICAL PHARMACOLOGY OF DIURETIC AGENTS
- [ ] p. 278: EDEMATOUS STATES
- [ ] p. 278: HEART FAILURE
- [ ] p. 278: KIDNEY DISEASE AND RENAL FAILURE
- [ ] p. 279: HEPATIC CIRRHOSIS
- [ ] p. 279: IDIOPATHIC EDEMA
- [ ] p. 280: NONEDEMATOUS STATES HYPERTENSION
- [ ] p. 280: NEPHROLITHIASIS
- [ ] p. 280: HYPERCALCEMIA
- [ ] p. 280: DIABETES INSIPIDUS
- [ ] p. 281: RENAL & CARDIAC PROTECTION
- [ ] p. 281: RISK OF HYPONATREMIA WITH DIFFERENT DIURETIC CLASSES
- [ ] p. 282: VASOPRESSIN (ADH) ANTAGONISTS
- [ ] p. 42: PHARMACOKINETICS
- [ ] p. 43: Volume of Distribution
- [ ] p. 48: Drug Accumulation
- [ ] p. 49: Rate of Absorption
- [ ] p. 49: Extraction Ratio & the First-Pass Effect
- [ ] p. 49: THE TIME COURSE OF DRUG EFFECT
- [ ] p. 50: Immediate Effects
- [ ] p. 50: Delayed Effects
- [ ] p. 50: Schedule-Dependent Effects
- [ ] p. 50: Conc Effect
- [ ] p. 51: Cumulative Effects
- [ ] p. 51: Maintenance Dose
- [ ] p. 52: Loading Dose
- [ ] p. 53: The Target Concentration Strategy
- [ ] p. 54: Dosing History
- [ ] p. 56: Distribution & Clearance

## Figures saved from the slides
- [ ] `S13_1.png` — caption + viz type
- [ ] `S14_1.jpg` — caption + viz type
- [ ] `S16_1.png` — caption + viz type
- [ ] `S20_1.png` — caption + viz type
- [ ] `S21_1.jpg` — caption + viz type
- [ ] `S23_1.jpg` — caption + viz type
- [ ] `S24_1.png` — caption + viz type
- [ ] `S26_1.jpg` — caption + viz type
- [ ] `S4_1.jpg` — caption + viz type
- [ ] `S6_1.png` — caption + viz type
- [ ] `S9_1.png` — caption + viz type

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
