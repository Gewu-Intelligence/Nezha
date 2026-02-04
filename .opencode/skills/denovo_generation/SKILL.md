---
name: denovo_generation
description: This skill is used to perform de novo molecule generation basd on a given protein and a coordinate of center of pocket. 
license: Proprietary. LICENSE.txt has complete terms
---

# De Novo generation Guide

## Overview
This skill is used to perform de novo molecule generation using Python libraries and command-line tools. Users are required to provide two input files: a receptor protein structure file (.pdb) and a csv file (.csv) containing the coordinates for the binding pocket center. All generated molecules are saved in the given output directory as .sdf files. Additionally, the corresponding SMILES representations of these molecules are consolidated into a single .csv file, which is also in the given output directory. You should not read the content of the input .pdb and .csv files or pick which pocket to generate molecules. Just run the script directly. 
 
### Arguments
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `protein_path` | string | 否 | 用户可以指定路径名，默认为binding_pocket操作或上一步操作输出目录中的'best.pdb'文件，扩展名为.pdb |
| `center_path` | string | 否 | 用户可以指定路径名，默认为binding_pocket操作或上一步操作输出目录中的文件，可能为包含'rank01_'字段或者名为pockets_summary.csv，扩展名为.csv |
| `output_path` | string | 否 | 用户可以指定路径名，默认为denovo_generation_output |
| `n_samples` | int | 否 | 生成分子的数量，默认为10 |

---

## Quick start

```bash
source "$(conda info --base)/etc/profile.d/conda.sh" && conda activate molgen && python main.py --protein_path ./xxx.pdb --center_path ./xxx.csv --output_path ./denovo_generation_output --n_samples 10
```