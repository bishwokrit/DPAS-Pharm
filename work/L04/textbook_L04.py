"""Textbook (Katzung 16e — Ch. 27 skeletal muscle relaxants, the gout part of Ch. 36, Ch. 42 bone mineral homeostasis) additions for L04.
Imported by author_L04.py. Only details that sharpen what the lecture teaches; every fact is TB-tagged and cited to a printed page.
The NSAID, DMARD and analgesic sections of Ch. 36 were taught in Session 1 (L03)."""

GOUT = "Gout: Acute Flares & Urate-Lowering Therapy"
SMR = "Skeletal Muscle Relaxants"
BONE = "Bone Pharmacology & Osteoporosis"

ADD = {
    GOUT: {
        "overview": [
            ("Humans lack uricase, the enzyme other mammals use to turn uric acid into soluble allantoin; most people with hyperuricemia never have a gout attack.", "p. 695"),
            ("Treat gout, not a number: long-term drug treatment of asymptomatic hyperuricemia is unproven. Adherence is poor (18–26% in younger patients).", "p. 695"),
        ],
        "moa": [
            ("Allopurinol is a purine analog; its metabolite oxypurinol (half-life 15 hours) also inhibits xanthine oxidase, so it is dosed once daily.", "p. 695"),
            ("Colchicine relieves gout pain and inflammation in 12–24 hours without changing urate metabolism or excretion.", "p. 696"),
            ("Glucocorticoids in gout: reduce neutrophil migration, prostaglandins, and IL-1β.", "p. 698"),
        ],
        "indications": [
            ("Colchicine flare regimen: 1.2 mg, then 0.6 mg an hour later; prophylaxis 0.6 mg once or twice daily during urate-lowering therapy initiation.", "p. 696"),
            ("Corticosteroids are a good alternative when NSAIDs or colchicine are contraindicated, including CKD: prednisone 30–50 mg/d for 1–2 days, tapered over 7–10 days, or intra-articular.", "p. 698"),
            ("All NSAIDs except aspirin, salicylates, and tolmetin treat gout flares.", "p. 697"),
            ("Febuxostat appears safe in moderate CKD; it can be tried after allopurinol hypersensitivity, though a reaction may still occur.", "p. 697"),
        ],
        "adverse": [
            ("Allopurinol hypersensitivity syndrome (SJS/TEN, fever, eosinophilia, hepatitis, renal failure) usually appears 2–4 weeks after starting — stop at the first rash.", "p. 696"),
            ("Colchicine can also cause marrow suppression, myopathy, rhabdomyolysis, and neuritis; it is not removed by dialysis.", "p. 696"),
            ("Febuxostat: liver function abnormalities, diarrhea, headache, nausea.", "p. 697"),
        ],
        "contra": [
            ("Aspirin is avoided in gout: at low doses (≤2.6 g/d) it causes renal retention of uric acid.", "p. 697"),
            ("Uricosurics should not be used in patients who already excrete large amounts of uric acid.", "p. 698"),
        ],
        "interactions": [
            ("Allopurinol with azathioprine: cut the azathioprine dose by 75%.", "p. 696"),
            ("Probenecid also reduces renal secretion of other weak acids, such as penicillin.", "p. 698"),
        ],
        "pk": [
            ("Allopurinol: start 100 mg/d (≤50 mg/d in CKD), titrate every 2–5 weeks to uric acid <6 mg/dL (max 800 mg/d).", "p. 695"),
        ],
        "monitoring": [
            ("Probenecid: keep urine volume high and urine pH above 6.0 early on to prevent stones; start 2–3 weeks after an attack.", "p. 698"),
            ("Pegloticase: premedicate with a corticosteroid and antihistamine; flares are common in the first 3–6 months.", "p. 698"),
        ],
        "pearls": [
            ("Allopurinol already running when a flare hits? Don’t stop it — stopping can worsen and lengthen the attack.", "p. 696"),
        ],
    },
    SMR: {
        "overview": [
            ("Spasticity is common after spinal injury, cerebral palsy, multiple sclerosis, and stroke; these drugs relieve painful spasm better than they restore function.", "p. 510; p. 511"),
        ],
        "moa": [
            ("Diazepam (GABA-A) reduces spasticity partly in the spinal cord, but sedates at the doses needed.", "p. 511"),
            ("Dantrolene binds RyR1; cardiac and smooth muscle use RyR2, so they are minimally depressed.", "p. 513"),
        ],
        "indications": [
            ("Malignant hyperthermia: give IV dantrolene 1 mg/kg, repeated as needed, while controlling acidosis and temperature.", "p. 513"),
            ("Cyclobenzaprine is ineffective for spasm from cerebral palsy or spinal cord injury.", "p. 513"),
            ("Gabapentin has shown promise as a spasmolytic in multiple sclerosis.", "p. 512"),
        ],
        "adverse": [
            ("Botulinum toxin: black box warning for distant spread of toxin, greatest in children treated for spasticity.", "p. 513"),
            ("Tizanidine causes hypotension in 16–33%; abrupt withdrawal causes rebound hypertension and tachycardia.", "p. 512"),
            ("High-dose baclofen: somnolence, respiratory depression, coma; more seizures in epilepsy.", "p. 512"),
            ("Carisoprodol withdrawal after long use: anxiety, tremor, twitching, insomnia, hallucinations.", "p. 511"),
        ],
        "pk": [
            ("Tizanidine: start 2 mg every 6–8 hours, max 36 mg/d; adjust for hepatic or renal impairment.", "p. 512"),
            ("Dantrolene: only about one-third of an oral dose is absorbed; half-life about 8 hours.", "p. 513"),
        ],
        "monitoring": [
            ("Botulinum toxin injections: no more often than every 3 months.", "p. 513"),
        ],
        "pearls": [
            ("Neuromuscular blockers (anesthesia, ICU) paralyze at the end plate and have no CNS activity; succinylcholine is the only depolarizing one.", "p. 499; p. 503"),
            ("Succinylcholine can cause fatal hyperkalemia after burns, denervation, or major trauma, and with volatile anesthetics can trigger malignant hyperthermia.", "p. 508"),
            ("Sugammadex reverses rocuronium/vecuronium; it binds progestins, so use backup contraception for 7 days.", "p. 509; p. 510"),
        ],
    },
    BONE: {
        "overview": [
            ("About 98% of the body’s calcium is in bone; PTH, FGF23, and 1,25-dihydroxyvitamin D are the principal regulators.", "p. 811; p. 812"),
            ("Excess endogenous PTH nets bone resorption, but low intermittent doses build bone first — the basis for teriparatide.", "p. 815"),
            ("Glucocorticoids block vitamin D–driven gut calcium transport, raise renal calcium loss, block formation, and initially stimulate resorption.", "p. 818"),
        ],
        "moa": [
            ("Amino-bisphosphonates (alendronate, risedronate) inhibit farnesyl pyrophosphate synthase in the mevalonate pathway.", "p. 820"),
            ("Denosumab does not kill osteoclasts and does not deposit in bone, so its effect reverses when stopped.", "p. 820"),
        ],
        "indications": [
            ("Raloxifene protects against spine fractures but not hip fractures; bisphosphonates, denosumab, and teriparatide protect both.", "p. 827"),
            ("Vitamin D (800 IU/d) with calcium improves bone density, reduces falls, and prevents fractures — the base under every osteoporosis drug.", "p. 827"),
            ("Calcitonin is less effective (spine fractures only); bisphosphonates and calcitonin are first-line for Paget disease.", "p. 828; p. 829"),
        ],
        "adverse": [
            ("Romosozumab: black box — contraindicated after MI or stroke within the past year.", "p. 820"),
            ("Osteonecrosis of the jaw is rare at osteoporosis doses (~1/100,000 patient-years), more common with high-dose IV zoledronate for cancer.", "p. 820"),
            ("Denosumab: possible infection risk, transient hypocalcemia (CKD, vitamin D deficiency), and rebound resorption if interrupted.", "p. 820"),
        ],
        "contra": [
            ("Unlike bisphosphonates, denosumab can be used in advanced renal disease (not renally cleared) — watch calcium.", "p. 820"),
        ],
        "pk": [
            ("Bisphosphonates: less than 10% of an oral dose is absorbed; about half goes to bone, the rest is excreted unchanged in urine.", "p. 819"),
            ("Denosumab 60 mg SC every 6 months; teriparatide 20 mcg SC daily; romosozumab 210 mg SC monthly for one year, then an antiresorptive.", "p. 819; p. 827"),
        ],
        "monitoring": [
            ("Reassess after 5 years of bisphosphonate (3 for zoledronate); a drug holiday if fracture risk allows.", "p. 820"),
        ],
    },
}

CONFLICTS = {
    GOUT: [
        {"topic": "Febuxostat cardiovascular risk",
         "slides": {"text": "Febuxostat carries a boxed warning for cardiovascular death.", "src": "S13"},
         "textbook": {"text": "Initial concerns about increased MACE with febuxostat have not been borne out; the FDA approved only the 40- and 80-mg doses.", "src": "p. 697"}},
        {"topic": "Colchicine timing",
         "slides": {"text": "Best started within 24 hours of flare onset.", "src": "S11"},
         "textbook": {"text": "Guidelines suggest giving colchicine within 36 hours of an attack; efficacy falls after that.", "src": "p. 696"}},
    ],
    BONE: [
        {"topic": "Oral bisphosphonate absorption",
         "slides": {"text": "Poor oral absorption (under 1%).", "src": "S53"},
         "textbook": {"text": "Less than 10% of an oral dose is absorbed.", "src": "p. 819"}},
    ],
}

DISCREPANCIES = [
    ("**Febuxostat CV risk:** the slides teach a boxed warning for cardiovascular death; the textbook says early MACE concerns were not borne out. Answer course exams with the slide version (boxed warning).", "S13; p. 697"),
    ("**Colchicine window:** slides say best within 24 hours of onset; the textbook cites a 36-hour guideline window. Both agree: start early.", "S11; p. 696"),
    ("**ULT prophylaxis:** slides give colchicine or an NSAID for 3–6 months; the textbook says 6 months or longer. Answer with the slides.", "S13; p. 695"),
    ("**Bisphosphonate absorption and holidays:** slides say under 1% absorbed and a holiday after 3–5 years of oral therapy; the textbook says under 10% absorbed and reassessment after 5 years (3 for zoledronate).", "S48; S53; p. 819; p. 820"),
    ("**Starting vs. stopping in a flare:** don’t *start* urate-lowering therapy during a flare (slides), but don’t *stop* allopurinol a patient already takes (textbook).", "S9; p. 696"),
]

CRAM = [
    ("Allopurinol dosing", "Start 100 mg/d (≤50 in CKD); titrate to uric acid <6 mg/dL; max 800", "p. 695"),
    ("Allopurinol hypersensitivity", "2–4 weeks in; stop at first rash; screen HLA-B 5801 in Han Chinese, Korean, Thai", "p. 696"),
    ("Colchicine flare dose", "1.2 mg, then 0.6 mg 1 h later", "p. 696"),
    ("Gout steroid option", "Prednisone 30–50 mg/d × 1–2 days, taper 7–10 days; good in CKD", "p. 698"),
    ("Pegloticase dose", "8 mg IV every 2 weeks; premedicate", "p. 698"),
    ("Probenecid", "Start 2–3 weeks after an attack; urine pH > 6.0; ↓ penicillin secretion", "p. 698"),
    ("Dantrolene in MH", "1 mg/kg IV, repeat; RyR1 (heart uses RyR2)", "p. 513"),
    ("Succinylcholine dangers", "Hyperkalemia (burns, denervation, trauma); MH trigger", "p. 508"),
    ("Sugammadex", "Reverses rocuronium/vecuronium; backup contraception 7 days", "p. 509; p. 510"),
    ("Bisphosphonate doses", "Alendronate 70 mg/wk · risedronate 35 mg/wk · ibandronate 150 mg/mo · zoledronate 5 mg/yr", "p. 818"),
    ("Teriparatide · abaloparatide", "20 mcg · 80 mcg SC daily; 2 years", "p. 827"),
    ("Raloxifene", "Spine, not hip; VTE; no hot-flush relief", "p. 827"),
    ("Vitamin D", "600 IU/d adults; deficiency 1000–4000 IU/d or 50,000 IU/week", "p. 825"),
]

QUESTIONS = [
    dict(topic=GOUT, kind="vignette",
         stem="A patient with gout and CKD stage 3 is starting allopurinol. Which textbook starting dose fits?",
         correct="No more than 50 mg/d, titrated by 50 mg",
         why_correct="In chronic kidney disease the initial allopurinol dose should not exceed 50 mg/d, with 50-mg titrations (p. 695).",
         distractors=[("300 mg/d from day one to reach target fast", "High starting doses raise hypersensitivity risk (p. 696)."),
                      ("800 mg/d, the usual maximum dose", "800 mg/d is the ceiling, not the start (p. 695)."),
                      ("100 mg/d, the same as normal kidney function", "100 mg/d is the usual start without CKD (p. 695)."),
                      ("Allopurinol is not used at all in CKD", "It is used with a lower start (p. 695).")],
         src="p. 695"),
    dict(topic=SMR, kind="vignette",
         stem="A young man with extensive burns needs emergency intubation. Why is succinylcholine avoided?",
         correct="Potassium release can cause cardiac arrest",
         why_correct="Burns and denervation proliferate extrajunctional receptors; succinylcholine then releases potassium, which can cause cardiac arrest (p. 508).",
         distractors=[("It is reversed too quickly by sugammadex", "Sugammadex reverses rocuronium and vecuronium, not succinylcholine (p. 509)."),
                      ("It lasts many hours in burned patients", "Its block lasts under 10 minutes (p. 507)."),
                      ("Burns make it a nondepolarizing blocker", "It remains depolarizing (p. 503)."),
                      ("It cannot reach the burned muscle tissue", "The danger is hyperkalemia (p. 508).")],
         src="p. 508"),
    dict(topic=BONE, kind="mechanism",
         stem="Why does raloxifene suit some patients with vertebral osteoporosis but not those whose main risk is hip fracture?",
         correct="It reduces spine fractures but not hip fractures",
         why_correct="Raloxifene protects against spine fractures but not hip fractures, unlike bisphosphonates, denosumab, and teriparatide (p. 827).",
         distractors=[("It builds new bone only in the hip", "It is antiresorptive and spine-protective (p. 827)."),
                      ("It raises hip fracture risk through VTE", "VTE is a clotting risk, not a fracture mechanism (p. 827)."),
                      ("It must be stopped after 2 years", "The 2-year limit is teriparatide (p. 827)."),
                      ("It is contraindicated in all women over 65", "Not a taught contraindication (p. 827).")],
         src="p. 827"),
]

COMPARISONS = {
    GOUT: [
        {"title": "Gout drugs in the reading (textbook)", "columns": ["Drug", "Dose / PK", "What sets it apart"],
         "rows": [["Allopurinol", "Start 100 mg/d; +100 mg every 2–5 weeks to <6 mg/dL (max 800); oxypurinol t½ 15 h", "Pruritic rash 3%; AHS 2–4 weeks in; HLA-B 5801 (Han Chinese, Korean, Thai); cut azathioprine 75%"],
                  ["Colchicine", "1.2 mg then 0.6 mg; prophylaxis 0.6 mg once–twice daily; t½ 9 h", "Within 36 h (guideline); not dialyzable; no longer given IV"],
                  ["Febuxostat", "40 or 80 mg daily; target <6.0 mg/dL", "Safe in moderate CKD; for allopurinol intolerance"],
                  ["NSAIDs", "Any except aspirin, salicylates, tolmetin", "Aspirin ≤2.6 g/d retains urate"],
                  ["Pegloticase", "8 mg IV every 2 weeks; t½ 6–14 days", "With methotrexate fewer reactions; flares first 3–6 months; avoid in G6PD deficiency"],
                  ["Probenecid (lesinurad withdrawn 2019)", "0.5 g/d → 1 g/d after 1 week", "Start 2–3 weeks after an attack; high urine volume, pH > 6.0; ↓ penicillin secretion"],
                  ["Glucocorticoids in gout", "Prednisone 30–50 mg/d × 1–2 days, taper 7–10 days; intra-articular triamcinolone", "Rule out joint infection; good in CKD"],
                  ["Interleukin-1 inhibitors in gout", "Anakinra 100 mg/day × 3 days; canakinumab 150 mg once", "Not FDA approved for gout; option when standard drugs fail"]],
         "src": "p. 695; p. 696; p. 697; p. 698"},
    ],
    SMR: [
        {"title": "Spasmolytics in the reading (textbook)", "columns": ["Drug", "Dose / PK", "What sets it apart"],
         "rows": [["Baclofen", "15 mg twice daily → 100 mg daily; t½ 3–4 h; intrathecal", "Less sedating than diazepam; withdraw very slowly; caution in pregnancy"],
                  ["Tizanidine", "2 mg every 6–8 h, max 36 mg/d", "1/10–1/15 of clonidine’s BP effect; hypotension 16–33%; CYP1A2; rebound hypertension"],
                  ["Diazepam", "4 mg/d → max 60 mg/d", "GABA-A; works for spasm of any origin but sedates"],
                  ["Cyclobenzaprine", "20–40 mg/d in divided doses", "Antimuscarinic; confusion, hallucinations; not for CP or cord injury"],
                  ["Carisoprodol, meprobamate", "Schedule IV", "Withdrawal syndrome after extensive use"],
                  ["Botulinum toxin", "Injected; lasts weeks to months", "Cleaves SNAP-25/synaptobrevin; dystonia, spastic disorders; black box: spread of toxin"],
                  ["Dantrolene", "25 mg/d → 100 mg four times daily; MH 1 mg/kg IV", "RyR1 only; weakness, sedation, hepatitis"],
                  ["Gabapentin, pregabalin", "Not covered in materials", "Other centrally acting spasmolytic drugs: promising in MS spasticity"]],
         "src": "p. 511; p. 512; p. 513"},
        {"title": "Neuromuscular blockers (anesthesia) — the reading’s essentials", "columns": ["", "Nondepolarizing (rocuronium, vecuronium, cisatracurium)", "Depolarizing (succinylcholine)"],
         "rows": [["Normal neuromuscular function → mechanism of action", "Compete with ACh at the nicotinic end-plate receptor", "Agonist: depolarizes and holds the end plate (phase I), then desensitizes (phase II)"],
                  ["Skeletal muscle paralysis", "Onset: rocuronium fastest (60–120 s)", "Fasciculations, then paralysis < 90 s; lasts < 10 min"],
                  ["Neuromuscular response to cholinesterase inhibitors", "Reversed (neostigmine); sugammadex for rocuronium/vecuronium", "Phase I block augmented, not reversed"],
                  ["Cardiovascular effects", "Vecuronium, cisatracurium, rocuronium: minimal; histamine release with atracurium/tubocurarine", "Arrhythmias; bradycardia with a repeat dose"],
                  ["Neuromuscular blockade enhanced by", "Volatile anesthetics (isoflurane most), aminoglycosides, myasthenia gravis, old age", "Plasma cholinesterase variants (dibucaine number)"],
                  ["Key dangers", "Residual block → hypoventilation", "Hyperkalemia (burns, denervation); MH trigger; ↑ intraocular and intragastric pressure"]],
         "src": "p. 500; p. 503; p. 504; p. 507; p. 508; p. 509"},
    ],
    BONE: [
        {"title": "Hormones and drugs in bone mineral homeostasis (textbook)", "columns": ["Regulator / drug", "What it does", "Clinical use or point"],
         "rows": [["Parathyroid hormone (PTH)", "↑ serum calcium, ↓ phosphate; ↑ 1,25(OH)₂D; RANKL via osteoblasts", "Intermittent PTH 1-34 (teriparatide) is anabolic; rhPTH 1-84 for hypoparathyroidism"],
                  ["Vitamin D (1,25-dihydroxyvitamin D)", "↑ gut calcium and phosphate absorption", "Vitamin D preparations: D3 preferred; calcitriol when speed matters"],
                  ["Fibroblast growth factor 23", "↓ phosphate reabsorption and 1,25(OH)₂D", "Burosumab (anti-FGF23) for X-linked hypophosphatemia"],
                  ["Calcitonin (secondary regulator)", "Inhibits osteoclasts; ↓ calcium and phosphate", "Salmon form lasts 40–50 min; Paget, hypercalcemia, osteoporosis (weaker)"],
                  ["Glucocorticoids", "Net bone loss", "Common cause of adult osteoporosis; treat sarcoid/vitamin D hypercalcemia"],
                  ["Estrogens", "Reduce PTH-driven resorption", "Prevent postmenopausal loss; long-term use out of favor → SERMs"],
                  ["Sclerostin antibodies (romosozumab)", "Unblock Wnt → osteoblasts; ↓ resorption", "1 year, then antiresorptive; MI/stroke boxed warning"],
                  ["Calcimimetics (cinacalcet, etelcalcetide)", "Activate the calcium-sensing receptor → ↓ PTH", "Secondary hyperparathyroidism in CKD; cinacalcet 30 → 90 mg"],
                  ["Thiazide diuretics", "↓ renal calcium excretion", "Idiopathic hypercalciuria stones; avoid loop diuretics there"],
                  ["Fluoride", "Stabilizes hydroxyapatite", "Dental caries; not FDA approved for osteoporosis (fractures not reduced)"],
                  ["Strontium ranelate", "↓ resorption, ↑ formation", "Europe only; not approved in the USA"]],
         "src": "p. 813; p. 815; p. 816; p. 817; p. 818; p. 819; p. 820; p. 821; p. 824; p. 825"},
        {"title": "Calcium and phosphate disorders (textbook, clinical pharmacology)", "columns": ["Disorder", "Drug approach", "Pearl"],
         "rows": [["Hypercalcemia", "Saline diuresis 500–1000 mL/h, then furosemide; pamidronate 60–90 mg or zoledronate 4 mg IV; calcitonin", "Calcitonin acts in 4–6 h; gallium nitrate seldom used; glucocorticoids for sarcoid, vitamin D, myeloma"],
                  ["Hypocalcemia", "IV 10% calcium gluconate slowly; oral 1000–1500 mg elemental/day; calcitriol 0.25–1 mcg", "Calcium carbonate 40% calcium (with meals if achlorhydric) vs. citrate 21%; check magnesium"],
                  ["Hyperphosphatemia", "Diet + binders: sevelamer, lanthanum, calcium", "Aluminum binders sparingly (bone disease)"],
                  ["Hypophosphatemia", "Oral phosphate", "Long term: weakness, osteomalacia"],
                  ["Primary hyperparathyroidism", "Surgery; cinacalcet if not a candidate", "Rule out familial hypocalciuric hypercalcemia"],
                  ["Hypoparathyroidism", "Calcitriol + calcium; rhPTH 1-84", "Hypercalciuria limits standard therapy"],
                  ["Nutritional vitamin D deficiency or insufficiency", "D2 or D3 1000–4000 IU/d or 50,000 IU/week", "25(OH)D > 12 ng/mL prevents rickets; 20–30 ng/mL target"],
                  ["Chronic kidney disease", "Calcitriol, doxercalciferol, paricalcitol; binders", "Keep calcium × phosphate < 55"],
                  ["Intestinal osteodystrophy (malabsorption)", "High-dose vitamin D 25,000–50,000 IU", "Osteoporosis + osteomalacia"],
                  ["Idiopathic hypercalciuria", "Hydrochlorothiazide up to 50 mg twice daily", "Not loop diuretics; allopurinol an alternative"],
                  ["Paget disease of bone", "Bisphosphonates (higher doses), calcitonin", "Follow alkaline phosphatase"],
                  ["Enteric oxaluria", "Calcium carbonate 1–2 g/day", "Calcium binds gut oxalate"]],
         "src": "p. 822; p. 823; p. 824; p. 825; p. 826; p. 829"},
    ],
}

DEEPER = {
    GOUT: (36, 695, 698, "Every gout drug’s dosing, toxicity, and interactions"),
    SMR: (27, 510, 514, "Spasmolytics, botulinum toxin, dantrolene, and the neuromuscular blockers"),
    BONE: (42, 818, 828, "Osteoporosis drugs, calcium and vitamin D therapy, and calcium disorders"),
}

_CH36_L03 = ["THE IMMUNE RESPONSE", "THERAPEUTIC STRATEGIES", "Chemistry & Pharmacokinetics", "ASPIRIN", "NONACETYLATED SALICYLATES",
             "COX-2 SELECTIVE INHIBITORS", "Other NSAIDs", "CHOICE OF NSAID", "DISEASE-MODIFYING ANTIRHEUMATIC DRUGS", "ABATACEPT",
             "ANIFROLUMAB", "APREMILAST", "AZATHIOPRINE", "BARICITINIB", "BELIMUMAB", "RISANKIZUMAB", "CHLOROQUINE AND HYDROXYCHLOROQUINE",
             "INTERLEUKIN-1 INHIBITORS", "GUSELKUMAB", "IXEKIZUMAB", "JANUS KINASE INHIBITORS", "LEFLUNOMIDE", "MESALAMINE",
             "Baricitinib Tofacitinib Upadacitinib", "MYCOPHENOLATE MOFETIL", "SARILUMAB", "SECUKINUMAB", "SULFASALAZINE", "TOCILIZUMAB",
             "USTEKINUMAB", "BIOSIMILARS", "GLUCOCORTICOID DRUGS (LIMITED TO RHEUMATIC DISEASES)", "OTHER ANALGESICS", "ACETAMINOPHEN",
             "KETOROLAC", "TRAMADOL"]

READING_SKIP = (
    [{"heading": h, "reason": "Taught in L03 (Session 1: NSAIDs, DMARDs, and other analgesics, Ch. 36)"} for h in _CH36_L03]
    + [{"heading": "Disease-Modifying Antirheumatic Drugs & Glucocorticoids", "reason": "Reference-list heading (citations only, no teaching content)"},
       {"heading": "Gabarone, Gralise, Neurontin", "reason": "Preparations list (brand names only, no teaching content)"},
       {"heading": "BASIC PHARMACOLOGY", "reason": "Chapter part label; its content is taught under the subheadings"},
       {"heading": "CLINICAL PHARMACOLOGY", "reason": "Chapter part label; its content is taught under the subheadings"},
       {"heading": "IDIOPATHIC INFANTILE HYPERCALCEMIA", "reason": "Beyond PA scope for this lecture (rare CYP24A1 genetic disorder; no prescribing decision beyond avoiding vitamin D)"},
       {"heading": "NEPHROTIC SYNDROME", "reason": "Beyond PA scope for this lecture (vitamin D loss in nephrotic syndrome; the textbook notes no trials to guide therapy)"}]
)
