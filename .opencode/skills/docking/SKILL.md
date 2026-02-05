---
name: docking
description: 分子对接操作，需要提供蛋白的pdb文件，化合物的sdf文件，以及配置box和center的文件等
license: Proprietary. LICENSE.txt has complete terms
---

## Overview
To perform molecular docking, the user should provide the protein structure (.pdb), the ligand structure (.sdf), and any required configuration files defining the docking box and center (or equivalent parameters).

### Arguments
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `protein_file` | string | 是 | 蛋白文件，通常是pdb文件 ｜
| `ligand_file` | string | 是 | 化合物的文件，通常是sdf文件 |
| `configure_file` | string | 是 | 蛋白口袋文件，通常是csv文件 |
| `output_dir` | string | 否 | 输出文件的目录 |

## Quick Start

## 从pdb bank下载
### 有输出文件夹

```bash
python run_docking.py --protein_file {{protein_file}} --ligand_file {{ligand_file}} --configure_file {{configure_file}} --results_dir {{output_dir}}

```

### 没有输出文件夹
```bash
python run_docking.py --protein_file {{protein_file}} --ligand_file {{ligand_file}} --configure_file {{configure_file}} 

```
