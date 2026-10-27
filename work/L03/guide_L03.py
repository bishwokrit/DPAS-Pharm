"""Study-guide extras for L03 (6-sentence summary, flow diagrams, cram sheet). Imported by author_L03.py."""

# Home-page teaser (two sentences, shown on the class day and until the next lecture)
TEASER = "Today: acetaminophen vs. NSAIDs, the COX-1/COX-2 trade-off, methotrexate’s weekly rule, and the biologic DMARDs for rheumatoid arthritis. One cited guide and exam-style practice — no more hours lost rereading the textbook."

SUMMARY = [
    ("Tissue injury releases **prostaglandins, bradykinin, histamine, and cytokines** that sensitize nociceptors; **corticosteroids** block phospholipase A₂ upstream, while **NSAIDs** block COX.", "S6; S9; SG U2-R1; SG U2-R2"),
    ("**Acetaminophen** treats pain and fever but is not a reliable anti-inflammatory; overdose depletes glutathione so **NAPQI** injures the liver, and **N-acetylcysteine** is the antidote.", "S15; S19; SG U2-R3"),
    ("**COX-1** is the housekeeping enzyme (gastric protection, renal blood flow) and **COX-2** makes inflammatory prostaglandins; **celecoxib** lowers GI risk but raises cardiovascular risk, with similar renal risk.", "S26; S29; SG U2-R4; SG U2-R5"),
    ("NSAID harms are **GI, renal, and cardiovascular**; flag anticoagulants, ACE inhibitors/ARBs plus diuretics (**triple whammy**), and corticosteroids — and prefer acetaminophen when red flags stack up.", "S34; S36; S37"),
    ("**OA** is degenerative (treat pain and function); **RA** is autoimmune and needs **DMARDs**, which change the disease course; **methotrexate** is the anchor — **weekly**, with folate, never in pregnancy.", "S41; S45; S49; SG U2-R6; SG U2-R7"),
    ("**Biologics** target the cascade — TNF (adalimumab, etanercept, infliximab), IL-6 (tocilizumab), B cells (rituximab), T-cell costimulation (abatacept) — and all DMARDs share **infection risk**: screen for TB and hepatitis, vaccinate first.", "S51; S56; SG U2-R8"),
]

FLOWS = {
    "Musculoskeletal Pain & the Inflammatory Cascade": [
        {"title": "How injury becomes pain", "steps": ["Tissue injury", "Inflammatory mediators released", "Nociceptors sensitized", "Pain"], "src": "S6"},
        {"title": "The arachidonic acid pathway", "steps": ["Membrane phospholipids", "Phospholipase A₂ (blocked by corticosteroids)", "Arachidonic acid", "COX-1 / COX-2 (blocked by NSAIDs)", "Prostaglandins", "Pain, inflammation, fever"], "src": "S8; S9"},
    ],
    "Acetaminophen": [
        {"title": "Therapeutic dose", "steps": ["Oral acetaminophen → liver", "~90%: glucuronidation and sulfation → safe urinary excretion", "~5–10%: CYP2E1 → NAPQI", "Glutathione (GSH) conjugation → safe excretion"], "src": "S16"},
        {"title": "Overdose and rescue", "steps": ["Glucuronidation/sulfation saturate", "More drug shunted to CYP2E1", "More NAPQI; glutathione depleted", "NAPQI binds hepatocyte proteins", "Centrilobular liver necrosis", "NAC replenishes GSH — give early"], "src": "S17; SG U2-R3"},
        {"title": "Using the Rumack-Matthew nomogram", "steps": ["Single acute ingestion, known time", "Level drawn at ≥ 4 h", "Plot level vs. hours since ingestion", "Above the treatment line → give NAC", "Below → toxicity unlikely", "Late, chronic, unknown time, or > 24 h → clinical judgment, AST/ALT, poison control"], "src": "S18; S18 (notes)"},
    ],
    "NSAIDs & COX-2 Selective Inhibition": [
        {"title": "How NSAIDs work", "steps": ["NSAID", "COX inhibition", "↓ Prostaglandins and TXA2", "↓ Pain, inflammation, fever (and ↑ bleeding risk)"], "src": "S24; S25"},
        {"title": "Why celecoxib raises cardiovascular risk", "steps": ["Celecoxib blocks COX-2", "Endothelial PGI2 falls", "Platelet TXA2 (COX-1) preserved", "Balance tips toward clotting", "↑ Cardiovascular events"], "src": "S29 (notes); S30"},
        {"title": "Is an NSAID the right first choice?", "steps": ["Check GI: ulcer or bleeding history?", "Check kidney: CKD, ACEi/ARB, diuretic?", "Check heart: HF, CV disease, hypertension?", "Check bleeding: anticoagulant, older age?", "Red flags → acetaminophen or topical/non-NSAID strategy"], "src": "S34; S36; S37; S43"},
    ],
    "Conventional DMARDs & Methotrexate": [
        {"title": "Methotrexate safety", "steps": ["Weekly dose (never daily)", "Folate co-prescribed", "Watch liver, marrow, lung", "Avoid in pregnancy (teratogenic)"], "src": "S49; SG U2-R7"},
        {"title": "Methotrexate and the folate pathway", "steps": ["Dihydrofolate (DHF)", "DHFR — blocked by methotrexate", "Tetrahydrofolate (THF)", "Purine and thymidylate (DNA) synthesis", "Low dose: anti-inflammatory (adenosine release)", "Weekly dosing only"], "src": "S50"},
    ],
    "Biologic DMARDs & Immunosuppression Safety": [
        {"title": "Starting a biologic", "steps": ["Screen: TB, hepatitis B/C", "Update vaccines (especially live)", "Start therapy", "Regular labs: cytopenias, liver, infection", "Report fever or infection promptly"], "src": "S56"},
    ],
}

CRAM = [
    ("Pain by mechanism", "Nociceptive · inflammatory · neuropathic", "S5"),
    ("Chronic pain", "Persists beyond expected healing, often > 3 months", "S5"),
    ("4 pain mediators", "Prostaglandins, bradykinin, histamine, cytokines (TNF-α, IL-1, IL-6)", "S6; SG U2-R1"),
    ("Corticosteroid site", "Phospholipase A₂ (upstream) → broad mediator suppression", "S9; SG U2-R2"),
    ("NSAID site", "COX → prostaglandins specifically", "S9; S24"),
    ("Acetaminophen effects", "Analgesic + antipyretic; minimal anti-inflammatory", "S15"),
    ("Acetaminophen toxic metabolite", "NAPQI (N-acetyl-p-benzoquinone imine)", "S19; S19 (notes)"),
    ("Acetaminophen antidote", "N-acetylcysteine — glutathione precursor", "S19; SG U2-R3"),
    ("Hidden acetaminophen", "Combination cold, flu, and sleep products — ask about ALL sources", "S20"),
    ("COX-1", "Housekeeping: gastric protection, renal blood flow", "S26; SG U2-R4"),
    ("COX-2", "Induced at inflammation; main inflammatory prostaglandin source", "S26; SG U2-R4"),
    ("Ibuprofen", "Common first-line for mild-moderate pain", "S28"),
    ("Naproxen", "Longer half-life, twice-daily", "S28"),
    ("Diclofenac", "Oral and topical", "S28"),
    ("Indomethacin", "More potent; more GI/CNS effects", "S28"),
    ("Ketorolac", "Short-term only; significant GI/renal risk", "S28"),
    ("Celecoxib trade-off", "↓ GI risk, ↑ CV risk, same renal risk", "S29; SG U2-R5"),
    ("NSAID adverse effects", "GI (ulcer, bleed) · renal (AKI, fluid) · CV (HTN, events)", "S34"),
    ("NSAID cautions", "GI bleed/ulcer, CKD, HF/CV disease, anticoagulant, late pregnancy", "S36"),
    ("Triple whammy", "NSAID + ACEi/ARB + diuretic → AKI", "S36 (notes)"),
    ("NSAID + corticosteroid", "↑ GI ulcer risk", "S36"),
    ("OA vs. RA", "Degenerative → pain/function vs. autoimmune → suppress disease", "S41"),
    ("OA drugs", "Acetaminophen, oral/topical NSAIDs, intra-articular steroid for a single-joint flare", "S43"),
    ("DMARD", "Alters RA’s course, not just symptoms", "S45; SG U2-R6"),
    ("Conventional DMARDs", "Methotrexate (anchor), hydroxychloroquine (milder), sulfasalazine (combos), leflunomide (MTX intolerant)", "S47"),
    ("Methotrexate", "DHFR inhibitor · weekly · folate · liver/marrow/lung · teratogenic", "S49; SG U2-R7"),
    ("TNF inhibitors", "Adalimumab, etanercept, infliximab", "S51; SG U2-R8"),
    ("IL-6 inhibitor", "Tocilizumab", "S51"),
    ("B-cell therapy", "Rituximab", "S51"),
    ("T-cell costimulation", "Abatacept", "S51; SG U2-M"),
    ("DMARD shared risk", "Immunosuppression → infection", "S56; SG U2-R8"),
    ("Before biologics", "TB + hepatitis B/C screen; update vaccines (live) first", "S56"),
    ("Acetaminophen routes", "~90% glucuronidation/sulfation (safe) · ~5–10% CYP2E1 → NAPQI", "S16"),
    ("Who's at higher acetaminophen risk", "Chronic alcohol use, fasting (↓ GSH, ↑ CYP2E1)", "S17"),
    ("Liver lesion in overdose", "Centrilobular necrosis", "S17"),
    ("Rumack-Matthew nomogram", "Single acute ingestion; level ≥ 4 h; above the line → NAC; not used > 24 h", "S18"),
    ("Nomogram example", "8 h, 120 mcg/mL → above the line → start NAC", "S18"),
    ("Nomogram line (illustrative)", "150 mcg/mL at 4 h, halving every 4 h, 4.7 at 24 h", "S18"),
    ("COX-1 vs. COX-2", "Constitutive (gastric mucosa, platelet TXA2, kidney) vs. inducible (inflamed tissue)", "S27"),
    ("Celecoxib CV mechanism", "PGI2 falls, TXA2 preserved", "S30"),
    ("NSAID organ effects", "GI: ↓ mucus/bicarbonate · kidney: ↓ afferent dilation · platelets: ↓ TXA2", "S35"),
    ("RA joint destruction", "Synovitis → pannus; TNF-α and IL-6 drive erosion", "S42"),
    ("NSAID vs. DMARD onset", "NSAID relief in days · DMARD protection over weeks–months", "S46"),
    ("Leflunomide target", "DHODH (pyrimidine synthesis)", "S48"),
    ("Hydroxychloroquine action", "Alters lysosomal and TLR signaling", "S48"),
    ("Methotrexate at low dose", "Likely anti-inflammatory via adenosine release", "S50"),
    ("Abatacept", "CTLA-4-Ig: binds CD80/86, blocks CD28 costimulation — acts earliest", "S52; S55"),
    ("Rituximab", "Anti-CD20; after TNF-inhibitor failure; check hepatitis B", "S52"),
    ("Infection monitoring on DMARDs", "CBC, liver, kidney labs every 1–3 months", "S57"),
    ("Name stems", "-zumab humanized · -ximab chimeric · -umab human · -cept fusion · -tinib kinase · -coxib COX-2", "S60"),
]
