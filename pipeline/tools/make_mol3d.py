"""One-off: 3D coordinates for the drug-sheet constellation (needs RDKit: pip install rdkit).
Writes work/mol3d.json, which the site build copies to docs/drugs/. Each SMILES is checked against its
molecular formula before use. Biologics, mixtures and foods (heparin, insulin, St. John's wort…) have none.
    python3 pipeline/tools/make_mol3d.py"""
import json
from pathlib import Path

from rdkit import Chem
from rdkit.Chem import AllChem, rdMolDescriptors

# name: (SMILES, expected molecular formula)
S = {
 "Acetaminophen": ("CC(=O)Nc1ccc(O)cc1", "C8H9NO2"),
 "Albuterol": ("CC(C)(C)NCC(O)c1ccc(O)c(CO)c1", "C13H21NO3"),
 "Warfarin": ("CC(=O)CC(c1ccccc1)C1=C(O)c2ccccc2OC1=O", "C19H16O4"),
 "Lithium": ("[Li+].[Li+].[O-]C([O-])=O", "CLi2O3"),
 "Phenytoin": ("O=C1NC(=O)C(N1)(c1ccccc1)c1ccccc1", "C15H12N2O2"),
 "Nitroglycerin": ("C(C(CO[N+](=O)[O-])O[N+](=O)[O-])O[N+](=O)[O-]", "C3H5N3O9"),
 "Propranolol": ("CC(C)NCC(O)COc1cccc2ccccc12", "C16H21NO2"),
 "Metoprolol": ("COCCc1ccc(OCC(O)CNC(C)C)cc1", "C15H25NO3"),
 "Morphine": ("CN1CC[C@]23[C@@H]4[C@H]1CC5=C2C(=C(C=C5)O)O[C@H]3[C@H](C=C4)O", "C17H19NO3"),
 "Codeine": ("CN1CC[C@]23[C@@H]4[C@H]1CC5=C2C(=C(C=C5)OC)O[C@H]3[C@H](C=C4)O", "C18H21NO3"),
 "Clopidogrel": ("COC(=O)[C@H](c1ccccc1Cl)N1CCc2sccc2C1", "C16H16ClNO2S"),
 "Azathioprine": ("Cn1cnc([N+](=O)[O-])c1Sc1ncnc2nc[nH]c12", "C9H7N7O2S"),
 "Allopurinol": ("O=c1[nH]cnc2[nH]ncc12", "C5H4N4O"),
 "Abacavir": ("Nc1nc(NC2CC2)c2ncn([C@@H]3C[C@H](CO)C=C3)c2n1", "C14H18N6O"),
 "Aspirin": ("CC(=O)Oc1ccccc1C(=O)O", "C9H8O4"),
 "Theophylline": ("Cn1c(=O)c2[nH]cnc2n(C)c1=O", "C7H8N4O2"),
 "Phenoxybenzamine": ("CC(COc1ccccc1)N(CCCl)Cc1ccccc1", "C18H22ClNO"),
 "Ketoconazole": ("CC(=O)N1CCN(CC1)c1ccc(OC[C@H]2CO[C@](Cn3ccnc3)(O2)c2ccc(Cl)cc2Cl)cc1", "C26H28Cl2N4O4"),
 "Ritonavir": ("CC(C)c1nc(CN(C)C(=O)N[C@@H](C(C)C)C(=O)N[C@@H](Cc2ccccc2)C[C@H](O)[C@H](Cc2ccccc2)NC(=O)OCc2cncs2)cs1", "C37H48N6O5S2"),
 "N-acetylcysteine": ("CC(=O)N[C@@H](CS)C(=O)O", "C5H9NO3S"),
 "Thalidomide": ("O=C1CCC(N2C(=O)c3ccccc3C2=O)C(=O)N1", "C13H10N2O4"),
 "Isoniazid": ("NNC(=O)c1ccncc1", "C6H7N3O"),
 "Digoxin": ("C[C@@H]1O[C@H](C[C@H](O)[C@@H]1O[C@H]1C[C@H](O)[C@H](O[C@H]2C[C@H](O)[C@H](O)[C@@H](C)O2)[C@@H](C)O1)O[C@H]1CC[C@@]2(C)[C@H](CC[C@@H]3[C@@H]2C[C@@H](O)[C@]2(C)[C@H](CC[C@]32O)C2=CC(=O)OC2)C1", "C41H64O14"),
}


def coords(smi):
    m = Chem.AddHs(Chem.MolFromSmiles(smi))
    AllChem.EmbedMolecule(m, randomSeed=7)
    AllChem.MMFFOptimizeMolecule(m)
    m = Chem.RemoveHs(m)
    pos = m.GetConformer().GetPositions()
    pos -= pos.mean(axis=0)
    return {"a": [[a.GetSymbol(), *(round(float(v), 2) for v in pos[a.GetIdx()])] for a in m.GetAtoms()],
            "b": [[b.GetBeginAtomIdx(), b.GetEndAtomIdx(), 2 if b.GetBondTypeAsDouble() == 2 else 1] for b in m.GetBonds()]}


if __name__ == "__main__":
    out = {}
    for name, (smi, formula) in S.items():
        got = rdMolDescriptors.CalcMolFormula(Chem.MolFromSmiles(smi)).replace("+2", "").replace("-2", "")
        assert got == formula, f"{name}: {got} != {formula}"
        out[name] = {"f": formula, **coords(smi)}
    p = Path(__file__).resolve().parents[2] / "work" / "mol3d.json"
    p.write_text(json.dumps(out, separators=(",", ":")))
    print(f"{len(out)} structures -> {p} ({p.stat().st_size // 1024} KB)")
