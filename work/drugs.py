"""Cumulative drug index — one card per drug named in the course materials.

Every card has the same fields, in this order (the Drugs tab shows them all; an empty field says "Not covered in materials"):
  generic name · drug class · mechanism of action · indications · contraindications · adverse effects ·
  clinically significant interactions · distinguishing characteristics / patient-specific factors · extra information
Sources only: lecture slides ("L03 S29"), the assigned Katzung pages ("p. 677"), the course study guide ("SG U2-R5").
A fact whose source has no lecture or study-guide reference is textbook-only (shown with a TB tag).
Add new drugs as each unit is taught; reuse the class-level lists (NSAID_*, DMARD_*) so every card in a class stays complete.
"""
import re

SECTIONS = [("moa", "Mechanism of action"), ("ind", "Indications"), ("contra", "Contraindications"), ("ae", "Adverse effects"),
            ("ix", "Clinically significant interactions"), ("pt", "Distinguishing characteristics / patient-specific factors"),
            ("extra", "Extra information")]


def D(name, cls, tags, secs, aliases=(), unit=1, utd=None):
    # utd: optional exact UpToDate link; otherwise the site links an UpToDate search for the drug's name
    facts = [{"text": t, "src": s, "tb": not re.search(r"\bL\d\d|\bSG\b", s), "sec": k} for k, _ in SECTIONS for t, s in secs.get(k, [])]
    return {"name": name, "cls": cls, "tags": list(tags), "aliases": list(aliases), "unit": unit, **({"utd": utd} if utd else {}), "facts": facts}


# ---------------------------------------------------------------- class-level facts shared by every drug in the class
NSAID_MOA = [("Inhibits COX-1 and COX-2 → ↓ prostaglandins (pain, inflammation, fever) and ↓ TXA2 (bleeding risk).", "L03 S24-25; S28")]
NSAID_IND = [("Oral NSAIDs treat osteoarthritis pain effectively but carry systemic risks; topical NSAIDs give local relief with much lower systemic exposure.", "L03 S43"),
             ("Relieve symptoms but, unlike DMARDs, do not alter the course of any arthritic disorder.", "p. 676")]
NSAID_CONTRA = [("Caution/avoid: active GI bleeding or ulcer history, chronic kidney disease, heart failure or CV disease, anticoagulant therapy, late pregnancy.", "L03 S36")]
NSAID_AE = [("GI: gastritis, peptic ulcer, bleeding (less mucus/bicarbonate). Renal: ↓ afferent dilation → AKI, fluid retention. CV: hypertension, CV events. Platelets: ↓ TXA2 → bleeding.", "L03 S34-35"),
            ("Also: headache, tinnitus, dizziness, liver test abnormalities, asthma, rashes, hyperkalemia.", "p. 676")]
NSAID_IX = [("+ anticoagulant → ↑ bleeding; + ACE inhibitor/ARB → ↑ AKI (“triple whammy” with a diuretic); + diuretic → ↓ diuretic effect, ↑ renal risk; + corticosteroid → ↑ GI ulcer.", "L03 S36")]
NSAID_PT = [("Older patient with CKD, hypertension, and an anticoagulant: three NSAID red flags — acetaminophen or a non-NSAID strategy is generally safer first-line.", "L03 S37-39")]

DMARD_PT = [("Immunosuppression → infection risk: screen for TB (IGRA or TST) and hepatitis B/C, update vaccines before starting, then CBC and liver/kidney labs every 1–3 months; report fevers promptly.", "L03 S56-57")]
TNF_AE = [("Boxed warning (all TNF inhibitors): malignancy, especially lymphoma.", "p. 692"),
          ("Serious infections — latent TB reactivation, fungal and opportunistic infections, hepatitis B reactivation; new or worse heart failure; demyelinating disease; lupus-like syndrome.", "p. 690; p. 692")]


DRUGS = [
    # ---------------------------------------------------------------- Unit 1 (principles lectures) — sparse by design: later units fill these in
    D("Acetaminophen", "Analgesic and antipyretic (not an NSAID)", ["Naming", "Toxic metabolite", "Antidote", "Analgesic", "OA"], {
        "moa": [("Analgesia and antipyresis are mainly central (reduced CNS prostaglandin synthesis; hypothalamic temperature center); minimal peripheral anti-inflammatory action.", "L03 S15-16"),
                ("Textbook: a weak peripheral COX-1/COX-2 inhibitor; pain relief also involves opioid, cannabinoid, and serotonergic systems.", "p. 694")],
        "ind": [("Mild-to-moderate pain and fever; reasonable first-line for mild osteoarthritis pain.", "L03 S15; S43"),
                ("Preferred over aspirin in aspirin allergy, hemophilia, peptic ulcer history, or aspirin-induced bronchospasm; alone it is inadequate for RA.", "p. 694")],
        "contra": [("Caution in liver disease, significant alcohol use, or malnutrition (prolonged fasting, anorexia).", "p. 694")],
        "ae": [("Overdose: glutathione depleted → NAPQI accumulates → binds hepatocyte proteins → centrilobular liver necrosis.", "L03 S17; S19; SG U2-R3"),
               ("Ingesting 15 g may be fatal; even 4 g/day is associated with liver function test abnormalities.", "p. 694")],
        "ix": [("Combination cold, flu, and sleep products hide acetaminophen — unintentional double-dosing is a leading cause of liver injury. Ask about ALL sources.", "L03 S20"),
               ("Combined with an NSAID it improves pain control but can potentiate the NSAID’s GI toxicity.", "p. 694")],
        "pt": [("Chronic alcohol use and fasting lower glutathione and induce CYP2E1 → higher toxicity risk.", "L03 S17"),
               ("Safer first-line than an NSAID when NSAID red flags (CKD, anticoagulant, older age) stack up.", "L03 S37"),
               ("Generic name — sold as Tylenol and many store brands; two brands can hide the same ingredient.", "L01 S7; S9; SG U1-R2")],
        "extra": [("Metabolism: ~90% glucuronidation/sulfation (safe); ~5–10% CYP2E1 → NAPQI, neutralized by glutathione at therapeutic doses.", "L03 S16"),
                  ("Acute single ingestion: plot a 4-hour-or-later level on the Rumack-Matthew nomogram — above the line, give N-acetylcysteine (early); check AST/ALT. Not used after 24 h or for chronic ingestion.", "L03 S17-18"),
                  ("Normal Phase I metabolism makes the toxic metabolite NAPQI (Lecture 1’s example).", "L02 S4 (notes)"),
                  ("Adults generally no more than 4 g/day; half-life 2–3 h; N-acetylcysteine within 8–16 hours prevents fulminant hepatotoxicity.", "p. 694; p. 66")],
    }, aliases=["Tylenol", "NAPQI"]),
    D("Albuterol", "Selective β2-adrenergic receptor agonist", ["Receptors", "Inhaled"], {
        "moa": [("Binds and activates β2 → ↑ intracellular cAMP → bronchial smooth muscle relaxes → bronchodilation.", "L01 S26")],
        "extra": [("The lecture’s model for receptor-to-response logic you reuse for every agonist.", "L01 S26")],
    }),
    D("Warfarin", "Anticoagulant", ["Narrow TI", "Protein-bound", "Pharmacogenomics", "CYP interactions"], {
        "ix": [("NSAIDs + anticoagulants → ↑ bleeding risk.", "L03 S36"),
               ("Inducers (barbiturates, St. John’s wort) lower its level; stopping the inducer raises it and can cause bleeding.", "p. 72"),
               ("Celecoxib (CYP2C9 substrate) occasionally interacts; tocilizumab stimulates CYP450, so warfarin doses may need adjusting.", "p. 679; p. 692")],
        "pt": [("Dose requirements vary up to 20-fold; CYP2C9 and VKORC1 genotypes explain much of it.", "p. 90")],
        "extra": [("Classic narrow-therapeutic-index drug — careful dosing and blood-level monitoring.", "L01 S38; SG U1-R7"),
                  ("99% protein-bound; half-life about 37 h.", "p. 45")],
    }),
    D("Lithium", "Not covered in materials", ["Narrow TI", "Renal dosing"], {
        "ix": [("Celecoxib raises lithium levels.", "p. 679"),
               ("Thiazides raise lithium levels — monitor.", "L09 S38; p. 280")],
        "pt": [("Renally cleared with a narrow TI — adjust dose or interval in renal impairment.", "L02 S15")],
        "extra": [("Classic narrow-TI drug requiring blood-level monitoring.", "L01 S38; SG U1-R7"),
                  ("About 95% excreted unchanged in urine, 0% protein-bound; target ~0.7 mEq/L, toxic above 2 mEq/L; half-life ~22 h.", "p. 44")],
    }),
    D("Digoxin", "Not covered in materials", ["Narrow TI", "High Vd", "Renal dosing", "Transporters"], {
        "ix": [("Inhibiting P-glycoprotein (MDR1) raises digoxin blood levels.", "p. 9"),
               ("Hypokalemia from loop diuretics increases digoxin toxicity.", "L09 S38; p. 278")],
        "pt": [("Renally cleared — adjust dose or interval in renal impairment.", "L02 S15"),
               ("Older adult with CrCl 22 mL/min: clearance falls to 3.7 L/h, so about 127 mcg/day (two 62.5-mcg tablets); draw levels at least 6 hours after a dose.", "p. 55; p. 56")],
        "extra": [("Classic narrow-TI drug requiring blood-level monitoring.", "L01 S38; SG U1-R7"),
                  ("Very high Vd — mostly sequestered in tissue, not plasma.", "L01 S52 (notes)"),
                  ("Vd ~500 L, half-life ~39 h; target ~1 ng/mL, toxic above 2 ng/mL.", "p. 44")],
    }),
    D("Phenytoin", "Not covered in materials", ["Narrow TI", "Saturable elimination", "CYP inducer"], {
        "ix": [("A CYP inducer — lowers levels of CYP substrates.", "p. 63; p. 64")],
        "extra": [("Classic narrow-TI drug requiring blood-level monitoring.", "L01 S38; SG U1-R7"),
                  ("Capacity-limited (saturable) elimination — clearance falls as concentration rises.", "p. 47"),
                  ("Target ~10 mg/L, toxic above 20 mg/L; 89% protein-bound.", "p. 45")],
    }),
    D("Nitroglycerin", "Not covered in materials", ["First-pass", "Routes"], {
        "pt": [("Large first-pass effect — needs a higher oral dose or a non-oral route; sublingual dosing enters systemic veins directly, bypassing the liver.", "L01 S51; S55; SG U1-R9")],
    }),
    D("Propranolol", "Nonselective β-adrenoceptor antagonist (β blocker)", ["First-pass", "Receptors", "Competitive antagonist"], {
        "moa": [("Competitive β antagonist: exercise or stress catecholamines can overcome a fixed dose.", "p. 25")],
        "contra": [("Asthma: blocking β2 can cause bronchoconstriction — a β1-selective blocker is an alternative.", "p. 41")],
        "ae": [("Bronchoconstriction in asthma (β2 blockade).", "p. 41")],
        "pt": [("Large first-pass effect — much higher oral than IV dose for the same exposure.", "L01 S51; SG U1-R9"),
               ("Slows heart rate markedly in pheochromocytoma but not a trained runner’s resting rate.", "p. 39")],
    }),
    D("Metoprolol", "β1-selective adrenoceptor antagonist", ["Receptors"], {
        "moa": [("Binds preferentially to β1 (heart), with lower affinity for β2.", "p. 41")],
        "pt": [("An alternative to propranolol in a patient with asthma.", "p. 41")],
    }),
    D("Morphine", "Opioid analgesic", ["First-pass", "Pharmacogenomics"], {
        "pt": [("Large first-pass effect.", "L01 S51; SG U1-R9")],
        "extra": [("Active metabolite of codeine, about 200× more potent than codeine.", "p. 81")],
    }),
    D("Codeine", "Opioid (prodrug)", ["Pharmacogenomics", "Prodrug"], {
        "moa": [("Prodrug: CYP2D6 converts it to morphine.", "L02 S33; p. 81")],
        "pt": [("CYP2D6 poor metabolizers get little relief; ultrarapid metabolizers risk toxicity — CPIC recommends an alternative analgesic for both.", "L02 S33; SG U1-R12; p. 81; p. 82")],
    }),
    D("Clopidogrel", "Antiplatelet (prodrug)", ["Pharmacogenomics", "Prodrug"], {
        "moa": [("Prodrug: about 85% of a dose is inactivated by esterases; CYP2C19 forms the active metabolite.", "p. 81")],
        "pt": [("CYP2C19 variation affects activation; poor/intermediate metabolizers after PCI → prasugrel or ticagrelor (CPIC).", "L02 S33; p. 81; p. 82")],
    }),
    D("Azathioprine", "Thiopurine immunosuppressant · conventional DMARD", ["Pharmacogenomics", "DMARD"], {
        "moa": [("Converted to 6-mercaptopurine and then 6-thioguanine, which suppresses B- and T-cell function, immunoglobulin production, and IL-2.", "p. 682")],
        "ind": [("Active rheumatoid arthritis (2 mg/kg/day orally); prevents kidney transplant rejection.", "p. 682; p. 683")],
        "ae": [("Bone marrow suppression, GI disturbance, carcinogenicity, increased infection risk.", "p. 683")],
        "ix": [("Allopurinol (xanthine oxidase inhibitor) raises levels — reduce the dose (textbook: by 75%).", "L04 S13; p. 696")],
        "pt": [("TPMT deficiency raises thiopurine toxicity risk.", "L02 S33; SG U1-R12"),
               ("TPMT intermediate activity: start at 30–70% of the target dose; deficient: drastically reduce or use an alternative. NUDT15 variants also predict leukopenia.", "p. 83; p. 683")],
    }),
    D("Allopurinol", "Xanthine oxidase inhibitor (urate-lowering therapy)", ["Pharmacogenomics", "Hypersensitivity", "Gout", "Renal dosing"], {
        "moa": [("Purine analog; it and its metabolite oxypurinol block xanthine oxidase → ↓ uric acid production.", "L04 S12-13; p. 695; SG U2-R9")],
        "ind": [("First-line chronic urate-lowering therapy for most patients with gout — started only after the flare resolves.", "L04 S9; S12; SG U2-R10")],
        "contra": [("Never start (or change) during an acute flare — it can prolong the flare.", "L04 S9; S13; SG U2-R10"),
                   ("HLA-B*5801-positive patients: don’t use (screen Han Chinese, Korean, and Thai patients).", "p. 696")],
        "ae": [("Severe hypersensitivity / cutaneous reactions (HLA-B*58:01); can precipitate flares when starting.", "L04 S12-13; p. 695"),
               ("Allopurinol hypersensitivity syndrome (SJS/TEN, fever, eosinophilia, hepatitis, renal failure) 2–4 weeks in — stop at the first rash; pruritic rash in 3%.", "p. 695; p. 696")],
        "ix": [("Reduce dose with azathioprine or mercaptopurine (textbook: cut azathioprine by 75%).", "L04 S13; p. 696"),
               ("Also inhibits metabolism of probenecid and oral anticoagulants; diuretics, amoxicillin, ampicillin raise hypersensitivity risk.", "p. 696")],
        "pt": [("HLA-B*5801 carriers have a sharply higher risk of severe hypersensitivity — screen before starting.", "L02 S35-36; SG U1-R12"),
               ("Reduce the dose in renal impairment (textbook: start ≤50 mg/d in CKD).", "L04 S13; p. 695")],
        "extra": [("Start low (100 mg/d) and titrate toward a serum urate target (<6 mg/dL); cover with colchicine or an NSAID for 3–6 months.", "L04 S13; p. 695"),
                  ("Don’t stop it if a flare occurs while already on it.", "p. 696"),
                  ("Suggested alternative when rasburicase is contraindicated (G6PD deficiency).", "p. 83")],
    }, unit=2),
    D("Abacavir", "Not covered in materials", ["Pharmacogenomics", "Hypersensitivity"], {
        "contra": [("HLA-B*57:01-positive patients (hypersensitivity).", "p. 83; p. 88")],
    }),
    D("Rasburicase", "Uricase (recombinant enzyme)", ["Pharmacogenomics", "Gout"], {
        "moa": [("Uricase converts uric acid to allantoin, which is soluble and excreted.", "L04 S15")],
        "ind": [("Uricases are reserved for refractory gout.", "L04 S15")],
        "contra": [("G6PD deficiency (hemolysis) — use an alternative such as allopurinol.", "L04 S15; p. 83")],
        "extra": [("-ase stem = enzyme (uricase).", "L04 S19")],
    }),
    D("Aspirin", "Salicylate NSAID (irreversible COX inhibitor)", ["Urine pH", "Saturable elimination", "Antiplatelet", "NSAID"], {
        "moa": [("Irreversibly acetylates platelet COX — the antiplatelet effect lasts 8–10 days (the platelet’s life).", "p. 675; p. 677")],
        "ind": [("Now used mainly as an antiplatelet (81–325 mg daily); low-dose aspirin also helps prevent preterm preeclampsia.", "p. 677")],
        "contra": [("Hemophilia (antiplatelet action).", "p. 677")],
        "ae": [("At antithrombotic doses: gastric upset and gastric/duodenal ulcers.", "p. 677")],
        "ix": [("Ibuprofen taken with aspirin blocks its irreversible platelet inhibition, limiting cardioprotection.", "p. 680"),
               ("Unlike acetaminophen, aspirin antagonizes uricosuric agents.", "p. 694")],
        "pt": [("Long-term low-dose aspirin in type 2 diabetes increases GI bleeding risk.", "p. 677")],
        "extra": [("Overdose: alkalinizing the urine traps ionized drug and speeds renal clearance (weak acid).", "L02 S14 (notes); p. 20"),
                  ("Hydrolyzed rapidly (serum half-life 15 minutes) to salicylate; capacity-limited (saturable) elimination.", "p. 677; p. 47")],
    }),
    D("Heparin", "Anticoagulant", ["Routes", "Reversal"], {
        "ix": [("Reversed by protamine, which binds it directly (chemical antagonism).", "p. 26")],
        "extra": [("Commonly given subcutaneously (slower, steady absorption).", "L01 S49")],
    }),
    D("Protamine", "Heparin reversal agent", ["Reversal", "Antagonism"], {
        "moa": [("Positively charged protein that binds negatively charged heparin — chemical antagonism, no receptor involved.", "p. 26")],
        "ind": [("Reversal of heparin.", "p. 26")],
    }),
    D("Insulin", "Not covered in materials", ["Routes"], {
        "extra": [("Commonly given subcutaneously (slower, steady absorption).", "L01 S49")],
    }),
    D("Theophylline", "Not covered in materials", ["PK math"], {
        "extra": [("Loading dose example: Vd 35 L × target 10 mg/L = 350 mg for a 70-kg adult.", "p. 52")],
    }),
    D("Phenoxybenzamine", "Irreversible α-adrenoceptor antagonist", ["Antagonism"], {
        "moa": [("Irreversible α blockade that lasts until new receptors are made.", "p. 25")],
        "ind": [("Hypertension of pheochromocytoma.", "p. 25")],
    }),
    D("Rifampin", "CYP inducer", ["CYP inducer"], {
        "ix": [("Induces CYP enzymes, speeding metabolism of substrates (levels fall).", "p. 63; p. 64")],
    }),
    D("St. John's wort", "Herbal product · CYP3A4 inducer", ["CYP inducer"], {
        "ix": [("Induces CYP3A4 — lowers levels of oral contraceptives, warfarin, cyclosporine, and others.", "p. 72")],
    }, aliases=["St John's wort", "St. John’s wort"]),
    D("Grapefruit juice", "CYP3A4 / P-glycoprotein inhibitor", ["CYP inhibitor"], {
        "ix": [("Inhibits gut-wall CYP3A4 and P-glycoprotein, raising absorption of some drugs (cyclosporine bioavailability by as much as 62%).", "p. 48; p. 64; p. 684")],
    }, aliases=["grapefruit"]),
    D("Ketoconazole", "CYP3A4 inhibitor", ["CYP inhibitor"], {
        "ix": [("CYP3A4 inhibitor — raises levels of CYP3A4 substrates (e.g., a narrow-TI substrate → toxicity).", "p. 64")],
    }),
    D("Ritonavir", "CYP3A4 inhibitor", ["CYP inhibitor"], {
        "ix": [("Potent CYP3A4 inhibitor (acutely).", "p. 64; p. 72")],
    }),
    D("N-acetylcysteine", "Antidote (glutathione precursor)", ["Antidote"], {
        "moa": [("Glutathione precursor: replenishes glutathione so NAPQI is detoxified.", "L03 S17; S19; SG U2-R3")],
        "ind": [("Acetaminophen overdose — a level above the Rumack-Matthew treatment line, or late/unknown-time ingestion with a significant dose.", "L03 S18; S18 (notes)")],
        "pt": [("Give early for best effect; protective when given within 8–16 hours.", "L03 S17; p. 66")],
    }, aliases=["NAC"]),
    D("Thalidomide", "Not covered in materials", ["Regulation"], {
        "extra": [("Caused about 10,000 birth defects; led to the Kefauver-Harris Amendments (1962), which required proof of efficacy.", "p. 16")],
    }),
    D("Isoniazid", "Not covered in materials", ["Pharmacogenomics"], {
        "pt": [("Slow NAT2 acetylators (~50% of people in the USA) are at higher toxicity risk.", "p. 70")],
    }),

    # ---------------------------------------------------------------- Unit 2 · L03: NSAIDs and other analgesics
    D("Ibuprofen", "Nonselective NSAID (propionic acid; COX-1 and COX-2)", ["NSAID", "OA"], {
        "moa": NSAID_MOA,
        "ind": [("Common first-line choice for mild-moderate pain.", "L03 S28"), *NSAID_IND,
                ("Indicated for OA, RA, and JRA; sold OTC as 200-mg tablets.", "p. 680")],
        "contra": [*NSAID_CONTRA, ("Relatively contraindicated with nasal polyps, angioedema, or bronchospastic reactivity to aspirin.", "p. 680")],
        "ae": [*NSAID_AE, ("Aseptic meningitis (particularly in SLE); rare agranulocytosis, aplastic anemia. Less fluid retention than indomethacin.", "p. 680")],
        "ix": [*NSAID_IX, ("Taken with aspirin, it blocks aspirin’s irreversible platelet inhibition (less cardioprotection).", "p. 680")],
        "pt": [*NSAID_PT, ("Switching a GI-ulcer patient from ibuprofen to celecoxib: lower GI risk, some increase in CV risk.", "L03 S32-33")],
        "extra": [("≤1600 mg/day is analgesic but not anti-inflammatory; 2400 mg/day equals 4 g aspirin. Half-life 2 h.", "p. 677; p. 680"),
                  ("-profen stem = propionic-acid NSAID.", "L03 S60")],
    }, aliases=["Advil", "Motrin"], unit=2),
    D("Naproxen", "Nonselective NSAID (propionic acid)", ["NSAID"], {
        "moa": NSAID_MOA,
        "ind": [*NSAID_IND, ("OA, RA, AS, pain, bursitis/tendonitis; also JIA, acute gout, and migraine.", "p. 680")],
        "contra": [*NSAID_CONTRA, ("Hepatic impairment.", "p. 680")],
        "ae": NSAID_AE,
        "ix": NSAID_IX,
        "pt": [*NSAID_PT, ("More OTC upper-GI bleeding than ibuprofen, but a more favorable cardiovascular profile.", "p. 680")],
        "extra": [("Longer half-life (12–17 h) → twice-daily dosing; the only NSAID sold as a single enantiomer; OTC 220-mg tablets.", "L03 S28; p. 677; p. 680"),
                  ("-profen-family (propionic-acid) NSAID.", "L03 S60")],
    }, aliases=["Aleve"], unit=2),
    D("Diclofenac", "Nonselective NSAID (acetic acid)", ["NSAID", "Topical", "OA"], {
        "moa": NSAID_MOA,
        "ind": [*NSAID_IND, ("OA, RA, and AS; the 1% topical gel is sold OTC for OA and muscular pain.", "p. 679")],
        "contra": NSAID_CONTRA,
        "ae": [*NSAID_AE, ("Raises serum aminotransferases more often than other NSAIDs.", "p. 679; p. 681")],
        "ix": [*NSAID_IX, ("Voriconazole (a CYP2C9 inhibitor) may increase diclofenac toxicity.", "p. 679")],
        "pt": [*NSAID_PT, ("Topical form = local relief with much lower systemic exposure — useful when systemic NSAID risk is a concern.", "L03 S28; S43")],
        "extra": [("Available oral and topical; also combined with misoprostol or omeprazole to reduce GI injury.", "L03 S28; p. 679"),
                  ("-fenac stem = acetic-acid NSAID.", "L03 S60")],
    }, aliases=["Voltaren"], unit=2),
    D("Indomethacin", "Nonselective NSAID (indole; potent)", ["NSAID"], {
        "moa": [*NSAID_MOA, ("Potent nonselective COX inhibitor that may also inhibit phospholipase A and C and reduce neutrophil migration.", "p. 680")],
        "ind": [*NSAID_IND, ("OA, RA, AS, bursitis/tendonitis, acute gouty arthritis; accelerates closure of patent ductus arteriosus.", "p. 680")],
        "contra": NSAID_CONTRA,
        "ae": [("More potent, with more GI/CNS adverse effects.", "L03 S28"), *NSAID_AE,
               ("Headache in 11.7%; can aggravate depression, epilepsy, and parkinsonism.", "p. 680")],
        "ix": NSAID_IX,
        "pt": [*NSAID_PT, ("Among the NSAIDs with the greatest toxicity in surveys.", "p. 681")],
    }, unit=2),
    D("Ketorolac", "Nonselective NSAID (used as an analgesic)", ["NSAID", "Short-term"], {
        "moa": NSAID_MOA,
        "ind": [("Short-term pain relief; an adjuvant with opioids and other analgesics.", "L03 S28; p. 694")],
        "contra": NSAID_CONTRA,
        "ae": [("Significant GI and renal risk.", "L03 S28"), *NSAID_AE, ("Renal toxicity is more common with chronic use.", "p. 694")],
        "ix": NSAID_IX,
        "pt": [("Short-term use only (no more than 5 days); halve all doses if over 65, under 50 kg, or with renal impairment.", "L03 S28; p. 694"), *NSAID_PT],
        "extra": [("Start IV, IM, or intranasal (not orally); max 120 mg/day. Half-life 5–6 h; about 90% renally excreted.", "p. 694")],
    }, unit=2),
    D("Celecoxib", "COX-2 selective NSAID (coxib)", ["NSAID", "COX-2", "CV risk"], {
        "moa": [("Selectively inhibits inducible COX-2 (the main source of inflammatory prostaglandins), largely sparing COX-1 in gastric mucosa and platelets.", "L03 S29-30"),
                ("About 10–20 times more selective for COX-2 than COX-1; no effect on platelet aggregation at usual doses.", "p. 677")],
        "ind": [("OA, RA, JRA, and AS; usual dose 100–200 mg bid.", "p. 677")],
        "contra": [*NSAID_CONTRA, ("CV risk rises with COX-2 selectivity — weigh carefully in cardiovascular disease.", "L03 S29")],
        "ae": [("Lower ulcer/bleeding risk than nonselective NSAIDs, but higher cardiovascular event risk; renal risk is similar.", "L03 S29-31; SG U2-R5")],
        "ix": [*NSAID_IX, ("A CYP2C9 substrate: occasionally interacts with warfarin and raises lithium and fluconazole levels.", "p. 679")],
        "pt": [("GI-ulcer history without CV disease: switching from ibuprofen lowers GI risk with some increase in CV risk — discuss it.", "L03 S32-33"),
               ("Safest for patients at high GI-bleeding risk (or a nonselective NSAID plus omeprazole or misoprostol).", "p. 681")],
        "extra": [("Why the CV risk: endothelial PGI2 falls without a matching drop in platelet TXA2.", "L03 S29-30"),
                  ("-coxib stem = selective COX-2 inhibitor.", "L03 S60")],
    }, aliases=["Celebrex"], unit=2),
    D("Meloxicam", "Oxicam NSAID (relatively COX-2 selective)", ["NSAID"], {
        "moa": [("Relatively COX-2 selective, particularly at 7.5 mg/day; thromboxane blockade doesn’t reduce platelet function in vivo.", "p. 679")],
        "ind": [("OA, RA, and JRA; 7.5–15 mg/day.", "p. 679")],
        "contra": NSAID_CONTRA,
        "ae": [("Fewer clinical GI symptoms than piroxicam, diclofenac, and naproxen; otherwise the usual NSAID effects.", "p. 679")],
        "ix": NSAID_IX,
        "extra": [("-oxicam stem = oxicam-class NSAID; half-life 20 h (once daily).", "L03 S60; p. 677")],
    }, unit=2),
    D("Tramadol", "Centrally acting analgesic (weak μ-opioid + serotonin/norepinephrine reuptake)", ["Analgesic"], {
        "moa": [("Weak affinity for μ-opioid receptors plus serotonin and norepinephrine reuptake inhibition.", "p. 694; p. 695")],
        "ind": [("Acute and chronic pain (no significant anti-inflammatory effect).", "p. 695")],
        "ae": [("Nausea, vomiting, vertigo, dizziness, sedation, dry mouth, constipation, sweating; serotonin syndrome, seizures, angioedema.", "p. 695")],
        "ix": [("Exaggerates anticoagulant effect.", "p. 695")],
        "pt": [("Fewer side effects and lower addiction potential than classic opioids.", "p. 695")],
        "extra": [("Up to 300 mg/day; elimination half-life about 6 hours.", "p. 695")],
    }, unit=2),

    # ---------------------------------------------------------------- Unit 2 · L03: DMARDs
    D("Methotrexate", "Conventional synthetic DMARD (antifolate)", ["DMARD", "Weekly dosing", "Teratogen"], {
        "moa": [("Inhibits dihydrofolate reductase (DHF → THF), reducing folate-dependent purine/thymidylate synthesis and immune-cell proliferation.", "L03 S49-50; SG U2-M"),
                ("At low RA doses likely anti-inflammatory via adenosine release, not cytotoxicity (textbook: mainly AICAR transformylase; DHFR effect minor).", "L03 S50; p. 688")],
        "ind": [("The anchor drug for most rheumatoid arthritis regimens.", "L03 S47"),
                ("Also psoriasis, psoriatic arthritis, JIA; slows new erosions in RA.", "p. 688")],
        "contra": [("Pregnancy (teratogenic).", "L03 S49; p. 689")],
        "ae": [("Hepatotoxicity, bone marrow suppression, pulmonary toxicity.", "L03 S49"),
               ("Most common: nausea and stomatitis; also leukopenia, anemia, GI ulceration, alopecia, dose-related liver enzyme rises.", "p. 689")],
        "ix": [("Hydroxychloroquine can reduce methotrexate clearance.", "p. 688")],
        "pt": [("Dosed WEEKLY, never daily — daily dosing has caused fatal toxicity.", "L03 S49-50; SG U2-R7"),
               ("Folic acid is co-prescribed to reduce liver, marrow, lung, and GI toxicity (may cut efficacy by 10–18%).", "L03 S49-50; SG U2-R7; p. 689"), *DMARD_PT],
        "extra": [("Starts at 7.5 mg weekly, rising to 15–25 mg weekly.", "p. 688")],
    }, aliases=["MTX"], unit=2),
    D("Hydroxychloroquine", "Conventional synthetic DMARD (antimalarial)", ["DMARD"], {
        "moa": [("Alters lysosomal and TLR signaling (less antigen signaling).", "L03 S48"),
                ("Suppresses T-lymphocyte responses and leukocyte chemotaxis; interferes with type 1 IFN.", "p. 684")],
        "ind": [("Milder RA; relatively favorable safety profile.", "L03 S47"),
                ("Also SLE (decreases mortality), discoid lupus, JIA, Sjögren syndrome.", "p. 684")],
        "ae": [("Retinopathy; dyspepsia, nausea, rashes, myopathy, cardiomyopathy, conduction defects, cytopenias.", "p. 684")],
        "ix": [("Can reduce methotrexate clearance.", "p. 688")],
        "pt": [("Relatively safe in pregnancy; baseline eye exam, then annual screening after 5 years.", "p. 684"), *DMARD_PT],
        "extra": [("Takes 3–6 months for a clinical response.", "p. 684")],
    }, aliases=["HCQ", "Plaquenil"], unit=2),
    D("Sulfasalazine", "Conventional synthetic DMARD", ["DMARD"], {
        "moa": [("Reduces cytokine and prostaglandin production.", "L03 S48"),
                ("Split into sulfapyridine (likely active in RA) and 5-aminosalicylic acid.", "p. 690")],
        "ind": [("RA, often in combination regimens.", "L03 S47"), ("Also ulcerative colitis; reduces radiologic progression in RA.", "p. 690")],
        "ae": [("About 30% stop it for toxicity: nausea, vomiting, headache, rash; toxic epidermal necrolysis; neutropenia; hemolytic anemia.", "p. 690")],
        "pt": [("Slow acetylators have more toxicity; reversible male infertility; relatively safe in pregnancy.", "p. 690"), *DMARD_PT],
    }, unit=2),
    D("Leflunomide", "Conventional synthetic DMARD (pyrimidine synthesis inhibitor)", ["DMARD"], {
        "moa": [("Inhibits DHODH, blocking pyrimidine synthesis → slower T-cell growth.", "L03 S47-48; p. 687")],
        "ind": [("RA when methotrexate is not tolerated; equal to methotrexate in efficacy.", "L03 S47; p. 687")],
        "ae": [("Diarrhea in 25%, liver test abnormalities, mild alopecia, weight gain, raised blood pressure.", "p. 688")],
        "pt": DMARD_PT,
        "extra": [("Half-life about 19 days; cholestyramine shortens it to about 1 day.", "p. 687")],
    }, unit=2),
    D("Adalimumab", "Biologic DMARD · TNF inhibitor (fully human antibody)", ["Biologic", "TNF", "Infection risk"], {
        "moa": [("Binds soluble and membrane TNF-α, preventing TNF receptor activation.", "L03 S51-52; SG U2-R8")],
        "ind": [("The first-line biologic for RA.", "L03 S52"),
                ("Also AS, PsA, JIA, uveitis, hidradenitis suppurativa, plaque psoriasis, Crohn disease, ulcerative colitis.", "p. 690")],
        "contra": [("Don’t combine biologics (abatacept with a TNF inhibitor raises serious infections).", "p. 682")],
        "ae": [("Watch for reactivation of latent TB.", "L03 S52"), *TNF_AE],
        "ix": [("Methotrexate inhibits adalimumab clearance.", "p. 690")],
        "pt": DMARD_PT,
        "extra": [("-umab stem = fully human antibody; usual RA dose 40 mg every other week.", "L03 S60; p. 690")],
    }, aliases=["Humira"], unit=2),
    D("Etanercept", "Biologic DMARD · TNF inhibitor (receptor fusion protein)", ["Biologic", "TNF"], {
        "moa": [("Receptor fusion protein that neutralizes soluble and membrane TNF-α.", "L03 S51-52; SG U2-R8; p. 691")],
        "ind": [("RA (also as monotherapy), juvenile arthritis, psoriasis, PsA, AS.", "p. 692")],
        "ae": [*TNF_AE, ("Injection-site reactions.", "p. 692")],
        "pt": [("Latent TB activation is lower than with other TNF blockers — still screen everyone.", "p. 692"), *DMARD_PT],
        "extra": [("-cept stem = receptor fusion protein; usually 50 mg weekly in RA.", "L03 S60; p. 692")],
    }, aliases=["Enbrel"], unit=2),
    D("Infliximab", "Biologic DMARD · TNF inhibitor (chimeric antibody)", ["Biologic", "TNF"], {
        "moa": [("Chimeric antibody that binds TNF-α, preventing TNF receptor activation.", "L03 S51-52; SG U2-R8; p. 692")],
        "ind": [("RA (with methotrexate), AS, PsA, Crohn disease, ulcerative colitis, psoriasis.", "p. 692")],
        "ae": [*TNF_AE, ("Human antichimeric antibodies in up to 62% of patients.", "p. 692")],
        "ix": [("Methotrexate markedly decreases antibodies against infliximab.", "p. 692")],
        "pt": DMARD_PT,
        "extra": [("-ximab stem = chimeric antibody. IV infusion at weeks 0, 2, and 6, then every 8 weeks.", "L03 S60; p. 692")],
    }, aliases=["Remicade"], unit=2),
    D("Tocilizumab", "Biologic DMARD · IL-6 receptor inhibitor (humanized antibody)", ["Biologic", "IL-6"], {
        "moa": [("Blocks membrane and soluble IL-6 receptors, reducing inflammatory signaling.", "L03 S51-52; SG U2-R8")],
        "ind": [("RA — works as monotherapy.", "L03 S52"), ("Also giant cell arteritis, systemic sclerosis–associated ILD, systemic JIA.", "p. 692")],
        "ae": [("Can raise lipids and liver enzymes.", "L03 S52"),
               ("Upper respiratory infections, headache, hypertension; serious infections; GI perforation with diverticulitis.", "p. 692; p. 693")],
        "ix": [("Stimulates CYP450 — cyclosporine or warfarin doses may need adjusting.", "p. 692")],
        "pt": [("Stop if ALT/AST reach 5 times the upper limit of normal, or with severe neutropenia or thrombocytopenia.", "p. 693"), *DMARD_PT],
        "extra": [("-zumab stem = humanized antibody.", "L03 S60")],
    }, aliases=["Actemra"], unit=2),
    D("Rituximab", "Biologic DMARD · B-cell (anti-CD20) therapy", ["Biologic", "B cell"], {
        "moa": [("Anti-CD20 antibody that depletes or modulates B cells for months.", "L03 S51-52; SG U2-R8")],
        "ind": [("RA after TNF-inhibitor failure (with methotrexate); also granulomatosis with polyangiitis.", "L03 S52; p. 689")],
        "ae": [("Rash with the first dose in about 30%; urticaria, anaphylaxis, rare fatal Stevens-Johnson syndrome; serious infections; hepatitis B reactivation.", "p. 689")],
        "pt": [("Check hepatitis B before starting.", "L03 S52"),
               ("Pretreat with acetaminophen, an antihistamine, and an H2 blocker to reduce infusion reactions; not linked to TB activation.", "p. 689"), *DMARD_PT],
        "extra": [("-mab stem = monoclonal antibody (chimeric). RA course: two 1000 mg IV infusions 2 weeks apart.", "L03 S60; p. 689")],
    }, aliases=["Rituxan"], unit=2),
    D("Abatacept", "Biologic DMARD · T-cell costimulation modulator (CTLA-4-Ig)", ["Biologic", "T cell"], {
        "moa": [("CTLA-4-Ig: binds CD80/86 and blocks CD28 costimulation — the second signal T cells need to activate. Acts earliest in the cascade.", "L03 S51-52; S54-55; SG U2-M")],
        "ind": [("RA, PsA, and polyarticular JIA (alone or with methotrexate).", "p. 682")],
        "contra": [("Concomitant TNF inhibitors or other biologics (more serious infections).", "p. 682")],
        "ae": [("Infections (upper respiratory, urinary), headache, nasopharyngitis, nausea; generally a lower infection signal than other biologics.", "L03 S52; p. 682")],
        "pt": [("Avoid live vaccines for up to 3 months after stopping.", "p. 682"), *DMARD_PT],
        "extra": [("-cept stem = receptor fusion protein.", "L03 S60")],
    }, aliases=["Orencia"], unit=2),
    D("Tofacitinib", "Targeted synthetic DMARD · JAK inhibitor", ["JAK", "Boxed warning"], {
        "moa": [("Oral small molecule that inhibits JAK 1, 2, and 3, interrupting JAK-STAT cytokine signaling.", "p. 687")],
        "ind": [("RA and PsA (5 mg twice daily), alone or with methotrexate.", "p. 687")],
        "ae": [("Boxed warning (all JAK inhibitors): VTE (DVT, PE), major cardiovascular events, and cancer; more herpes zoster; ↑ LDL.", "p. 686")],
        "ix": [("Reduce to 5 mg once daily with CYP enzyme inhibitors.", "p. 687")],
        "pt": [("Dose-reduce in moderate hepatic or renal impairment; avoid in severe hepatic disease; caution with diverticulitis.", "p. 687"), *DMARD_PT],
        "extra": [("-tinib stem = kinase inhibitor (here, JAK).", "L03 S60")],
    }, aliases=["Xeljanz"], unit=2),
    # ---------------------------------------------------------------- Unit 2 Session 2 (L04): gout
    D("Colchicine", "Antigout anti-inflammatory (plant-derived alkaloid)", ["Gout", "Narrow TI", "CYP interactions", "Renal dosing"], {
        "moa": [("Binds tubulin → blocks microtubule polymerization in neutrophils → ↓ neutrophil migration and NLRP3 activation → less crystal inflammation. Does not lower uric acid.", "L04 S10-11; S71; SG U2-M")],
        "ind": [("Acute gout flare — best started within 24 hours of onset.", "L04 S9-11"),
                ("Prophylaxis (with an NSAID as the alternative) for 3–6 months when starting urate-lowering therapy.", "L04 S13"),
                ("Textbook regimen: 1.2 mg, then 0.6 mg an hour later; prophylaxis 0.6 mg once or twice daily. Also pericarditis, familial Mediterranean fever, pseudogout.", "p. 696")],
        "contra": [("Dose-reduce in renal or hepatic impairment; not removed by dialysis.", "L04 S11; p. 696")],
        "ae": [("Narrow therapeutic window: diarrhea (GI) is common and dose-limiting.", "L04 S10-11"),
               ("Also marrow depression, myopathy, rhabdomyolysis, neuritis, hair loss.", "p. 696")],
        "ix": [("CYP3A4 and P-gp inhibitors (clarithromycin, cyclosporine, strong CYP3A4 inhibitors) → toxicity.", "L04 S11")],
        "pt": [("CKD patient with a flare: colchicine needs renal dose adjustment; a short corticosteroid course is often preferred.", "SG U2-S")],
        "extra": [("No shared stem — plant-derived alkaloid (autumn crocus).", "L04 S19; p. 696")],
    }, unit=2),
    D("Febuxostat", "Xanthine oxidase inhibitor (nonpurine)", ["Gout", "Boxed warning"], {
        "moa": [("Selective nonpurine xanthine oxidase inhibitor (different structure from allopurinol) → ↓ uric acid production.", "L04 S12-13; p. 697; SG U2-R9")],
        "ind": [("Alternative urate-lowering therapy when allopurinol is not tolerated or contraindicated.", "L04 S12"),
                ("40 or 80 mg daily, target uric acid <6.0 mg/dL; appears safe in moderate CKD.", "p. 697")],
        "contra": [("Not during an acute flare — start after it resolves.", "L04 S9; S13")],
        "ae": [("Boxed warning: cardiovascular death.", "L04 S13"),
               ("Liver function abnormalities, diarrhea, headache, nausea; dose-dependent rash.", "p. 697")],
        "pt": [("Textbook: early MACE concerns were not borne out — answer course exams with the slide’s boxed warning.", "p. 697; L04 S13")],
        "extra": [("-ostat stem = xanthine oxidase inhibitor.", "L04 S19"), ("Start prophylaxis (colchicine or NSAID) with it.", "L04 S13; p. 697")],
    }, unit=2),
    D("Probenecid", "Uricosuric", ["Gout", "Renal"], {
        "moa": [("Inhibits renal tubular reabsorption of uric acid (URAT1) → ↑ excretion.", "L04 S14-15; S71; SG U2-R9")],
        "ind": [("Second-line oral urate-lowering therapy; textbook: underexcreters, or when xanthine oxidase inhibitors are contraindicated, alone or combined.", "L04 S14-15; p. 698")],
        "contra": [("History of uric acid kidney stones or significant renal impairment.", "L04 S14-15"),
                   ("Not for patients who already excrete large amounts of uric acid.", "p. 698")],
        "ae": [("GI irritation, rash, nephrotic syndrome; rarely aplastic anemia.", "p. 698")],
        "ix": [("Reduces renal secretion of other weak acids such as penicillin.", "p. 698")],
        "pt": [("Needs adequate hydration; textbook: keep urine pH above 6.0 early on; start 2–3 weeks after an attack.", "L04 S15; p. 698")],
        "extra": [("A uricosuric, not a xanthine oxidase inhibitor.", "L04 S14; S71")],
    }, unit=2),
    D("Pegloticase", "Uricase (recombinant, PEGylated)", ["Gout", "Infusion", "Refractory"], {
        "moa": [("Recombinant uricase converts uric acid to allantoin, which is soluble and excreted.", "L04 S14-15")],
        "ind": [("Severe, refractory gout not controlled by other agents.", "L04 S14-15"),
                ("8 mg IV every 2 weeks; not for asymptomatic hyperuricemia.", "p. 698")],
        "contra": [("G6PD deficiency (hemolysis risk).", "L04 S15; p. 698")],
        "ae": [("Infusion reactions are common; anti-drug antibodies can reduce response.", "L04 S15"),
               ("Flares in the first 3–6 months; premedicate with a corticosteroid and antihistamine.", "p. 698")],
        "ix": [("Given with methotrexate: fewer allergic reactions and better efficacy.", "p. 698")],
        "pt": [("Reserved for refractory cases: cost, infusion-reaction risk, specialty administration.", "L04 S14")],
        "extra": [("-ase stem = enzyme (uricase).", "L04 S19")],
    }, unit=2),
    D("Prednisone", "Corticosteroid (glucocorticoid)", ["Gout", "Bone loss"], {
        "moa": [("Corticosteroids block phospholipase A₂ upstream; in gout they reduce neutrophil migration, prostaglandins, and IL-1β.", "L03 S9; p. 698")],
        "ind": [("Acute gout flare (oral or intra-articular) — a good alternative when NSAIDs or colchicine are contraindicated, including CKD: 30–50 mg/d for 1–2 days, tapered over 7–10 days.", "L04 S9; SG U2-S; p. 698")],
        "contra": [("Rule out joint infection before an intra-articular injection.", "p. 698")],
        "ae": [("Chronic use causes osteoporosis: ↑ osteoclast resorption, ↓ osteoblast formation.", "L04 S46; S71"),
               ("Short courses: mood changes, fluid retention, ↑ appetite, blood pressure, and glucose.", "p. 698")],
        "ix": [("With NSAIDs → ↑ GI ulcer risk.", "L03 S36")],
        "pt": [("Chronic glucocorticoid use is a key osteoporosis risk factor — consider bone protection.", "L04 S46; S59")],
        "extra": [("-sone / -olone stems mark corticosteroids (prednisone, methylprednisolone).", "L04 S19")],
    }, aliases=["Methylprednisolone"], unit=2),
    # ---------------------------------------------------------------- L04: skeletal muscle relaxants
    D("Baclofen", "Centrally acting spasmolytic · GABA-B agonist", ["Muscle relaxant", "Central", "Withdrawal", "Renal dosing"], {
        "moa": [("GABA-B receptor agonist in the spinal cord → K⁺ channels open, Ca²⁺ channels close (presynaptic inhibition) → less excitatory release → less spasticity.", "L04 S27-28; SG U2-M")],
        "ind": [("Spasticity, particularly from spinal cord injury or multiple sclerosis; intrathecal option for severe spasticity.", "L04 S27-28")],
        "contra": [("Caution in pregnancy (animal data) and epilepsy (more seizures).", "p. 512")],
        "ae": [("CNS depression: sedation, weakness; high doses: respiratory depression, coma.", "L04 S27-28; p. 512")],
        "ix": [("Additive sedation with other CNS depressants.", "L04 S27")],
        "pt": [("Abrupt discontinuation (especially intrathecal) → seizures, hyperthermia, rebound spasticity — taper slowly.", "L04 S27-28; p. 512"),
               ("Renal dose adjustment.", "L04 S28")],
        "extra": [("No shared stem (GABA analog). Textbook: 15 mg twice daily up to 100 mg daily; half-life 3–4 h; less sedating than diazepam.", "L04 S38; p. 512")],
    }, unit=2),
    D("Tizanidine", "Centrally acting spasmolytic · α2-adrenergic agonist", ["Muscle relaxant", "Central", "CYP interactions"], {
        "moa": [("Central α2 agonist → ↓ presynaptic release of excitatory amino acids → lower motor neuron activity → reduced tone.", "L04 S29-30")],
        "ind": [("Spasticity / increased muscle tone; textbook: also chronic migraine.", "L04 S23; S29; p. 512")],
        "contra": [("With ciprofloxacin or fluvoxamine (strong CYP1A2 inhibitors).", "L04 S30")],
        "ae": [("Sedation, hypotension (16–33%), bradycardia, dry mouth, hepatotoxicity.", "L04 S29-30; p. 512")],
        "ix": [("CYP1A2 inhibitors strongly raise levels; additive effect with antihypertensives.", "L04 S30")],
        "pt": [("Monitor LFTs with regular use; adjust for hepatic or renal impairment; avoid abrupt withdrawal (rebound hypertension, tachycardia).", "L04 S29-30; p. 512")],
        "extra": [("-idine (imidazoline) stem = central alpha-2 agonist, a clonidine congener with far less BP effect.", "L04 S38; p. 512")],
    }, unit=2),
    D("Cyclobenzaprine", "Centrally acting antispasmodic (tricyclic-like)", ["Muscle relaxant", "Central", "Anticholinergic", "Beers"], {
        "moa": [("Acts in the brainstem: antagonizes 5-HT2 and descending serotonergic/noradrenergic pathways → ↓ tonic somatic motor activity.", "L04 S31-32")],
        "ind": [("Short-term (2–3 weeks) treatment of acute, localized muscle spasm.", "L04 S31-32"),
                ("Ineffective for spasm from cerebral palsy or spinal cord injury.", "p. 513")],
        "contra": [("MAOIs contraindicated; caution in older adults (Beers list).", "L04 S31-32")],
        "ae": [("Prominent sedation (dose at night); anticholinergic: dry mouth, blurred vision, urinary retention, confusion; textbook adds visual hallucinations.", "L04 S31-32; p. 513")],
        "ix": [("Serotonin syndrome risk with SSRIs, SNRIs, tramadol.", "L04 S32")],
        "pt": [("Older adults: anticholinergic burden — consider alternatives.", "L04 S31-32")],
        "extra": [("Structurally related to tricyclic antidepressants (cyclo- clue). Textbook dose 20–40 mg/d.", "L04 S31; S38; p. 513")],
    }, aliases=["Flexeril"], unit=2),
    D("Carisoprodol", "Centrally acting relaxant (Schedule IV)", ["Muscle relaxant", "Central", "Controlled"], {
        "moa": [("Centrally acting; metabolized to meprobamate (a sedative).", "L04 S33; p. 511")],
        "ind": [("An “other” centrally acting option for muscle spasm.", "L04 S23")],
        "ae": [("Dependence and misuse; withdrawal after long use (anxiety, tremor, insomnia, hallucinations).", "L04 S33; p. 511")],
        "pt": [("Schedule IV controlled substance.", "L04 S33")],
    }, unit=2),
    D("Methocarbamol", "Centrally acting relaxant", ["Muscle relaxant", "Central"], {
        "ind": [("An “other” centrally acting option for acute muscle spasm.", "L04 S23; p. 513")],
        "pt": [("Generally less sedating than cyclobenzaprine.", "L04 S33")],
    }, unit=2),
    D("Metaxalone", "Centrally acting relaxant", ["Muscle relaxant", "Central"], {
        "ind": [("An “other” centrally acting option for acute muscle spasm.", "L04 S23; p. 513")],
        "pt": [("Relatively favorable sedation profile among this group.", "L04 S33")],
    }, unit=2),
    D("Chlorzoxazone", "Centrally acting relaxant", ["Muscle relaxant", "Central", "Hepatotoxic"], {
        "ind": [("An “other” centrally acting option for acute muscle spasm.", "L04 S23; p. 513")],
        "ae": [("Rare but notable hepatotoxicity.", "L04 S33")],
    }, unit=2),
    D("Diazepam", "Benzodiazepine (GABA-A)", ["Muscle relaxant", "Central"], {
        "moa": [("Facilitates GABA at GABA-A synapses; reduces spasticity partly in the spinal cord.", "L04 S38; p. 511")],
        "ind": [("Spasm of almost any origin; textbook: 4 mg/d up to 60 mg/d.", "p. 511")],
        "ae": [("Sedation at the doses required to reduce muscle tone.", "p. 511")],
        "extra": [("-azepam stem = benzodiazepine.", "L04 S38")],
    }, aliases=["Valium"], unit=2),
    D("Dantrolene", "Peripherally acting relaxant · RyR1 blocker", ["Muscle relaxant", "Peripheral", "Emergency", "Hepatotoxic"], {
        "moa": [("Blocks RyR1 in skeletal muscle → ↓ Ca²⁺ release from the sarcoplasmic reticulum → relaxation. Acts on the muscle fiber, not the CNS; cardiac/smooth muscle (RyR2) spared.", "L04 S34-35; p. 513; SG U2-R11; SG U2-M")],
        "ind": [("Malignant hyperthermia (triggered by volatile anesthetics and succinylcholine) — IV, life-saving; textbook: 1 mg/kg IV, repeated.", "L04 S34-35; p. 513; SG U2-R11"),
                ("Chronic spasticity when central agents are not appropriate; neuroleptic malignant syndrome.", "L04 S34-35")],
        "ae": [("Hepatotoxicity; generalized weakness; sedation.", "L04 S35; p. 513")],
        "pt": [("The only relaxant in the peripheral (muscle) bucket — useful when a central mechanism isn’t wanted.", "L04 S23-24")],
        "extra": [("-trolene (hydantoin derivative) clue. Oral: about one-third absorbed; half-life about 8 h.", "L04 S38; p. 513")],
    }, unit=2),
    D("Botulinum toxin", "Neuromuscular junction blocker (local injection)", ["Muscle relaxant", "Peripheral", "Boxed warning"], {
        "moa": [("Blocks presynaptic acetylcholine release at the neuromuscular junction (cleaves SNAP-25 or synaptobrevin).", "L04 S33; p. 513")],
        "ind": [("Focal spasticity or dystonia; textbook also cerebral palsy, overactive bladder, chronic migraine, wrinkles.", "L04 S33; p. 513")],
        "ae": [("Black box warning: distant spread of toxin (greatest in children treated for spasticity); weakness, falls.", "p. 513")],
        "pt": [("Local and temporary — repeat injections, no more often than every 3 months.", "L04 S33; p. 513")],
        "extra": [("-toxin clue.", "L04 S38")],
    }, aliases=["Botox", "onabotulinumtoxinA"], unit=2),
    D("Succinylcholine", "Depolarizing neuromuscular blocker", ["Anesthesia", "MH trigger"], {
        "moa": [("Nicotinic agonist that holds the end plate depolarized (phase I), then desensitizes it (phase II).", "L04 S38; p. 503-504")],
        "ind": [("Rapid intubation; block lasts under 10 minutes (plasma cholinesterase).", "p. 502; p. 507")],
        "contra": [("Burns, denervation, major trauma: hyperkalemia → cardiac arrest.", "p. 508")],
        "ae": [("Triggers malignant hyperthermia with volatile anesthetics (treat with dantrolene); arrhythmias, myalgias, ↑ intraocular and intragastric pressure.", "L04 S35; p. 508")],
        "ix": [("Cholinesterase inhibitors augment (not reverse) a phase I block.", "p. 504")],
        "pt": [("Plasma cholinesterase variants (dibucaine number) prolong the block.", "p. 503")],
        "extra": [("-choline clue: the only depolarizing blocker.", "L04 S38")],
    }, unit=2),
    D("Vecuronium", "Nondepolarizing neuromuscular blocker (steroid)", ["Anesthesia"], {
        "moa": [("Competes with acetylcholine at the nicotinic end-plate receptor.", "L04 S38; p. 503")],
        "ind": [("Muscle relaxation for surgery, intubation, and ventilation.", "p. 510")],
        "ix": [("Reversed by neostigmine or sugammadex; volatile anesthetics and aminoglycosides enhance the block.", "p. 508; p. 509")],
        "pt": [("Liver-dependent elimination — prolonged in liver impairment; minimal cardiovascular effects.", "p. 502; p. 507")],
        "extra": [("-curonium clue = nondepolarizing blocker.", "L04 S38")],
    }, unit=2),
    D("Cisatracurium", "Nondepolarizing neuromuscular blocker (isoquinoline)", ["Anesthesia"], {
        "moa": [("Competes with acetylcholine at the nicotinic end-plate receptor.", "L04 S38; p. 503")],
        "ind": [("Muscle relaxation for surgery and the ICU; has virtually replaced atracurium.", "p. 502")],
        "pt": [("Mostly spontaneous (Hofmann) breakdown — not dependent on kidney or liver; little histamine release.", "p. 502; p. 514")],
        "extra": [("-curium clue = nondepolarizing blocker; atracurium is the older isomer mix (more histamine, laudanosine).", "L04 S38; p. 502")],
    }, aliases=["Atracurium"], unit=2),
    # ---------------------------------------------------------------- L04: bone
    *[D(_n, "Bisphosphonate (antiresorptive)", ["Bone", "Osteoporosis", "Renal dosing"] + _tags, {
        "moa": [("Binds hydroxyapatite; taken up by osteoclasts; nitrogen-containing agents inhibit FPP synthase → loss of GTPase prenylation → osteoclast apoptosis.", "L04 S47-48; p. 820")],
        "ind": [("First-line for most patients with osteoporosis.", "L04 S47"), _ind],
        "contra": [("Severe renal impairment (CrCl below 30–35 mL/min).", "L04 S48")] + _contra,
        "ae": [("Esophageal irritation, hypocalcemia, osteonecrosis of the jaw (rare), atypical femoral fractures (rare, long-term).", "L04 S48; S52")] + _ae,
        "ix": [("Food, calcium, coffee, and antacids reduce absorption.", "L04 S53")] if _oral else [],
        "pt": [("Replete calcium and vitamin D first; consider a drug holiday after 3–5 years of oral therapy (textbook: reassess at 5 years, 3 for zoledronate).", "L04 S48; S53; p. 820")] + _pt,
        "extra": [("-dronate stem = bisphosphonate; long skeletal half-life — effect persists after stopping.", "L04 S48; S62")],
    }, aliases=_al, unit=2) for _n, _tags, _ind, _contra, _ae, _oral, _pt, _al in [
        ("Alendronate", ["Oral"], ("Oral, typically weekly (textbook: 70 mg/week or 10 mg/d).", "L04 S47; p. 818"),
         [("Esophageal stricture, achalasia, or inability to sit upright.", "L04 S53")], [], True,
         [("Full glass of water, first thing in the morning, fasting; remain upright 30 minutes.", "L04 S52-53; SG U2-R13")], ["Fosamax"]),
        ("Risedronate", ["Oral"], ("Oral, typically weekly (textbook: 35 mg/week or 5 mg/d).", "L04 S47; p. 818"),
         [("Esophageal stricture, achalasia, or inability to sit upright.", "L04 S53")], [], True,
         [("Full glass of water, first thing in the morning, fasting; remain upright 30 minutes.", "L04 S52-53; SG U2-R13")], []),
        ("Ibandronate", ["Oral"], ("Oral, monthly (textbook: 150 mg/month; also IV every 3 months).", "L04 S47; p. 818; p. 827"),
         [("Esophageal stricture, achalasia, or inability to sit upright.", "L04 S53")], [], True,
         [("Full glass of water, first thing in the morning, fasting; remain upright 30 minutes.", "L04 S52-53; SG U2-R13")], []),
        ("Zoledronic acid", ["IV"], ("IV, as infrequently as once yearly (textbook: 5 mg annually; 4 mg for hypercalcemia of malignancy).", "L04 S47; S49; p. 818; p. 822"),
         [], [("Acute-phase (flu-like) reaction after the first infusion — mitigate with acetaminophen.", "L04 S53; p. 820")], False,
         [("Yearly IV dosing helps adherence and avoids esophageal irritation.", "L04 S49; S59")], ["Zoledronate"]),
    ]],
    D("Denosumab", "RANKL inhibitor (monoclonal antibody) · antiresorptive", ["Bone", "Osteoporosis", "Biologic"], {
        "moa": [("Human monoclonal antibody against RANKL (mimics OPG) → blocks osteoclast formation and activity.", "L04 S41; S54-55; p. 820; SG U2-M")],
        "ind": [("Osteoporosis (60 mg SC every 6 months); also bone loss from some cancer therapies.", "L04 S54; p. 819; p. 820")],
        "contra": [("Correct hypocalcemia first; can be used in advanced renal disease (not renally cleared) with calcium monitoring.", "p. 820")],
        "ae": [("Stopping causes rebound vertebral fractures — transition to a bisphosphonate.", "L04 S55"),
               ("Transient hypocalcemia, possible infection risk, osteonecrosis of the jaw and atypical fractures comparable to bisphosphonates.", "p. 820")],
        "pt": [("Never just stop — plan the handoff to a bisphosphonate.", "L04 S55")],
        "extra": [("-sumab (-mab) clue: monoclonal antibody targeting bone.", "L04 S62")],
    }, aliases=["Prolia"], unit=2),
    D("Teriparatide", "PTH analog (PTH 1-34) · anabolic", ["Bone", "Osteoporosis", "Anabolic"], {
        "moa": [("Intermittent PTH analog → stimulates osteoblasts and new bone formation (continuous PTH would raise resorption).", "L04 S41; S54-55; p. 815; SG U2-M")],
        "ind": [("Osteoporosis, especially higher fracture risk where an anabolic agent goes first.", "L04 S54; S59")],
        "pt": [("Limited to 2 years lifetime, then follow with an antiresorptive.", "L04 S55; p. 827")],
        "extra": [("Daily SC injection (textbook: 20 mcg). -tide (peptide) clue.", "L04 S55; S62; p. 827")],
    }, unit=2),
    D("Abaloparatide", "PTHrP analog · anabolic", ["Bone", "Osteoporosis", "Anabolic"], {
        "moa": [("PTH-analog “anabolic” agent → stimulates osteoblasts and bone formation.", "L04 S54-55; p. 815")],
        "ind": [("Osteoporosis, higher fracture risk.", "L04 S54; S59")],
        "pt": [("Textbook: 80 mcg SC daily for 2 years, then an antiresorptive.", "p. 827")],
        "extra": [("-tide clue.", "L04 S62")],
    }, unit=2),
    D("Romosozumab", "Sclerostin antibody · anabolic + antiresorptive", ["Bone", "Osteoporosis", "Anabolic", "Boxed warning"], {
        "moa": [("Monoclonal antibody against sclerostin (which inhibits Wnt in osteoblasts) → builds bone and limits resorption.", "L04 S41; S54-55")],
        "ind": [("Osteoporosis with high fracture risk; textbook: 210 mg SC monthly for one year, then an antiresorptive.", "L04 S54; p. 819; p. 827")],
        "contra": [("Textbook: MI or stroke within the past year.", "p. 820")],
        "ae": [("Boxed warning: MI, stroke, and cardiovascular death.", "L04 S55")],
        "extra": [("-sumab clue: monoclonal antibody targeting bone (sclerostin).", "L04 S62")],
    }, unit=2),
    D("Raloxifene", "Selective estrogen receptor modulator (SERM)", ["Bone", "Osteoporosis", "VTE"], {
        "moa": [("Estrogen-like effect on bone → antiresorptive.", "L04 S54-55")],
        "ind": [("Osteoporosis; also reduces breast cancer risk.", "L04 S54-55"),
                ("Protects against spine but not hip fractures.", "p. 827")],
        "contra": [("History of venous thromboembolism (raises VTE risk).", "L04 S55; p. 827")],
        "ae": [("VTE; hot flashes (does not prevent them).", "L04 S55; p. 827")],
        "extra": [("-fene clue = SERM.", "L04 S62")],
    }, unit=2),
    D("Calcitonin", "Hormone · antiresorptive", ["Bone", "Osteoporosis", "Hypercalcemia"], {
        "moa": [("Lowers serum calcium and opposes PTH; inhibits osteoclast resorption.", "L04 S42-43; S55; p. 818")],
        "ind": [("Osteoporosis (weaker — spine fractures only), Paget disease, adjunct for hypercalcemia (acts in 4–6 hours).", "p. 818; p. 822; p. 828")],
        "pt": [("Salmon calcitonin lasts longer (40–50 min half-life); nasal or parenteral.", "p. 817; p. 822")],
        "extra": [("No shared stem (hormone).", "L04 S62")],
    }, unit=2),
]

# where each drug-class label comes from
CLASS_SOURCES = {"Albuterol": "L01 S26", "Warfarin": "p. 72", "Propranolol": "p. 25; p. 41", "Metoprolol": "p. 41", "Morphine": "p. 81",
                 "Codeine": "p. 81", "Clopidogrel": "p. 81", "Azathioprine": "L02 S33; p. 682", "Heparin": "p. 26", "Protamine": "p. 26",
                 "Phenoxybenzamine": "p. 25", "Rifampin": "p. 63", "St. John's wort": "p. 72", "Grapefruit juice": "p. 48; p. 64",
                 "Ketoconazole": "p. 64", "Ritonavir": "p. 64", "N-acetylcysteine": "L03 S19; p. 66",
                 "Acetaminophen": "L03 S15", "Aspirin": "p. 675; p. 677", "Ibuprofen": "L03 S28; S60", "Naproxen": "L03 S28", "Diclofenac": "L03 S28; S60",
                 "Indomethacin": "L03 S28", "Ketorolac": "L03 S28", "Celecoxib": "L03 S29; S60", "Tramadol": "p. 694", "Methotrexate": "L03 S47-49",
                 "Hydroxychloroquine": "L03 S47; p. 684", "Sulfasalazine": "L03 S47", "Leflunomide": "L03 S47; p. 687", "Adalimumab": "L03 S51; S60",
                 "Etanercept": "L03 S51; S60", "Infliximab": "L03 S51; S60", "Tocilizumab": "L03 S51; S60", "Rituximab": "L03 S51", "Abatacept": "L03 S51-52",
                 "Tofacitinib": "p. 686", "Meloxicam": "L03 S60; p. 679",
                 "Allopurinol": "L04 S12", "Rasburicase": "L04 S15", "Colchicine": "L04 S10; S19", "Febuxostat": "L04 S12", "Probenecid": "L04 S14",
                 "Pegloticase": "L04 S14", "Prednisone": "L04 S19", "Baclofen": "L04 S27; S38", "Tizanidine": "L04 S29; S38", "Cyclobenzaprine": "L04 S31; S38",
                 "Carisoprodol": "L04 S23; S33", "Methocarbamol": "L04 S23", "Metaxalone": "L04 S23", "Chlorzoxazone": "L04 S23", "Diazepam": "L04 S38",
                 "Dantrolene": "L04 S34; S38", "Botulinum toxin": "L04 S33; S38", "Succinylcholine": "L04 S38", "Vecuronium": "L04 S38", "Cisatracurium": "L04 S38",
                 "Alendronate": "L04 S47; S62", "Risedronate": "L04 S47", "Ibandronate": "L04 S47", "Zoledronic acid": "L04 S47", "Denosumab": "L04 S54",
                 "Teriparatide": "L04 S54", "Abaloparatide": "L04 S54", "Romosozumab": "L04 S54-55", "Raloxifene": "L04 S54; S62", "Calcitonin": "L04 S42; S62"}
for _d in DRUGS:
    _d["cls_src"] = CLASS_SOURCES.get(_d["name"], "")


# ---------------------------------------------------------------- Unit 3 (L05, L06): cards built from the lectures' Drug Profile slides
# Every profile field (indications, adverse effects, contraindications, toxicity, formulation, dose) is copied from the slide;
# mechanism and patient-specific lines below come from the teaching slides of the same lecture.
import profiles as _profiles

_MOA = {
    "Omeprazole": ("Irreversibly inhibits the H⁺/K⁺-ATPase proton pump — the final common pathway of acid secretion (acid-activated prodrug, covalent bond).", "L05 S15-16; SG U3-R2"),
    "Esomeprazole": ("PPI: irreversibly inhibits the H⁺/K⁺-ATPase proton pump (S-isomer of omeprazole).", "L05 S15; p. 1157"),
    "Pantoprazole": ("PPI: irreversibly inhibits the H⁺/K⁺-ATPase proton pump.", "L05 S15"),
    "Lansoprazole": ("PPI: irreversibly inhibits the H⁺/K⁺-ATPase proton pump.", "L05 S15"),
    "Dexlansoprazole": ("PPI: irreversibly inhibits the H⁺/K⁺-ATPase proton pump (R-isomer of lansoprazole).", "L05 S15; p. 1157"),
    "Famotidine": ("Competitively blocks histamine at the parietal-cell H2 receptor → less cAMP → less pump activity → less acid.", "L05 S13-14"),
    "Cimetidine": ("Competitively blocks histamine at the parietal-cell H2 receptor.", "L05 S13-14"),
    "Calcium carbonate": ("Antacid: directly neutralizes existing gastric acid; does not reduce acid production.", "L05 S12"),
    "Magnesium hydroxide": ("Antacid: neutralizes existing acid; also an osmotic laxative (draws water into the lumen).", "L05 S12; L06 S4"),
    "Aluminum hydroxide": ("Antacid: neutralizes existing acid; also binds phosphate.", "L05 S12; S55"),
    "Sucralfate": ("Polymerizes in acid (pH below 4) and binds the ulcer base, forming a protective barrier; minimal systemic absorption.", "L05 S20-21; SG U3-R5"),
    "Misoprostol": ("PGE1 analog: acts on EP receptors to cut acid and raise mucus and bicarbonate — restores the prostaglandin tone NSAIDs suppress.", "L05 S20-21; SG U3-R5"),
    "Bismuth subsalicylate": ("Antisecretory, mild antimicrobial, and anti-inflammatory; coats ulcers.", "L06 S9; p. 1162"),
    "Amoxicillin": ("Penicillin: blocks bacterial cell wall synthesis (H. pylori triple therapy).", "L05 S24; S28"),
    "Clarithromycin": ("Macrolide: binds the 50S ribosome (H. pylori triple therapy).", "L05 S24 (notes)"),
    "Metronidazole": ("Nitroimidazole: adds a second antibiotic mechanism in H. pylori regimens.", "L05 S24"),
    "Tetracycline": ("Tetracycline antibiotic in bismuth quadruple therapy.", "L05 S23-24"),
    "Ondansetron": ("Blocks serotonin 5-HT3 receptors on gut vagal afferents and the chemoreceptor trigger zone, so no signal reaches the vomiting center.", "L05 S30-31; SG U3-M"),
    "Metoclopramide": ("D2 antagonism in the CTZ (antiemetic) plus D2 blockade and 5-HT4 agonism in the gut → more acetylcholine → faster gastric emptying (prokinetic).", "L05 S36-37; SG U3-M"),
    "Aprepitant": ("Blocks substance P/neurokinin at NK1 receptors in the CTZ.", "L05 S30; SG U3-M"),
    "Meclizine": ("Blocks histamine H1 (and acetylcholine) signals from the vestibular system.", "L05 S30; SG U3-M"),
    "Scopolamine": ("Muscarinic antagonist: blocks acetylcholine from the vestibular system.", "L05 S30; S43; SG U3-M"),
    "Prochlorperazine": ("Phenothiazine: blocks dopamine D2 at the CTZ (and other receptors).", "L05 S30; S43"),
    "Dronabinol": ("Synthetic cannabinoid: activates CB1 receptors in the vomiting center and CTZ, reducing neurotransmitter release; also stimulates appetite — a pathway distinct from 5-HT3, D2, NK1, H1/M1.", "L05 S38-39; SG U3-M"),
    "Dexamethasone": ("Corticosteroid that adds to other antiemetics in chemotherapy regimens.", "L05 S32; S43"),
    "Polyethylene glycol 3350": ("Osmotic laxative: draws water into the lumen.", "L06 S4-5"),
    "Psyllium": ("Bulk-forming laxative: absorbs water, increases stool bulk and transit.", "L06 S4-5"),
    "Methylcellulose": ("Bulk-forming laxative: holds water and expands stool.", "L06 S4-5"),
    "Lactulose": ("Osmotic laxative (nonabsorbable sugar): draws water into the lumen; also lowers ammonia.", "L06 S4; S57"),
    "Senna": ("Stimulant laxative: directly stimulates enteric nerves and motility.", "L06 S4-5"),
    "Bisacodyl": ("Stimulant laxative: activates enteric nerves.", "L06 S4-5"),
    "Lubiprostone": ("Secretagogue: activates the ClC-2 chloride channel → more chloride and fluid secretion.", "L06 S4-5; S60"),
    "Linaclotide": ("Secretagogue: guanylate cyclase-C agonist → more chloride and fluid secretion.", "L06 S4-5; S61"),
    "Loperamide": ("Peripheral mu-opioid agonist on enteric neurons → less acetylcholine → slower peristalsis, more water absorbed; enters the CNS poorly (P-gp efflux).", "L06 S9-10"),
    "Diphenoxylate/atropine": ("Opioid-receptor agonist slows motility; atropine at a subtherapeutic dose discourages misuse.", "L06 S9-10; SG U3-R10"),
    "Mesalamine": ("5-ASA: anti-inflammatory action local to the GI mucosa, reducing inflammatory mediators.", "L06 S16-17"),
    "Budesonide": ("Locally acting corticosteroid with high first-pass metabolism — less systemic exposure than prednisone.", "L06 S18"),
    "Mercaptopurine": ("Thiopurine: metabolized to thioguanine nucleotides that block purine synthesis in lymphocytes.", "L06 S19"),
    "Vedolizumab": ("Blocks α4β7 integrin-mediated leukocyte gut-homing — gut-selective, less systemic immunosuppression.", "L06 S20; S52; SG U3-R11"),
    "Ustekinumab": ("Blocks interleukin-12 and -23 signaling.", "L06 S20"),
    "Cyanocobalamin": ("Replaces vitamin B12 (absorption needs stomach acid to free it from food and intrinsic factor in the terminal ileum).", "L06 S33"),
    "Folic acid": ("Replaces folate (water-soluble vitamin B9).", "L06 S32; S77"),
    "Vitamin D": ("Fat-soluble vitamin; deficiency impairs bone mineralization.", "L06 S30; S32"),
    "Phytonadione": ("Vitamin K1: supports carboxylation of clotting factors II, VII, IX, X, opposing warfarin.", "L06 S32; S35"),
    "Ferrous sulfate": ("Replaces iron; absorption enhanced by vitamin C, impaired by antacids and PPIs.", "L06 S32"),
    "Ginkgo biloba": ("Herbal supplement that raises bleeding risk with anticoagulants/antiplatelets.", "L06 S40"),
    "Fish oil": ("Omega-3 fatty acids; raise bleeding risk at high doses with anticoagulants.", "L06 S40; S83"),
}
_PT = {
    "Omeprazole": [("Take 30-60 minutes before the first meal (works on actively secreting pumps).", "L05 S15-16"),
                   ("Omeprazole and esomeprazole inhibit CYP2C19 and can blunt clopidogrel activation.", "L05 S15; SG U3-R4"),
                   ("Long-term risks: C. difficile, fractures, hypomagnesemia, B12 deficiency, pneumonia, acute interstitial nephritis; rebound acid on stopping.", "L05 S16; SG U3-R3")],
    "Esomeprazole": [("Like omeprazole, inhibits CYP2C19 (clopidogrel interaction).", "L05 S16")],
    "Pantoprazole": [("Fewer CYP drug interactions than omeprazole — textbook: preferred with clopidogrel.", "L05 S48; p. 1161")],
    "Famotidine": [("Most commonly used H2 blocker; minimal CYP450 interaction; renal dose adjustment; confusion risk in older adults.", "L05 S13-14")],
    "Cimetidine": [("Potent CYP450 inhibitor (1A2, 2C19, 3A4) and antiandrogenic (gynecomastia) — raises warfarin, phenytoin, theophylline.", "L05 S13-14; S52")],
    "Calcium carbonate": [("Separate from other oral drugs by at least 2 hours.", "L05 S12")],
    "Magnesium hydroxide": [("Diarrhea; caution in renal impairment (magnesium accumulation).", "L05 S12; L06 S4")],
    "Aluminum hydroxide": [("Constipating.", "L05 S12")],
    "Sucralfate": [("Needs acid to activate — empty stomach, separated from antacids/PPIs and other drugs by 2 hours; aluminum accumulates in CKD.", "L05 S20-21")],
    "Misoprostol": [("Contraindicated in pregnancy — potent uterotonic/abortifacient; diarrhea and cramping common.", "L05 S20-21; SG U3-R5")],
    "Clarithromycin": [("Strong CYP3A4 inhibitor (statins); recent macrolide exposure raises resistance concern → bismuth quadruple therapy.", "L05 S23-25; SG U3-R6")],
    "Metronidazole": [("Disulfiram-like reaction with alcohol; substitutes for amoxicillin with penicillin allergy.", "L05 S23; SG U3-R6")],
    "Tetracycline": [("Avoid in pregnancy and children.", "L05 S23")],
    "Amoxicillin": [("Penicillin allergy rules it out — substitute metronidazole or use bismuth quadruple therapy.", "L05 S23; S25; SG U3-R6")],
    "Ondansetron": [("Give before chemotherapy; QT prolongation; CYP2D6 ultrarapid metabolizers may respond less well.", "L05 S31")],
    "Metoclopramide": [("Boxed warning: tardive dyskinesia — avoid beyond 12 weeks; acute dystonia → diphenhydramine or benztropine; avoid in Parkinson disease; renal dosing; CYP2D6 poor metabolizers need lower doses.", "L05 S36-37; SG U3-R8")],
    "Meclizine": [("Motion sickness is vestibular — H1/M1 blockers fit.", "L05 S33; SG U3-R7")],
    "Dronabinol": [("Reserved for refractory CINV; dronabinol Schedule III, nabilone Schedule II; caution in older adults.", "L05 S38-39")],
    "Polyethylene glycol 3350": [("First-line for chronic constipation; fast, reliable onset.", "L06 S4-5")],
    "Psyllium": [("Slowest onset, safest long term; needs adequate fluids; avoid in obstruction.", "L06 S4-5")],
    "Senna": [("Short-term or breakthrough use; cramping.", "L06 S4-5")],
    "Linaclotide": [("Diarrhea; contraindicated in mechanical obstruction and in children under 2.", "L06 S5")],
    "Lubiprostone": [("Nausea is the classic adverse effect.", "L06 S5")],
    "Loperamide": [("Avoid in suspected C. difficile and in bloody or febrile diarrhea; very high doses → QT prolongation.", "L06 S9-11; SG U3-R10")],
    "Diphenoxylate/atropine": [("Schedule V; avoid in young children and in infectious diarrhea.", "L06 S9-10; SG U3-R10")],
    "Mesalamine": [("First-line for mild-to-moderate UC; monitor renal function (interstitial nephritis); enemas/suppositories for distal disease.", "L06 S16-17; SG U3-R11")],
    "Budesonide": [("Short-term induction of remission; not for maintenance.", "L06 S18")],
    "Mercaptopurine": [("Test TPMT and NUDT15 first; allopurinol → cut dose by about two-thirds to three-quarters; monitor CBC and LFTs; onset weeks to months.", "L06 S19")],
    "Vedolizumab": [("The IBD biologic that is most gut-selective.", "L06 S52; SG U3-R11")],
    "Cyanocobalamin": [("Monitor B12 in long-term PPI or metformin users; treat with IM or high-dose oral B12.", "L06 S33; SG U3-R12")],
    "Folic acid": [("Critical in pregnancy to prevent neural tube defects.", "L06 S32")],
    "Phytonadione": [("Warfarin patients: keep vitamin K intake consistent rather than avoiding it.", "L06 S35")],
    "Ginkgo biloba": [("Ask about supplements at every medication reconciliation.", "L06 S40")],
}
_MOA.update({
    "Furosemide": ("Loop diuretic: blocks NKCC2 in the thick ascending limb (~25% of filtered Na⁺) and collapses the lumen-positive potential → ↑ Ca²⁺ and Mg²⁺ excretion.", "L09 S10-11"),
    "Bumetanide": ("Loop diuretic: blocks NKCC2 in the thick ascending limb; about 40× furosemide potency mg for mg.", "L09 S10; S24; S28"),
    "Torsemide": ("Loop diuretic: blocks NKCC2 in the thick ascending limb.", "L09 S10"),
    "Hydrochlorothiazide": ("Thiazide: blocks the Na-Cl cotransporter (NCC) in the distal convoluted tubule (~5–8% of Na⁺); lower cell Na⁺ drives NCX Ca²⁺ reabsorption → ↓ urinary Ca²⁺.", "L09 S12-13"),
    "Chlorthalidone": ("Thiazide-like: blocks NCC in the distal convoluted tubule; same site as HCTZ, longer action.", "L09 S12; S24"),
    "Spironolactone": ("Aldosterone (mineralocorticoid) receptor antagonist in the collecting duct → less ENaC and Na/K pump activity → less K⁺ and H⁺ secretion; also antiandrogen.", "L09 S17-18"),
    "Eplerenone": ("Selective aldosterone receptor antagonist in the collecting duct; far fewer antiandrogen effects than spironolactone.", "L09 S17-18; S33"),
    "Amiloride": ("ENaC blocker: blocks the collecting-duct sodium channel directly, independent of aldosterone → less K⁺ and H⁺ secretion.", "L09 S17-18"),
    "Triamterene": ("ENaC blocker: blocks the collecting-duct sodium channel directly, independent of aldosterone.", "L09 S17-18"),
    "Acetazolamide": ("Carbonic anhydrase inhibitor: blocks Na⁺/HCO₃⁻ reabsorption in the proximal tubule → bicarbonate diuresis and metabolic acidosis; weak diuretic.", "L09 S19-20; SG U5-R6"),
    "Mannitol": ("Osmotic diuretic: filtered but poorly reabsorbed, so it holds water in the tubule lumen; draws water out of cells (lowers ICP/IOP).", "L09 S19-20"),
})
_PT.update({
    "Furosemide": [("Preferred over thiazides in edema and advanced CKD (GFR < 30); give IV no faster than 4 mg/min.", "L09 S14-15; S27"),
                   ("Hypokalemia raises digoxin toxicity; aminoglycosides add ototoxicity; NSAIDs blunt the effect.", "L09 S38"),
                   ("Hypercalcemia: give with saline — a loop alone causes volume contraction.", "p. 280")],
    "Bumetanide": [("About 40 times more potent than furosemide mg for mg.", "L09 S28")],
    "Torsemide": [("Longer half-life and more predictable absorption than furosemide; less ototoxicity.", "L09 S29")],
    "Hydrochlorothiazide": [("First-line for essential hypertension with preserved renal function; loses efficacy below GFR ~30 — switch to a loop.", "L09 S12; S15"),
                            ("Hyponatremia in older adults; raises lithium levels; useful for calcium stones and osteoporosis.", "L09 S12; S38"),
                            ("Hyperglycemia mainly above 50 mg/d.", "p. 272")],
    "Chlorthalidone": [("Often preferred for 24-hour BP control (half-life 40–60 h); more hypokalemia and hyponatremia than HCTZ at equal dose.", "L09 S12; S31")],
    "Spironolactone": [("Hyperkalemia, especially with ACE inhibitors/ARBs or CKD — check potassium and creatinine within 1 week; gynecomastia.", "L09 S17; S23; S32"),
                       ("Cirrhotic ascites responds well; RALES benefit in severe heart failure.", "p. 275; p. 279")],
    "Eplerenone": [("Choose over spironolactone when gynecomastia is a problem; avoid with strong CYP3A4 inhibitors, K⁺ > 5.5 or CrCl < 30.", "L09 S17; S33")],
    "Amiloride": [("Adjunct to a loop or thiazide to preserve potassium; lithium-induced nephrogenic diabetes insipidus.", "L09 S17; S34")],
    "Triamterene": [("Combined with HCTZ (Maxzide, Dyazide); kidney stones, blue urine; AKI with NSAIDs.", "L09 S35; p. 275")],
    "Acetazolamide": [("Niche uses: glaucoma, altitude sickness (start a day before ascent), metabolic alkalosis; sulfonamide caution.", "L09 S19; S36; S38")],
    "Mannitol": [("Raised ICP/IOP; needs intact renal perfusion; avoid in heart failure and volume depletion; monitor osmolality and electrolytes.", "L09 S19-20; S37")],
})
_EXTRA_ALIAS = {"Dronabinol": ["Nabilone", "Cesamet"], "Diphenoxylate/atropine": ["Diphenoxylate"], "Polyethylene glycol 3350": ["PEG 3350", "Polyethylene glycol"],
                "Mercaptopurine": ["6-mercaptopurine"]}
_by = {d["name"].lower(): d for d in DRUGS}
_LOOP_IX = [("Digoxin: loop hypokalemia increases toxicity. Aminoglycosides: additive ototoxicity. NSAIDs blunt the diuretic effect and raise AKI risk.", "L09 S38")]
_THZ_IX = [("Lithium levels rise; NSAIDs blunt the effect.", "L09 S38")]
_KS_IX = [("Hyperkalemia with ACE inhibitors, ARBs, potassium supplements, trimethoprim, or CKD.", "L09 S17; S38")]
_IX = {"Furosemide": _LOOP_IX, "Bumetanide": _LOOP_IX, "Torsemide": _LOOP_IX, "Hydrochlorothiazide": _THZ_IX, "Chlorthalidone": _THZ_IX,
       "Spironolactone": _KS_IX, "Eplerenone": [*_KS_IX, ("Strong CYP3A4 inhibitors (ketoconazole) raise levels sharply.", "L09 S33")],
       "Amiloride": _KS_IX, "Triamterene": [*_KS_IX, ("AKI with NSAIDs (indomethacin).", "L09 S35; p. 275")],
       "Acetazolamide": [("Sulfonamide allergy: use caution.", "L09 S38")]}
_ACEI_MOA = ("Blocks ACE (angiotensin I → II): less vasoconstriction and aldosterone; also less bradykinin breakdown (cough, angioedema). Dilates the efferent arteriole → ↓ intraglomerular pressure and proteinuria.", "L10 S5-6; S8; SG U5-R8")
_ARB_MOA = ("Blocks the AT1 receptor directly; no bradykinin rise, so no cough. Same efferent-arteriole renoprotection as ACE inhibitors.", "L10 S7-8")
_RAAS_PT = [("First-line in proteinuric CKD; creatinine rise up to ~30% is expected — continue; more → renal artery stenosis or volume depletion.", "L10 S5; S8; S10; SG U5-R9"),
            ("Contraindicated in pregnancy; check potassium and creatinine within 1–2 weeks; sick-day rules (hold in vomiting, diarrhea, dehydration).", "L10 S5; S8-9")]
_RAAS_IX = [("Hyperkalemia with potassium supplements, potassium-sparing diuretics, trimethoprim; triple whammy AKI with an NSAID plus a diuretic; never with aliskiren in diabetes.", "L10 S7; S23; S55")]
_DHP_MOA = ("Dihydropyridine CCB: arteriolar dilation → ↓ afterload — the same mechanism treats hypertension and angina.", "L10 S12-13; S22; SG U5-R10")
_NDHP_MOA = ("Non-dihydropyridine CCB: ↓ heart rate and contractility, ↑ coronary flow, plus arteriolar dilation.", "L10 S12-13; S22")
_NDHP_IX = [("With a beta-blocker → bradycardia and AV block; raises digoxin levels; rifampin and carbamazepine lower levels.", "L10 S13; S55")]
_BB_MOA = ("Beta-1 selective blocker: ↓ heart rate, contractility and renin release.", "L10 S12-13")
_NIT_MOA = ("Releases nitric oxide → guanylate cyclase → ↑ cGMP → smooth-muscle relaxation, mainly venodilation → ↓ preload and O₂ demand.", "L10 S19-20; SG U5-R11")
_NIT_PT = [("Absolute contraindication with PDE5 inhibitors (sildenafil) — life-threatening hypotension; nitrate-free interval prevents tolerance.", "L10 S19-20; SG U5-R11")]
_MOA.update({
    "Captopril": _ACEI_MOA, "Lisinopril": _ACEI_MOA, "Enalapril": _ACEI_MOA, "Losartan": _ARB_MOA, "Valsartan": _ARB_MOA,
    "Aliskiren": ("Direct renin inhibitor: blocks the rate-limiting first step of the RAAS.", "L10 S7"),
    "Amlodipine": _DHP_MOA, "Nifedipine ER": _DHP_MOA, "Diltiazem": _NDHP_MOA, "Verapamil": _NDHP_MOA, "Metoprolol": _BB_MOA, "Atenolol": _BB_MOA,
    "Clonidine": ("Central α2 agonist: ↓ sympathetic outflow → ↓ BP.", "L10 S16"),
    "Methyldopa": ("Central α2 agonist: ↓ sympathetic outflow → ↓ BP.", "L10 S16"),
    "Hydralazine": ("Direct arteriolar vasodilator → reflex tachycardia and fluid retention.", "L10 S16"),
    "Nitroglycerin": _NIT_MOA, "Isosorbide mononitrate": _NIT_MOA, "Isosorbide dinitrate": _NIT_MOA,
})
_PT.update({
    "Captopril": _RAAS_PT, "Lisinopril": _RAAS_PT, "Enalapril": _RAAS_PT,
    "Losartan": [("The usual switch for ACE-inhibitor cough.", "L10 S6-7"), *_RAAS_PT], "Valsartan": [("The usual switch for ACE-inhibitor cough.", "L10 S6-7"), *_RAAS_PT],
    "Aliskiren": [("Limited use; not combined with an ACE inhibitor or ARB (additive hyperkalemia and hypotension, no benefit).", "L10 S7")],
    "Amlodipine": [("Pairs safely with beta-blockers; peripheral edema is the class adverse effect.", "L10 S12-13")],
    "Nifedipine ER": [("Avoid immediate-release forms; peripheral edema, reflex tachycardia.", "L10 S22; S44")],
    "Diltiazem": [("Avoid with beta-blockers (bradycardia, AV block).", "L10 S13; S22")],
    "Verapamil": [("Avoid with beta-blockers; constipation; raises digoxin.", "L10 S13; S22; S55")],
    "Metoprolol": [("Not first-line for uncomplicated HTN; compelling with CAD, heart failure, arrhythmia; never with diltiazem/verapamil; do not stop abruptly.", "L10 S12-13; S47")],
    "Atenolol": [("Accumulates in renal impairment — reduce dose when CrCl < 35 mL/min.", "L10 S48")],
    "Clonidine": [("Abrupt withdrawal → rebound hypertension; reserved for resistant hypertension.", "L10 S12; S16")],
    "Methyldopa": [("Preferred oral option for hypertension in pregnancy.", "L10 S12; S16; S50")],
    "Hydralazine": [("Must be paired with a beta-blocker and a diuretic; drug-induced lupus.", "L10 S16; S51")],
    "Nitroglycerin": [("Acute angina: 0.4 mg SL every 5 minutes up to 3 doses.", "L10 S19; S52"), *_NIT_PT],
    "Isosorbide mononitrate": _NIT_PT, "Isosorbide dinitrate": [*_NIT_PT, ("With hydralazine for heart failure in Black patients.", "L10 S54")],
})
_IX.update({"Captopril": _RAAS_IX, "Lisinopril": _RAAS_IX, "Enalapril": _RAAS_IX, "Losartan": _RAAS_IX, "Valsartan": _RAAS_IX,
            "Aliskiren": [("Never with ACE inhibitors or ARBs in diabetes or eGFR < 60.", "L10 S7; S42")],
            "Amlodipine": [("Grapefruit juice raises dihydropyridine levels.", "L10 S55")], "Nifedipine ER": [("Grapefruit juice raises dihydropyridine levels.", "L10 S55")],
            "Diltiazem": _NDHP_IX, "Verapamil": _NDHP_IX,
            "Metoprolol": [("With diltiazem or verapamil → bradycardia, AV block.", "L10 S13")], "Atenolol": [("With diltiazem or verapamil → bradycardia, AV block.", "L10 S13")],
            "Nitroglycerin": [("PDE5 inhibitors or riociguat → severe hypotension.", "L10 S19; S52")],
            "Isosorbide mononitrate": [("PDE5 inhibitors or riociguat → severe hypotension.", "L10 S53")],
            "Isosorbide dinitrate": [("PDE5 inhibitors or riociguat → severe hypotension.", "L10 S54")]})
_EXTRA_ALIAS.update({"Nifedipine ER": ["Nifedipine"]})
_INS = ("Activates the insulin receptor → GLUT4 to the cell surface (glucose uptake), glycogen storage, ↓ hepatic glucose output.", "L08 S12-13")
_INS_PT = [("Main risk hypoglycemia: rule of 15; beta-blockers mask warning signs; rotate sites; never share pens.", "L08 S12-13")]
_COC_MOA = ("Estrogen + progestin suppress GnRH/FSH/LH → no follicle maturation or LH surge; progestin thickens cervical mucus and thins the endometrium.", "L08 S4-6")
_PO_MOA = ("Progestin: thickens cervical mucus and thins the endometrium; no estrogen, so no estrogen-related VTE risk.", "L08 S5-6")
_PO_PT = [("Preferred when estrogen is contraindicated (VTE/stroke, smoker ≥ 35, migraine with aura).", "L08 S5-6")]
_GLP = ("GLP-1 receptor agonist: glucose-dependent insulin release, less glucagon, slower gastric emptying, satiety/weight loss.", "L08 S18-19")
_GLP_PT = [("GI upset, pancreatitis, gallstones; contraindicated with personal/family MTC or MEN2; never with a DPP-4 inhibitor.", "L08 S18-19")]
_DPP = ("DPP-4 inhibitor: blocks breakdown of endogenous GLP-1, prolonging its glucose-dependent effect.", "L08 S18-19")
_DPP_PT = [("Weight-neutral, well tolerated, low hypoglycemia risk — a good add-on for an older adult who falls.", "L08 S18; S21")]
_SU = ("Sulfonylurea: binds and closes the β-cell K-ATP channel → insulin release regardless of glucose.", "L08 S11; S14; S35")
_SU_PT = [("Highest hypoglycemia risk among oral agents — avoid in an older adult living alone with falls.", "L08 S14; S21")]
_MOA.update({
    "Combined oral contraceptives": _COC_MOA, "Norethindrone": _PO_MOA, "Medroxyprogesterone depot": _PO_MOA, "Levonorgestrel IUD": _PO_MOA,
    "Tamoxifen": ("SERM: estrogen-receptor antagonist in breast, agonist in bone and endometrium (prodrug activated by CYP2D6).", "L08 S7-8"),
    "Raloxifene": ("SERM: agonist in bone; antagonist in breast and endometrium.", "L08 S7-8"),
    "Testosterone": ("Androgen replacement; converted to DHT by 5-alpha-reductase.", "L08 S7; S9"),
    "Finasteride": ("5-alpha-reductase inhibitor: blocks testosterone → DHT in prostate and skin.", "L08 S9"),
    "Insulin lispro": _INS, "Insulin aspart": _INS, "Regular insulin": _INS, "NPH insulin": _INS, "Insulin glargine": _INS, "Insulin detemir": _INS, "Insulin degludec": _INS,
    "Metformin": ("Biguanide: enters hepatocytes via OCT1, inhibits mitochondrial complex I and activates AMPK → ↓ gluconeogenesis; ↑ muscle insulin sensitivity.", "L08 S14-15"),
    "Glipizide": _SU, "Glyburide": _SU,
    "Repaglinide": ("Meglitinide: closes K-ATP channels — short-acting mealtime insulin secretagogue.", "L08 S14; S28"),
    "Pioglitazone": ("Thiazolidinedione (PPAR-γ agonist): ↑ peripheral insulin sensitivity.", "L08 S14; p. 798"),
    "Empagliflozin": ("SGLT2 inhibitor: blocks proximal-tubule glucose reabsorption (SGLT2 normally takes back ~90%) → glucosuria.", "L08 S16"),
    "Exenatide": _GLP, "Liraglutide": _GLP, "Semaglutide": _GLP, "Sitagliptin": _DPP, "Linagliptin": _DPP,
    "Cinacalcet": ("Calcimimetic: makes the parathyroid calcium-sensing receptor more sensitive, so PTH secretion falls.", "L08 S25-26"),
    "Calcitriol": ("Active vitamin D (1,25-dihydroxy): bypasses the PTH-dependent activation step.", "L08 S25; S35"),
    "Recombinant PTH 1-84": ("Replaces parathyroid hormone.", "L08 S25"),
    "Calcium carbonate or citrate": ("Calcium replacement given with calcitriol in hypoparathyroidism.", "L08 S25"),
})
_PT.update({
    "Combined oral contraceptives": [("No estrogen with VTE/stroke, smoker ≥ 35, migraine with aura, estrogen-sensitive cancer, uncontrolled HTN, liver disease.", "L08 S5; SG U4-R10")],
    "Norethindrone": _PO_PT, "Medroxyprogesterone depot": [*_PO_PT, ("Bone density warning with long-term use.", "L08 S6 (notes)")], "Levonorgestrel IUD": _PO_PT,
    "Tamoxifen": [("Endometrial cancer and VTE risk, hot flashes — report vaginal bleeding.", "L08 S8")],
    "Raloxifene": [("Prevents osteoporosis/vertebral fracture; no endometrial cancer increase; VTE and hot flashes; not for breast cancer treatment.", "L08 S8")],
    "Testosterone": [("Monitor hematocrit (erythrocytosis), PSA and lipids; avoid in prostate cancer.", "L08 S7; S9")],
    "Finasteride": [("PSA falls by about half — double it when screening; pregnant women must not handle crushed tablets; sexual side effects.", "L08 S9")],
    "Insulin lispro": [("Rapid-acting: dose with meals (onset ~15 min).", "L08 S12-13"), *_INS_PT], "Insulin aspart": [("Rapid-acting: dose with meals (onset ~15 min).", "L08 S12-13"), *_INS_PT],
    "Regular insulin": [("Short-acting (onset ~30 min, give 30 min before meals); the only insulin given IV.", "L08 S12; S13"), *_INS_PT],
    "NPH insulin": [("Intermediate: cloudy suspension, variable absorption, peaks about 4–10 h.", "L08 S12-13"), *_INS_PT],
    "Insulin glargine": [("Basal, relatively peakless; do not mix with other insulins.", "L08 S12; p. 793"), *_INS_PT],
    "Insulin detemir": [("Basal, relatively peakless.", "L08 S12"), *_INS_PT], "Insulin degludec": [("Ultra-long basal.", "L08 S12"), *_INS_PT],
    "Metformin": [("First-line type 2 diabetes: no weight gain, low hypoglycemia; GI upset (start low, with food); B12 deficiency.", "L08 S14-15"),
                  ("Avoid eGFR < 30 (lactic acidosis); hold for iodinated contrast with reduced kidney function.", "L08 S15; S67; p. 798")],
    "Glipizide": _SU_PT, "Glyburide": _SU_PT,
    "Repaglinide": [("Take with meals; gemfibrozil raises levels (CYP2C8).", "L08 S67")],
    "Pioglitazone": [("Fluid retention/heart failure, weight gain; contraindicated in NYHA III–IV.", "L08 S14; p. 799")],
    "Empagliflozin": [("Cardiorenal benefit; genital yeast infections, volume depletion, euglycemic DKA — hold when ill or before surgery; rare Fournier gangrene.", "L08 S16")],
    "Exenatide": _GLP_PT, "Liraglutide": _GLP_PT, "Semaglutide": _GLP_PT, "Sitagliptin": _DPP_PT, "Linagliptin": _DPP_PT,
    "Cinacalcet": [("Secondary hyperparathyroidism in CKD on dialysis, parathyroid carcinoma; nausea, hypocalcemia, QT — monitor calcium.", "L08 S25-26")],
    "Calcitriol": [("With oral calcium for hypoparathyroidism (post-thyroidectomy); monitor for hypercalcemia.", "L08 S25; S27")],
    "Recombinant PTH 1-84": [("Reserved when calcium/calcitriol fail; monitor for hypercalcemia/hypercalciuria.", "L08 S25")],
})
_IX.update({
    "Combined oral contraceptives": [("Rifampin, carbamazepine, phenytoin, St. John’s wort lower efficacy — backup contraception.", "L08 S6; S67")],
    "Tamoxifen": [("CYP2D6 inhibitors (paroxetine, fluoxetine) blunt activation.", "L08 S8 (notes); S67")],
    "Metformin": [("Iodinated contrast with reduced kidney function → hold metformin.", "L08 S67")],
    "Glipizide": [("Beta-blockers mask hypoglycemia symptoms.", "L08 S67")], "Glyburide": [("Beta-blockers mask hypoglycemia symptoms.", "L08 S67")],
    "Repaglinide": [("Gemfibrozil raises levels (CYP2C8).", "L08 S67")],
    "Cinacalcet": [("CYP2D6 inhibitor.", "L08 S26")],
    "Semaglutide": [("Do not combine with a DPP-4 inhibitor.", "L08 S19")], "Liraglutide": [("Do not combine with a DPP-4 inhibitor.", "L08 S19")],
    "Exenatide": [("Do not combine with a DPP-4 inhibitor.", "L08 S19")],
})
_EXTRA_ALIAS.update({"Combined oral contraceptives": ["Combined pill", "Ethinyl estradiol"], "Medroxyprogesterone depot": ["DMPA", "Medroxyprogesterone"],
                     "Levonorgestrel IUD": ["Levonorgestrel"], "Regular insulin": ["Insulin regular"], "Recombinant PTH 1-84": ["Parathyroid hormone"]})
_MOA.update({
    "Estradiol": ("Binds intracellular estrogen receptors (ER-α, ER-β) → gene transcription in reproductive, bone, cardiovascular and CNS tissue.", "L11 S5; SG U6-R1"),
    "Anastrozole": ("Aromatase inhibitor: blocks peripheral (fat) conversion of androgens to estrogens.", "L11 S13-14; SG U6-R6"),
    "Letrozole": ("Aromatase inhibitor: blocks peripheral conversion of androgens to estrogens.", "L11 S13-14"),
    "Flutamide": ("Pure androgen-receptor blocker.", "L11 S15-16; SG U6-R8"),
    "Bicalutamide": ("Pure androgen-receptor blocker (once daily).", "L11 S15-16; p. 782"),
    "Dutasteride": ("5-alpha-reductase (types 1 and 2) inhibitor: blocks testosterone → DHT.", "L11 S15-16"),
})
_PT.update({
    "Estradiol": [("With a uterus, always add a progestin (unopposed estrogen → endometrial cancer); VTE risk rises with smoking and age > 35.", "L11 S5-7; SG U6-R2")],
    "Anastrozole": [("Postmenopausal only (ovaries still make estrogen before menopause); bone loss and joint pain — protect bone.", "L11 S14; S45")],
    "Letrozole": [("Postmenopausal only; bone loss and joint pain; off-label ovulation induction.", "L11 S14; S37; S45")],
    "Flutamide": [("Prostate cancer, often with a GnRH agonist; gynecomastia and reversible hepatotoxicity.", "L11 S15; p. 782")],
    "Bicalutamide": [("Prostate cancer with a GnRH analog (leuprolide) to prevent tumor flare.", "L11 S15; S45; p. 782")],
    "Dutasteride": [("Hirsutism, alopecia and BPH (Session 2); lowers PSA; much longer half-life than finasteride.", "L11 S15; p. 781")],
})
_IX.update({"Anastrozole": [("Bisphosphonates and calcium with vitamin D protect bone.", "L11 S45")],
            "Letrozole": [("Bisphosphonates and calcium with vitamin D protect bone.", "L11 S45")],
            "Bicalutamide": [("Combined with leuprolide (GnRH agonist) in prostate cancer.", "L11 S45")],
            "Flutamide": [("Combined with a GnRH agonist in prostate cancer.", "L11 S15; S45")]})
_AM = ("Antimuscarinic: blocks M3 (and M2) receptors on the detrusor → fewer involuntary contractions, larger functional capacity.", "L12 S13-14; SG U6-R12")
_AM_PT = [("Dry mouth, constipation, blurred vision, confusion (older adults); anticholinergic burden is cumulative; avoid in narrow-angle glaucoma and urinary retention.", "L12 S13")]
_AM_IX = [("Other anticholinergics add burden; cholinesterase inhibitors (donepezil) oppose the effect.", "L12 S58")]
_A1 = ("Alpha1 blocker: relaxes bladder-neck, prostatic and proximal-urethral smooth muscle → better urinary flow in BPH; the same receptors set vascular tone.", "L12 S21-22")
_A1_IX = [("Additive hypotension with antihypertensives and PDE5 inhibitors.", "L12 S26; S58")]
_P5 = ("PDE5 inhibitor: blocks cGMP breakdown, prolonging corpus cavernosum relaxation (needs sexual stimulation).", "L12 S26-27")
_P5_PT = [("Absolute contraindication with any nitrate (or riociguat) — life-threatening hypotension; caution with alpha1 blockers; headache, flushing, dyspepsia.", "L12 S26; S28; SG U6-R16")]
_P5_IX = [("Nitrates, riociguat: contraindicated. Strong CYP3A4 inhibitors (ketoconazole, clarithromycin) raise levels.", "L12 S26; S58")]
_MOA.update({"Oxybutynin": _AM, "Tolterodine": _AM, "Solifenacin": _AM, "Darifenacin": _AM,
             "Mirabegron": ("Beta3 agonist: enhances detrusor relaxation during filling, with no anticholinergic activity.", "L12 S15; SG U6-R13"),
             "Tamsulosin": _A1, "Silodosin": _A1, "Doxazosin": _A1, "Terazosin": _A1, "Sildenafil": _P5, "Tadalafil": _P5, "Vardenafil": _P5})
_PT.update({"Oxybutynin": [("Highest CNS anticholinergic burden of the class — avoid in older adults or dementia risk; switch to mirabegron if confused.", "L12 S13; S17"), *_AM_PT],
            "Tolterodine": _AM_PT, "Solifenacin": [*_AM_PT, ("Strong CYP3A4 inhibitors raise levels.", "L12 S58")], "Darifenacin": _AM_PT,
            "Mirabegron": [("Preferred in older adults or patients on other anticholinergics; may raise blood pressure; can combine with an antimuscarinic.", "L12 S15; S17")],
            "Tamsulosin": [("Uroselective — less vascular effect; still orthostasis, first-dose effect, floppy iris in cataract surgery.", "L12 S21; SG U6-R14")],
            "Silodosin": [("Highly uroselective; avoid with CrCl below 30 mL/min.", "L12 S21; S50")],
            "Doxazosin": [("Less selective — lowers blood pressure more; first dose at bedtime (first-dose hypotension).", "L12 S21")],
            "Terazosin": [("Less selective — lowers blood pressure more; first-dose effect.", "L12 S21")],
            "Sildenafil": [*_P5_PT, ("Blue-tinged vision.", "L12 S26")], "Tadalafil": [*_P5_PT, ("Longer half-life, flexible dosing.", "L12 S26")], "Vardenafil": _P5_PT})
_IX.update({"Oxybutynin": _AM_IX, "Tolterodine": _AM_IX, "Solifenacin": _AM_IX, "Darifenacin": _AM_IX,
            "Mirabegron": [("Inhibits CYP2D6.", "L12 S15 (notes)")], "Tamsulosin": _A1_IX, "Silodosin": _A1_IX, "Doxazosin": _A1_IX, "Terazosin": _A1_IX,
            "Sildenafil": _P5_IX, "Tadalafil": _P5_IX, "Vardenafil": _P5_IX})
_SSA = ("Somatostatin analog: binds somatostatin receptors and lowers GH release (IGF-1 falls).", "L07 S6-7")
_DA = ("Dopamine D2 agonist (ergot-derived): restores dopamine’s brake on prolactin; tumor often shrinks.", "L07 S8-9; SG U4-R3")
_TH = ("Thionamide: blocks thyroid hormone organification and coupling.", "L07 S14-15")
_GC = ("Glucocorticoid: binds the cytoplasmic receptor → nucleus → anti-inflammatory genes on, NF-kB cytokines off.", "L07 S20-21")
_GC_PT = [("Chronic use suppresses CRH/ACTH — taper, never stop abruptly; hyperglycemia, osteoporosis, infection, mood change, cataracts.", "L07 S21-22; SG U4-R8")]
_MOA.update({
    "Somatropin": ("Recombinant human growth hormone (replacement).", "L07 S6"),
    "Octreotide": _SSA, "Lanreotide": _SSA,
    "Pegvisomant": ("GH-receptor antagonist: blocks GH action so IGF-1 falls (GH itself rises).", "L07 S7"),
    "Cabergoline": _DA, "Bromocriptine": _DA,
    "Desmopressin": ("Synthetic vasopressin V2 agonist: aquaporin-2 insertion → free water retained.", "L07 S10"),
    "Tolvaptan": ("Vasopressin V2 receptor antagonist: free water excreted (aquaresis).", "L07 S10"),
    "Demeclocycline": ("Tetracycline that blunts ADH action in the collecting duct.", "L07 S10"),
    "Levothyroxine": ("Synthetic T4, converted peripherally to active T3, which binds nuclear receptors.", "L07 S12-13"),
    "Methimazole": _TH, "Propylthiouracil": ("Thionamide: blocks organification and coupling and also peripheral T4 → T3 conversion.", "L07 S14-15"),
    "Potassium iodide": ("Iodine: acutely blocks thyroid hormone release (Wolff-Chaikoff).", "L07 S16; p. 725"),
    "Hydrocortisone": ("Cortisol: glucocorticoid with mineralocorticoid activity.", "L07 S21; S27"),
    "Fludrocortisone": ("Mineralocorticoid: renal sodium retention and potassium excretion.", "L07 S20"),
    "Metyrapone": ("Blocks 11-β-hydroxylase, the final step of cortisol synthesis.", "L07 S23-24"),
    "Mifepristone": ("Glucocorticoid-receptor antagonist (also a progesterone-receptor antagonist).", "L07 S23-24"),
})
_PT.update({
    "Somatropin": [("Monitor growth velocity in children and IGF-1 in adults.", "L07 S6-7")],
    "Octreotide": [("Also variceal bleeding and carcinoid syndrome; GI upset, gallstones, bradycardia, glucose changes.", "L07 S6-7")],
    "Lanreotide": [("GI upset, gallstones, bradycardia; monitor IGF-1.", "L07 S7")],
    "Pegvisomant": [("Does not shrink the tumor; monitor IGF-1 (not GH) and liver tests.", "L07 S7")],
    "Cabergoline": [("Twice weekly, better tolerated; high doses (Parkinson) linked to valve fibrosis; nausea, orthostasis.", "L07 S9")],
    "Bromocriptine": [("Daily dosing; nausea, orthostatic hypotension, dizziness.", "L07 S9")],
    "Desmopressin": [("Central DI; risk is hyponatremia — monitor sodium and limit fluids.", "L07 S8; S10")],
    "Tolvaptan": [("SIADH refractory to fluid restriction; overcorrection (osmotic demyelination) and liver injury — start in hospital.", "L07 S8; S10")],
    "Demeclocycline": [("Refractory SIADH; photosensitivity and nephrotoxicity.", "L07 S10")],
    "Levothyroxine": [("Empty stomach 30–60 min before breakfast; separate calcium, iron, antacids, PPIs, binders by 4 h; TSH at 6–8 weeks.", "L07 S12-13; SG U4-R5"),
                      ("Start low in older adults and cardiac disease; over-replacement → AF, bone loss; pregnancy raises needs.", "L07 S12-13")],
    "Methimazole": [("First line for most non-pregnant patients (once daily); avoid in first trimester; agranulocytosis and liver boxed warning — fever or sore throat → CBC.", "L07 S15")],
    "Propylthiouracil": [("First trimester and thyroid storm only — severe hepatotoxicity boxed warning.", "L07 S15; SG U4-R6")],
    "Potassium iodide": [("Thyroid storm: give at least 1 hour after a thionamide — never first (supplies substrate).", "L07 S16-18; SG U4-R7")],
    "Hydrocortisone": [("Adrenal crisis: immediate IV hydrocortisone plus IV fluids.", "L07 S27"), *_GC_PT],
    "Fludrocortisone": [("Addison disease with a glucocorticoid; monitor blood pressure and potassium.", "L07 S20")],
    "Metyrapone": [("Cushing syndrome and diagnostic testing; raises androgens and deoxycorticosterone.", "L07 S23-24")],
    "Mifepristone": [("Cushing hyperglycemia when surgery isn’t an option; contraindicated in pregnancy; hypokalemia; cortisol stays high — monitor clinically.", "L07 S23-24")],
})
_IX.update({
    "Levothyroxine": [("Calcium, iron, antacids block absorption; estrogens raise needs; rifampin, phenytoin, carbamazepine speed clearance.", "L07 S52")],
    "Cabergoline": [("Antipsychotics and metoclopramide raise prolactin.", "L07 S52")], "Bromocriptine": [("Antipsychotics and metoclopramide raise prolactin.", "L07 S52")],
    "Hydrocortisone": [("Azole antifungals raise exposure (CYP3A4); insulin and oral agents need adjusting.", "L07 S52")],
})
_SAME = {"calcium carbonate or citrate": "calcium carbonate"}
_UNIT = {"L03": 2, "L04": 2, "L05": 3, "L06": 3, "L07": 4, "L08": 4, "L09": 5, "L10": 5, "L11": 6, "L12": 6}
_TAG = {"L03": "Musculoskeletal", "L04": "Musculoskeletal", "L05": "GI", "L06": "GI & nutrition", "L07": "Endocrine", "L08": "Endocrine", "L09": "Renal", "L10": "Cardiorenal", "L11": "Reproductive", "L12": "Genitourinary"}
for _lec in ("L03", "L04", "L05", "L06", "L07", "L08", "L09", "L10", "L11", "L12"):
    for _p in _profiles.read(_lec):
        _c = f"{_lec} S{_p['slide']}"
        _f = [("ind", _p.get("ind"), _c), ("ae", _p.get("ae"), _c), ("contra", _p.get("contra"), _c),
              ("ae", "Toxicity/overdose: " + _p["tox"] if _p.get("tox") else None, _c),
              ("extra", f"Formulation: {_p.get('form', '')}. Adult dose: {_p.get('dose', '')}.", _c)]
        if _lec in ("L03", "L04"):  # these cards were written in full from the lecture; the profiles add dosing, toxicity and profile contraindications
            _f = [("contra", "Profile contraindications: " + _p["contra"] if _p.get("contra") else None, _c), _f[3], _f[4]]
        if _p["name"] in _MOA:
            _f.insert(0, ("moa", *_MOA[_p["name"]]))
        _f += [("pt", t, s) for t, s in _PT.get(_p["name"], [])]
        _f += [("ix", t, s) for t, s in _IX.get(_p["name"], [])]
        _facts = [{"text": t, "src": s, "tb": not re.search(r"\bL\d\d|\bSG\b", s), "sec": k} for k, t, s in _f if t]
        _d = _by.get(_SAME.get(_p["name"].lower(), _p["name"].lower()))
        if _d:
            _d["facts"] += _facts
            _d["unit"] = min(_d.get("unit", _UNIT[_lec]), _UNIT[_lec]) if _d.get("unit") else _UNIT[_lec]
            for _a in _p["aliases"] + _EXTRA_ALIAS.get(_p["name"], []):
                if _a not in _d["aliases"]:
                    _d["aliases"].append(_a)
            if _d["cls"].startswith("Not covered"):
                _d["cls"] = _p["cls"]
        else:
            _d = {"name": _p["name"], "cls": _p["cls"], "tags": [_TAG[_lec], _p["cls"].split(",")[0]],
                  "aliases": _p["aliases"] + _EXTRA_ALIAS.get(_p["name"], []), "unit": _UNIT[_lec], "facts": _facts}
            DRUGS.append(_d)
            _by[_p["name"].lower()] = _d
        CLASS_SOURCES.setdefault(_p["name"], _c)
        if not _d.get("cls_src"):
            _d["cls_src"] = CLASS_SOURCES[_p["name"]]
