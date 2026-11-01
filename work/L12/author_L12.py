"""Authoring source for L12 content.json. Run: python3 author_L12.py"""
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


PROF = {p["slide"]: p for p in PR.read("L12")}


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
    {"id": "SO1", "src": "S2", "text": "Describe the autonomic and somatic innervation of the bladder and lower urinary tract, and the receptor subtypes governing storage versus voiding."},
    {"id": "SO2", "src": "S2", "text": "Describe the mechanism, indications, and adverse effects of antimuscarinic agents and beta-3 agonists in overactive bladder and urinary incontinence."},
    {"id": "SO3", "src": "S2", "text": "Describe the mechanism and adverse effects of alpha1 blockers and 5-alpha-reductase inhibitors in benign prostatic hyperplasia (BPH)."},
    {"id": "SO4", "src": "S2", "text": "Describe non-adrenergic, noncholinergic (NANC) neurotransmission and the NO-cGMP pathway underlying erectile function and PDE5 inhibitor pharmacology, including the absolute nitrate contraindication."},
    {"id": "SO5", "src": "S2", "text": "Integrate autonomic receptor pharmacology across the genitourinary and cardiovascular systems, and apply the full Unit 6 toolkit to integrated clinical scenarios with a cumulative recall quiz."},
]

about = [
    F("**PA PHARMACOLOGY COURSE · LECTURE 6 · SESSION 2 OF 2** — Genitourinary & Reproductive Pharmacology. **Session 2: Autonomic Pharmacology of the Bladder and Lower Urinary Tract  |  Tuesday, December 1  |  8:30–11:00 AM**", "S1"),
    F("Recap: Session 1 covered gonadal steroid pharmacology (estrogens, progestins, SERMs, aromatase inhibitors, androgens/antiandrogens) and the PCOS reproductive-metabolic overlap.", "S2"),
    F("Today is autonomic pharmacology — mechanistically distinct from steroid hormones; the connective tissue between sessions is mostly the finasteride/dutasteride callback and the shared organ system. Three nerve supplies, three receptor families, and every drug maps to one receptor at one location.", "S2 (notes)"),
    F("**APPENDIX 1** — **Formulation, dose, indications, adverse effects, contraindications and toxicity** — your study reference: know the dose logic, the serious adverse effects, the contraindication that changes decisions and the toxicity you would need to recognize.", "S35; S35 (notes); S36-49"),
    F("**PO = by mouth** **TID = three times daily** **IR / ER = immediate-release / extended-release** **BPH = benign prostatic hyperplasia** **PSA = prostate-specific antigen** **ED = erectile dysfunction** **PAH = pulmonary arterial hypertension** **OAB = overactive bladder** **CNS = central nervous system**", "S35"),
    F("**QT = QT interval on ECG** **CYP = cytochrome P450** **eGFR / CrCl = estimated glomerular filtration rate / creatinine clearance** **PDE5 = phosphodiesterase type 5** **GnRH = gonadotropin-releasing hormone** **BP = blood pressure** **GI = gastrointestinal** **ECG = electrocardiogram** **NO / cGMP = nitric oxide / cyclic guanosine monophosphate**", "S35"),
    F("**Standard adult dosing for teaching; verify against current prescribing information.**", "S36-49"),
    F("**Appendix 2: DRUG PROFILE · SUPPORTING** — supporting drugs explain interactions. **Listed for context; not profiled in detail.**", "S50; S50 (notes)"),
    F("**Original figures in this deck:** Figures 9, 12, 13, 15 and 18 (Autonomic & Somatic Receptors of the Lower Urinary Tract; Antimuscarinics vs. Beta-3 Agonists: Two Mechanisms for Bladder Storage; Alpha1 Blockade at the Bladder Neck and Prostate;", "S51"),
    F("NANC Neurotransmission and the NO-cGMP Pathway in Erectile Function; Autonomic Receptor Map Across the Genitourinary Tract) were generated by the course director using the AI tool Claude — original diagrams, not reproduced from Katzung or any other copyrighted source.", "S51; S51 (notes)"),
    F("**Mechanism illustrations:** Figures 10, 11, 14, 16 and 17 are illustrative AI-generated schematics, not reproduced from copyrighted sources. **Reference:** Anthropic. (2026). Claude (Sonnet 5) [Large language model]. https://claude.ai", "S51"),
]

# ---------------------------------------------------------------- Part 1: autonomic control
t1 = {
    "name": "Autonomic Control of the Lower Urinary Tract", "template": "drug_class", "objectives": ["SO1", "IO6.1"],
    "sections": {
        "overview": [
            F("**Three nerve supplies, three receptor families — the physiologic foundation for every drug in this session.**", "S3"),
            F("Parasympathetic M3 contracts the detrusor, sympathetic alpha-1 closes the bladder neck and beta-3 relaxes the reservoir, and somatic nicotinic control holds the external sphincter.", "S3 (notes); S4 (notes)"),
            F("**Figure 9. Original illustrative diagram (not from Katzung): the parasympathetic, sympathetic, and somatic nervous systems each innervate a different structure of the lower urinary tract through a distinct receptor family —**", "S4"),
            F("**the organizing map for every drug class covered this session.** Every class is anchored back to its receptor and anatomic location; Sections 5 and 6 \"zoom in\" on parts of this map.", "S4; S4 (notes)"),
        ],
        "prototype": [
            F("Oxybutynin (blocks M3 on the detrusor), tamsulosin (blocks alpha1 at the bladder neck/prostate) and mirabegron (stimulates beta3 on the detrusor body) each target one receptor of this map.", "S4; S5; S7"),
        ],
        "moa": [
            F("**The parasympathetic pelvic nerve releases acetylcholine, which acts on M3 muscarinic receptors on the detrusor muscle to produce contraction — the primary driver of bladder emptying (voiding).**", "S5; SG U6-R11"),
            F("M3 is the dominant muscarinic subtype in the bladder, though M2 receptors are also present in high density (smaller functional contribution normally, may increase in disease).", "S5; S5 (notes)"),
            F("Chain (Figure 10): pelvic nerve releases acetylcholine → ACh binds M3 on the detrusor → Gq activates phospholipase C; calcium rises → detrusor contracts and the bladder empties.", "S6; S6 (notes)"),
            F("**M3 is the dominant bladder muscarinic subtype.** **M2 is more abundant but contributes less to contraction.** **Blocking M3 underlies antimuscarinic OAB treatment.**", "S6"),
            F("**The sympathetic hypogastric nerve releases norepinephrine, which acts on two different adrenergic receptor subtypes in two different locations, producing two different (and complementary) effects.**", "S7; S7 (notes)"),
            F("Chain (Figure 11): sympathetic hypogastric nerve releases norepinephrine → alpha-1: outlet closed; beta-3: reservoir relaxed → continence maintained during storage.", "S8"),
            F("Alpha1 receptors at the bladder neck, trigone, and proximal urethra: norepinephrine causes contraction, helping maintain continence during storage.", "S7; S8; SG U6-R11"),
            F("Beta3 receptors on the detrusor body: norepinephrine causes relaxation, allowing the bladder to fill without a premature urge to void (low pressure).", "S7; S8; SG U6-R11"),
        ],
        "indications": [
            F("**Because M3 blockade reduces detrusor contraction, antimuscarinic drugs (Section 5) are a logical treatment for conditions of bladder overactivity.**", "S5"),
            F("**Both of these receptor subtypes become specific drug targets later in this session: alpha1 blockers for BPH (Section 6), and beta3 agonists for overactive bladder (Section 5).**", "S7"),
        ],
        "adverse": [],
        "contra": [],
        "interactions": [],
        "pk": [],
        "monitoring": [],
        "pearls": [
            F("Net storage effect: sympathetic tone keeps the outlet closed (alpha1) while keeping the reservoir relaxed (beta3) — parasympathetic tone is low; both arms work together for continence. During voiding, this pattern reverses.", "S7; S8; S8 (notes)"),
            F("This is applied Chapter 6: the same muscarinic family that governs other smooth muscle and glands throughout the body — the bladder is simply one more target organ.", "S5; S5 (notes)"),
            F("Know which receptor does what where (alpha1 at the outlet vs. beta3 on the detrusor body) before moving on — it makes the rest of the session’s pharmacology make sense.", "S7 (notes)"),
        ],
    },
    "figures": [
        {"image": "S4_1.jpg", "title": "Figure 9 · Autonomic and somatic receptors of the lower urinary tract", "src": "S4; S4 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): parasympathetic M3 (detrusor contraction), sympathetic alpha1 (bladder neck closure) and beta3 (detrusor relaxation), somatic nicotinic (external sphincter) — the map for every drug in the session.",
         "viz": path([N("ps", "Parasympathetic\n(pelvic): ACh", "signal", 10, 10, 160, "blue"), N("sy", "Sympathetic\n(hypogastric): NE", "signal", 10, 120, 160, "amber"),
                      N("m3", "M3 on detrusor:\ncontract (void)", "membrane", 230, 10, 170, "teal"), N("a1", "Alpha1 at neck:\nclose outlet", "membrane", 230, 100, 170, "coral"),
                      N("b3", "Beta3 on detrusor:\nrelax (store)", "membrane", 230, 190, 170, "sage"), N("so", "Somatic nicotinic:\nexternal sphincter", "membrane", 450, 100, 170, "deep")],
                     [["ps", "m3"], ["sy", "a1"], ["sy", "b3"]],
                     [Dg("Oxybutynin", "m3", "Blocks M3 — OAB (S11).", off=["m3"]), Dg("Tamsulosin", "a1", "Blocks alpha1 — BPH (S17).", off=["a1"]),
                      Dg("Mirabegron", "b3", "Stimulates beta3 — OAB (S13).")],
                     "One receptor, one location, one drug class.", h=270)},
        {"image": "S6_1.png", "title": "Figure 10 · M3 signaling and detrusor contraction", "src": "S6; S6 (notes)",
         "caption": "**Schematic (illustrative)** — Figure 10. Acetylcholine acting on M3 receptors (Gq → phospholipase C → calcium) drives detrusor contraction and bladder emptying.",
         "viz": path([N("ach", "ACh released", "molecule", 10, 55, 120, "blue"), N("m3", "M3 receptor", "membrane", 150, 55, 120, "teal"),
                      N("gq", "Gq → PLC →\ncalcium ↑", "signal", 290, 55, 140, "amber"), N("c", "Detrusor\ncontracts", "effect", 450, 55, 160, "coral")],
                     [["ach", "m3"], ["m3", "gq"], ["gq", "c"]],
                     [Dg("Antimuscarinic (solifenacin)", "m3", "Fewer involuntary contractions (S11).", off=["gq", "c"])],
                     "Block M3, calm the detrusor.")},
        {"image": "S8_1.png", "title": "Figure 11 · Alpha-1 vs. beta-3: outlet closed, reservoir relaxed", "src": "S8; S8 (notes)",
         "caption": "Schematic (illustrative) — Figure 11. Alpha-1 contraction closes the outlet while beta-3 relaxation lets the bladder store urine — together, continence during storage.",
         "viz": path([N("ne", "Norepinephrine", "molecule", 10, 95, 140, "amber"), N("a1", "Alpha1: outlet\nclosed", "membrane", 220, 20, 150, "coral"),
                      N("b3", "Beta3: reservoir\nrelaxed", "membrane", 220, 170, 150, "sage"), N("st", "Continence\nduring storage", "effect", 450, 95, 160, "teal")],
                     [["ne", "a1"], ["ne", "b3"], ["a1", "st"], ["b3", "st"]],
                     [Dg("Mirabegron", "b3", "Enhances relaxation (S13)."), Dg("Tamsulosin", "a1", "Opens the outlet in BPH (S17).", off=["a1"])],
                     "Two receptors, one storage phase.", h=250)},
    ],
    "comparisons": [
        {"title": "Storage phase vs. voiding phase (S9)", "columns": ["", "Storage phase", "Voiding phase"],
         "rows": [["Dominant tone", "Sympathetic", "Parasympathetic"],
                  ["Detrusor", "Beta3 agonism relaxes the detrusor body", "M3 agonism contracts the detrusor body"],
                  ["Bladder neck", "Alpha1 agonism contracts the bladder neck/urethra", "Sympathetic tone withdraws, bladder neck relaxes"],
                  ["External sphincter", "Somatic (pudendal) tone keeps it closed", "Voluntary relaxation (somatic)"]],
         "src": "S9; S9 (notes)"},
    ],
    "hooks": [
        {"kind": "mnemonic", "text": "Store with the Sympathetic (alpha1 shuts the door, beta3 relaxes the tank); Pee with the Parasympathetic (M3 squeezes).", "src": "S9"},
    ],
    "high_yield": [
        F("M3 (detrusor) contracts to void; alpha1 (neck) closes and beta3 (detrusor) relaxes to store.", "S5; S7; SG U6-R11"),
    ],
    "questions": [
        Q("mechanism", "Which receptor on the detrusor body relaxes the bladder during filling?",
          "Beta3 adrenergic receptor",
          "Norepinephrine at beta3 on the detrusor body causes relaxation during storage (S7).",
          [("M3 muscarinic receptor", "Contracts the detrusor (S5)."),
           ("Alpha1 adrenergic receptor", "Contracts the bladder neck (S7)."),
           ("Nicotinic receptor", "External sphincter (S9)."),
           ("M2 muscarinic receptor", "Smaller contraction role (S5).")], "S7; S8; SG U6-R11"),
        Q("mechanism", "During the storage phase, which pattern of autonomic tone is correct?",
          "Sympathetic dominates; outlet closed",
          "Sympathetic tone keeps the outlet closed (alpha1) and reservoir relaxed (beta3); parasympathetic tone is low (S7; S9).",
          [("Parasympathetic dominates; detrusor contracts", "That is voiding (S9)."),
           ("Both systems are silent during storage", "Sympathetic dominates (S9)."),
           ("Sympathetic contracts the detrusor body", "Beta3 relaxes it (S7)."),
           ("Somatic tone opens the external sphincter", "It keeps it closed (S9).")], "S7; S9"),
    ],
}

# ---------------------------------------------------------------- Part 2: OAB
t2 = {
    "name": "Overactive Bladder Drugs", "template": "drug_class", "objectives": ["SO2", "IO6.1", "IO6.2", "IO6.3", "IO6.4", "IO6.6"],
    "sections": {
        "overview": [
            F("**Two mechanisms, one goal — calming an overactive detrusor to improve storage and reduce urgency.** Antimuscarinics block the detrusor’s muscarinic signal, while beta-3 agonists relax it.", "S10; S10 (notes)"),
            F("**Figure 12. Original illustrative diagram (not from Katzung): antimuscarinics block the M3-mediated contraction signal, while beta3 agonists enhance the norepinephrine-mediated relaxation signal —**", "S14"),
            F("**two distinct mechanisms converging on the same clinical goal of improved bladder storage.** Complementary, not competing — the basis for combination therapy.", "S14; S14 (notes)"),
        ],
        "prototype": [
            F("Oxybutynin, tolterodine, solifenacin, darifenacin (antimuscarinics); mirabegron (beta3 agonist).", "S11; S13"),
        ],
        "moa": [
            F("**Mechanism: block M3 (and, to a lesser extent, M2) muscarinic receptors on the detrusor, reducing involuntary contractions and increasing functional bladder capacity.**", "S11; SG U6-R12"),
            F("Antimuscarinic agents differ mainly in receptor selectivity and anticholinergic side-effect burden rather than core mechanism.", "S11"),
            F("Chain (Figure 13): drug blocks M3 receptors on the detrusor → fewer involuntary contractions, larger capacity → same blockade in brain, salivary gland and bowel → bladder relaxes, but dry mouth, constipation and confusion follow.", "S12; S12 (notes)"),
            F("Oxybutynin has the highest CNS anticholinergic burden; mirabegron, a beta-3 agonist, avoids this anticholinergic burden.", "S12"),
            F("**Mechanism: stimulate beta3 adrenergic receptors on the detrusor, enhancing smooth muscle relaxation during the storage/filling phase.** Mirabegron is the primary beta3 agonist in clinical use for overactive bladder.", "S13; SG U6-R13"),
        ],
        "indications": [
            F("**Key advantage: lacks the systemic anticholinergic burden of antimuscarinics, making it a preferred option in older adults or patients already on multiple anticholinergic medications.**", "S13; SG U6-R13"),
            F("Mirabegron can be used alone or combined with an antimuscarinic for refractory symptoms — complementary (not redundant) mechanisms.", "S13; S14 (notes)"),
        ],
        "adverse": [
            F("**Adverse effects follow directly from systemic antimuscarinic blockade: dry mouth, constipation, blurred vision, and — importantly — cognitive impairment and confusion, especially in older adults.**", "S11; S11 (notes)"),
            F("Anticholinergic burden is cumulative across all of a patient’s medications — oxybutynin has the highest CNS anticholinergic burden of this class and is often avoided in older adults or those with dementia risk.", "S11; S12; SG U6-R12"),
            F("Mirabegron: can raise blood pressure (monitor in uncontrolled hypertension); headache or nasopharyngitis; less commonly, urinary retention.", "S13"),
        ],
        "contra": [
            F("Antimuscarinics: caution/contraindication in narrow-angle glaucoma and significant urinary retention.", "S11"),
        ],
        "interactions": [
            F("Mirabegron inhibits CYP2D6. Other anticholinergics (diphenhydramine, tricyclic antidepressants) add to anticholinergic burden; cholinesterase inhibitors (donepezil) oppose antimuscarinics.", "S13 (notes); S50; S50 (notes)"),
            F("Strong CYP3A4 inhibitors (ketoconazole, clarithromycin) raise solifenacin levels.", "S50; S50 (notes)"),
        ],
        "pk": [],
        "monitoring": [],
        "pearls": [
            F("Case: a 78-year-old with mild cognitive impairment and urge incontinence starts oxybutynin; three weeks later, worsening confusion and new difficulty with daily tasks. **What is the most likely explanation, and what change in therapy would you consider?**", "S15"),
            F("**Oxybutynin carries a relatively high CNS anticholinergic burden, and in an older adult — especially one with pre-existing cognitive impairment — this can precipitate or worsen confusion.**", "S15"),
            F("**Switching to a beta3 agonist (mirabegron), which lacks anticholinergic activity, treats the same overactive bladder symptoms without this risk.** Review other anticholinergics too (medication reconciliation).", "S15; S15 (notes)"),
            F("The anticholinergic-burden-in-older-adults point is the highest-yield safety point in this section; \"no anticholinergic burden\" is mirabegron’s single most important advantage.", "S11 (notes); S13 (notes)"),
        ],
    },
    "figures": [
        {"image": "S12_1.png", "title": "Figure 13 · Antimuscarinics: bladder benefit and anticholinergic burden", "src": "S12; S12 (notes)",
         "caption": "**Schematic (illustrative)** — Antimuscarinics relax the bladder but block the same receptors throughout the body (brain, salivary glands, gut): dry mouth, constipation and confusion. (The slide labels this “Figure 93”.)",
         "viz": path([N("m3", "M3 block in\ndetrusor", "membrane", 10, 20, 140, "teal"), N("b", "Fewer contractions,\nlarger capacity", "effect", 180, 20, 170, "sage"),
                      N("cns", "Brain: confusion", "cell", 180, 110, 170, "coral"), N("sal", "Mouth, gut:\ndry, constipated", "cell", 180, 190, 170, "amber")],
                     [["m3", "b"], ["m3", "cns"], ["m3", "sal"]],
                     [Dg("Oxybutynin", "m3", "Highest CNS burden (S11–S12)."), Dg("Mirabegron", "b", "Same goal, no anticholinergic burden (S12–S13).", off=["cns", "sal"])],
                     "The bladder benefit comes with body-wide blockade.", h=260)},
        {"image": "S14_1.jpg", "title": "Figure 12 · Antimuscarinics vs. beta-3 agonists", "src": "S14; S14 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): antimuscarinics block the M3 contraction signal; beta3 agonists enhance the relaxation signal — complementary mechanisms for better storage.",
         "viz": path([N("con", "M3 contraction\nsignal", "signal", 10, 20, 150, "coral"), N("rel", "Beta3 relaxation\nsignal", "signal", 10, 130, 150, "sage"),
                      N("st", "Better storage,\nless urgency", "effect", 400, 75, 170, "teal")],
                     [["con", "st"], ["rel", "st"]],
                     [Dg("Solifenacin / oxybutynin", "con", "Block contraction (S11).", off=["con"]), Dg("Mirabegron", "rel", "Enhance relaxation (S13).")],
                     "Two levers, same goal — they can be combined.", h=220)},
    ],
    "comparisons": [
        {"title": "Antimuscarinics vs. mirabegron (S11; S13)", "columns": ["", "Antimuscarinics", "Mirabegron (beta3 agonist)"],
         "rows": [["Mechanism", "Block M3 (and M2) on the detrusor", "Stimulate beta3 on the detrusor"],
                  ["Adverse effects", "Dry mouth, constipation, blurred vision, confusion", "Raises BP; headache, nasopharyngitis"],
                  ["Older adults", "Avoid oxybutynin (highest CNS burden)", "Preferred — no anticholinergic burden"],
                  ["Cautions", "Narrow-angle glaucoma, urinary retention", "Uncontrolled hypertension; CYP2D6 inhibitor"]],
         "src": "S11; S13"},
        *tab((36, 37, 38, 39, 40), "Overactive bladder drug profiles"),
    ],
    "hooks": [
        {"kind": "why", "text": "Why does oxybutynin confuse an older adult? It blocks muscarinic receptors in the brain too, and anticholinergic burden adds up across every drug she takes.", "src": "S11; S12; S15"},
    ],
    "high_yield": [
        F("OAB in an older adult or anyone on other anticholinergics → mirabegron; oxybutynin has the highest CNS burden.", "S11; S13; S15"),
    ],
    "questions": [
        Q("vignette", "A 78-year-old with mild cognitive impairment becomes more confused 3 weeks after starting oxybutynin. Best change?",
          "Switch to mirabegron (beta3 agonist)",
          "Oxybutynin’s CNS anticholinergic burden worsens confusion; mirabegron treats OAB without it (S15).",
          [("Increase oxybutynin for better control", "Worsens burden (S15)."),
           ("Add a second antimuscarinic", "Adds burden (S33)."),
           ("Add donepezil and keep oxybutynin", "Opposes antimuscarinics (S50)."),
           ("Confusion is unrelated; continue", "It is related (S15).")], "S15; S34", from_slides="S15; S33; S34"),
        Q("mechanism", "How does mirabegron improve overactive bladder?",
          "Stimulates beta3 to relax the detrusor",
          "Mirabegron enhances beta3-mediated detrusor relaxation without blocking muscarinic receptors (S13; S34).",
          [("Blocks M3 on the detrusor", "That is antimuscarinics (S11)."),
           ("Blocks alpha1 at the bladder neck", "That is tamsulosin (S17)."),
           ("Lowers DHT to shrink the prostate", "That is finasteride (S19)."),
           ("Raises cGMP in smooth muscle", "That is PDE5 inhibitors (S22).")], "S13; S34"),
        Q("vignette", "A patient with uncontrolled hypertension needs OAB therapy. What concern applies to mirabegron?",
          "It can raise blood pressure",
          "Mirabegron can raise blood pressure; monitor in uncontrolled hypertension (S13; S40).",
          [("It causes severe confusion", "Antimuscarinics (S11)."),
           ("It causes first-dose hypotension", "Alpha1 blockers (S17)."),
           ("It lowers PSA by half", "5-ARIs (S19)."),
           ("It worsens narrow-angle glaucoma", "Antimuscarinics (S11).")], "S13; S40"),
    ],
}

# ---------------------------------------------------------------- Part 3: BPH, ED, PDE5
t3 = {
    "name": "BPH, Erectile Dysfunction & PDE5 Inhibitors", "template": "drug_class", "objectives": ["SO3", "SO4", "IO6.1", "IO6.2", "IO6.3", "IO6.4", "IO6.5", "IO6.6"],
    "sections": {
        "overview": [
            F("**Where genitourinary pharmacology meets the cardiovascular system — alpha1 blockade, nitric oxide signaling, and a life-threatening drug interaction.** Alpha1 blockers relax the prostate; nitric oxide and cGMP drive erection.", "S16; S16 (notes)"),
        ],
        "prototype": [
            F("Tamsulosin, silodosin, doxazosin, terazosin (alpha1 blockers); finasteride, dutasteride (5-ARIs); sildenafil, tadalafil, vardenafil (PDE5 inhibitors).", "S17; S19; S22"),
        ],
        "moa": [
            F("**Mechanism: block alpha1 receptors at the bladder neck, prostatic smooth muscle, and proximal urethra, relaxing outflow resistance and improving urinary flow in benign prostatic hyperplasia.**", "S17"),
            F("**Figure 13. Original illustrative diagram (not from Katzung): sympathetic norepinephrine normally contracts bladder neck and prostatic smooth muscle via alpha1 receptors, narrowing the outflow tract;**", "S18"),
            F("**alpha1 blockers relax this same muscle to improve urinary flow — while the same receptor family elsewhere mediates vascular tone.**", "S18; S18 (notes)"),
            F("**Mechanism: block 5-alpha-reductase, the enzyme that converts testosterone to the more potent dihydrotestosterone (DHT) — the same mechanism introduced in Session 1 for hirsutism and androgenetic alopecia.**", "S19; S19 (notes)"),
            F("5-ARI chain (Figure 14): testosterone is converted by 5-alpha-reductase → the enzyme makes DHT → DHT drives prostate growth → enzyme blocked, DHT falls, prostate shrinks slowly.", "S20; S20 (notes)"),
            F("**Figure 15. Original illustrative diagram (not from Katzung): non-adrenergic, noncholinergic (NANC) nerves release nitric oxide, raising cGMP and relaxing corpus cavernosum smooth muscle;**", "S21"),
            F("**PDE5 normally terminates this signal by breaking down cGMP, and nitrates independently raise NO/cGMP systemically — the mechanistic basis for the absolute nitrate/PDE5-inhibitor contraindication.**", "S21"),
            F("**Mechanism: block phosphodiesterase type 5 (PDE5), the enzyme that normally breaks down cGMP, prolonging smooth muscle relaxation in the corpus cavernosum and sustaining erectile function (Figure 15).**", "S22"),
            F("Chain (Figure 16): sexual stimulation → NANC nerves release nitric oxide → guanylate cyclase makes cGMP → cGMP relaxes corpus cavernosum smooth muscle → erection. PDE5 breaks down cGMP and ends the signal.", "S23"),
            F("Sildenafil, tadalafil and vardenafil block PDE5 and prolong the signal; an erection still needs sexual stimulation to start the pathway.", "S23; S23 (notes)"),
        ],
        "indications": [
            F("Tamsulosin, silodosin (more uroselective, less vascular effect) vs. doxazosin, terazosin (less selective, more likely to lower blood pressure systemically).", "S17; S17 (notes); SG U6-R14"),
            F("Finasteride, dutasteride: in BPH, reducing DHT shrinks prostatic tissue over time, improving urinary symptoms.", "S19"),
            F("Onset: 5-ARI benefit typically takes 3–6 months, unlike the rapid onset of alpha1 blockers — the classes are frequently combined (alpha1 blocker for rapid relief, 5-ARI for long-term disease modification). Alpha1 blockers act in days; 5-ARIs take months.", "S19; S20; SG U6-R15"),
            F("PDE5 agents: sildenafil, tadalafil (longer half-life, allows more flexible dosing), vardenafil.", "S22"),
        ],
        "adverse": [
            F("**Adverse effects: orthostatic hypotension and a \"first-dose effect\" (pronounced hypotension with the first dose) — because alpha1 receptors also mediate vascular smooth muscle tone, not just bladder neck tone.**", "S17; SG U6-R14"),
            F("Floppy iris syndrome is a recognized intraoperative complication during cataract surgery in patients on alpha1 blockers — relevant to preoperative medication reconciliation.", "S17; S17 (notes)"),
            F("**Adverse effects: decreased libido, erectile dysfunction, and — a key counseling point — these agents lower PSA levels by roughly half, which must be accounted for when interpreting PSA values in patients on long-term therapy.**", "S19; S20; SG U6-R15"),
            F("PDE5 common adverse effects: headache, flushing, dyspepsia, and visual disturbances (blue-tinged vision, more notable with sildenafil).", "S22"),
        ],
        "contra": [
            F("**Absolute contraindication: concurrent use with any nitrate — both raise NO/cGMP signaling, and together they can cause profound, life-threatening hypotension.**", "S22"),
            F("Why absolute rather than relative: nitrates and PDE5 inhibitors independently raise NO/cGMP signaling, and together can produce profound, life-threatening hypotension — pharmacodynamic and severe regardless of dose.", "SG U6-R16"),
            F("**This mirrors the identical nitrate/PDE5-inhibitor warning from Unit 5's angina content, now from the opposite side of the interaction.** Riociguat is also contraindicated with PDE5 inhibitors.", "S22; S22 (notes); S50"),
            F("5-ARI pregnancy caution: finasteride/dutasteride can cause ambiguous genitalia in a male fetus; pregnant partners should avoid handling crushed or broken tablets.", "S19; S20"),
        ],
        "interactions": [
            F("Use caution with alpha1 blockers and PDE5 inhibitors together — additive hypotension, less severe than with nitrates, still warrants spacing doses or careful monitoring.", "S22; S25"),
            F("Nitrate + PDE5 inhibitor (Figure 17): nitrate raises NO and cGMP systemically → PDE5 inhibitor stops cGMP breakdown → together, vasodilation becomes profound → severe hypotension and syncope. Never combine.", "S25; S25 (notes)"),
            F("Antihypertensives: additive hypotension with alpha-1 blockers. Strong CYP3A4 inhibitors (ketoconazole, clarithromycin) raise PDE5 inhibitor levels.", "S50; S50 (notes)"),
        ],
        "pk": [],
        "monitoring": [
            F("PSA falls about half on long-term 5-ARI therapy; read PSA accordingly.", "S20"),
        ],
        "pearls": [
            F("**This is the exact same receptor family targeted by alpha1-blocking antihypertensives and central agents discussed in Unit 5 — the difference here is clinical intent (urinary flow vs. blood pressure), not a different drug class.**", "S17; S17 (notes); S18 (notes)"),
            F("Finasteride/dutasteride here are a deliberate callback to Session 1: same mechanism, same drugs, different clinical application.", "S19 (notes)"),
            F("Figure 15 applies the Chapter 6 non-adrenergic, noncholinergic neuron reading; the nitrate warning is the highest-stakes safety point in the unit — students saw it from the nitrate side in Unit 5, today from the PDE5 side.", "S21 (notes); S22 (notes)"),
            F("Case: a 64-year-old with stable angina on isosorbide mononitrate asks for an ED prescription — a friend takes sildenafil \"with no problems.\" Ask yourself: **What should the PA do, and why?**", "S24"),
            F("**PDE5 inhibitors are absolutely contraindicated with any nitrate — both raise NO/cGMP signaling, and the combination can cause severe, life-threatening hypotension.**", "S24"),
            F("**This prescription should not be written while the patient remains on a nitrate; the conversation should include alternative angina management or alternative ED options that do not involve this interaction, in consultation with his cardiologist.**", "S24; S24 (notes)"),
            F("This case pulls a Unit 5 drug (isosorbide mononitrate) into a Unit 6 decision, making the shared NO-cGMP mechanism unmistakable.", "S24 (notes)"),
            F("Drug names reveal the class: **-osin** alpha1 blocker (tamsulosin, doxazosin, terazosin, silodosin; opens the outlet); **-terodine** antimuscarinic (tolterodine, fesoterodine; dampens detrusor M3 signal); **-fenacin** antimuscarinic (solifenacin, darifenacin; same class, same target).", "S26; S26 (notes)"),
            F("**oxybutynin / trospium** antimuscarinic (older, higher CNS burden); **-begron** beta-3 agonist (mirabegron, vibegron; relaxes the reservoir); **-afil** PDE5 inhibitor (sildenafil, tadalafil, vardenafil; keeps cGMP high).", "S26"),
            F("**-steride** 5-alpha-reductase inhibitor (finasteride, dutasteride; lowers DHT, shrinks prostate); **-nitrate / nitro-** nitrate (isosorbide, nitroglycerin; never with a PDE5 inhibitor).", "S26"),
        ],
    },
    "figures": [
        {"image": "S18_1.jpg", "title": "Figure 13 · Alpha1 blockade at the bladder neck and prostate", "src": "S18; S18 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): norepinephrine contracts bladder-neck and prostatic smooth muscle via alpha1, narrowing outflow; alpha1 blockers relax it — and the same receptors in vessels explain orthostatic hypotension.",
         "viz": path([N("ne", "Norepinephrine", "molecule", 10, 95, 130, "amber"), N("pr", "Alpha1 in prostate,\nbladder neck", "membrane", 190, 20, 170, "coral"),
                      N("ve", "Alpha1 in\nblood vessels", "membrane", 190, 170, 170, "blue"), N("fl", "Outflow narrowed", "effect", 420, 20, 160, "deep"),
                      N("bp", "Vascular tone (BP)", "effect", 420, 170, 160, "teal")],
                     [["ne", "pr"], ["ne", "ve"], ["pr", "fl"], ["ve", "bp"]],
                     [Dg("Tamsulosin / silodosin", "pr", "Uroselective; less BP effect (S17).", off=["fl"]),
                      Dg("Doxazosin / terazosin", "pr", "Also lower BP — first-dose effect (S17).", off=["fl", "bp"])],
                     "Same receptor in the prostate and the vessels.", h=250)},
        {"image": "S20_1.jpg", "title": "Figure 14 · 5-ARIs: shrinking the prostate slowly", "src": "S20; S20 (notes)",
         "caption": "**Schematic (illustrative)** — Figure 14. 5-ARIs block DHT production, so the prostate shrinks slowly over months; combine with an alpha1 blocker for fast relief.",
         "viz": {"type": "bars", "title": "BPH drug onset", "yLabel": "Time to symptomatic benefit (days, approximate)",
                 "point": "Alpha1 blockers act in days; 5-ARIs take months — so combine them.",
                 "bars": [{"label": "Alpha1 blocker", "value": 3, "col": "teal", "note": "Days — relaxes smooth muscle."},
                          {"label": "5-ARI", "value": 135, "col": "amber", "note": "3–6 months — shrinks the gland."}],
                 "steps": [{"label": "Alpha1 blocker", "pick": 0}, {"label": "5-alpha-reductase inhibitor", "pick": 1}]}},
        {"image": "S21_1.jpg", "title": "Figure 15 · NANC neurotransmission and the NO-cGMP pathway", "src": "S21; S21 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): NANC nerves release NO → cGMP → corpus cavernosum relaxation; PDE5 breaks cGMP down; nitrates independently raise NO/cGMP — hence the absolute contraindication.",
         "viz": path([N("no", "NANC nerves\nrelease NO", "signal", 10, 55, 130, "blue"), N("gc", "Guanylate\ncyclase → cGMP", "enzyme", 160, 55, 140, "teal"),
                      N("rel", "Smooth muscle\nrelaxes: erection", "effect", 320, 55, 150, "sage"), N("pde", "PDE5 breaks\ncGMP down", "enzyme", 160, 160, 140, "amber"),
                      N("nit", "Nitrate: more NO\nsystemically", "molecule", 10, 160, 130, "coral")],
                     [["no", "gc"], ["gc", "rel"], ["gc", "pde"], ["nit", "gc"]],
                     [Dg("Sildenafil / tadalafil", "pde", "Prolong cGMP — needs sexual stimulation (S22–S23).", off=["pde"]),
                      Dg("Isosorbide mononitrate", "nit", "With a PDE5 inhibitor → life-threatening hypotension (S21–S22).")],
                     "Two ways to raise cGMP — never both.", h=250)},
        {"image": "S23_1.jpg", "title": "Figure 16 · PDE5 inhibitors: NO, cGMP and erection", "src": "S23; S23 (notes)",
         "caption": "**Schematic (illustrative)** — Figure 16. PDE5 inhibitors keep cGMP high, prolonging smooth muscle relaxation; sexual stimulation is still needed to start the pathway.",
         "viz": path([N("s", "Sexual\nstimulation", "signal", 10, 55, 120, "blue"), N("n", "NO released", "molecule", 150, 55, 120, "teal"),
                      N("c", "cGMP ↑", "molecule", 290, 55, 110, "amber"), N("e", "Erection", "effect", 420, 55, 120, "sage")],
                     [["s", "n"], ["n", "c"], ["c", "e"]],
                     [Dg("Tadalafil", "c", "Longer half-life, flexible dosing (S22).")],
                     "No stimulation, no signal to prolong.")},
        {"image": "S25_1.png", "title": "Figure 17 · Nitrate plus PDE5 inhibitor: a double hit on cGMP", "src": "S25; S25 (notes)",
         "caption": "**Schematic (illustrative)** — Figure 17. Nitrates and PDE5 inhibitors both raise cGMP, so vasodilation and hypotension stack — severe hypotension and syncope. Never combine; caution with alpha1 blockers too.",
         "viz": path([N("n", "Nitrate: NO,\ncGMP ↑", "molecule", 10, 55, 130, "coral"), N("p", "PDE5 inhibitor:\ncGMP kept", "enzyme", 160, 55, 140, "amber"),
                      N("v", "Profound\nvasodilation", "effect", 320, 55, 130, "blue"), N("h", "Severe hypotension,\nsyncope", "effect", 470, 55, 160, "deep")],
                     [["n", "v"], ["p", "v"], ["v", "h"]],
                     [Dg("Hold the PDE5 inhibitor", "p", "Absolute contraindication with any nitrate (S25).", off=["p"])],
                     "Both raise cGMP; together, blood pressure collapses.")},
    ],
    "comparisons": [
        {"title": "BPH drug classes (S17; S19)", "columns": ["", "Alpha1 blockers", "5-alpha-reductase inhibitors"],
         "rows": [["Mechanism", "Relax prostate/bladder-neck smooth muscle", "Block testosterone → DHT; shrink the gland"],
                  ["Onset", "Days", "3–6 months"],
                  ["Adverse effects", "Orthostatic hypotension, first-dose effect, floppy iris", "Decreased libido, ED; PSA halved"],
                  ["Use", "Rapid symptom relief", "Long-term disease modification — often combined"]],
         "src": "S17; S19; S20"},
        *tab((41, 42, 43, 44), "Alpha1 blocker profiles"),
        *tab((45, 46), "5-alpha-reductase inhibitor profiles"),
        *tab((47, 48, 49), "PDE5 inhibitor profiles"),
    ],
    "hooks": [
        {"kind": "why", "text": "Why does tamsulosin cause dizziness on standing? Alpha1 receptors in blood vessels are blocked too; the uroselective drugs do it less.", "src": "S17; S34"},
    ],
    "high_yield": [
        F("BPH: alpha1 blocker (days; orthostasis, first dose) + 5-ARI (3–6 months; PSA halved) — often together.", "S17; S19"),
        F("PDE5 inhibitor + any nitrate = absolute contraindication; caution with alpha1 blockers.", "S22; S25; SG U6-R16"),
    ],
    "questions": [
        Q("vignette", "A 64-year-old on isosorbide mononitrate for stable angina asks for sildenafil. What should the PA do?",
          "Do not prescribe; involve his cardiologist",
          "PDE5 inhibitors are absolutely contraindicated with any nitrate — life-threatening hypotension (S24).",
          [("Prescribe a low dose of sildenafil", "Still contraindicated (S24)."),
           ("Prescribe tadalafil instead", "Same class (S22)."),
           ("Space the two doses by 6 hours", "Absolute contraindication (S22)."),
           ("Prescribe if his BP is normal today", "Not acceptable (S24).")], "S24; SG U6-R16", from_slides="S24"),
        Q("mechanism", "Why are alpha1 blockers for BPH associated with orthostatic hypotension?",
          "Alpha1 also sets vascular smooth muscle tone",
          "Alpha1 receptors also mediate vascular tone, so blockade lowers systemic resistance (S34).",
          [("They have no effect outside the bladder", "They do (S34)."),
           ("Only beta3 agonists cause it", "Not true (S34)."),
           ("They block cardiac beta receptors", "Not the mechanism (S34)."),
           ("They raise cGMP like nitrates do", "Not the mechanism (S34).")], "S33; S34", from_slides="S33; S34"),
        Q("mechanism", "Why is a nitrate plus a PDE5 inhibitor absolutely contraindicated?",
          "Both raise NO/cGMP — profound hypotension",
          "Both raise NO/cGMP signaling by independent mechanisms; combined, additive to synergistic hypotension (S34).",
          [("PDE5 inhibitors inactivate nitrates", "Not true (S34)."),
           ("The combination has no interaction", "Life-threatening (S34)."),
           ("Nitrates block PDE5, so it is redundant", "Not true (S34)."),
           ("Both raise heart rate dangerously", "Hypotension is the danger (S34).")], "S33; S34", from_slides="S33; S34"),
        Q("vignette", "A man with BPH wants fast relief and long-term shrinkage of his prostate. Best plan?",
          "Alpha1 blocker plus a 5-ARI",
          "Alpha1 blockers act in days; 5-ARIs take 3–6 months to modify disease — combine them (S19–S20).",
          [("5-ARI alone for fast relief", "Takes months (S19)."),
           ("Oxybutynin for outflow obstruction", "Risks retention (S11)."),
           ("Sildenafil plus a nitrate", "Contraindicated (S22)."),
           ("Doxazosin alone for shrinkage", "No shrinkage (S17).")], "S19; S20; S29"),
        Q("vignette", "A man on finasteride for 2 years has a PSA of 1.8 ng/mL. How should it be read?",
          "As about 3.6 ng/mL (double it)",
          "5-ARIs lower PSA by roughly half on long-term therapy (S19–S20).",
          [("At face value, 1.8 ng/mL", "It is halved (S19)."),
           ("As about 0.9 ng/mL", "Doubled, not halved (S19)."),
           ("As meaningless on therapy", "Still usable (S19)."),
           ("Only after a 6-month drug holiday", "Not the taught approach (S19).")], "S19; S20; SG U6-R15"),
        Q("vignette", "A patient starting doxazosin for BPH is told to take the first dose at bedtime. Why?",
          "To avoid first-dose hypotension",
          "Alpha1 blockers cause a first-dose effect and orthostatic hypotension (S17).",
          [("To prevent nighttime urinary retention", "Not the reason (S17)."),
           ("Because it works only at night", "Not the reason (S17)."),
           ("To avoid anticholinergic confusion", "Antimuscarinics (S11)."),
           ("To lower PSA faster", "5-ARIs (S19).")], "S17; S43"),
    ],
}

# ---------------------------------------------------------------- Part 4: integration
t4 = {
    "name": "Putting It All Together: GU Toolkit", "template": "concept", "objectives": ["SO5", "IO6.3", "IO6.4", "IO6.6"],
    "sections": {
        "definitions": [
            F("**Applying the whole genitourinary and reproductive pharmacology toolkit, across both sessions.**", "S27"),
            F("**Figure 18. Original illustrative diagram (not from Katzung): the detrusor, bladder neck/prostate, and corpus cavernosum each rely on receptor families — muscarinic, adrenergic, and NO-cGMP signaling — that recur in the systemic vasculature,**", "S28"),
            F("**explaining why so many genitourinary drug classes have direct cardiovascular counterparts or interactions.** Receptor families are shared with the vasculature — the unifying theme of the session.", "S28; S28 (notes)"),
        ],
        "how": [
            F("Session 1’s gonadal hormone pharmacology (Ch. 40) and PCOS (Ch. 41 overlap) and Session 2’s autonomic bladder pharmacology (Ch. 6) are distinct but connect through shared classes — 5-alpha-reductase inhibitors appear in both sessions.", "S30"),
            F("The lower urinary tract is governed by three nerve supplies and three receptor families (Figure 9): parasympathetic/M3, sympathetic/alpha1 and beta3, and somatic/nicotinic.", "S30"),
            F("Antimuscarinics and beta3 agonists treat overactive bladder through complementary mechanisms — blocking contraction vs. enhancing relaxation — with anticholinergic burden the key safety differentiator in older adults.", "S30"),
            F("Alpha1 blockers and 5-ARIs treat BPH through different timescales and mechanisms and are often combined; alpha1 blockade overlaps directly with Unit 5’s antihypertensive pharmacology.", "S30"),
            F("The NO-cGMP pathway (Figure 15) underlies both erectile function and nitrate angina therapy (Unit 5) — therapeutic in one context, dangerous in combination in another: one of the highest-stakes safety points in the course.", "S30"),
            F("Close by naming the cross-unit integration: genitourinary pharmacology shares receptor families and drug classes with cardiovascular pharmacology covered earlier in the course.", "S30 (notes)"),
        ],
        "clinical": [
            F("**Patient A — older adult with urge incontinence and mild cognitive impairment, needs therapy that avoids anticholinergic burden:** mirabegron (Section 5).", "S29; S29 (notes)"),
            F("**Patient B — man with BPH, wants both rapid symptom relief and long-term disease modification:** combine an alpha1 blocker with a 5-alpha-reductase inhibitor (Section 6).", "S29; S29 (notes)"),
            F("**Patient C — woman with PCOS, irregular cycles, and hirsutism, not currently trying to conceive:** combined hormonal contraception ± metformin (Session 1).", "S29; S29 (notes)"),
            F("**Patient D — man with stable angina on a long-acting nitrate, requesting treatment for erectile dysfunction:** PDE5 inhibitors are contraindicated; this requires a cardiology-involved conversation about alternatives.", "S29; S29 (notes)"),
        ],
        "examples": [
            F("**A cumulative self-test spanning both sessions — use this to review before exams.**", "S31"),
            F("**Recall Q1:** unopposed estrogen drives unchecked endometrial proliferation, raising hyperplasia and cancer risk with a uterus — a progestin is always paired unless she has had a hysterectomy.", "S32; S34"),
            F("**Recall Q2:** tamoxifen is an endometrial agonist (cancer risk) and breast antagonist; raloxifene shares breast antagonist and bone agonist effects but is essentially neutral at the endometrium.", "S32; S34"),
            F("**Recall Q3:** hyperinsulinemia stimulates ovarian theca-cell androgen production and lowers hepatic SHBG, raising free testosterone — the center of the PCOS cycle (Figure 7).", "S32; S34"),
            F("**Recall Q4:** a patient on an antimuscarinic for overactive bladder develops new confusion — switch to mirabegron, which enhances beta3-mediated detrusor relaxation without blocking muscarinic receptors.", "S33; S34"),
            F("That avoids the cumulative anticholinergic burden that can precipitate or worsen confusion in susceptible patients, particularly older adults.", "S34"),
            F("**Recall Q5:** alpha1 receptors are not bladder-specific — blockade also lowers systemic vascular resistance (orthostatic hypotension, first-dose effect). **Q6:** nitrates and PDE5 inhibitors both raise NO/cGMP; combined, potentially fatal hypotension.", "S33; S34"),
        ],
        "traps": [
            F("Integrated case: a PDE5 inhibitor should not be prescribed while this patient remains on isosorbide mononitrate — both drugs independently raise NO/cGMP signaling; the combination can cause profound, life-threatening hypotension.", "SG U6-S"),
            F("This is an absolute contraindication, and any ED treatment decision must involve his cardiologist and consideration of whether his anginal nitrate therapy can be modified first.", "SG U6-S"),
            F("Even without the nitrate, tamsulosin and a PDE5 inhibitor both lower blood pressure (alpha1 blockade and NO-cGMP potentiation) — additive orthostatic hypotension warrants spacing doses or close monitoring.", "SG U6-S"),
            F("His wife’s new vaginal bleeding on tamoxifen should not be dismissed — tamoxifen’s endometrial agonism raises hyperplasia/cancer risk; she needs prompt gynecologic evaluation.", "SG U6-S"),
            F("Match each drug or drug class to its mechanism or site of action — tamoxifen: breast antagonist, bone/endometrium agonist; raloxifene — endometrium neutral; finasteride/dutasteride — 5-alpha-reductase inhibition; oxybutynin — M3 (and M2) antagonism on the detrusor.", "SG U6-M"),
            F("Match: mirabegron — beta3 agonism on the detrusor; tamsulosin — uroselective alpha1 antagonism; sildenafil/tadalafil — PDE5 inhibition prolonging cGMP; metformin (PCOS) — insulin sensitization, indirectly lowering ovarian androgens.", "SG U6-M"),
        ],
    },
    "comparisons": [
        {"title": "Which approach would you choose? (S29)", "columns": ["Patient", "Approach", "Biggest safety check"],
         "rows": [["A · Older adult, urge incontinence, mild cognitive impairment", "Mirabegron", "Blood pressure; avoid anticholinergics"],
                  ["B · BPH, wants fast relief and disease modification", "Alpha1 blocker + 5-ARI", "Orthostasis, first dose; PSA halved"],
                  ["C · PCOS, irregular cycles, hirsutism, no pregnancy plans", "Combined contraception ± metformin", "Estrogen contraindications"],
                  ["D · Angina on a long-acting nitrate, wants ED treatment", "No PDE5 inhibitor; involve cardiology", "Life-threatening hypotension"]],
         "src": "S29; S29 (notes)"},
        {"title": "Supporting drugs at a glance (S50)", "columns": ["Drug(s)", "Why it matters here"],
         "rows": [["**Nitrates**", "Isosorbide, nitroglycerin: never combine with PDE5 inhibitors"],
                  ["**Riociguat**", "Contraindicated with PDE5 inhibitors"],
                  ["**Other anticholinergics**", "Diphenhydramine, tricyclic antidepressants: add to anticholinergic burden"],
                  ["**Cholinesterase inhibitors**", "Donepezil: oppose antimuscarinics"],
                  ["**Antihypertensives**", "Additive hypotension with alpha-1 blockers"],
                  ["**Strong CYP3A4 inhibitors**", "Ketoconazole, clarithromycin: raise PDE5 inhibitor and solifenacin levels"],
                  ["**Desmopressin**", "Nocturia, beyond this lecture"],
                  ["**OnabotulinumtoxinA**", "Refractory overactive bladder, beyond this lecture"],
                  ["**Duloxetine**", "Stress incontinence, beyond this lecture"]],
         "src": "S50; S50 (notes)"},
    ],
    "hooks": [
        {"kind": "mnemonic", "text": "Every case, two answers: **the approach** and **the one thing to check**.", "src": "S29 (instructor script)"},
    ],
    "high_yield": [
        F("GU receptor families recur in the vasculature: alpha1 blockers lower BP; PDE5 inhibitors and nitrates share cGMP.", "S28; S30"),
    ],
    "questions": [
        Q("mechanism", "Why is unopposed estrogen avoided in a patient with an intact uterus?",
          "It raises endometrial hyperplasia and cancer risk",
          "Unopposed estrogen drives unchecked endometrial proliferation (S34).",
          [("It has no effect on the endometrium", "It does (S34)."),
           ("It always causes immediate heavy bleeding", "Absolute claim (S34)."),
           ("It matters only in postmenopausal patients", "Any patient with a uterus (S34)."),
           ("It raises PSA in partners", "Not related (S34).")], "S32; S34", from_slides="S32; S34"),
        Q("mechanism", "Why does tamoxifen raise endometrial cancer risk while raloxifene largely does not?",
          "Tamoxifen is an endometrial agonist",
          "Tamoxifen is an ER agonist at the endometrium; raloxifene is essentially neutral there (S34).",
          [("Tamoxifen blocks the androgen receptor", "ER, not AR (S34)."),
           ("Raloxifene has no ER effects anywhere", "Bone agonist (S34)."),
           ("Both have identical endometrial effects", "They differ (S34)."),
           ("Raloxifene blocks aromatase", "Not the mechanism (S34).")], "S32; S34", from_slides="S32; S34"),
        Q("mechanism", "What is the central pathophysiologic driver linking insulin resistance to hyperandrogenism in PCOS?",
          "Hyperinsulinemia ↑ ovarian androgens, ↓ SHBG",
          "This raises free testosterone — the center of the PCOS cycle (S34).",
          [("No mechanistic connection exists", "There is one (S34)."),
           ("Hyperandrogenism always comes first", "Absolute claim (S34)."),
           ("Metformin blocks the androgen receptor", "Indirect action (S34)."),
           ("Insulin raises SHBG, lowering free testosterone", "Reversed (S34).")], "S32; S34", from_slides="S32; S34"),
    ],
}

content = {
    "lecture": {"id": "L12", "title": "Genitourinary & Reproductive Pharmacology — Session 2", "date": "Tue, Dec 1, 2026"},
    "textbook_status": "included",
    "objectives": objectives,
    "about": about,
    "classes": [t1, t2, t3, t4],
    "notebooklm": {
        "patient": "a 78-year-old with mild cognitive impairment who becomes confused on oxybutynin, and a 64-year-old on isosorbide mononitrate who asks for sildenafil (the lecture’s cases)",
        "suggested_questions": [
            "Map the bladder receptors: what M3, alpha1, beta3 and nicotinic receptors each do.",
            "Why switch an older adult from oxybutynin to mirabegron?",
            "Compare tamsulosin with doxazosin, and alpha1 blockers with 5-ARIs.",
            "Why does finasteride change how PSA is read?",
            "Walk the NO-cGMP pathway and explain the nitrate–PDE5 contraindication.",
        ],
    },
    "audit_skip": [
        {"ref": "S1", "starts_with": "Diane", "reason": "instructor name (no names on the site)"},
        {"ref": "S2", "starts_with": "Start with a genuine", "reason": "teaching instruction; the recap is in About this lecture"},
        {"ref": "S2", "starts_with": "Recap Session 1 in a minute", "reason": "teaching instruction"},
        *[{"ref": r, "starts_with": "Section transition", "reason": "section divider"} for r in ("S3", "S10", "S16")],
        {"ref": "S4", "starts_with": "The spine of the session", "reason": "presenter script; taught from S4"},
        {"ref": "S5", "starts_with": "M3 is dominant; M2", "reason": "presenter script; taught from S5"},
        {"ref": "S6", "starts_with": "Acetylcholine, M3, Gq", "reason": "presenter script; taught from S6"},
        {"ref": "S7", "starts_with": "Norepinephrine acts on", "reason": "presenter script; taught from S7"},
        {"ref": "S9", "starts_with": "Use this slide", "reason": "teaching instruction"},
        {"ref": "S9", "starts_with": "Students should generate", "reason": "teaching instruction"},
        {"ref": "S11", "starts_with": "Oxybutynin, tolterodine, solifenacin, darifenacin. Dry", "reason": "presenter script; taught from S11"},
        {"ref": "S14", "starts_with": "Complementary mechanisms", "reason": "presenter script"},
        {"ref": "S15", "starts_with": "This case is designed", "reason": "teaching instruction"},
        {"ref": "S17", "starts_with": "Tamsulosin and silodosin are uroselective;", "reason": "presenter script; taught from S17"},
        {"ref": "S18", "starts_with": "Same receptor family", "reason": "presenter script"},
        {"ref": "S19", "starts_with": "Finasteride, dutasteride; benefit", "reason": "presenter script; taught from S19"},
        {"ref": "S21", "starts_with": "Slow down", "reason": "teaching instruction"},
        {"ref": "S22", "starts_with": "Sildenafil, tadalafil, vardenafil. Absolute", "reason": "presenter script; taught from S22"},
        {"ref": "S24", "starts_with": "Never prescribe together", "reason": "presenter script; taught from S24"},
        {"ref": "S25", "starts_with": "Nitrates and PDE5 inhibitors both raise cGMP; never", "reason": "presenter script; taught from S25"},
        {"ref": "S26", "starts_with": "Drug names reveal", "reason": "presenter script; the stems are taught in Part 3"},
        {"ref": "S28", "starts_with": "This capstone figure", "reason": "teaching instruction; the theme is taught from S28"},
        {"ref": "S28", "starts_with": "Receptor families are shared", "reason": "presenter script; taught from S28"},
        {"ref": "S29", "starts_with": "Pairs:", "reason": "teaching instruction"},
        {"ref": "S30", "starts_with": "Common thread", "reason": "presenter script; taught from S30"},
        {"ref": "S35", "starts_with": "Class activity", "reason": "teaching instruction"},
        {"ref": "S35", "starts_with": "Abbreviation key: review", "reason": "teaching instruction"},
        {"ref": "S35", "starts_with": "Teaching points", "reason": "teaching instruction; the drugs are in the profiles"},
        *[{"ref": "S35", "starts_with": w, "reason": "Bloom's teaching prompt; rebuilt as practice questions"} for w in ("Bloom", "Understand", "Apply", "Analyze", "Evaluate")],
        *[{"ref": r, "starts_with": w, "reason": "teaching instruction"} for r, w in (("S4", "Take the extra time"), ("S5", "This slide is deliberately framed"),
            ("S13", "The \"no anticholinergic burden\" advantage"), ("S14", "Reinforce that"), ("S17", "The Unit 5 cross-reference"), ("S18", "Point explicitly"),
            ("S19", "Explicitly call back"), ("S21", "This figure is the direct application"), ("S22", "Make the connection"), ("S29", "Work through these"))],
        {"ref": "S50", "starts_with": "Supporting drugs:", "reason": "presenter script; the table covers it"},
        {"ref": "S51", "starts_with": "This slide documents", "reason": "administrative note on AI-tool citation"},
        {"ref": "S51", "starts_with": "Original Claude-generated", "reason": "administrative note on AI-tool citation"},
    ],
}

for _cl in content["classes"]:
    for _fg in _cl.get("figures", []):
        if not _fg["viz"].get("title"):
            _fg["viz"]["title"] = _fg["title"].split("·", 1)[-1].strip()

sys.path.insert(0, str(Path(__file__).parent))
import guide_L12 as G  # noqa: E402
content["guide"] = {"summary": [{"text": t, "src": s} for t, s in G.SUMMARY], "teaser": getattr(G, "TEASER", ""),
                    "cram": [{"prompt": p, "answer": a, "src": s} for p, a, s in G.CRAM], "discrepancies": []}
for _cl in content["classes"]:
    _cl["flows"] = G.FLOWS.get(_cl["name"], [])

import textbook_L12 as TBK  # noqa: E402
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
