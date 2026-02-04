---
name: md_simulation
description: 当用户提供一个蛋白质文件（.pdb）、运行时间（ns)和输出路径时，进行md模拟
license: Proprietary. LICENSE.txt has complete terms
---

## Overview
When the user provides a protein structure file (.pdb), a simulation length (in ns), and an output path, run an MD simulation and write the results to the specified location.

### Arguments
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `pdb_file` | string | 是 | 目标受体（Protein）文件路径，扩展名为 .pdb |
| `output_dir` | string | 是 | 文件输出的目录 |
| `md_time` | float | 否 | 模拟步数 |

## 执行
### 如果有输入模拟的步数
```bash
python pdb2gromacs.py {{pdb_file}} --output-dir {{output_dir}} --md-time {{md_time}}
```

### 如果没有输入的模拟步数
```bash
python pdb2gromacs.py {{pdb_file}} --output-dir {{output_dir}}
```