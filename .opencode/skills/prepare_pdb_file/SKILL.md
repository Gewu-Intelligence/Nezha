---
name: prepare_pdb_file
description: 输入PDB ID，获取相应的PDB文件
license: Proprietary. LICENSE.txt has complete terms
---



## Overview

根据输入的ID，获取pdb文件



### Arguments
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `file` | string | 否 | 包含pdb id的文件, 通常是info-file文件 |
| `pdb_id` | string | 否 | pdb ID号 |
| `output_path` | string | 否 | 文件输出的目录，默认输出在当前文件下 |

## Quick Start

##如果输入的是info-file文件，且有输出文件夹
```bash
craton prepare pdb -i {{file}} -o {{output_path}}

```

##如果输入的是pdb id，且有输出文件夹
```bash
craton prepare pdb -id {{pdb_id}} -o {{output_path}}

```

##如果输入的是info-file文件，没有输出文件夹
```bash
craton prepare pdb -i {{file}}

```

##如果输入的是pdb id，没有输出文件夹
```bash
craton prepare pdb -id {{pdb_id}}

```