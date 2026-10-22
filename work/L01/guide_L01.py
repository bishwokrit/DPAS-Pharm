"""Study-guide extras for L01 (6-sentence summary, flow diagrams, cram sheet). Imported by author_L01.py."""

# Home-page teaser (two sentences, shown on the class day and until the next lecture)
TEASER = 'This week: how drugs act on receptors, why potency isn’t efficacy, and what first-pass metabolism does to an oral dose. One cited guide and exam-style practice — no more hours lost rereading the textbook.'

SUMMARY = [
    ("Pharmacology studies how drugs interact with living systems: **pharmacokinetics** is what the body does to the drug (ADME), and **pharmacodynamics** is what the drug does to the body.", "S5; S6"),
    ("Learn and prescribe by **generic name** — brand names can hide a shared ingredient and cause unintentional double-dosing.", "S7; S9"),
    ("Drugs move from discovery through preclinical testing, **Phase I–III** trials, FDA review, and **Phase IV** postmarketing surveillance — where rare adverse effects are often first found.", "S12; S13; S12 (notes)"),
    ("Drugs act on five target classes; a **competitive antagonist** shifts the dose-response curve right (same Emax), while a **noncompetitive/irreversible** antagonist lowers Emax.", "S20; S22 (notes)"),
    ("**Potency** (EC₅₀) is the dose needed and **efficacy** (Emax) is the ceiling — efficacy matters more — and narrow-TI drugs (**warfarin, lithium, digoxin, phenytoin**) need careful dosing and blood levels.", "S30; S34; S38"),
    ("Oral drugs face **first-pass** hepatic metabolism that lowers bioavailability (IV = 100%), and distribution depends on protein binding, lipid solubility, perfusion, and barriers like the BBB.", "S50; S51; S52; S53"),
]

FLOWS = {
    "Drug Development & Regulation": [
        {"title": "From discovery to patient", "steps": ["Discovery", "Preclinical testing", "Clinical trials (Phases I–III)", "FDA review", "Approval", "Postmarket surveillance (Phase IV)"], "src": "S12; S13"},
    ],
    "Pharmacodynamics: Targets & Receptors": [
        {"title": "The pharmacodynamic pathway", "steps": ["Drug", "Target (e.g., receptor)", "Signal transduction", "Pharmacologic response"], "src": "S19 (notes); S21"},
        {"title": "Albuterol: receptor → second messenger → effect", "steps": ["Albuterol binds β2-adrenergic receptor", "β2 receptor activated", "↑ intracellular cAMP", "Bronchial smooth muscle relaxes", "Bronchodilation"], "src": "S26"},
        {"title": "Competitive antagonism", "steps": ["Antagonist reversibly occupies the agonist's site", "More agonist needed for same effect", "Curve shifts right", "Same Emax still reachable (surmountable)"], "src": "S22; S22 (notes); S25"},
    ],
    "Pharmacokinetics: ADME — Absorption & Distribution": [
        {"title": "ADME", "steps": ["Dose", "Absorption → blood", "Distribution → tissues", "Metabolism (mainly liver)", "Excretion (mainly kidney)"], "src": "S45; S46"},
        {"title": "First-pass effect (oral route)", "steps": ["Oral drug", "GI tract", "Portal circulation", "Liver (first-pass metabolism)", "Systemic circulation"], "src": "S51"},
    ],
}

CRAM = [
    # language
    ("Pharmacology", "Study of how drugs interact with living systems — molecule to whole patient", "S5"),
    ("Drug (medication)", "Chemical used to diagnose, treat, cure, prevent disease, or alter a physiologic process", "S5"),
    ("Pharmacologic vs. therapeutic effect", "Any measurable biological change vs. the intended, beneficial effect", "S5"),
    ("Adverse drug reaction (ADR)", "Unintended, harmful response at **normal therapeutic doses**", "S5"),
    ("Toxicity", "Harm when dose/exposure **exceeds the therapeutic range**", "S5"),
    ("Chemical / generic / brand name", "Exact structure (rarely used) / official non-proprietary, one per drug / manufacturer's, many, vary by country", "S7"),
    ("Why prescribe by generic name", "Unambiguous, international; avoids hidden duplicate therapy (double-dosing)", "S7; S9"),
    ("Tylenol", "Brand name of acetaminophen", "S7"),
    ("Pharmacokinetics vs. pharmacodynamics", "Body → drug (ADME) vs. drug → body (receptors & effect)", "S6"),
    ("Pharmacogenomics", "How genetic variation shapes individual drug response", "S6"),
    ("Clinical pharmacology / toxicology", "Applying PK/PD to real patients; the study of poisoning", "S6"),
    # development
    ("4 sources of new drugs", "Natural products · synthetic & biotech · biologics · drug repurposing", "S11"),
    ("Biologics", "Monoclonal antibodies, gene- and cell-based therapies", "S11"),
    ("Drug pipeline", "Discovery → preclinical → clinical trials → FDA review → approval → postmarket surveillance", "S12"),
    ("Phase I", "Safety, tolerability, dose-finding — small group of **healthy volunteers**", "S13"),
    ("Phase II", "Preliminary efficacy & side effects — a few hundred patients with the condition", "S13"),
    ("Phase III", "Confirm efficacy, monitor AEs at scale — hundreds to thousands, multi-site", "S13"),
    ("Phase IV", "Postmarketing surveillance — general prescribed population", "S13"),
    ("Rare AE (1 in 10,000)", "Often first found in Phase IV — trials too small/short", "S12 (notes)"),
    ("Efficacy vs. effectiveness", "Ideal trial conditions vs. everyday practice (adherence, comorbidities)", "S14"),
    ("FDA MedWatch", "Adverse-event reporting system (voluntary + mandatory)", "S14"),
    ("Risk-benefit case: 70% improve, 1% serious hepatotoxicity", "Always comparative — \"compared to what?\"", "S15; S15 (notes)"),
    # PD
    ("5 drug target classes", "Receptors · ion channels · enzymes · transporters · nucleic acids", "S20"),
    ("Receptor types", "G-protein-coupled · ligand-gated ion channel · enzyme-linked · nuclear", "S20"),
    ("Most common targets", "Receptors and enzymes (ion channels/transporters: cardiac & CNS drugs)", "S20 (notes)"),
    ("Full / partial / inverse agonist", "Maximal activation / submaximal even at full occupancy / lowers baseline activity", "S22"),
    ("Competitive antagonist", "Same site, reversible, overcome by more agonist → **curve right, same Emax**", "S22; S22 (notes)"),
    ("Noncompetitive / irreversible antagonist", "Binds elsewhere or irreversibly → **lower Emax**; irreversible lasts until new receptor made", "S22; S22 (notes)"),
    ("Albuterol", "Selective β2 agonist → ↑ cAMP → bronchial smooth muscle relaxes → bronchodilation", "S26"),
    # dose-response
    ("Potency", "Dose needed for an effect — **lower EC₅₀ = more potent**", "S30; S34"),
    ("Efficacy (Emax)", "Maximum possible effect — **higher Emax = more efficacious**; matters more clinically", "S30; S34"),
    ("EC₅₀", "Concentration giving 50% of Emax — standard measure of potency", "S30"),
    ("Therapeutic index", "**TI = TD₅₀ ÷ ED₅₀**; narrow = careful dosing + blood levels", "S38"),
    ("Narrow-TI drugs", "**Warfarin, lithium, digoxin, phenytoin**", "S38"),
    # PK
    ("ADME", "Absorption → distribution → metabolism (mainly liver) → excretion (mainly kidney)", "S45"),
    ("Bioavailability (F)", "Fraction of dose reaching systemic circulation unchanged; **IV = 100%**", "S50"),
    ("Why oral F < 100%", "Incomplete absorption + first-pass hepatic metabolism", "S50"),
    ("First-pass path", "Oral → GI tract → portal circulation → liver → systemic circulation", "S51"),
    ("Big first-pass drugs", "Nitroglycerin, propranolol, morphine — need higher oral doses", "S51"),
    ("Routes that bypass first-pass", "Every route except oral (IV, sublingual, inhaled, transdermal, topical, SC, IM)", "S49 (notes)"),
    ("Sublingual", "Directly into systemic venous circulation — skips portal vein & liver", "S49; S55"),
    ("IM / SC / transdermal", "Faster than oral, depot · slower steady (insulin, heparin) · slow sustained", "S49"),
    ("Inhaled / topical", "Rapid local lung effect · local effect, minimal systemic absorption", "S49"),
    ("Plasma protein binding", "Only **free (unbound)** drug is active and crosses membranes", "S52"),
    ("Tissue perfusion", "Brain, heart, kidney get drug fast; fat, bone slowly", "S52"),
    ("Volume of distribution (Vd)", "Total drug in body vs. plasma concentration; theoretical; high = in tissue (digoxin)", "S52; S52 (notes)"),
    ("Blood-brain barrier", "Tight junctions; small, lipophilic, non-ionized cross; P-glycoprotein pumps out", "S53"),
    ("Polar antibiotic + meningitis", "Usually poor BBB entry — better when meninges are inflamed", "S53 (notes)"),
]
