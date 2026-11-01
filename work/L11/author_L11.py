"""Authoring source for L11 content.json. Run: python3 author_L11.py"""
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


PROF = {p["slide"]: p for p in PR.read("L11")}


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
    {"id": "IO6.1", "src": "Syllabus", "text": "Identify major pharmacologic classes used in the management of genitourinary and reproductive conditions and describe their mechanisms of action."},
    {"id": "IO6.2", "src": "Syllabus", "text": "Describe the indications, contraindications, adverse effects, and clinically significant interactions associated with medications used to treat genitourinary and reproductive conditions."},
    {"id": "IO6.3", "src": "Syllabus", "text": "Compare pharmacologic agents within and across therapeutic classes to distinguish clinically relevant differences in efficacy, safety, and use."},
    {"id": "IO6.4", "src": "Syllabus", "text": "Select appropriate pharmacologic therapy for common genitourinary and reproductive conditions based on clinical presentation and patient-specific factors."},
    {"id": "IO6.5", "src": "Syllabus", "text": "Identify appropriate dosing, administration, and monitoring considerations for medications used in genitourinary and reproductive conditions."},
    {"id": "IO6.6", "src": "Syllabus", "text": "Explain important medication-use and safety information to patients receiving genitourinary and reproductive pharmacotherapy."},
    {"id": "SO1", "src": "S2", "text": "Describe the physiologic roles and clinical uses of estrogens and progestins, including combined and progestin-only hormonal contraception."},
    {"id": "SO2", "src": "S2", "text": "Describe the mechanism, tissue-selective actions, and adverse effects of selective estrogen receptor modulators (SERMs) and aromatase inhibitors."},
    {"id": "SO3", "src": "S2", "text": "Describe the clinical uses, adverse effects, and monitoring considerations for androgens and antiandrogens."},
    {"id": "SO4", "src": "S2", "text": "Explain the pathophysiology of polycystic ovary syndrome (PCOS) as a reproductive-metabolic overlap condition, including the central role of insulin resistance."},
    {"id": "SO5", "src": "S2", "text": "Describe the role of metformin and other antidiabetic agents in the management of PCOS and related reproductive-metabolic conditions."},
]

about = [
    F("**PA PHARMACOLOGY COURSE · LECTURE 6 · SESSION 1 OF 2** — Genitourinary & Reproductive Pharmacology. **Session 1: Gonadal Hormones and the Reproductive-Metabolic Overlap  |  Tuesday, November 24  |  8:30–11:00 AM**", "S1"),
    F("Organizing idea: the hypothalamic-pituitary-gonadal axis. Every drug in this session replaces a sex steroid, blocks its receptor, blocks its synthesis, or reduces the metabolic driver, insulin resistance, that fuels androgen excess in PCOS.", "S1 (notes)"),
    F("Arc: gonadal steroid pharmacology first (estrogens, progestins, SERMs, aromatase inhibitors, androgens/antiandrogens), then the reproductive-metabolic overlap through PCOS.", "S2 (notes)"),
    F("Preview: autonomic pharmacology of the bladder and lower urinary tract continues in Session 2 (Tuesday, December 1) — mechanistically distinct, but sharing cross-system classes (alpha1 blockers, NO-cGMP signaling).", "S2; S2 (notes)"),
    F("Readings: Katzung chapter 40 (The Gonadal Hormones and Inhibitors) and selected sections of chapter 41 (Pancreatic Hormones & Antidiabetic Drugs) focused on the reproductive/metabolic overlap (e.g., PCOS and insulin resistance).", "S3; S3 (notes)"),
    F("Chapter 6 (Introduction to Autonomic Pharmacology) — the sections on Autonomic Receptors and Non-Adrenergic, Noncholinergic (NANC) Neurons — supports Session 2’s bladder and lower urinary tract content, not today.", "S3; S3 (notes)"),
    F("Required text: Katzung’s Basic and Clinical Pharmacology, 16th Edition (Todd W. Vanderah, 2024/2025, McGraw-Hill Education; ISBN 1260463303 eBook). Pharmacotherapy Principles and Practice (Chisholm-Burns et al., 2022) remains additional support alongside all assigned chapters.", "S3"),
    F("**Appendix 1** — Drug Profiles: study reference for the drugs covered in Session 1. Know the dose logic, the serious adverse effect, the contraindication that changes decisions and the toxicity you would need to recognize.", "S28; S28 (notes)"),
    F("**Abbreviation key** **PO = by mouth** **IM = intramuscular** **IV = intravenous** **SC = subcutaneous** **BID / TID = twice / three times daily** **ER = extended-release** **IUD = intrauterine device** **DMPA = depot medroxyprogesterone acetate**", "S28; S28 (notes)"),
    F("**GnRH = gonadotropin-releasing hormone** **VTE = venous thromboembolism** **DVT / PE = deep vein thrombosis / pulmonary embolism** **MI = myocardial infarction** **PCOS = polycystic ovary syndrome** **BPH = benign prostatic hyperplasia**", "S28; S28 (notes)"),
    F("**PSA = prostate-specific antigen** **CBC = complete blood count** **CYP = cytochrome P450** **GI = gastrointestinal** **DCIS = ductal carcinoma in situ** **eGFR / CrCl = estimated glomerular filtration rate / creatinine clearance** **ER-positive = estrogen receptor-positive**", "S28; S28 (notes)"),
    F("**Standard adult dosing for teaching; verify against current prescribing information.**", "S29-44"),
    F("**Appendix 2: DRUG PROFILE · SUPPORTING** — supporting drugs explain interactions. Listed for context; not profiled in detail.", "S45; S45 (notes)"),
    F("**Original figures in this deck:** Figures 2, 4 and 7 (The Hypothalamic-Pituitary-Gonadal (HPG) Axis: Sites of Hormonal Drug Action; Two Ways to Reduce Estrogen Signaling: SERMs vs. Aromatase Inhibitors; The PCOS–Insulin Resistance Cycle) were generated by the course director using the AI tool Claude.", "S46"),
    F("They are original diagrams, not reproduced from Katzung’s Basic and Clinical Pharmacology or any other copyrighted source. **Mechanism illustrations:** Figures 1, 3, 5, 6 and 8 are illustrative AI-generated schematics. **Reference:** Anthropic. (2026). Claude (Sonnet 5) [Large language model]. https://claude.ai", "S46; S46 (notes)"),
]

# ---------------------------------------------------------------- Part 1: estrogens, progestins, contraception
t1 = {
    "name": "Estrogens, Progestins & Contraception", "template": "drug_class", "objectives": ["SO1", "IO6.1", "IO6.2", "IO6.4", "IO6.6"],
    "sections": {
        "overview": [
            F("**The two core gonadal steroid classes, and how they are combined for contraception and hormone therapy.**", "S4"),
            F("**Figure 2. Original illustrative diagram (not from Katzung): GnRH drives FSH/LH release, which drives gonadal sex-steroid production, which in turn negatively feeds back on the hypothalamus and pituitary —**", "S8"),
            F("**with four distinct classes of drugs intervening at different points along this axis.** This is the organizing map for the session: GnRH agonists/antagonists, SERMs, aromatase inhibitors and antiandrogens each anchor to a point on it.", "S8; S8 (notes)"),
        ],
        "prototype": [
            F("Estradiol and ethinyl estradiol (estrogens); norethindrone, medroxyprogesterone, levonorgestrel (progestins); combined oral contraceptives.", "S5; S6; S26"),
        ],
        "moa": [
            F("**Mechanism: bind intracellular estrogen receptors (ER-alpha, ER-beta), regulating gene transcription in reproductive, bone, cardiovascular, and CNS tissue.**", "S5; S4 (notes); SG U6-R1"),
            F("Estrogen physiologic effects: endometrial proliferation, breast development, bone density maintenance, favorable lipid profile effects (↑ HDL, ↓ LDL).", "S5; SG U6-R1"),
            F("**Mechanism: bind progesterone receptors, counteracting estrogen-driven endometrial proliferation and thickening cervical mucus.**", "S6"),
            F("Unopposed estrogen chain (Figure 1): estrogen binds ER in the endometrium → proliferation and thickening of the lining → without progestin: hyperplasia and cancer risk → progestin binds PR: limits proliferation, matures the endometrium.", "S7; S7 (notes)"),
            F("Unopposed estrogen drives unchecked endometrial proliferation; a progestin counteracts this proliferation.", "SG U6-R2"),
            F("Combined methods (oral pills, transdermal patch, vaginal ring) suppress ovulation via negative feedback on FSH/LH.", "S9"),
        ],
        "indications": [
            F("Estrogen clinical uses: hormonal contraception (combined with a progestin), menopausal hormone therapy for vasomotor symptoms, and hypogonadism.", "S5"),
            F("Progestins: a required component of combined hormonal contraception (protects the endometrium from unopposed estrogen), progestin-only contraception, and management of abnormal uterine bleeding.", "S6"),
            F("Progestin-only methods — the \"mini-pill,\" depot medroxyprogesterone acetate (DMPA) injection, the subdermal implant, and the levonorgestrel intrauterine system — avoid estrogen-related VTE risk entirely.", "S6; S9; SG U6-R4"),
            F("Combined methods are often chosen for added benefits: cycle regulation, acne/hirsutism improvement.", "S9"),
            F("When estrogen is contraindicated, a progestin-only method is not a compromise — it is often the correct first choice (safe with VTE history, migraine with aura, or smokers over 35).", "S9; S9 (notes)"),
        ],
        "adverse": [
            F("**Adverse effects: venous thromboembolism (VTE) risk, increased risk with smoking and age over 35, nausea, breast tenderness, and a possible increase in certain hormone-sensitive cancer risks with long-term use.**", "S5"),
            F("Estrogen’s VTE risk is the single most tested adverse effect: know the risk factors (smoking, age > 35, personal/family VTE history) that shift a patient from \"candidate\" to \"contraindicated.\"", "S5 (notes)"),
            F("**Adverse effects: irregular bleeding/spotting (especially early in use), mood changes, and — with DMPA specifically — reversible bone mineral density loss with prolonged use.**", "S6; S9; SG U6-R4"),
            F("**Unopposed estrogen (estrogen without a progestin) in a patient with a uterus significantly increases endometrial cancer risk — this is why progestin-only or combined regimens, never estrogen alone, are used in patients with an intact uterus.**", "S6; SG U6-R2"),
        ],
        "contra": [
            F("Estrogen contraindications: history of VTE, estrogen-sensitive breast cancer, uncontrolled hypertension, and smokers over age 35 — all raise cardiovascular/thrombotic risk substantially. Smoking combined with age over 35 makes a progestin-only method (no estrogen, no added VTE risk) the appropriate choice.", "S5; S5 (notes); SG U6-R3"),
            F("Combined methods carry estrogen-related VTE risk — require screening for contraindications. Hysterectomy patients can take estrogen alone.", "S7; S9"),
        ],
        "interactions": [
            F("Enzyme inducers (rifampin, carbamazepine, phenytoin, St. John’s wort) lower combined contraceptive efficacy.", "S45; S45 (notes)"),
        ],
        "pk": [],
        "monitoring": [
            F("Progestin-only methods have more irregular bleeding patterns, especially initially; DMPA specifically: reversible bone density loss with long-term use.", "S9"),
        ],
        "pearls": [
            F("The \"unopposed estrogen\" point is a classic exam item: any patient with a uterus receiving estrogen needs a progestin too, unless she has had a hysterectomy.", "S6 (notes); S7 (notes)"),
        ],
    },
    "figures": [
        {"image": "S7_1.jpg", "title": "Figure 1 · Unopposed estrogen: why a progestin is added", "src": "S7; S7 (notes)",
         "caption": "**Schematic (illustrative)** — Figure 1. Progestin counters estrogen’s proliferative effect on the endometrium: without it, hyperplasia and cancer risk; estrogen alone only after hysterectomy.",
         "viz": path([N("e", "Estrogen binds\nER (endometrium)", "membrane", 10, 55, 150, "teal"), N("p", "Lining\nproliferates", "cell", 180, 55, 130, "amber"),
                      N("h", "Hyperplasia,\ncancer risk", "effect", 330, 55, 140, "coral"), N("m", "Matured,\nprotected lining", "effect", 490, 55, 140, "sage")],
                     [["e", "p"], ["p", "h"]],
                     [Dg("Estradiol alone (uterus intact)", "e", "Unopposed — endometrial cancer risk (S6–S7)."),
                      Dg("Add a progestin", "p", "PR limits proliferation (S6–S7).", off=["h"]),
                      Dg("After hysterectomy", "e", "Estrogen alone is fine (S7).", off=["h"])],
                     "Uterus present? Add a progestin.")},
        {"image": "S8_1.jpg", "title": "Figure 2 · The HPG axis: sites of hormonal drug action", "src": "S8; S8 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): GnRH → FSH/LH → gonadal sex steroids, which feed back negatively on the hypothalamus and pituitary; GnRH analogs, combined contraceptives, SERMs, aromatase inhibitors and antiandrogens act at different points.",
         "viz": path([N("gn", "Hypothalamus:\nGnRH", "signal", 10, 55, 130, "blue"), N("lh", "Pituitary:\nFSH, LH", "signal", 160, 55, 130, "teal"),
                      N("st", "Gonad: estrogen,\ntestosterone", "cell", 310, 55, 150, "amber"), N("r", "Tissue\nreceptors", "membrane", 480, 55, 140, "sage")],
                     [["gn", "lh"], ["lh", "st"], ["st", "r"]],
                     [Dg("Combined pill", "gn", "Feedback suppression of FSH/LH (S9).", off=["lh"]),
                      Dg("Leuprolide (GnRH agonist)", "gn", "Used with antiandrogens in prostate cancer (S45)."),
                      Dg("Anastrozole", "st", "Blocks peripheral estrogen synthesis (S14)."),
                      Dg("Tamoxifen / bicalutamide", "r", "Receptor-level blockers (S11; S16).")],
                     "Each class acts at a different point on one axis.")},
    ],
    "comparisons": [
        {"title": "Combined vs. progestin-only contraception (S9)", "columns": ["", "Combined (estrogen + progestin)", "Progestin-only"],
         "rows": [["Forms", "Oral pills, transdermal patch, vaginal ring", "Mini-pill, DMPA injection, subdermal implant, levonorgestrel IUD"],
                  ["How", "Suppresses ovulation via negative feedback on FSH/LH", "Thickens cervical mucus; counters endometrial proliferation"],
                  ["VTE", "Carries estrogen-related VTE risk — screen for contraindications", "No estrogen — safe with VTE history, migraine with aura, smokers over 35"],
                  ["Other", "Cycle regulation, acne/hirsutism improvement", "Irregular bleeding early; DMPA reversible bone loss"]],
         "src": "S9"},
        *tab((29, 30, 31, 32, 33), "Estrogen, progestin and contraceptive profiles"),
    ],
    "hooks": [
        {"kind": "why", "text": "Why a progestin with estrogen when the uterus is intact? Estrogen alone keeps the lining growing — hyperplasia, then cancer; the progestin matures it.", "src": "S6; S7"},
    ],
    "high_yield": [
        F("Estrogen = VTE (smoking, age > 35, VTE history); unopposed estrogen = endometrial cancer → always pair with a progestin if the uterus is intact.", "S5; S6"),
        F("Estrogen contraindicated → progestin-only is the right first choice; DMPA = reversible bone loss.", "S6; S9"),
    ],
    "questions": [
        Q("vignette", "A 52-year-old with an intact uterus wants estradiol for hot flashes. What must be added?",
          "A progestin to protect the endometrium",
          "Unopposed estrogen with a uterus raises endometrial cancer risk; add a progestin (S6–S7).",
          [("Nothing, if the dose is low", "Still unopposed (S6)."),
           ("Tamoxifen to block the endometrium", "Tamoxifen stimulates it (S11)."),
           ("An aromatase inhibitor", "Not the answer (S14)."),
           ("Spironolactone for balance", "Not the answer (S15).")], "S6; S7"),
        Q("vignette", "A 36-year-old smoker with migraine with aura wants contraception. Which choice fits best?",
          "Progestin-only method (LNG IUD)",
          "Estrogen is contraindicated; progestin-only methods avoid estrogen VTE risk and are the correct first choice (S9).",
          [("A combined pill at the lowest dose", "Still estrogen (S9)."),
           ("A combined vaginal ring", "Contains estrogen (S9)."),
           ("A combined transdermal patch", "Contains estrogen (S9)."),
           ("Estradiol tablets alone", "Unopposed estrogen (S6).")], "S5; S9"),
        Q("mechanism", "How do progestins protect the endometrium in combined or hormone therapy?",
          "They counter estrogen-driven proliferation",
          "Progestins bind progesterone receptors, limiting estrogen-driven proliferation and maturing the endometrium (S6–S7).",
          [("They block estrogen receptors in the uterus", "They act at PR, not ER (S6)."),
           ("They lower circulating estrogen levels", "Not the mechanism (S6)."),
           ("They thin cervical mucus to aid clearance", "They thicken mucus (S6)."),
           ("They block aromatase in the endometrium", "Aromatase inhibitors do that elsewhere (S14).")], "S6; S7; SG U6-R2"),
        Q("mechanism", "Which adverse effect is specific to depot medroxyprogesterone (DMPA) with prolonged use?",
          "Reversible bone mineral density loss",
          "DMPA specifically causes reversible bone density loss with long-term use (boxed warning) (S6; S9; S31).",
          [("Endometrial cancer from unopposed estrogen", "DMPA contains no estrogen (S6)."),
           ("Hyperkalemia from potassium retention", "Drospirenone or spironolactone (S29; S39)."),
           ("Erythrocytosis with a high hematocrit", "Testosterone (S15)."),
           ("Lactic acidosis in renal impairment", "Metformin (S22).")], "S6; S9; S31"),
    ],
}

# ---------------------------------------------------------------- Part 2: SERMs, AIs, androgens
t2 = {
    "name": "SERMs, Aromatase Inhibitors & Androgens", "template": "drug_class", "objectives": ["SO2", "SO3", "IO6.1", "IO6.2", "IO6.3", "IO6.5"],
    "sections": {
        "overview": [
            F("**Tissue-selective and blocking strategies — how drugs can turn hormone signaling on in one tissue and off in another.**", "S10"),
            F("A receptor-blocking strategy and a synthesis/activation-blocking strategy exist on both the estrogen and androgen sides.", "S17; S17 (notes)"),
        ],
        "prototype": [
            F("Tamoxifen, raloxifene (SERMs); anastrozole, letrozole (aromatase inhibitors); testosterone; spironolactone, flutamide, bicalutamide (antiandrogens); finasteride, dutasteride (5-ARIs).", "S11; S14; S15"),
        ],
        "moa": [
            F("**Mechanism: bind the estrogen receptor, but act as an agonist in some tissues and an antagonist in others — the defining feature of this class.** Same receptor, different conformation and co-regulators in each tissue.", "S11; S12 (notes); SG U6-R5"),
            F("Tamoxifen: ER antagonist in breast tissue but an ER agonist in bone (preserves density) and, notably, in the endometrium. Tamoxifen antagonizes breast and agonizes bone and endometrium.", "S11; S12; S10 (notes)"),
            F("Raloxifene: ER antagonist in breast and ER agonist in bone, but — unlike tamoxifen — essentially neutral at the endometrium; tamoxifen is an ER agonist at the endometrium (raising endometrial cancer risk), both being ER antagonists in breast.", "S11; S12; SG U6-R5"),
            F("Aromatase chain (Figure 5): androgens (androstenedione, testosterone) → aromatase in fat tissue converts them to estrogens → estrogens drive ER-positive tumor growth → anastrozole and letrozole block aromatase.", "S14"),
            F("**Figure 4. Original illustrative diagram (not from Katzung): SERMs block the estrogen receptor directly in breast tissue (while remaining agonists elsewhere), while aromatase inhibitors block the peripheral enzymatic conversion of androgens to estrogen —**", "S13"),
            F("**two distinct strategies converging on the same clinical goal in hormone-sensitive breast cancer.** Receptor blockade versus synthesis blockade.", "S13; S13 (notes)"),
            F("Androgen pathway (Figure 6): testosterone (circulating androgen) → 5-alpha-reductase converts it to DHT (more potent) → binds the androgen receptor → hair follicle and prostate effects.", "S16; S15 (notes)"),
            F("Finasteride and dutasteride block 5-alpha-reductase, lowering DHT; spironolactone, flutamide and bicalutamide block the androgen receptor. Blocking the enzyme or the receptor both reduce androgen action — different mechanisms grouped under the same broad \"antiandrogen\" label.", "S16; S16 (notes); SG U6-R8"),
        ],
        "indications": [
            F("Tamoxifen: ER-positive breast cancer treatment and prevention. Raloxifene: preferred option for osteoporosis prevention in postmenopausal women without a breast cancer indication.", "S11"),
            F("Aromatase inhibitors block peripheral enzymatic conversion of androgens to estrogen rather than acting at the receptor — postmenopausal use only: before menopause the ovaries are the dominant estrogen source (often combined with ovarian suppression).", "S13 (notes); S14; S14 (notes); SG U6-R6"),
            F("**●  Testosterone (androgen):** used for male hypogonadism.", "S15"),
            F("**●  Spironolactone (antiandrogen):** blocks the androgen receptor (in addition to its aldosterone-antagonist diuretic effect from Unit 5) — used off-label for hirsutism and acne in women, especially in PCOS.", "S15"),
            F("**●  Flutamide / bicalutamide (antiandrogens):** pure androgen receptor blockers used primarily in prostate cancer, often combined with a GnRH agonist (leuprolide).", "S15; S45"),
            F("**●  Finasteride / dutasteride (5-alpha-reductase inhibitors):** block conversion of testosterone to the more potent dihydrotestosterone (DHT); used for hirsutism and androgenetic alopecia here, and — in Session 2 — for benign prostatic hyperplasia (BPH).", "S15; S15 (notes)"),
            F("Estrogen-pathway drugs are used primarily in hormone-sensitive breast cancer; androgen-pathway drugs for hirsutism, prostate cancer, alopecia, and BPH.", "S17"),
        ],
        "adverse": [
            F("**Tamoxifen’s endometrial agonist activity increases the risk of endometrial hyperplasia and endometrial cancer — patients require counseling on abnormal bleeding and routine gynecologic follow-up.**", "S11"),
            F("Both SERMs carry an increased VTE risk, similar in magnitude to estrogen therapy itself.", "S11; S12"),
            F("Aromatase inhibitor adverse effects: bone loss and joint pain.", "S14; S14 (notes)"),
            F("Testosterone: erythrocytosis, hepatotoxicity (oral formulations), and suppression of endogenous testicular function/fertility.", "S15"),
        ],
        "contra": [
            F("Spironolactone: avoid in pregnancy (teratogenic risk).", "S24"),
        ],
        "interactions": [
            F("CYP2D6 inhibitors (paroxetine, fluoxetine) blunt tamoxifen activation. Testosterone and tamoxifen raise INR with warfarin.", "S45; S45 (notes)"),
            F("Bisphosphonates and calcium with vitamin D protect bone with aromatase inhibitors. ACE inhibitors, ARBs and potassium: hyperkalemia with spironolactone.", "S45; S45 (notes)"),
        ],
        "pk": [],
        "monitoring": [
            F("Testosterone therapy requires monitoring hematocrit (erythrocytosis risk) and PSA with long-term use, with additional risks of hepatotoxicity (oral formulations) and suppression of endogenous fertility.", "S15; SG U6-R7"),
        ],
        "pearls": [
            F("The tamoxifen-vs-raloxifene endometrial distinction is a classic high-yield comparison: tamoxifen carries the endometrial cancer risk because of tissue-selective agonism, not a class effect.", "S11 (notes); S12 (notes)"),
            F("Finasteride/dutasteride are a direct bridge to Session 2 — the same drugs reappear for BPH (prostate growth rather than hirsutism).", "S15 (notes)"),
            F("Case: a 52-year-old postmenopausal woman with ER-positive breast cancer starts tamoxifen; six months later, new-onset irregular vaginal bleeding. **What is the most likely explanation, and what should happen next?**", "S18"),
            F("**Tamoxifen acts as an estrogen receptor agonist in the endometrium even while acting as an antagonist in breast tissue — this tissue-selective agonism increases the risk of endometrial hyperplasia and endometrial cancer.**", "S18"),
            F("**New abnormal bleeding on tamoxifen warrants prompt gynecologic evaluation, not reassurance.** A natural contrast with raloxifene’s neutral endometrial profile.", "S18; S18 (notes)"),
        ],
    },
    "figures": [
        {"image": "S12_1.png", "title": "Figure 3 · SERMs: one receptor, different tissue effects", "src": "S12; S12 (notes)",
         "caption": "Schematic (illustrative) — Figure 3. Tamoxifen and raloxifene act on the same receptor but differ by tissue; tamoxifen’s endometrial agonism carries cancer risk. Both raise VTE risk.",
         "viz": path([N("er", "Estrogen receptor", "membrane", 10, 95, 150, "teal"), N("br", "Breast", "cell", 260, 10, 130, "blue"),
                      N("bo", "Bone", "cell", 260, 95, 130, "sage"), N("en", "Endometrium", "cell", 260, 180, 130, "coral"),
                      N("risk", "Endometrial\ncancer risk", "effect", 470, 180, 150, "deep")],
                     [["er", "br"], ["er", "bo"], ["er", "en"], ["en", "risk"]],
                     [Dg("Tamoxifen", "er", "Breast blocked; bone and endometrium activated (S11–S12).", off=["br"]),
                      Dg("Raloxifene", "er", "Breast blocked; bone activated; endometrium neutral (S11–S12).", off=["br", "en", "risk"])],
                     "Same receptor, different answer in each tissue.", h=260)},
        {"image": "S13_1.jpg", "title": "Figure 4 · Two ways to reduce estrogen signaling", "src": "S13; S13 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): SERMs block the receptor in breast; aromatase inhibitors block peripheral conversion of androgens to estrogen — two strategies for hormone-sensitive breast cancer.",
         "viz": path([N("an", "Androgens", "molecule", 10, 55, 120, "amber"), N("ar", "Aromatase\n(fat tissue)", "enzyme", 150, 55, 130, "blue"),
                      N("es", "Estrogen", "molecule", 300, 55, 120, "teal"), N("er", "ER in breast\ntumor → growth", "effect", 440, 55, 180, "coral")],
                     [["an", "ar"], ["ar", "es"], ["es", "er"]],
                     [Dg("Anastrozole / letrozole", "ar", "Synthesis blockade; postmenopausal only (S13–S14).", off=["es", "er"]),
                      Dg("Tamoxifen", "er", "Receptor blockade in breast (S11; S13).", off=["er"])],
                     "Block the factory or block the lock.")},
        {"image": "S14_1.png", "title": "Figure 5 · Aromatase inhibitors: blocking estrogen synthesis", "src": "S14; S14 (notes)",
         "caption": "Schematic (illustrative) — Figure 5. Aromatase converts androgens to estrogens in peripheral fat; aromatase inhibitors block this step. They act downstream of the ovary, so they work mainly after menopause.",
         "viz": path([N("ov", "Ovary\n(premenopausal)", "cell", 10, 20, 140, "sage"), N("fat", "Fat aromatase\n(postmenopausal)", "enzyme", 10, 130, 150, "blue"),
                      N("e", "Estrogen", "molecule", 260, 75, 120, "teal"), N("t", "ER+ tumor\ngrowth", "effect", 450, 75, 160, "coral")],
                     [["ov", "e"], ["fat", "e"], ["e", "t"]],
                     [Dg("Letrozole", "fat", "Bone loss, joint pain (S14).", off=["fat"]),
                      Dg("Before menopause", "ov", "Ovary still makes estrogen — AI alone insufficient (S13–S14).")],
                     "Why aromatase inhibitors are postmenopausal drugs.", h=230)},
        {"image": "S16_1.png", "title": "Figure 6 · Androgen pathway: where each drug acts", "src": "S16; S16 (notes)",
         "caption": "Schematic (illustrative) — Figure 6. Androgen pathway from testosterone to receptor action, with the sites of finasteride, dutasteride (enzyme) and spironolactone, flutamide, bicalutamide (receptor).",
         "viz": path([N("t", "Testosterone", "molecule", 10, 55, 130, "teal"), N("r5", "5-alpha-\nreductase", "enzyme", 160, 55, 120, "blue"),
                      N("d", "DHT", "molecule", 300, 55, 100, "amber"), N("ar", "Androgen\nreceptor", "membrane", 420, 55, 120, "deep"),
                      N("eff", "Hair, prostate", "effect", 420, 150, 130, "coral")],
                     [["t", "r5"], ["r5", "d"], ["d", "ar"], ["ar", "eff"]],
                     [Dg("Finasteride / dutasteride", "r5", "Lower DHT (S16).", off=["d"]),
                      Dg("Spironolactone / flutamide / bicalutamide", "ar", "Block the receptor (S16).", off=["eff"])],
                     "Enzyme blockers vs. receptor blockers.", h=230)},
    ],
    "comparisons": [
        {"title": "Estrogen-pathway vs. androgen-pathway drugs (S17)", "columns": ["", "Estrogen pathway", "Androgen pathway"],
         "rows": [["Receptor strategy", "SERMs (tamoxifen, raloxifene): tissue-selective agonist/antagonist", "Antiandrogens (spironolactone, flutamide): block the androgen receptor"],
                  ["Synthesis strategy", "Aromatase inhibitors (anastrozole, letrozole): postmenopausal only", "5-alpha-reductase inhibitors (finasteride, dutasteride): block DHT formation"],
                  ["Main uses", "Hormone-sensitive breast cancer", "Hirsutism, prostate cancer, alopecia, BPH"]],
         "src": "S17"},
        {"title": "Tamoxifen vs. raloxifene (S11–S12)", "columns": ["Tissue", "Tamoxifen", "Raloxifene"],
         "rows": [["Breast", "Antagonist", "Antagonist"], ["Bone", "Agonist", "Agonist"],
                  ["Endometrium", "Agonist — hyperplasia/cancer risk", "Essentially neutral"], ["VTE", "Increased", "Increased"]],
         "src": "S11; S12"},
        *tab((34, 35, 36, 37), "SERM and aromatase inhibitor profiles"),
        *tab((38, 39, 40, 41, 42, 43), "Androgen and antiandrogen profiles"),
    ],
    "hooks": [
        {"kind": "why", "text": "Why are aromatase inhibitors useless before menopause? The ovary still makes most of the estrogen; the drug only blocks the peripheral (fat) source.", "src": "S13 (notes); S14"},
    ],
    "high_yield": [
        F("Tamoxifen: breast antagonist, endometrial agonist → bleeding needs evaluation; raloxifene: endometrium neutral; both VTE.", "S11; S18"),
        F("Aromatase inhibitors: postmenopausal only; bone loss and joint pain.", "S14"),
    ],
    "questions": [
        Q("vignette", "Six months into tamoxifen for ER-positive breast cancer, a 52-year-old reports new irregular vaginal bleeding. Next step?",
          "Prompt gynecologic evaluation",
          "Tamoxifen is an endometrial agonist (hyperplasia/cancer risk); new bleeding needs prompt evaluation, not reassurance (S18).",
          [("Reassure — expected with tamoxifen", "Not reassurance (S18)."),
           ("Add estrogen to stabilize the lining", "Worsens risk (S6)."),
           ("Switch to raloxifene for her cancer", "Not a breast cancer treatment (L08 S8)."),
           ("Stop tamoxifen, no further workup", "Evaluate first (S18).")], "S18", from_slides="S18"),
        Q("mechanism", "Why is raloxifene preferred over tamoxifen for osteoporosis prevention in a woman without breast cancer?",
          "It is neutral at the endometrium",
          "Both are bone agonists; raloxifene is essentially neutral at the endometrium (S11).",
          [("It does not raise VTE risk", "Both raise VTE (S11)."),
           ("It is an endometrial agonist", "That is tamoxifen (S11)."),
           ("It blocks aromatase", "That is anastrozole (S14)."),
           ("It antagonizes bone resorption via DHT", "Not the mechanism (S11).")], "S11; S12"),
        Q("vignette", "A 45-year-old premenopausal woman with ER-positive breast cancer asks about letrozole alone. Key point?",
          "Insufficient alone before menopause",
          "Before menopause the ovaries are the dominant estrogen source; AIs need ovarian suppression (S13–S14).",
          [("Ideal — works best before menopause", "Postmenopausal only (S14)."),
           ("It blocks the estrogen receptor", "It blocks synthesis (S14)."),
           ("Its main risk is endometrial cancer", "Bone loss and joint pain (S14)."),
           ("It raises estrogen to fight the tumor", "Lowers it (S14).")], "S13; S14"),
        Q("mechanism", "How do finasteride and spironolactone differ in reducing androgen action?",
          "Finasteride blocks DHT synthesis; spironolactone the receptor",
          "5-ARIs block testosterone → DHT; spironolactone blocks the androgen receptor (S16).",
          [("Both block 5-alpha-reductase", "Spironolactone blocks the receptor (S16)."),
           ("Both block the androgen receptor", "Finasteride blocks the enzyme (S16)."),
           ("Finasteride blocks aromatase", "Anastrozole does (S14)."),
           ("Spironolactone lowers testosterone production in the testis", "Receptor blocker (S16).")], "S15; S16"),
        Q("vignette", "A man on testosterone therapy has a hematocrit of 55%. What adverse effect is this?",
          "Erythrocytosis from testosterone",
          "Testosterone causes erythrocytosis; monitor hematocrit and PSA (S15).",
          [("Hemolysis from G6PD deficiency", "Not testosterone (S15)."),
           ("Dehydration from spironolactone", "Not given (S15)."),
           ("Expected; no monitoring needed", "Monitor hematocrit (S15)."),
           ("Aromatase-inhibitor bone loss", "Not related (S14).")], "S15; S38"),
    ],
}

# ---------------------------------------------------------------- Part 3: PCOS
t3 = {
    "name": "PCOS & the Reproductive-Metabolic Overlap", "template": "drug_class", "objectives": ["SO4", "SO5", "IO6.1", "IO6.3", "IO6.4", "IO6.5"],
    "sections": {
        "overview": [
            F("**Where Chapter 40 and Chapter 41 meet — insulin resistance as a driver of reproductive endocrine disease.**", "S19"),
            F("**Polycystic ovary syndrome (PCOS) is defined by a combination of hyperandrogenism, ovulatory dysfunction, and polycystic ovarian morphology — but its pharmacologic management is fundamentally a metabolic problem as much as a reproductive one.**", "S20"),
            F("**This is why PCOS management routinely pulls drugs from Chapter 41 (antidiabetic agents) as well as Chapter 40 (hormonal agents) — the two chapters converge on the same patient.** PCOS pharmacology is not purely \"gynecologic.\"", "S20; S20 (notes)"),
        ],
        "prototype": [
            F("Metformin; combined hormonal contraception; spironolactone; GLP-1 receptor agonists.", "S24"),
        ],
        "moa": [
            F("Insulin resistance and compensatory hyperinsulinemia are central to PCOS pathophysiology in most patients, independent of body weight.", "S20"),
            F("Hyperinsulinemia stimulates ovarian theca-cell androgen production directly and lowers hepatic sex hormone-binding globulin (SHBG) production, raising free (biologically active) testosterone — the mechanistic core of PCOS.", "S20; S19 (notes); SG U6-R9"),
            F("**Figure 7. Original illustrative diagram (not from Katzung): insulin resistance and hyperandrogenism reinforce one another in a self-sustaining cycle — hyperinsulinemia raises free testosterone, and hyperandrogenism worsens insulin resistance,**", "S21"),
            F("**explaining why metabolic therapy improves reproductive symptoms and vice versa.** Walk both arrows of the cycle.", "S21; S21 (notes)"),
            F("Metformin is not a direct hormonal agent — it improves hyperandrogenism indirectly, by reducing hyperinsulinemia’s stimulatory effect on ovarian androgen production (Figure 7) — by improving insulin sensitivity, not by acting on any hormone receptor.", "S22; SG U6-R10"),
            F("Chain (Figure 8): insulin resistance → high insulin → ovarian androgens up; liver SHBG down → free testosterone up → metformin lowers insulin → androgens fall; cycles and ovulation can return.", "S23; S23 (notes)"),
        ],
        "indications": [
            F("Clinical features follow the mechanism: hirsutism, acne, and anovulation/irregular cycles from hyperandrogenism; an elevated long-term risk of type 2 diabetes and metabolic syndrome from insulin resistance.", "S20"),
            F("**Metformin: first-line insulin-sensitizing agent in PCOS management; improves insulin sensitivity, can restore ovulatory cycles, and is commonly used alongside or instead of hormonal therapy depending on the patient's goals (cycle regulation vs. fertility).**", "S22"),
            F("GLP-1 receptor agonists are increasingly used off-label in PCOS patients with obesity, given their weight-loss and insulin-sensitizing effects — an emerging extension of the same principle.", "S22; S45"),
            F("Combined hormonal contraception remains first-line specifically for cycle regulation and hirsutism/acne when pregnancy is not desired — metformin and hormonal therapy are frequently used together, not as alternatives.", "S22; S24 (notes)"),
        ],
        "adverse": [
            F("**Adverse effects: GI upset (common, often transient), and rare but serious lactic acidosis risk in renal impairment — recall the renal dose-adjustment principles from Unit 5.**", "S22; S22 (notes)"),
            F("Common early effect: GI upset (nausea, diarrhea); take with meals.", "S23"),
        ],
        "contra": [
            F("Hold metformin for an iodinated contrast study or renal impairment.", "S23; S23 (notes)"),
        ],
        "interactions": [],
        "pk": [],
        "monitoring": [],
        "pearls": [
            F("Case: a 24-year-old with PCOS — irregular cycles, hirsutism, BMI 31 — not trying to conceive, no contraindications to estrogen. **What are the two major pharmacologic strategies available, and how do their goals differ?**", "S25"),
            F("**Combined hormonal contraception directly regulates cycles and improves hirsutism/acne through its hormonal effects, while metformin addresses the underlying insulin resistance driving the condition metabolically.**", "S25"),
            F("**The two are frequently combined rather than chosen as alternatives — contraception for immediate symptom control, metformin for the metabolic driver and long-term diabetes risk reduction.**", "S25; S25 (notes)"),
            F("Drug names reveal the class: **Stem** · **Class** · **Examples** · **Memory aid** — estr-/-estradiol estrogen (estradiol, ethinyl estradiol); -gest-/-gestrel progestin (levonorgestrel, norethindrone, medroxyprogesterone: gest- = pregnancy hormone).", "S26; S26 (notes)"),
            F("-ifene SERM (tamoxifen, raloxifene: modulates the estrogen receptor); -trozole aromatase inhibitor (anastrozole, letrozole: blocks aromatase); -steride 5-alpha-reductase inhibitor (finasteride, dutasteride: blocks steroid enzyme).", "S26"),
            F("-lutamide antiandrogen (flutamide, bicalutamide: blocks the androgen receptor); -sterone androgen or antagonist (testosterone, spironolactone: steroid; drug sets the effect); -formin biguanide (metformin: lowers insulin).", "S26"),
            F("Recap: **1.** Estrogens and progestins are always paired in a patient with a uterus — unopposed estrogen significantly raises endometrial cancer risk (Chapter 40).", "S27"),
            F("**2.** SERMs and aromatase inhibitors are two distinct strategies for reducing estrogen signaling in hormone-sensitive breast cancer — tissue-selective receptor modulation (Figure 3) vs. blocking peripheral synthesis (Figure 5), compared in Figure 4.", "S27"),
            F("**3.** Finasteride and dutasteride appear here for hirsutism and alopecia — the same drugs return in Session 2 for BPH. **4.** PCOS: insulin resistance and hyperandrogenism reinforce one another (Figure 7), so metformin and hormonal therapy are frequently combined.", "S27; S27 (notes)"),
            F("**5.** Session 2 (Tuesday, December 1) shifts to autonomic pharmacology of the bladder and lower urinary tract — mechanistically different, but sharing cross-system drug-class connections with Units 5 and 6.", "S27; S27 (notes)"),
        ],
    },
    "figures": [
        {"image": "S21_1.jpg", "title": "Figure 7 · The PCOS–insulin resistance cycle", "src": "S21; S21 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): hyperinsulinemia raises free testosterone (ovarian androgens up, SHBG down) and hyperandrogenism worsens insulin resistance — a self-sustaining cycle that metformin interrupts.",
         "viz": path([N("ir", "Insulin resistance,\nhigh insulin", "signal", 10, 20, 170, "amber"), N("ov", "Ovarian androgens ↑,\nSHBG ↓", "cell", 330, 20, 180, "coral"),
                      N("ft", "Free testosterone ↑:\nhirsutism, anovulation", "effect", 330, 140, 200, "deep"), N("back", "Worsens insulin\nresistance", "signal", 10, 140, 170, "blue")],
                     [["ir", "ov"], ["ov", "ft"], ["ft", "back"], ["back", "ir"]],
                     [Dg("Metformin", "ir", "Lowers insulin → androgens fall; ovulation can return (S22–S23).", less=["ir", "ov", "ft"]),
                      Dg("Combined contraception", "ft", "Direct cycle and hirsutism control (S22; S25).", less=["ft"]),
                      Dg("Spironolactone", "ft", "Androgen receptor block for hirsutism/acne (S15; S24).", less=["ft"])],
                     "Two arrows, one cycle — hit both.", h=230)},
        {"image": "S23_1.png", "title": "Figure 8 · Metformin in PCOS: insulin, androgens and ovulation", "src": "S23; S23 (notes)",
         "caption": "Schematic (illustrative) — Figure 8. Insulin, androgens and ovulation in PCOS, and where metformin acts in the loop: lower insulin → lower androgens → cycles and ovulation can return.",
         "viz": path([N("i", "High insulin", "signal", 10, 55, 120, "amber"), N("a", "Ovarian androgens ↑\nSHBG ↓", "cell", 150, 55, 160, "coral"),
                      N("f", "Free testosterone ↑", "molecule", 330, 55, 150, "deep"), N("o", "Ovulation\nreturns", "effect", 500, 55, 130, "sage")],
                     [["i", "a"], ["a", "f"]],
                     [Dg("Metformin", "i", "GI upset (take with meals); hold for contrast or renal impairment (S23).", less=["i", "a", "f"])],
                     "Lower the insulin, lower the androgens.")},
    ],
    "comparisons": [
        {"title": "Table 1 · Agents used in PCOS management at a glance", "columns": ["Agent", "Primary goal", "Key teaching point"],
         "rows": [["Combined hormonal contraception", "Cycle regulation, hirsutism/acne", "Progestin component opposes unopposed-estrogen endometrial risk"],
                  ["Metformin", "Insulin sensitization", "First-line metabolic therapy; can restore ovulation; GI upset common"],
                  ["Spironolactone", "Antiandrogen effect on hirsutism/acne", "Androgen receptor blockade; avoid in pregnancy (teratogenic risk)"],
                  ["GLP-1 receptor agonists", "Weight loss, insulin sensitization", "Emerging off-label use in PCOS with obesity"]],
         "src": "S24; S24 (notes)"},
        {"title": "Supporting drugs at a glance (S45)", "columns": ["Drug(s)", "Why it matters here"],
         "rows": [["**Enzyme inducers**", "Rifampin, carbamazepine, phenytoin and St. John's wort lower combined contraceptive efficacy"],
                  ["**Warfarin**", "Testosterone and tamoxifen raise INR"],
                  ["**GnRH agonists**", "Leuprolide is used with antiandrogens in prostate cancer"],
                  ["**GLP-1 receptor agonists**", "Off-label for PCOS with obesity"],
                  ["**Clomiphene and letrozole**", "Ovulation induction, beyond this lecture"],
                  ["**Bisphosphonates and calcium with vitamin D**", "Bone protection with aromatase inhibitors"],
                  ["**CYP2D6 inhibitors**", "Paroxetine and fluoxetine blunt tamoxifen activation"],
                  ["**ACE inhibitors, ARBs and potassium**", "Hyperkalemia with spironolactone"]],
         "src": "S45; S45 (notes)"},
        *tab((44,), "Metformin profile"),
    ],
    "hooks": [
        {"kind": "why", "text": "Why does a diabetes drug help hirsutism? Insulin drives the ovary to make androgens and the liver to make less SHBG; lower the insulin and free testosterone falls.", "src": "S20; S23"},
    ],
    "high_yield": [
        F("PCOS = insulin resistance ↔ hyperandrogenism cycle; metformin (metabolic) + combined contraception (cycles, hirsutism) are usually combined.", "S21; S22; S25"),
    ],
    "questions": [
        Q("vignette", "A 24-year-old with PCOS (irregular cycles, hirsutism, BMI 31) does not want pregnancy and can take estrogen. Best plan?",
          "Combined contraception plus metformin",
          "Contraception for immediate symptom control and metformin for the metabolic driver — frequently combined (S25).",
          [("Metformin alone, never hormones", "Usually combined (S25)."),
           ("Clomiphene to induce ovulation", "She is not trying to conceive (S45)."),
           ("Estradiol alone for cycles", "Unopposed estrogen (S6)."),
           ("Letrozole for hirsutism", "Ovulation induction only (S45).")], "S22; S25", from_slides="S25"),
        Q("mechanism", "How does metformin improve hirsutism and ovulation in PCOS?",
          "Lowers insulin, so ovarian androgens fall",
          "Metformin reduces hyperinsulinemia’s stimulation of ovarian androgens and raises SHBG — indirect, not hormonal (S22–S23).",
          [("It blocks the androgen receptor", "Spironolactone (S15)."),
           ("It blocks 5-alpha-reductase", "Finasteride (S16)."),
           ("It suppresses FSH and LH directly", "Combined contraception (S9)."),
           ("It blocks aromatase in fat", "Anastrozole (S14).")], "S22; S23"),
        Q("mechanism", "In PCOS, how does hyperinsulinemia raise free testosterone?",
          "More ovarian androgen and less SHBG",
          "Hyperinsulinemia stimulates theca-cell androgen production and lowers hepatic SHBG (S20).",
          [("It activates 5-alpha-reductase in skin", "Not the taught mechanism (S20)."),
           ("It blocks aromatase in the ovary", "Not the mechanism (S20)."),
           ("It raises SHBG, freeing testosterone", "SHBG falls (S20)."),
           ("It suppresses LH release entirely", "Not the mechanism (S20).")], "S20; SG U6-R9"),
        Q("vignette", "A woman with PCOS on spironolactone for hirsutism plans pregnancy. What is the key counseling point?",
          "Stop it — teratogenic in pregnancy",
          "Spironolactone: avoid in pregnancy (teratogenic risk; feminization of a male fetus) (S24; S39).",
          [("Continue; it is safe in pregnancy", "Avoid (S24)."),
           ("Double it to improve fertility", "Not the advice (S24)."),
           ("Add potassium supplements", "Hyperkalemia risk (S45)."),
           ("Switch to testosterone", "Wrong direction (S15).")], "S24; S39"),
    ],
}

content = {
    "lecture": {"id": "L11", "title": "Genitourinary & Reproductive Pharmacology — Session 1", "date": "Tue, Nov 24, 2026"},
    "textbook_status": "included",
    "objectives": objectives,
    "about": about,
    "classes": [t1, t2, t3],
    "notebooklm": {
        "patient": "a 52-year-old on tamoxifen with new vaginal bleeding, and a 24-year-old with PCOS, hirsutism and irregular cycles (the lecture’s cases)",
        "suggested_questions": [
            "Why must a woman with a uterus get a progestin with estrogen?",
            "Who should get a progestin-only method instead of a combined one?",
            "Compare tamoxifen and raloxifene tissue by tissue.",
            "Why are aromatase inhibitors postmenopausal drugs?",
            "Where do finasteride, spironolactone and bicalutamide act on the androgen pathway?",
            "Explain the PCOS–insulin resistance cycle and why metformin helps.",
        ],
    },
    "audit_skip": [
        {"ref": "S1", "starts_with": "Diane", "reason": "instructor name (no names on the site)"},
        {"ref": "S3", "starts_with": "AccessMedicine", "reason": "access link for the textbook"},
        *[{"ref": r, "starts_with": "Section transition", "reason": "section divider"} for r in ("S4", "S10", "S19")],
        {"ref": "S6", "starts_with": "Progestins oppose", "reason": "presenter script; taught from S6"},
        {"ref": "S7", "starts_with": "Explain that the progestin", "reason": "teaching instruction"},
        {"ref": "S8", "starts_with": "Spend real time", "reason": "teaching instruction"},
        {"ref": "S8", "starts_with": "Name the points", "reason": "teaching instruction; the points are the Figure 2 interactive"},
        {"ref": "S9", "starts_with": "Use this slide", "reason": "teaching instruction; the point is taught from S9"},
        {"ref": "S11", "starts_with": "Tamoxifen antagonizes breast, agonizes bone and endometrium. Raloxifene", "reason": "presenter script; taught from S11"},
        {"ref": "S12", "starts_with": "Tamoxifen's endometrial agonism", "reason": "presenter script; taught from S12"},
        {"ref": "S13", "starts_with": "Emphasize the postmenopausal", "reason": "teaching instruction; the caveat is taught from S14"},
        {"ref": "S14", "starts_with": "Anastrozole and letrozole block", "reason": "presenter script; taught from S14"},
        {"ref": "S16", "starts_with": "Anchor each drug", "reason": "teaching instruction"},
        {"ref": "S16", "starts_with": "Finasteride and dutasteride block the enzyme;", "reason": "presenter script; taught from S16"},
        {"ref": "S17", "starts_with": "Use this slide", "reason": "teaching instruction"},
        {"ref": "S18", "starts_with": "This case makes", "reason": "teaching instruction"},
        {"ref": "S18", "starts_with": "New bleeding on tamoxifen", "reason": "presenter script; taught from S18"},
        {"ref": "S20", "starts_with": "This is the thesis slide", "reason": "teaching instruction"},
        {"ref": "S21", "starts_with": "This figure is the mechanistic payoff", "reason": "teaching instruction"},
        {"ref": "S22", "starts_with": "Reinforce the Unit 5", "reason": "teaching instruction; the callback is taught from S22"},
        {"ref": "S22", "starts_with": "Metformin is first-line metabolic therapy", "reason": "presenter script; taught from S22"},
        {"ref": "S23", "starts_with": "Explain that metformin", "reason": "teaching instruction"},
        {"ref": "S24", "starts_with": "Use this table", "reason": "teaching instruction"},
        {"ref": "S25", "starts_with": "Use this case", "reason": "teaching instruction"},
        {"ref": "S27", "starts_with": "Close Session 1", "reason": "teaching instruction"},
        {"ref": "S27", "starts_with": "Preview Session 2", "reason": "teaching instruction"},
        {"ref": "S28", "starts_with": "Appendix talk track", "reason": "teaching instruction"},
        {"ref": "S28", "starts_with": "Class activity", "reason": "teaching instruction"},
        {"ref": "S28", "starts_with": "Abbreviation key: Review", "reason": "teaching instruction"},
        {"ref": "S28", "starts_with": "Teaching points", "reason": "teaching instruction; the drugs are in the profiles"},
        *[{"ref": "S28", "starts_with": w, "reason": "Bloom's teaching prompt; rebuilt as practice questions"} for w in ("Bloom", "Understand", "Apply", "Analyze", "Evaluate")],
        {"ref": "S45", "starts_with": "Supporting drugs:", "reason": "presenter script; the table covers it"},
        {"ref": "S46", "starts_with": "This slide documents", "reason": "administrative note on AI-tool citation"},
        {"ref": "S46", "starts_with": "The original Claude-generated", "reason": "administrative note on AI-tool citation"},
    ],
}

for _cl in content["classes"]:
    for _fg in _cl.get("figures", []):
        if not _fg["viz"].get("title"):
            _fg["viz"]["title"] = _fg["title"].split("·", 1)[-1].strip()

sys.path.insert(0, str(Path(__file__).parent))
import guide_L11 as G  # noqa: E402
content["guide"] = {"summary": [{"text": t, "src": s} for t, s in G.SUMMARY], "teaser": getattr(G, "TEASER", ""),
                    "cram": [{"prompt": p, "answer": a, "src": s} for p, a, s in G.CRAM], "discrepancies": []}
for _cl in content["classes"]:
    _cl["flows"] = G.FLOWS.get(_cl["name"], [])

import textbook_L11 as TBK  # noqa: E402
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
