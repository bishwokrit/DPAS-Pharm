"""Comprehensive final mock — 100 questions drawn from every unit's practice-exam bank (about 17 per unit),
spread across each unit's topics. Questions are copied, so the unit exams are untouched."""
import copy
import importlib.util
import random
from pathlib import Path

HERE = Path(__file__).resolve().parent
PER_UNIT = {"U1": 9, "U1B": 8, "U2": 17, "U3": 17, "U4": 17, "U5": 16, "U6": 16}
NAMES = {"U1": "Unit 1", "U1B": "Unit 1", "U2": "Unit 2", "U3": "Unit 3", "U4": "Unit 4", "U5": "Unit 5", "U6": "Unit 6"}


def _unit_bank(uid):
    d = HERE.parent / uid
    out = []
    for f in sorted(d.glob("bank*.py")):
        import sys
        sys.path.insert(0, str(d))
        spec = importlib.util.spec_from_file_location(f"final_{uid}_{f.stem}", f)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        sys.path.remove(str(d))
        for k in ("bank_a", "bank_b", "bank_c"):
            sys.modules.pop(k, None)
        out += [q for name in sorted(vars(mod)) if name.startswith("BANK_") for q in getattr(mod, name)]
    return out


def _pick(bank, n, rng):
    """Round-robin across topics so every topic in the unit is represented."""
    by = {}
    for q in bank:
        by.setdefault(q["topic"], []).append(q)
    for v in by.values():
        rng.shuffle(v)
    topics = sorted(by)
    rng.shuffle(topics)
    out = []
    while len(out) < n and any(by.values()):
        for t in topics:
            if by[t] and len(out) < n:
                out.append(by[t].pop())
    return out


rng = random.Random(1211)
BANK_FINAL = []
for uid, n in PER_UNIT.items():
    for q in _pick(_unit_bank(uid), n, rng):
        q = copy.deepcopy(q)
        q["topic"] = NAMES[uid]
        BANK_FINAL.append(q)
