# Gnexus

[English](README.md) | [简体中文](README.zh.md) | [视频](https://www.bilibili.com/video/BV19CcTzFEH4)

Gnexus is an integrated multi-agent skills system designed for AI-driven drug discovery (AIDD), covering the full computational discovery workflow from target protein investigation, structural analysis, pocket-based molecular generation, docking, molecular dynamics (MD) simulations, to high-accuracy FEP free-energy calculations. Rather than functioning as isolated tools, the Agents act as clearly specialized “professional AI roles” that can collaborate with one another: they automatically hand off tasks within a unified framework, share intermediate results, and interact with team members through natural language and structured information. This enables a modularized, automated, and collaborative research workflow, advancing drug discovery from “human-driven” to “agent-collaboration-driven.”

<div align="center">
<img src="./docs/flowchart_en.jpg" alt="main_flowchart" width="100%" />
</div>

## Skills

- Bioinformatics & structural investigation: UniProt/PDB fetch, chain & conformation selection, identification of missing residues and ligands.

- Patent research: WO/US/CN patent searching and analysis

- PDB file processing: PDB download, format conversion, chain splitting, hydrogen addition/completion, protonation, removal of waters/ions, etc.

- Protein preparation: conformation cleanup, residue repair, apo/holo selection, energy minimization

- Molecular dynamics (MD) simulation: system setup, short relaxation, production runs, trajectory and energy output/analysis

- Pocket prediction: geometry/energy/deep-learning based scoring

- Molecule generation: SMILES generation based on pocket/constraints/fragments/property conditions

- Ligand preparation: desalting, stereoisomers/protonation/tautomers selection, 3D conformers, SDF output

- Molecular docking: grid docking box, docking, scoring, pose filtering/selection

- FEP: relative/absolute free-energy calculation, FEP workflow management, topology mapping, results summarization

- Synthetic route prediction: retrosynthetic routes analysis

- Communication & collaboration: email drafting (internal medicinal chemistry review / external vendor RFQs)

- Compound registration: structured entry of compound & project metadata into inventory (registration number, batch, properties, source, etc.)

## Installation

#### 1. Clone the project

```bash
git clone https://github.com/Gewu-Intelligence/Gnexus
cd Gnexus
```

#### 2. Create a conda environment

```bash
conda env create -f environment.yml
conda activate gnexus
```

#### 3. Install OpenCode

```bash
npm install -g opencode-ai
## or
curl -fsSL https://opencode.ai/install | bash
```
You can also install it using other methods described in the [OpenCode docs](https://opencode.ai/docs).

After that, you should be able to launch the OpenCode TUI (terminal user interface) from your shell:

```bash
opencode
``` 
or start a local web server:
 
```bash
OPENCODE_SERVER_USERNAME=who OPENCODE_SERVER_PASSWORD=secret opencode web --hostname 127.0.0.1 --port 4059
```

Open a browser and go to [https://localhost:4059]. Log in with the corresponding username and password to access OpenCode’s web service. For LAN access, replace 127.0.0.1 with 0.0.0.0.

For the LLM model, Zhipu AI GLM-4.7 is recommended.

> 
#### 4. Other software (optional)

1. Gromacs
    
    If you plan to use GROMACS for MD simulations, make sure gmx or gmx_mpi is correctly set in your environment variables (PATH). Please refer to the[GROMACS Installation guide](https://manual.gromacs.org/documentation/current/install-guide/index.html)
    ```bash
    # vi ~/.bashrc
    # settings of MPI environmnet
    # settings of cuda if it is required 
    source $GMX_PATH/install/bin/GMXRC
    gmx_mpi --version
    ```
2. Retrosynthesis

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
<img src="./docs/wciki-bm6ev.gif" alt="main_flowchart" width="80%" />
</div>

More examples can be found in [example docs](example/example.md)

* Download pdb
```
Download the PDB file of 8S99 (save as .pdb，output to ./pdb)
```

* Structure preparation
```
Protein preparation of 8S99 (input ./pdb/8S99.pdb，output to ./pdb)
```
* MD
```
Run MD simulation (10000 steps, input ./pdb/protein_A_apo.pdb.pdb；output to ./md)
```

* Pocket prediction
```
Predict the pocket of 8S99, (input ./pdb/protein_A_apo.pdb.pdb, output to ./pocket/)
```
