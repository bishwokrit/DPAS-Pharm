"""Study-guide extras for L06 (summary, flows, cram sheet). Imported by author_L06.py."""

TEASER = "Today: the four laxative buckets and when not to stop diarrhea, IBD step therapy from mesalamine to biologics, and how vitamins and supplements change drug therapy. One cited guide, every drug profile, and the recall quiz rebuilt."

SUMMARY = [
    ("Laxatives fall into four buckets — **bulk-forming** (slowest, safest), **osmotic** (fast; PEG first-line), **stimulant** (short-term), **secretagogue** (IBS-C) — and osmotic/stimulant act in hours, bulk-forming in days.", "S4; S6; SG U3-R9"),
    ("**Loperamide** and **diphenoxylate/atropine** slow the gut via mu receptors; never use them in **C. difficile** or bloody/febrile diarrhea, and atropine is there to deter misuse.", "S7; S9; SG U3-R10"),
    ("IBD therapy **steps up with severity**: 5-ASA → short-term steroids → thiopurines for maintenance (test TPMT/NUDT15; cut dose with allopurinol) → biologics/small molecules.", "S11; S14; S15; SG U3-R11"),
    ("Biologics share **immunosuppression risk**: screen TB and hepatitis B/C and update vaccines first; **vedolizumab** is the gut-selective one.", "S16; S18; SG U3-R11"),
    ("**Fat-soluble** vitamins (A, D, E, K) accumulate; water-soluble are excreted. Long-term **PPI or metformin** → check **B12**; refeed slowly with thiamine.", "S22; S25; S29; SG U3-R12"),
    ("Warfarin’s effect falls with **dietary vitamin K** (pharmacodynamic) and with **St. John’s wort** (CYP3A4 induction, pharmacokinetic); ginkgo and fish oil raise bleeding — always ask about supplements.", "S26; S27; S30; SG U3-R13"),
]

FLOWS = {
    "Laxatives & Antidiarrheals": [
        {"title": "Diarrhea: is an antimotility agent safe?", "steps": ["Bloody stool, fever, or recent antibiotics?", "Yes → suspect C. difficile / invasive infection", "Avoid loperamide and diphenoxylate", "Treat the cause (oral vancomycin or fidaxomicin)", "No red flags → loperamide is reasonable"], "src": "S7; S9"},
    ],
    "Inflammatory Bowel Disease": [
        {"title": "IBD step therapy", "steps": ["Mild UC → mesalamine", "Flare → short-term prednisone or budesonide", "Maintenance → azathioprine/6-MP (TPMT/NUDT15 first)", "Moderate-severe or refractory → biologic or JAK inhibitor", "Before biologics: TB, hepatitis B/C, vaccines"], "src": "S11; S14; S15; S18"},
    ],
    "Nutrition, Vitamins & Dietary Supplements": [
        {"title": "Refeeding sequence", "steps": ["Prolonged starvation", "Carbohydrate feeding raises insulin", "Phosphate, potassium, magnesium shift into cells", "Dangerously low levels: heart, muscle, breathing", "Prevent: start slowly, thiamine first, check electrolytes daily"], "src": "S29"},
        {"title": "B12 absorption", "steps": ["Dietary B12 bound to food protein", "Stomach acid and pepsin release it", "Free B12 binds intrinsic factor", "Absorbed in the terminal ileum", "PPIs, metformin, ileal surgery impair it"], "src": "S25"},
    ],
}

CRAM = [
    ("Laxative buckets", "Bulk-forming · osmotic · stimulant · secretagogue", "S4"),
    ("Fastest laxatives", "Osmotic (~2 h), stimulant (~8 h); bulk-forming ~60 h", "S6; SG U3-R9"),
    ("PEG", "First-line chronic constipation", "S5"),
    ("Lubiprostone vs. linaclotide", "ClC-2, nausea · GC-C, diarrhea, not under age 2", "S5; S46; S47"),
    ("Loperamide", "Peripheral mu agonist; P-gp keeps it out of CNS; high dose → QT", "S7; S8"),
    ("Lomotil atropine", "Subtherapeutic, deters misuse; Schedule V", "S7; SG U3-R10"),
    ("C. difficile", "No antimotility agents; oral vancomycin or fidaxomicin", "S9; SG U3-R10"),
    ("IBD ladder", "5-ASA → steroids (flare) → thiopurines (maintenance) → biologics", "S11; SG U3-R11"),
    ("Sulfasalazine", "Sulfapyridine AEs (rash, G6PD hemolysis, agranulocytosis); folic acid", "S12; S13"),
    ("Mesalamine", "Mild-moderate UC first-line; monitor renal function", "S12; S13"),
    ("Budesonide", "High first-pass → less systemic exposure", "S14"),
    ("Thiopurines", "TPMT/NUDT15 first; CBC, LFTs; allopurinol → cut dose 2/3–3/4", "S15"),
    ("IBD targets", "TNF-α infliximab/adalimumab · α4β7 vedolizumab · IL-12/23 ustekinumab · JAK tofacitinib", "S16; S17"),
    ("Gut-selective biologic", "Vedolizumab", "S38; SG U3-R11"),
    ("Before biologics", "TB, hepatitis B/C, vaccines (live) first", "S18"),
    ("Fat- vs. water-soluble", "ADEK stored, toxic risk · B, C excreted", "S22; SG U3-R12"),
    ("B12 risk", "PPI/H2 blocker, metformin, bariatric surgery, older age, vegan", "S25"),
    ("Iron absorption", "↑ vitamin C, ↓ antacids/PPIs", "S24"),
    ("Enteral vs. parenteral", "If the gut works, use it", "S28"),
    ("Refeeding", "Slow start, thiamine, daily phosphate/K/Mg", "S29"),
    ("Warfarin + vitamin K", "Keep intake consistent", "S27"),
    ("Warfarin + St. John’s wort", "CYP3A4 induction → ↓ INR", "S26; SG U3-R13"),
    ("Bleeding supplements", "Ginkgo, fish oil", "S27; S30"),
]
