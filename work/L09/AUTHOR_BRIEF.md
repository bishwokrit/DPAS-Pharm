# Authoring brief — L09: Unit 5: Renal — Session 1 (2026-11-17)

Tell Claude: **"author L09"**. Claude writes `work/L09/author_L09.py`, `guide_L09.py` and `textbook_L09.py` (copy the shape of the L02 files), adds the lecture's drugs to `work/drugs.py`, then runs `./run.sh new L09` until every gate says PASS.

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
- **Drugs:** every drug named gets a card (or new facts) in `work/drugs.py`, citing `L09 S#` or `p. N`, filled field by field: class, mechanism, indications, contraindications, adverse effects, interactions, distinguishing / patient-specific factors, extra.
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

## Slides (39) — every one must be covered
- [ ] S1: Renal Pharmacotherapeutics
- [ ] S2: Learning Objectives — Session 1
- [ ] S3: Required & Recommended Readings — Unit 5
- [ ] S4: 01
- [ ] S5: Renal Drug Clearance and Dosing
- [ ] S6: Renal Dose Adjustment: Dose, Interval, or Both
- [ ] S7: Diuretic Sites of Action Along the Nephron
- [ ] S8: Dosing Adjustment in Renal Impairment
- [ ] S9: 02
- [ ] S10: Loop Diuretics
- [ ] S11: The Na-K-2Cl Cotransporter (NKCC2): Loop Diuretic Target
- [ ] S12: Thiazide Diuretics
- [ ] S13: Thiazides: Distal Tubule NCC Block and Calcium Reabsorption
- [ ] S14: Loop vs. Thiazide Diuretics
- [ ] S15: Choosing a Diuretic for Advancing CKD
- [ ] S16: 03
- [ ] S17: Potassium-Sparing Diuretics
- [ ] S18: Collecting Duct: Aldosterone Blockers vs. ENaC Blockers
- [ ] S19: Carbonic Anhydrase Inhibitors & Osmotic Diuretics
- [ ] S20: Proximal Tubule: Acetazolamide and Mannitol
- [ ] S21: Diuretic Class Comparison: Natriuretic Potency
- [ ] S22: Diuretic Classes at a Glance
- [ ] S23: The Hyperkalemia Setup
- [ ] S24: Drug Names Reveal the Class: Renal Agents
- [ ] S25: Session 1 Recap — To Be Continued
- [ ] S26: Drug Profiles
- [ ] S27: Furosemide (Lasix)
- [ ] S28: Bumetanide (Bumex)
- [ ] S29: Torsemide (Demadex)
- [ ] S30: Hydrochlorothiazide (Microzide)
- [ ] S31: Chlorthalidone (Thalitone)
- [ ] S32: Spironolactone (Aldactone)
- [ ] S33: Eplerenone (Inspra)
- [ ] S34: Amiloride (Midamor)
- [ ] S35: Triamterene (Dyrenium; Maxzide and Dyazide combinations)
- [ ] S36: Acetazolamide (Diamox)
- [ ] S37: Mannitol (Osmitrol)
- [ ] S38: Supporting Drugs at a Glance
- [ ] S39: Image Attribution

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
- [ ] `S11_1.jpg` — caption + viz type
- [ ] `S13_1.png` — caption + viz type
- [ ] `S18_1.png` — caption + viz type
- [ ] `S21_1.jpg` — caption + viz type
- [ ] `S6_1.png` — caption + viz type
- [ ] `S7_1.jpg` — caption + viz type

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
