"""Study-guide extras for L05 (summary, flows, cram sheet). Imported by author_L05.py."""

TEASER = "Today: why PPIs out-suppress H2 blockers, the long-term PPI risks, choosing an H. pylori regimen, and matching each antiemetic to its receptor. One cited guide, every drug profile, and exam-style practice."

SUMMARY = [
    ("Acid-peptic disease is a **balance**: acid, pepsin, H. pylori and NSAIDs push against mucus, bicarbonate, prostaglandins and epithelial turnover.", "S5; SG U3-R1"),
    ("Gastrin, histamine and acetylcholine converge on the **proton pump**: **H2 blockers** cut one input, **PPIs** block the final common pathway, **antacids** neutralize acid already made.", "S8; S10; SG U3-R2"),
    ("PPIs are the most potent but carry long-term risks — **B12 deficiency, hypomagnesemia, fractures, C. difficile** — and omeprazole blunts **clopidogrel** via CYP2C19.", "S13; SG U3-R3; SG U3-R4"),
    ("**Sucralfate** shields the ulcer base (needs acid); **misoprostol** restores prostaglandins for NSAID-ulcer prevention but is **contraindicated in pregnancy**.", "S16; SG U3-R5"),
    ("**H. pylori** needs eradication: triple therapy, or **bismuth quadruple** with penicillin allergy, recent macrolide, or clarithromycin resistance; test of cure ≥ 4 weeks later, off the PPI 2 weeks.", "S19; S21; SG U3-R6"),
    ("Antiemetics block one input to the vomiting center: **5-HT3** (ondansetron), **D2** (metoclopramide — boxed tardive dyskinesia), **NK1** (aprepitant), **H1/M1** (meclizine, scopolamine — motion sickness), plus **CB1** (dronabinol).", "S24; S28; S30; SG U3-R7; SG U3-R8"),
]

FLOWS = {
    "Acid-Peptic Disease & Gastric Acid Secretion": [
        {"title": "How the mucosa gets injured", "steps": ["Aggressive factors: acid, pepsin, H. pylori, NSAIDs", "Overwhelm mucus, bicarbonate, prostaglandin blood flow", "Mucosal injury", "GERD, ulcer or gastritis"], "src": "S6"},
    ],
    "Antacids, H2 Blockers & Proton Pump Inhibitors": [
        {"title": "PPI activation", "steps": ["Enteric-coated prodrug absorbed in the small intestine", "Reaches the parietal cell canaliculus", "Activated by acid", "Binds cysteine on H+/K+ ATPase covalently", "Pump blocked until new pumps are made"], "src": "S14"},
        {"title": "H2 blocker action", "steps": ["Histamine from ECL cells", "Binds H2 receptor on the parietal cell", "Raises cAMP", "Stimulates the proton pump", "Famotidine competes at the receptor → less acid"], "src": "S12"},
    ],
    "Mucosal Protectants & H. pylori Eradication": [
        {"title": "H. pylori decision", "steps": ["Confirmed H. pylori", "Penicillin allergy or macrolide in recent months?", "No → PPI + amoxicillin + clarithromycin, 14 days", "Yes → bismuth quadruple: PPI + bismuth + metronidazole + tetracycline", "Test of cure ≥ 4 weeks later, PPI held 2 weeks"], "src": "S19; S21"},
    ],
    "Antiemetics": [
        {"title": "Pick the antiemetic by the trigger", "steps": ["Chemotherapy / gut irritation → 5-HT3 (+ NK1 + dexamethasone)", "CTZ / drugs → D2 or NK1", "Motion sickness → H1/M1 (meclizine, scopolamine)", "Anticipatory → benzodiazepine", "Refractory CINV → dronabinol"], "src": "S26; S30"},
    ],
}

CRAM = [
    ("Aggressive factors", "Acid, pepsin, H. pylori, NSAIDs", "S5; SG U3-R1"),
    ("Protective factors", "Mucus–bicarbonate, prostaglandins, epithelial turnover", "S5; SG U3-R1"),
    ("Antacids", "Neutralize acid; fast, short; separate drugs by 2 h", "S10"),
    ("Al vs. Mg vs. Ca antacid", "Al constipates · Mg diarrhea (caution CKD) · Ca constipates, milk-alkali", "S10"),
    ("Famotidine", "H2 block; renal dosing; confusion in older adults; minimal CYP", "S11; S12"),
    ("Cimetidine", "CYP inhibitor (1A2, 2C19, 3A4); gynecomastia", "S11; S12"),
    ("H2 blocker strength", "Nocturnal acid; tachyphylaxis", "S12"),
    ("PPI mechanism", "Irreversible H+/K+-ATPase block (final common pathway)", "S13; SG U3-R2"),
    ("PPI timing", "30–60 min before the first meal", "S13; S14"),
    ("Long-term PPI risks", "B12, Mg, fractures, C. difficile, pneumonia, interstitial nephritis, rebound acid", "S13; S14; SG U3-R3"),
    ("Omeprazole + clopidogrel", "CYP2C19 inhibition blunts activation", "S13; SG U3-R4"),
    ("Sucralfate", "Barrier in acid; 2 h from other drugs; aluminum in CKD", "S16; S17"),
    ("Misoprostol", "PGE1 analog; NSAID ulcers; NOT in pregnancy; diarrhea", "S16; SG U3-R5"),
    ("Triple therapy", "PPI + amoxicillin + clarithromycin, 14 days", "S19"),
    ("Bismuth quadruple", "PPI + bismuth + metronidazole + tetracycline", "S19; SG U3-R6"),
    ("Penicillin allergy (triple)", "Metronidazole replaces amoxicillin", "S19"),
    ("Test of cure", "≥ 4 weeks after; PPI held 2 weeks", "S19; S20"),
    ("Clarithromycin / metronidazole", "CYP3A4 (statins) / disulfiram-like with alcohol", "S20"),
    ("Antiemetic targets", "5-HT3 ondansetron · D2 metoclopramide · NK1 aprepitant · H1/M1 meclizine, scopolamine · CB1 dronabinol", "S24; SG U3-M"),
    ("Motion sickness", "Vestibular → H1/M1", "S27; SG U3-R7"),
    ("Ondansetron", "QT; constipation; serotonin syndrome; give before chemo", "S25"),
    ("Metoclopramide", "Boxed tardive dyskinesia; ≤ 12 weeks; no obstruction/Parkinson", "S28; S29; SG U3-R8"),
    ("Chemo combo", "5-HT3 + NK1 + dexamethasone", "S26"),
    ("Pregnancy nausea", "Pyridoxine (B6) ± doxylamine first-line", "S32"),
    ("Cannabinoids", "CB1; dronabinol C-III, nabilone C-II", "S30; S31"),
    ("Stems", "-prazole PPI · -tidine H2 · -prostol PG · -setron 5-HT3 · -pitant NK1 · -izine H1", "S22; S33"),
]
