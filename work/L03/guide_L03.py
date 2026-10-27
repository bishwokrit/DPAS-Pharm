"""Study-guide extras for L03 (6-sentence summary, flow diagrams, cram sheet). Imported by author_L03.py."""

# Home-page teaser (two sentences, shown on the class day and until the next lecture)
TEASER = "Today: acetaminophen vs. NSAIDs, the COX-1/COX-2 trade-off, methotrexate’s weekly rule, and the biologic DMARDs for rheumatoid arthritis. One cited guide and exam-style practice — no more hours lost rereading the textbook."

SUMMARY = [
    ("Tissue injury releases **prostaglandins, bradykinin, histamine, and cytokines** that sensitize nociceptors; **corticosteroids** block phospholipase A₂ upstream, while **NSAIDs** block COX.", "S6; S8; SG U2-R1; SG U2-R2"),
    ("**Acetaminophen** treats pain and fever but is not a reliable anti-inflammatory; overdose depletes glutathione so **NAPQI** injures the liver, and **N-acetylcysteine** is the antidote.", "S10; S11; SG U2-R3"),
    ("**COX-1** is the housekeeping enzyme (gastric protection, renal blood flow) and **COX-2** makes inflammatory prostaglandins; **celecoxib** lowers GI risk but raises cardiovascular risk, with similar renal risk.", "S15; S17; SG U2-R4; SG U2-R5"),
    ("NSAID harms are **GI, renal, and cardiovascular**; flag anticoagulants, ACE inhibitors/ARBs plus diuretics (**triple whammy**), and corticosteroids — and prefer acetaminophen when red flags stack up.", "S19; S20; S21"),
    ("**OA** is degenerative (treat pain and function); **RA** is autoimmune and needs **DMARDs**, which change the disease course; **methotrexate** is the anchor — **weekly**, with folate, never in pregnancy.", "S23; S25; S27; SG U2-R6; SG U2-R7"),
    ("**Biologics** target the cascade — TNF (adalimumab, etanercept, infliximab), IL-6 (tocilizumab), B cells (rituximab), T-cell costimulation (abatacept) — and all DMARDs share **infection risk**: screen for TB and hepatitis, vaccinate first.", "S28; S30; SG U2-R8"),
]

FLOWS = {
    "Musculoskeletal Pain & the Inflammatory Cascade": [
        {"title": "How injury becomes pain", "steps": ["Tissue injury", "Inflammatory mediators released", "Nociceptors sensitized", "Pain"], "src": "S6"},
        {"title": "The arachidonic acid pathway", "steps": ["Membrane phospholipids", "Phospholipase A₂ (blocked by corticosteroids)", "Arachidonic acid", "COX-1 / COX-2 (blocked by NSAIDs)", "Prostaglandins", "Pain, inflammation, fever"], "src": "S7; S8"},
    ],
    "Acetaminophen": [
        {"title": "Acetaminophen overdose", "steps": ["Acetaminophen", "NAPQI (toxic metabolite)", "Glutathione conjugation → safe excretion", "Overdose: glutathione depleted", "NAPQI accumulates → hepatocyte injury", "Antidote: N-acetylcysteine refills glutathione"], "src": "S11; SG U2-R3"},
    ],
    "NSAIDs & COX-2 Selective Inhibition": [
        {"title": "How NSAIDs work", "steps": ["NSAID", "COX inhibition", "↓ Prostaglandins", "↓ Pain, inflammation, fever"], "src": "S14"},
        {"title": "Is an NSAID the right first choice?", "steps": ["Check GI: ulcer or bleeding history?", "Check kidney: CKD, ACEi/ARB, diuretic?", "Check heart: HF, CV disease, hypertension?", "Check bleeding: anticoagulant, older age?", "Red flags → acetaminophen or topical/non-NSAID strategy"], "src": "S19; S20; S21; S24"},
    ],
    "Conventional DMARDs & Methotrexate": [
        {"title": "Methotrexate safety", "steps": ["Weekly dose (never daily)", "Folate co-prescribed", "Watch liver, marrow, lung", "Avoid in pregnancy (teratogenic)"], "src": "S27; SG U2-R7"},
    ],
    "Biologic DMARDs & Immunosuppression Safety": [
        {"title": "Starting a biologic", "steps": ["Screen: TB, hepatitis B/C", "Update vaccines (especially live)", "Start therapy", "Regular labs: cytopenias, liver, infection", "Report fever or infection promptly"], "src": "S30"},
    ],
}

CRAM = [
    ("Pain by mechanism", "Nociceptive · inflammatory · neuropathic", "S5"),
    ("Chronic pain", "Persists beyond expected healing, often > 3 months", "S5"),
    ("4 pain mediators", "Prostaglandins, bradykinin, histamine, cytokines (TNF-α, IL-1, IL-6)", "S6; SG U2-R1"),
    ("Corticosteroid site", "Phospholipase A₂ (upstream) → broad mediator suppression", "S8; SG U2-R2"),
    ("NSAID site", "COX → prostaglandins specifically", "S8; S14"),
    ("Acetaminophen effects", "Analgesic + antipyretic; minimal anti-inflammatory", "S10"),
    ("Acetaminophen toxic metabolite", "NAPQI (N-acetyl-p-benzoquinone imine)", "S11; S11 (notes)"),
    ("Acetaminophen antidote", "N-acetylcysteine — glutathione precursor", "S11; SG U2-R3"),
    ("Hidden acetaminophen", "Combination cold, flu, and sleep products — ask about ALL sources", "S12"),
    ("COX-1", "Housekeeping: gastric protection, renal blood flow", "S15; SG U2-R4"),
    ("COX-2", "Induced at inflammation; main inflammatory prostaglandin source", "S15; SG U2-R4"),
    ("Ibuprofen", "Common first-line for mild-moderate pain", "S16"),
    ("Naproxen", "Longer half-life, twice-daily", "S16"),
    ("Diclofenac", "Oral and topical", "S16"),
    ("Indomethacin", "More potent; more GI/CNS effects", "S16"),
    ("Ketorolac", "Short-term only; significant GI/renal risk", "S16"),
    ("Celecoxib trade-off", "↓ GI risk, ↑ CV risk, same renal risk", "S17; SG U2-R5"),
    ("NSAID adverse effects", "GI (ulcer, bleed) · renal (AKI, fluid) · CV (HTN, events)", "S19"),
    ("NSAID cautions", "GI bleed/ulcer, CKD, HF/CV disease, anticoagulant, late pregnancy", "S20"),
    ("Triple whammy", "NSAID + ACEi/ARB + diuretic → AKI", "S20 (notes)"),
    ("NSAID + corticosteroid", "↑ GI ulcer risk", "S20"),
    ("OA vs. RA", "Degenerative → pain/function vs. autoimmune → suppress disease", "S23"),
    ("OA drugs", "Acetaminophen, oral/topical NSAIDs, intra-articular steroid for a single-joint flare", "S24"),
    ("DMARD", "Alters RA’s course, not just symptoms", "S25; SG U2-R6"),
    ("Conventional DMARDs", "Methotrexate (anchor), hydroxychloroquine (milder), sulfasalazine (combos), leflunomide (MTX intolerant)", "S26"),
    ("Methotrexate", "DHFR inhibitor · weekly · folate · liver/marrow/lung · teratogenic", "S27; SG U2-R7"),
    ("TNF inhibitors", "Adalimumab, etanercept, infliximab", "S28; SG U2-R8"),
    ("IL-6 inhibitor", "Tocilizumab", "S28"),
    ("B-cell therapy", "Rituximab", "S28"),
    ("T-cell costimulation", "Abatacept", "S28; SG U2-M"),
    ("DMARD shared risk", "Immunosuppression → infection", "S30; SG U2-R8"),
    ("Before biologics", "TB + hepatitis B/C screen; update vaccines (live) first", "S30"),
]
