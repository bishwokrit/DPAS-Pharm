"""Authoring source for L10 content.json. Run: python3 author_L10.py"""
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


PROF = {p["slide"]: p for p in PR.read("L10")}


def prof(*slides):
    return [PROF[s] for s in slides]


def path(nodes, edges, drugs, point, h=170, read="Pick a drug to see where it acts."):
    return {"type": "pathway", "title": "", "h": h, "point": point, "nodes": nodes, "edges": edges, "drugs": drugs, "read": read}


def N(id, label, glyph, x, y, w, col):
    return {"id": id, "label": label, "glyph": glyph, "x": x, "y": y, "w": w, "col": col}


def Dg(label, at, note, off=(), less=()):
    return {"label": label, "at": at, "off": list(off), "less": list(less), "note": note}


objectives = [
    {"id": "IO5.1", "src": "Syllabus", "text": "Identify major pharmacologic classes used in the management of renal conditions and describe their mechanisms of action."},
    {"id": "IO5.2", "src": "Syllabus", "text": "Describe the indications, contraindications, adverse effects, and clinically significant interactions associated with medications used to treat renal conditions."},
    {"id": "IO5.3", "src": "Syllabus", "text": "Compare pharmacologic agents within and across therapeutic classes to distinguish clinically relevant differences in efficacy, safety, and use."},
    {"id": "IO5.4", "src": "Syllabus", "text": "Select appropriate pharmacologic therapy for common renal conditions based on clinical presentation and patient-specific factors."},
    {"id": "IO5.5", "src": "Syllabus", "text": "Identify appropriate dosing, administration, and monitoring considerations for medications used in renal conditions."},
    {"id": "IO5.6", "src": "Syllabus", "text": "Explain important medication-use and safety information to patients receiving pharmacotherapy for renal."},
    {"id": "SO1", "src": "S2", "text": "Describe the renin-angiotensin-aldosterone system (RAAS) and identify where each antihypertensive drug class acts."},
    {"id": "SO2", "src": "S2", "text": "Explain why ACE inhibitors and ARBs are preferred first-line therapy for hypertension in chronic kidney disease, including their renoprotective mechanism."},
    {"id": "SO3", "src": "S2", "text": "Identify major antihypertensive drug classes beyond RAAS blockers, their mechanisms, and their role in CKD-specific management."},
    {"id": "SO4", "src": "S2", "text": "Describe vasodilator pharmacology (nitrates, calcium channel blockers) in angina pectoris and its mechanistic overlap with cardiovascular-renal disease management."},
    {"id": "SO5", "src": "S2", "text": "Identify high-risk drug combinations and monitoring needs at the cardiorenal interface, including the \"triple whammy,\" and apply the full renal/cardiorenal toolkit to integrated clinical scenarios with a cumulative recall quiz."},
]

about = [
    F("**PA PHARMACOLOGY COURSE · LECTURE 5 · SESSION 2 OF 2** — Renal Pharmacotherapeutics. **Session 2: Hypertension in CKD and the Cardiovascular-Renal Overlap  |  Thursday, November 19  |  8:30–11:00 AM**", "S1"),
    F("Recap: Session 1 covered renal dosing principles and the five diuretic classes, organized by nephron site — Session 1 gave us nephron sites — plus the hyperkalemia-with-ACEi/ARB preview from the closing case.", "S1 (notes); S2; S2 (notes)"),
    F("Today we follow one pathway, the renin-angiotensin-aldosterone system, then see where it intersects with angina drugs and with the most preventable cause of AKI, the triple whammy — closing with a cumulative recall quiz spanning both sessions.", "S2 (notes)"),
    F("Appendix 1 abbreviation key: PO = by mouth; IV = intravenous; SL = sublingual; BID / TID / QID = two / three / four times daily; ER / SR = extended-release / sustained-release; IR = immediate-release; HF = heart failure; MI = myocardial infarction.", "S36; S36 (notes)"),
    F("LV = left ventricular; EF = ejection fraction; AV = atrioventricular; SVT = supraventricular tachycardia; WPW = Wolff-Parkinson-White; CAD = coronary artery disease; ECG = electrocardiogram; ICP = intracranial pressure; CBC = complete blood count.", "S36; S36 (notes)"),
    F("ACE = angiotensin-converting enzyme; ARB = angiotensin receptor blocker; AKI = acute kidney injury; CKD = chronic kidney disease; CrCl = creatinine clearance; eGFR = estimated glomerular filtration rate; PDE5 = phosphodiesterase type 5; CYP = cytochrome P450.", "S36; S36 (notes); S55 (notes)"),
    F("The profiles give **Formulation, dose, indications, adverse effects, contraindications and toxicity** — your study reference: know the dose logic, the serious adverse effects, the contraindication that changes decisions and the toxicity you would need to recognize. **Standard adult dosing for teaching; verify against current prescribing information.**", "S36; S36 (notes); S37-54"),
    F("**Appendix 2: DRUG PROFILE · SUPPORTING** — supporting drugs explain interactions, not doses. **Listed for context; not profiled in detail.**", "S55; S55 (notes)"),
    F("**Original figures in this deck:** Figures 8, 12, 15, 16 and 18 (The Renin-Angiotensin-Aldosterone System: Where Antihypertensives Act; Antihypertensive Classes: BP-Lowering Efficacy vs. Renoprotection in CKD; Angina Pathophysiology: Where Nitrates and Calcium Channel Blockers Act;", "S56"),
    F("The \"Triple Whammy\": A Classic Preventable Cause of AKI; The Cardiorenal-Hypertension Cycle) were generated by the course director using the AI tool Claude to illustrate standard, non-copyrighted pharmacologic concepts — original diagrams, not reproduced from Katzung’s Basic and Clinical Pharmacology or any other copyrighted source.", "S56; S56 (notes)"),
    F("**Mechanism illustrations:** Figures 9, 10, 11, 13, 14 and 17 are illustrative AI-generated schematics of drug mechanisms, not reproduced from any copyrighted source. **Reference:** Anthropic. (2026). Claude (Sonnet 5) [Large language model]. https://claude.ai", "S56; S56 (notes)"),
]

# ---------------------------------------------------------------- Part 1: RAAS blockers
t1 = {
    "name": "RAAS Blockers", "template": "drug_class", "objectives": ["SO1", "SO2", "IO5.1", "IO5.2", "IO5.4", "IO5.5"],
    "sections": {
        "overview": [
            F("**One pathway, four drug classes, and the preferred therapy for hypertension in CKD.** Today we follow the renin-angiotensin-aldosterone system, the pathway these drugs act on.", "S3; S3 (notes)"),
            F("**Figure 8. Original illustrative diagram (not from Katzung): angiotensinogen is converted to angiotensin I by renin, then to angiotensin II by ACE; angiotensin II drives both vasoconstriction and aldosterone release.**", "S4; SG U5-R7"),
            F("**Direct renin inhibitors, ACE inhibitors, ARBs, and aldosterone antagonists each block a different point in this cascade.**", "S4; SG U5-R7"),
            F("This is the conceptual spine for the session: walk the cascade before naming drugs — angiotensinogen, renin, angiotensin I, ACE, angiotensin II, vasoconstriction and aldosterone.", "S4 (notes)"),
        ],
        "prototype": [
            F("ACE inhibitors: captopril, lisinopril, enalapril — \"-pril\" suffix across the class. ARBs: losartan, valsartan — \"-sartan\" suffix. Direct renin inhibitor: aliskiren.", "S5; S7"),
        ],
        "moa": [
            F("**Mechanism: block the conversion of angiotensin I to angiotensin II, reducing both vasoconstriction and aldosterone release (Figure 8).**", "S5"),
            F("ACE also breaks down bradykinin: ACE inhibitor blocks ACE → less angiotensin II (less vasoconstriction and aldosterone) → less bradykinin breakdown, so bradykinin accumulates → cough or angioedema → switch to an ARB for cough.", "S6; S6 (notes)"),
            F("ARBs block the AT1 receptor directly, rather than preventing angiotensin II formation. Aliskiren blocks the rate-limiting first step of the entire cascade.", "S7"),
            F("Renoprotection: by reducing angiotensin II, these drugs preferentially dilate the efferent (outflow) arteriole of the glomerulus, lowering intraglomerular pressure and reducing proteinuria — a direct, structural renoprotective effect beyond systemic BP control.", "S8; SG U5-R8"),
            F("Chain (Figure 10): angiotensin II normally constricts the efferent arteriole → ACE inhibitor or ARB removes that signal → efferent arteriole dilates; intraglomerular pressure falls → proteinuria falls; creatinine rises up to ~30%.", "S9"),
        ],
        "indications": [
            F("**ACE inhibitors and ARBs are first-line antihypertensive therapy in CKD, especially with proteinuria — not simply because they lower blood pressure.**", "S8"),
            F("ARBs: no bradykinin-related cough — preferred alternative when ACE inhibitor cough is intolerable. ARBs do not raise bradykinin, so they are the usual switch.", "S6; S7"),
            F("Aliskiren: limited clinical use; useful mainly as a teaching example of where a drug could act upstream of ACE — included for conceptual completeness on Figure 8.", "S7; S7 (notes)"),
            F("The drug class students might expect to avoid in kidney disease is actually the preferred therapy, precisely because of how it works at the glomerulus.", "S8 (notes)"),
        ],
        "adverse": [
            F("**Adverse effects: dry cough (bradykinin accumulation — the single most common reason for switching to an ARB), angioedema (rare but potentially life-threatening), and hyperkalemia.**", "S5"),
            F("Cough is bradykinin-mediated, not allergic. Angioedema is rare but can be life-threatening: stop the drug.", "S6"),
            F("An initial rise in serum creatinine of up to ~30% after starting therapy is expected and acceptable — reflects reduced intraglomerular pressure, not drug-induced kidney injury; a larger rise warrants evaluation for renal artery stenosis.", "S5; SG U5-R9"),
            F("Students frequently get the creatinine point wrong: many want to stop the ACE inhibitor at the first rise. It is a predictable hemodynamic effect, not toxicity — the mechanism and the \"side effect\" are two faces of the same action.", "S5 (notes); S8; S9 (notes)"),
        ],
        "contra": [
            F("**Contraindicated in pregnancy — fetal renal toxicity; avoid in women who are or may become pregnant.** ARBs share the same pregnancy contraindication and hyperkalemia risk as ACE inhibitors.", "S5; S7"),
            F("Aliskiren: generally not combined with an ACE inhibitor or ARB due to additive hyperkalemia/hypotension risk with no added benefit — never in diabetes.", "S7; S7 (notes)"),
        ],
        "interactions": [
            F("Potassium supplements, potassium-sparing diuretics and trimethoprim: hyperkalemia with ACE inhibitors and ARBs. NSAIDs blunt antihypertensives and raise AKI risk with an ACE inhibitor or ARB plus diuretic.", "S55; S55 (notes)"),
        ],
        "pk": [],
        "monitoring": [
            F("**Monitor potassium and renal function within 1–2 weeks of starting or up-titrating therapy, and periodically thereafter.**", "S8; S9 (notes)"),
            F("**Hold or use with caution during acute illness causing volume depletion (\"sick day rules\") — combined with reduced renal perfusion, RAAS blockade can precipitate acute kidney injury.**", "S8"),
            F("Sick-day rules: hold the ACE inhibitor or ARB during vomiting, diarrhea or dehydration. An early creatinine rise is expected and hemodynamic, not nephrotoxicity; a larger rise warrants checking for volume depletion or renal artery stenosis.", "S9; SG U5-R9"),
        ],
        "pearls": [
            F("Case: a patient with hypertension and diabetic nephropathy is started on lisinopril; two weeks later serum creatinine has risen from 1.1 to 1.4 mg/dL. **Is this an indication to stop the ACE inhibitor?**", "S10"),
            F("**A rise of roughly 27% is within the expected range for ACE inhibitor initiation, reflecting reduced intraglomerular pressure from efferent arteriolar dilation — not drug toxicity.**", "S10; S10 (notes)"),
            F("**Therapy should generally continue with ongoing monitoring; a rise beyond approximately 30%, or a much sharper increase, should prompt evaluation for renal artery stenosis or volume depletion.**", "S10"),
            F("A student who reflexively says \"stop the drug\" has missed that this creatinine rise is expected and even reflects the mechanism working as intended.", "S10 (notes)"),
        ],
    },
    "figures": [
        {"image": "S4_1.jpg", "title": "Figure 8 · The RAAS: where antihypertensives act", "src": "S4; S4 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): angiotensinogen → (renin) → angiotensin I → (ACE) → angiotensin II → vasoconstriction and aldosterone. Direct renin inhibitors, ACE inhibitors, ARBs and aldosterone antagonists each block a different step.",
         "viz": path([N("agt", "Angiotensinogen", "molecule", 10, 20, 140, "sage"), N("a1", "Angiotensin I", "molecule", 170, 20, 130, "teal"),
                      N("a2", "Angiotensin II", "molecule", 320, 20, 130, "amber"), N("at1", "AT1 receptor", "membrane", 470, 20, 150, "blue"),
                      N("vc", "Vasoconstriction", "effect", 330, 140, 150, "coral"), N("ald", "Aldosterone →\nNa⁺ retention", "signal", 490, 140, 140, "deep")],
                     [["agt", "a1"], ["a1", "a2"], ["a2", "at1"], ["at1", "vc"], ["at1", "ald"]],
                     [Dg("Aliskiren (renin)", "agt>a1", "Top of the cascade; never with ACEi/ARB in diabetes (S7).", off=["a1", "a2", "at1", "vc", "ald"]),
                      Dg("Lisinopril (ACE)", "a1>a2", "Cough, angioedema, hyperkalemia; pregnancy contraindicated (S5).", off=["a2", "at1", "vc", "ald"]),
                      Dg("Losartan (AT1)", "a2>at1", "No bradykinin cough (S7).", off=["at1", "vc", "ald"]),
                      Dg("Spironolactone", "ald", "Blocks aldosterone’s receptor — hyperkalemia with ACEi/ARB (L09).", less=["ald"])],
                     "One pathway, four places to block it.", h=240)},
        {"image": "S6_1.png", "title": "Figure 9 · ACE inhibitors: bradykinin, cough and angioedema", "src": "S6; S6 (notes)",
         "caption": "Schematic (illustrative) — Figure 9. ACE inhibition and bradykinin accumulation: ACE also breaks down bradykinin, so blocking it raises bradykinin (cough, angioedema); ARBs spare bradykinin.",
         "viz": path([N("ace", "ACE (kininase)", "enzyme", 10, 55, 140, "amber"), N("bk", "Bradykinin\naccumulates", "molecule", 175, 55, 140, "coral"),
                      N("cough", "Dry cough", "effect", 340, 20, 130, "blue"), N("ae", "Angioedema\n(rare, serious)", "effect", 340, 105, 130, "coral"),
                      N("arb", "Switch to an ARB", "effect", 495, 55, 135, "sage")],
                     [["ace", "bk"], ["bk", "cough"], ["bk", "ae"], ["cough", "arb"]],
                     [Dg("ACE inhibitor", "ace", "Blocks bradykinin breakdown → cough (not allergic) (S6)."),
                      Dg("ARB (losartan)", "arb", "Does not raise bradykinin — the usual switch (S6–S7).", off=["bk", "cough"])],
                     "Cough is a mechanism, not an allergy.", h=190)},
        {"image": "S9_1.png", "title": "Figure 10 · Efferent arteriole dilation: why creatinine rises", "src": "S9; S9 (notes)",
         "caption": "Schematic (illustrative) — Figure 10. Efferent arteriole dilation and intraglomerular pressure: removing angiotensin II’s efferent constriction lowers glomerular pressure — less proteinuria, and an expected creatinine rise of up to ~30%.",
         "viz": path([N("a2", "Angiotensin II\nconstricts efferent", "signal", 10, 55, 150, "amber"), N("eff", "Efferent arteriole\ndilates", "membrane", 180, 55, 150, "blue"),
                      N("igp", "Intraglomerular\npressure falls", "effect", 350, 55, 140, "teal"), N("out", "Less proteinuria;\ncreatinine ≤ 30% ↑", "effect", 505, 55, 130, "sage")],
                     [["a2", "eff"], ["eff", "igp"], ["igp", "out"]],
                     [Dg("Lisinopril or losartan", "a2", "Removes the efferent signal: benefit and creatinine rise are the same action (S8–S9).", off=["a2"]),
                      Dg("Volume depletion (sick day)", "igp", "Hold the ACEi/ARB: pressure can fall too far → AKI (S8–S9).")],
                     "The benefit and the creatinine rise are the same action.")},
    ],
    "comparisons": [
        {"title": "ACE inhibitors vs. ARBs vs. aliskiren", "columns": ["", "ACE inhibitors (-pril)", "ARBs (-sartan)", "Aliskiren (-kiren)"],
         "rows": [["Block", "Angiotensin I → II conversion", "AT1 receptor", "Renin (first step)"],
                  ["Cough / bradykinin", "Yes — most common reason to switch", "No", "Cough listed on profile"],
                  ["Pregnancy", "Contraindicated", "Contraindicated", "Contraindicated"],
                  ["Use", "First-line HTN in proteinuric CKD", "First-line; ACEi cough alternative", "Limited; never with ACEi/ARB in diabetes"]],
         "src": "S5; S7; S37-42"},
        *PR.table(prof(37, 38, 39), "ACE inhibitor profiles"),
        *PR.table(prof(40, 41, 42), "ARB and renin inhibitor profiles"),
    ],
    "hooks": [
        {"kind": "why", "text": "Why does creatinine rise on an ACE inhibitor? The drug lowers glomerular pressure on purpose — that same drop protects the kidney from proteinuria.", "src": "S8; S9; SG U5-R8"},
        {"kind": "mnemonic", "text": "Thirty is fine, more is a sign: up to ~30% creatinine rise → continue; more → look for renal artery stenosis or volume depletion.", "src": "S5; S10; SG U5-R9"},
    ],
    "high_yield": [
        F("ACEi/ARB first-line in proteinuric CKD: efferent dilation lowers intraglomerular pressure and proteinuria.", "S8; SG U5-R8"),
        F("Creatinine rise up to ~30% is expected; check K⁺ and creatinine in 1–2 weeks; sick-day rules; never in pregnancy.", "S5; S8; S9; SG U5-R9"),
    ],
    "questions": [
        Q("vignette", "Two weeks after starting lisinopril for diabetic nephropathy, creatinine rose from 1.1 to 1.4 mg/dL. What is the best response?",
          "Continue lisinopril and keep monitoring",
          "A ~27% rise is within the expected range, reflecting reduced intraglomerular pressure; continue with monitoring (S10).",
          [("Stop lisinopril for nephrotoxicity", "This is expected, not toxicity (S10)."),
           ("Switch to an NSAID for blood pressure", "NSAIDs raise AKI risk (S55)."),
           ("Add aliskiren to protect the kidney", "Never with ACEi in diabetes (S7)."),
           ("Double the lisinopril dose today", "Not the response (S10).")], "S10; SG U5-R9", from_slides="S10"),
        Q("mechanism", "Why does an ACE inhibitor cause a dry cough?",
          "Bradykinin accumulates because ACE also degrades it",
          "ACE also breaks down bradykinin; blocking it raises bradykinin, causing cough and angioedema (S6).",
          [("It is an IgE-mediated allergy to the drug", "Cough is not allergic (S6)."),
           ("Angiotensin II rises and irritates airways", "Angiotensin II falls (S5)."),
           ("Aldosterone excess dries the airway", "Aldosterone falls (S5)."),
           ("It blocks AT1 receptors in the lung", "That is an ARB, which spares cough (S7).")], "S6; S7"),
        Q("vignette", "A woman of reproductive age with proteinuric CKD needs antihypertensive therapy. What must be addressed first with an ACE inhibitor?",
          "Pregnancy risk — fetal renal toxicity",
          "ACE inhibitors (and ARBs) are contraindicated in pregnancy; avoid in women who are or may become pregnant (S5; S7).",
          [("Bradykinin cough risk only", "Pregnancy is the contraindication (S5)."),
           ("Ototoxicity with loop diuretics", "Not an ACEi issue (L09)."),
           ("Gynecomastia with long-term use", "Spironolactone (L09)."),
           ("Rebound hypertension if stopped", "Clonidine (S16).")], "S5; S7"),
        Q("mechanism", "Why are ACE inhibitors and ARBs preferred in proteinuric CKD beyond lowering blood pressure?",
          "They dilate the efferent arteriole",
          "Reducing angiotensin II preferentially dilates the efferent arteriole, lowering intraglomerular pressure and proteinuria (S8; SG U5-R8).",
          [("They constrict the afferent arteriole", "That is NSAIDs (S23)."),
           ("They increase aldosterone to retain sodium", "They lower aldosterone (S5)."),
           ("They are the only class allowed in CKD", "Other classes are used too (S12)."),
           ("They raise GFR by expanding volume", "Not the mechanism (S8).")], "S8; S9; SG U5-R8"),
    ],
}

# ---------------------------------------------------------------- Part 2: other antihypertensives
t2 = {
    "name": "Other Antihypertensives & Resistant Hypertension", "template": "drug_class", "objectives": ["SO3", "IO5.1", "IO5.2", "IO5.3", "IO5.4"],
    "sections": {
        "overview": [
            F("**RAAS blockers are first-line — but rarely the whole story.** Other major classes: CCBs, beta-blockers, diuretics, central agents and direct vasodilators.", "S11; S11 (notes); S12 (notes)"),
            F("This four-card slide is a brief classification recap — CCBs and beta-blockers get fuller treatment later this session (angina) and in cardiovascular coursework.", "S12 (notes)"),
        ],
        "prototype": [
            F("Calcium channel blockers: dihydropyridines (amlodipine) and non-dihydropyridines (diltiazem, verapamil). Beta-blockers: metoprolol, atenolol. Central α2 agonists: clonidine, methyldopa. Direct arteriolar vasodilator: hydralazine.", "S12; S28"),
        ],
        "moa": [
            F("Dihydropyridines (amlodipine): arteriolar dilation. Non-dihydropyridines (diltiazem, verapamil): also ↓ HR/contractility.", "S12"),
            F("Beta-blockers: ↓ heart rate, ↓ contractility, ↓ renin release.", "S12"),
            F("Chain (Figure 11): dihydropyridine arteriolar dilation → afterload falls; blood pressure lowers. Non-DHP CCB or beta-blocker: heart rate and contractility fall → renin release falls.", "S13; S13 (notes)"),
            F("Clonidine or methyldopa stimulates central α2 receptors → sympathetic outflow falls, so BP falls. Hydralazine dilates arterioles directly → reflex tachycardia and fluid retention.", "S16; S16 (notes)"),
        ],
        "indications": [
            F("Beta-blockers: not generally first-line for uncomplicated HTN, but compelling indications include concurrent CAD/heart failure/arrhythmia.", "S12"),
            F("If all these classes lower blood pressure similarly, why are RAAS blockers preferred in CKD? Similar BP lowering; ACE inhibitors and ARBs add renoprotection — the renoprotective gap in Figure 12, not a difference in BP control.", "S14; S14 (notes)"),
            F("Thiazide / loop diuretics (covered in depth in Session 1): thiazides first-line with preserved renal function; loops preferred as GFR falls.", "S12"),
            F("Central agents (clonidine, methyldopa) and hydralazine: reserved for resistant hypertension or specific situations (e.g., methyldopa in pregnancy).", "S12; S16"),
        ],
        "adverse": [
            F("Peripheral edema is a CCB class adverse effect.", "S12"),
            F("Hydralazine: reflex tachycardia and fluid retention — must be paired with a beta-blocker and a diuretic.", "S16; S16 (notes)"),
            F("Abrupt clonidine withdrawal causes rebound hypertension.", "S16; S16 (notes)"),
        ],
        "contra": [
            F("Atenolol accumulates in renal impairment (reduce dose when CrCl is below 35 mL/min); beta-blockers: do not stop abruptly.", "S47; S48"),
        ],
        "interactions": [
            F("Diltiazem or verapamil with a beta-blocker risks bradycardia and AV block; dihydropyridines pair with beta-blockers without that conduction risk.", "S13; S13 (notes)"),
            F("Verapamil and diltiazem raise digoxin levels. Rifampin and carbamazepine lower CCB levels; grapefruit juice raises dihydropyridine levels.", "S55; S55 (notes)"),
        ],
        "pk": [],
        "monitoring": [
            F("**Resistant hypertension (BP above goal despite three or more antihypertensive classes, including a diuretic) is common in CKD, often driven by volume overload.**", "S15"),
            F("First step: confirm diuretic therapy is adequate — a thiazide may simply no longer be effective at the patient’s current GFR (Session 1’s loop-vs-thiazide cutoff).", "S15; S15 (notes)"),
            F("Switching from a thiazide to a loop diuretic, or increasing loop diuretic dosing, is often the most effective single change in advanced CKD.", "S15"),
            F("**Aldosterone antagonists (spironolactone) can be added for resistant hypertension, but require close potassium and renal-function monitoring, especially on top of an ACE inhibitor or ARB.**", "S15"),
        ],
        "pearls": [
            F("\"Resistant hypertension in CKD\" is often really a diuretic-selection problem, not a need for an entirely new drug class — check diuretic adequacy first; thiazide to loop switch; add spironolactone with close monitoring.", "S15 (notes)"),
            F("Case: CKD (eGFR 28 mL/min), still hypertensive despite lisinopril, amlodipine, and hydrochlorothiazide. **What is the most likely contributor to inadequate control, and what change would you suggest first?**", "S17"),
            F("**At this GFR, hydrochlorothiazide has largely lost its natriuretic efficacy (Session 1). Switching to a loop diuretic such as furosemide or torsemide is usually the most effective next step before adding an entirely new drug class.**", "S17"),
            F("This case is a direct callback to the Session 1 \"Choosing a Diuretic for Advancing CKD\" case — point out the parallel if you remember it.", "S17 (notes)"),
        ],
    },
    "figures": [
        {"image": "S13_1.png", "title": "Figure 11 · CCBs and beta-blockers: different targets", "src": "S13; S13 (notes)",
         "caption": "**Schematic (illustrative)** — Figure 11. Vascular versus cardiac targets of antihypertensive drugs: dihydropyridines dilate arterioles (afterload falls); non-dihydropyridines and beta-blockers slow heart rate and contractility (beta-blockers also cut renin).",
         "viz": path([N("ves", "Arterioles", "membrane", 10, 20, 130, "teal"), N("aft", "Afterload falls", "effect", 170, 20, 140, "sage"),
                      N("hrt", "Heart: rate and\ncontractility", "cell", 10, 130, 150, "coral"), N("ren", "Renin release", "signal", 190, 130, 130, "amber"),
                      N("bp", "Blood pressure\nlowers", "effect", 470, 75, 150, "blue")],
                     [["ves", "aft"], ["aft", "bp"], ["hrt", "bp"], ["ren", "bp"]],
                     [Dg("Amlodipine (DHP)", "ves", "Arteriolar dilation; peripheral edema (S12–S13)."),
                      Dg("Diltiazem / verapamil", "hrt", "↓ HR and contractility; avoid with beta-blockers (AV block) (S13).", less=["hrt"]),
                      Dg("Metoprolol (beta-blocker)", "hrt", "↓ HR, contractility and renin (S12).", less=["hrt", "ren"])],
                     "Vessel drugs vs. heart drugs — never stack two heart-slowers.", h=240)},
        {"image": "S14_1.jpg", "title": "Figure 12 · BP-lowering efficacy vs. renoprotection in CKD", "src": "S14; S14 (notes)",
         "caption": "Original illustrative comparison (illustrative relative values, not from Katzung): BP-lowering efficacy is broadly comparable — ACEi/ARBs 70, CCBs 72, thiazide/loop diuretics 68, beta-blockers 55 — but renoprotection in proteinuric CKD is far greater with ACEi/ARBs (90) than CCBs (45), diuretics (35) or beta-blockers (30).",
         "viz": {"type": "bars", "title": "BP vs. renoprotection", "yLabel": "Illustrative relative scale",
                 "point": "Similar BP lowering; only ACE inhibitors/ARBs add big renoprotection.",
                 "legend": [["blue", "BP-lowering efficacy"], ["teal", "Renoprotection in proteinuric CKD"]],
                 "bars": [{"label": "ACEi/ARB · BP", "value": 70, "col": "blue", "note": "Comparable BP lowering."},
                          {"label": "ACEi/ARB · kidney", "value": 90, "col": "teal", "note": "Efferent dilation, less proteinuria."},
                          {"label": "CCB · BP", "value": 72, "col": "blue", "note": "Comparable BP lowering."},
                          {"label": "CCB · kidney", "value": 45, "col": "teal", "note": "Less renoprotection."},
                          {"label": "Diuretic · BP", "value": 68, "col": "blue", "note": "Comparable BP lowering."},
                          {"label": "Diuretic · kidney", "value": 35, "col": "teal", "note": "Less renoprotection."},
                          {"label": "BB · BP", "value": 55, "col": "blue", "note": "Somewhat less BP lowering."},
                          {"label": "BB · kidney", "value": 30, "col": "teal", "note": "Least renoprotection."}],
                 "steps": [{"label": "ACEi/ARB kidney", "pick": 1}, {"label": "CCB kidney", "pick": 3}, {"label": "Diuretic kidney", "pick": 5}, {"label": "Beta-blocker kidney", "pick": 7}]}},
        {"image": "S16_1.png", "title": "Figure 13 · Central agents and hydralazine", "src": "S16; S16 (notes)",
         "caption": "Schematic (illustrative) — Figure 13. Central agents and direct arteriolar vasodilation: clonidine and methyldopa reduce sympathetic outflow; hydralazine dilates arterioles directly, triggering reflex tachycardia and fluid retention.",
         "viz": path([N("a2", "Central α2\nreceptors", "signal", 10, 20, 140, "blue"), N("sym", "Sympathetic\noutflow falls", "effect", 170, 20, 140, "teal"),
                      N("art", "Arterioles dilate", "membrane", 10, 130, 150, "amber"), N("ref", "Reflex tachycardia,\nfluid retention", "effect", 190, 130, 160, "coral"),
                      N("bp", "BP falls", "effect", 480, 75, 140, "sage")],
                     [["a2", "sym"], ["sym", "bp"], ["art", "bp"], ["art", "ref"]],
                     [Dg("Clonidine", "a2", "Rebound hypertension if stopped abruptly (S16)."),
                      Dg("Methyldopa", "a2", "Used in pregnancy (S16)."),
                      Dg("Hydralazine", "art", "Pair with a beta-blocker and a diuretic (S16).")],
                     "When others are not enough.", h=240)},
    ],
    "comparisons": [
        {"title": "Other major antihypertensive classes (S12)", "columns": ["Class", "Examples", "Mechanism", "Key point"],
         "rows": [["Calcium channel blockers", "Amlodipine; diltiazem, verapamil", "Arteriolar dilation; non-DHP also ↓ HR/contractility", "Peripheral edema"],
                  ["Beta-blockers", "Metoprolol, atenolol", "↓ HR, contractility, renin", "Compelling: CAD, HF, arrhythmia"],
                  ["Thiazide / loop diuretics", "HCTZ; furosemide", "Session 1", "Loops as GFR falls"],
                  ["Central agents & direct vasodilators", "Clonidine, methyldopa; hydralazine", "Central α2; direct arteriolar", "Resistant HTN; methyldopa in pregnancy"]],
         "src": "S12"},
        *PR.table(prof(43, 44, 45, 46), "Calcium channel blocker profiles"),
        *PR.table(prof(47, 48), "Beta-blocker profiles"),
        *PR.table(prof(49, 50, 51), "Central agent and hydralazine profiles"),
    ],
    "hooks": [
        {"kind": "why", "text": "Why pair hydralazine with a beta-blocker and a diuretic? Direct dilation triggers reflex tachycardia and fluid retention; the partners cancel both.", "src": "S16"},
    ],
    "high_yield": [
        F("Non-DHP CCB + beta-blocker → bradycardia/AV block; DHP + beta-blocker is fine.", "S13"),
        F("Resistant HTN in CKD: fix the diuretic first (thiazide → loop), then spironolactone with K⁺ monitoring.", "S15; S17"),
    ],
    "questions": [
        Q("vignette", "A patient with eGFR 28 mL/min stays hypertensive on lisinopril, amlodipine and hydrochlorothiazide. What change comes first?",
          "Switch hydrochlorothiazide to a loop diuretic",
          "At this GFR HCTZ has largely lost efficacy; switching to furosemide or torsemide is usually the most effective next step (S17).",
          [("Add clonidine as a fourth drug class", "Fix the diuretic first (S15)."),
           ("Add aliskiren to the lisinopril", "Hyperkalemia/hypotension, no benefit (S7)."),
           ("Double the hydrochlorothiazide dose", "The site has too little filtrate (S17)."),
           ("Stop lisinopril because of CKD", "First-line in CKD (S8).")], "S15; S17", from_slides="S17"),
        Q("vignette", "A patient on metoprolol develops heart block after a second drug is added for blood pressure. Which drug most likely?",
          "Verapamil",
          "Non-dihydropyridines (diltiazem, verapamil) with a beta-blocker risk bradycardia and AV block (S13).",
          [("Amlodipine", "DHPs pair safely with beta-blockers (S13)."),
           ("Lisinopril", "No conduction effect (S5)."),
           ("Losartan", "No conduction effect (S7)."),
           ("Hydralazine", "Causes reflex tachycardia (S16).")], "S13; S46"),
        Q("vignette", "A pregnant patient needs an oral antihypertensive. Which central agent is the preferred option on the slides?",
          "Methyldopa",
          "Methyldopa is used in pregnancy (S12; S16; S50).",
          [("Lisinopril", "Contraindicated in pregnancy (S5)."),
           ("Losartan", "Contraindicated in pregnancy (S7)."),
           ("Aliskiren", "Contraindicated in pregnancy (S42)."),
           ("Clonidine", "Rebound risk; not the pregnancy agent (S16).")], "S12; S16; S50"),
        Q("mechanism", "Why must hydralazine be paired with a beta-blocker and a diuretic?",
          "To block reflex tachycardia and fluid retention",
          "Direct arteriolar dilation triggers reflex tachycardia and fluid retention (S16).",
          [("To prevent rebound hypertension on stopping", "That is clonidine (S16)."),
           ("To prevent bradykinin cough", "That is ACE inhibitors (S6)."),
           ("To reduce its hepatic first-pass loss", "Not the taught reason (S16)."),
           ("To avoid hyperkalemia from RAAS blockade", "Not the reason (S16).")], "S16"),
        Q("mechanism", "What happens if clonidine is stopped abruptly?",
          "Rebound hypertension",
          "Abrupt clonidine withdrawal causes rebound hypertension (S16; S49).",
          [("Bradykinin cough", "ACE inhibitors (S6)."),
           ("Hyperkalemia", "RAAS blockers (S5)."),
           ("Angioedema", "ACE inhibitors (S5)."),
           ("Drug-induced lupus", "Hydralazine (S51).")], "S16; S49"),
    ],
}

# ---------------------------------------------------------------- Part 3: vasodilators, angina, triple whammy
t3 = {
    "name": "Nitrates, Angina & the Triple Whammy", "template": "drug_class", "objectives": ["SO4", "SO5", "IO5.1", "IO5.2", "IO5.3", "IO5.6"],
    "sections": {
        "overview": [
            F("**Where cardiovascular and renal pharmacology converge — and where that convergence can go wrong.** This section covers vasodilators and angina, then the cardiorenal overlap.", "S18; S18 (notes)"),
            F("**Figure 15. Original illustrative diagram (not from Katzung): angina results when myocardial oxygen demand exceeds supply; nitrates reduce preload, dihydropyridine CCBs reduce afterload,**", "S21"),
            F("**non-dihydropyridine CCBs also reduce heart rate/contractility and increase coronary flow, and beta-blockers reduce heart rate and contractility.**", "S21"),
            F("This figure organizes every antianginal drug class by exactly which side of the supply/demand equation it affects — sort nitrates, each CCB subtype, and beta-blockers onto it from memory.", "S21 (notes)"),
        ],
        "prototype": [
            F("Nitroglycerin (sublingual for acute angina; IV/patch for sustained use), isosorbide mononitrate/dinitrate (oral, longer-acting).", "S19"),
        ],
        "moa": [
            F("**Mechanism: release nitric oxide, activating guanylate cyclase and increasing cGMP, producing smooth muscle relaxation — predominantly venodilation at usual doses, reducing preload and myocardial oxygen demand.**", "S19; SG U5-R11"),
            F("Chain (Figure 14): nitrate donates nitric oxide (NO) → NO activates guanylate cyclase, so cGMP rises → cGMP relaxes smooth muscle: venodilation → preload and oxygen demand fall.", "S20; S20 (notes)"),
            F("**Dihydropyridines (amlodipine, nifedipine) — predominantly arteriolar dilation, reducing afterload; the same mechanism used for hypertension (Section 5).**", "S22; SG U5-R10"),
            F("**Non-dihydropyridines (diltiazem, verapamil) — also reduce heart rate and contractility and increase coronary blood flow; avoid combining with beta-blockers due to additive bradycardia/AV block risk.**", "S22"),
        ],
        "indications": [
            F("CCBs are the clearest example in the unit of the same drug class, same mechanism, treating two different conditions (hypertension and angina).", "S22; SG U5-R10"),
            F("This is the deliberate cardiovascular-renal \"overlap\" moment the lecture title promises — calcium channel blockers are not a separate topic from the antihypertensive content in Section 5; they are the same drugs doing double duty.", "S22 (notes)"),
        ],
        "adverse": [
            F("**Adverse effects: headache (vasodilation), reflex tachycardia, orthostatic hypotension.**", "S19"),
            F("**Adverse effects: peripheral edema and reflex tachycardia (dihydropyridines); bradycardia, AV block, and constipation (non-dihydropyridines, especially verapamil).**", "S22"),
        ],
        "contra": [
            F("**Absolute contraindication: concurrent use with PDE5 inhibitors (sildenafil and similar) — the combination can cause life-threatening hypotension.**", "S19; SG U5-R11"),
            F("PDE5 inhibitors such as sildenafil block cGMP breakdown, causing severe hypotension with nitrates.", "S20; S20 (notes)"),
            F("The PDE5-inhibitor interaction is one of the highest-stakes medication-safety points in this whole unit — a real-world, repeatedly tested safety question worth a memorable callout.", "S19 (notes)"),
        ],
        "interactions": [
            F("**Figure 16. Original illustrative diagram (not from Katzung): an NSAID (afferent arteriolar constriction), an ACE inhibitor or ARB (efferent arteriolar dilation), and a diuretic (volume depletion) each independently reduce glomerular filtration pressure —**", "S23; SG U5-R12"),
            F("**combined, the effect on kidney perfusion is additive to synergistic, substantially raising acute kidney injury risk.** An extremely common, often missed, entirely preventable cause of AKI.", "S23; S23 (notes); SG U5-R12"),
            F("Three hits (Figure 17): NSAID constricts the afferent arteriole → ACE inhibitor or ARB dilates the efferent arteriole → diuretic causes volume depletion → filtration pressure collapses: AKI.", "S24; S24 (notes)"),
        ],
        "pk": [],
        "monitoring": [
            F("Tolerance develops with continuous exposure — a nitrate-free interval (typically overnight) is required to maintain efficacy with long-acting formulations.", "S19; S20"),
            F("Prevention: counsel patients about over-the-counter NSAIDs — ask which OTC NSAIDs they commonly take.", "S24; S24 (notes)"),
        ],
        "pearls": [
            F("The triple whammy is the capstone cardiorenal interaction: Session 1’s diuretics + this session’s RAAS blockers + NSAIDs students will meet constantly in practice.", "S23 (notes)"),
            F("Hypertension → CKD: uncontrolled blood pressure causes glomerular capillary injury and nephrosclerosis over time — a leading cause of CKD progression, alongside diabetes.", "S25; S25 (notes)"),
            F("CKD → hypertension: reduced renal function causes volume overload and RAAS activation, which worsens and complicates blood pressure control, often requiring multiple drug classes.", "S25; S25 (notes)"),
            F("**Figure 18. Original illustrative diagram (not from Katzung): hypertension and chronic kidney disease drive one another in a self-reinforcing cycle — uncontrolled blood pressure causes glomerular injury and CKD progression,**", "S26"),
            F("**while CKD causes volume overload and RAAS activation that worsens hypertension.**", "S26"),
            F("Figure 18 is the conceptual closer for the whole unit — tie it back to Figure 8: RAAS blockade is effective precisely because it intervenes in both directions of this cycle at once.", "S26 (notes)"),
            F("Case: an older adult on lisinopril and hydrochlorothiazide starts a regular OTC NSAID for a knee injury; one week later, lethargy and an acute rise in creatinine. **What is the most likely explanation, and how could this have been prevented?**", "S27"),
            F("**This is a classic \"triple whammy\" presentation (Figure 16) — the NSAID, ACE inhibitor, and diuretic each independently reduced glomerular filtration pressure, and together precipitated acute kidney injury.**", "S27; SG U5-S"),
            F("**Prevention requires counseling patients on RAAS blockers and diuretics to avoid regular NSAID use and to seek guidance before starting one, even an over-the-counter product.**", "S27; SG U5-S"),
            F("This case is the direct clinical application of Figure 16 and reinforces IO5.6 (patient counseling): the preventable element is entirely what the patient was or wasn’t told about OTC NSAID use.", "S27 (notes)"),
            F("Same patient, eGFR now 25: hydrochlorothiazide has likely lost much of its efficacy — switching to a loop diuretic (furosemide, torsemide) is more effective for blood pressure regardless of the NSAID issue.", "SG U5-S"),
            F("Counsel the patient to avoid regular OTC NSAID use and to check with a prescriber or pharmacist before starting any new OTC product, given the RAAS blocker + diuretic combination already in place.", "SG U5-S"),
        ],
    },
    "figures": [
        {"image": "S20_1.png", "title": "Figure 14 · Nitrates: NO, cGMP and venodilation", "src": "S20; S20 (notes)",
         "caption": "Schematic (illustrative) — Figure 14. Nitrate action: NO → guanylate cyclase → cGMP → smooth-muscle relaxation (venodilation) → lower preload and oxygen demand. PDE5 inhibitors block cGMP breakdown — severe hypotension with nitrates.",
         "viz": path([N("no", "Nitrate donates\nNO", "molecule", 10, 55, 130, "teal"), N("gc", "Guanylate\ncyclase", "enzyme", 160, 55, 120, "blue"),
                      N("cg", "cGMP rises", "molecule", 300, 55, 120, "amber"), N("ven", "Venodilation:\npreload, O₂ demand ↓", "effect", 440, 55, 190, "sage")],
                     [["no", "gc"], ["gc", "cg"], ["cg", "ven"]],
                     [Dg("Nitroglycerin SL", "no", "Acute angina: 0.4 mg every 5 min up to 3 doses (S19; S52)."),
                      Dg("Isosorbide mononitrate", "no", "Long-acting; needs a nitrate-free interval (S19; S53)."),
                      Dg("Sildenafil (PDE5 inhibitor)", "cg", "Blocks cGMP breakdown → life-threatening hypotension with nitrates (S19–S20).")],
                     "NO → cGMP → veins relax; never add a PDE5 inhibitor.")},
        {"image": "S21_1.jpg", "title": "Figure 15 · Angina: where nitrates and CCBs act", "src": "S21; S21 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): angina results when myocardial oxygen demand exceeds supply. Nitrates reduce preload; dihydropyridine CCBs reduce afterload; non-dihydropyridine CCBs also reduce heart rate/contractility and increase coronary flow; beta-blockers reduce heart rate and contractility.",
         "viz": path([N("pre", "Preload", "effect", 10, 20, 120, "teal"), N("aft", "Afterload", "effect", 10, 100, 120, "blue"),
                      N("hr", "Heart rate,\ncontractility", "cell", 10, 180, 140, "coral"), N("dem", "O₂ demand", "signal", 260, 100, 130, "amber"),
                      N("sup", "Coronary\nsupply", "signal", 260, 200, 130, "sage"), N("ang", "Angina when\ndemand > supply", "effect", 470, 140, 160, "deep")],
                     [["pre", "dem"], ["aft", "dem"], ["hr", "dem"], ["dem", "ang"], ["sup", "ang"]],
                     [Dg("Nitrates", "pre", "Reduce preload (S21).", less=["pre", "dem"]),
                      Dg("Amlodipine (DHP)", "aft", "Reduce afterload (S21–S22).", less=["aft", "dem"]),
                      Dg("Diltiazem / verapamil", "hr", "↓ HR/contractility and ↑ coronary flow (S21–S22).", less=["hr", "dem"]),
                      Dg("Metoprolol", "hr", "↓ HR and contractility (S21).", less=["hr", "dem"])],
                     "Sort each drug: preload, afterload, or heart rate.", h=280)},
        {"image": "S23_1.jpg", "title": "Figure 16 · The triple whammy", "src": "S23; S23 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): NSAID (afferent constriction) + ACE inhibitor or ARB (efferent dilation) + diuretic (volume depletion) each independently lower glomerular filtration pressure — combined, additive to synergistic AKI risk.",
         "viz": path([N("aff", "Afferent arteriole\n(inflow)", "membrane", 10, 20, 160, "coral"), N("vol", "Plasma volume", "molecule", 10, 130, 160, "blue"),
                      N("eff", "Efferent arteriole\n(outflow)", "membrane", 200, 75, 160, "amber"), N("gfp", "Glomerular filtration\npressure", "signal", 390, 75, 160, "teal"),
                      N("aki", "AKI", "effect", 570, 75, 60, "deep")],
                     [["aff", "gfp"], ["vol", "gfp"], ["eff", "gfp"], ["gfp", "aki"]],
                     [Dg("NSAID", "aff", "Constricts the afferent arteriole (S23–S24).", less=["aff", "gfp"]),
                      Dg("Lisinopril or losartan", "eff", "Dilates the efferent arteriole (S23–S24).", less=["gfp"]),
                      Dg("Hydrochlorothiazide / furosemide", "vol", "Volume depletion (S23–S24).", less=["vol", "gfp"])],
                     "Add all three hits to see filtration pressure collapse.", h=240)},
        {"image": "S24_1.png", "title": "Figure 17 · Three hits on glomerular pressure", "src": "S24; S24 (notes)",
         "caption": "Schematic (illustrative) — Figure 17. Three hits on glomerular filtration pressure: afferent constriction (NSAID), efferent dilation (ACE inhibitor or ARB), volume depletion (diuretic) → filtration pressure collapses: AKI. Prevention: counsel patients about OTC NSAIDs.",
         "viz": path([N("n", "NSAID: afferent\nconstricts", "membrane", 10, 55, 145, "coral"), N("a", "ACEi/ARB: efferent\ndilates", "membrane", 170, 55, 150, "amber"),
                      N("d", "Diuretic: volume\ndepleted", "molecule", 335, 55, 140, "blue"), N("k", "Filtration\npressure → AKI", "effect", 490, 55, 140, "deep")],
                     [["n", "a"], ["a", "d"], ["d", "k"]],
                     [Dg("Stop the OTC NSAID", "n", "Counsel: avoid regular NSAIDs on a RAAS blocker + diuretic (S24; S27).", off=["n"]),
                      Dg("Sick-day rules", "a", "Hold ACEi/ARB in vomiting, diarrhea, dehydration (S9).", off=["a"])],
                     "Remove one hit to protect the kidney.")},
        {"image": "S26_1.jpg", "title": "Figure 18 · The cardiorenal-hypertension cycle", "src": "S26; S26 (notes)",
         "caption": "Original illustrative diagram (not from Katzung): uncontrolled blood pressure causes glomerular injury and CKD progression, while CKD causes volume overload and RAAS activation that worsens hypertension — a self-reinforcing cycle that RAAS blockade interrupts in both directions.",
         "viz": path([N("htn", "Hypertension", "signal", 10, 20, 140, "coral"), N("inj", "Glomerular injury,\nnephrosclerosis", "cell", 330, 20, 170, "amber"),
                      N("ckd", "CKD", "cell", 330, 140, 170, "blue"), N("vol", "Volume overload,\nRAAS activation", "signal", 10, 140, 160, "teal")],
                     [["htn", "inj"], ["inj", "ckd"], ["ckd", "vol"], ["vol", "htn"]],
                     [Dg("ACE inhibitor / ARB", "vol", "Interrupts both directions at once (S26).", less=["vol", "inj"])],
                     "Managing one well means managing the other.", h=230)},
    ],
    "comparisons": [
        {"title": "Calcium channel blockers: DHP vs. non-DHP (S22)", "columns": ["", "Dihydropyridines", "Non-dihydropyridines"],
         "rows": [["Examples", "Amlodipine, nifedipine", "Diltiazem, verapamil"],
                  ["Main action", "Arteriolar dilation → ↓ afterload", "↓ HR, contractility; ↑ coronary flow"],
                  ["Adverse effects", "Peripheral edema, reflex tachycardia", "Bradycardia, AV block, constipation (verapamil)"],
                  ["With a beta-blocker", "Safe pairing", "Avoid — bradycardia/AV block"]],
         "src": "S13; S22"},
        {"title": "Drug names reveal the class: cardiorenal agents (S28)", "columns": ["Stem", "Class", "Examples", "Memory aid"],
         "rows": [["-pril", "ACE inhibitor", "Lisinopril, enalapril, captopril", "Angiotensin-converting enzyme"],
                  ["-sartan", "ARB", "Losartan, valsartan", "Angiotensin receptor blocker"],
                  ["-kiren", "Direct renin inhibitor", "Aliskiren", "Renin is the top of the cascade"],
                  ["-dipine", "Dihydropyridine CCB", "Amlodipine, nifedipine", "Arteriolar dilation"],
                  ["-olol", "Beta-blocker", "Metoprolol, atenolol", "Heart rate and renin down"],
                  ["-azine / -alazine", "Hydralazine vasodilator", "Hydralazine", "Pair with beta-blocker and diuretic"],
                  ["-onidine", "Central alpha-2 agonist", "Clonidine", "Central, so sympathetic outflow falls"],
                  ["-nitrate / nitro-", "Nitrates", "Isosorbide, nitroglycerin", "Venodilation, preload down"],
                  ["-afil", "PDE5 inhibitor", "Sildenafil", "Never combine with nitrates"],
                  ["-semide", "Loop diuretic", "Furosemide", "Loop of Henle"]],
         "src": "S28; S28 (notes)"},
        {"title": "Supporting drugs at a glance (S55)", "columns": ["Drug(s)", "Why it matters here"],
         "rows": [["NSAIDs", "Blunt antihypertensives; raise AKI risk with ACE inhibitor or ARB plus diuretic"],
                  ["PDE5 inhibitors (such as sildenafil)", "Never combine with nitrates"],
                  ["Potassium supplements and potassium-sparing diuretics", "Hyperkalemia with ACE inhibitors and ARBs"],
                  ["Trimethoprim", "Hyperkalemia"],
                  ["Loop and thiazide diuretics", "Covered in Session 1"],
                  ["Statins and aspirin", "Cardiovascular risk reduction"],
                  ["Digoxin", "Verapamil and diltiazem raise digoxin levels"],
                  ["Rifampin and carbamazepine", "Lower calcium channel blocker levels"],
                  ["Grapefruit juice", "Raises dihydropyridine calcium channel blocker levels"]],
         "src": "S55; S55 (notes)"},
        *PR.table(prof(52, 53, 54), "Nitrate profiles"),
    ],
    "hooks": [
        {"kind": "mnemonic", "text": "Stems: **-pril**, **-sartan**, **-kiren**, **-dipine**, **-olol**, **-azine / -alazine**, **-onidine**, **-nitrate / nitro-**, **-afil**, **-semide**. Read the **Stem**, name the **Class**, recall the **Examples** and the **Memory aid**.", "src": "S28; S28 (notes)"},
        {"kind": "why", "text": "Why are nitrates + sildenafil deadly? Nitrates make cGMP; sildenafil stops its breakdown — cGMP piles up and blood pressure collapses.", "src": "S20"},
    ],
    "high_yield": [
        F("Nitrates: NO → cGMP → venodilation, ↓ preload; nitrate-free interval; never with PDE5 inhibitors.", "S19; S20; SG U5-R11"),
        F("Triple whammy: NSAID (afferent) + ACEi/ARB (efferent) + diuretic (volume) → AKI; counsel on OTC NSAIDs.", "S23; S27; SG U5-R12"),
    ],
    "questions": [
        Q("vignette", "An older adult on lisinopril and hydrochlorothiazide starts daily OTC ibuprofen for a knee injury. A week later creatinine is up acutely. Best explanation?",
          "Triple whammy: three hits on filtration pressure",
          "The NSAID, ACE inhibitor and diuretic each independently reduce glomerular filtration pressure, together precipitating AKI (S27).",
          [("Allergic interstitial nephritis from lisinopril", "Not the taught picture (S27)."),
           ("Expected creatinine rise from starting lisinopril", "He is not newly started (S27)."),
           ("Thiazide-induced hypercalcemia", "Not the mechanism (S27)."),
           ("Contrast nephropathy from imaging", "No contrast given (S27).")], "S27; SG U5-S", from_slides="S27"),
        Q("vignette", "A man using sildenafil asks for a nitroglycerin prescription for chest pain. What is the key concern?",
          "Life-threatening hypotension",
          "Concurrent PDE5 inhibitors are an absolute contraindication to nitrates — severe hypotension (S19–S20).",
          [("Reflex bradycardia and AV block", "Nitrates cause reflex tachycardia (S19)."),
           ("Severe hyperkalemia", "Not a nitrate effect (S19)."),
           ("Bradykinin-mediated cough", "ACE inhibitors (S6)."),
           ("Faster nitrate tolerance only", "The interaction is the danger (S19).")], "S19; S20; SG U5-R11"),
        Q("mechanism", "How do nitrates relieve angina?",
          "NO raises cGMP, venodilation cuts preload",
          "Nitrates release NO → guanylate cyclase → cGMP → venodilation, reducing preload and oxygen demand (S19–S20).",
          [("They block β1 receptors to slow the heart", "Beta-blockers (S21)."),
           ("They block L-type calcium channels", "CCBs (S22)."),
           ("They block ACE to lower angiotensin II", "ACE inhibitors (S5)."),
           ("They inhibit PDE5 to raise cAMP", "PDE5 inhibitors (S20).")], "S19; S20"),
        Q("mechanism", "Why does a patient on long-acting isosorbide mononitrate need a nitrate-free interval?",
          "Continuous exposure causes tolerance",
          "Tolerance develops with continuous exposure; a nitrate-free interval (typically overnight) maintains efficacy (S19).",
          [("To prevent rebound hypertension", "Clonidine (S16)."),
           ("To let potassium normalize", "Not a nitrate issue (S19)."),
           ("To prevent angioedema", "ACE inhibitors (S5)."),
           ("To clear its toxic metabolite", "Not the reason (S19).")], "S19; S53"),
        Q("mechanism", "Which drug class is used for both hypertension and angina via the same mechanism?",
          "Calcium channel blockers",
          "CCBs dilate arterioles, lowering afterload — treating both hypertension and angina (S22; SG U5-R10).",
          [("Thiazide diuretics", "Hypertension only (L09)."),
           ("Carbonic anhydrase inhibitors", "Niche diuretic uses (L09)."),
           ("Aldosterone antagonists", "Not an angina class (L09)."),
           ("Central alpha-2 agonists", "Resistant HTN (S16).")], "S22; SG U5-R10"),
    ],
}

# ---------------------------------------------------------------- Part 4: integration + recall quiz
t4 = {
    "name": "Putting It All Together: Renal Toolkit", "template": "concept", "objectives": ["SO5", "IO5.3", "IO5.4", "IO5.6"],
    "sections": {
        "definitions": [
            F("**Applying the whole Renal pharmacology toolkit.** Integration: put the drug classes together — for each patient, name a first-line approach AND the single biggest safety concern to check before prescribing or counseling.", "S29; S29 (notes); S30 (notes)"),
        ],
        "how": [
            F("**1.** Diuretic classes (Session 1) and RAAS-blocking antihypertensives both map onto specific, drug-targetable points in renal physiology — the nephron (Figure 1) and the RAAS cascade (Figure 8), respectively.", "S31"),
            F("**2.** ACE inhibitors and ARBs are preferred first-line therapy for hypertension in CKD because of their renoprotective efferent-arteriolar mechanism, not just their blood-pressure-lowering effect.", "S31"),
            F("**3.** Calcium channel blockers exemplify the cardiovascular-renal overlap directly — the same drug class, same mechanism, treats both hypertension and angina.", "S31"),
            F("**4.** The \"triple whammy\" (NSAID + ACEi/ARB + diuretic) is a classic, common, and preventable cause of acute kidney injury that draws on content from both sessions at once.", "S31"),
            F("**5.** Hypertension and chronic kidney disease exist in a bidirectional, self-reinforcing cycle (Figure 18) — which is exactly why managing one well so often means managing the other.", "S31"),
            F("All three threads center on glomerular filtration pressure.", "S31 (notes)"),
            F("Connecting back to earlier units: drug-metabolism/dosing concepts (Unit 1) and the biologic-mechanism callbacks from Units 2–4 all reinforce that pharmacology is cumulative — the cardiorenal interface is where several organ-system units visibly intersect.", "S31 (notes)"),
        ],
        "clinical": [
            F("**Patient A — advancing CKD, hypertension no longer controlled on a thiazide:** switch to a loop diuretic; check potassium and volume status.", "S30; S15; S17"),
            F("**Patient B — proteinuric CKD, needs first-line antihypertensive therapy:** ACE inhibitor or ARB; check potassium and creatinine in 1–2 weeks and pregnancy potential.", "S30; S5; S8"),
            F("**Patient C — on an ACE inhibitor and a diuretic, about to start a daily OTC NSAID:** counsel against regular NSAID use — triple whammy AKI risk.", "S30; S27"),
            F("**Patient D — stable angina, already on a beta-blocker, needs additional symptom control:** add a dihydropyridine CCB or a long-acting nitrate; avoid diltiazem/verapamil (AV block) and PDE5 inhibitors with nitrates.", "S30; S13; S19; S22"),
        ],
        "examples": [
            F("**A cumulative self-test spanning both sessions — use this to review before exams.** The recall quiz is a standalone resource, separate from in-lecture quick checks.", "S32; S32 (notes); S35 (notes)"),
            F("**Recall Q1–2:** loops collapse the lumen-positive potential (↑ Ca²⁺ excretion), thiazides increase distal Ca²⁺ reabsorption; at eGFR 22 switch the thiazide to a loop.", "S33; S35"),
            F("**Recall Q3–4:** a creatinine rise up to ~30% on an ACE inhibitor is expected — continue with monitoring; ACEi/ARBs dilate the efferent arteriole, lowering intraglomerular pressure and proteinuria.", "S33; S34; S35"),
            F("**Recall Q5:** the triple whammy is three independent reductions in filtration pressure combining additively to synergistically, precipitating AKI.", "S34; S35"),
            F("**Recall Q6:** CCBs treat hypertension via arteriolar dilation (reducing afterload/systemic vascular resistance) and angina via the same mechanism (reducing afterload and myocardial oxygen demand) — one drug class, one mechanism, two indications.", "S34; S35"),
        ],
        "traps": [
            F("Reflexively stopping an ACE inhibitor for a ≤30% creatinine rise is the classic trap.", "S5 (notes); S10 (notes)"),
            F("Adding a new drug class when the real problem is a thiazide at low GFR.", "S15 (notes); S17"),
        ],
    },
    "comparisons": [
        {"title": "Which approach would you choose? (S30)", "columns": ["Patient", "First-line approach", "Biggest safety check"],
         "rows": [["A · Advancing CKD, BP no longer controlled on a thiazide", "Switch to a loop diuretic", "Potassium, volume status"],
                  ["B · Proteinuric CKD, first-line therapy", "ACE inhibitor or ARB", "K⁺ and creatinine in 1–2 weeks; pregnancy"],
                  ["C · ACEi + diuretic, about to start daily OTC NSAID", "Counsel to avoid the NSAID", "Triple whammy AKI"],
                  ["D · Stable angina on a beta-blocker", "Add DHP CCB or long-acting nitrate", "No non-DHP with BB; no PDE5 with nitrates"]],
         "src": "S30; S13; S15; S19; S27"},
    ],
    "hooks": [
        {"kind": "mnemonic", "text": "Every case, two answers: **the approach** and **the one thing to check**.", "src": "S30 (notes)"},
    ],
    "high_yield": [
        F("Five takeaways: two targetable maps · ACEi/ARB renoprotection · CCB overlap · triple whammy · HTN–CKD cycle.", "S31"),
    ],
    "questions": [
        Q("mechanism", "Why do loop diuretics increase calcium excretion while thiazide diuretics decrease it?",
          "Loops collapse the lumen-positive potential",
          "Loops block NKCC2, collapsing the lumen-positive potential driving paracellular Ca²⁺/Mg²⁺ reabsorption; thiazides increase distal Ca²⁺ reabsorption (S35).",
          [("Loops act in the collecting duct", "Loops act at the thick ascending limb (S35)."),
           ("Thiazides block the Na-K-2Cl cotransporter", "Loops do (S35)."),
           ("There is no mechanistic difference", "There is (S35)."),
           ("Thiazides act in the proximal tubule", "Distal tubule (S35).")], "S33; S35", from_slides="S33; S35"),
        Q("vignette", "A patient’s thiazide stops controlling blood pressure as CKD advances to eGFR 22 mL/min. What is the best change?",
          "Switch to a loop diuretic",
          "Thiazides lose most natriuretic efficacy below GFR ~30; loops act upstream and remain effective (S35).",
          [("Increase the thiazide dose", "Too little filtrate reaches the site (S35)."),
           ("Add a second thiazide", "Same failing site (S35)."),
           ("Stop all diuretic therapy", "A loop remains effective (S35)."),
           ("Switch to acetazolamide", "Weak; not the answer (S35).")], "S33; S35", from_slides="S33; S35"),
        Q("vignette", "A patient starts lisinopril for proteinuric CKD; creatinine rises 25% in two weeks. What is the best response?",
          "Continue with monitoring; this is expected",
          "A rise up to ~30% reflects reduced intraglomerular pressure — an expected hemodynamic effect (S35).",
          [("Stop the ACE inhibitor immediately", "Expected, not toxicity (S35)."),
           ("Double the lisinopril dose", "Not the response (S35)."),
           ("Switch to an NSAID instead", "NSAIDs raise AKI risk (S35)."),
           ("Add aliskiren for renoprotection", "Avoid the combination (S7).")], "S33; S35", from_slides="S33; S35"),
        Q("mechanism", "Why are ACE inhibitors and ARBs preferred first-line therapy in proteinuric CKD?",
          "They dilate the efferent arteriole",
          "They preferentially dilate the efferent arteriole, lowering intraglomerular pressure and proteinuria (S35).",
          [("They have no renal effects at all", "They do (S35)."),
           ("They are the only class usable in CKD", "Other classes are used (S35)."),
           ("They increase aldosterone release", "They reduce it (S35)."),
           ("They constrict the afferent arteriole", "That is NSAIDs (S23).")], "S34; S35", from_slides="S34; S35"),
        Q("mechanism", "A patient on an ACE inhibitor and a diuretic starts a daily OTC NSAID and develops AKI. What is the mechanism?",
          "Three reductions in filtration pressure add up",
          "NSAID afferent constriction + ACEi efferent dilation + diuretic volume depletion combine additively to synergistically (S35).",
          [("NSAIDs have no renal effects", "They constrict the afferent arteriole (S35)."),
           ("The ACE inhibitor inactivates the NSAID", "Not a mechanism (S35)."),
           ("This combination has no extra risk", "It is the triple whammy (S35)."),
           ("The diuretic causes allergic nephritis", "Not the mechanism (S35).")], "S34; S35", from_slides="S34; S35"),
        Q("mechanism", "Which drug class treats BOTH hypertension and angina pectoris via the same mechanism?",
          "Calcium channel blockers",
          "CCBs treat hypertension and angina via the same arteriolar-dilation mechanism (S35).",
          [("Thiazide diuretics", "Hypertension only (S35)."),
           ("Carbonic anhydrase inhibitors", "Not antianginal (S35)."),
           ("Aldosterone antagonists", "Not antianginal (S35)."),
           ("Loop diuretics", "Edema, not angina (S35).")], "S34; S35", from_slides="S34; S35"),
    ],
}

content = {
    "lecture": {"id": "L10", "title": "Renal Pharmacotherapeutics — Session 2", "date": "Thu, Nov 19, 2026"},
    "textbook_status": "included",
    "objectives": objectives,
    "about": about,
    "classes": [t1, t2, t3, t4],
    "notebooklm": {
        "patient": "a diabetic-nephropathy patient whose creatinine rises from 1.1 to 1.4 on lisinopril, a CKD patient (eGFR 28) uncontrolled on lisinopril, amlodipine and hydrochlorothiazide, and an older adult on lisinopril and HCTZ who starts an OTC NSAID (the lecture’s and study guide’s cases)",
        "suggested_questions": [
            "Walk the RAAS cascade and name the drug that blocks each step.",
            "Why are ACE inhibitors and ARBs first-line in proteinuric CKD, and why does creatinine rise?",
            "When do you switch an ACE inhibitor to an ARB, and what about aliskiren?",
            "Compare dihydropyridine and non-dihydropyridine CCBs.",
            "How do nitrates work, and why never with sildenafil?",
            "Explain the triple whammy and how to prevent it.",
        ],
    },
    "audit_skip": [
        {"ref": "S1", "starts_with": "Diane", "reason": "instructor name (no names on the site)"},
        {"ref": "S2", "starts_with": "Briefly recap", "reason": "teaching instruction; the recap is in About this lecture"},
        *[{"ref": r, "starts_with": "Section transition", "reason": "section divider"} for r in ("S3", "S18", "S29", "S32")],
        {"ref": "S4", "starts_with": "Walk it step by step", "reason": "teaching instruction"},
        {"ref": "S12", "starts_with": "The point here is classification", "reason": "teaching instruction"},
        {"ref": "S20", "starts_with": "Walk through the NO", "reason": "teaching instruction; the pathway is Figure 14"},
        {"ref": "S33", "starts_with": "D.  Discontinue", "reason": "quiz distractor (wrong option); the quiz is rebuilt as practice questions"},
        {"ref": "S34", "starts_with": "D.  They increase aldosterone", "reason": "quiz distractor (wrong option); the quiz is rebuilt as practice questions"},
        {"ref": "S4", "starts_with": "This is the conceptual spine", "reason": "teaching instruction; taught from S4 (notes) script"},
        {"ref": "S6", "starts_with": "Explain that bradykinin", "reason": "teaching instruction; taught from S6"},
        {"ref": "S7", "starts_with": "Aliskiren is included mainly", "reason": "teaching instruction; taught from S7"},
        {"ref": "S8", "starts_with": "This slide is the clinical payoff", "reason": "teaching instruction; the payoff is taught from S8"},
        {"ref": "S9", "starts_with": "Frame the creatinine", "reason": "teaching instruction"},
        {"ref": "S11", "starts_with": "Section transition", "reason": "section divider"},
        {"ref": "S13", "starts_with": "Contrast vascular", "reason": "teaching instruction"},
        {"ref": "S14", "starts_with": "Use this figure", "reason": "teaching instruction; the question is answered in the Figure 12 caption"},
        {"ref": "S16", "starts_with": "Contrast central", "reason": "teaching instruction"},
        {"ref": "S17", "starts_with": "Case cue", "reason": "teaching instruction"},
        {"ref": "S21", "starts_with": "Have students sort", "reason": "teaching instruction; the sorting is the Figure 15 interactive"},
        {"ref": "S23", "starts_with": "NSAID plus ACE", "reason": "presenter script; taught from S23"},
        {"ref": "S25", "starts_with": "Direct students to Figure 18", "reason": "teaching instruction"},
        {"ref": "S27", "starts_with": "Case cue", "reason": "teaching instruction"},
        {"ref": "S28", "starts_with": "Walk the stems", "reason": "teaching instruction"},
        {"ref": "S30", "starts_with": "Have students work", "reason": "teaching instruction"},
        {"ref": "S30", "starts_with": "Work in pairs", "reason": "teaching instruction"},
        {"ref": "S33", "starts_with": "Use the quiz", "reason": "teaching instruction"},
        {"ref": "S36", "starts_with": "Class activity", "reason": "teaching instruction"},
        {"ref": "S36", "starts_with": "Teaching points", "reason": "teaching instruction; the drugs are in the profiles"},
        *[{"ref": "S36", "starts_with": w, "reason": "Bloom's teaching prompt; rebuilt as practice questions"} for w in ("Bloom", "Understand", "Apply", "Analyze", "Evaluate")],
        {"ref": "S55", "starts_with": "Abbreviation key: Review", "reason": "teaching instruction; the abbreviations are in About this lecture"},
        {"ref": "S56", "starts_with": "This slide documents", "reason": "administrative note on AI-tool citation"},
        {"ref": "S56", "starts_with": "The diagrams in this deck", "reason": "administrative note on AI-tool citation"},
    ],
}

for _cl in content["classes"]:
    for _fg in _cl.get("figures", []):
        if not _fg["viz"].get("title"):
            _fg["viz"]["title"] = _fg["title"].split("·", 1)[-1].strip()

sys.path.insert(0, str(Path(__file__).parent))
import guide_L10 as G  # noqa: E402
content["guide"] = {"summary": [{"text": t, "src": s} for t, s in G.SUMMARY], "teaser": getattr(G, "TEASER", ""),
                    "cram": [{"prompt": p, "answer": a, "src": s} for p, a, s in G.CRAM], "discrepancies": []}
for _cl in content["classes"]:
    _cl["flows"] = G.FLOWS.get(_cl["name"], [])

import textbook_L10 as TBK  # noqa: E402
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
