---
name: compound-query
description: 根据smiles, cas-no, iupac name等条件，搜索完整的分子信息
license: Proprietary. LICENSE.txt has complete terms
---

## Overview
Given a SMILES string, CAS number, IUPAC name, or similar identifiers, retrieve the compound’s complete molecular information.

```bash
# 查询化合物（自动检测类型）
python compound_query.py "CCO"              # SMILES (乙醇)
python compound_query.py "ethanol"          # IUPAC 名称
python compound_query.py "64-17-5" -t cas   # CAS 号

# 查询并显示详细信息
python compound_query.py "CCO" -v

# 保存结果
python compound_query.py "CCO" -o ethanol.json
python compound_query.py "ethanol" -f json -o ethanol.json
python compound_query.py "ethanol" -f csv -o ethanol.csv

# 使用不同格式输出
python compound_query.py "CCO" -f json
python compound_query.py "CCO" -f csv
```

### Arguments
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `smiles` | string | 是 | 化合物的smiles ｜
| `cas` | string | 是 | 化合物的cas number |

## Quick Start

## 从pubchem获取化合物的信息
### 通过smiles查询

```bash
python compound_query.py {{smiles}} -o compound.json

```

### 通过cas number查询
```bash
compound_query.py {{cas}} -t cas -o compound.json

```
