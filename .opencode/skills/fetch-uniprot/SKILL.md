---
name: fetch-uniprot
description: 根据蛋白名或uniprot ID，查询蛋白的信息，并获取fasta，以及对应的PDB ID
license: Proprietary. LICENSE.txt has complete terms
---

## Overview
Given a protein name or UniProt ID, look up the protein’s details and retrieve its FASTA sequence along with any associated PDB ID(s).

### Arguments
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `uniprot_ID` | string | 是 | 某个uniprot ID，以P或Q字母开头 |
| `protein_name` | string | 是 | 蛋白的名称，俗称或描述 |
| `path_dir` | string | 是 | 信息保存的文件夹 |

## Quick Start

## 从uniprot网站查询
### 根据蛋白名查询,如果有文件夹

```bash
python fetch_uniprot.py name:{{protein_name}} {{path_dir}}

```

### 根据蛋白名查询,没有文件夹
```bash
python fetch_uniprot.py name:{{protein_name}}

```

### 根据uniprot ID查询
```bash
python fetch_uniprot.py {{uniprot_ID}}

```