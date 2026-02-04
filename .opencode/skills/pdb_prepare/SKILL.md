---
name: pdb_prepare
description: 当用户提供一个蛋白质文件（.pdb）时，提出对蛋白进行蛋白准备的操作
license: Proprietary. LICENSE.txt has complete terms
---

# PDF Processing Guide

## Overview

Start by splitting the downloaded PDB crystal structure: extract chain A and remove any ligands, waters, and metal ions to obtain the apo protein in PDB format. Next, use sed to standardize specific residue and terminal-atom naming so the force field can recognize them correctly. Finally, run GROMACS pdb2gmx to generate the protein topology and coordinate files, preparing the system for downstream MD setup. Output the extracted small-molecule 3D structure in SDF format and the processed protein structure.


### Arguments
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `pdb_path` | string | 是 | 目标受体（Protein）文件路径，扩展名为 .pdb |
| `output_path` | string | 是 | 文件输出的目录 |

## Quick Start

```bash
python protein_prepare.py {{pdb_path}} {{output_path}}

```
