import csv
from meeko import MoleculePreparation
from rdkit import Chem
from vina import Vina
from openbabel import pybel
from openbabel import openbabel
import argparse,os,datetime

def convert_pdbqt_to_sdf(pdbqt_file,sdf_file):
    

    # 1. 初始化转换器
    obConversion = openbabel.OBConversion()
    obConversion.SetInAndOutFormats("pdbqt", "sdf")
    
    # 2. 创建分子对象
    mol = openbabel.OBMol()
    
    # 3. 读取文件
    read_ok = obConversion.ReadFile(mol, pdbqt_file)
    if not read_ok:
        print("❌ 读取文件失败")
        return

    # 4. 关键步骤：加氢 (对应命令行中的 -h)
    # AddHydrogens() 会为分子补全所有氢原子（包括非极性氢）
    mol.AddHydrogens()
    
    # 5. 写入文件
    write_ok = obConversion.WriteFile(mol, sdf_file)
    if write_ok:
        print(f"✅ 成功生成带氢 sdf: {sdf_file}")

# 使用示例
#py_obabel_convert_with_h("output.pdbqt", "final_results.pdb")

def run_vina(protein_pdbqt,ligand_pdbqt,output_pdbqt,center,box_size):
    
    # 1. 初始化 Vina 引擎（指定 CPU 核心数和搜索详尽度）
    v = Vina(sf_name='vina', cpu=4)

    # 2. 设置受体和配体
    v.set_receptor(protein_pdbqt)
    v.set_ligand_from_file(ligand_pdbqt)

    # 3. 定义对接盒子 (Center & Size)
    v.compute_vina_maps(center=center, box_size=box_size)

    # 4. 执行对接
    v.dock(exhaustiveness=8, n_poses=9)

    # 5. 输出结果
    v.write_poses(output_pdbqt, n_poses=5, overwrite=True)

    # 6. 获取得分
    energies = v.energies()
    #print(f"最高结合亲和力: {energies[0][0]:.2f} kcal/mol")
    return f"{energies[0][0]:.2f}"

def read_config(config_file,pocket_id=0):
    with open(config_file) as inf:
        reader = list(csv.DictReader(inf))
    row = reader[pocket_id]
    center = [float(row["center_x"]), float(row["center_y"]), float(row["center_z"])]
    box_size = [float(row["size_x"]), float(row["size_y"]), float(row["size_z"])]
    print(center,box_size)
    return center,box_size

def meeko_convert_sdf_to_pdbqt(script, pdbqt_file):
    # 1. 使用 RDKit 读取分子
    #mol = Chem.SDMolSupplier(sdf_file)[0]
    mol = Chem.MolFromMolBlock(script)
    mol = Chem.AddHs(mol) # 记得加氢
    
    # 2. 初始化 Meeko 准备工具
    preparer = MoleculePreparation()
    
    # 3. 准备分子（计算柔性键等）
    preparer.prepare(mol)
    
    # 4. 写入 pdbqt 文件
    preparer.write_pdbqt_file(pdbqt_file)
    #print(f"✅ 转换完成: {pdbqt_file}")

def meeko_convert_pdb_to_pdbqt(pdb_file, pdbqt_file):
    # 1. 使用 RDKit 读取分子
    mol = Chem.MolFromPDBFile(pdb_file, removeHs=False)
    mol = Chem.AddHs(mol, addCoords=True)
    
    # 2. 初始化 Meeko 准备工具
    preparer = MoleculePreparation()
    
    # 3. 准备分子（计算柔性键等）
    preparer.prepare(mol)
    
    # 4. 写入 pdbqt 文件
    preparer.write_pdbqt_file(pdbqt_file)
    #print(f"✅ 转换完成: {pdbqt_file}")

def pybel_convert_to_pdbqt(input_file, output_file, is_receptor=False):
    # 1. 读取分子 (根据扩展名自动识别格式)
    fmt = input_file.split('.')[-1]
    mol = next(pybel.readfile(fmt, input_file))
    
    # 2. 预处理
    mol.addh() # 加氢
    
    # 3. 设置输出格式为 pdbqt
    output = pybel.Outputfile("pdbqt", output_file, overwrite=True)
    
    # 如果是受体，需要添加特殊的选项（类似命令行的 -xr）
    if is_receptor:
        # 在 pybel 中，可以通过这种方式传递选项
        mol.write("pdbqt", output_file, opt={"r": None}, overwrite=True)
    else:
        output.write(mol)
    
    output.close()
    #print(f"✅ 转换成功: {output_file}")

def read_sdf_file(ligand_file):
    arrs = []
    with open(ligand_file) as inf:
        lines = inf.read()
    script_arr = lines.split("$$$$\n")
    print(f"Found {len(script_arr)} molecules in SDF file")
    for idx, script in enumerate(script_arr):
        if len(script) > 10:  # Minimum lines for a valid SDF molecule
            try:
                # Parse standard SDF format
                lines_list = script.strip().split('\n')
                # First line is usually the molecule name/identifier
                mol_name = lines_list[0].strip() if lines_list else f"molecule_{idx+1}"
                
                # Find SMILES in the properties section (after the END of coordinates)
                smiles = None
                for line in lines_list:
                    if line.strip().startswith('> <smiles>'):
                        # SMILES is on the next line
                        smi_idx = lines_list.index(line)
                        if smi_idx + 1 < len(lines_list):
                            smiles = lines_list[smi_idx + 1].strip()
                            break
                
                if not smiles:
                    # Try to use RDKit to read the SDF directly
                    mol = Chem.MolFromMolBlock(script)
                    if mol:
                        smiles = Chem.MolToSmiles(mol)
                
                if smiles:
                    mol = Chem.MolFromMolBlock(script)
                    if mol:
                        # Convert to molblock string
                        molblock = Chem.MolToMolBlock(mol)
                        name = f"ligand_{len(arrs)+1}"
                        arrs.append([name, molblock])
                        print(f"  Successfully parsed molecule {idx}")
                    else:
                        print(f"  Failed to create RDKit molecule from molblock for molecule {idx}")
                else:
                    print(f"  No SMILES found for molecule {idx}")
            except Exception as e:
                print(f"  Error processing molecule {idx}: {e}")
    print(f"Total successfully parsed molecules: {len(arrs)}")
    return arrs

def run():
    parser = argparse.ArgumentParser(description="run docking")
    parser.add_argument("--protein_file", type=str, default="protein.pdb", help="pdb file")
    parser.add_argument("--ligand_file", type=str, default="ligand.sdf", help="ligand file")
    parser.add_argument("--configure_file", type=str, default="pocket.csv", help="configure file")
    parser.add_argument("--results_dir", type=str, default="./Docking", help="output directory")
    args = parser.parse_args()
    protein_file = args.protein_file
    ligand_file = args.ligand_file
    configure_file = args.configure_file
    results_dir = args.results_dir
    os.makedirs(f"{results_dir}/input",exist_ok=True)
    os.makedirs(f"{results_dir}/pdbqt_output",exist_ok=True)
    os.makedirs(f"{results_dir}/output",exist_ok=True)
    rec_pdbqt = f"{results_dir}/receptor.pdbqt"
    pybel_convert_to_pdbqt(protein_file,rec_pdbqt,is_receptor=True)
    center,box_size = read_config(configure_file)

    arrs = read_sdf_file(ligand_file)
    infos = []
    for arr in arrs:
        ligand_pdbqt = f"{results_dir}/input/{arr[0]}.pdbqt"
        output_pdbqt = f"{results_dir}/pdbqt_output/{arr[0]}_docking.pdbqt"
        meeko_convert_sdf_to_pdbqt(arr[1], ligand_pdbqt)
        score = run_vina(rec_pdbqt,ligand_pdbqt,output_pdbqt,center,box_size)
        output_sdf = f"{results_dir}/output/{arr[0]}_docking.sdf"
        convert_pdbqt_to_sdf(output_pdbqt,output_sdf)
        with open(output_sdf) as inf:
            lines = inf.readlines()
        lines[0] = f"{arr[0]}\n"
        lines[-2] = (f"><score>\n")
        lines[-1] = (f"{score}\n")
        scripts = "".join(lines)
        infos.append([score,scripts])
    infos = sorted(infos,key = lambda x:x[0], reverse=True)
    total_scripts = "$$$$\n".join([s[1] for s in infos])
    ligand_name = os.path.basename(ligand_file)
    ligand_base = os.path.splitext(ligand_name)[0]
    total_output_sdf = f"{results_dir}/output/{ligand_base}_docking.sdf"
    with open(total_output_sdf, 'w') as outf:
        outf.write(total_scripts)

if __name__ == "__main__":
    run()






