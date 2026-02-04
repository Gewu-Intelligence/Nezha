#!/usr/bin/env python3
import os
import sys
import subprocess
import shutil
from Bio.PDB import PDBParser, PDBIO, Select
from rdkit import Chem

GMX_CMD = None
for _gmx_cmd in ["gmx","gmx_mpi"]:
    if shutil.which(_gmx_cmd):
        GMX_CMD = _gmx_cmd
        break
if GMX_CMD is None:
    sys.exit("没有找到gromacs")

print(f"运行命令：{GMX_CMD}")

METAL_IONS = {"ZN","MG","NA","K","CA","MN","FE","CU","CO","NI","CD","HG"}

# ================== 选择A链蛋白 ==================
class ChainAProteinSelect(Select):
    def accept_chain(self, chain):
        return chain.id == "A"

    def accept_residue(self, residue):
        return residue.id[0] == " "  # 只保留标准氨基酸


def extract_chainA_protein(input_pdb, output_pdb):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("X", input_pdb)

    io = PDBIO()
    io.set_structure(structure)
    io.save(output_pdb, ChainAProteinSelect())

    print(f"✔ Protein chain A extracted → {output_pdb}")


# ================== 提取A链小分子 ==================
def extract_ligands(input_pdb, output_sdf):
    lig_blocks = []
    current_block = []
    current_res = None

    with open(input_pdb) as f:
        for line in f:
            if line.startswith("HETATM"):
                chain_id = line[21].strip()
                resname = line[17:20].strip()
                resseq = line[22:26].strip()

                if chain_id != "A":
                    continue
                if resname in METAL_IONS or resname in {"HOH", "WAT"}:
                    continue

                res_id = (resname, resseq)

                if current_res is None:
                    current_res = res_id

                if res_id != current_res:
                    lig_blocks.append(current_block)
                    current_block = []
                    current_res = res_id

                current_block.append(line)

        if current_block:
            lig_blocks.append(current_block)

    writer = Chem.SDWriter(output_sdf)
    count = 0

    for block in lig_blocks:
        pdb_block = "HEADER    LIGAND\n" + "".join(block) + "END\n"
        mol = Chem.MolFromPDBBlock(pdb_block, removeHs=False)
        if mol:
            Chem.SanitizeMol(mol, catchErrors=True)
            writer.write(mol)
            count += 1

    writer.close()
    print(f"✔ Extracted {count} ligand(s) → {output_sdf}")


# ================== sed 修正命名 ==================
def fix_pdb_naming(pdb_file):
    sed_cmd = r"""sed -i 's/CD  I/CD1 I/g; s/OC1/O  /g; s/OC2/OXT/g' {}""".format(pdb_file)
    subprocess.run(sed_cmd, shell=True, check=True)
    print("✔ PDB atom naming fixed (ILE CD → CD1, OC1/OC2 fix)")


# ================== 运行 pdb2gmx ==================
def run_pdb2gmx(input_pdb, out_dir):
    cmd = f"""

    {GMX_CMD} pdb2gmx -f {input_pdb} -o {out_dir}/processed.pdb -water tip3p -ignh -ff amber99sb-ildn
    """

    subprocess.run(f"bash -c '{cmd}'", shell=True, check=True)
    print("✔ pdb2gmx finished → topology + processed.gro generated")


# ================== 主程序 ==================
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python prepare_chainA_md.py input.pdb output_dir")
        sys.exit(1)

    input_pdb = sys.argv[1]
    output_dir = sys.argv[2]
    os.makedirs(output_dir, exist_ok=True)

    protein_pdb = os.path.join(output_dir, "protein_A_apo.pdb")
    ligand_sdf = os.path.join(output_dir, "ligands_A.sdf")

    extract_chainA_protein(input_pdb, protein_pdb)
    extract_ligands(input_pdb, ligand_sdf)
    #fix_pdb_naming(protein_pdb)
    run_pdb2gmx(protein_pdb, output_dir)

    print("\n🎉 ALL DONE")
    print("Protein PDB :", protein_pdb)
    print("Ligand SDF  :", ligand_sdf)
    print("MD Structure:", os.path.join(output_dir, "processed.gro"))
