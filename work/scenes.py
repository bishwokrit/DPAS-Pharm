"""Physiology scenes: picture-first interactive versions of lecture figures (site_src/assets/scenes.js).
SCENES[lecture][image] replaces that figure's "viz". Notes carry the lecture's facts and citations; the drawings are
illustrative (outside knowledge is used only to design the picture, never to add facts)."""

EMESIS_NOTES = {
    "ond": "Blocks 5-HT3 on gut vagal afferents and in the CTZ — the serotonin released from damaged enterochromaffin cells can't fire the signal. Give before chemo; QT prolongation, constipation, headache. (S30–S31)",
    "meto": "Blocks D2 in the CTZ (less nausea); in the gut, D2 blockade plus 5-HT4 agonism release more acetylcholine — faster gastric emptying. Boxed warning: tardive dyskinesia — avoid beyond 12 weeks. (S36–S37)",
    "pro": "Blocks dopamine (D2) at the chemoreceptor trigger zone. (S30)",
    "apr": "Blocks substance P / neurokinin (NK1) at the CTZ. For chemotherapy, combine classes with different targets: 5-HT3 + NK1 antagonists + dexamethasone. (S30; S32)",
    "mec": "Antihistamine: blocks the histamine/acetylcholine signal from the vestibular system — the motion-sickness pathway. (S30; S33)",
    "sco": "Anticholinergic: blocks the vestibular input. Patch behind the ear at least 4 hours before travel. (S30; S67)",
    "dro": "Synthetic cannabinoid: activates CB1 in the vomiting center and CTZ, reducing neurotransmitter release — a third pathway, for refractory chemotherapy nausea; also stimulates appetite. Dizziness, euphoria/dysphoria, tachycardia. (S38–S39)",
    "bzd": "Benzodiazepines (and cannabinoids) quiet the higher cortical input — anxiety and anticipatory nausea. (S32)",
}

SEESAW_MUCOSA = {
    "type": "seesaw", "title": "Mucosal balance",
    "point": "Ulcers, GERD and gastritis appear when aggressive factors win or defenses fall. Add the factors and drugs — watch the balance tip.",
    "left": {"title": "Aggressive factors", "items": [{"id": "acid", "label": "Gastric acid (HCl)", "w": 2}, {"id": "pep", "label": "Pepsin", "w": 1}]},
    "right": {"title": "Mucosal defense", "items": [{"id": "muc", "label": "Mucus–bicarbonate", "w": 1.5}, {"id": "pg", "label": "Prostaglandins", "w": 1.5}, {"id": "epi", "label": "Epithelial turnover", "w": 1}]},
    "drugs": [
        {"id": "hp", "label": "H. pylori infection", "col": "var(--vz-2)", "side": "L", "add": "H. pylori (ammonia)", "w": 1.5,
         "note": "H. pylori urease makes ammonia, which injures the mucosa. (S5–S6)"},
        {"id": "nsaid", "label": "NSAID use", "col": "var(--vz-2)", "side": "L", "add": "NSAIDs", "w": 1, "remove": ["pg"],
         "note": "NSAIDs block COX-1 prostaglandins — the prostaglandin weight falls off the defense side. (S5–S6)"},
        {"id": "miso", "label": "Misoprostol", "col": "var(--vz-1)", "side": "R", "add": "Misoprostol (PGE1)", "w": 1.5,
         "note": "A PGE1 analog: puts back the prostaglandin tone NSAIDs remove — used to prevent NSAID ulcers. Contraindicated in pregnancy; diarrhea is common. (S20–S21)"},
        {"id": "suc", "label": "Sucralfate", "col": "var(--vz-1)", "side": "R", "add": "Sucralfate barrier", "w": 1.5,
         "note": "In acid (pH below 4) it polymerizes and binds the ulcer base — a physical shield. Needs acid, so take it on an empty stomach, separated from antacids/PPIs. (S20–S21)"},
        {"id": "ppi", "label": "PPI or H2 blocker", "col": "var(--vz-4)", "scale": [["acid", 0.35]],
         "note": "Less acid on the aggressive side. (S8; S13–S16)"},
    ],
    "verdict": {"left": "Tipped toward injury → GERD, ulcer or gastritis (S6)", "right": "Defenses hold the line.", "even": "Balanced."},
    "steps": [{"label": "NSAID use", "on": ["nsaid"]}, {"label": "NSAID + misoprostol", "on": ["nsaid", "miso"]},
              {"label": "H. pylori + NSAID", "on": ["hp", "nsaid"]}, {"label": "Ulcer: sucralfate + PPI", "on": ["hp", "suc", "ppi"]}],
    "read": "Tap a factor or a drug to put it on the scale.",
}

SCENES = {
    "L05": {
        "S8_1.jpg": {"type": "parietal"},
        "S14_1.jpg": {"type": "parietal", "drugs": [{"id": "fam", "label": "Famotidine"}, {"id": "cim", "label": "Cimetidine"}, {"id": "ppi", "label": "Omeprazole (PPI)"}],
                      "point": "ECL cells release histamine onto the H2 receptor. Block it — but watch what acetylcholine and gastrin still do.",
                      "steps": [{"label": "A meal", "mode": "meal"}, {"label": "Famotidine", "mode": "meal", "on": ["fam"]}, {"label": "Compare: omeprazole", "mode": "meal", "on": ["ppi"]}]},
        "S16_1.jpg": {"type": "parietal", "drugs": [{"id": "ppi", "label": "Omeprazole (PPI)"}, {"id": "fam", "label": "Famotidine"}], "mode": "fast",
                      "point": "A PPI locks only pumps that are switched on. Dose it while fasting, then eat — or before the meal — and compare.",
                      "steps": [{"label": "PPI while fasting", "mode": "fast", "on": ["ppi"]}, {"label": "PPI before a meal", "mode": "meal", "on": ["ppi"]}]},
        "S21_1.jpg": SEESAW_MUCOSA,
        "S24_1.jpg": {"type": "hpylori"},
        "S31_1.jpg": {"type": "emesis", "drugs": ["ond", "mec"], "causes": ["chemo", "motion"], "notes": EMESIS_NOTES,
                      "point": "Chemotherapy damages enterochromaffin cells in the gut; their serotonin fires 5-HT3 receptors on the vagus and in the CTZ, which signal the vomiting center.",
                      "steps": [{"label": "Chemo + ondansetron", "mode": "chemo", "on": ["ond"]}, {"label": "Motion + ondansetron?", "mode": "motion", "on": ["ond"]}],
                      "read": "Drag ondansetron onto the gut or brain."},
        "S32_1.jpg": {"type": "emesis", "drugs": ["ond", "pro", "apr", "mec", "sco", "dro", "bzd"], "notes": EMESIS_NOTES,
                      "steps": [{"label": "Chemo: 5-HT3 + NK1", "mode": "chemo", "on": ["ond", "apr"]}, {"label": "Motion: meclizine", "mode": "motion", "on": ["mec"]}, {"label": "Anticipatory", "mode": "anx", "on": ["bzd"]}],
                      "read": "Pick a cause, then add drugs. Match the drug to the input that's firing."},
        "S33_1.jpg": {"type": "emesis", "drugs": ["ond", "meto", "pro", "apr", "mec", "sco"], "mode": "motion", "causes": ["motion", "chemo"], "notes": EMESIS_NOTES,
                      "point": "Motion sickness is vestibular. Try a chemo drug on it — then the right one.",
                      "steps": [{"label": "Motion + ondansetron", "mode": "motion", "on": ["ond"]}, {"label": "Motion + scopolamine", "mode": "motion", "on": ["sco"]}, {"label": "Chemo: three CTZ blockers", "mode": "chemo", "on": ["ond", "apr", "pro"]}],
                      "read": "Motion sickness: the signal comes from the inner ear."},
        "S37_1.jpg": {"type": "emesis", "drugs": ["meto", "ond"], "causes": ["chemo"], "notes": EMESIS_NOTES,
                      "point": "Metoclopramide does two jobs: blocks D2 in the CTZ (antiemetic) and speeds the stomach (prokinetic). Watch the food in the stomach.",
                      "steps": [{"label": "Metoclopramide", "mode": "chemo", "on": ["meto"]}, {"label": "Add ondansetron", "mode": "chemo", "on": ["meto", "ond"]}],
                      "read": "Drag metoclopramide onto the brain or stomach."},
        "S38_1.jpg": {"type": "emesis", "drugs": ["ond", "apr", "dro"], "causes": ["chemo"], "notes": EMESIS_NOTES,
                      "point": "Cannabinoids work through a third pathway — CB1 in the vomiting center — so they help when standard antiemetics fall short.",
                      "steps": [{"label": "Standard: 5-HT3 + NK1", "mode": "chemo", "on": ["ond", "apr"]}, {"label": "Add dronabinol", "mode": "chemo", "on": ["ond", "apr", "dro"]}],
                      "read": "Start with the standard drugs, then add dronabinol."},
        "S39_1.jpg": {"type": "emesis", "drugs": ["dro", "bzd", "ond"], "causes": ["chemo", "anx"], "notes": EMESIS_NOTES,
                      "point": "Dronabinol or nabilone binds CB1 on neurons in the vomiting center and CTZ, turning down neurotransmitter release.",
                      "steps": [{"label": "Dronabinol", "mode": "chemo", "on": ["dro"]}, {"label": "Anticipatory nausea", "mode": "anx", "on": ["bzd"]}],
                      "read": "Drag dronabinol onto the vomiting center."},
    },
}
