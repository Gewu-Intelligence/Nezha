import sys,os
from rdkit import Chem

from rdkit.Chem import AllChem
from dimorphite_dl import protonate_smiles
from pathlib import Path
import argparse

def ligand_prepare(m,m_name=None):
    _smiles = Chem.MolToSmiles(m)
    smiles = AllChem.CanonSmiles(_smiles)
    protonated_smiles = protonate_smiles(smiles,ph_min=7.4,ph_max=7.4)
    
    m = Chem.MolFromSmiles(protonated_smiles[0])

    rdkmh = Chem.AddHs(m)
    AllChem.EmbedMolecule(rdkmh)
    
    inchi = Chem.inchi.MolToInchi(rdkmh)
    inchi_key = Chem.inchi.InchiToInchiKey(inchi)
    _scripts = Chem.MolToMolBlock(rdkmh)
    scripts = _scripts.split("\n")
    if m_name is None:
        m_name = inchi_key
    scripts[0] = f"{m_name}"
    scripts.append("> <smiles>")
    scripts.append(f"{protonated_smiles[0]}")
    scripts.append("> <origin_smiles>")
    if len(protonated_smiles) > 1:
        scripts.append(f"{protonated_smiles[1]}")
    else:
        scripts.append(f"{protonated_smiles[0]}")
    scripts.append("> <inchi_key>")
    scripts.append(f"{inchi_key}")
    scripts.append(f"\n")

    return "\n".join(scripts)

def run(fs,output_dir):
    parser = argparse.ArgumentParser(description='ligands文件')
    parser.add_argument('ligand_file', help='ligand文件')
    parser.add_argument('--output_dir', default='ligand_prepare', 
                       help='输出文件夹 (默认: ligand_prepare)')
    args = parser.parse_args()

    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    print(f"输出文件夹: {output_dir}")
    fs = args.ligand_file
    scripts = []
    if fs[-4:] == ".sdf":
        with open(fs) as inf:
            lines = inf.read()
        script_arr = lines.split("$$$$\n")
        for script in script_arr:
            if len(script) > 0:
                m_name = script.split("\n")[0].strip()
                m = Chem.MolFromMolBlock(script)
                scripts.append(ligand_prepare(m,m_name=m_name))
    elif fs[-4:] == ".mol":
        with open(fs) as inf:
            lines = inf.readlines()
        m_name = lines[0].strip()
        m = Chem.MolFromMolBlock("".join(lines))
        scripts.append(ligand_prepare(m,m_name=m_name))
    elif fs[-4:] == ".txt":
        with open(fs) as inf:
            lines = inf.readlines()
        for ss in lines:
            m = Chem.MolFromSmiles(ss.strip())
            scripts.append(ligand_prepare(m))
    else:
        m = Chem.MolFromSmiles(fs)
        scripts.append(ligand_prepare(m))
    total_scripts = "$$$$\n".join(scripts)

    with open(f"{output_dir}/ligands.sdf",'w') as outf:
        outf.write(total_scripts)

if __name__ == "__main__":
    fs = sys.argv[1]
    output_dir = "./"
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    run(fs,output_dir)


