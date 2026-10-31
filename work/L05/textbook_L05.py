"""Textbook (Katzung 16e, Ch. 62 — acid-peptic, prokinetic and antiemetic sections) additions for L05.
Laxatives, antidiarrheals, IBS, IBD, pancreatic/bile/variceal drugs (rest of Ch. 62) and Ch. 65 supplements are taught in Session 2 (L06)."""

ACID = "Acid-Peptic Disease & Gastric Acid Secretion"
ANTI = "Antacids, H2 Blockers & Proton Pump Inhibitors"
PROT = "Mucosal Protectants & H. pylori Eradication"
EMES = "Antiemetics"

ADD = {
    ACID: {
        "definitions": [
            ("Over 90% of peptic ulcers are caused by H. pylori infection or NSAIDs; bile also counts as an aggressive factor.", "p. 1153"),
        ],
        "how": [
            ("**Physiology of acid secretion:** gastrin acts mainly by releasing histamine from ECL cells; acetylcholine (M3) stimulates the parietal cell directly; somatostatin from antral D cells turns gastrin off.", "p. 1154"),
        ],
    },
    ANTI: {
        "moa": [
            ("H2 blockers inhibit 60–70% of 24-hour acid secretion; PPIs inhibit 90–98% because they block the final common pathway.", "p. 1156; p. 1159"),
        ],
        "indications": [
            ("Infrequent heartburn (fewer than three times per week): antacids or as-needed H2 blockers; antacids act faster but last 1–2 hours vs. 6–10 hours.", "p. 1156"),
            ("PPIs heal over 90% of duodenal ulcers within 4 weeks; GERD recurs in over 80% within 6 months of stopping.", "p. 1159"),
            ("Stress-related bleeding prophylaxis in high-risk ICU patients: an oral PPI if enteral meds are possible, otherwise IV H2 blocker or PPI.", "p. 1157"),
        ],
        "adverse": [
            ("PPIs carry an FDA warning for hip, spine and wrist fractures and for life-threatening hypomagnesemia; 2–3-fold more C. difficile infection.", "p. 1160"),
            ("Sodium bicarbonate causes belching and metabolic alkalosis; excess calcium carbonate with dairy causes hypercalcemia, renal insufficiency and alkalosis (milk-alkali).", "p. 1155"),
        ],
        "contra": [
            ("Magnesium and aluminum antacids are renally excreted: avoid long-term use in renal insufficiency.", "p. 1155"),
        ],
        "interactions": [
            ("Antacids should not be given within 2 hours of tetracyclines, fluoroquinolones, itraconazole, and iron.", "p. 1155"),
            ("With clopidogrel, prefer pantoprazole or rabeprazole (minimal CYP2C19 inhibition).", "p. 1161"),
            ("Less acid lowers absorption of ketoconazole, itraconazole, digoxin, and atazanavir.", "p. 1161"),
        ],
        "pk": [
            ("PPIs: food cuts bioavailability by about 50%; half-life about 1.5 hours yet acid inhibition lasts up to 24 hours; full effect takes 3–4 days.", "p. 1158"),
            ("PPIs need no renal dose reduction; consider reduction in severe liver impairment.", "p. 1159"),
        ],
    },
    PROT: {
        "moa": [
            ("Sucralfate is sucrose complexed to sulfated aluminum hydroxide; less than 3% is absorbed.", "p. 1161"),
            ("Bismuth coats ulcers, has direct antimicrobial effects and binds enterotoxins (traveler’s diarrhea).", "p. 1162"),
        ],
        "indications": [
            ("Misoprostol cuts NSAID-induced ulcers to less than 3% and ulcer complications by 50%, but dosing 3–4 times daily and diarrhea limit use.", "p. 1162"),
        ],
        "adverse": [
            ("Bismuth blackens stool (can mimic GI bleeding) and darkens the tongue; avoid in renal insufficiency.", "p. 1162"),
        ],
        "monitoring": [
            ("After antibiotics, continue the PPI once daily for a total of 4–6 weeks to complete ulcer healing.", "p. 1159"),
        ],
    },
    EMES: {
        "moa": [
            ("**Pathophysiology of vomiting:** the vomiting center sits in the lateral medullary reticular formation; the CTZ (area postrema) lies outside the blood-brain barrier.", "p. 1169"),
        ],
        "indications": [
            ("5-HT3 antagonists control vagal and chemotherapy emesis but poorly control motion sickness; palonosetron also prevents delayed emesis.", "p. 1170"),
            ("**Pharmacokinetics & pharmacodynamics (5-HT3):** first-generation agents have half-lives of 4–9 hours; palonosetron 40 hours; no dose cut in renal insufficiency.", "p. 1170"),
            ("NK1 antagonist + 5-HT3 antagonist + dexamethasone prevents acute emesis in 80–90% of highly emetogenic chemotherapy patients.", "p. 1171"),
            ("Benzodiazepines (lorazepam, diazepam) prevent anticipatory vomiting before chemotherapy.", "p. 1172"),
        ],
        "adverse": [
            ("Metoclopramide: restlessness, drowsiness and agitation in 10–20%; extrapyramidal effects in 25% at high doses; prolactin rises (galactorrhea, gynecomastia).", "p. 1164"),
            ("Droperidol prolongs the QT interval (rare fatal torsades) — only if alternatives fail.", "p. 1172"),
        ],
        "interactions": [
            ("Aprepitant is a CYP3A4 substrate/inhibitor: lowers INR with warfarin; dexamethasone dose is often reduced with it.", "p. 1171"),
        ],
    },
}

CONFLICTS = {
    PROT: [
        {"topic": "H. pylori triple therapy duration",
         "slides": {"text": "Triple therapy: PPI + amoxicillin + clarithromycin for 10–14 days (usual duration 14 days).", "src": "S19; S19 (notes)"},
         "textbook": {"text": "A 14-day regimen is recommended; quadruple therapy is now first-line where clarithromycin resistance is likely.", "src": "p. 1159"}},
    ],
}

DISCREPANCIES = [
    ("**Triple therapy length:** slides say 10–14 days (usual 14); the textbook recommends 14 days and quadruple therapy first-line where clarithromycin resistance is likely. Answer with 14 days.", "S19; p. 1159"),
    ("**Cimetidine’s CYP targets:** slides list 1A2, 2C19, 3A4; the textbook lists 1A2, 2C9, 2D6, 3A4. Either way: a broad CYP inhibitor that raises warfarin, phenytoin, theophylline.", "S12; p. 1157"),
]

CRAM = [
    ("H2 blocker vs. PPI suppression", "60–70% vs. 90–98% of 24-hour acid", "p. 1156; p. 1159"),
    ("PPI timing", "30–60 min before breakfast; full effect in 3–4 days", "p. 1158"),
    ("PPI with clopidogrel", "Prefer pantoprazole or rabeprazole", "p. 1161"),
    ("Antacid spacing", "2 hours from tetracyclines, fluoroquinolones, itraconazole, iron", "p. 1155"),
    ("Bismuth", "Black stool and tongue; avoid in renal insufficiency", "p. 1162"),
    ("CINV triple combo", "NK1 + 5-HT3 + dexamethasone: 80–90% prevention", "p. 1171"),
]

QUESTIONS = [
    dict(topic=ANTI, kind="vignette",
         stem="A patient on clopidogrel after a stent needs long-term acid suppression. Which PPI does the textbook prefer?",
         correct="Pantoprazole, with minimal CYP2C19 inhibition",
         why_correct="When PPIs are prescribed with clopidogrel, agents with minimal CYP2C19 inhibition (pantoprazole or rabeprazole) may be preferred (p. 1161).",
         distractors=[("Omeprazole, the most studied prototype", "Omeprazole inhibits CYP2C19 (S13)."),
                      ("Esomeprazole, the S-isomer of omeprazole", "Also inhibits CYP2C19 (S14)."),
                      ("Cimetidine, since it is not a PPI", "A broad CYP inhibitor (S11)."),
                      ("Any PPI — none interact with clopidogrel", "Several do (p. 1161).")],
         src="p. 1161"),
]

COMPARISONS = {
    EMES: [
        {"title": "Prokinetic agents in the reading (textbook)", "columns": ["Drug", "How it speeds the gut", "Point"],
         "rows": [["Metoclopramide, domperidone", "D2 blockade removes dopamine’s brake on cholinergic stimulation", "Gastroparesis first-line; domperidone barely enters the brain"],
                  ["Cholinomimetic agents: bethanechol, neostigmine", "M3 agonist; acetylcholinesterase inhibitor", "Bethanechol seldom used; IV neostigmine for acute colonic pseudo-obstruction"],
                  ["Macrolides (erythromycin)", "Motilin receptor agonist", "Gastroparesis trial; tolerance develops rapidly"]],
         "src": "p. 1163; p. 1164"},
    ],
}

DEEPER = {
    ANTI: (62, 1153, 1161, "Antacids, H2 blockers and PPIs: pharmacokinetics, uses, and long-term safety"),
    PROT: (62, 1161, 1162, "Sucralfate, misoprostol, bismuth and H. pylori regimens"),
    EMES: (62, 1162, 1172, "Prokinetics and every antiemetic class"),
}

_L06_CH62 = ["BULK-FORMING LAXATIVES", "STOOL SURFACTANT AGENTS (SOFTENERS)", "OSMOTIC LAXATIVES", "Balanced Polyethylene Glycol", "STIMULANT LAXATIVES",
             "Anthraquinone Derivatives", "Diphenylmethane Derivatives", "CHLORIDE SECRETION ACTIVATORS", "OPIOID RECEPTOR ANTAGONISTS",
             "SEROTONIN 5-HT 4-RECEPTOR AGONISTS", "ANTIDIARRHEAL AGENTS", "OPIOID AGONISTS", "COLLOIDAL BISMUTH COMPOUNDS", "BILE SAL T-BINDING RESINS",
             "OCTREOTIDE", "ANTISPASMODICS (ANTICHOLINERGICS)", "SEROTONIN 5-HT 3-RECEPTOR ANTAGONISTS", "CHLORIDE CHANNEL ACTIVATORS",
             "DRUGS USED TO TREAT INFLAMMATORY BOWEL DISEASE (IBD)", "Chemistry & Formulations", "Infliximab Adalimumab Certolizumab Golimumab",
             "ANTI-INTEGRIN THERAPY", "ANTI–IL-23 THERAPY", "JANUS KINASE INHIBITORS", "PANCREATIC ENZYME SUPPLEMENTS",
             "GLUCAGON-LIKE PEPTIDE 2 ANALOG FOR SHORT-BOWEL SYNDROME", "BILE ACID AGENTS", "DRUGS USED TO TREAT VARICEAL HEMORRHAGE",
             "SOMATOSTATIN & OCTREOTIDE", "VASOPRESSIN & TERLIPRESSIN", "BETA-RECEPTOR-BLOCKING DRUGS", "PANCREATIC SUPPLEMENTS"]
_L06_CH65 = ["Candy Tsourounis, PharmD", "HISTORIC & REGULATORY FACTORS", "Pharmacologic Effects", "Clinical Trials", "Drug Interactions & Precautions",
             "Drug Interactions, Precautions, & Dosage", "PURIFIED NUTRITIONAL SUPPLEMENTS COENZYME Q10", "GLUCOSAMINE",
             "Pharmacologic Effects & Clinical Uses", "MELATONIN"]
_REFS = ["Acid-Peptic Diseases", "Motility Disorders", "Drugs Used for Irritable Bowel Syndrome", "Drugs Used for Inflammatory Bowel Disease",
         "Drugs for Portal Hypertension", "Drugs for Short-Bowel Syndrome"]

READING_SKIP = (
    [{"heading": h, "reason": "Taught in L06 (Session 2: bowel disorders, IBD, and GI drugs, Ch. 62)"} for h in _L06_CH62]
    + [{"heading": h, "reason": "Taught in L06 (Session 2: dietary supplements and herbal medications, Ch. 65)"} for h in _L06_CH65]
    + [{"heading": h, "reason": "Reference-list heading (citations only, no teaching content)"} for h in _REFS]
    + [{"heading": "INTRODUCTION", "reason": "Chapter introduction (orientation paragraph, no drug content)"},
       {"heading": "GENERIC NAME AVAILABLE AS ANTACIDS", "reason": "Preparations list (brand names only, no teaching content)"},
       {"heading": "GENERIC NAME AVAILABLE AS", "reason": "Preparations list (brand names only, no teaching content)"},
       {"heading": "Toxicities, Interactions", "reason": "Chapter summary-table column heading; the drugs are taught in their own sections"}]
)
