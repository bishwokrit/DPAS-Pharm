"""Study-guide extras for L04 (6-sentence summary, flow diagrams, cram sheet). Imported by author_L04.py."""

# Home-page teaser (two sentences, shown on the class day and until the next lecture)
TEASER = "Today: gout’s two treatment phases, central vs. peripheral muscle relaxants, and the drugs that tip the bone remodeling balance. One cited guide and exam-style practice, with the Unit 2 recall quiz rebuilt."

SUMMARY = [
    ("Gout runs **purine → uric acid (xanthine oxidase) → urate crystals → neutrophil flare**; treat the **flare** with colchicine, an NSAID, or a corticosteroid, and **never start urate-lowering therapy during a flare**.", "S5; S7; S14; SG U2-R10"),
    ("**Allopurinol/febuxostat** cut uric acid production (xanthine oxidase), **probenecid** raises excretion (URAT1), and **pegloticase** breaks uric acid down — watch HLA-B*58:01, febuxostat’s CV boxed warning, and G6PD deficiency.", "S10; S11; S12; S13; SG U2-R9"),
    ("Muscle relaxants sort by site: **central** (baclofen GABA-B, tizanidine α2, cyclobenzaprine brainstem) vs. **peripheral** (**dantrolene** on RyR1 in muscle; botulinum toxin at the junction).", "S19; S20; SG U2-R11"),
    ("**Dantrolene** is the emergency drug for **malignant hyperthermia**; never stop intrathecal **baclofen** abruptly; check **LFTs** and CYP1A2 inhibitors with tizanidine; cyclobenzaprine is anticholinergic (Beers).", "S22; S24; S26; S28; S29"),
    ("Bone is a **balance**: PTH answers low calcium via bone, kidney, and gut; **bisphosphonates** (first-line), **denosumab**, raloxifene, and calcitonin slow resorption, while **teriparatide/abaloparatide** and **romosozumab** build bone.", "S32; S35; S37; S42; S44; SG U2-R12"),
    ("Oral bisphosphonates need a **full glass of water, fasting, and 30 minutes upright**; denosumab must not just be stopped, teriparatide is 2 years, and romosozumab carries an MI/stroke boxed warning.", "S40; S41; S43; SG U2-R13"),
]

FLOWS = {
    "Gout: Acute Flares & Urate-Lowering Therapy": [
        {"title": "From purines to a flare", "steps": ["Purine breakdown", "Hypoxanthine → xanthine", "Uric acid (xanthine oxidase)", "Hyperuricemia", "Monosodium urate crystals in joint", "Neutrophil/macrophage activation (NLRP3, IL-1β)", "Acute flare"], "src": "S5"},
        {"title": "Gout visit decision", "steps": ["Acute flare?", "Yes → colchicine, NSAID, or corticosteroid now", "Defer urate-lowering therapy", "Flare resolved → start allopurinol low, titrate to urate target", "Cover with colchicine/NSAID prophylaxis 3–6 months", "Refractory → pegloticase (check G6PD)"], "src": "S7; S11; S13; S14"},
        {"title": "How colchicine works", "steps": ["Colchicine binds tubulin", "Blocks microtubule polymerization", "Reduced neutrophil migration and NLRP3 activation", "Less inflammation at the crystal site"], "src": "S9"},
    ],
    "Skeletal Muscle Relaxants": [
        {"title": "Where muscle tone is controlled", "steps": ["Upper motor neurons (descending inhibition)", "Spinal interneurons (GABA, glycine, α2) — baclofen, tizanidine", "Alpha motor neuron", "Neuromuscular junction (ACh) — botulinum toxin", "Muscle fiber (SR Ca²⁺ release) — dantrolene"], "src": "S18"},
        {"title": "Baclofen", "steps": ["Binds GABA-B receptors", "Opens K⁺, closes Ca²⁺ channels (presynaptic inhibition)", "Less excitatory transmitter", "Lower motor neuron firing → less spasticity"], "src": "S22"},
        {"title": "Dantrolene", "steps": ["Action potential → DHPR activated", "RyR1 opens → Ca²⁺ released from SR", "Contraction", "Dantrolene blocks RyR1 → less Ca²⁺", "Relaxation"], "src": "S29"},
    ],
    "Bone Pharmacology & Osteoporosis": [
        {"title": "RANKL → osteoclast", "steps": ["Osteoblast/stromal cell expresses RANKL", "RANKL binds RANK on osteoclast precursors", "Osteoclast differentiation and activation", "Bone resorption releases calcium", "OPG (decoy) and denosumab block RANKL"], "src": "S33"},
        {"title": "How bisphosphonates kill osteoclasts", "steps": ["Bind hydroxyapatite at resorption sites", "Osteoclast takes the drug up", "N-bisphosphonates inhibit FPP synthase", "Loss of GTPase prenylation", "Osteoclast apoptosis → less resorption"], "src": "S38"},
        {"title": "Taking an oral bisphosphonate", "steps": ["First thing in the morning, fasting", "Full glass of plain water", "Stay upright 30 minutes", "No food, calcium, coffee, or antacids before then", "Less esophageal irritation"], "src": "S40; S41; SG U2-R13"},
    ],
}

CRAM = [
    ("Gout chain", "Purine → xanthine → uric acid (xanthine oxidase) → MSU crystals → neutrophil flare", "S5; S6"),
    ("Raise uric acid", "Purine/fructose diet, beer, thiazide/loop diuretics, CKD", "S5"),
    ("Flare drugs", "Colchicine, NSAIDs, corticosteroids", "S7"),
    ("Urate-lowering drugs", "Allopurinol, febuxostat (↓ production); probenecid (↑ excretion)", "S7; SG U2-R9"),
    ("ULT in a flare?", "Never start or change — it can prolong the flare", "S7; SG U2-R10"),
    ("ULT prophylaxis", "Colchicine or NSAID for 3–6 months", "S11"),
    ("Colchicine", "Microtubules · best within 24 h · diarrhea · CYP3A4/P-gp", "S8; S9"),
    ("Allopurinol", "XO inhibitor (oxypurinol) · first-line · HLA-B*58:01 · ↓ dose renal, azathioprine", "S10; S11"),
    ("Febuxostat", "XO inhibitor · boxed CV death", "S11"),
    ("Probenecid", "URAT1 block · hydrate · no uric acid stones/renal impairment", "S12; S13"),
    ("Pegloticase, rasburicase", "Uricase → allantoin · IV · no G6PD deficiency", "S13"),
    ("Spasticity vs. rigidity", "Velocity-dependent (UMN) vs. constant tone", "S17"),
    ("Central relaxants", "Cyclobenzaprine, tizanidine, baclofen (+ carisoprodol, methocarbamol, metaxalone, chlorzoxazone)", "S19"),
    ("Peripheral relaxants", "Dantrolene (muscle), botulinum toxin (junction)", "S19"),
    ("Baclofen", "GABA-B · MS/spinal cord spasticity · intrathecal · withdrawal seizures, hyperthermia", "S21; S22"),
    ("Tizanidine", "α2 agonist · hypotension, LFTs · no ciprofloxacin/fluvoxamine", "S23; S24"),
    ("Cyclobenzaprine", "Brainstem 5-HT2 · TCA-like anticholinergic · 2–3 weeks · Beers", "S25; S26"),
    ("Carisoprodol", "→ meprobamate · Schedule IV", "S27"),
    ("Dantrolene", "RyR1 · malignant hyperthermia, NMS · hepatotoxic", "S28; S29"),
    ("Malignant hyperthermia triggers", "Volatile anesthetics, succinylcholine", "S29"),
    ("Osteoporosis risk", "Age, estrogen loss, glucocorticoids, low Ca/vitamin D, inactivity", "S36"),
    ("PTH loop", "↓ Ca → PTH → bone resorption, renal reabsorption, vitamin D gut absorption", "S35; SG U2-R12"),
    ("Intermittent vs. continuous PTH", "Formation vs. resorption (↑ RANKL)", "S33"),
    ("Bisphosphonate schedules", "Alendronate/risedronate weekly · ibandronate monthly · zoledronic acid yearly IV", "S37; S39"),
    ("Bisphosphonate counseling", "Full glass of water, fasting, upright 30 min", "S40; S41; SG U2-R13"),
    ("Bisphosphonate limits", "CrCl < 30–35 · ONJ, atypical femur fracture · holiday after 3–5 y", "S38"),
    ("Denosumab", "RANKL antibody · stopping → rebound vertebral fractures", "S42; S43"),
    ("Teriparatide", "PTH 1-34 · anabolic · 2 years lifetime", "S43; SG U2-M"),
    ("Romosozumab", "Sclerostin antibody · builds + limits resorption · boxed MI/stroke/CV death", "S42; S43"),
    ("Raloxifene", "SERM · VTE, hot flashes · ↓ breast cancer risk", "S42; S43"),
    ("Name stems", "-ostat XO · -ase uricase · -curonium NMB · -dronate · -sumab · -fene SERM · -tide PTH", "S15; S30; S46"),
]
