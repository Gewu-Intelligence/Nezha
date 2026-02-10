# Gnexus

[English](README.md) | [简体中文](README.zh.md) | [视频](https://www.bilibili.com/video/BV19CcTzFEH4)


Gnexus是一套面向智能药物研发的 多智能体技能（Skills）体系，覆盖从靶点调研与结构分析、分子生成与设计、对接与打分筛选、分子动力学模拟，到高精度 FEP 自由能计算的完整计算研发流程。各类 Agent 不再是孤立工具，而是具备明确分工、可相互协作的“专业智能角色”，能够在统一框架下自动衔接任务、共享中间结果，并与团队成员进行自然语言与结构化信息交互，实现科研流程的模块化、自动化与协同化，推动药物发现从“人工驱动”向“智能体协作驱动”演进。

<div align="center">
<img src="./images/flowchart_zh.jpg" alt="main_flowchart" width="80%" />
</div>

## 能力
- 生物信息与结构信息调研：UniProt / PDB / 链与构象选择 / 缺失残基与配体识别
- 专利调研：WO/US/CN 专利检索
- 结构文件获取与处理：PDB 下载、格式转换、链拆分、加氢/补全、质子化、去水/去离子等
- 蛋白准备（Protein Prep）：构象清理、残基修复、选择 apo/holo、能量最小化
- 分子动力学（MD）：体系构建、短程 relax / 生产模拟、轨迹与能量输出
- 口袋预测：几何/能量/深度打分
- 分子生成：基于口袋/约束/片段/性质条件生成 SMILES
- 小分子准备（Ligand Prep）：去盐、立体异构、质子化/互变异构、3D构象、SDF输出
- 分子对接（Docking）：定义网格、对接打分、pose筛选
- FEP：相对/绝对自由能流程管理、拓扑映射、结果汇总
- 合成路线预测：逆合成拆解
- 沟通与协作：邮件撰写（内部药化审核/外部供应商询价）
- 入库：化合物与项目元数据结构化写入数据库（注册号/批次/属性/来源等）


## 安装

### 下载

```bash
git clone https://github.com/Gewu-Intelligence/Gnexus
cd Gnexus
```

### 设置conda环境

```bash
conda env create -f environment.yml
conda activate gnexus
```

### OpenCode安装

```bash
npm install -g opencode-ai
## or
curl -fsSL https://opencode.ai/install | bash
```
或可通过其他[OpenCode docs](https://opencode.ai/docs)中的其他方式安装。

随后应可在shell中启动Opencode TUI(terminal user interface)

```bash
opencode
``` 
或启动一个本地web服务 
```bash

OPENCODE_SERVER_USERNAME=who OPENCODE_SERVER_PASSWORD=secret opencode web --hostname 127.0.0.1 --port 4059
```
使用浏览器访问 (https://localhost:4059)，并使用相应的用户名和密码在浏览器中登录，即可访问opencode的网页服务。如需局域网访问，请将127.0.0.1替换成0.0.0.0。

随后需要设置API_key。以Opencode TUI为例，可输入`/connect`命令设置API。我们推荐使用Zhipu GLM-4.7模型，本项目现有能力均在该模型上测试。

### 其他软件（可选）

#### Gromacs
    
如需使用gromacs进行分子动力学模拟，请确保gmx或gmx_mpi已正确设置在环境变量中，请参见[GROMACS Installation guide](https://manual.gromacs.org/documentation/current/install-guide/index.html)
```bash
# vi ~/.bashrc
# settings of MPI environmnet
# settings of cuda if it is required 
source $GMX_PATH/install/bin/GMXRC
gmx_mpi --version
```


#### Retrosynthesis

逆合成分析使用团队开发的[RXNGraphormer](https://github.com/licheng-xu-echo/RXNGraphormer)工具，建议使用pytorch2分支
```bash
conda create -n rxngraphormer python=3.10
conda activate rxngraphormer
git clone -b pytorch2 https://github.com/licheng-xu-echo/RXNGraphormer.git
cd RXNGraphormer/

pip install torch==2.2.1 --index-url https://download.pytorch.org/whl/cu121
pip install pyg_lib torch_scatter torch_sparse torch_cluster torch_spline_conv -f https://data.pyg.org/whl/torch-2.2.0+cu121.html
pip install rdkit==2024.3.2 ipykernel pandas python-box OpenNMT-py==1.2.0 torchdata==0.7.1 torch_geometric rxnmapper localmapper transformers==4.30.0 numpy==1.26.4 scikit-learn
pip install .
```
模型使用的权重需单独下载，请参见[RXNGraphormer](https://github.com/licheng-xu-echo/RXNGraphormer)


## 示例

<div align="center">
<img src="./images/wciki-bm6ev.gif" alt="main_flowchart" width="80%" />
</div>

更多示例请参考[示例文档](example/example.md)

* 下载pdb
```
下载 8S99 的 PDB（存为 .pdb，输出到 ./pdb）
```

* 结构准备
```
准备蛋白（输入 ./pdb/8S99.pdb，输出到 ./pdb）
```
* MD
```
运行MD模拟（10000 步；输入 ./pdb/protein_A_apo.pdb.pdb；输出到 ./md）
```

* 预测结合口袋
```
预测结合口袋（输入 ./pdb/protein_A_apo.pdb.pdb；输出到 ./pocket/）
```
