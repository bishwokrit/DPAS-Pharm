"""Study-guide extras for L10 (summary, flows, cram sheet). Imported by author_L10.py."""

TEASER = "Today: the renin-angiotensin-aldosterone system and why ACE inhibitors and ARBs protect the kidney, the other antihypertensive classes, nitrates and calcium channel blockers in angina, and the triple whammy. The recall quiz spans both renal sessions."

SUMMARY = [
    ("The **RAAS**: angiotensinogen → (renin) → angiotensin I → (ACE) → angiotensin II → vasoconstriction + aldosterone; aliskiren, ACE inhibitors, ARBs and aldosterone antagonists each block one step.", "S4; SG U5-R7"),
    ("**ACE inhibitors/ARBs** are first-line in proteinuric CKD: efferent dilation lowers glomerular pressure; a creatinine rise **up to ~30%** is expected; check K⁺/creatinine in 1–2 weeks; **never in pregnancy**.", "S5; S8; S10; SG U5-R8; SG U5-R9"),
    ("ACE-inhibitor **cough** is bradykinin, not allergy → switch to an **ARB**; angioedema → stop.", "S6; S7"),
    ("**Non-DHP CCBs + beta-blockers** → bradycardia/AV block; resistant HTN in CKD is often a thiazide that needs to become a **loop**.", "S13; S15; S17"),
    ("**Nitrates**: NO → cGMP → venodilation; nitrate-free interval; **never with PDE5 inhibitors**. **CCBs** treat both hypertension and angina by the same mechanism.", "S19; S20; S22; SG U5-R10; SG U5-R11"),
    ("**Triple whammy**: NSAID + ACEi/ARB + diuretic → AKI; counsel against OTC NSAIDs.", "S23; S27; SG U5-R12; SG U5-S"),
]

FLOWS = {
    "RAAS Blockers": [
        {"title": "Creatinine rose after starting an ACE inhibitor", "steps": ["Recheck K⁺ and creatinine at 1–2 weeks", "Rise ≤ ~30%? Expected — continue and monitor", "Rise > 30% or sharp? Look for volume depletion or renal artery stenosis", "Vomiting, diarrhea, dehydration → sick-day rules: hold it"], "src": "S8; S9; S10"},
    ],
    "Other Antihypertensives & Resistant Hypertension": [
        {"title": "Resistant hypertension in CKD", "steps": ["BP above goal on 3+ classes including a diuretic", "Check the diuretic first: thiazide at low GFR?", "Switch thiazide → loop, or raise the loop dose", "Then add spironolactone with close K⁺ and renal monitoring"], "src": "S15; S17"},
    ],
    "Nitrates, Angina & the Triple Whammy": [
        {"title": "Triple whammy", "steps": ["NSAID constricts the afferent arteriole", "ACE inhibitor or ARB dilates the efferent arteriole", "Diuretic causes volume depletion", "Filtration pressure collapses → AKI", "Prevent: counsel on OTC NSAIDs"], "src": "S24; S27"},
    ],
}

CRAM = [
    ("RAAS blocks", "Aliskiren renin · -pril ACE · -sartan AT1 · spironolactone aldosterone", "S4; S28; SG U5-R7"),
    ("ACEi adverse effects", "Cough (bradykinin), angioedema, hyperkalemia", "S5; S6"),
    ("ACEi cough → ?", "Switch to an ARB", "S6; S7"),
    ("ACEi/ARB in pregnancy", "Contraindicated (fetal renal toxicity)", "S5; S7"),
    ("Why first-line in proteinuric CKD", "Efferent dilation → ↓ intraglomerular pressure, ↓ proteinuria", "S8; SG U5-R8"),
    ("Creatinine after ACEi", "Up to ~30% expected; more → stenosis or volume depletion", "S5; S10; SG U5-R9"),
    ("Monitoring", "K⁺ and creatinine within 1–2 weeks; sick-day rules", "S8; S9"),
    ("Aliskiren", "Never with ACEi/ARB in diabetes", "S7; S42"),
    ("DHP vs. non-DHP", "Arterioles · heart rate/contractility", "S12; S22"),
    ("Non-DHP + beta-blocker", "Bradycardia, AV block", "S13"),
    ("Hydralazine", "Pair with beta-blocker + diuretic", "S16"),
    ("Clonidine", "Rebound hypertension if stopped abruptly", "S16"),
    ("Methyldopa", "Hypertension in pregnancy", "S16; S50"),
    ("Nitrates", "NO → cGMP → venodilation; nitrate-free interval", "S19; S20"),
    ("Nitrate + PDE5 inhibitor", "Absolute contraindication — hypotension", "S19; SG U5-R11"),
    ("HTN and angina, one mechanism", "Calcium channel blockers", "S22; SG U5-R10"),
    ("Triple whammy", "NSAID + ACEi/ARB + diuretic", "S23; SG U5-R12"),
]
