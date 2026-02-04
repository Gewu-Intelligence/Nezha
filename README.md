# Gnexus

Gnexus是一套面向智能药物研发的 多智能体技能（Skills）体系，覆盖从靶点调研与结构分析、分子生成与设计、对接与打分筛选、分子动力学模拟，到高精度 FEP 自由能计算的完整计算研发流程。各类 Agent 不再是孤立工具，而是具备明确分工、可相互协作的“专业智能角色”，能够在统一框架下自动衔接任务、共享中间结果，并与团队成员进行自然语言与结构化信息交互，实现科研流程的模块化、自动化与协同化，推动药物发现从“人工驱动”向“智能体协作驱动”演进。

## 安装

### 1. Clone the project

```bash
git clone xxxx
cd xxxx
```

### 2. 设置conda环境

```bash
conda env create -f environment.yml
conda activate gnexus
```

### 3. OpenCode安装

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
使用浏览器访问https://localhost:4059，并使用相应的用户名和密码在浏览器中登录，即可访问opencode的网页服务

> 如需局域网访问，请将127.0.0.1替换成0.0.0.0

### 4. 其他软件（可选）

1. Gromacs
    
如需使用gromacs进行分子动力学模拟，请确保gmx或gmx_mpi已正确设置在环境变量中，请参见[GROMACS Installation guide](https://manual.gromacs.org/documentation/current/install-guide/index.html)
```bash
# vi ~/.bashrc
# settings of MPI environmnet
# settings of cuda if it is required 
source $GMX_PATH/install/bin/GMXRC
gmx_mpi --version
```

2. ADMET
如需使用admet预测，需安装[admet-ai](https://github.com/swansonk14/admet_a)
```bash
conda create -y -n admet_ai python=3.12
conda activate admet_ai
pip install admet-ai
```

3. Retrosynthesis
逆合成分析使用团队开发的[RXNGraphormer](https://github.com/licheng-xu-echo/RXNGraphormer)工具
```bash
conda create -n rxngraphormer python=3.8
conda activate rxngraphormer
pip install rxngraphormer -i https://pypi.org/simple -f https://data.pyg.org/whl/torch-1.12.0+cu113.html --extra-index-url https://download.pytorch.org/whl/cu113
```