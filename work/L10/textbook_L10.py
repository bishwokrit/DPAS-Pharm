"""Textbook additions for L10. The syllabus assigns Ch. 15 and Ch. 3 to both renal sessions; every section is taught in
Session 1 (L09). The few points below come from those same pages and bear directly on today’s topics."""

RAAS = "RAAS Blockers"
OTHER = "Other Antihypertensives & Resistant Hypertension"
NIT = "Nitrates, Angina & the Triple Whammy"

ADD = {
    RAAS: {
        "pk": [
            ("Enalapril’s ACE-inhibition half-life is about 4 hours, yet once-daily dosing works: concentrations stay far above the C50, so ACE stays inhibited.", "p. 50"),
        ],
        "interactions": [
            ("Hyperkalemia with potassium-sparing diuretics rises with drugs that cut renin or angiotensin II: β blockers, NSAIDs, aliskiren, ACE inhibitors, ARBs.", "p. 275"),
        ],
    },
    OTHER: {
        "indications": [
            ("Diuretics enhance the efficacy of many agents, particularly ACE inhibitors; hydralazine and minoxidil need a diuretic because they cause salt and water retention.", "p. 280"),
            ("Spironolactone may be the most effective single agent for drug-resistant hypertension.", "p. 280"),
        ],
    },
    NIT: {
        "interactions": [
            ("NSAIDs blunt loop and thiazide action by reducing renal prostaglandins — significant in nephrotic syndrome or cirrhosis.", "p. 270; p. 272"),
        ],
    },
}

CONFLICTS = {}
DISCREPANCIES = []
CRAM = [
    ("Once-daily ACE inhibitor", "Levels stay far above C50", "p. 50"),
    ("Hydralazine + diuretic", "Vasodilators cause salt and water retention", "p. 280"),
]
QUESTIONS = []
COMPARISONS = {}
DEEPER = {}

_HEAD = ["RENAL TUBULE TRANSPORT MECHANISMS PROXIMAL TUBULE", "DISTAL CONVOLUTED TUBULE", "COLLECTING TUBULE SYSTEM", "RENAL AUTACOIDS", "ADENOSINE",
         "PROSTAGLANDINS", "PEPTIDES", "CARBONIC ANHYDRASE INHIBITORS", "Drug Usual Oral Dosage", "SODIUM GLUCOSE COTRANSPORTER 2 (SGL T2) INHIBITORS",
         "Clinical Indications", "Adverse Reactions", "LOOP DIURETICS", "Clinical Indications & Dosage", "THIAZIDES", "Chemistry & Pharmacokinetics",
         "POTASSIUM-SPARING DIURETICS", "Agent Hydrochlorothiazide", "AGENTS THAT AL TER WATER EXCRETION (AQUARETICS) OSMOTIC DIURETICS",
         "ANTIDIURETIC HORMONE ANTAGONISTS", "UREARETICS", "DIURETIC COMBINATIONS LOOP AGENTS & THIAZIDES", "CLINICAL PHARMACOLOGY OF DIURETIC AGENTS",
         "EDEMATOUS STATES", "HEART FAILURE", "KIDNEY DISEASE AND RENAL FAILURE", "HEPATIC CIRRHOSIS", "IDIOPATHIC EDEMA", "NONEDEMATOUS STATES HYPERTENSION",
         "NEPHROLITHIASIS", "HYPERCALCEMIA", "DIABETES INSIPIDUS", "RENAL & CARDIAC PROTECTION", "RISK OF HYPONATREMIA WITH DIFFERENT DIURETIC CLASSES",
         "VASOPRESSIN (ADH) ANTAGONISTS", "PHARMACOKINETICS", "Volume of Distribution", "Drug Accumulation", "Rate of Absorption",
         "Extraction Ratio & the First-Pass Effect", "THE TIME COURSE OF DRUG EFFECT", "Immediate Effects", "Delayed Effects", "Schedule-Dependent Effects",
         "Conc Effect", "Cumulative Effects", "Maintenance Dose", "Loading Dose", "The Target Concentration Strategy", "Dosing History", "Distribution & Clearance"]

READING_SKIP = [{"heading": h, "reason": "Taught in L09 (Session 1: diuretics and renal dosing — same assigned chapters)"} for h in _HEAD]
