"""Study-guide extras for L12 (summary, flows, cram sheet). Imported by author_L12.py."""

TEASER = "Today: the bladder’s three nerve supplies and the receptor behind each drug, overactive bladder drugs and anticholinergic burden, BPH with alpha-1 blockers and 5-ARIs, and the NO-cGMP pathway behind PDE5 inhibitors and the nitrate warning."

SUMMARY = [
    ("Bladder map: **M3** contracts the detrusor (void); **alpha1** closes the neck and **beta3** relaxes the detrusor (store); somatic nicotinic holds the external sphincter.", "S4; S7; S9; SG U6-R11"),
    ("**Antimuscarinics** block M3 — dry mouth, constipation, confusion; **oxybutynin** has the highest CNS burden → older adults get **mirabegron** (beta3; may raise BP).", "S13; S15; S17; SG U6-R12; SG U6-R13"),
    ("**Alpha1 blockers** relax the outlet in days (orthostasis, first dose, floppy iris); tamsulosin/silodosin are uroselective.", "S21; SG U6-R14"),
    ("**5-ARIs** shrink the prostate over 3–6 months and **halve PSA**; often combined with an alpha1 blocker.", "S23; S24; SG U6-R15"),
    ("**PDE5 inhibitors** keep cGMP high; **any nitrate = absolute contraindication** (and caution with alpha1 blockers).", "S26; S29; SG U6-R16"),
]

FLOWS = {
    "Overactive Bladder Drugs": [
        {"title": "Choosing OAB therapy", "steps": ["Older adult, cognitive impairment, or other anticholinergics?", "Yes → mirabegron (check BP)", "No → antimuscarinic (solifenacin, tolterodine)", "Avoid with narrow-angle glaucoma or retention", "Refractory → combine both mechanisms"], "src": "S13; S15; S17"},
    ],
    "BPH, Erectile Dysfunction & PDE5 Inhibitors": [
        {"title": "ED request: safe to prescribe a PDE5 inhibitor?", "steps": ["Any nitrate (isosorbide, nitroglycerin) or riociguat?", "Yes → do not prescribe; involve cardiology", "On an alpha1 blocker → caution, space doses", "Strong CYP3A4 inhibitor → levels rise", "Counsel: needs sexual stimulation"], "src": "S26; S28; S58"},
    ],
}

CRAM = [
    ("Detrusor contraction", "M3 (Gq → PLC → Ca²⁺)", "S5; S6"),
    ("Storage receptors", "Alpha1 (neck closed) + beta3 (detrusor relaxed)", "S7; S8"),
    ("Antimuscarinic AEs", "Dry mouth, constipation, blurred vision, confusion", "S13"),
    ("Highest CNS burden", "Oxybutynin", "S13; SG U6-R12"),
    ("Mirabegron", "Beta3 agonist; no anticholinergic burden; ↑ BP; CYP2D6 inhibitor", "S15"),
    ("Uroselective alpha1", "Tamsulosin, silodosin", "S21; SG U6-R14"),
    ("Alpha1 blocker AEs", "Orthostatic hypotension, first-dose effect, floppy iris", "S21"),
    ("5-ARI", "3–6 months; PSA halved; pregnant partners avoid crushed tablets", "S23; SG U6-R15"),
    ("PDE5 + nitrate", "Absolute contraindication — profound hypotension", "S26; SG U6-R16"),
    ("Tadalafil", "Longer half-life", "S26"),
    ("Sildenafil", "Blue-tinged vision", "S26"),
]
