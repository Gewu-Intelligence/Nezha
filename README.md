# Huntianling

[English](README.md) | [简体中文](README.zh.md) | [视频](https://www.bilibili.com/video/BV19CcTzFEH4)

Huntianling is an integrated multi-agent skills system designed for AI-driven material sciences, aimed at building an orchestrable, extensible, and accumulable foundation for intelligent computing. It covers key stages from prediction of moleculars' macroscopic physicochemical properties, molecular dynamics simulation, materials property calculations, free-energy perturbation calculations, to reaction and synthesis planning —forming workflows that run through computational chemistry, materials science, drug discovery, and related fields. Tools work together under one framework, share intermediate results, and serve researchers through natural language and structured outputs—helping move materials research from manual, tool-by-tool work toward agent-collaboration-driven workflows with closed-loop support.

Taking molecule drug discovery as an example:
<div align="center">
<img src="./images/flowchart_en.jpg" alt="main_flowchart" width="100%" />
</div>

## Skills
* Reaction and synthesis planning: Retrosynthetic route prediction, forward synthesis product prediction, reaction yield and selectivity prediction
* Physicochemical property prediction (Suiren fine-tuned model): Phase-transition temperature, density, vapor pressure, and critical properties, dielectric constant, etc.
* Molecular dynamics simulation: MD simulation of multiple systems, liquid-phase property calculation, free energy calculation(FEP)
* Molecular topology analysis: Structural feature identification, parameter measurement, structural manipulation, molecular fragmentation
* Molecular mechanics and force fields: Energy/force/Hessian evaluation, structure optimization, potential energy surface scanning, force field parameter fitting
* Protein processing: Structure preprocessing, amino acid mutation/modification, PDB/UniProt information retrieval
* Molecular discovery and design: Molecular docking, pocket detection, binding free energy, solubility, and partition coefficient calculation
* ADMET assessment: Compound ADMET property prediction, molecular information queries, database management
* Auxiliary tools: Structure visualization, PDB download, patent and literature search

## Installation

### Install via image (Recommended)

We recommend installing via Docker. The environment, dependencies, and Python environment required for Huntianling are all packaged in the image. You can pull and start the image using the following command:
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
Subsequently, a web-based chat service should be accessible via https://localhost:3000 on the local network.

Users can select their LLM provider and model through the web UI. We recommend using the Zhipu GLM-5 model, as all current capabilities of this project have been tested on this model.


### Install directly

#### 1. Clone the project

Install the basic environment using the following command:
```bash
git clone https://github.com/golab-ai/Huntianling
cd Huntianling
conda env create -f environment.yaml
conda activate huntianling
```

Then, the web page service and canvas service are started:
```bash
conda activate huntianling && opencode-linux-x64/bin/opencode web --hostname 0.0.0.0 --port 3000 &
bash opencode_canvas/start_drug_design.sh
```
You can access web services by visiting  https://localhost:3000 in your browser. Similarly, you can then select your LLM provider and model through the web UI.

> 
#### 4. Other software (optional)

##### Gromacs
    
    If you plan to use GROMACS for MD simulations, make sure gmx or gmx_mpi is correctly set in your environment variables (PATH). Please refer to the[GROMACS Installation guide](https://manual.gromacs.org/documentation/current/install-guide/index.html)
    ```bash
    # vi ~/.bashrc
    # settings of MPI environmnet
    # settings of cuda if it is required 
    source $GMX_PATH/install/bin/GMXRC
    gmx_mpi --version
    ```

##### Retrosynthesis

    For retrosynthesis analysis, use the team-developed [RXNGraphormer](https://github.com/licheng-xu-echo/RXNGraphormer)
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


## Example

<div align="center">
<img src="./images/wciki-bm6ev.gif" alt="main_flowchart" width="80%" />
</div>

```
Download an 8S9A protein and then add hydrogen to it.
```

```
Run MD simulation, 10000 steps, input with example/tyk2_protein.pdb, output to ./runjob/md
```

```
There's a tyk2 PDB file and a ligand SDF file in the example folder. Perform a docking.
```

```
Calculate the dielectric constant of example/molecule.csv and output it to ./runjob/property_er
```

```
Perform retrosynthetic analysis on the target molecules in the list. ['COC(=O)[C@H](CCCCN)NC(=O)Nc1cc(OC)cc(C(C)(C)C)c1O', 'O=C(Nc1cccc2cnccc12)c1cc([N+](=O)[O-])c(Sc2c(Cl)cncc2Cl)s1', 'CCN(CC)Cc1ccc(-c2nc(C)c(COc3ccc([C@H](CC(=O)N4C(=O)OC[C@@H]4Cc4ccccc4)c4ccon4)cc3)s2)cc1']
```
