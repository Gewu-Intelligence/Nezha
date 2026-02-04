---
name: ligand-prepare
description: 对化合物、小分子或配体进行准备工作，进行加氢、质子化操作等
license: Proprietary. LICENSE.txt has complete terms
---

## Overview
Prepare a compound (small molecule/ligand) by performing standard preprocessing steps such as adding hydrogens and assigning protonation states.

### Arguments
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `f_path` | string | 是 | 输入的分子文件，可以是*.sdf、*.mol以及smiles ｜
| `output_dir` | string | 是 | 处理后要保存的文件 |

## Quick Start

## 从pdb bank下载
### 有输出文件夹

```bash
python ligand_prepare.py {{f_path}} --output_dir {{output_dir}}

```

### 没有输出文件夹
```bash
python ligand_prepare.py {{f_path}}

```