"""Study-guide extras for L05 (summary, flows, cram sheet). Imported by author_L05.py."""

TEASER = "Today: why PPIs out-suppress H2 blockers, the long-term PPI risks, choosing an H. pylori regimen, and matching each antiemetic to its receptor. One cited guide, every drug profile, and exam-style practice."

SUMMARY = [
    ("Acid-peptic disease is a **balance**: acid, pepsin, H. pylori and NSAIDs push against mucus, bicarbonate, prostaglandins and epithelial turnover.", "S5; SG U3-R1"),
    ("Gastrin, histamine and acetylcholine converge on the **proton pump**: **H2 blockers** cut one input, **PPIs** block the final common pathway, **antacids** neutralize acid already made.", "S8; S12; SG U3-R2"),
    ("PPIs are the most potent but carry long-term risks — **B12 deficiency, hypomagnesemia, fractures, C. difficile** — and omeprazole blunts **clopidogrel** via CYP2C19.", "S15; SG U3-R3; SG U3-R4"),
    ("**Sucralfate** shields the ulcer base (needs acid); **misoprostol** restores prostaglandins for NSAID-ulcer prevention but is **contraindicated in pregnancy**.", "S20; SG U3-R5"),
    ("**H. pylori** needs eradication: triple therapy, or **bismuth quadruple** with penicillin allergy, recent macrolide, or clarithromycin resistance; test of cure ≥ 4 weeks later, off the PPI 2 weeks.", "S23; S25; SG U3-R6"),
    ("Antiemetics block one input to the vomiting center: **5-HT3** (ondansetron), **D2** (metoclopramide — boxed tardive dyskinesia), **NK1** (aprepitant), **H1/M1** (meclizine, scopolamine — motion sickness), plus **CB1** (dronabinol).", "S30; S36; S38; SG U3-R7; SG U3-R8"),
]

FLOWS = {
    "Acid-Peptic Disease & Gastric Acid Secretion": [
        {"title": "How the mucosa gets injured", "steps": ["Aggressive factors: acid, pepsin, H. pylori, NSAIDs", "Overwhelm mucus, bicarbonate, prostaglandin blood flow", "Mucosal injury", "GERD, ulcer or gastritis"], "src": "S6"},
    ],
    "Antacids, H2 Blockers & Proton Pump Inhibitors": [
        {"title": "PPI activation", "steps": ["Enteric-coated prodrug absorbed in the small intestine", "Reaches the parietal cell canaliculus", "Activated by acid", "Binds cysteine on H+/K+ ATPase covalently", "Pump blocked until new pumps are made"], "src": "S16"},
        {"title": "H2 blocker action", "steps": ["Histamine from ECL cells", "Binds H2 receptor on the parietal cell", "Raises cAMP", "Stimulates the proton pump", "Famotidine competes at the receptor → less acid"], "src": "S14"},
    ],
    "Mucosal Protectants & H. pylori Eradication": [
        {"title": "H. pylori decision", "steps": ["Confirmed H. pylori", "Penicillin allergy or macrolide in recent months?", "No → PPI + amoxicillin + clarithromycin, 14 days", "Yes → bismuth quadruple: PPI + bismuth + metronidazole + tetracycline", "Test of cure ≥ 4 weeks later, PPI held 2 weeks"], "src": "S23; S25"},
    ],
    "Antiemetics": [
        {"title": "Pick the antiemetic by the trigger", "steps": ["Chemotherapy / gut irritation → 5-HT3 (+ NK1 + dexamethasone)", "CTZ / drugs → D2 or NK1", "Motion sickness → H1/M1 (meclizine, scopolamine)", "Anticipatory → benzodiazepine", "Refractory CINV → dronabinol"], "src": "S32; S38"},
    ],
}

CRAM = [
    ("Aggressive factors", "Acid, pepsin, H. pylori, NSAIDs", "S5; SG U3-R1"),
    ("Protective factors", "Mucus–bicarbonate, prostaglandins, epithelial turnover", "S5; SG U3-R1"),
    ("Antacids", "Neutralize acid; fast, short; separate drugs by 2 h", "S12"),
    ("Al vs. Mg vs. Ca antacid", "Al constipates · Mg diarrhea (caution CKD) · Ca constipates, milk-alkali", "S12"),
    ("Famotidine", "H2 block; renal dosing; confusion in older adults; minimal CYP", "S13; S14"),
    ("Cimetidine", "CYP inhibitor (1A2, 2C19, 3A4); gynecomastia", "S13; S14"),
    ("H2 blocker strength", "Nocturnal acid; tachyphylaxis", "S14"),
    ("PPI mechanism", "Irreversible H+/K+-ATPase block (final common pathway)", "S15; SG U3-R2"),
    ("PPI timing", "30–60 min before the first meal", "S15; S16"),
    ("Long-term PPI risks", "B12, Mg, fractures, C. difficile, pneumonia, interstitial nephritis, rebound acid", "S15; S16; SG U3-R3"),
    ("Omeprazole + clopidogrel", "CYP2C19 inhibition blunts activation", "S15; SG U3-R4"),
    ("Sucralfate", "Barrier in acid; 2 h from other drugs; aluminum in CKD", "S20; S21"),
    ("Misoprostol", "PGE1 analog; NSAID ulcers; NOT in pregnancy; diarrhea", "S20; SG U3-R5"),
    ("Triple therapy", "PPI + amoxicillin + clarithromycin, 14 days", "S23"),
    ("Bismuth quadruple", "PPI + bismuth + metronidazole + tetracycline", "S23; SG U3-R6"),
    ("Penicillin allergy (triple)", "Metronidazole replaces amoxicillin", "S23"),
    ("Test of cure", "≥ 4 weeks after; PPI held 2 weeks", "S23; S24"),
    ("Clarithromycin / metronidazole", "CYP3A4 (statins) / disulfiram-like with alcohol", "S24"),
    ("Antiemetic targets", "5-HT3 ondansetron · D2 metoclopramide · NK1 aprepitant · H1/M1 meclizine, scopolamine · CB1 dronabinol", "S30; SG U3-M"),
    ("Motion sickness", "Vestibular → H1/M1", "S33; SG U3-R7"),
    ("Ondansetron", "QT; constipation; serotonin syndrome; give before chemo", "S31"),
    ("Metoclopramide", "Boxed tardive dyskinesia; ≤ 12 weeks; no obstruction/Parkinson", "S36; S37; SG U3-R8"),
    ("Chemo combo", "5-HT3 + NK1 + dexamethasone", "S32"),
    ("Pregnancy nausea", "Pyridoxine (B6) ± doxylamine first-line", "S40"),
    ("Cannabinoids", "CB1; dronabinol C-III, nabilone C-II", "S38; S39"),
    ("Stems", "-prazole PPI · -tidine H2 · -prostol PG · -setron 5-HT3 · -pitant NK1 · -izine H1", "S28; S43"),
]
