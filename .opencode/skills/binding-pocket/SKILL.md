---
name: binding-pocket
description: 探索蛋白口袋位置，输出每个口袋的位置、大小、体积、表面积等。用户需要提供一个蛋白文件(.pdb)
license: Proprietary. LICENSE.txt has complete terms
---

## Overview
Given a protein structure file (.pdb), identify potential binding pockets and report each pocket’s location and key descriptors such as size, volume, and surface area.

### Arguments
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `protein_file` | string | 是 | 蛋白文件，通常是pdb文件 ｜
| `output_dir` | string | 否 | 输出文件的目录 |

## Quick Start

## 从pdb bank下载
### 有输出文件夹

```bash
python pocket_analyzer {{protein_file}}  -o {{output_dir}}/pockets_summary.csv

```