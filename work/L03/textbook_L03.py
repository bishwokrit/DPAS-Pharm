"""Textbook (Katzung 16e, Ch. 36 — NSAIDs, DMARDs, other analgesics) additions for L03. Imported by author_L03.py.
Only details that sharpen what the lecture teaches; every fact is TB-tagged and cited to a printed page.
Ch. 27 (muscle relaxants), Ch. 42 (bone), and the gout part of Ch. 36 are taught in Session 2 (L04)."""

ADD = {
    "Musculoskeletal Pain & the Inflammatory Cascade": {
        "how": [
            ("**The immune response:** chronic inflammation involves eicosanoids, leukotrienes, cytokines, chemokines, and many immune cells; RA, SLE, vasculitis, and gout all stem from this cascade.", "p. 675"),
            ("The lipoxygenase branch of arachidonic acid makes leukotrienes (chemotaxis, bronchoconstriction, vascular permeability) — a separate branch from the COX step NSAIDs block.", "p. 675; p. 678"),
        ],
        "clinical": [
            ("**Therapeutic strategies:** goal 1 is symptom relief and function (NSAIDs and DMARDs); goal 2 is slowing tissue damage, for which DMARDs are absolutely necessary. Response is tracked with indices such as DAS28 in RA.", "p. 675"),
        ],
    },
    "Acetaminophen": {
        "moa": [
            ("Textbook adds: a weak peripheral COX-1/COX-2 inhibitor whose pain relief also involves opioid, cannabinoid, and serotonergic systems.", "p. 694"),
        ],
        "indications": [
            ("Preferred over aspirin in aspirin allergy, hemophilia, peptic ulcer history, or aspirin-induced bronchospasm; alone it is inadequate for inflammatory conditions such as RA.", "p. 694"),
        ],
        "adverse": [
            ("Ingesting 15 g may be fatal (centrilobular hepatic necrosis); take care with liver disease, heavy alcohol use, or malnutrition.", "p. 694"),
        ],
        "contra": [
        ],
        "interactions": [
            ("Combining acetaminophen with an NSAID improves pain control but can potentiate the NSAID’s GI toxicity.", "p. 694"),
        ],
        "pk": [
            ("Mostly conjugated to inactive sulfate and glucuronide; half-life 2–3 hours, relatively unaffected by renal function.", "p. 694"),
        ],
        "monitoring": [
            ("Adults: generally no more than 4 g/day — and even 4 g is associated with more liver function test abnormalities.", "p. 694"),
        ],
        "pearls": [
            ("**Other analgesics — tramadol:** weak μ-opioid agonist plus serotonin/norepinephrine reuptake inhibition; no anti-inflammatory effect; up to 300 mg/day; risks serotonin syndrome and seizures.", "p. 694; p. 695"),
        ],
    },
    "NSAIDs & COX-2 Selective Inhibition": {
        "moa": [
            ("Aspirin irreversibly blocks platelet COX (the effect lasts the 8–10-day life of the platelet); other nonselective NSAIDs are reversible inhibitors.", "p. 675; p. 677"),
            ("COX-2 inhibitors spare platelet thromboxane (made by COX-1) but block endothelial prostacyclin — so they are not cardioprotective.", "p. 677"),
        ],
        "indications": [
            ("NSAIDs ease symptoms but, unlike DMARDs, do not alter the course of any arthritic disorder.", "p. 676"),
            ("Used in RA, spondyloarthropathies, OA, sprains and strains, low back pain, and gout (tolmetin appears ineffective in gout).", "p. 676"),
        ],
        "adverse": [
            ("Beyond GI, renal, and CV: headache, tinnitus, dizziness, rare aseptic meningitis, liver test abnormalities, asthma, rashes, hyperkalemia.", "p. 676"),
        ],
        "contra": [
            ("Ibuprofen is relatively contraindicated with nasal polyps, angioedema, or bronchospastic reactivity to aspirin.", "p. 680"),
        ],
        "interactions": [
            ("Ibuprofen taken with aspirin blocks aspirin’s irreversible platelet inhibition, limiting its cardioprotective effect.", "p. 680"),
            ("Celecoxib (a CYP2C9 substrate) occasionally interacts with warfarin and raises lithium and fluconazole levels.", "p. 679"),
        ],
        "pk": [
            ("**Chemistry & pharmacokinetics:** most NSAIDs are weak acids, well absorbed, ~98% albumin-bound, metabolized by CYP3A or CYP2C, and renally excreted.", "p. 675"),
        ],
        "monitoring": [
            ("Highest GI-bleeding risk: celecoxib, or a nonselective NSAID plus omeprazole or misoprostol.", "p. 681"),
        ],
        "pearls": [
            ("**Choice of NSAID:** all are about equally effective, so choose by toxicity, cost, and patient factors; in renal insufficiency nonacetylated salicylates may be best.", "p. 681"),
        ],
    },
    "Osteoarthritis vs. Rheumatoid Arthritis": {
        "clinical": [
            ("**Glucocorticoid drugs in rheumatic diseases:** used chronically in 30–70% of RA patients; relief is prompt and dramatic, and they slow new bone erosions.", "p. 693"),
            ("Long-term prednisone in RA: no more than 7.5 mg daily, tapered when possible — even 2.8 mg daily for over 5 years is linked to severe infections.", "p. 693"),
            ("Intra-articular corticosteroids often relieve painful symptoms for up to several months.", "p. 693"),
            ("Long-term glucocorticoid harms: osteoporosis, hyperglycemia, Cushing syndrome, infections, cataract, glaucoma, gastric ulcer, depression.", "p. 694"),
        ],
        "examples": [
            ("Topical diclofenac 1% gel is sold over the counter for OA and muscular pain.", "p. 679"),
        ],
    },
    "Conventional DMARDs & Methotrexate": {
        "overview": [
            ("DMARD effects take 2 weeks to 6 months to appear. Types: conventional synthetic (cs), biologic (b), and targeted synthetic (ts, e.g., tofacitinib).", "p. 681"),
        ],
        "moa": [
        ],
        "indications": [
            ("Methotrexate starts at 7.5 mg weekly and rises to 15–25 mg weekly; it slows new erosions in RA.", "p. 688"),
            ("**Combination therapy with DMARDs** is now the rule when monotherapy falls short; triple therapy (methotrexate, sulfasalazine, hydroxychloroquine) rivals etanercept plus methotrexate.", "p. 693"),
        ],
        "adverse": [
            ("Methotrexate’s most common toxicities are nausea and stomatitis; dose-related liver enzyme elevations are frequent.", "p. 689"),
        ],
        "contra": [
        ],
        "interactions": [
            ("Hydroxychloroquine can reduce methotrexate clearance.", "p. 688"),
        ],
        "pk": [
        ],
        "monitoring": [
            ("Folic acid or leucovorin reduces stomatitis, GI, and liver test problems but may cut methotrexate efficacy by 10–18%.", "p. 689"),
            ("Hydroxychloroquine: baseline eye exam, then annual screening after 5 years (retinopathy).", "p. 684"),
        ],
    },
    "Biologic DMARDs & Immunosuppression Safety": {
        "overview": [
            ("Biologics are large molecules, usually proteins made by recombinant DNA technology; JAK inhibitors are oral small-molecule targeted synthetic DMARDs.", "p. 681; p. 686"),
        ],
        "adverse": [
            ("**Boxed warning — all TNF inhibitors:** possible malignancy, especially lymphoma.", "p. 692"),
            ("**Boxed warning — all JAK inhibitors:** venous thromboembolism (DVT, PE), major adverse cardiovascular events, and cancer.", "p. 686"),
            ("TNF inhibitors: TB reactivation, fungal infections, hepatitis B reactivation, new or worse heart failure, demyelinating disease, lupus-like syndrome.", "p. 690; p. 692"),
        ],
        "contra": [
            ("Don’t stack biologics: abatacept with a TNF inhibitor probably raises serious infections; upadacitinib with biologic DMARDs is not recommended.", "p. 682; p. 687"),
        ],
        "interactions": [
            ("Tocilizumab stimulates CYP450 — doses of cyclosporine or warfarin may need adjusting.", "p. 692"),
            ("Methotrexate given with TNF inhibitors reduces anti-drug antibodies (infliximab, golimumab, certolizumab).", "p. 691; p. 692"),
        ],
        "monitoring": [
            ("Avoid live vaccines for up to 3 months after stopping abatacept; stop upadacitinib before a live attenuated vaccine.", "p. 682; p. 687"),
        ],
        "pearls": [
            ("**Biosimilars:** near-copies of legacy biologics with the same efficacy, toxicity, and immunogenicity at potentially lower cost.", "p. 693"),
            ("If methotrexate alone falls short: add csDMARDs or a biologic — usually a TNF inhibitor first, then non-TNF biologics or JAK inhibitors.", "p. 701"),
        ],
    },
}

CONFLICTS = {
    "Conventional DMARDs & Methotrexate": [
        {"topic": "How methotrexate works at RA doses",
         "slides": {"text": "Inhibits dihydrofolate reductase, reducing immune cell proliferation at low RA doses.", "src": "S27; SG U2-M"},
         "textbook": {"text": "Low-dose methotrexate mainly inhibits AICAR transformylase and thymidylate synthetase, raising extracellular AMP that suppresses inflammation; its dihydrofolate reductase effect is relatively minor at rheumatic doses.", "src": "p. 688"}},
    ],
}

DISCREPANCIES = [
    ("**Methotrexate mechanism:** the slides and study guide say dihydrofolate reductase inhibition; the textbook says that effect is relatively minor at RA doses and credits AICAR transformylase. Answer course exams with the slide/study-guide version.", "S27; SG U2-M; p. 688"),
]

CRAM = [
    ("Acetaminophen max (adults)", "Generally ≤ 4 g/day; 15 g may be fatal", "p. 694"),
    ("Aspirin vs. other NSAIDs", "Aspirin: irreversible platelet COX (8–10 days); others reversible", "p. 675; p. 677"),
    ("Ketorolac limits", "Start IV/IM/intranasal; ≤ 120 mg/day; ≤ 5 days; halve if > 65, < 50 kg, renal impairment", "p. 694"),
    ("Celecoxib selectivity", "10–20× more selective for COX-2", "p. 677"),
    ("Methotrexate dose", "7.5 mg weekly → 15–25 mg weekly", "p. 688"),
    ("Hydroxychloroquine monitoring", "Baseline eye exam; annual after 5 years", "p. 684"),
    ("TNF inhibitor boxed warning", "Malignancy, especially lymphoma", "p. 692"),
    ("JAK inhibitor boxed warning", "VTE (DVT/PE), MACE, cancer", "p. 686"),
    ("JAK inhibitors", "Baricitinib, tofacitinib, upadacitinib — oral; zoster, ↑ LDL", "p. 686"),
    ("RA prednisone ceiling", "≤ 7.5 mg daily long term, taper", "p. 693"),
]

QUESTIONS = [
    dict(topic="NSAIDs & COX-2 Selective Inhibition", kind="vignette",
         stem="A patient takes low-dose aspirin for cardioprotection and starts regular ibuprofen for back pain. What is the textbook concern?",
         correct="Ibuprofen blocks aspirin’s irreversible platelet inhibition",
         why_correct="Concomitant ibuprofen antagonizes aspirin’s irreversible platelet inhibition, limiting its cardioprotective effect (p. 680).",
         distractors=[("Ibuprofen converts aspirin to the toxic metabolite NAPQI", "NAPQI comes from acetaminophen (S11)."),
                      ("Aspirin makes ibuprofen COX-2 selective, raising CV risk", "Aspirin does not change ibuprofen’s selectivity (p. 680)."),
                      ("Both drugs together protect the kidney from injury", "NSAIDs reduce renal perfusion; they don’t protect the kidney (S19)."),
                      ("Ibuprofen speeds aspirin’s renal excretion fivefold", "Not the textbook’s interaction (p. 680).")],
         src="p. 680"),
    dict(topic="Biologic DMARDs & Immunosuppression Safety", kind="vignette",
         stem="A patient with RA and high cardiovascular risk is being considered for tofacitinib. Which boxed warning applies to all JAK inhibitors?",
         correct="Venous thromboembolism, major cardiovascular events, and cancer",
         why_correct="All JAK inhibitors carry an FDA boxed warning for VTE (DVT, PE), MACE, and cancer (p. 686).",
         distractors=[("Fatal hepatotoxicity from NAPQI accumulating in the liver", "NAPQI is acetaminophen toxicity (S11)."),
                      ("Teratogenicity that requires strict weekly-only dosing", "Weekly dosing is a methotrexate rule (S27)."),
                      ("Lymphoma only, exactly the same as the TNF inhibitors", "The TNF inhibitor warning is malignancy; JAK inhibitors add VTE and MACE (p. 686; p. 692)."),
                      ("Retinopathy that requires annual eye examinations", "Retinal screening applies to hydroxychloroquine (p. 684).")],
         src="p. 686"),
    dict(topic="Conventional DMARDs & Methotrexate", kind="mechanism",
         stem="Which conventional DMARD requires a baseline eye exam and annual screening after 5 years because of retinopathy?",
         correct="Hydroxychloroquine",
         why_correct="Antimalarials bind melanin-rich tissue such as the retina; a baseline exam and annual screening after 5 years are recommended (p. 684).",
         distractors=[("Mycophenolate mofetil", "Mycophenolate’s issues are GI, liver, cytopenias, and infection (p. 689)."),
                      ("Leflunomide", "Leflunomide’s issues are diarrhea and liver tests (p. 688)."),
                      ("Sulfasalazine", "Sulfasalazine’s issues are GI, rash, and cytopenias (p. 690)."),
                      ("Methotrexate", "Methotrexate monitoring targets liver, marrow, and lung (S27).")],
         src="p. 684"),
]

COMPARISONS = {
    "NSAIDs & COX-2 Selective Inhibition": [
        {"title": "Other NSAIDs in the reading (textbook)", "columns": ["Drug", "Half-life (h)", "What sets it apart"],
         "rows": [["Aspirin", "0.25", "Now mainly antiplatelet (81–325 mg daily); avoid in hemophilia"],
                  ["Nonacetylated salicylates", "Not covered in materials", "Anti-inflammatory without platelet inhibition: an option in asthma, bleeding tendency, renal dysfunction"],
                  ["Ibuprofen", "2", "≤ 1600 mg/day analgesic only; 2400 mg/day anti-inflammatory"],
                  ["Naproxen", "12–17", "More GI bleeding than OTC ibuprofen, better CV profile; avoid in hepatic impairment"],
                  ["Diclofenac", "1.9–2.3", "More aminotransferase rises; 1% topical gel OTC"],
                  ["Indomethacin", "4–5", "Headache in 11.7%; can worsen depression, epilepsy, parkinsonism"],
                  ["Ketorolac", "5–6", "Analgesic use; start IV/IM/intranasal; ≤ 120 mg/day; ≤ 5 days"],
                  ["Celecoxib", "11.2", "10–20× COX-2 selective; 100–200 mg bid; no platelet effect at usual doses"],
                  ["Meloxicam", "20", "Relatively COX-2 selective at 7.5 mg/day; fewer GI effects"],
                  ["Etodolac", "6.4", "Relatively COX-2 selective; linked to acute pancreatitis"],
                  ["Nabumetone", "22.5–29.8", "Only nonacid NSAID (prodrug); less ulceration"],
                  ["Piroxicam", "50", "Above 20 mg/day sharply raises ulcer and bleeding risk"],
                  ["Sulindac", "16.4", "Less effect on renal prostaglandins; more liver test abnormalities"],
                  ["Oxaprozin · diflunisal · flurbiprofen · tolmetin", "54.9 · 8–12 · 3.8 · 1–2", "Oxaprozin once daily; diflunisal rarely used; flurbiprofen rare tremor/rigidity; tolmetin ineffective in gout"]],
         "src": "p. 677; p. 679; p. 680; p. 681; p. 694"},
    ],
    "Conventional DMARDs & Methotrexate": [
        {"title": "Conventional synthetic DMARDs (textbook)", "columns": ["Drug", "How it works", "Main uses", "Watch for"],
         "rows": [["**Methotrexate**", "DHFR (slides); AICAR transformylase (textbook)", "RA anchor; psoriasis, PsA, JIA", "Nausea, stomatitis, liver, marrow, lung; teratogenic"],
                  ["**Hydroxychloroquine**, chloroquine", "Suppress T-cell responses and chemotaxis; dampen type 1 IFN", "Mild RA; SLE (lowers mortality); Sjögren", "Retinopathy (eye exams); cardiomyopathy; 3–6 months to respond"],
                  ["**Sulfasalazine**", "Split into sulfapyridine + 5-aminosalicylic acid", "RA (slows radiologic progression); ulcerative colitis", "~30% stop it; rash, toxic epidermal necrolysis, neutropenia; reversible male infertility"],
                  ["**Leflunomide**", "Dihydroorotate dehydrogenase inhibitor", "RA (equals methotrexate)", "Diarrhea (25%), liver tests, hypertension; half-life 19 days (cholestyramine shortens)"],
                  ["Azathioprine", "Becomes 6-thioguanine; suppresses B and T cells", "RA, SLE, transplant", "Marrow suppression (TPMT, NUDT15), GI upset, cancer, infection"],
                  ["Mycophenolate mofetil", "IMPDH inhibitor", "SLE (renal and nonrenal), scleroderma lung; not proven in RA", "GI, liver, cytopenias, infection; contraindicated in pregnancy"],
                  ["Cyclosporine, tacrolimus, voclosporin", "Calcineurin inhibitors (block T-cell cytokines)", "Severe RA; lupus nephritis", "Nephro-, neuro-, cardiotoxicity, hypertension; CYP3A4 interactions (grapefruit)"],
                  ["Cyclophosphamide", "Cross-links DNA", "Lupus nephritis, CNS lupus, vasculitis", "Cytopenias, infection, sterility, bladder and skin cancer"],
                  ["Apremilast", "PDE4 inhibitor (↑ cAMP)", "Plaque psoriasis, PsA, Behçet oral ulcers", "Diarrhea, nausea, weight loss, mood changes; CYP3A4"],
                  ["Mesalamine", "Topical colonic 5-aminosalicylate", "Ulcerative colitis", "Diarrhea, headache; renal impairment (monitor)"]],
         "src": "S26; S27; p. 682; p. 683; p. 684; p. 687; p. 688; p. 689; p. 690"},
    ],
    "Biologic DMARDs & Immunosuppression Safety": [
        {"title": "Biologic and targeted DMARDs in the reading (textbook)", "columns": ["Drug(s)", "Target", "Main uses", "Watch for"],
         "rows": [["**Adalimumab, etanercept, infliximab**, certolizumab, golimumab", "TNF-α", "RA, PsA, AS, psoriasis; infliximab and adalimumab also Crohn and UC", "TB, fungal, hepatitis B; heart failure; demyelination; lymphoma (boxed)"],
                  ["**Tocilizumab**, sarilumab", "IL-6 receptor", "RA; tocilizumab also giant cell arteritis", "Infection, liver enzymes, lipids, cytopenias; no sarilumab with diverticulitis"],
                  ["**Rituximab**", "CD20 B cells (depletion)", "RA with methotrexate; GPA", "First-dose rash (~30%), infusion reactions, hepatitis B reactivation"],
                  ["**Abatacept**", "CD80/86–CD28 costimulation", "RA, PsA, JIA", "Infection; don’t combine with TNF inhibitors; live vaccines"],
                  ["Anakinra, canakinumab, rilonacept", "Interleukin-1", "CAPS; anakinra approved but rarely used in RA", "Injection-site reactions (up to 40%), URIs"],
                  ["Baricitinib, tofacitinib, upadacitinib", "Janus kinase (JAK-STAT), oral", "RA after TNF or methotrexate failure; PsA; UC", "Boxed VTE/MACE/cancer; herpes zoster; ↑ LDL; caution with diverticulitis"],
                  ["Secukinumab, ixekizumab", "IL-17A", "Psoriasis, PsA, AS", "Infection; can cause or worsen IBD; TB screen"],
                  ["Ustekinumab", "IL-12/IL-23 (p40)", "PsA, psoriasis, Crohn, UC", "URIs; stop ≥ 15 weeks before live vaccines"],
                  ["Guselkumab, risankizumab", "IL-23 (p19)", "Plaque psoriasis, PsA", "URIs; TB screen"],
                  ["Belimumab", "BLyS (B-cell survival)", "SLE, lupus nephritis", "Infection; depression and suicide reported"],
                  ["Anifrolumab", "Type 1 interferon receptor", "Nonrenal SLE", "URIs, bronchitis, infusion reactions"]],
         "src": "S28; p. 682; p. 683; p. 684; p. 685; p. 686; p. 689; p. 690; p. 692; p. 693"},
    ],
}

FLOWS = {}

DEEPER = {
    "Acetaminophen": (36, 694, 695, "Acetaminophen dosing and toxicity, plus ketorolac and tramadol"),
    "NSAIDs & COX-2 Selective Inhibition": (36, 675, 681, "Every NSAID’s half-life, dose, and quirks (Table 36–1)"),
    "Osteoarthritis, Rheumatoid Arthritis & DMARDs": (36, 681, 694, "Each DMARD, biologic, and JAK inhibitor, plus glucocorticoids in rheumatic disease"),
}

_CH27 = ["Normal Neuromuscular Function", "Blocking Drugs", "Mechanism of Action", "Skeletal Muscle Paralysis", "Cardiovascular Effects",
         "Neuromuscular Response", "Neuromuscular Blockade", "SPASMOLYTIC & ANTISPASMODIC DRUGS", "TIZANIDINE",
         "OTHER CENTRALLY ACTING SPASMOLYTIC DRUGS", "BOTULINUM TOXIN", "DANTROLENE", "Gabarone, Gralise, Neurontin", "Neuromuscular Blockers"]
_GOUT = ["ALLOPURINOL", "COLCHICINE", "FEBUXOSTAT", "PEGLOTICASE", "PROBENECID AND LESINURAD", "GLUCOCORTICOIDS IN GOUT", "INTERLEUKIN-1 INHIBITORS IN GOUT"]
_CH42 = ["BASIC PHARMACOLOGY", "PRINCIPAL HORMONAL REGULATORS OF BONE MINERAL HOMEOSTASIS PARATHYROID HORMONE", "FIBROBLAST GROWTH FACTOR 23",
         "SECONDARY HORMONAL REGULATORS OF BONE MINERAL HOMEOSTASIS", "CALCITONIN", "GLUCOCORTICOIDS", "ESTROGENS", "Therapies for Osteoporosis",
         "NONHORMONAL AGENTS AFFECTING BONE MINERAL HOMEOSTASIS BISPHOSPHONATES", "DENOSUMAB", "SCLEROSTIN ANTIBODIES", "CALCIMIMETICS",
         "THIAZIDE DIURETICS", "FLUORIDE", "STRONTIUM RANELATE", "CLINICAL PHARMACOLOGY", "ABNORMAL SERUM CALCIUM & PHOSPHATE LEVELS HYPERCALCEMIA",
         "Saline Diuresis", "Gallium Nitrate", "HYPOCALCEMIA", "HYPERPHOSPHATEMIA", "HYPOPHOSPHATEMIA",
         "SPECIFIC DISORDERS INVOLVING BONE MINERAL–REGULATING HORMONES PRIMARY HYPERPARATHYROIDISM", "HYPOPARATHYROIDISM",
         "NUTRITIONAL VITAMIN D DEFICIENCY OR INSUFFICIENCY", "CHRONIC KIDNEY DISEASE", "Vitamin D Preparations", "INTESTINAL OSTEODYSTROPHY",
         "OSTEOPOROSIS", "IDIOPATHIC INFANTILE HYPERCALCEMIA", "NEPHROTIC SYNDROME", "IDIOPATHIC HYPERCALCIURIA",
         "OTHER DISORDERS OF BONE MINERAL HOMEOSTASIS PAGET DISEASE OF BONE", "ENTERIC OXALURIA", "SCLEROSTIN ANTIBODY", "CALCIUM"]

READING_SKIP = (
    [{"heading": h, "reason": "Taught in L04 (Session 2: skeletal muscle relaxants, Ch. 27)"} for h in _CH27]
    + [{"heading": h, "reason": "Taught in L04 (Session 2: gout, end of Ch. 36)"} for h in _GOUT]
    + [{"heading": h, "reason": "Taught in L04 (Session 2: bone pharmacology, Ch. 42)"} for h in _CH42]
    + [{"heading": "Disease-Modifying Antirheumatic Drugs & Glucocorticoids", "reason": "Reference-list heading (citations only, no teaching content)"}]
)
