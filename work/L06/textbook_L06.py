"""Textbook (Katzung 16e — Ch. 62 bowel/IBD/other GI sections and Ch. 65 dietary supplements) additions for L06.
The acid-peptic, prokinetic and antiemetic sections of Ch. 62 are taught in Session 1 (L05)."""

LAX = "Laxatives & Antidiarrheals"
IBD = "Inflammatory Bowel Disease"
NUT = "Nutrition, Vitamins & Dietary Supplements"

ADD = {
    LAX: {
        "moa": [
            ("Opioid receptor antagonists (methylnaltrexone, naloxegol, naldemedine, alvimopan) block gut μ-receptors without entering the CNS, so analgesia is kept.", "p. 1166"),
        ],
        "adverse": [
            ("Mineral oil: aspiration causes lipid pneumonitis; long-term use impairs fat-soluble vitamin absorption.", "p. 1164"),
            ("Sodium phosphate purgatives risk electrolyte shifts and acute renal failure — avoid in frail, elderly or renal patients.", "p. 1165"),
        ],
        "contra": [
            ("Antidiarrheals should not be used with bloody diarrhea, high fever, or systemic toxicity.", "p. 1166"),
        ],
        "pk": [
            ("Senna works in 6–12 hours orally; bisacodyl in 6–10 hours orally and 30–60 minutes rectally.", "p. 1165"),
        ],
    },
    IBD: {
        "moa": [
            ("**Chemistry & formulations:** azo compounds (sulfasalazine, balsalazide, olsalazine) are cleaved by colonic bacteria; mesalamine formulations release 5-ASA at set pH or times.", "p. 1173"),
        ],
        "adverse": [
            ("Up to 40% cannot tolerate therapeutic sulfasalazine doses; give 1 mg/d folic acid; reversible oligospermia.", "p. 1174"),
            ("Anti-TNF: TB reactivation — test before starting; antibodies to the drug reduce response; infliximab infusion reactions in up to 10%.", "p. 1177"),
            ("Tofacitinib: fourfold herpes zoster reactivation (vaccinate first); check lipids at 8 weeks.", "p. 1178"),
        ],
        "contra": [
            ("No azathioprine/6-MP with absent TPMT activity (low in 11%, absent in 0.3%).", "p. 1175"),
        ],
        "pk": [
            ("Thiopurines take a median 17 weeks to benefit; budesonide bioavailability about 10% (CYP3A4 inhibitors raise it).", "p. 1174; p. 1175"),
        ],
        "indications": [
            ("Corticosteroids: prednisone 40–60 mg/d for flares, tapered after response; rectal forms for distal disease; not for maintenance.", "p. 1174; p. 1175"),
        ],
    },
    NUT: {
        "interactions": [
            ("St. John’s wort activates PXR, inducing CYP 3A4, 2C9, 1A2 and P-glycoprotein: lowers digoxin, birth control, cyclosporine, HIV drugs, warfarin; serotonin syndrome with antidepressants.", "p. 1214"),
            ("Garlic, ginkgo and ginseng have antiplatelet effects — avoid or monitor with anticoagulants and around surgery.", "p. 1208; p. 1210; p. 1211"),
            ("Coenzyme Q10 and melatonin may decrease warfarin’s effect; glucosamine may increase the INR.", "p. 1216; p. 1218"),
        ],
        "pearls": [
            ("Under DSHEA (1994), supplements are regulated as foods: the FDA must prove a product harmful before restricting it.", "p. 1204"),
        ],
    },
}

CONFLICTS = {
    LAX: [
        {"topic": "Age cutoff for diphenoxylate/atropine",
         "slides": {"text": "Avoid in children under 2 (S7 notes); under 6 (S8, S49).", "src": "S7 (notes); S8; S49"},
         "textbook": {"text": "Small amounts of atropine are added to discourage overdosage (no age cutoff given).", "src": "p. 1166"}},
    ],
    IBD: [
        {"topic": "Thiopurine onset",
         "slides": {"text": "Onset takes weeks to months (azathioprine 8–12 weeks).", "src": "S15; S54"},
         "textbook": {"text": "A median delay of 17 weeks before benefit.", "src": "p. 1175"}},
    ],
}

DISCREPANCIES = [
    ("**Diphenoxylate/atropine age limit:** the speaker notes say under 2; the depth slide and drug profile say under 6. Use under 6 (the profile).", "S7 (notes); S8; S49"),
    ("**Thiopurine onset:** slides say weeks to months (8–12 weeks on the profile); the textbook gives a median of 17 weeks. Either way, not for acute flares.", "S14; S54; p. 1175"),
]

CRAM = [
    ("Opioid-induced constipation", "Methylnaltrexone, naloxegol, naldemedine (peripheral μ blockers)", "p. 1166"),
    ("Sulfasalazine intolerance", "Up to 40%; folic acid 1 mg/d", "p. 1174"),
    ("TPMT", "Low in 11%, absent in 0.3% — absent = no thiopurine", "p. 1175"),
    ("Tofacitinib extras", "Zoster ×4 (vaccinate), lipids at 8 weeks", "p. 1178"),
    ("St. John’s wort mechanism", "PXR → CYP 3A4, 2C9, 1A2 + P-gp induction", "p. 1214"),
    ("Antiplatelet herbs", "Garlic, ginkgo, ginseng", "p. 1208; p. 1210; p. 1211"),
    ("Warfarin and supplements", "CoQ10, melatonin ↓ effect; glucosamine ↑ INR", "p. 1216; p. 1218"),
]

QUESTIONS = [
    dict(topic=NUT, kind="vignette",
         stem="A patient on warfarin starts glucosamine for knee arthritis. What does the textbook warn?",
         correct="The INR may rise, increasing bleeding risk",
         why_correct="Glucosamine sulfate may increase the INR in patients taking warfarin; avoid or monitor carefully (p. 1216).",
         distractors=[("The INR will fall from CYP3A4 induction", "That is St. John’s wort (p. 1214)."),
                      ("Glucosamine supplies vitamin K and lowers INR", "CoQ10 is the vitamin K–like one (p. 1216)."),
                      ("No interaction — glucosamine is a food", "An INR interaction is reported (p. 1216)."),
                      ("Serotonin syndrome with warfarin", "Not a glucosamine effect (p. 1216).")],
         src="p. 1216"),
]

COMPARISONS = {
    LAX: [
        {"title": "Other bowel drugs in the reading (textbook)", "columns": ["Group", "Drugs", "Point"],
         "rows": [["Bulk-forming laxatives", "Psyllium, methylcellulose, polycarbophil", "Hydrophilic gel distends colon; bloating, flatus"],
                  ["Stool surfactant agents (softeners)", "Docusate, glycerin, mineral oil", "Mineral oil: lipid pneumonitis if aspirated"],
                  ["Osmotic laxatives; balanced polyethylene glycol", "Magnesium, sorbitol, lactulose; PEG lavage", "PEG causes no significant cramps or flatus; bowel prep 1–2 L"],
                  ["Stimulant laxatives: anthraquinone and diphenylmethane derivatives", "Senna, cascara (melanosis coli); bisacodyl", "Long-term use probably safe in most"],
                  ["Chloride secretion activators", "Lubiprostone (ClC-2); linaclotide, plecanatide (GC-C)", "Nausea up to 30% (lubiprostone); diarrhea up to 20% (linaclotide)"],
                  ["Opioid receptor antagonists", "Methylnaltrexone, naloxegol, naldemedine, alvimopan", "Opioid-induced constipation; alvimopan postoperative ileus only"],
                  ["Serotonin 5-HT4-receptor agonists", "Prucalopride", "Chronic constipation; 1 mg/day if CrCl < 30"],
                  ["Antidiarrheal agents: opioid agonists", "Loperamide, diphenoxylate, eluxadoline", "Eluxadoline: IBS-D; sphincter of Oddi spasm"],
                  ["Colloidal bismuth compounds", "Bismuth subsalicylate", "Traveler’s diarrhea"],
                  ["Bile salt-binding resins", "Cholestyramine, colestipol, colesevelam", "Bile-acid diarrhea; separate other drugs by 2 hours"],
                  ["Octreotide", "Somatostatin analog", "Secretory tumor diarrhea; gallstones with long-term use"],
                  ["IBS: antispasmodics (anticholinergics)", "Dicyclomine, hyoscyamine", "Short-term pain relief; anticholinergic effects"],
                  ["IBS: serotonin 5-HT3-receptor antagonists", "Alosetron", "Women with severe IBS-D; ischemic colitis, severe constipation"],
                  ["IBS: chloride channel activators", "Lubiprostone 8 mcg twice daily; linaclotide 290 mcg", "IBS-C"]],
         "src": "p. 1164; p. 1165; p. 1166; p. 1167; p. 1168"},
    ],
    IBD: [
        {"title": "IBD and other GI drugs in the reading (textbook)", "columns": ["Drug / group", "Mechanism", "Point"],
         "rows": [["Infliximab, adalimumab, certolizumab, golimumab", "Anti-TNF antibodies", "Screen TB first; certolizumab lacks an Fc portion"],
                  ["Anti-integrin therapy: vedolizumab (natalizumab)", "α4β7 (α4) integrin block", "Natalizumab risks PML; vedolizumab PML risk extremely low"],
                  ["Anti-IL-23 therapy: ustekinumab, risankizumab", "IL-12/23 p40; IL-23 p19", "Risankizumab: drug-induced liver injury (check LFTs)"],
                  ["Janus kinase inhibitors: tofacitinib, upadacitinib", "JAK-STAT", "Boxed: heart attack, stroke, thrombosis, cancer, death"],
                  ["Ozanimod", "Sphingosine-1-phosphate receptor agonist", "Bradyarrhythmia, macular edema; ECG first"],
                  ["Pancreatic enzyme supplements (pancrelipase)", "Lipase, amylase, protease replacement", "With every meal; swallow, don’t chew"],
                  ["Glucagon-like peptide 2 analog for short-bowel syndrome (teduglutide)", "Mucosal growth", "Cuts parenteral support; neoplasia risk"],
                  ["Bile acid agents: ursodiol, obeticholic acid", "Lower bile cholesterol; FXR ligand", "Gallstone dissolution; primary biliary cirrhosis"],
                  ["Drugs used to treat variceal hemorrhage: somatostatin & octreotide", "Reduce portal blood flow", "Acute variceal bleeding for 3–5 days"],
                  ["Vasopressin & terlipressin", "Splanchnic vasoconstriction", "Vasopressin: ischemia, hyponatremia"],
                  ["Beta-receptor-blocking drugs (propranolol, nadolol)", "Nonselective β block lowers portal inflow", "Prevent variceal bleeding (15% vs 25%)"]],
         "src": "p. 1176; p. 1177; p. 1178; p. 1179; p. 1180"},
    ],
    NUT: [
        {"title": "Dietary supplements in the reading (textbook)", "columns": ["Supplement", "Pharmacologic effects & clinical uses (clinical trials)", "Drug interactions, precautions & dosage"],
         "rows": [["Historic & regulatory factors", "DSHEA (1994): regulated as foods; GMP rule only in 2007", "FDA must prove harm to restrict; serious adverse events must be reported"],
                  ["Echinacea", "Cold prevention (mixed trials)", "Avoid in immune deficiency, autoimmune disease, immunosuppression; ≤ 10–14 days"],
                  ["Garlic", "Modest lipid lowering", "Antiplatelet: caution with warfarin, aspirin, ibuprofen"],
                  ["Ginkgo", "Dementia (240 mg/d extract)", "Antiplatelet: avoid with anticoagulants; avoid in seizure disorders"],
                  ["Ginseng", "Glucose, fatigue", "Antiplatelet; mania with phenelzine, lithium, neuroleptics"],
                  ["Milk thistle", "Liver disease (no proven benefit)", "No significant drug interactions"],
                  ["St. John’s wort", "Mild-moderate depression (900 mg/d)", "CYP/P-gp induction; serotonin syndrome"],
                  ["Saw palmetto", "BPH symptoms (160 mg twice daily)", "No drug interactions reported"],
                  ["Purified nutritional supplements: coenzyme Q10", "Low endogenous levels; heart failure", "Vitamin K–like: may decrease warfarin effect"],
                  ["Glucosamine", "Osteoarthritis (1500 mg daily)", "May increase INR with warfarin"],
                  ["Melatonin", "Jet lag (0.5–5 mg), insomnia", "CYP1A2 (fluvoxamine); may decrease warfarin effect"]],
         "src": "p. 1204; p. 1207; p. 1208; p. 1210; p. 1211; p. 1213; p. 1214; p. 1215; p. 1216; p. 1217; p. 1218"},
    ],
}

DEEPER = {
    LAX: (62, 1164, 1169, "Every laxative, antidiarrheal and IBS drug"),
    IBD: (62, 1172, 1180, "IBD drugs plus pancreatic, bile acid and variceal-bleeding drugs"),
    NUT: (65, 1203, 1218, "Regulation of supplements and the major herbs"),
}

_L05 = ["DRUGS USED IN ACID-PEPTIC DISEASES", "Physiology of Acid Secretion", "H2-Receptor Antagonists", "Lansoprazole Rabeprazole", "MUCOSAL PROTECTIVE AGENTS",
        "DRUGS STIMULATING GASTROINTESTINAL MOTILITY", "Physiology of the Enteric Nervous System", "CHOLINOMIMETIC AGENTS", "METOCLOPRAMIDE & DOMPERIDONE",
        "Clinical Uses", "Adverse Effects", "MACROLIDES", "ANTIEMETIC AGENTS", "PATHOPHYSIOLOGY", "Pharmacokinetics & Pharmacodynamics", "CORTICOSTEROIDS",
        "NEUROKININ RECEPTOR ANTAGONISTS", "Adverse Effects & Drug Interactions",
        "ANTIPSYCHOTIC AGENTS AS ANTIEMETICS (PHENOTHIAZINES, BUTYROPHENONES, & THIENOBENZODIAZEPINES)", "SUBSTITUTED BENZAMIDES",
        "H1 ANTIHISTAMINES & ANTICHOLINERGIC DRUGS", "BENZODIAZEPINES", "CANNABINOIDS"]
_REFS = ["Acid-Peptic Diseases", "Motility Disorders", "Drugs Used for Irritable Bowel Syndrome", "Drugs Used for Inflammatory Bowel Disease",
         "Drugs for Portal Hypertension", "Drugs for Short-Bowel Syndrome"]

READING_SKIP = (
    [{"heading": h, "reason": "Taught in L05 (Session 1: acid-peptic disease, prokinetics, antiemetics, Ch. 62)"} for h in _L05]
    + [{"heading": h, "reason": "Reference-list heading (citations only, no teaching content)"} for h in _REFS]
    + [{"heading": "INTRODUCTION", "reason": "Chapter introduction (orientation paragraph, no drug content)"},
       {"heading": "Candy Tsourounis, PharmD", "reason": "Chapter author byline (no teaching content; no names on the site)"},
       {"heading": "GENERIC NAME AVAILABLE AS ANTACIDS", "reason": "Preparations list (brand names only, no teaching content)"},
       {"heading": "GENERIC NAME AVAILABLE AS", "reason": "Preparations list (brand names only, no teaching content)"},
       {"heading": "Toxicities, Interactions", "reason": "Chapter summary-table column heading; the drugs are taught in their own sections"}]
)
