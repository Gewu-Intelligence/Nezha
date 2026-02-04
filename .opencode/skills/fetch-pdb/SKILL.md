---
name: fetch-pdb
description: 下载对应PDB文件，用户可以输入一个PDB ID号，或输入一个文件
license: Proprietary. LICENSE.txt has complete terms
---

## Overview
Download the corresponding PDB structure file. The user can either provide a PDB ID directly or upload a file containing the desired ID(s).

### Arguments
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `pdb_id` | string | 是 | pdb文件的ID ｜
| `info_file` | string | 是 | 记录pdb ID的文件 |
| `output_dir` | string | 是 | 信息保存的文件夹 |
| `output_format` | string | 否 | 文件格式 |

## Quick Start

## 从pdb bank下载
### 如果是info-file文件（.txt）

```bash
python fetch_pdb.py --info_file {{info_file}} --output_dir {{output_dir}}

```

### 如果是PDB ID
```bash
python fetch_pdb.py --pdb_id {{pdb_id}} --output_dir {{output_dir}}

```

### 同时下载cif文件
```bash
python fetch_pdb.py --info_file {{info_file}} --output_dir {{output_dir}} --output_format {{output_fromat}}

```