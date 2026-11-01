"""Authoring source for L08 content.json. Run: python3 author_L08.py"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import profiles as PR  # noqa: E402


def F(text, src, tb=False, sg=False):
    d = {"text": text, "src": src}
    if tb:
        d["tb"] = True
    if sg:
        d["sg"] = True
    return d


def Q(kind, stem, correct, why_correct, distractors, src, from_slides=None):
    q = {"kind": kind, "stem": stem, "correct": correct, "why_correct": why_correct,
         "distractors": [{"text": t, "why": w} for t, w in distractors], "src": src}
    if from_slides:
        q["from_slides"] = from_slides
    return q


PROF = {p["slide"]: p for p in PR.read("L08")}


def prof(*slides):
    return [PROF[s] for s in slides]


def tab(slides, title):
    return PR.table(prof(*slides), title, bold=True)


def path(nodes, edges, drugs, point, h=170, read="Pick a drug to see where it acts."):
    return {"type": "pathway", "title": "", "h": h, "point": point, "nodes": nodes, "edges": edges, "drugs": drugs, "read": read}


def N(id, label, glyph, x, y, w, col):
    return {"id": id, "label": label, "glyph": glyph, "x": x, "y": y, "w": w, "col": col}


def Dg(label, at, note, off=(), less=()):
    return {"label": label, "at": at, "off": list(off), "less": list(less), "note": note}


objectives = [
    {"id": "IO4.1", "src": "Syllabus", "text": "Identify major pharmacologic classes used in the management of endocrine conditions and describe their mechanisms of action."},
    {"id": "IO4.2", "src": "Syllabus", "text": "Describe the indications, contraindications, adverse effects, and clinically significant interactions associated with medications used to treat endocrine conditions."},
    {"id": "IO4.3", "src": "Syllabus", "text": "Compare pharmacologic agents within and across therapeutic classes to distinguish clinically relevant differences in efficacy, safety, and use."},
    {"id": "IO4.4", "src": "Syllabus", "text": "Select appropriate pharmacologic therapy for common endocrine conditions based on clinical presentation and patient-specific factors."},
    {"id": "IO4.5", "src": "Syllabus", "text": "Identify appropriate dosing, administration, and monitoring considerations for medications used in endocrine conditions."},
    {"id": "IO4.6", "src": "Syllabus", "text": "Explain important medication-use and safety information to patients receiving pharmacotherapy for endocrine conditions."},
    {"id": "SO1", "src": "S2", "text": "Describe the mechanisms and clinical uses of gonadal hormone agents, including combined hormonal contraception, SERMs, and androgens/antiandrogens."},
    {"id": "SO2", "src": "S2", "text": "Classify glucose-lowering drugs by mechanism and site of action, and compare agents on efficacy, hypoglycemia risk, and key adverse effects."},
    {"id": "SO3", "src": "S2", "text": "Distinguish hyperparathyroidism from hypoparathyroidism and identify the drug strategy used for each."},
    {"id": "SO4", "src": "S2", "text": "Identify key contraindications, adverse effects, and drug interactions throughout."},
    {"id": "SO5", "src": "S2", "text": "Apply the full Endocrine pharmacology toolkit to integrated clinical scenarios, and complete a cumulative recall quiz spanning both sessions."},
]

about = [
    F("**PA PHARMACOLOGY COURSE · LECTURE 4 · SESSION 2 OF 2** — Endocrine Pharmacotherapy. **Session 2: Reproductive Hormones, Diabetes, and Bone Mineral Homeostasis  |  Thursday, November 12  |  8:30–11:00 AM**", "S1"),
    F("Recap: Session 1 (Nov 10) covered the hypothalamic-pituitary axis, thyroid/antithyroid drugs, and adrenocorticosteroid pharmacology. Session 1 gave us the axis.", "S1 (notes); S2; S2 (notes)"),
    F("Today the same negative-feedback logic explains contraception, then the many ways to lower glucose, finishing with the two opposite parathyroid problems — then integration and the cumulative recall quiz.", "S1 (notes); S2 (notes)"),
    F("Today picks up with gonadal hormones (Section 4) and runs through diabetes, parathyroid disorders, integration, and the cumulative recall quiz.", "S2 (notes)"),
    F("**Appendix 1 abbreviation key: PO = by mouth; SC = subcutaneous; IM = intramuscular; IV = intravenous; ER / XL = extended-release; BID = twice daily; mcg = microgram; U-100 etc. = units of insulin per mL; IUD = intrauterine device.**", "S36; S36 (notes)"),
    F("**DCIS = ductal carcinoma in situ; VTE / DVT / PE = venous thromboembolism / deep vein thrombosis / pulmonary embolism; MI = myocardial infarction; BPH = benign prostatic hyperplasia; PSA = prostate-specific antigen; PCOS = polycystic ovary syndrome.**", "S36; S36 (notes)"),
    F("**DKA = diabetic ketoacidosis; eGFR / CrCl = estimated glomerular filtration rate / creatinine clearance; CKD = chronic kidney disease; NPH = neutral protamine Hagedorn; SGLT2 = sodium-glucose cotransporter 2; DPP-4 = dipeptidyl peptidase-4; GLP-1 = glucagon-like peptide 1.**", "S36; S36 (notes)"),
    F("**MEN2 = multiple endocrine neoplasia type 2; CaSR = calcium-sensing receptor; PTH = parathyroid hormone; NYHA = New York Heart Association; CV = cardiovascular; CYP = cytochrome P450; QT = QT interval on ECG.**", "S36; S36 (notes)"),
    F("**APPENDIX 1** gives **Formulation, dose, indications, adverse effects, contraindications and toxicity** — your study reference: know the dose logic, the serious adverse effects, the contraindication that changes your decision, and the toxicity you would need to recognize.", "S36; S36 (notes); S37-66"),
    F("**Appendix 2: DRUG PROFILE · SUPPORTING** — supporting drugs explain interactions and rescue. **Listed for context; not profiled in detail.**", "S67; S67 (notes)"),
    F("**Original figures in this deck:** Figures 11, 15, 19, 21 and 22 (Combined Hormonal Contraception: Suppressing the HPG Axis; Pancreatic β-Cell Insulin Secretion: Secretagogue & Incretin Targets; Glucose-Lowering Drugs by Site of Action;", "S68"),
    F("HbA1c-Lowering Efficacy vs. Hypoglycemia Risk by Class; Parathyroid Disorders: Two Opposite Problems, Two Drug Strategies) were generated by the course director using the AI tool Claude — original diagrams, not reproduced from Katzung’s Basic and Clinical Pharmacology or any other copyrighted source.", "S68; S68 (notes)"),
    F("**Mechanism illustrations** (AI-generated, illustrative, not reproduced from copyrighted sources; schematic and not to scale): combined pills (Figure 12, slide 6); SERMs (Figure 13, slide 8); testosterone and 5-alpha-reductase inhibitors (Figure 14, slide 9); insulin signaling (Figure 16, slide 15);", "S68"),
    F("metformin (Figure 17, slide 17); SGLT2 inhibitors (Figure 18, slide 18); incretin drugs (Figure 20, slide 21); cinacalcet and the calcium-sensing receptor (Figure 23, slide 32). **Reference:** Anthropic. (2026). Claude (Sonnet 5) [Large language model]. https://claude.ai", "S68"),
]

# ---------------------------------------------------------------- Part 1: gonadal hormones
t1 = {
    "name": "Gonadal Hormones & Inhibitors", "template": "drug_class", "objectives": ["SO1", "SO4", "IO4.1", "IO4.2", "IO4.4", "IO4.6"],
    "sections": {
        "overview": [
            F("**Suppressing, replacing, or selectively modulating the reproductive axis.** Today the same negative-feedback logic explains contraception.", "S3; S3 (notes)"),
            F("**Figure 11. Original illustrative diagram (not from Katzung): exogenous estrogen and progestin suppress GnRH pulsatility and the FSH/LH surge, preventing the dominant-follicle development and LH surge required for ovulation.**", "S4; S4 (notes)"),
            F("This is the same negative-feedback template from Figure 1 (Session 1), now applied to the HPG axis.", "S4 (notes)"),
        ],
        "prototype": [
            F("Combined oral contraceptives (ethinyl estradiol plus a progestin); progestin-only: norethindrone \"minipill,\" depot medroxyprogesterone, levonorgestrel IUD; SERMs tamoxifen, raloxifene; testosterone; finasteride; spironolactone.", "S5; S7"),
        ],
        "moa": [
            F("**Mechanism: estrogen + progestin suppress GnRH/FSH/LH, preventing ovulation (Figure 11); progestin also thickens cervical mucus and thins the endometrium.**", "S5; S6 (notes)"),
            F("Chain (Figure 12): ethinyl estradiol plus progestin enter the bloodstream → hypothalamus lowers GnRH pulses; pituitary lowers FSH and LH → no follicle maturation and no LH surge, so no ovulation → result: pregnancy prevented (over 99% with perfect use).", "S6; S4 (notes)"),
            F("SERMs: tamoxifen or raloxifene bind the estrogen receptor → the receptor shape recruits different co-factors in each tissue.", "S8"),
            F("Breast: blocked (antagonist), so cancer growth is slowed. Bone: activated (agonist), so bone density is kept. Endometrium: tamoxifen activates (cancer risk); raloxifene blocks.", "S8"),
            F("Testes make testosterone → 5-alpha-reductase converts it to DHT in prostate and skin → DHT drives prostate growth and hair loss → finasteride blocks 5-alpha-reductase → lower DHT: smaller prostate, less hair loss.", "S9; S9 (notes)"),
        ],
        "indications": [
            F("Combined contraception is available as oral pills, transdermal patch, or vaginal ring.", "S5"),
            F("Tamoxifen — antagonist in breast tissue (breast cancer treatment/prevention), agonist in endometrium (raises endometrial cancer risk). Tissue-selective activity is the defining feature of this class.", "S7; S7 (notes)"),
            F("Raloxifene — antagonist in breast/endometrium, agonist in bone (osteoporosis prevention) — ties back to Unit 2 bone pharmacology; prevents vertebral fracture; not used to treat breast cancer.", "S7; S8"),
            F("Testosterone — replacement for hypogonadism; monitor hematocrit (erythrocytosis risk) and lipids. Finasteride — 5-α-reductase inhibitor; reduces conversion of testosterone to DHT (BPH, androgenetic alopecia).", "S7"),
            F("Spironolactone — antiandrogen effect at high doses; used off-label for hirsutism/acne (same drug as the mineralocorticoid antagonist from Session 1): same molecule, different receptor, different clinical use.", "S7; S7 (notes); S9"),
        ],
        "adverse": [
            F("Combined pills: risks include venous thromboembolism, hypertension and stroke. Common effects: nausea, breast tenderness, breakthrough bleeding.", "S6"),
            F("Tamoxifen raises endometrial cancer and VTE risk and causes hot flashes; patients should report vaginal bleeding. Raloxifene does not increase endometrial cancer, but raises VTE risk and hot flashes.", "S8; S8 (notes)"),
            F("Finasteride lowers PSA by about half, so double the PSA value when screening; sexual side effects occur.", "S9; S9 (notes)"),
        ],
        "contra": [
            F("**Contraindications: history of VTE/stroke, estrogen-sensitive cancer, uncontrolled hypertension, migraine with aura, and smokers age 35 or older (increased thromboembolic risk).** Liver disease too.", "S5; S5 (notes)"),
            F("Smoking at age 35+ substantially raises thromboembolic/cardiovascular risk with estrogen — the basis of the contraindication.", "S5; SG U4-R10"),
            F("\"Smoker over 35\" and \"migraine with aura\" are the classic exam triggers for choosing a progestin-only method — smokers 35 or older, migraine with aura and prior VTE rule out estrogen.", "S5 (notes); S6"),
            F("Progestin-only options (e.g., the \"minipill,\" depot medroxyprogesterone (bone density warning), levonorgestrel IUD) avoid estrogen-related thromboembolic risk and are preferred when estrogen is contraindicated.", "S5; S6; S6 (notes)"),
            F("Both SERMs are contraindicated with prior VTE. Finasteride is teratogenic: pregnant women should not handle crushed or broken tablets. Testosterone: avoid in prostate cancer.", "S8; S9; S9 (notes)"),
        ],
        "interactions": [
            F("Enzyme inducers (rifampin, carbamazepine, phenytoin, St. John’s wort, some antiepileptics) lower contraceptive efficacy; use backup contraception.", "S5 (notes); S6; S67"),
            F("CYP2D6 inhibitors (paroxetine, fluoxetine) blunt tamoxifen activation.", "S8 (notes); S67"),
        ],
        "pk": [],
        "monitoring": [
            F("Testosterone replacement: monitor hematocrit, PSA and lipids.", "S9; S9 (notes)"),
        ],
        "pearls": [
            F("The contraindication list is the highest-yield content in contraception.", "S5 (notes)"),
        ],
    },
    "figures": [
        {"image": "S4_1.jpg", "title": "Figure 11 · Combined hormonal contraception suppresses the HPG axis", "src": "S4; S4 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): exogenous estrogen and progestin feed back on the hypothalamus and pituitary, suppressing GnRH pulses and the FSH/LH surge, so no dominant follicle and no ovulation.",
         "viz": path([N("hyp", "Hypothalamus:\nGnRH pulses", "signal", 10, 55, 150, "blue"), N("pit", "Pituitary:\nFSH and LH", "signal", 180, 55, 140, "teal"),
                      N("ov", "Follicle and\nLH surge", "cell", 340, 55, 130, "amber"), N("out", "Ovulation", "effect", 490, 55, 140, "coral")],
                     [["hyp", "pit"], ["pit", "ov"], ["ov", "out"]],
                     [Dg("Combined pill", "hyp", "Estrogen + progestin feedback: no surge, no ovulation (S4–S5).", off=["pit", "ov", "out"]),
                      Dg("Rifampin (inducer)", "hyp", "Lowers hormone levels — backup contraception (S6; S67).")],
                     "Feedback from outside hormones switches the axis off.")},
        {"image": "S6_1.jpg", "title": "Figure 12 · Combined pills: ovulation block and backup barriers", "src": "S6; S6 (notes)",
         "caption": "Schematic (illustrative) — Figure 12. Teal: hormone entry; blue: brain and ovary signaling; grey-green: local cervical and endometrial effects; red: outcome. Arrows show negative feedback: no ovulation, thick mucus, thin endometrium.",
         "viz": path([N("ee", "Estradiol +\nprogestin", "molecule", 10, 20, 130, "teal"), N("axis", "GnRH, FSH, LH ↓", "signal", 165, 20, 150, "blue"),
                      N("ovu", "No ovulation", "effect", 340, 20, 130, "coral"), N("muc", "Thick cervical\nmucus, thin lining", "membrane", 165, 130, 160, "sage"),
                      N("prev", "Pregnancy\nprevented", "effect", 490, 75, 140, "deep")],
                     [["ee", "axis"], ["axis", "ovu"], ["ee", "muc"], ["ovu", "prev"], ["muc", "prev"]],
                     [Dg("Ethinyl estradiol + progestin", "ee", ">99% with perfect use (S6)."),
                      Dg("Progestin-only (minipill, DMPA, IUD)", "muc", "No estrogen: use when estrogen is contraindicated (S5–S6).")],
                     "Two locks: no ovulation, and a barrier at the cervix.", h=230)},
        {"image": "S8_1.jpg", "title": "Figure 13 · SERMs: one receptor, different tissue effects", "src": "S8; S8 (notes)",
         "caption": "Schematic (illustrative) — Figure 13. Teal: receptor binding; blue and grey-green: tissue responses; green check = agonist, red X = antagonist; red outcome = risk in endometrium. Tamoxifen activates the endometrium (cancer risk); raloxifene blocks it.",
         "viz": path([N("er", "Estrogen receptor", "membrane", 10, 95, 150, "teal"), N("br", "Breast", "cell", 260, 10, 130, "blue"),
                      N("bo", "Bone", "cell", 260, 95, 130, "sage"), N("en", "Endometrium", "cell", 260, 180, 130, "coral"),
                      N("risk", "Endometrial\ncancer risk", "effect", 470, 180, 150, "deep")],
                     [["er", "br"], ["er", "bo"], ["er", "en"], ["en", "risk"]],
                     [Dg("Tamoxifen", "er", "Blocks breast; activates bone and endometrium — report bleeding (S7–S8).", off=["br"]),
                      Dg("Raloxifene", "er", "Blocks breast and endometrium; activates bone (S7–S8).", off=["br", "en", "risk"])],
                     "Same receptor, opposite answers by tissue.", h=260)},
        {"image": "S9_1.png", "title": "Figure 14 · Testosterone, DHT and 5-alpha-reductase inhibitors", "src": "S9; S9 (notes)",
         "caption": "Schematic (illustrative) — Figure 14. Teal: start; blue: enzyme and hormone steps; green-grey: blocking drug; red: outcome, lower DHT. Finasteride blocks 5-alpha-reductase: smaller prostate, less hair loss, PSA roughly halved.",
         "viz": path([N("t", "Testosterone\n(testes)", "molecule", 10, 55, 140, "teal"), N("ar", "5-alpha-\nreductase", "enzyme", 170, 55, 130, "blue"),
                      N("dht", "DHT", "molecule", 320, 55, 110, "amber"), N("eff", "Prostate growth,\nhair loss", "effect", 450, 55, 180, "coral")],
                     [["t", "ar"], ["ar", "dht"], ["dht", "eff"]],
                     [Dg("Finasteride", "ar", "Lowers DHT; PSA falls by about half; teratogenic tablets (S9).", off=["dht", "eff"]),
                      Dg("Testosterone replacement", "t", "Monitor hematocrit, PSA, lipids (S9).")],
                     "Block the enzyme, lower the DHT.")},
    ],
    "comparisons": [
        *tab((37, 38, 39, 40), "Contraceptive profiles"),
        *tab((41, 42, 43, 44), "SERM and androgen profiles"),
    ],
    "hooks": [
        {"kind": "why", "text": "Why does a smoker over 35 get a progestin-only method? Estrogen adds clotting risk on top of smoking and age — the progestin-only options carry no estrogen.", "src": "S5; S6"},
    ],
    "high_yield": [
        F("No estrogen with prior VTE/stroke, smoker ≥ 35, migraine with aura, estrogen-sensitive cancer, uncontrolled hypertension → progestin-only.", "S5; S6"),
        F("Tamoxifen: endometrial agonist (report bleeding); raloxifene: bone agonist, endometrium blocked; both VTE.", "S7; S8"),
    ],
    "questions": [
        Q("vignette", "A 37-year-old who smokes a pack a day wants hormonal contraception. Which choice fits best?",
          "A levonorgestrel IUD (progestin-only)",
          "Smoking at 35 or older contraindicates estrogen; progestin-only options are preferred (S5; S35).",
          [("A combined oral contraceptive pill", "Estrogen contraindicated (S5)."),
           ("A combined transdermal patch", "Contains estrogen (S5)."),
           ("A combined vaginal ring", "Contains estrogen (S5)."),
           ("Any combined method at low dose", "Still estrogen (S5).")], "S5; S33; S35", from_slides="S33; S35"),
        Q("vignette", "A woman on a combined pill starts rifampin for latent TB. What counseling is needed?",
          "Use backup contraception",
          "Enzyme inducers (rifampin, some antiepileptics, St. John’s wort) lower contraceptive efficacy (S6).",
          [("No change; rifampin has no effect", "It lowers efficacy (S6)."),
           ("Stop the pill during rifampin", "Backup, not stopping (S6)."),
           ("Double the pill each day", "Not the advice (S6)."),
           ("Switch rifampin to St. John’s wort", "Also an inducer (S6).")], "S6; S67"),
        Q("mechanism", "Which statement about tamoxifen and raloxifene is correct?",
          "Only tamoxifen activates the endometrium",
          "Tamoxifen is an endometrial agonist (cancer risk); raloxifene blocks the endometrium (S7–S8).",
          [("Only raloxifene raises VTE risk", "Both do (S8)."),
           ("Raloxifene treats breast cancer", "Not used to treat it (S8)."),
           ("Both are breast agonists", "Both block breast (S8)."),
           ("Tamoxifen weakens bone", "Bone agonist (S8).")], "S7; S8"),
        Q("vignette", "A man on finasteride for BPH has a PSA of 2.0 ng/mL. How should it be interpreted?",
          "Double it — about 4.0 — when screening",
          "Finasteride lowers PSA by about half, so double the value (S9).",
          [("Take it at face value", "It is halved (S9)."),
           ("Halve it to about 1.0", "Doubled, not halved (S9)."),
           ("Stop finasteride for a month first", "Not the taught approach (S9)."),
           ("PSA is meaningless on finasteride", "Still usable, doubled (S9).")], "S9"),
    ],
}

# ---------------------------------------------------------------- Part 2: insulin
t2 = {
    "name": "Insulin", "template": "drug_class", "objectives": ["SO2", "IO4.1", "IO4.2", "IO4.5", "IO4.6"],
    "sections": {
        "overview": [
            F("**Many mechanisms, one shared goal: glycemic control without excess hypoglycemia.** Today we cover the many ways to lower glucose.", "S10; S10 (notes)"),
            F("**Figure 15. Original illustrative diagram (not from Katzung): glucose entry raises ATP, closing K-ATP channels and triggering depolarization and calcium-dependent insulin release;**", "S11; S11 (notes)"),
            F("**sulfonylureas/meglitinides force channel closure directly, while GLP-1 receptor agonists and DPP-4 inhibitors amplify glucose-dependent release via the incretin pathway.** ", "S11"),
            F("This is the mechanistic foundation for the insulin secretagogue and incretin-based drug classes that follow — the \"glucose-dependent\" nature of incretin-based therapy is exactly why these agents carry lower hypoglycemia risk than sulfonylureas.", "S11 (notes)"),
        ],
        "prototype": [
            F("Insulin lispro, aspart (rapid); regular (short); NPH (intermediate); glargine, detemir, degludec (long-acting).", "S12"),
        ],
        "moa": [
            F("**Mechanism: exogenous insulin activates the insulin receptor, promoting cellular glucose uptake and suppressing hepatic gluconeogenesis.**", "S12"),
            F("Chain (Figure 16): insulin binds the insulin receptor on muscle, fat and liver cells → receptor autophosphorylation starts the signal cascade → GLUT4 moves to the cell surface so glucose enters.", "S13; S13 (notes)"),
            F("Then the liver stores glycogen and stops making glucose → blood glucose falls (hypoglycemia is the main risk).", "S13"),
        ],
        "indications": [
            F("Rapid-acting (lispro, aspart) — mealtime dosing; onset ~15 minutes. Short-acting (regular) — onset ~30 minutes.", "S12"),
            F("Intermediate-acting (NPH) — cloudy suspension; more variable absorption. Long-acting (glargine, detemir, degludec) — basal coverage; relatively peakless profile.", "S12"),
            F("Rapid-acting is given with meals; regular 30 minutes before. NPH peaks at about 4–10 hours; glargine, detemir and degludec are basal. Only regular insulin is given IV.", "S12 (notes); S13"),
            F("Sort any named insulin into rapid, short, intermediate or long-acting before discussing regimens — the scaffold for every insulin question.", "S12 (notes)"),
        ],
        "adverse": [
            F("**Primary adverse effect across all insulins: hypoglycemia — counsel patients on recognition and treatment (rapid-acting carbohydrate).**", "S12"),
            F("Adverse effects: hypoglycemia, weight gain, lipohypertrophy, hypokalemia. Never share pens.", "S13"),
        ],
        "contra": [],
        "interactions": [
            F("Beta-blockers can mask hypoglycemia warning symptoms. Glucagon and dextrose: rescue for severe hypoglycemia.", "S12 (notes); S13; S67"),
        ],
        "pk": [],
        "monitoring": [
            F("Rule of 15 for hypoglycemia: 15 g carbohydrate, recheck in 15 minutes.", "S12 (notes); S13"),
        ],
        "pearls": [],
    },
    "figures": [
        {"image": "S11_1.jpg", "title": "Figure 15 · β-cell insulin secretion: secretagogue and incretin targets", "src": "S11; S11 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): glucose → ATP → K-ATP channels close → depolarization → Ca²⁺ → insulin release. Sulfonylureas/meglitinides force closure directly (any glucose); GLP-1 agonists and DPP-4 inhibitors amplify release only when glucose is high.",
         "viz": path([N("glu", "Glucose enters,\nATP rises", "molecule", 10, 55, 140, "teal"), N("katp", "K-ATP channel\ncloses", "membrane", 170, 55, 140, "blue"),
                      N("ca", "Depolarization,\nCa²⁺ in", "signal", 330, 55, 130, "amber"), N("ins", "Insulin\nreleased", "effect", 480, 55, 150, "sage"),
                      N("inc", "Incretin (GLP-1)\nsignal", "signal", 330, 150, 150, "deep")],
                     [["glu", "katp"], ["katp", "ca"], ["ca", "ins"], ["inc", "ins"]],
                     [Dg("Glipizide (sulfonylurea)", "katp", "Forces closure regardless of glucose — highest oral hypoglycemia risk (S11; S14)."),
                      Dg("Repaglinide (meglitinide)", "katp", "Mealtime secretagogue (S14; S28)."),
                      Dg("Semaglutide / sitagliptin", "inc", "Glucose-dependent release — low hypoglycemia risk (S11; S18).")],
                     "Forced vs. glucose-dependent release.", h=230)},
        {"image": "S13_1.jpg", "title": "Figure 16 · Insulin: receptor signaling and time-action profiles", "src": "S13; S13 (notes)",
         "caption": "Schematic (illustrative) — Figure 16. Teal: insulin binding; blue: intracellular signaling and glucose uptake; grey-green: liver; red: outcome. Right panel shows onset, peak and duration by insulin type: rapid (lispro, aspart), short (regular), NPH (peak ~4–10 h), basal (glargine, detemir, degludec).",
         "viz": {"type": "bars", "title": "Insulin onset", "yLabel": "Approximate onset (minutes, from the slides)",
                 "point": "Rapid-acting goes with the meal; regular goes 30 minutes before.",
                 "bars": [{"label": "Lispro/aspart", "value": 15, "col": "teal", "note": "Mealtime; onset ~15 min."},
                          {"label": "Regular", "value": 30, "col": "blue", "note": "Onset ~30 min; the only IV insulin."},
                          {"label": "NPH", "value": 120, "col": "amber", "note": "Cloudy; peaks ~4–10 h; variable."},
                          {"label": "Basal", "value": 60, "col": "sage", "note": "Glargine, detemir, degludec — peakless basal."}],
                 "steps": [{"label": "Rapid-acting", "pick": 0}, {"label": "Regular", "pick": 1}, {"label": "NPH", "pick": 2}, {"label": "Basal", "pick": 3}]}},
    ],
    "comparisons": [
        {"title": "Insulin by time-action (S12)", "columns": ["Type", "Examples", "Onset / profile", "Use"],
         "rows": [["Rapid-acting", "Lispro, aspart", "~15 min", "Mealtime"],
                  ["Short-acting", "Regular", "~30 min", "30 min before meals; only IV insulin"],
                  ["Intermediate", "NPH", "Cloudy; peak ~4–10 h; variable", "Basal/peak coverage"],
                  ["Long-acting", "Glargine, detemir, degludec", "Relatively peakless", "Basal coverage"]],
         "src": "S12; S13"},
        *tab((45, 46, 47, 48, 49, 50, 51), "Insulin profiles"),
    ],
    "hooks": [
        {"kind": "mnemonic", "text": "Rule of 15: 15 g fast carbohydrate, recheck in 15 minutes.", "src": "S13"},
    ],
    "high_yield": [
        F("Insulin’s main risk is hypoglycemia; beta-blockers mask its warning signs; only regular insulin goes IV.", "S12; S13"),
    ],
    "questions": [
        Q("vignette", "A patient on insulin and propranolol has a glucose of 45 mg/dL but no tremor or palpitations. Why?",
          "Beta-blockade masks warning symptoms",
          "Beta-blockers can mask hypoglycemia warning symptoms (S13; S67).",
          [("Insulin is no longer working", "Glucose is low (S13)."),
           ("Hypoglycemia never causes tremor", "Tremor is a warning sign masked here (S13)."),
           ("Propranolol raises glucose", "Not the reason (S13)."),
           ("The meter is reading falsely low", "Not the taught answer (S13).")], "S13; S67"),
        Q("mechanism", "Which insulin is the only one given intravenously?",
          "Regular insulin",
          "Only regular insulin is given IV (S12 notes).",
          [("Insulin glargine", "Basal, SC (S12)."),
           ("NPH insulin", "Cloudy suspension, SC (S12)."),
           ("Insulin degludec", "Basal, SC (S12)."),
           ("Insulin detemir", "Basal, SC (S12).")], "S12; S47"),
        Q("vignette", "A patient on insulin is shaky with glucose 58 mg/dL and can swallow. What first?",
          "15 g fast carbs, recheck in 15 min",
          "Rule of 15 (S13).",
          [("1 mg glucagon IM before any carbs", "For patients who cannot take oral carbs (S67)."),
           ("Skip the next meal and rest", "Treat now (S13)."),
           ("Give the next insulin dose early", "Worsens it (S13)."),
           ("Wait one hour, then recheck", "Treat now (S13).")], "S13"),
    ],
}

# ---------------------------------------------------------------- Part 3: non-insulin agents
t3 = {
    "name": "Non-Insulin Glucose-Lowering Drugs", "template": "drug_class", "objectives": ["SO2", "SO4", "IO4.1", "IO4.2", "IO4.3", "IO4.4", "IO4.5"],
    "sections": {
        "overview": [
            F("Four non-incretin oral cards: metformin, sulfonylureas/meglitinides, TZDs, SGLT2 inhibitors; then the incretin classes (GLP-1 RAs, DPP-4 inhibitors) and the site-of-action map.", "S14; S14 (notes)"),
            F("**Figure 19. Original illustrative diagram (not from Katzung): glucose-lowering drug classes act at distinct sites — pancreatic β-cell, liver, muscle/fat, kidney, gut, and the incretin axis — each converging on overall blood glucose control.**", "S17; S17 (notes)"),
        ],
        "prototype": [
            F("Metformin; glipizide, glyburide (sulfonylureas); repaglinide (meglitinide); pioglitazone (TZD); empagliflozin (SGLT2); exenatide, liraglutide, semaglutide (GLP-1 RA); sitagliptin, linagliptin (DPP-4).", "S14; S18"),
        ],
        "moa": [
            F("Metformin decreases hepatic gluconeogenesis: enters hepatocytes through OCT1 → inhibits mitochondrial complex I and activates AMPK → gluconeogenesis falls → insulin sensitivity improves in muscle → fasting glucose falls without hypoglycemia.", "S14; S15; S15 (notes)"),
            F("Sulfonylureas / meglitinides force K-ATP channel closure — insulin secretagogues (glipizide, glyburide, repaglinide). TZDs (pioglitazone) increase peripheral insulin sensitivity.", "S14"),
            F("Match each drug class to its mechanism/site: metformin — ↓ hepatic gluconeogenesis; sulfonylureas — force K-ATP channel closure (insulin secretagogue); TZDs — ↑ peripheral insulin sensitivity; SGLT2 inhibitors — block renal glucose reabsorption.", "SG U4-M; SG U4-R11"),
            F("GLP-1 receptor agonists — glucose-dependent insulin release, slowed gastric emptying; DPP-4 inhibitors — prevent endogenous GLP-1 breakdown (incretin pathway). Sulfonylureas carry the highest hypoglycemia risk (glucose-independent insulin release).", "SG U4-M; SG U4-R11"),
            F("SGLT2 inhibitors block renal glucose reabsorption: glucose is filtered at the glomerulus → SGLT2 in the proximal tubule normally reabsorbs about 90% → empagliflozin blocks SGLT2.", "S14; S16"),
            F("Glucose and water are lost in the urine (glucosuria) → glucose, weight and blood pressure fall; infection risk rises.", "S16; S16 (notes)"),
            F("GLP-1 receptor agonists: glucose-dependent insulin release, slow gastric emptying, promote satiety/weight loss. DPP-4 inhibitors prevent breakdown of endogenous GLP-1, prolonging its glucose-dependent effect.", "S18; S18 (notes)"),
            F("Incretin chain (Figure 20): food in the gut releases GLP-1 → GLP-1 acts on the beta cell: glucose-dependent insulin release, less glucagon → DPP-4 normally breaks GLP-1 down quickly.", "S19; S19 (notes)"),
            F("Sitagliptin blocks DPP-4; semaglutide and liraglutide mimic GLP-1 → lower glucose, slower gastric emptying and less appetite.", "S19"),
        ],
        "indications": [
            F("Metformin: first-line for type 2 diabetes; no weight gain and low hypoglycemia risk.", "S14; S15; S15 (notes)"),
            F("SGLT2 inhibitors: cardiorenal benefit — benefits in heart failure and chronic kidney disease, beyond glucose lowering.", "S14; S16; S16 (notes)"),
            F("**Figure 21. Original illustrative comparison (illustrative relative values, not from Katzung): insulin and sulfonylureas show the greatest HbA1c-lowering efficacy but also carry the highest hypoglycemia risk,**", "S20"),
            F("**while metformin, DPP-4 inhibitors, and SGLT2 inhibitors show a more favorable efficacy-to-hypoglycemia-risk balance.** ", "S20"),
            F("Figure 21 is the quantified summary of the drug-class discussion — it answers \"why is metformin still first-line\": not because it is the most potent, but because of its favorable risk profile.", "S20 (notes)"),
        ],
        "adverse": [
            F("Sulfonylureas: highest hypoglycemia risk among oral agents. TZDs: fluid retention/heart failure, weight gain.", "S14"),
            F("Metformin: GI upset is common — start low and take with food; vitamin B12 deficiency with long-term use; monitor B12 levels.", "S15; S15 (notes)"),
            F("SGLT2 inhibitors: genital yeast (mycotic) infections, volume depletion, euglycemic DKA — hold when ill or before surgery; rare Fournier gangrene.", "S14; S16; S16 (notes)"),
            F("GLP-1 RAs: nausea/GI upset, vomiting, pancreatitis risk and gallstones. DPP-4 inhibitors are generally weight-neutral, well tolerated, with low hypoglycemia risk.", "S18; S18 (notes); S19"),
        ],
        "contra": [
            F("Metformin: avoid in significant renal impairment — lactic acidosis risk; avoid when eGFR is below 30; hold for contrast dye with reduced kidney function (iodinated contrast).", "S14; S15; S15 (notes); S67"),
            F("GLP-1 RAs: contraindicated with personal or family history of medullary thyroid carcinoma or MEN2 (thyroid C-cell warning).", "S18; S18 (notes); S19"),
            F("SGLT2 inhibitors: avoid for glycemic effect when eGFR is low.", "S16"),
        ],
        "interactions": [
            F("Do not combine a GLP-1 RA with a DPP-4 inhibitor. Gemfibrozil raises repaglinide levels (CYP2C8).", "S19; S67"),
        ],
        "pk": [],
        "monitoring": [],
        "pearls": [
            F("Case: a 72-year-old with type 2 diabetes on metformin monotherapy, HbA1c above goal, lives alone, prior fall. **Which class of add-on therapy best balances efficacy and safety for this patient, and why?**", "S21; S21 (notes)"),
            F("**Given the fall history and the risks of hypoglycemia-induced falls, a DPP-4 inhibitor or SGLT2 inhibitor (low intrinsic hypoglycemia risk) is generally preferable to a sulfonylurea in an older adult living alone —**", "S21"),
            F("**matching drug choice to patient-specific risk, not just HbA1c-lowering potency.** ", "S21"),
            F("This vignette applies Figure 21 directly to a geriatric safety scenario: \"most potent\" and \"most appropriate\" are not always the same answer.", "S21 (notes)"),
            F("Drug names reveal the class: **-gliptin** DPP-4 inhibitor (sitagliptin, linagliptin; low hypoglycemia risk); **-glutide** GLP-1 receptor agonist (liraglutide, semaglutide; weight loss, GI upset).", "S28; S28 (notes)"),
            F("**-gliflozin** SGLT2 inhibitor (empagliflozin; genital infections, euglycemic DKA); **-glitazone** thiazolidinedione (pioglitazone; fluid retention, heart failure); **-glinide** meglitinide (repaglinide; mealtime insulin secretagogue).", "S28"),
            F("**gli- (prefix)** sulfonylurea (glipizide, glyburide; K-ATP closure, hypoglycemia); **-ifene** SERM (tamoxifen, raloxifene; tissue-selective estrogen action); **-steride** 5-alpha-reductase inhibitor (finasteride; lowers DHT); **-gestrel** progestin (levonorgestrel).", "S28"),
            F("**-calcet** calcimimetic (cinacalcet; activates the CaSR, lowers PTH). A stem is a memory aid, not a rule: where no shared stem exists, learn the class name instead.", "S28"),
        ],
    },
    "figures": [
        {"image": "S15_1.jpg", "title": "Figure 17 · Metformin: hepatic glucose output and AMPK", "src": "S15; S15 (notes)",
         "caption": "Schematic (illustrative) — Figure 17. Teal: drug entry; blue: AMPK signaling and glucose output; grey-green: muscle; short arrow = reduced gluconeogenesis; red: outcome — fasting glucose falls without hypoglycemia.",
         "viz": path([N("oct", "Enters liver\nvia OCT1", "membrane", 10, 55, 130, "teal"), N("ampk", "Complex I ↓,\nAMPK on", "enzyme", 160, 55, 130, "blue"),
                      N("gng", "Gluconeogenesis\nfalls", "effect", 310, 55, 140, "amber"), N("fg", "Fasting glucose ↓,\nno hypoglycemia", "effect", 470, 55, 160, "sage")],
                     [["oct", "ampk"], ["ampk", "gng"], ["gng", "fg"]],
                     [Dg("Metformin", "oct", "First line; GI upset, B12; hold for contrast; avoid eGFR < 30 (S15).")],
                     "Turn down the liver’s glucose factory.")},
        {"image": "S16_1.png", "title": "Figure 18 · SGLT2 inhibitors: glucose lost in the urine", "src": "S16; S16 (notes)",
         "caption": "Schematic (illustrative) — Figure 18. Teal: filtration; blue: tubule transport; green-grey: drug block; red: outcome, glucose lost in urine — lower glucose, weight and BP, with genital infection and euglycemic DKA risks.",
         "viz": path([N("f", "Glucose\nfiltered", "molecule", 10, 55, 120, "teal"), N("s", "SGLT2 reabsorbs\n~90%", "membrane", 150, 55, 150, "blue"),
                      N("bl", "Back to blood", "effect", 320, 10, 130, "amber"), N("ur", "Glucose and\nwater in urine", "effect", 320, 110, 140, "coral"),
                      N("ben", "Glucose, weight,\nBP fall", "effect", 480, 110, 150, "sage")],
                     [["f", "s"], ["s", "bl"], ["f", "ur"], ["ur", "ben"]],
                     [Dg("Empagliflozin", "s", "Heart failure and CKD benefit; yeast infections, euglycemic DKA (S16).", off=["bl"])],
                     "Spill glucose into the urine.", h=210)},
        {"image": "S17_1.jpg", "title": "Figure 19 · Glucose-lowering drugs by site of action", "src": "S17; S17 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): β-cell (sulfonylureas, meglitinides), liver (metformin), muscle/fat (TZDs), kidney (SGLT2 inhibitors), gut and incretin axis (GLP-1 RAs, DPP-4 inhibitors) — all converging on blood glucose.",
         "viz": path([N("b", "β-cell", "cell", 10, 10, 120, "blue"), N("l", "Liver", "cell", 10, 90, 120, "teal"),
                      N("m", "Muscle / fat", "cell", 10, 170, 120, "sage"), N("k", "Kidney", "cell", 220, 10, 120, "amber"),
                      N("g", "Gut / incretin", "cell", 220, 170, 130, "deep"), N("bg", "Blood glucose", "effect", 460, 90, 160, "coral")],
                     [["b", "bg"], ["l", "bg"], ["m", "bg"], ["k", "bg"], ["g", "bg"]],
                     [Dg("Glipizide", "b", "Secretagogue (S14)."), Dg("Metformin", "l", "↓ gluconeogenesis (S15)."),
                      Dg("Pioglitazone", "m", "↑ insulin sensitivity (S14)."), Dg("Empagliflozin", "k", "Glucosuria (S16)."),
                      Dg("Semaglutide / sitagliptin", "g", "Incretin axis (S18–S19).")],
                     "Place each class on the map.", h=250)},
        {"image": "S19_1.png", "title": "Figure 20 · Incretin drugs: gut, pancreas and brain", "src": "S19; S19 (notes)",
         "caption": "Schematic (illustrative) — Figure 20. Teal: gut signal; blue: beta-cell and enzyme steps; green-grey: drugs; red: clinical outcome. GLP-1 RAs mimic GLP-1; DPP-4 inhibitors protect it — lower glucose, slower gastric emptying, less appetite.",
         "viz": path([N("food", "Food releases\nGLP-1", "molecule", 10, 55, 130, "teal"), N("beta", "β-cell: insulin ↑\n(glucose-dependent)", "cell", 160, 55, 170, "blue"),
                      N("dpp", "DPP-4 breaks\nGLP-1 down", "enzyme", 160, 150, 150, "amber"), N("out", "Glucose ↓, slower\nemptying, less appetite", "effect", 350, 55, 200, "sage")],
                     [["food", "beta"], ["beta", "out"], ["food", "dpp"]],
                     [Dg("Semaglutide / liraglutide", "beta", "Mimic GLP-1; weight loss; MTC/MEN2 contraindication (S18–S19)."),
                      Dg("Sitagliptin", "dpp", "Blocks DPP-4; weight neutral (S18–S19).", off=["dpp"])],
                     "Mimic the hormone or protect it.", h=230)},
        {"image": "S20_1.jpg", "title": "Figure 21 · HbA1c lowering vs. hypoglycemia risk", "src": "S20; S20 (notes)",
         "caption": "Original illustrative comparison (illustrative relative values, not from Katzung): insulin and sulfonylureas lower HbA1c most but carry the highest hypoglycemia risk; metformin, DPP-4 inhibitors and SGLT2 inhibitors balance efficacy and hypoglycemia risk more favorably.",
         "viz": {"type": "bars", "title": "Efficacy vs. hypoglycemia", "yLabel": "Illustrative relative hypoglycemia risk",
                 "point": "Most potent is not always most appropriate.",
                 "bars": [{"label": "Insulin", "value": 90, "col": "coral", "note": "Greatest efficacy; highest hypoglycemia risk."},
                          {"label": "Sulfonylurea", "value": 75, "col": "amber", "note": "Forces insulin release at any glucose."},
                          {"label": "Metformin", "value": 10, "col": "teal", "note": "First line; low risk."},
                          {"label": "DPP-4", "value": 10, "col": "blue", "note": "Glucose-dependent; low risk."},
                          {"label": "SGLT2", "value": 10, "col": "sage", "note": "Glucosuria; low risk."}],
                 "steps": [{"label": "Insulin", "pick": 0}, {"label": "Sulfonylurea", "pick": 1}, {"label": "Metformin", "pick": 2}, {"label": "DPP-4 inhibitor", "pick": 3}, {"label": "SGLT2 inhibitor", "pick": 4}]}},
    ],
    "comparisons": [
        {"title": "Glucose-lowering classes (S14; S18)", "columns": ["Class", "Example", "Mechanism", "Key risk"],
         "rows": [["Metformin", "Metformin", "↓ Hepatic gluconeogenesis", "GI, B12; lactic acidosis — avoid eGFR < 30"],
                  ["Sulfonylureas / meglitinides", "Glipizide, glyburide, repaglinide", "Force K-ATP closure", "Highest oral hypoglycemia risk"],
                  ["TZDs", "Pioglitazone", "↑ Peripheral insulin sensitivity", "Fluid retention/heart failure, weight gain"],
                  ["SGLT2 inhibitors", "Empagliflozin", "Block renal glucose reabsorption", "Genital mycotic infection, euglycemic DKA"],
                  ["GLP-1 RAs", "Exenatide, liraglutide, semaglutide", "Glucose-dependent insulin; slow emptying", "GI, pancreatitis; MTC/MEN2"],
                  ["DPP-4 inhibitors", "Sitagliptin, linagliptin", "Protect endogenous GLP-1", "Weight-neutral; low hypoglycemia"]],
         "src": "S14; S18"},
        *tab((52, 53, 54, 55, 56, 57), "Oral glucose-lowering profiles"),
        *tab((58, 59, 60, 61, 62), "Incretin drug profiles"),
    ],
    "hooks": [
        {"kind": "why", "text": "Why do DPP-4 inhibitors rarely cause hypoglycemia? The incretin effect only boosts insulin when glucose is already high; sulfonylureas push insulin out regardless.", "src": "S11; S35"},
    ],
    "high_yield": [
        F("Metformin first-line (no weight gain, low hypoglycemia); avoid eGFR < 30; hold for contrast; B12.", "S14; S15"),
        F("Older adult with falls → DPP-4 or SGLT2, not a sulfonylurea.", "S21"),
    ],
    "questions": [
        Q("vignette", "A 72-year-old on metformin, living alone with a prior fall, needs an add-on. Which class fits best?",
          "A DPP-4 inhibitor or SGLT2 inhibitor",
          "Low intrinsic hypoglycemia risk; sulfonylureas risk hypoglycemia-induced falls (S21).",
          [("A sulfonylurea such as glyburide", "Highest oral hypoglycemia risk (S14)."),
           ("Mealtime insulin lispro", "Hypoglycemia risk (S12)."),
           ("A second sulfonylurea, glipizide", "Hypoglycemia risk (S14)."),
           ("Repaglinide before each meal", "Secretagogue, hypoglycemia (S14).")], "S21", from_slides="S21"),
        Q("mechanism", "Why do sulfonylureas carry a higher hypoglycemia risk than DPP-4 inhibitors?",
          "They force insulin release at any glucose",
          "Sulfonylureas close K-ATP channels regardless of glucose; incretins act only when glucose is elevated (S35).",
          [("DPP-4 inhibitors do not affect insulin", "They prolong GLP-1 (S35)."),
           ("Sulfonylureas work only in type 1", "Type 2 agents (S35)."),
           ("There is no difference in risk", "There is (S35)."),
           ("DPP-4 inhibitors raise glucagon", "They lower it (S19).")], "S34; S35", from_slides="S34; S35"),
        Q("mechanism", "A patient on an SGLT2 inhibitor develops a genital yeast infection. What is the mechanism?",
          "More urinary glucose feeds fungal growth",
          "Blocking renal glucose reabsorption raises urinary glucose, favoring fungal overgrowth (S35).",
          [("Direct immunosuppression by the drug", "Not the mechanism (S35)."),
           ("Decreased renal blood flow", "Not the mechanism (S35)."),
           ("Systemic candidemia from the drug", "Not the mechanism (S35)."),
           ("Euglycemic DKA lowering immunity", "Not the mechanism (S35).")], "S34; S35", from_slides="S34; S35"),
        Q("vignette", "A patient on metformin with eGFR 40 is scheduled for a CT with iodinated contrast. What should happen?",
          "Hold metformin around the contrast study",
          "Hold for contrast dye with reduced kidney function — lactic acidosis risk (S15; S67).",
          [("Double metformin to cover the stress", "Raises risk (S15)."),
           ("Continue without change", "Hold (S15)."),
           ("Switch to glyburide permanently", "Not the taught step (S15)."),
           ("Add an SGLT2 inhibitor the same day", "Not the answer (S16).")], "S15; S67"),
        Q("vignette", "A patient with a family history of medullary thyroid carcinoma asks about semaglutide for diabetes and weight. Best answer?",
          "Avoid GLP-1 RAs (C-cell warning)",
          "GLP-1 RAs are contraindicated with personal or family history of MTC or MEN2 (S19).",
          [("Safe; it only affects the gut", "C-cell warning (S19)."),
           ("Use it with a DPP-4 inhibitor", "Never combine (S19)."),
           ("Safe if taken with food", "Not relevant (S19)."),
           ("Only liraglutide is a concern", "Class warning (S18).")], "S18; S19"),
        Q("mechanism", "Which class most often causes fluid retention and can worsen heart failure?",
          "Thiazolidinediones (pioglitazone)",
          "TZDs: fluid retention/heart failure, weight gain (S14).",
          [("SGLT2 inhibitors (empagliflozin)", "Benefit heart failure (S16)."),
           ("DPP-4 inhibitors (sitagliptin)", "Weight neutral (S18)."),
           ("Biguanides (metformin)", "No fluid retention (S15)."),
           ("GLP-1 agonists (liraglutide)", "Weight loss (S18).")], "S14; S56"),
    ],
}

# ---------------------------------------------------------------- Part 4: parathyroid
t4 = {
    "name": "Parathyroid Disorders", "template": "drug_class", "objectives": ["SO3", "IO4.1", "IO4.4", "IO4.5"],
    "sections": {
        "overview": [
            F("**A brief recap of bone pharmacology, then a new angle: PTH itself.** Unit 2 covered osteoporosis drug therapy in depth: bisphosphonates, denosumab, teriparatide, and raloxifene (a SERM, also discussed again this session).", "S22; S23"),
            F("That therapy targets bone remodeling directly, generally in patients with normal parathyroid function. **This section takes a different angle: what happens — and what drugs are used — when parathyroid hormone secretion itself is the primary problem.**", "S23; S23 (notes)"),
            F("**If you need a refresher on bisphosphonate dosing or denosumab safety, revisit the Unit 2, Session 2 materials — that content is not repeated here.**", "S23"),
            F("This section is intentionally NOT re-teaching osteoporosis pharmacotherapy — it is new content on parathyroid pathology, so don’t expect bisphosphonate-level detail here.", "S23 (notes)"),
            F("**Figure 22. Original illustrative diagram (not from Katzung): hyperparathyroidism (excess PTH, high calcium) is treated with cinacalcet to lower PTH,**", "S24"),
            F("**while hypoparathyroidism (deficient PTH, low calcium) is treated with calcitriol and oral calcium, sometimes with recombinant PTH 1-84 in severe cases.**", "S24"),
            F("Figure 22 is the organizing concept for the section — two opposite pathologies, two opposite drug strategies, both targeting the same hormone axis.", "S24 (notes)"),
        ],
        "prototype": [
            F("Cinacalcet (calcimimetic); calcitriol (active vitamin D) plus calcium; recombinant human PTH 1-84.", "S25"),
        ],
        "moa": [
            F("Cinacalcet — a calcimimetic; activates the calcium-sensing receptor on parathyroid cells, reducing PTH secretion.", "S25"),
            F("Chain (Figure 23): parathyroid cells sense calcium through the CaSR → low calcium keeps PTH release high → cinacalcet makes the receptor more sensitive to calcium.", "S26"),
            F("The cell reads calcium as high and lowers PTH → PTH and serum calcium fall.", "S26; S26 (notes)"),
            F("Calcitriol (active vitamin D) plus oral calcium — mainstay for hypoparathyroidism, since PTH deficiency impairs vitamin D activation; calcitriol bypasses the PTH activation step.", "S25; S25 (notes)"),
        ],
        "indications": [
            F("Cinacalcet: used for secondary hyperparathyroidism (e.g., in chronic kidney disease on dialysis) and parathyroid carcinoma.", "S25; S26"),
            F("Recombinant human PTH 1-84 — reserved for patients not adequately controlled on calcium/calcitriol alone.", "S25"),
        ],
        "adverse": [
            F("Cinacalcet adverse effects: nausea, hypocalcemia and QT prolongation, so monitor calcium.", "S26"),
        ],
        "contra": [],
        "interactions": [
            F("Cinacalcet is a CYP2D6 inhibitor. Thiazides raise calcium, loops lower it. Vitamin D (cholecalciferol) replaces or supports calcitriol in deficiency.", "S26; S67"),
        ],
        "pk": [],
        "monitoring": [
            F("Hyperparathyroidism — cinacalcet (lowers PTH secretion); hypoparathyroidism — calcitriol (bypasses the PTH-dependent vitamin D activation step) plus oral calcium.", "SG U4-R13"),
            F("Opposite monitoring targets: watch for hypocalcemia with cinacalcet, hypercalcemia/hypercalciuria with calcitriol/PTH replacement — a symmetry worth drawing out.", "S25; S25 (notes); S26"),
        ],
        "pearls": [
            F("Case: a patient with chronic kidney disease is found to have an elevated PTH level with low-normal serum calcium. A second, unrelated patient who underwent recent thyroidectomy develops perioral numbness and low serum calcium with a low PTH level.", "S27"),
            F("**How does drug therapy differ between these two patients?**", "S27"),
            F("**The CKD patient has secondary hyperparathyroidism and may benefit from cinacalcet to reduce PTH secretion.**", "S27"),
            F("**The post-thyroidectomy patient has surgical hypoparathyroidism (inadvertent parathyroid gland injury) and needs calcitriol plus calcium replacement — the opposite pharmacologic strategy for the opposite underlying problem.**", "S27; S27 (notes)"),
            F("Post-thyroidectomy hypoparathyroidism is a classic, testable scenario and a bridge back to thyroid surgery from Session 1 (antithyroid drugs can also precede surgical management).", "S27 (notes)"),
        ],
    },
    "figures": [
        {"image": "S24_1.jpg", "title": "Figure 22 · Parathyroid disorders: two opposite strategies", "src": "S24; S24 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): hyperparathyroidism (excess PTH, high calcium) → cinacalcet lowers PTH; hypoparathyroidism (deficient PTH, low calcium) → calcitriol plus oral calcium, sometimes recombinant PTH 1-84.",
         "viz": path([N("hyper", "Hyperpara-\nthyroidism", "cell", 10, 20, 150, "coral"), N("hypo", "Hypopara-\nthyroidism", "cell", 10, 140, 150, "blue"),
                      N("low", "PTH lowered", "effect", 330, 20, 150, "sage"), N("up", "Calcium and\nactive vit D restored", "effect", 330, 140, 190, "teal")],
                     [["hyper", "low"], ["hypo", "up"]],
                     [Dg("Cinacalcet", "hyper", "Watch hypocalcemia (S25–S26)."),
                      Dg("Calcitriol + calcium", "hypo", "Watch hypercalcemia (S25)."),
                      Dg("Recombinant PTH 1-84", "hypo", "If calcium/calcitriol fail (S25).")],
                     "Opposite problems, opposite drugs.", h=230)},
        {"image": "S26_1.png", "title": "Figure 23 · Cinacalcet: tricking the calcium-sensing receptor", "src": "S26; S26 (notes)",
         "caption": "Schematic (illustrative) — Figure 23. Teal: sensing; blue: PTH steps; green-grey: drug; red: outcome, PTH and calcium fall. Cinacalcet sensitizes the CaSR so the cell reads calcium as high.",
         "viz": path([N("casr", "CaSR senses\ncalcium", "membrane", 10, 55, 140, "teal"), N("pth", "PTH release", "signal", 170, 55, 130, "blue"),
                      N("ca", "Serum calcium", "molecule", 320, 55, 130, "amber"), N("out", "PTH and\ncalcium fall", "effect", 470, 55, 150, "sage")],
                     [["casr", "pth"], ["pth", "ca"], ["ca", "out"]],
                     [Dg("Cinacalcet", "casr", "CaSR more sensitive → PTH falls; nausea, hypocalcemia, QT; CYP2D6 inhibitor (S26).", less=["pth", "ca"])],
                     "Make the gland think calcium is high.")},
    ],
    "comparisons": [
        {"title": "Hyperparathyroidism vs. hypoparathyroidism therapy (S25)", "columns": ["", "Hyperparathyroidism", "Hypoparathyroidism"],
         "rows": [["Drug", "Cinacalcet (calcimimetic)", "Calcitriol + oral calcium; PTH 1-84 if refractory"],
                  ["How", "Activates CaSR → ↓ PTH", "Bypasses the PTH-dependent vitamin D activation"],
                  ["Typical patient", "CKD on dialysis; parathyroid carcinoma", "Post-thyroidectomy"],
                  ["Monitor for", "Hypocalcemia", "Hypercalcemia / hypercalciuria"]],
         "src": "S25; S26; S27"},
        *tab((63, 64, 65, 66), "Parathyroid and calcium profiles"),
    ],
    "hooks": [
        {"kind": "why", "text": "Why calcitriol, not plain vitamin D, after thyroidectomy? Activating vitamin D needs PTH; calcitriol is already active.", "src": "S25; S35"},
    ],
    "high_yield": [
        F("High PTH (CKD) → cinacalcet, watch hypocalcemia; low PTH (post-thyroidectomy) → calcitriol + calcium, watch hypercalcemia.", "S25; S27"),
    ],
    "questions": [
        Q("vignette", "After thyroidectomy, a patient has perioral numbness, low calcium and low PTH. Which therapy is the mainstay?",
          "Calcitriol plus oral calcium",
          "PTH is needed to activate vitamin D; calcitriol bypasses it, with oral calcium (S35).",
          [("Cinacalcet alone", "Lowers PTH — wrong direction (S35)."),
           ("Bisphosphonate plus denosumab", "Osteoporosis drugs (S35)."),
           ("Levothyroxine plus methimazole", "Thyroid drugs (S35)."),
           ("Plain cholecalciferol alone", "Needs activation by PTH (S25).")], "S27; S34; S35", from_slides="S34; S35"),
        Q("vignette", "A dialysis patient has an elevated PTH with low-normal calcium. Which drug lowers PTH secretion?",
          "Cinacalcet",
          "Calcimimetic for secondary hyperparathyroidism in CKD; monitor for hypocalcemia (S25–S27).",
          [("Calcitriol", "Hypoparathyroidism (S25)."),
           ("Recombinant PTH 1-84", "Adds PTH (S25)."),
           ("Calcium carbonate", "Supplement (S66)."),
           ("Teriparatide", "Unit 2 osteoporosis (S23).")], "S25; S27", from_slides="S27"),
        Q("mechanism", "What should be monitored after starting cinacalcet?",
          "Serum calcium for hypocalcemia",
          "Cinacalcet lowers PTH and calcium; monitor for hypocalcemia (and QT) (S25–S26).",
          [("Calcium for hypercalcemia", "That is calcitriol (S25)."),
           ("Potassium for hyperkalemia", "Not the taught target (S26)."),
           ("Glucose for hypoglycemia", "Not the taught target (S26)."),
           ("TSH for hypothyroidism", "Not the taught target (S26).")], "S25; S26"),
    ],
}

# ---------------------------------------------------------------- Part 5: integration
t5 = {
    "name": "Putting It All Together: Endocrine Toolkit", "template": "concept", "objectives": ["SO5", "IO4.3", "IO4.4", "IO4.6"],
    "sections": {
        "definitions": [
            F("**Applying the whole Endocrine pharmacology toolkit.** The shared principle is negative feedback suppression by exogenous hormone. For each patient, name a first-line approach AND the single biggest safety concern.", "S29; S29 (notes); S30 (notes)"),
        ],
        "how": [
            F("**1.** The hypothalamic-pituitary-target gland axis is a shared template across thyroid, adrenal, and gonadal pharmacology — exogenous hormone therapy suppresses the levels above it via negative feedback.", "S31"),
            F("**2.** Antithyroid drug selection (methimazole vs. PTU) and glucocorticoid tapering both hinge on understanding exactly where and how each drug intervenes in its pathway.", "S31"),
            F("**3.** Glucose-lowering drugs act at distinct sites (pancreas, liver, muscle/fat, kidney, gut, incretin axis) — drug selection balances efficacy against hypoglycemia and other class-specific risks.", "S31"),
            F("**4.** Hyperparathyroidism and hypoparathyroidism require opposite drug strategies (lowering vs. raising effective PTH activity) — a new angle distinct from, but related to, the osteoporosis pharmacotherapy of Unit 2.", "S31"),
            F("**5.** Endocrine pharmacology is deeply interconnected — spironolactone, dopamine agonists, and SERMs each reappear across more than one organ system in this unit alone.", "S31"),
            F("Connecting back: osteoporosis pharmacology (Unit 2) and drug-metabolism/interaction concepts (Unit 1) both reappear here — pharmacology is cumulative, not siloed by unit.", "S31 (notes)"),
        ],
        "clinical": [
            F("**Patient A — Graves disease, in thyroid storm:** PTU (blocks synthesis and peripheral T4-to-T3 conversion); check liver toxicity.", "S30; S35"),
            F("**Patient B — chronic prednisone user, abruptly out of refills:** restart the glucocorticoid and taper; the risk is adrenal insufficiency from HPA suppression.", "S30; S35"),
            F("**Patient C — type 2 diabetes, older adult with fall history, needs add-on therapy:** DPP-4 or SGLT2 inhibitor; avoid sulfonylurea hypoglycemia.", "S30; S21"),
            F("**Patient D — post-thyroidectomy, perioral numbness and low calcium:** calcitriol plus calcium; monitor for hypercalcemia.", "S30; S27"),
        ],
        "examples": [
            F("**A cumulative self-test spanning both sessions — use this to review before exams.** The recall quiz is a standalone resource, separate from in-lecture quick checks.", "S32; S32 (notes); S35 (notes)"),
            F("**Recall Q1:** PTU blocks both new thyroid hormone synthesis and peripheral T4-to-T3 conversion, giving it a faster effect on circulating active hormone than methimazole — important in thyroid storm.", "S33; S35"),
            F("**Recall Q2:** a patient on chronic glucocorticoid therapy abruptly stops the medication and develops hypotension and weakness: HPA-axis suppression leaves endogenous cortisol production unable to resume quickly.", "S33; S35"),
            F("Chronic exogenous glucocorticoid exposure suppresses CRH/ACTH via negative feedback (Figure 9), reducing the adrenal cortex’s stimulus; abrupt withdrawal does not give the axis time to recover, precipitating adrenal insufficiency.", "S35"),
            F("**Recall Q3:** smoking at 35 or older contraindicates estrogen-containing contraception (thromboembolic and cardiovascular risk). **Q4:** sulfonylureas force K-ATP closure regardless of glucose; incretins act only when glucose is high.", "S33; S34; S35"),
            F("**Recall Q4 distractor:** DPP-4 inhibitors do affect insulin secretion — they prolong GLP-1’s glucose-dependent effect.", "S34; S35"),
            F("**Recall Q5:** a patient with hypoparathyroidism after thyroid surgery needs treatment — the mainstay is calcitriol plus oral calcium: because PTH is required to activate vitamin D, calcitriol (already-active vitamin D) bypasses that activation step.", "S34; S35; SG U4-R13"),
            F("**Recall Q6:** SGLT2 inhibitors block renal glucose reabsorption, increasing urinary glucose excretion and creating a favorable environment for genital fungal overgrowth — a mechanism-based adverse effect.", "S34; S35; SG U4-R12"),
        ],
        "traps": [
            F("Choosing the most potent glucose-lowering drug instead of the safest for an older adult who falls.", "S21 (notes)"),
            F("Integrated case — diabetes: a DPP-4 or SGLT2 inhibitor is preferable to a sulfonylurea given the fall history — sulfonylureas force glucose-independent insulin release, raising hypoglycemia-driven fall risk.", "SG U4-S"),
            F("Integrated case — thyroid storm: beta-blocker + PTU first, then iodine solution only after PTU (never before — iodine first would supply substrate for new hormone synthesis before synthesis is blocked, worsening the crisis).", "SG U4-S"),
            F("Corticosteroids also help in thyroid storm by blunting peripheral conversion and covering relative adrenal insufficiency.", "SG U4-S"),
            F("Shared concept: effective endocrine drug selection depends on knowing exactly where in a pathway (or which receptor/site) a drug acts — that position determines both its efficacy and its specific risks.", "SG U4-S"),
        ],
    },
    "comparisons": [
        {"title": "Which drug would you choose? (S30)", "columns": ["Patient", "Approach", "Biggest safety check"],
         "rows": [["A · Graves disease, thyroid storm", "PTU", "Liver toxicity"],
                  ["B · Chronic prednisone, out of refills", "Restart and taper the glucocorticoid", "Adrenal insufficiency"],
                  ["C · Older adult with type 2 diabetes and falls", "DPP-4 or SGLT2 inhibitor", "Avoid sulfonylurea hypoglycemia"],
                  ["D · Post-thyroidectomy, low calcium", "Calcitriol + calcium", "Hypercalcemia"]],
         "src": "S30; S35"},
        {"title": "Supporting drugs at a glance (S67)", "columns": ["Drug(s)", "Why it matters here"],
         "rows": [["**Rifampin, carbamazepine, phenytoin**", "**CYP inducers that lower contraceptive efficacy**"],
                  ["**Paroxetine and fluoxetine**", "**CYP2D6 inhibitors that blunt tamoxifen activation**"],
                  ["**Glucagon and dextrose**", "**Rescue for severe hypoglycemia**"],
                  ["**Beta-blockers**", "**Can mask hypoglycemia symptoms**"],
                  ["**Iodinated contrast**", "**Hold metformin in reduced kidney function**"],
                  ["**Gemfibrozil**", "**Raises repaglinide levels (CYP2C8)**"],
                  ["**Bisphosphonates and denosumab**", "**Osteoporosis agents covered in Unit 2**"],
                  ["**Thiazide and loop diuretics**", "**Thiazides raise calcium, loops lower it**"],
                  ["**Vitamin D (cholecalciferol)**", "**Replaces or supports calcitriol in deficiency**"]],
         "src": "S67; S67 (notes)"},
    ],
    "hooks": [
        {"kind": "mnemonic", "text": "Every case, two answers: **the approach** and **the one thing to check**.", "src": "S30 (notes)"},
    ],
    "high_yield": [
        F("Five takeaways: shared axis template · know where each drug intervenes · glucose drugs by site · opposite parathyroid strategies · cross-system drugs.", "S31"),
    ],
    "questions": [
        Q("mechanism", "Why is PTU, rather than methimazole, preferred in thyroid storm?",
          "PTU also blocks peripheral T4-to-T3 conversion",
          "PTU blocks synthesis and peripheral conversion, a faster effect on active hormone (S35).",
          [("PTU is better absorbed orally", "Not the reason (S35)."),
           ("PTU has no hepatotoxicity risk", "Not true (S35)."),
           ("PTU works faster at iodide trapping", "Not the reason (S35)."),
           ("PTU is longer acting than methimazole", "Not the reason (S35).")], "S33; S35", from_slides="S33; S35"),
        Q("mechanism", "A patient on chronic prednisone stops abruptly and becomes hypotensive and weak. What is the mechanism?",
          "Suppressed HPA axis cannot restart quickly",
          "Chronic glucocorticoids suppress CRH/ACTH; abrupt withdrawal precipitates adrenal insufficiency (S35).",
          [("Direct adrenal destruction by the drug", "Suppression, not destruction (S35)."),
           ("An allergic reaction to prednisone", "Not the mechanism (S35)."),
           ("Excess aldosterone production", "Not the mechanism (S35)."),
           ("Prednisone-induced hypoglycemia", "Not the mechanism (S35).")], "S33; S35", from_slides="S33; S35"),
        Q("vignette", "Which counseling point reflects a true contraindication to estrogen-containing contraception?",
          "Smoking at age 35 or older",
          "Smoking at 35 or older raises thromboembolic and cardiovascular risk (S35).",
          [("Age under 20 at the first visit", "Not a contraindication (S35)."),
           ("Mild seasonal allergies each spring", "Not a contraindication (S35)."),
           ("Family history of type 2 diabetes", "Not a contraindication (S35)."),
           ("Regular moderate exercise", "Not a contraindication (S35).")], "S33; S35", from_slides="S33; S35"),
    ],
}

content = {
    "lecture": {"id": "L08", "title": "Endocrine Pharmacotherapy — Session 2", "date": "Thu, Nov 12, 2026"},
    "textbook_status": "included",
    "objectives": objectives,
    "about": about,
    "classes": [t1, t2, t3, t4, t5],
    "notebooklm": {
        "patient": "a 72-year-old with type 2 diabetes on metformin who lives alone and has fallen, a smoker over 35 asking for contraception, a CKD patient with high PTH, and a post-thyroidectomy patient with perioral numbness (the lecture’s cases)",
        "suggested_questions": [
            "How does combined contraception suppress the HPG axis, and who should not get estrogen?",
            "Compare tamoxifen and raloxifene tissue by tissue.",
            "Sort the insulins by onset and explain the rule of 15.",
            "Place each glucose-lowering class on the site-of-action map.",
            "Why choose a DPP-4 or SGLT2 inhibitor over a sulfonylurea in an older adult?",
            "Compare cinacalcet with calcitriol plus calcium.",
        ],
    },
    "audit_skip": [
        {"ref": "S1", "starts_with": "Diane", "reason": "instructor name (no names on the site)"},
        {"ref": "S2", "starts_with": "Briefly recap", "reason": "teaching instruction; the recap is in About this lecture"},
        {"ref": "S2", "starts_with": "Read the two objectives", "reason": "teaching instruction"},
        *[{"ref": r, "starts_with": "Section transition", "reason": "section divider"} for r in ("S3", "S10", "S22", "S29", "S32")],
        {"ref": "S4", "starts_with": "Estrogen plus progestin suppress", "reason": "presenter script; taught from S4"},
        {"ref": "S12", "starts_with": "Sort insulins", "reason": "presenter script; taught from S12"},
        {"ref": "S14", "starts_with": "Classes overview", "reason": "presenter script"},
        {"ref": "S14", "starts_with": "This four-card split", "reason": "teaching instruction; taught in the overview"},
        {"ref": "S17", "starts_with": "Use this as the capstone", "reason": "teaching instruction; the map is the Figure 19 interactive"},
        {"ref": "S17", "starts_with": "Place each class", "reason": "teaching instruction"},
        {"ref": "S18", "starts_with": "The \"glucose-dependent\" mechanism", "reason": "teaching instruction; taught with Figure 15"},
        {"ref": "S20", "starts_with": "Figure 21: efficacy", "reason": "presenter script"},
        {"ref": "S21", "starts_with": "Case: a 72-year-old", "reason": "presenter script; the case is rebuilt as a practice question"},
        {"ref": "S23", "starts_with": "Recap of calcium", "reason": "presenter script; taught from S23"},
        {"ref": "S24", "starts_with": "Figure 22: two opposite", "reason": "presenter script"},
        {"ref": "S27", "starts_with": "Case: elevated PTH", "reason": "presenter script; the case is rebuilt as a practice question"},
        {"ref": "S28", "starts_with": "Drug name stems", "reason": "presenter script; the stems are taught in Non-Insulin Glucose-Lowering Drugs"},
        {"ref": "S30", "starts_with": "Have students work", "reason": "teaching instruction"},
        {"ref": "S30", "starts_with": "Pairs name", "reason": "teaching instruction"},
        {"ref": "S31", "starts_with": "Read the takeaways", "reason": "teaching instruction"},
        {"ref": "S33", "starts_with": "Students work", "reason": "teaching instruction"},
        {"ref": "S34", "starts_with": "Students work", "reason": "teaching instruction"},
        {"ref": "S35", "starts_with": "Use the answer key", "reason": "teaching instruction"},
        {"ref": "S36", "starts_with": "How to use in class", "reason": "teaching instruction"},
        {"ref": "S36", "starts_with": "Teaching points by class", "reason": "teaching instruction"},
        *[{"ref": "S36", "starts_with": w, "reason": "Bloom's teaching prompt; rebuilt as practice questions"} for w in ("Bloom", "Understand", "Apply", "Analyze", "Evaluate")],
        {"ref": "S14", "starts_with": "Metformin, SGLT2 inhibitors and incretin", "reason": "presenter script (signpost to next slides)"},
        {"ref": "S22", "starts_with": "Today we finish", "reason": "section divider"},
        {"ref": "S25", "starts_with": "Hyperparathyroidism vs.", "reason": "presenter script fragment; taught from S25"},
        {"ref": "S67", "starts_with": "Read quickly", "reason": "teaching instruction"},
        {"ref": "S68", "starts_with": "This slide documents", "reason": "administrative note on AI-tool citation"},
        {"ref": "S68", "starts_with": "Figures 11, 15, 19, 21 and 22 are original", "reason": "administrative note on AI-tool citation"},
    ],
}

for _cl in content["classes"]:
    for _fg in _cl.get("figures", []):
        if not _fg["viz"].get("title"):
            _fg["viz"]["title"] = _fg["title"].split("·", 1)[-1].strip()

sys.path.insert(0, str(Path(__file__).parent))
import guide_L08 as G  # noqa: E402
content["guide"] = {"summary": [{"text": t, "src": s} for t, s in G.SUMMARY], "teaser": getattr(G, "TEASER", ""),
                    "cram": [{"prompt": p, "answer": a, "src": s} for p, a, s in G.CRAM], "discrepancies": []}
for _cl in content["classes"]:
    _cl["flows"] = G.FLOWS.get(_cl["name"], [])

import textbook_L08 as TBK  # noqa: E402
_by_name = {cl["name"]: cl for cl in content["classes"]}
for _name, _secs in TBK.ADD.items():
    for _key, _facts in _secs.items():
        _by_name[_name]["sections"].setdefault(_key, [])
        _by_name[_name]["sections"][_key] += [F(t, s, tb=True) for t, s in _facts]
for _cl in [c for c in content["classes"] if "adverse" in c["sections"]]:
    _adv = _cl["sections"]["adverse"]
    _box = lambda f: "boxed" in f["text"].lower()  # noqa: E731
    _cl["sections"]["adverse"] = [f for f in _adv if _box(f)] + [f for f in _adv if not _box(f)]
for _name, _cfs in TBK.CONFLICTS.items():
    _by_name[_name].setdefault("conflicts", []).extend(_cfs)
for _q in TBK.QUESTIONS:
    _q = dict(_q)
    _topic = _q.pop("topic")
    _by_name[_topic]["questions"].append({**Q(**_q), "tb": True})
for _name, _tbls in TBK.COMPARISONS.items():
    _by_name[_name].setdefault("comparisons", []).extend(_tbls)
for _name, (_ch, _a, _b, _why) in TBK.DEEPER.items():
    _by_name[_name]["deeper"] = {"chapter": _ch, "first": _a, "last": _b, "why": _why}
content["guide"]["discrepancies"] = [{"text": t, "src": s} for t, s in TBK.DISCREPANCIES]
content["guide"]["cram"] += [{"prompt": p, "answer": a, "src": s, "tb": True} for p, a, s in TBK.CRAM]

out = Path(__file__).with_name("content.json")
out.write_text(json.dumps(content, indent=1, ensure_ascii=False))
print(f"wrote {out}")
