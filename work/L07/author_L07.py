"""Authoring source for L07 content.json. Run: python3 author_L07.py"""
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


PROF = {p["slide"]: p for p in PR.read("L07")}


def prof(*slides):
    return [PROF[s] for s in slides]


def tab(slides, title):
    return PR.table(prof(*slides), title)


def path(nodes, edges, drugs, point, h=170, read="Pick a drug to see where it acts."):
    return {"type": "pathway", "title": "", "h": h, "point": point, "nodes": nodes, "edges": edges, "drugs": drugs, "read": read}


def N(id, label, glyph, x, y, w, col):
    return {"id": id, "label": label, "glyph": glyph, "x": x, "y": y, "w": w, "col": col}


def Dg(label, at, note, off=(), less=(), more=()):
    return {"label": label, "at": at, "off": list(off), "less": list(less), "more": list(more), "note": note}


objectives = [
    {"id": "IO4.1", "src": "Syllabus", "text": "Identify major pharmacologic classes used in the management of endocrine conditions and describe their mechanisms of action."},
    {"id": "IO4.2", "src": "Syllabus", "text": "Describe the indications, contraindications, adverse effects, and clinically significant interactions associated with medications used to treat endocrine conditions."},
    {"id": "IO4.3", "src": "Syllabus", "text": "Compare pharmacologic agents within and across therapeutic classes to distinguish clinically relevant differences in efficacy, safety, and use."},
    {"id": "IO4.4", "src": "Syllabus", "text": "Select appropriate pharmacologic therapy for common endocrine conditions based on clinical presentation and patient-specific factors."},
    {"id": "IO4.5", "src": "Syllabus", "text": "Identify appropriate dosing, administration, and monitoring considerations for medications used in endocrine conditions."},
    {"id": "IO4.6", "src": "Syllabus", "text": "Explain important medication-use and safety information to patients receiving pharmacotherapy for endocrine conditions."},
    {"id": "SO1", "src": "S2", "text": "Describe the hypothalamic-pituitary-target gland axis as a shared regulatory template, and identify where drug therapy intervenes at each level."},
    {"id": "SO2", "src": "S2", "text": "Identify the major agents used for growth hormone disorders, hyperprolactinemia, and disorders of antidiuretic hormone (diabetes insipidus, SIADH)."},
    {"id": "SO3", "src": "S2", "text": "Describe the mechanisms, indications, and monitoring of thyroid hormone replacement and antithyroid drug therapy, including management of thyroid storm."},
    {"id": "SO4", "src": "S2", "text": "Compare glucocorticoid and mineralocorticoid pharmacology, and identify agents used to block adrenocortical hormone synthesis or action."},
    {"id": "SO5", "src": "S2", "text": "Identify dosing, administration, and monitoring considerations, and explain key medication-safety counseling points to patients, including HPA-axis suppression and the need to taper chronic glucocorticoids."},
]

about = [
    F("**PA PHARMACOLOGY COURSE · LECTURE 4 · SESSION 1 OF 2** — Endocrine Pharmacotherapy. **Session 1: Pituitary, Thyroid, and Adrenal Pharmacology  |  Tuesday, November 10  |  8:30–11:00 AM**", "S1"),
    F("One template runs this whole unit: hypothalamus drives the pituitary, the pituitary drives a target gland, and the gland’s hormone feeds back to turn the levels above it down. Every drug today replaces a hormone, blocks one, or interrupts that loop.", "S1 (notes); S4 (notes)"),
    F("Arc: the shared HPA-template concept, then pituitary, thyroid and adrenal in turn. Preview: gonadal hormones, pancreatic/diabetes pharmacology, and parathyroid disorders continue in Session 2 (Thursday, November 12).", "S2"),
    F("Orient to the arc: the shared HPA-template concept, then three organ systems in turn (pituitary, thyroid, adrenal) that all follow the same hypothalamic-pituitary-target gland logic of Figure 1; Session 2 continues with gonadal hormones, diabetes, and parathyroid disorders on Nov 12.", "S2 (notes)"),
    F("Readings: Katzung’s Chapters 37–42 are required for Unit 4 (Hypothalamic & Pituitary Hormones; Thyroid & Antithyroid Drugs; Adrenocorticosteroids & Adrenocortical Antagonists; Gonadal Hormones & Inhibitors; Pancreatic Hormones & Glucose-Lowering Drugs; Agents That Affect Bone Mineral Homeostasis).", "S3; S3 (notes)"),
    F("Session 1 covers Chapters 37–39; Session 2 covers Chapters 40–42. Recommended: Pharmacotherapy Principles and Practice (Chisholm-Burns, Schwinghammer, Malone, Kolesar, Lee, 2022, McGraw-Hill; print ISBN 9781260460278, eText ISBN 9781260460285) as supplemental support, not a substitute.", "S3; S3 (notes)"),
    F("Required text: Katzung’s Basic and Clinical Pharmacology, 16th Edition (Todd W. Vanderah, 2024/2025, McGraw-Hill Education; ISBN 1260463303 eBook).", "S3"),
    F("**APPENDIX 1** gives **Formulation, dose, indications, adverse effects, contraindications and toxicity** — your study reference: know the dose logic, the one or two serious adverse effects, the contraindication that changes the decision, and the toxicity you would need to recognize.", "S29; S29 (notes); S30-51"),
    F("**Abbreviation key** **PO** **= by mouth** **SC** **= subcutaneous** **IM** **= intramuscular** **IV** **= intravenous** **ER** **= extended-release** **ODT** **= orally disintegrating tablet** **LAR** **= long-acting release** **BID / TID / QID** **= two / three / four times daily** **mcg** **= microgram**", "S29; S29 (notes)"),
    F("**GH** **= growth hormone** **IGF-1** **= insulin-like growth factor 1** **TSH** **= thyroid-stimulating hormone** **T4 / T3** **= thyroxine / triiodothyronine** **DI** **= diabetes insipidus** **SIADH** **= syndrome of inappropriate ADH secretion** **HPA** **= hypothalamic-pituitary-adrenal**", "S29; S29 (notes)"),
    F("**CBC** **= complete blood count** **LFT** **= liver function tests** **QT** **= QT interval on ECG** **CYP** **= cytochrome P450** **MI** **= myocardial infarction** **MRI** **= magnetic resonance imaging** **ARB** **= angiotensin receptor blocker** **AV** **= atrioventricular** **CNS** **= central nervous system**", "S29; S29 (notes)"),
    F("**Appendix 2: DRUG PROFILE · SUPPORTING** — supporting drugs explain interactions, not doses. Listed for context; not profiled in detail.", "S52; S52 (notes)"),
    F("**Original figures in this deck:** Figures 1, 6 and 9 (The Hypothalamic-Pituitary-Target Gland Axis; Thyroid Hormone Synthesis: Where Antithyroid Drugs Act; Exogenous Corticosteroids and HPA Axis Suppression) were generated by the course director using the AI tool Claude to illustrate standard, non-copyrighted pharmacologic concepts.", "S53"),
    F("They are original diagrams, not reproduced from Katzung’s Basic and Clinical Pharmacology or any other copyrighted source. **Mechanism illustrations:** (AI-generated, illustrative, not reproduced from copyrighted sources; schematic and not to scale): somatostatin analogs and pegvisomant (Figure 2, slide 7); dopamine agonists (Figure 3, slide 9);", "S53; S53 (notes)"),
    F("ADH, desmopressin and tolvaptan (Figure 4, slide 10); levothyroxine absorption (Figure 5, slide 15); thyroid storm targets (Figure 7, slide 19); glucocorticoid receptor signaling (Figure 8, slide 25); steroid synthesis and receptor blockade (Figure 10, slide 30). **Reference:** Anthropic. (2026). Claude (Sonnet 5) [Large language model]. https://claude.ai", "S53"),
]

# ---------------------------------------------------------------- Part 1: pituitary
t1 = {
    "name": "Pituitary: GH, Prolactin & ADH", "template": "drug_class", "objectives": ["SO1", "SO2", "IO4.1", "IO4.2", "IO4.4", "IO4.5"],
    "sections": {
        "overview": [
            F("**One regulatory template governs thyroid, adrenal, and gonadal control alike.**", "S4"),
            F("**Figure 1. Original illustrative diagram (not from Katzung): the hypothalamus drives the anterior pituitary, which drives a target endocrine gland, whose peripheral hormone produces end-organ effects and negatively feeds back to suppress the levels above it.**", "S5"),
            F("This is the conceptual spine for the unit — thyroid, adrenal and gonadal pharmacology all map onto this three-level axis; return to it every time a new gland appears.", "S5 (notes); SG U4-R1"),
            F("The peripheral hormone negatively feeds back on the hypothalamus/pituitary above it — which explains why every exogenous hormone therapy in the unit suppresses the levels above it.", "SG U4-R1"),
        ],
        "prototype": [
            F("Somatropin (GH deficiency); octreotide, lanreotide, pegvisomant (GH excess); cabergoline, bromocriptine (prolactin); desmopressin (DI); tolvaptan, demeclocycline (SIADH).", "S6; S8"),
        ],
        "moa": [
            F("GH axis (Figure 2): pituitary somatotroph releases GH → GH drives liver IGF-1 production → octreotide and lanreotide bind somatostatin receptors and lower GH release.", "S7; S7 (notes)"),
            F("Pegvisomant blocks the GH receptor so IGF-1 falls → acromegaly symptoms improve (monitor IGF-1). GH rises on pegvisomant, so GH is not used to monitor it.", "S7; S7 (notes)"),
            F("Dopamine normally inhibits prolactin release — dopamine agonists restore that inhibitory tone. Hypothalamic dopamine is the brake on lactotrophs; prolactinoma or drugs (antipsychotics, metoclopramide) lift the brake.", "S8; S9; S8 (notes); SG U4-R3"),
            F("Cabergoline or bromocriptine activate D2 receptors → prolactin release falls and the tumor often shrinks → cycles and fertility return; galactorrhea resolves.", "S9; S9 (notes)"),
            F("ADH (Figure 4): ADH binds the V2 receptor in the collecting duct → aquaporin-2 channels insert → water is reabsorbed and urine concentrates.", "S10"),
            F("Desmopressin boosts this (diabetes insipidus); tolvaptan or demeclocycline blunt it (SIADH) → free water retained in DI therapy, excreted in SIADH therapy.", "S10; S10 (notes)"),
        ],
        "indications": [
            F("**●  GH deficiency:** treated with recombinant human growth hormone (somatropin); monitor growth velocity in children and IGF-1 levels in adults.", "S6; S7; S6 (notes); SG U4-R2"),
            F("**●  GH excess (acromegaly):** treated with somatostatin analogs (octreotide, lanreotide — suppress GH release), the GH-receptor antagonist pegvisomant, or dopamine agonists (cabergoline) in select cases.", "S6; SG U4-R2"),
            F("**●  Clinical pearl:** octreotide also has major uses outside the pituitary axis — variceal bleeding and carcinoid syndrome — worth flagging as a cross-system agent.", "S6; S6 (notes)"),
            F("**●  Indication:** octreotide and lanreotide treat acromegaly; octreotide also treats carcinoid syndrome and variceal bleeding.", "S7"),
            F("Hyperprolactinemia: dopamine agonists are first-line — cabergoline, bromocriptine — used for prolactinomas and drug-induced hyperprolactinemia.", "S8"),
            F("Diabetes insipidus (ADH deficiency/resistance): desmopressin (DDAVP) for central DI. SIADH (ADH excess): fluid restriction first-line; vasopressin-receptor antagonists (tolvaptan) or demeclocycline for refractory cases.", "S8; S10; SG U4-R4"),
            F("**●  Somatropin (GH deficiency):** monitor growth velocity or IGF-1.", "S7"),
        ],
        "adverse": [
            F("**●  Adverse effects:** GI upset, gallstones and bradycardia with octreotide and lanreotide (also glucose changes).", "S7; S7 (notes)"),
            F("**●  Limitation:** pegvisomant does not shrink the tumor; monitor IGF-1 and liver tests.", "S7"),
            F("**●  Adverse effects:** nausea, orthostatic hypotension and dizziness (dopamine agonists).", "S9"),
            F("Cabergoline is twice weekly and better tolerated; high doses link to valvulopathy.", "S9 (notes)"),
            F("**●  Caution:** high-dose cabergoline in Parkinson patients is linked to cardiac valve fibrosis; use caution with severe psychiatric disease and avoid unmonitored antipsychotic changes.", "S9; S9 (notes)"),
            F("**●  Desmopressin:** risk is hyponatremia; monitor sodium and limit fluids.", "S10; S10 (notes)"),
            F("**●  Tolvaptan:** can overcorrect sodium (osmotic demyelination) and cause liver injury; start in hospital.", "S10; S10 (notes)"),
            F("**●  SIADH:** first-line is fluid restriction; demeclocycline causes photosensitivity and nephrotoxicity.", "S10"),
        ],
        "contra": [],
        "interactions": [
            F("Antipsychotics and metoclopramide raise prolactin by blocking dopamine.", "S9 (notes); S52"),
        ],
        "pk": [
            F("**●  Dosing:** cabergoline is better tolerated and given twice weekly; bromocriptine is daily.", "S9; S9 (notes)"),
        ],
        "monitoring": [
            F("**●  Monitoring:** pregnancy testing and prolactin monitoring (dopamine agonists). Monitor IGF-1 for acromegaly therapy.", "S9; S7 (notes)"),
        ],
        "pearls": [
            F("DI vs. SIADH is a classic exam pairing — opposite problems; anchor it to \"which way does free water move\" rather than drug names in isolation.", "S8; S8 (notes)"),
            F("Octreotide reappears in GI/variceal contexts — drug classes are not siloed by organ system.", "S6 (notes)"),
        ],
    },
    "figures": [
        {"image": "S5_1.jpg", "title": "Figure 1 · The hypothalamic-pituitary-target gland axis", "src": "S5; S5 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): hypothalamus → anterior pituitary → target gland → peripheral hormone and end-organ effects, with negative feedback to the levels above. Trace the axis and the feedback arrows.",
         "viz": path([N("h", "Hypothalamus\n(TRH, CRH, GnRH)", "signal", 10, 55, 150, "blue"), N("p", "Anterior pituitary\n(TSH, ACTH, LH/FSH)", "signal", 180, 55, 160, "teal"),
                      N("g", "Target gland", "cell", 360, 55, 120, "amber"), N("e", "Hormone,\nend-organ effects", "effect", 500, 55, 130, "sage")],
                     [["h", "p"], ["p", "g"], ["g", "e"]],
                     [Dg("Levothyroxine", "e", "Exogenous hormone feeds back → TSH falls (S12).", less=["p"]),
                      Dg("Chronic prednisone", "e", "Suppresses CRH/ACTH → taper (S22).", less=["h", "p", "g"]),
                      Dg("Combined pill", "e", "Suppresses GnRH/FSH/LH (Session 2).", less=["h", "p"])],
                     "Give a hormone and the levels above it turn down.")},
        {"image": "S7_1.jpg", "title": "Figure 2 · Somatostatin analogs and pegvisomant", "src": "S7; S7 (notes)",
         "caption": "Schematic (illustrative) — Figure 2. Octreotide and lanreotide lower GH release; pegvisomant blocks the GH receptor so IGF-1 falls; acromegaly improves — monitor IGF-1.",
         "viz": path([N("gh", "Somatotroph\nreleases GH", "cell", 10, 55, 140, "teal"), N("rec", "GH receptor\n(liver)", "membrane", 170, 55, 130, "blue"),
                      N("igf", "IGF-1", "molecule", 320, 55, 110, "amber"), N("acro", "Acromegaly\nfeatures", "effect", 450, 55, 150, "coral")],
                     [["gh", "rec"], ["rec", "igf"], ["igf", "acro"]],
                     [Dg("Octreotide / lanreotide", "gh", "Lower GH release; GI upset, gallstones, bradycardia (S7).", less=["gh", "igf", "acro"]),
                      Dg("Pegvisomant", "rec", "Blocks the receptor; GH rises — monitor IGF-1, LFTs (S7).", off=["igf", "acro"])],
                     "Cut the GH or block its receptor.")},
        {"image": "S9_1.jpg", "title": "Figure 3 · Dopamine agonists: restoring the brake on prolactin", "src": "S9; S9 (notes)",
         "caption": "Schematic (illustrative) — Figure 3. Dopamine is the brake on prolactin; prolactinomas or dopamine blockers lift it; cabergoline and bromocriptine (D2 agonists) restore it — prolactin falls, cycles and fertility return.",
         "viz": path([N("da", "Hypothalamic\ndopamine (brake)", "signal", 10, 55, 150, "teal"), N("lac", "Lactotroph\n(D2 receptor)", "cell", 180, 55, 140, "blue"),
                      N("prl", "Prolactin", "molecule", 340, 55, 110, "amber"), N("out", "Galactorrhea,\ninfertility", "effect", 470, 55, 150, "coral")],
                     [["da", "lac"], ["lac", "prl"], ["prl", "out"]],
                     [Dg("Cabergoline", "lac", "Twice weekly, better tolerated (S9).", less=["prl", "out"]),
                      Dg("Antipsychotic / metoclopramide", "da", "Blocks dopamine → prolactin rises (S9; S52).")],
                     "Dopamine is the brake; D2 agonists press it.")},
        {"image": "S10_1.jpg", "title": "Figure 4 · ADH, desmopressin and tolvaptan", "src": "S10; S10 (notes)",
         "caption": "Schematic (illustrative) — Figure 4. ADH → V2 → aquaporin-2 → water reabsorbed. Desmopressin keeps water in (DI; hyponatremia risk); tolvaptan lets it pass out (SIADH; overcorrection risk).",
         "viz": path([N("adh", "ADH binds V2\n(collecting duct)", "membrane", 10, 55, 150, "blue"), N("aqp", "Aquaporin-2\ninserted", "membrane", 180, 55, 140, "teal"),
                      N("w", "Water\nreabsorbed", "effect", 340, 55, 130, "sage"), N("na", "Serum sodium", "molecule", 490, 55, 130, "amber")],
                     [["adh", "aqp"], ["aqp", "w"], ["w", "na"]],
                     [Dg("Desmopressin (central DI)", "adh", "Keeps water, so sodium is diluted — watch hyponatremia (S10).", less=["na"], more=["aqp", "w"]),
                      Dg("Tolvaptan (SIADH)", "adh", "Lets water go, so sodium rises — overcorrection risk; start in hospital (S10).", off=["aqp", "w"], more=["na"])],
                     "Which way does free water move?")},
    ],
    "comparisons": [
        {"title": "Opposite ADH problems (S8; S10)", "columns": ["", "Diabetes insipidus", "SIADH"],
         "rows": [["Problem", "ADH deficiency/resistance — water lost", "ADH excess — water retained"],
                  ["Drug", "Desmopressin (central DI)", "Fluid restriction; tolvaptan or demeclocycline if refractory"],
                  ["Watch for", "Hyponatremia — limit fluids", "Overcorrection (osmotic demyelination); liver injury; photosensitivity"]],
         "src": "S8; S10; SG U4-R4"},
        *tab((30, 31, 32, 33), "GH-axis profiles"),
        *tab((34, 35, 36, 37, 38), "Prolactin and ADH profiles"),
    ],
    "hooks": [
        {"kind": "why", "text": "Why is GH useless for monitoring pegvisomant? The drug blocks the receptor, not the release — GH actually rises; IGF-1 is what falls.", "src": "S7 (notes)"},
    ],
    "high_yield": [
        F("Acromegaly: octreotide/lanreotide or pegvisomant (monitor IGF-1); prolactinoma: cabergoline; DI: desmopressin (hyponatremia); SIADH: fluid restriction, then tolvaptan.", "S6; S8; S10"),
    ],
    "questions": [
        Q("vignette", "A patient with acromegaly starts pegvisomant. Which lab best tracks the response?",
          "IGF-1",
          "Pegvisomant blocks the GH receptor so IGF-1 falls; GH rises and is not used to monitor it (S7).",
          [("Serum GH", "GH rises on pegvisomant (S7)."),
           ("Prolactin", "Not the target (S9)."),
           ("Sodium", "ADH drugs (S10)."),
           ("Cortisol", "Adrenal axis (S22).")], "S7"),
        Q("mechanism", "How does cabergoline treat a prolactinoma?",
          "D2 agonism restores dopamine’s brake",
          "Dopamine normally inhibits prolactin; D2 agonists restore that tone and often shrink the tumor (S8–S9; SG U4-R3).",
          [("Blocks dopamine D2 receptors", "That raises prolactin (S9)."),
           ("Blocks somatostatin receptors", "Not the mechanism (S7)."),
           ("Blocks the prolactin receptor", "Not the mechanism (S9)."),
           ("Inhibits thyroid hormone release", "Not related (S16).")], "S8; S9; SG U4-R3"),
        Q("mechanism", "How do octreotide and lanreotide treat acromegaly?",
          "They lower GH release",
          "Somatostatin analogs bind somatostatin receptors and suppress GH release (S6–S7).",
          [("They block the GH receptor", "That is pegvisomant (S7)."),
           ("They activate D2 receptors", "Dopamine agonists (S9)."),
           ("They block IGF-1 receptors", "Not the mechanism (S7)."),
           ("They replace missing GH", "That is somatropin (S6).")], "S6; S7; SG U4-R2"),
        Q("vignette", "A patient with central diabetes insipidus starts desmopressin. What is the main safety counseling?",
          "Limit fluids (hyponatremia)",
          "Desmopressin keeps free water; risk is hyponatremia — monitor sodium and limit fluids (S10).",
          [("Drink extra water all day", "Raises hyponatremia risk (S10)."),
           ("Watch for hypernatremia", "Opposite direction (S10)."),
           ("Check liver tests monthly", "Tolvaptan (S10)."),
           ("Avoid sun exposure", "Demeclocycline (S10).")], "S8; S10; SG U4-R4"),
        Q("vignette", "A patient with SIADH stays hyponatremic despite fluid restriction. Tolvaptan is planned. Why start it in hospital?",
          "Risk of sodium overcorrection",
          "Tolvaptan can overcorrect sodium (osmotic demyelination) and injure the liver; start in hospital (S10).",
          [("It causes severe hypoglycemia", "Not tolvaptan (S10)."),
           ("It causes hyperkalemia", "Not the taught risk (S10)."),
           ("It must be given IV only", "Oral drug (S37)."),
           ("It causes bradycardia", "Octreotide (S7).")], "S8; S10"),
    ],
}

# ---------------------------------------------------------------- Part 2: thyroid
t2 = {
    "name": "Thyroid & Antithyroid Drugs", "template": "drug_class", "objectives": ["SO3", "SO5", "IO4.1", "IO4.2", "IO4.3", "IO4.4", "IO4.5", "IO4.6"],
    "sections": {
        "overview": [
            F("**Replacing a deficient gland, or slowing down an overactive one.**", "S11"),
            F("**Figure 6. Original illustrative diagram (not from Katzung): iodide trapping, organification, and coupling produce T3/T4, which undergo peripheral T4-to-T3 conversion; methimazole and PTU block organification and coupling, while PTU additionally blocks peripheral conversion.**", "S14"),
            F("Figure 6 is the key to the next slides: PTU, not methimazole, is preferred in thyroid storm because it blocks an extra step.", "S14 (notes)"),
        ],
        "prototype": [
            F("Levothyroxine (replacement); methimazole, propylthiouracil (thionamides); propranolol; potassium iodide.", "S12; S15; S16"),
        ],
        "moa": [
            F("**Mechanism: synthetic T4, converted peripherally to active T3.**", "S12"),
            F("Levothyroxine path (Figure 5): tablet taken on an empty stomach → absorbed in the small intestine; calcium, iron and antacid binders block it.", "S13"),
            F("T4 converted to active T3 in tissues → T3 binds nuclear receptors and restores metabolism → TSH falls to the target range (recheck at 6–8 weeks).", "S13"),
            F("Methimazole and PTU block organification and coupling; PTU also blocks peripheral T4→T3 conversion — a faster symptomatic effect in crisis.", "S14; S15"),
            F("Storm targets (Figure 7): Graves thyroid makes excess hormone — PTU blocks synthesis; hormone is released — iodine (after PTU) blocks release.", "S17"),
            F("T4 converts to T3 in tissues — PTU, propranolol and steroids block conversion; T3 stimulates beta receptors — propranolol blunts tachycardia and tremor; crisis settles with fluids, cooling and support.", "S17; S17 (notes)"),
        ],
        "indications": [
            F("Levothyroxine: first-line for hypothyroidism; narrow therapeutic index — dose titrated using TSH (primary hypothyroidism) with repeat labs every 6–8 weeks after a dose change.", "S12; S12 (notes)"),
            F("About 1.6 mcg/kg/day is full replacement; estrogen raises needs. **●  Pregnancy:** often raises dose needs; monitor TSH closely.", "S12 (notes); S13"),
            F("Methimazole: first-line for most non-pregnant patients — once-daily dosing, more convenient; avoid in the first trimester of pregnancy (teratogenic risk).", "S15; S15 (notes)"),
            F("PTU: preferred in the first trimester of pregnancy and in thyroid storm. PTU first trimester (lower teratogenic risk) and thyroid storm (also blocks peripheral T4→T3 conversion).", "S15; SG U4-R6"),
            F("**A life-threatening hyperthyroid crisis requiring rapid, multi-pronged therapy.** Thyroid storm is treated with four drugs that hit four targets.", "S16; S16 (notes)"),
            F("Beta-blockers (propranolol) — control adrenergic symptoms (tachycardia, tremor) and blunt peripheral T4-to-T3 conversion. PTU (preferred over methimazole) — blocks new hormone synthesis and peripheral conversion.", "S16"),
            F("Iodine solution (given after PTU/methimazole) — acutely blocks hormone release; must follow the antithyroid drug to avoid providing substrate for new synthesis. Corticosteroids — blunt peripheral conversion and treat relative adrenal insufficiency.", "S16"),
        ],
        "adverse": [
            F("Methimazole boxed warning: agranulocytosis, hepatotoxicity. PTU boxed warning: severe hepatotoxicity (more than methimazole) — reserve for specific indications.", "S15; S17"),
            F("Both thionamides carry agranulocytosis and liver warnings; PTU has the greater liver risk. Fever or sore throat on a thionamide means stop and check a CBC.", "S15 (notes)"),
            F("**●  Over-replacement:** tachycardia, atrial fibrillation and bone loss.", "S13; S12 (notes)"),
        ],
        "contra": [
            F("**Older adults and patients with cardiac disease: start at lower doses and titrate slowly to avoid precipitating angina/arrhythmia.**", "S12; S13; S12 (notes)"),
            F("**●  Propranolol:** avoided in decompensated heart failure and asthma.", "S17"),
        ],
        "interactions": [
            F("**Significant absorption interactions: calcium, iron, and antacids can all reduce absorption — separate dosing by at least 4 hours.**", "S12; SG U4-R5"),
            F("**●  Timing:** separate from calcium, iron, antacids, PPIs and bile acid binders by 4 hours.", "S13"),
            F("Amiodarone and lithium can cause hypo- or hyperthyroidism. Estrogens raise thyroid-binding globulin, so levothyroxine needs rise. Rifampin, phenytoin, carbamazepine speed clearance of levothyroxine and steroids.", "S52; S52 (notes)"),
            F("**●  Steroids:** also treat relative adrenal insufficiency; avoid aspirin in thyroid storm (it frees bound hormone).", "S17"),
        ],
        "pk": [
            F("Take on an empty stomach, 30–60 minutes before breakfast, consistently relative to other medications and food.", "S12; S13 (notes)"),
        ],
        "monitoring": [
            F("**●  Start low:** in older adults and in cardiac disease. Check TSH at 6–8 weeks.", "S13; S12 (notes)"),
        ],
        "pearls": [
            F("The absorption-interaction list is extremely high-yield — many patients also take calcium or iron, so timing counseling matters as much as the drug itself.", "S12 (notes)"),
            F("The pregnancy-trimester switch (PTU in first trimester, methimazole after) is a frequently tested nuance — worth stating explicitly rather than assuming one drug is simply \"better.\"", "S15 (notes)"),
            F("**●  Sequence:** start PTU and beta-blocker first; give iodine at least an hour later. **●  PTU:** boxed warning for hepatotoxicity.", "S17"),
            F("Case: fever, tachycardia, and altered mental status in untreated Graves disease. **What is the correct sequence of pharmacologic therapy, and why does the order matter?**", "S18"),
            F("**Beta-blockade and PTU are started first; iodine solution is given only after PTU, since giving iodine first would supply additional substrate for thyroid hormone synthesis before the gland’s synthetic machinery is blocked — potentially worsening the crisis.**", "S18; S16 (notes); SG U4-R7"),
            F("Iodine-first sequencing is the classic high-yield detail: giving iodine first can worsen the crisis by supplying substrate before synthesis is blocked.", "S16 (notes); S18 (notes)"),
        ],
    },
    "figures": [
        {"image": "S13_1.jpg", "title": "Figure 5 · Levothyroxine: absorption, conversion and timing", "src": "S13; S13 (notes)",
         "caption": "**Schematic (illustrative)** — Figure 5. Red X marks absorption blocked by calcium, iron or antacids. Blue steps show T4 to T3 conversion and receptor action. Red outcome: TSH falls to target.",
         "viz": path([N("tab", "Tablet, empty\nstomach", "molecule", 10, 55, 130, "teal"), N("abs", "Small-bowel\nabsorption", "membrane", 160, 55, 130, "blue"),
                      N("t3", "T4 → T3\nin tissues", "enzyme", 310, 55, 120, "amber"), N("tsh", "TSH falls\nto target", "effect", 450, 55, 150, "sage")],
                     [["tab", "abs"], ["abs", "t3"], ["t3", "tsh"]],
                     [Dg("Calcium / iron / antacid", "abs", "Binds the dose — separate by 4 hours (S12–S13).", off=["t3", "tsh"]),
                      Dg("Levothyroxine", "tab", "30–60 min before breakfast; TSH at 6–8 weeks (S12–S13).")],
                     "Timing decides whether the dose gets in.")},
        {"image": "S14_1.jpg", "title": "Figure 6 · Thyroid hormone synthesis: where antithyroid drugs act", "src": "S14; S14 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): iodide trapping → organification → coupling → T3/T4 release → peripheral T4-to-T3 conversion. Methimazole and PTU block organification and coupling; PTU also blocks conversion.",
         "viz": path([N("trap", "Iodide\ntrapping", "membrane", 10, 55, 110, "teal"), N("org", "Organification,\ncoupling", "enzyme", 140, 55, 140, "blue"),
                      N("rel", "T4/T3\nrelease", "molecule", 300, 55, 110, "amber"), N("conv", "T4 → T3\n(peripheral)", "enzyme", 430, 55, 130, "coral")],
                     [["trap", "org"], ["org", "rel"], ["rel", "conv"]],
                     [Dg("Methimazole", "org", "First line, once daily (S15).", off=["rel"]),
                      Dg("PTU", "org", "Also blocks conversion — storm, first trimester (S14–S15).", off=["rel", "conv"]),
                      Dg("Iodine (after PTU)", "rel", "Blocks release (S16).", off=["rel", "conv"])],
                     "PTU blocks one extra step.")},
        {"image": "S17_1.jpg", "title": "Figure 7 · Thyroid storm: four drugs, four targets", "src": "S17; S17 (notes)",
         "caption": "Schematic (illustrative) — Figure 7. Red bars mark where PTU (synthesis), iodine (release, after PTU), propranolol and steroids (conversion, symptoms) act.",
         "viz": path([N("syn", "Synthesis", "enzyme", 10, 55, 110, "teal"), N("rel", "Release", "molecule", 140, 55, 110, "blue"),
                      N("conv", "T4 → T3", "enzyme", 270, 55, 110, "amber"), N("beta", "Beta-receptor\neffects", "effect", 400, 55, 150, "coral")],
                     [["syn", "rel"], ["rel", "conv"], ["conv", "beta"]],
                     [Dg("PTU (first)", "syn", "Blocks synthesis and conversion (S16–S17).", off=["rel"]),
                      Dg("Iodine (≥1 h after PTU)", "rel", "Blocks release (S16–S17).", off=["rel", "conv"]),
                      Dg("Propranolol", "beta", "Rate, tremor; also less conversion; avoid in asthma (S17).", less=["beta"]),
                      Dg("Hydrocortisone", "conv", "Blunts conversion; covers adrenal insufficiency (S16–S17).", less=["conv"])],
                     "Four drugs, four targets — in order.")},
    ],
    "comparisons": [
        {"title": "Methimazole vs. propylthiouracil (S15)", "columns": ["", "Methimazole", "Propylthiouracil (PTU)"],
         "rows": [["Use", "First-line for most non-pregnant patients; once daily", "First trimester of pregnancy; thyroid storm"],
                  ["Extra action", "—", "Also blocks peripheral T4→T3 conversion"],
                  ["Pregnancy", "Avoid in first trimester (teratogenic)", "Preferred in first trimester"],
                  ["Boxed warning", "Agranulocytosis, hepatotoxicity", "Severe hepatotoxicity (more than methimazole)"]],
         "src": "S15; SG U4-R6"},
        *tab((39, 40, 41, 42, 43), "Thyroid drug profiles"),
    ],
    "hooks": [
        {"kind": "mnemonic", "text": "Storm order: Block (beta-blocker), then Block synthesis (PTU), then Block release (iodine) — iodine never first.", "src": "S16; S18"},
    ],
    "high_yield": [
        F("Levothyroxine: empty stomach, separate calcium/iron/antacids by 4 h, TSH at 6–8 weeks, start low in older/cardiac patients.", "S12; S13; SG U4-R5"),
        F("PTU for storm and first trimester; methimazole otherwise; fever/sore throat → stop, CBC.", "S15; SG U4-R6"),
    ],
    "questions": [
        Q("vignette", "A patient with untreated Graves disease presents with fever, tachycardia and confusion. What is the correct order of therapy?",
          "Beta-blocker and PTU first, iodine after",
          "Iodine is given only after PTU; giving it first supplies substrate for new hormone synthesis (S18).",
          [("Iodine first, then PTU", "Worsens the crisis (S18)."),
           ("Methimazole alone, no beta-blocker", "Propranolol controls symptoms (S16)."),
           ("Levothyroxine to reset feedback", "Wrong direction (S12)."),
           ("Aspirin for the fever first", "Frees bound hormone (S17).")], "S16; S18; SG U4-R7", from_slides="S18"),
        Q("vignette", "A woman taking levothyroxine with her calcium and iron each morning has a high TSH. Best advice?",
          "Separate them by at least 4 hours",
          "Calcium, iron and antacids reduce absorption — separate by at least 4 hours; take it 30–60 minutes before breakfast (S12–S13).",
          [("Double the levothyroxine dose", "Fix the timing first (S12)."),
           ("Take it with breakfast instead", "Empty stomach (S12)."),
           ("Switch to methimazole", "Antithyroid drug (S15)."),
           ("Stop calcium permanently", "Separation is enough (S13).")], "S12; S13; SG U4-R5"),
        Q("vignette", "A woman in her first trimester has hyperthyroidism. Which drug is preferred?",
          "Propylthiouracil",
          "PTU is preferred in the first trimester; methimazole is avoided then (teratogenic) (S15).",
          [("Methimazole", "Avoid in first trimester (S15)."),
           ("Radioactive iodine", "Contraindicated in pregnancy (p. 732)."),
           ("Potassium iodide alone", "Escape and fetal goiter risk (p. 732)."),
           ("Levothyroxine", "For hypothyroidism (S12).")], "S15; SG U4-R6"),
        Q("vignette", "Six weeks into methimazole, a patient has fever and a sore throat. What should happen?",
          "Stop it and check a CBC",
          "Thionamides carry an agranulocytosis warning; fever or sore throat → stop and check a CBC (S15).",
          [("Continue and add an antibiotic", "Check for agranulocytosis first (S15)."),
           ("Switch to PTU immediately", "Check the CBC first (S15)."),
           ("Double the dose", "Not the answer (S15)."),
           ("Reassure: a common cold", "Not reassurance (S15).")], "S15"),
        Q("mechanism", "Why is PTU preferred over methimazole in thyroid storm?",
          "It also blocks T4→T3 conversion",
          "PTU blocks synthesis and conversion, a faster effect on active hormone (S14–S15).",
          [("It is better absorbed orally", "Not the reason (S15)."),
           ("It has no liver toxicity", "Greater liver risk (S15)."),
           ("It blocks iodide trapping faster", "Not the reason (S14)."),
           ("It is a beta-blocker", "Propranolol (S16).")], "S14; S15"),
        Q("mechanism", "What is levothyroxine, and how does it act?",
          "Synthetic T4, converted to T3",
          "Levothyroxine is synthetic T4, converted peripherally to active T3, which binds nuclear receptors (S12–S13).",
          [("Synthetic T3 acting directly", "That is liothyronine (S12)."),
           ("A TSH-receptor agonist drug", "Not the mechanism (S12)."),
           ("A TRH analog acting centrally", "Not the mechanism (S12)."),
           ("An iodide supplement for synthesis", "Not the mechanism (S12).")], "S12; S13"),
        Q("vignette", "An 80-year-old with coronary disease is newly hypothyroid. How should levothyroxine be started?",
          "Low dose, titrated slowly",
          "Older adults and cardiac patients start low and titrate slowly to avoid angina or arrhythmia (S12).",
          [("Full 1.6 mcg/kg/day at once", "Risks angina (S12)."),
           ("A loading dose then full dose", "Not the approach (S12)."),
           ("Liothyronine (T3) at a high dose", "Not taught (S12)."),
           ("No treatment until TSH > 20", "Not the approach (S12).")], "S12; S13"),
    ],
}

# ---------------------------------------------------------------- Part 3: adrenal
t3 = {
    "name": "Adrenocorticosteroids & Antagonists", "template": "drug_class", "objectives": ["SO4", "SO5", "IO4.1", "IO4.2", "IO4.3", "IO4.4", "IO4.5", "IO4.6"],
    "sections": {
        "overview": [
            F("**Glucocorticoid power and mineralocorticoid balance — and what happens when therapy stops.**", "S19"),
            F("**Figure 9. Original illustrative diagram (not from Katzung): chronic exogenous glucocorticoid use suppresses CRH and ACTH via negative feedback, reducing endogenous cortisol production — abrupt withdrawal can precipitate adrenal insufficiency.**", "S22"),
            F("This is the single most clinically important concept in the glucocorticoid section — it explains why tapering (not stopping) is the standard of care.", "S22 (notes)"),
        ],
        "prototype": [
            F("Prednisone, dexamethasone, hydrocortisone (glucocorticoids); fludrocortisone (mineralocorticoid); ketoconazole, metyrapone, mifepristone, spironolactone (antagonists).", "S20; S23"),
        ],
        "moa": [
            F("Glucocorticoids (e.g., prednisone, dexamethasone): anti-inflammatory and immunosuppressive effects, with a spectrum of relative potency and mineralocorticoid activity across agents.", "S20"),
            F("Signaling (Figure 8): prednisone or cortisol crosses the cell membrane → binds the cytoplasmic glucocorticoid receptor → the complex moves into the nucleus → switches on anti-inflammatory genes and represses NF-kB cytokines → fewer inflammatory cells and mediators.", "S21; S21 (notes)"),
            F("Mineralocorticoids (fludrocortisone): promote renal sodium retention and potassium excretion.", "S20"),
            F("Synthesis chain (Figure 10): cholesterol enters the adrenal cortex → CYP enzymes convert it to cortisol and aldosterone → ketoconazole blocks several enzymes; metyrapone blocks the last cortisol step (11-beta-hydroxylase).", "S24"),
            F("Then cortisol or aldosterone binds its receptor → mifepristone blocks the glucocorticoid receptor; spironolactone blocks the mineralocorticoid receptor. Receptor blockers leave hormone levels high.", "S24; S24 (notes)"),
        ],
        "indications": [
            F("Glucocorticoids are used across nearly every organ system for inflammatory/autoimmune disease.", "S20"),
            F("Fludrocortisone: replacement therapy in primary adrenal insufficiency (Addison disease), alongside a glucocorticoid — primary adrenal insufficiency needs BOTH hormone classes replaced, not just cortisol.", "S20; S20 (notes)"),
            F("**●  Ketoconazole:** inhibits multiple steps in steroidogenesis (CYP enzymes); used for Cushing syndrome; significant drug-interaction and hepatotoxicity concerns.", "S23; SG U4-R9"),
            F("**●  Metyrapone:** blocks the final step of cortisol synthesis (11-β-hydroxylase); used diagnostically and for Cushing syndrome.", "S23; SG U4-R9"),
            F("**●  Mifepristone:** a glucocorticoid-receptor antagonist; used for hyperglycemia associated with Cushing syndrome when surgery is not an option (distinct from its progesterone-receptor antagonist use in pregnancy termination).", "S23; S23 (notes); SG U4-R9"),
            F("**●  Spironolactone:** a mineralocorticoid-receptor antagonist; used for hyperaldosteronism and as a potassium-sparing diuretic — ties back to the diuretic pharmacology concepts from earlier coursework.", "S23; SG U4-R9"),
        ],
        "adverse": [
            F("**●  Adverse effects:** hyperglycemia, osteoporosis, infection, mood change, cataracts, adrenal suppression.", "S21; S20 (notes)"),
            F("**●  Ketoconazole:** hepatotoxicity, QT prolongation, strong CYP3A4 inhibition.", "S24; S23 (notes)"),
            F("**●  Metyrapone:** raises androgens and deoxycorticosterone (hirsutism, hypertension).", "S24; S23 (notes)"),
            F("**●  Mifepristone:** contraindicated in pregnancy; causes hypokalemia; cortisol levels rise, so monitor clinically. **●  Spironolactone:** hyperkalemia and gynecomastia.", "S24; S24 (notes)"),
        ],
        "contra": [],
        "interactions": [
            F("Azole antifungals raise corticosteroid exposure through CYP3A4. ACE inhibitors, ARBs and potassium add to spironolactone hyperkalemia. Insulin and oral agents need adjusting during steroid therapy.", "S52; S52 (notes)"),
        ],
        "pk": [
            F("**●  Potency vs. hydrocortisone:** prednisone about 4x, dexamethasone about 25-30x. **●  Mineralocorticoid action:** fludrocortisone has it; hydrocortisone has both.", "S21; S20 (notes)"),
            F("**●  Dosing:** take in the morning with food; consider bone and GI protection.", "S21"),
        ],
        "monitoring": [
            F("Fludrocortisone: monitor blood pressure and potassium.", "S20"),
            F("Chronic steroids suppress CRH and ACTH — abrupt withdrawal risks adrenal crisis; taper. Chronic suppression leaves the axis unable to resume adequate cortisol quickly — taper, don’t stop abruptly.", "S22 (notes); SG U4-R8"),
        ],
        "pearls": [
            F("Case: chronic high-dose prednisone for a rheumatologic condition, stopped abruptly after running out of refills; now hypotension, weakness, nausea, confusion. **What is the most likely cause of this presentation, and how should it be managed?**", "S27"),
            F("**This presentation is consistent with acute adrenal insufficiency (adrenal crisis) from abrupt glucocorticoid withdrawal after HPA-axis suppression.**", "S27"),
            F("**Management requires immediate IV hydrocortisone (which has both glucocorticoid and mineralocorticoid activity) and IV fluids — this is a medical emergency, not a routine medication-refill issue.**", "S27; S27 (notes)"),
            F("The fix for a missed refill here is not \"just restart the pill\" — it is emergent IV steroid replacement; tapering protects against it.", "S27 (notes)"),
            F("Mifepristone’s dual identity (glucocorticoid-receptor antagonist here vs. progesterone-receptor antagonist elsewhere) is worth flagging explicitly — don’t conflate the two uses or assume a single mechanism.", "S23 (notes)"),
            F("Drug names reveal the class: **-tide** somatostatin analog (octreotide, lanreotide; lowers GH release); **-pressin** vasopressin analog (desmopressin; central diabetes insipidus); **-vaptan** V2 antagonist (tolvaptan; SIADH).", "S26; S26 (notes)"),
            F("**-ergoline** dopamine agonist, ergot-derived (cabergoline; lowers prolactin); **-thyroxine** thyroid hormone (levothyroxine; replacement, titrate to TSH); **-imazole / -thiouracil** thionamide antithyroid (methimazole, propylthiouracil; blocks hormone synthesis).", "S26"),
            F("**-sone / -solone** corticosteroid (prednisone, dexamethasone; anti-inflammatory, taper); **-conazole** azole steroidogenesis inhibitor (ketoconazole; Cushing syndrome); **-pristone** receptor antagonist (mifepristone; glucocorticoid-receptor block); **-lactone** mineralocorticoid antagonist (spironolactone; hyperkalemia risk).", "S26"),
            F("**A stem is a memory aid, not a rule: where no shared stem exists, learn the class name instead.**", "S26"),
            F("Recap: **1.** The hypothalamic-pituitary-target gland axis (Figure 1) is a shared regulatory template across thyroid, adrenal, and gonadal systems — drug therapy can intervene at any level.", "S28"),
            F("**2.** Thyroid hormone synthesis has distinct, drug-targetable steps (Figure 6); PTU uniquely blocks peripheral T4-to-T3 conversion, making it preferred in thyroid storm and first-trimester pregnancy.", "S28"),
            F("**3.** Chronic exogenous glucocorticoid use suppresses the HPA axis (Figure 9) — abrupt withdrawal risks adrenal crisis, so chronic therapy is tapered, not stopped.", "S28"),
            F("**4.** Adrenocortical antagonists (ketoconazole, metyrapone, mifepristone, spironolactone) block cortisol or aldosterone synthesis/action at different points for Cushing syndrome and hyperaldosteronism. **5.** Session 2 (Thursday, November 12) continues with gonadal hormones, diabetes, and parathyroid disorders.", "S28; S28 (notes)"),
        ],
    },
    "figures": [
        {"image": "S21_1.jpg", "title": "Figure 8 · Glucocorticoid receptor signaling", "src": "S21; S21 (notes)",
         "caption": "**Schematic (illustrative)** — Figure 8. A steroid enters the cell, binds its cytoplasmic receptor, and the complex switches genes on and off in the nucleus; NF-kB-driven cytokines are repressed.",
         "viz": path([N("st", "Steroid enters\nthe cell", "molecule", 10, 55, 130, "teal"), N("gr", "Cytoplasmic\nGR binds", "membrane", 160, 55, 130, "blue"),
                      N("nuc", "Nucleus: genes\non/off, NF-kB ↓", "signal", 310, 55, 160, "amber"), N("out", "Less\ninflammation", "effect", 490, 55, 130, "sage")],
                     [["st", "gr"], ["gr", "nuc"], ["nuc", "out"]],
                     [Dg("Prednisone (~4×)", "st", "Morning with food; bone and GI protection (S21)."),
                      Dg("Dexamethasone (~25–30×)", "st", "Long-acting (S21)."),
                      Dg("Mifepristone", "gr", "Blocks the receptor; cortisol rises (S24).", off=["nuc", "out"])],
                     "Receptor → nucleus → fewer cytokines.")},
        {"image": "S22_1.jpg", "title": "Figure 9 · Exogenous corticosteroids and HPA suppression", "src": "S22; S22 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): chronic exogenous glucocorticoid suppresses CRH and ACTH via negative feedback; endogenous cortisol falls; abrupt withdrawal → adrenal insufficiency. Taper.",
         "viz": path([N("crh", "Hypothalamus:\nCRH", "signal", 10, 55, 130, "blue"), N("acth", "Pituitary:\nACTH", "signal", 160, 55, 130, "teal"),
                      N("adr", "Adrenal\ncortisol", "cell", 310, 55, 130, "amber"), N("crisis", "Stop abruptly →\nadrenal crisis", "effect", 460, 55, 160, "coral")],
                     [["crh", "acth"], ["acth", "adr"], ["adr", "crisis"]],
                     [Dg("Chronic prednisone", "crh", "Feedback suppresses CRH/ACTH (S22).", less=["crh", "acth", "adr"]),
                      Dg("Slow taper", "adr", "Gives the axis time to recover (S22; S28).")],
                     "Suppressed axes need time — taper.")},
        {"image": "S24_1.jpg", "title": "Figure 10 · Blocking steroid synthesis vs. blocking the receptor", "src": "S24; S24 (notes)",
         "caption": "Schematic (illustrative) — Figure 10. Left: enzyme blocks on the cortisol pathway (ketoconazole, metyrapone). Right: receptor blocks (mifepristone at the glucocorticoid receptor, spironolactone at the mineralocorticoid receptor).",
         "viz": path([N("ch", "Cholesterol", "molecule", 10, 95, 120, "teal"), N("cyp", "CYP enzymes\n(11β-hydroxylase)", "enzyme", 150, 95, 150, "blue"),
                      N("cort", "Cortisol", "molecule", 330, 20, 120, "amber"), N("ald", "Aldosterone", "molecule", 330, 170, 120, "amber"),
                      N("gr", "GR", "membrane", 490, 20, 110, "coral"), N("mr", "MR", "membrane", 490, 170, 110, "deep")],
                     [["ch", "cyp"], ["cyp", "cort"], ["cyp", "ald"], ["cort", "gr"], ["ald", "mr"]],
                     [Dg("Ketoconazole", "cyp", "Several enzymes; liver, QT, CYP3A4 (S23–S24).", off=["cort", "ald"]),
                      Dg("Metyrapone", "cyp", "Last cortisol step (S23–S24).", off=["cort"]),
                      Dg("Mifepristone", "gr", "Receptor block; cortisol stays high (S24).", off=["gr"]),
                      Dg("Spironolactone", "mr", "Hyperkalemia (S24).", off=["mr"])],
                     "Block the factory or block the lock.", h=250)},
    ],
    "comparisons": [
        {"title": "Glucocorticoids vs. mineralocorticoids (S20)", "columns": ["", "Glucocorticoids (prednisone, dexamethasone)", "Mineralocorticoids (fludrocortisone)"],
         "rows": [["Main effect", "Anti-inflammatory, immunosuppressive", "Renal sodium retention, potassium excretion"],
                  ["Use", "Inflammatory/autoimmune disease in nearly every organ system", "Addison disease replacement, with a glucocorticoid"],
                  ["Monitor", "Glucose, bone, infection, mood; taper chronic use", "Blood pressure and potassium"]],
         "src": "S20"},
        {"title": "Table 1 · Adrenal pharmacology at a glance", "columns": ["Agent", "Category", "Key teaching point"],
         "rows": [["Prednisone, dexamethasone", "Glucocorticoid", "Anti-inflammatory; chronic use risks HPA suppression — taper, don’t stop abruptly"],
                  ["Fludrocortisone", "Mineralocorticoid", "Sodium retention/potassium excretion; replacement in Addison disease"],
                  ["Ketoconazole, metyrapone", "Steroidogenesis inhibitor", "Block cortisol synthesis at different steps; used in Cushing syndrome"],
                  ["Mifepristone", "Glucocorticoid-receptor antagonist", "Hyperglycemia in Cushing syndrome when surgery isn’t an option"]],
         "src": "S25; S25 (notes)"},
        {"title": "Supporting drugs at a glance (S52)", "columns": ["Drug(s)", "Why it matters here"],
         "rows": [["**Antipsychotics and metoclopramide**", "Raise prolactin by blocking dopamine"],
                  ["**Calcium, iron and antacids**", "Block levothyroxine absorption; separate by 4 hours"],
                  ["**Amiodarone and lithium**", "Can cause hypo- or hyperthyroidism"],
                  ["**Estrogens**", "Raise thyroid-binding globulin, so levothyroxine needs rise"],
                  ["**Rifampin, phenytoin, carbamazepine**", "Speed clearance of levothyroxine and steroids"],
                  ["**Azole antifungals**", "Raise corticosteroid exposure through CYP3A4"],
                  ["**ACE inhibitors, ARBs and potassium**", "Add to spironolactone hyperkalemia"],
                  ["**Insulin and oral agents**", "Doses need adjusting during steroid therapy"]],
         "src": "S52; S52 (notes)"},
        *tab((44, 45, 46, 47), "Corticosteroid profiles"),
        *tab((48, 49, 50, 51), "Adrenal antagonist profiles"),
    ],
    "hooks": [
        {"kind": "why", "text": "Why IV hydrocortisone in adrenal crisis, not just prednisone? Hydrocortisone replaces both glucocorticoid and mineralocorticoid action — and the patient is in shock.", "src": "S21; S27"},
    ],
    "high_yield": [
        F("Chronic steroids suppress CRH/ACTH → taper; abrupt stop → adrenal crisis → IV hydrocortisone + fluids.", "S22; S27; SG U4-R8"),
        F("Addison disease needs a glucocorticoid plus fludrocortisone.", "S20"),
    ],
    "questions": [
        Q("vignette", "A patient on chronic high-dose prednisone ran out of refills and now has hypotension, weakness and confusion. Best management?",
          "IV hydrocortisone and IV fluids now",
          "Adrenal crisis from abrupt withdrawal after HPA suppression — emergent IV hydrocortisone and fluids (S27).",
          [("Restart oral prednisone at home", "This is an emergency (S27)."),
           ("Give fludrocortisone alone", "Needs glucocorticoid too (S27)."),
           ("Give IV dexamethasone only, no fluids", "Fluids and hydrocortisone (S27)."),
           ("Observe; symptoms will pass", "Life-threatening (S27).")], "S22; S27; SG U4-R8", from_slides="S27"),
        Q("mechanism", "Why must chronic glucocorticoid therapy be tapered rather than stopped?",
          "The suppressed HPA axis needs time to recover",
          "Exogenous steroid suppresses CRH and ACTH; abrupt withdrawal leaves too little endogenous cortisol (S22; SG U4-R8).",
          [("To prevent rebound inflammation only", "Not the main reason (S22)."),
           ("Because the adrenal gland is destroyed", "Suppressed, not destroyed (S22)."),
           ("To prevent hyperkalemia", "Not the reason (S22)."),
           ("Because steroids cause dependence", "Not the mechanism (S22).")], "S22; SG U4-R8"),
        Q("vignette", "A patient with primary adrenal insufficiency is on hydrocortisone but has low BP and high potassium. What should be added?",
          "Fludrocortisone",
          "Addison disease needs mineralocorticoid replacement alongside a glucocorticoid (S20).",
          [("Spironolactone", "Blocks mineralocorticoid action (S23)."),
           ("Dexamethasone", "Little mineralocorticoid action (S21)."),
           ("Ketoconazole", "Blocks steroid synthesis (S23)."),
           ("Potassium supplement", "Wrong direction (S20).")], "S20; S47"),
        Q("mechanism", "What does fludrocortisone do at the kidney?",
          "Retains sodium, excretes potassium",
          "Mineralocorticoids promote renal sodium retention and potassium excretion; monitor BP and potassium (S20).",
          [("Excretes sodium, retains potassium", "Reversed (S20)."),
           ("Blocks the mineralocorticoid receptor", "That is spironolactone (S23)."),
           ("Suppresses inflammation only", "Glucocorticoid action (S20)."),
           ("Blocks ADH at V2 receptors", "That is tolvaptan (S10).")], "S20"),
        Q("mechanism", "How do chronic exogenous glucocorticoids cause adrenal insufficiency on abrupt withdrawal?",
          "Feedback suppresses CRH and ACTH",
          "Chronic steroid suppresses CRH/ACTH via negative feedback, so endogenous cortisol cannot resume quickly (S22; S28).",
          [("They destroy the adrenal cortex", "Suppression, not destruction (S22)."),
           ("They block cortisol synthesis enzymes", "That is metyrapone (S23)."),
           ("They raise ACTH until it is exhausted", "ACTH falls (S22)."),
           ("They block the glucocorticoid receptor", "That is mifepristone (S23).")], "S22; S28"),
        Q("mechanism", "Which drug lowers cortisol by blocking 11-β-hydroxylase?",
          "Metyrapone",
          "Metyrapone blocks the final step of cortisol synthesis (S23–S24).",
          [("Mifepristone", "Blocks the receptor (S23)."),
           ("Spironolactone", "Blocks the mineralocorticoid receptor (S23)."),
           ("Fludrocortisone", "Mineralocorticoid agonist (S20)."),
           ("Octreotide", "Somatostatin analog (S7).")], "S23; S24; SG U4-R9"),
        Q("vignette", "A patient with Cushing syndrome on mifepristone has persistently high cortisol levels. What explains this?",
          "Receptor blockade leaves cortisol high",
          "Mifepristone blocks the glucocorticoid receptor, so cortisol levels rise — monitor clinically (S24).",
          [("The drug has failed", "Expected effect (S24)."),
           ("It blocks 11-β-hydroxylase", "Metyrapone (S23)."),
           ("It increases ACTH secretion by itself", "Not the taught mechanism (S24)."),
           ("Lab interference from ketoconazole", "Not the reason (S24).")], "S24"),
    ],
}

content = {
    "lecture": {"id": "L07", "title": "Endocrine Pharmacotherapy — Session 1", "date": "Tue, Nov 10, 2026"},
    "textbook_status": "included",
    "objectives": objectives,
    "about": about,
    "classes": [t1, t2, t3],
    "notebooklm": {
        "patient": "a patient with untreated Graves disease in thyroid storm, and a patient who abruptly stopped chronic high-dose prednisone (the lecture’s cases)",
        "suggested_questions": [
            "Trace the hypothalamic-pituitary-target gland axis and its feedback.",
            "Compare desmopressin and tolvaptan: which way does water move?",
            "How should levothyroxine be taken and monitored?",
            "Methimazole vs. PTU: when is each used?",
            "Walk through thyroid storm treatment and why iodine comes last.",
            "Why taper steroids, and how is adrenal crisis treated?",
        ],
    },
    "audit_skip": [
        {"ref": "S1", "starts_with": "Diane", "reason": "instructor name (no names on the site)"},
        {"ref": "S2", "starts_with": "Objectives: Read", "reason": "teaching instruction"},
        {"ref": "S3", "starts_with": "AccessMedicine", "reason": "access link for the textbook"},
        {"ref": "S3", "starts_with": "Point students", "reason": "teaching instruction; the reading split is taught in About this lecture"},
        {"ref": "S3", "starts_with": "Readings: Katzung chapters 37-39", "reason": "presenter script; taught in About this lecture"},
        *[{"ref": r, "starts_with": "Section transition", "reason": "section divider"} for r in ("S4", "S11", "S19")],
        {"ref": "S4", "starts_with": "Section 01", "reason": "section divider"},
        {"ref": "S11", "starts_with": "Section 02", "reason": "section divider"},
        {"ref": "S19", "starts_with": "Section 03", "reason": "section divider"},
        {"ref": "S5", "starts_with": "Keep returning", "reason": "teaching instruction"},
        {"ref": "S7", "starts_with": "Figure 2. Teal", "reason": "figure colour key (the figure is redrawn as an interactive)"},
        {"ref": "S18", "starts_with": "\"Why must iodine", "reason": "teaching instruction; the answer is taught from S18"},
        {"ref": "S29", "starts_with": "Thyroid: levothyroxine", "reason": "teaching instruction; the drugs are in the profiles"},
        {"ref": "S29", "starts_with": "Adrenal: prednisone", "reason": "teaching instruction; the drugs are in the profiles"},
        {"ref": "S5", "starts_with": "Figure 1: Trace", "reason": "teaching instruction; the figure is interactive"},
        {"ref": "S6", "starts_with": "Acromegaly pharmacology", "reason": "teaching instruction; taught in pearls"},
        {"ref": "S8", "starts_with": "Prolactin: dopamine", "reason": "presenter script; taught from S9"},
        {"ref": "S8", "starts_with": "Ask: \"Which way", "reason": "teaching instruction"},
        {"ref": "S14", "starts_with": "Figure 6: Iodide", "reason": "presenter script; taught from S14"},
        {"ref": "S15", "starts_with": "Methimazole is first-line for most patients and", "reason": "presenter script; taught from S15"},
        {"ref": "S16", "starts_with": "Thyroid storm is treated", "reason": "presenter script"},
        {"ref": "S17", "starts_with": "Figure 7: Four drugs", "reason": "presenter script; taught from S17"},
        {"ref": "S18", "starts_with": "This case reinforces", "reason": "teaching instruction"},
        {"ref": "S18", "starts_with": "Ask: \"Why must", "reason": "teaching instruction; the answer is taught from S18"},
        {"ref": "S21", "starts_with": "Figure 8: The steroid", "reason": "presenter script; taught from S21"},
        {"ref": "S22", "starts_with": "Figure 9: Chronic", "reason": "presenter script; taught from S22"},
        {"ref": "S23", "starts_with": "Enzyme blockers", "reason": "presenter script"},
        {"ref": "S24", "starts_with": "Figure 10: Receptor", "reason": "presenter script; taught from S24"},
        {"ref": "S25", "starts_with": "Use this table", "reason": "teaching instruction"},
        {"ref": "S25", "starts_with": "Walk the four rows", "reason": "teaching instruction"},
        {"ref": "S26", "starts_with": "Drug-name stems", "reason": "presenter script; the stems are taught in Part 3"},
        {"ref": "S27", "starts_with": "Missed refills", "reason": "presenter script; taught from S27"},
        {"ref": "S28", "starts_with": "Close Session 1", "reason": "teaching instruction"},
        {"ref": "S28", "starts_with": "Read the five points", "reason": "teaching instruction"},
        {"ref": "S29", "starts_with": "How to use in class", "reason": "teaching instruction"},
        {"ref": "S29", "starts_with": "Abbreviation key: Review", "reason": "teaching instruction"},
        {"ref": "S29", "starts_with": "Teaching points by class", "reason": "teaching instruction; the drugs are in the profiles"},
        *[{"ref": "S29", "starts_with": w, "reason": "Bloom's teaching prompt; rebuilt as practice questions"} for w in ("Bloom", "Understand", "Apply", "Analyze", "Evaluate")],
        {"ref": "S52", "starts_with": "Supporting drugs: Read", "reason": "teaching instruction"},
        {"ref": "S53", "starts_with": "This slide documents", "reason": "administrative note on AI-tool citation"},
        {"ref": "S53", "starts_with": "Original figures 1, 6 and 9", "reason": "administrative note on AI-tool citation"},
    ],
}

for _cl in content["classes"]:
    for _fg in _cl.get("figures", []):
        if not _fg["viz"].get("title"):
            _fg["viz"]["title"] = _fg["title"].split("·", 1)[-1].strip()

sys.path.insert(0, str(Path(__file__).parent))
import guide_L07 as G  # noqa: E402
content["guide"] = {"summary": [{"text": t, "src": s} for t, s in G.SUMMARY], "teaser": getattr(G, "TEASER", ""),
                    "cram": [{"prompt": p, "answer": a, "src": s} for p, a, s in G.CRAM], "discrepancies": []}
for _cl in content["classes"]:
    _cl["flows"] = G.FLOWS.get(_cl["name"], [])

import textbook_L07 as TBK  # noqa: E402
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
