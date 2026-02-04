---
name: drug_compound_insert
description: 将化合物记录到compound数据库中。化合物可以记录在*.sdf、*.csv、*.mol、*.txt等格式的文件中，或者以smiles、inchi、inchi_key的形式表示。
license: Proprietary. LICENSE.txt has complete terms
---

## Overview
Register compounds into the compound database. Compounds may be supplied in files such as *.sdf, *.csv, *.mol, or *.txt, or provided directly as SMILES, InChI, or InChIKey strings.

### Arguments
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `compound` | string | 是 | 要插入的化合物的smiles、inchi、inchi_key或文件名，文件名扩展名为 .sdf .csv .mol .txt等|

## Quick Start

```bash
craton data insert prj_vcompound -i {{compound}}

```