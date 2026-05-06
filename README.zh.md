# 浑天绫(Huntianling)

[English](README.md) | [简体中文](README.zh.md)

浑天绫是一套面向物质科学的多智能体 Skills 体系，致力于构建可编排、可扩展、可沉淀的智能计算能力底座。平台覆盖从分子宏观物化性质预测、分子动力学模拟、材料性质计算、自由能微扰计算、反应与合成规划等关键环节，形成贯穿计算化学、材料科学、药物研发等领域的工作流。各类工具在统一框架下协同工作、共享中间结果，并以自然语言和结构化输出服务科研团队，推动物质科学研究从"人工驱动、工具堆叠"走向"智能体协作驱动、流程闭环支撑"。

以小分子药物发现为例：
<div align="center">
<img src="./images/flowchart_zh.jpg" alt="main_flowchart" width="80%" />
</div>


## 能力

* 反应与合成规划：逆合成路线预测、正向合成产物预测、反应产率/选择性预测
* 基于燧人微调模型物理化学性质预测：相变温度、密度、蒸气压、临界性质、介电常数等
* 分子动力学模拟：多体系MD模拟、液相性质计算、自由能计算(FEP)
* 分子拓扑分析：结构特征识别、参数测量、结构操作、分子碎片化
* 分子力学与力场：能量/力/Hessian计算、结构优化、势能面扫描、力场参数拟合
* 蛋白质处理：结构预处理、氨基酸突变/修饰、PDB/UniProt信息获取
* 分子发现与设计：分子对接、口袋发现、结合自由能/溶解度/分配系数计算
* ADMET评估：化合物ADMET性质预测、分子信息查询与数据库管理
* 辅助工具：结构可视化、PDB下载、专利/文献检索

## 安装

### 通过镜像安装（推荐）

我们建议通过docker安装。Huntianling所需的环境、依赖、python环境均已打包在镜像中，可通过以下命令拉取并启动镜像：
```
docker pull crpi-lk3um3q91l9bb8oe.cn-shanghai.personal.cr.aliyuncs.com/huntianling/hun:v0.0.2
docker run -d \
  --name huntianling-service \
  -p 3001:3001 \
  -p 3000:3000 \
  -e PDB_VIEWER_URL="https://localhost:3001" \
  -v ~/.opencodeconfig:/root/.local \
  crpi-lk3um3q91l9bb8oe.cn-shanghai.personal.cr.aliyuncs.com/huntianling/hun:v0.0.2
```
随后应可在局域网下访问 https://localhost:3000 访问网页对话服务。

可通过网页UI自行选择LLM提供商和模型。我们推荐使用Zhipu GLM-5模型，本项目现有能力均在该模型上测试。


### 从头安装

通过以下命令安装基础环境：

```bash
git clone https://github.com/golab-ai/Huntianling
cd Huntianling
conda env create -f environment.yaml
conda activate huntianling
```

随后启动网页服务和画布服务：
```bash
conda activate huntianling && opencode-linux-x64/bin/opencode web --hostname 0.0.0.0 --port 3000 &
bash opencode_canvas/start_drug_design.sh
```

使用浏览器访问 https://localhost:3000 ，即可访网页服务。类似地，随后可通过网页UI自行选择LLM提供商和模型。

#### 其他软件（可选）

##### Gromacs
    
如需使用gromacs进行分子动力学模拟，请确保gmx或gmx_mpi已正确设置在环境变量中，请参见[GROMACS Installation guide](https://manual.gromacs.org/documentation/current/install-guide/index.html)
```bash
# vi ~/.bashrc
# settings of MPI environmnet
# settings of cuda (optional)
source $GMX_PATH/install/bin/GMXRC
gmx_mpi --version
```

##### Retrosynthesis

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
模型使用的权重在会在脚本中自动下载，请参见[RXNGraphormer](https://github.com/licheng-xu-echo/RXNGraphormer)


## 示例

<div align="center">
<img src="./images/wciki-bm6ev.gif" alt="main_flowchart" width="80%" />
</div>

```
Download an 8S9A protein and then add hydrogen to it.
```

```
运行MD模拟（10000 步；输入 ./pdb/protein_A_apo.pdb.pdb；输出到 ./md）
```

```
example文件夹下有一个tyk2的pdb文件和配体的sdf文件，做一个对接
```

```
请帮我计算example/molecule.csv的介电常数, 输出到./runjob/property_er
```

```
帮我对列表中的目标分子进行逆合成分析 ['COC(=O)[C@H](CCCCN)NC(=O)Nc1cc(OC)cc(C(C)(C)C)c1O', 'O=C(Nc1cccc2cnccc12)c1cc([N+](=O)[O-])c(Sc2c(Cl)cncc2Cl)s1', 'CCN(CC)Cc1ccc(-c2nc(C)c(COc3ccc([C@H](CC(=O)N4C(=O)OC[C@@H]4Cc4ccccc4)c4ccon4)cc3)s2)cc1']
```
