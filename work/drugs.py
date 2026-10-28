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
    facts = [{"text": t, "src": s, "tb": not re.search(r"\bL0\d|\bSG\b", s), "sec": k} for k, _ in SECTIONS for t, s in secs.get(k, [])]
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
        "ix": [("Celecoxib raises lithium levels.", "p. 679")],
        "pt": [("Renally cleared with a narrow TI — adjust dose or interval in renal impairment.", "L02 S15")],
        "extra": [("Classic narrow-TI drug requiring blood-level monitoring.", "L01 S38; SG U1-R7"),
                  ("About 95% excreted unchanged in urine, 0% protein-bound; target ~0.7 mEq/L, toxic above 2 mEq/L; half-life ~22 h.", "p. 44")],
    }),
    D("Digoxin", "Not covered in materials", ["Narrow TI", "High Vd", "Renal dosing", "Transporters"], {
        "ix": [("Inhibiting P-glycoprotein (MDR1) raises digoxin blood levels.", "p. 9")],
        "pt": [("Renally cleared — adjust dose or interval in renal impairment.", "L02 S15")],
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
        "pt": [("TPMT deficiency raises thiopurine toxicity risk.", "L02 S33; SG U1-R12"),
               ("TPMT intermediate activity: start at 30–70% of the target dose; deficient: drastically reduce or use an alternative. NUDT15 variants also predict leukopenia.", "p. 83; p. 683")],
    }),
    D("Allopurinol", "Not covered in materials", ["Pharmacogenomics", "Hypersensitivity"], {
        "pt": [("HLA-B*5801 carriers have a sharply higher risk of severe hypersensitivity — screen before starting.", "L02 S35-36; SG U1-R12")],
        "extra": [("Suggested alternative when rasburicase is contraindicated (G6PD deficiency).", "p. 83")],
    }),
    D("Abacavir", "Not covered in materials", ["Pharmacogenomics", "Hypersensitivity"], {
        "contra": [("HLA-B*57:01-positive patients (hypersensitivity).", "p. 83; p. 88")],
    }),
    D("Rasburicase", "Not covered in materials", ["Pharmacogenomics"], {
        "contra": [("G6PD deficiency — use an alternative such as allopurinol.", "p. 83")],
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
                 "Tofacitinib": "p. 686", "Meloxicam": "L03 S60; p. 679"}
for _d in DRUGS:
    _d["cls_src"] = CLASS_SOURCES.get(_d["name"], "")
