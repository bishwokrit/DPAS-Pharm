"""Study-guide extras for L07 (summary, flows, cram sheet). Imported by author_L07.py."""

TEASER = "Today: one feedback template for the whole endocrine unit, then pituitary drugs for GH, prolactin and water balance, thyroid replacement and antithyroid drugs including thyroid storm, and steroids — why they are tapered and how adrenal crisis is treated."

SUMMARY = [
    ("One **axis** (hypothalamus → pituitary → gland) with **negative feedback**: every exogenous hormone suppresses the levels above it.", "S5; SG U4-R1"),
    ("**Acromegaly**: octreotide/lanreotide or pegvisomant (monitor IGF-1); **prolactinoma**: cabergoline; **DI**: desmopressin (hyponatremia); **SIADH**: fluid restriction, then tolvaptan (start in hospital).", "S6; S8; S10; SG U4-R2; SG U4-R3; SG U4-R4"),
    ("**Levothyroxine**: empty stomach, separate calcium/iron/antacids by 4 h, TSH at 6–8 weeks, start low in older/cardiac patients.", "S12; S13; SG U4-R5"),
    ("**Methimazole** first line; **PTU** in the first trimester and **thyroid storm** (also blocks T4→T3); fever/sore throat → CBC.", "S15; SG U4-R6"),
    ("**Thyroid storm**: beta-blocker + PTU first, **iodine after**, steroids too.", "S16; S18; SG U4-R7"),
    ("**Chronic steroids** suppress CRH/ACTH → **taper**; abrupt stop → adrenal crisis → IV hydrocortisone + fluids. Antagonists: ketoconazole, metyrapone, mifepristone, spironolactone.", "S22; S23; S27; SG U4-R8; SG U4-R9"),
]

FLOWS = {
    "Thyroid & Antithyroid Drugs": [
        {"title": "Thyroid storm sequence", "steps": ["Recognize: fever, tachycardia, altered mental status in Graves", "Propranolol (avoid in asthma/decompensated HF)", "PTU: blocks synthesis and T4→T3", "Iodine at least 1 hour after PTU", "Steroids; fluids, cooling; no aspirin"], "src": "S16; S17; S18"},
    ],
    "Adrenocorticosteroids & Antagonists": [
        {"title": "Chronic steroid patient", "steps": ["On steroids > 2 weeks → assume HPA suppression", "Stopping → taper, never abruptly", "Missed doses + hypotension, confusion → adrenal crisis", "IV hydrocortisone + IV fluids (emergency)", "Addison disease: glucocorticoid + fludrocortisone"], "src": "S20; S22; S27; p. 750"},
    ],
}

CRAM = [
    ("Axis rule", "Hormone feeds back to suppress the levels above", "S5; SG U4-R1"),
    ("Acromegaly drugs", "Octreotide, lanreotide, pegvisomant (IGF-1), cabergoline", "S6; S7"),
    ("Octreotide AEs", "GI upset, gallstones, bradycardia", "S7"),
    ("Prolactinoma", "Cabergoline (twice weekly) or bromocriptine", "S8; S9"),
    ("DI vs SIADH", "Desmopressin (hyponatremia) · fluid restriction, tolvaptan", "S8; S10"),
    ("Levothyroxine", "Empty stomach; separate Ca/Fe/antacids 4 h; TSH 6–8 weeks", "S12; S13"),
    ("Over-replacement", "AF, bone loss", "S13"),
    ("Methimazole vs PTU", "First line · first trimester and storm", "S15"),
    ("Thionamide + fever/sore throat", "Stop, check CBC (agranulocytosis)", "S15 (notes)"),
    ("Storm order", "Beta-blocker + PTU → iodine ≥ 1 h later → steroids", "S16; S17"),
    ("Steroid potency", "Prednisone ~4×, dexamethasone ~25–30× hydrocortisone", "S21"),
    ("Adrenal crisis", "IV hydrocortisone + IV fluids", "S27"),
    ("Addison disease", "Glucocorticoid + fludrocortisone", "S20"),
    ("Cushing drugs", "Ketoconazole, metyrapone (synthesis); mifepristone (receptor)", "S23"),
]
