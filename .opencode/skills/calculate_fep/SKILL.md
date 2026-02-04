---
name: calculate_fep
description: 当用户提供一个小分子文件（.sdf）和一个蛋白质文件（.pdb）时，进行小分子与蛋白靶点的FEP计算
license: Proprietary. LICENSE.txt has complete terms
---

## Overview
When the user provides a small-molecule structure file (.sdf) and a protein structure file (.pdb), run an FEP workflow to compute the ligand–protein binding free energy for the specified target.


### Arguments
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `sdf_path` | string | 是 | 待计算的小分子（Ligand）文件路径，扩展名为 .sdf |
| `pdb_path` | string | 是 | 目标受体（Protein）文件路径，扩展名为 .pdb |

## Quick Start

```bash
craton simulation rbfe --ligands {{sdf_path}} --protein {{pdb_path}} -o output

```