"""Study-guide extras for L11 (summary, flows, cram sheet). Imported by author_L11.py."""

TEASER = "Today: estrogens and progestins and why they travel together, contraception choices when estrogen is off the table, SERMs versus aromatase inhibitors, androgen drugs, and PCOS as a metabolic problem treated with metformin."

SUMMARY = [
    ("**Estrogens** bind ER-α/β (VTE risk with smoking, age > 35); **unopposed estrogen** with a uterus → endometrial cancer, so add a **progestin**.", "S5; S6; SG U6-R1; SG U6-R2"),
    ("Estrogen contraindicated (VTE, smoker > 35, migraine with aura) → **progestin-only** is the right first choice; **DMPA** = reversible bone loss.", "S9; SG U6-R3; SG U6-R4"),
    ("**SERMs**: tamoxifen blocks breast but stimulates endometrium (new bleeding → evaluate); raloxifene is endometrium-neutral; both raise VTE.", "S11; S18; SG U6-R5"),
    ("**Aromatase inhibitors** block peripheral estrogen synthesis — **postmenopausal only**; bone loss and joint pain.", "S13; S14; SG U6-R6"),
    ("**Testosterone**: erythrocytosis (hematocrit), PSA; **antiandrogens** block the receptor; **5-ARIs** block DHT formation.", "S15; S16; SG U6-R7; SG U6-R8"),
    ("**PCOS**: hyperinsulinemia ↑ ovarian androgens and ↓ SHBG; **metformin** works indirectly and is usually combined with contraception.", "S20; S22; S25; SG U6-R9; SG U6-R10"),
]

FLOWS = {
    "Estrogens, Progestins & Contraception": [
        {"title": "Choosing hormonal contraception", "steps": ["Screen: VTE/stroke history, smoker > 35, migraine with aura, estrogen-sensitive cancer, uncontrolled HTN", "Any present → progestin-only (mini-pill, DMPA, implant, LNG IUD)", "None → combined pill, patch or ring (cycle control, acne)", "On rifampin or other inducers → backup method"], "src": "S5; S9; S45"},
    ],
    "SERMs, Aromatase Inhibitors & Androgens": [
        {"title": "Reducing estrogen signaling in breast cancer", "steps": ["ER-positive breast cancer", "Premenopausal → tamoxifen (AI alone insufficient)", "Postmenopausal → aromatase inhibitor or tamoxifen", "Tamoxifen + new bleeding → gynecologic evaluation", "AI → protect bone (calcium, vitamin D, bisphosphonate)"], "src": "S11; S14; S18; S45"},
    ],
    "PCOS & the Reproductive-Metabolic Overlap": [
        {"title": "PCOS loop", "steps": ["Insulin resistance → high insulin", "Ovarian androgens up; liver SHBG down", "Free testosterone up: hirsutism, anovulation", "Metformin lowers insulin → androgens fall", "Add combined contraception for cycles and hirsutism"], "src": "S23; S25"},
    ],
}

CRAM = [
    ("Estrogen mechanism", "ER-α/ER-β → gene transcription", "S5"),
    ("Estrogen top AE", "VTE (smoking, age > 35)", "S5"),
    ("Uterus + estrogen", "Always add a progestin", "S6; S7"),
    ("Progestin-only methods", "Mini-pill, DMPA, implant, LNG IUD — no estrogen VTE risk", "S6; S9"),
    ("DMPA", "Reversible bone density loss", "S6; S9"),
    ("Tamoxifen", "Breast −, bone +, endometrium + (cancer); CYP2D6", "S11; S45"),
    ("Raloxifene", "Breast −, bone +, endometrium neutral; VTE", "S11"),
    ("Aromatase inhibitors", "Postmenopausal only; bone loss, joint pain", "S14"),
    ("Testosterone", "Hematocrit, PSA; oral hepatotoxicity", "S15"),
    ("Flutamide/bicalutamide vs finasteride", "Receptor block vs DHT synthesis block", "S16"),
    ("PCOS core", "Hyperinsulinemia ↑ theca androgens, ↓ SHBG", "S20"),
    ("Metformin in PCOS", "Indirect; GI upset; hold for contrast", "S22; S23"),
    ("Spironolactone in PCOS", "Androgen receptor block; avoid in pregnancy", "S15; S24"),
]
