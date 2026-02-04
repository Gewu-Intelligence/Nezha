#!/usr/bin/env python3
import os
import subprocess
import argparse
import sys
import shutil
from pathlib import Path
GMX_CMD = None
for _gmx_cmd in ["gmx","gmx_mpi"]:
    if shutil.which(_gmx_cmd):
        GMX_CMD = _gmx_cmd
        break
if GMX_CMD is None:
    sys.exit("没有找到gromacs")

print(f"运行命令：{GMX_CMD}")


def run_gromacs_command(cmd, description):
    """运行GROMACS命令并处理错误"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, 
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True)
        print(f"{description} 成功完成")
        return True
    except subprocess.CalledProcessError as e:
        print(f"{description} 失败:")
        print(f"错误信息: {e.stderr}")
        return False

def check_gromacs():
    """检查GROMACS是否安装"""
    try:
        result = subprocess.run("{GMX_CMD} --version", shell=True, check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              text=True)
        print(f"GROMACS已安装:\n{result.stdout}")
        return True
    except subprocess.CalledProcessError:
        print("错误: GROMACS未安装或不在PATH中")
        print("请先安装GROMACS: http://www.gromacs.org/")
        return False

def pdb2gmx(pdb_file, forcefield="amber99sb-ildn", water="tip3p", output_prefix="processed"):
    """使用pdb2gmx生成拓扑和坐标文件"""
    cmd = f"{GMX_CMD} pdb2gmx -f {pdb_file} -o {output_prefix}.gro -p {output_prefix}.top -water {water} -ff {forcefield}"
    return run_gromacs_command(cmd, "生成拓扑和坐标文件 (pdb2gmx)")

def editconf(gro_file, output_file="boxed.gro", d=1.0, bt="dodecahedron"):
    """定义模拟盒子"""
    cmd = f"{GMX_CMD} editconf -f {gro_file} -o {output_file} -c -d {d} -bt {bt}"
    return run_gromacs_command(cmd, "定义模拟盒子 (editconf)")

def solvate(gro_file="boxed.gro", top_file="processed.top", output="solvated.gro"):
    """添加水分子"""
    cmd = f"{GMX_CMD} solvate -cp {gro_file} -cs spc216.gro -o {output} -p {top_file}"
    return run_gromacs_command(cmd, "添加水分子 (solvate)")

def generate_ions(gro_file="solvated.gro", top_file="processed.top", 
                  output="ions.tpr", concentration=0.15, pname="NA", nname="CL"):
    """添加离子以中和电荷"""
    cmd1 = f"{GMX_CMD} grompp -f ions.mdp -c {gro_file} -p {top_file} -o {output}"
    if not run_gromacs_command(cmd1, "生成tpr文件 (grompp - ions)"):
        return False
    
    cmd2 = f"echo 13 | {GMX_CMD} genion -s {output} -o {gro_file} -p {top_file} -pname {pname} -nname {nname} -conc {concentration}"
    return run_gromacs_command(cmd2, "添加离子 (genion)")

def create_minimization_mdp(mdp_file="minimization.mdp"):
    """创建能量最小化的mdp文件"""
    content = """; energy minimization parameters
integrator  = steep
nsteps      = 50000

emtol       = 1000
emstep      = 0.01

nstlist         = 1
cutoff-scheme   = Verlet
ns_type         = grid
rlist           = 1.2
coulombtype     = PME
rcoulomb        = 1.2
rvdw            = 1.2
pbc             = xyz

constraints     = none
"""
    with open(mdp_file, 'w') as f:
        f.write(content)
    print(f"创建能量最小化mdp文件: {mdp_file}")
    return True

def create_equilibration_mdp(mdp_file="nvt.mdp", ensemble="nvt"):
    """创建NVT/NPT平衡的mdp文件"""
    if ensemble == "nvt":
        content = """; NVT equilibration
integrator  = md
nsteps      = 50000
dt          = 0.002

nstxout     = 5000
nstvout     = 5000
nstenergy   = 1000
nstlog      = 1000

nstlist         = 10
cutoff-scheme   = Verlet
ns_type         = grid
rlist           = 1.2
coulombtype     = PME
rcoulomb        = 1.2
rvdw            = 1.2
pbc             = xyz

tcoupl         = V-rescale
tc-grps        = Protein Non-Protein
tau_t          = 0.1     0.1
ref_t          = 300     300

constraints    = h-bonds
constraint_algorithm = LINCS
"""
    else:
        content = """; NPT equilibration
integrator  = md
nsteps      = 50000
dt          = 0.002

nstxout     = 5000
nstvout     = 5000
nstenergy   = 1000
nstlog      = 1000

nstlist         = 10
cutoff-scheme   = Verlet
ns_type         = grid
rlist           = 1.2
coulombtype     = PME
rcoulomb        = 1.2
rvdw            = 1.2
pbc             = xyz

tcoupl         = V-rescale
tc-grps        = Protein Non-Protein
tau_t          = 0.1     0.1
ref_t          = 300     300

pcoupl         = Parrinello-Rahman
pcoupltype     = isotropic
tau_p          = 2.0
compressibility = 4.5e-5
ref_p          = 1.0

constraints    = h-bonds
constraint_algorithm = LINCS
"""
    with open(mdp_file, 'w') as f:
        f.write(content)
    print(f"创建{ensemble.upper()}平衡mdp文件: {mdp_file}")
    return True

def create_production_mdp(mdp_file="md.mdp", time=100000):
    """创建生产模拟的mdp文件"""
    content = f"""; production MD
integrator  = md
nsteps      = {time}
dt          = 0.002

nstxout     = 5000
nstvout     = 5000
nstenergy   = 1000
nstlog      = 1000
nstxout-compressed  = 5000
compressed-x-precision = 1000

nstlist         = 10
cutoff-scheme   = Verlet
ns_type         = grid
rlist           = 1.2
coulombtype     = PME
rcoulomb        = 1.2
rvdw            = 1.2
pbc             = xyz

tcoupl         = V-rescale
tc-grps        = Protein Non-Protein
tau_t          = 0.1     0.1
ref_t          = 300     300

pcoupl         = Parrinello-Rahman
pcoupltype     = isotropic
tau_p          = 2.0
compressibility = 4.5e-5
ref_p          = 1.0

constraints    = h-bonds
constraint_algorithm = LINCS
"""
    with open(mdp_file, 'w') as f:
        f.write(content)
    print(f"创建生产模拟mdp文件: {mdp_file}")
    return True

def create_ions_mdp(mdp_file="ions.mdp"):
    """创建添加离子的mdp文件"""
    content = """; parameters for genion
integrator  = md
nsteps      = 1
nstlist     = 1
ns_type     = grid
rlist       = 1.2
coulombtype = PME
rcoulomb    = 1.2
rvdw        = 1.2
"""
    with open(mdp_file, 'w') as f:
        f.write(content)
    print(f"创建离子mdp文件: {mdp_file}")
    return True

def grompp(mdp_file, gro_file, top_file, output, maxwarn=0):
    """预处理生成tpr文件"""
    cmd = f"{GMX_CMD} grompp -f {mdp_file} -c {gro_file} -p {top_file} -o {output} -maxwarn {maxwarn}"
    return run_gromacs_command(cmd, f"预处理生成tpr文件 ({mdp_file})")

def mdrun(tpr_file, output="md"):
    """运行MD模拟"""
    cmd = f"{GMX_CMD} mdrun -deffnm {output} -s {tpr_file} -ntomp 4"
    return run_gromacs_command(cmd, f"运行MD模拟 ({output})")

def generate_bash_script(output_dir, args):
    """生成可执行的bash脚本"""
    pdb_name = Path(args.pdb_file).stem
    bash_script_path = os.path.join(output_dir, f"{pdb_name}_md_simulation.sh")
    
    content = f"""#!/bin/bash

# GROMACS MD Simulation Script
# Generated for: {args.pdb_file}
# Output directory: {output_dir}
# Date: {os.popen('date').read().strip()}

set -e

echo "========================================"
echo "GROMACS MD Simulation Script"
echo "========================================"

# Check GROMACS installation
if ! command -v {GMX_CMD} &> /dev/null; then
    echo "Error: GROMACS not found. Please install GROMACS first."
    exit 1
fi

# Parameters
PDB_FILE="{pdb_name}.pdb"
FORCEFIELD="{args.forcefield}"
WATER_MODEL="{args.water}"
BOX_TYPE="{args.box_type}"
BOX_DISTANCE={args.box_distance}
ION_CONC={args.ion_conc}
OUTPUT_PREFIX="processed"

# Change to output directory
cd "$(dirname "$0")"

echo ""
echo "Step 1: Generate topology and coordinate files..."
{GMX_CMD} pdb2gmx -f $PDB_FILE -o $OUTPUT_PREFIX.gro -p $OUTPUT_PREFIX.top -water $WATER_MODEL -ff $FORCEFIELD

echo ""
echo "Step 2: Define simulation box..."
{GMX_CMD} editconf -f $OUTPUT_PREFIX.gro -o boxed.gro -c -d $BOX_DISTANCE -bt $BOX_TYPE

echo ""
echo "Step 3: Add water molecules..."
{GMX_CMD} solvate -cp boxed.gro -cs spc216.gro -o solvated.gro -p $OUTPUT_PREFIX.top

echo ""
echo "Step 4: Add ions..."
{GMX_CMD} grompp -f ions.mdp -c solvated.gro -p $OUTPUT_PREFIX.top -o ions.tpr
echo "13" | {GMX_CMD} genion -s ions.tpr -o solvated.gro -p $OUTPUT_PREFIX.top -pname NA -nname CL -conc $ION_CONC

echo ""
echo "Step 5: Energy minimization..."
{GMX_CMD} grompp -f minimization.mdp -c solvated.gro -p $OUTPUT_PREFIX.top -o em.tpr
{GMX_CMD} mdrun -deffnm em -s em.tpr -ntomp 4

"""
    
    if args.with_equilibration:
        content += f"""echo ""
echo "Step 6: NVT equilibration..."
{GMX_CMD} grompp -f nvt.mdp -c em.gro -p processed.top -o nvt.tpr -maxwarn 1
{GMX_CMD} mdrun -deffnm nvt -s nvt.tpr -ntomp 4

echo ""
echo "Step 7: NPT equilibration..."
{GMX_CMD} grompp -f npt.mdp -c nvt.gro -p processed.top -o npt.tpr -maxwarn 1
{GMX_CMD} mdrun -deffnm npt -s npt.tpr -ntomp 4

PRODUCTION_GRO="npt.gro"
"""
    else:
        content += 'PRODUCTION_GRO="em.gro"\n'
    
    content += f"""
echo ""
echo "Step 8: Production MD simulation..."
{GMX_CMD} grompp -f md.mdp -c $PRODUCTION_GRO -p processed.top -o md.tpr
{GMX_CMD} mdrun -deffnm md -s md.tpr -ntomp 4

echo ""
echo "========================================"
echo "MD simulation completed successfully!"
echo "========================================"
echo ""
echo "Generated files:"
echo "  - Trajectory: md.xtc"
echo "  - Energy: md.edr"
echo "  - Log: md.log"
echo "  - Final coordinates: md.gro"
echo ""
echo "Analysis commands:"
echo "  {GMX_CMD} energy -f md.edr"
echo "  {GMX_CMD} view -f md.xtc"
"""
    
    with open(bash_script_path, 'w') as f:
        f.write(content)
    
    os.chmod(bash_script_path, 0o755)
    print(f"\n生成bash脚本: {bash_script_path}")
    return bash_script_path

def main():
    parser = argparse.ArgumentParser(description='从PDB文件生成GROMACS输入文件和bash脚本')
    parser.add_argument('pdb_file', help='输入的PDB文件')
    parser.add_argument('--output-dir', default='md_output', 
                       help='输出文件夹 (默认: md_output)')
    parser.add_argument('--forcefield', default='amber99sb-ildn', 
                       help='力场 (默认: amber99sb-ildn)')
    parser.add_argument('--water', default='tip3p', 
                       help='水模型 (默认: tip3p)')
    parser.add_argument('--box-type', default='dodecahedron', 
                       help='盒子类型 (默认: dodecahedron)')
    parser.add_argument('--box-distance', type=float, default=1.0, 
                       help='盒子边缘距离 (默认: 1.0 nm)')
    parser.add_argument('--ion-conc', type=float, default=0.15, 
                       help='离子浓度 (默认: 0.15 M)')
    parser.add_argument('--output-prefix', default='processed', 
                       help='输出文件前缀 (默认: processed)')
    parser.add_argument('--skip-mdrun', action='store_true', 
                       help='跳过实际的MD模拟，只生成输入文件')
    parser.add_argument('--with-equilibration', action='store_true', 
                       help='包含平衡阶段')
    parser.add_argument('--md-time', type=int, default=100000, 
                       help='生产模拟步数 (默认: 100000)')
    
    args = parser.parse_args()
    
    # 检查PDB文件是否存在
    if not os.path.exists(args.pdb_file):
        print(f"错误: PDB文件 '{args.pdb_file}' 不存在")
        sys.exit(1)
    
    # 创建输出文件夹
    output_dir = args.output_dir
    os.makedirs(output_dir, exist_ok=True)
    print(f"输出文件夹: {output_dir}")
    
    # 复制PDB文件到输出文件夹
    pdb_name = Path(args.pdb_file).stem
    dest_pdb = os.path.join(output_dir, f"{pdb_name}.pdb")
    shutil.copy2(args.pdb_file, dest_pdb)
    print(f"复制PDB文件到: {dest_pdb}")
    
    # 保存原始工作目录
    original_dir = os.getcwd()
    output_dir_abs = os.path.abspath(output_dir)
    
    # 切换到输出文件夹
    os.chdir(output_dir)
    
    # 检查GROMACS是否安装
    #if not check_gromacs():
    #    sys.exit(1)
    
    print(f"\n开始处理PDB文件: {pdb_name}.pdb")
    print("="*60)
    
    # 1. 生成mdp文件
    print("\n步骤1: 生成mdp参数文件...")
    create_ions_mdp()
    create_minimization_mdp()
    if args.with_equilibration:
        create_equilibration_mdp("nvt.mdp", "nvt")
        create_equilibration_mdp("npt.mdp", "npt")
    
    # 2. pdb2gmx: 生成拓扑和坐标文件
    if not pdb2gmx(f"{pdb_name}.pdb", args.forcefield, args.water, args.output_prefix):
        sys.exit(1)
    
    gro_file = f"{args.output_prefix}.gro"
    top_file = f"{args.output_prefix}.top"
    
    # 3. editconf: 定义盒子
    if not editconf(gro_file, "boxed.gro", args.box_distance, args.box_type):
        sys.exit(1)
    
    # 4. solvate: 添加水分子
    if not solvate("boxed.gro", top_file, "solvated.gro"):
        sys.exit(1)
    
    # 5. 添加离子
    if not generate_ions("solvated.gro", top_file, "ions.tpr", 
                         args.ion_conc, "NA", "CL"):
        sys.exit(1)
    
    # 6. 能量最小化
    print("\n步骤6: 能量最小化...")
    if not grompp("minimization.mdp", "solvated.gro", top_file, "em.tpr"):
        sys.exit(1)
    
    if not args.skip_mdrun:
        if not mdrun("em.tpr", "em"):
            sys.exit(1)
    else:
        print("跳过能量最小化模拟 (--skip-mdrun)")
    
    # 7. 平衡阶段 (可选)
    production_gro = "solvated.gro"
    
    if args.with_equilibration:
        print("\n步骤7: 平衡阶段...")
        
        # NVT平衡
        if args.skip_mdrun:
            production_gro = "solvated.gro"
        else:
            if not grompp("nvt.mdp", "em.gro", top_file, "nvt.tpr", maxwarn=1):
                sys.exit(1)
            
            if not mdrun("nvt.tpr", "nvt"):
                sys.exit(1)
            
            production_gro = "nvt.gro"
        
        # NPT平衡
        if not args.skip_mdrun:
            if not grompp("npt.mdp", "nvt.gro", top_file, "npt.tpr", maxwarn=1):
                sys.exit(1)
            
            if not mdrun("npt.tpr", "npt"):
                sys.exit(1)
            production_gro = "npt.gro"
    else:
        if args.skip_mdrun:
            production_gro = "solvated.gro"
        else:
            production_gro = "em.gro"
    
    # 8. 生产模拟
    print("\n步骤8: 生产模拟...")
    create_production_mdp("md.mdp", args.md_time)
    if not grompp("md.mdp", production_gro, top_file, "md.tpr"):
        sys.exit(1)
    
    if not args.skip_mdrun:
        if not mdrun("md.tpr", "md"):
            sys.exit(1)
    else:
        print("跳过生产模拟 (--skip-mdrun)")
    
    # 9. 生成bash脚本
    print("\n步骤9: 生成bash脚本...")
    bash_script = generate_bash_script(output_dir_abs, args)
    
    print("\n" + "="*60)
    print("GROMACS输入文件生成完成!")
    print(f"\n所有文件已输出到: {output_dir}")
    print("\n生成的文件:")
    print(f"- PDB文件: {pdb_name}.pdb")
    print(f"- 拓扑文件: {top_file}")
    print(f"- 坐标文件: {gro_file}")
    print(f"- mdp文件: ions.mdp, minimization.mdp")
    if args.with_equilibration:
        print(f"- 平衡mdp文件: nvt.mdp, npt.mdp")
    print(f"- 生产mdp文件: md.mdp")
    print(f"- TPR文件: ions.tpr, em.tpr, md.tpr")
    if args.with_equilibration:
        print(f"- 平衡TPR文件: nvt.tpr, npt.tpr")
    
    if not args.skip_mdrun:
        print(f"- 轨迹文件: em.xtc, md.xtc")
        print(f"- 能量文件: em.edr, md.edr")
        print(f"- 日志文件: em.log, md.log")
    
    bash_script_name = os.path.basename(bash_script)
    print(f"\nBash脚本: {bash_script}")
    print("\n使用方法:")
    print(f"  进入输出文件夹: cd {output_dir}")
    print(f"  运行bash脚本: ./{bash_script_name}")
    print("\n或者直接使用:")
    print(f"  运行模拟: {GMX_CMD} mdrun -s md.tpr -deffnm md")
    print(f"  分析轨迹: {GMX_CMD} energy -f md.edr")
    print(f"  查看轨迹: {GMX_CMD} view -f md.xtc")

if __name__ == "__main__":
    main()
