---
name: retrosynthesis
description:  输入一个包含多个化合物的smiles的文件，对所有的分子进行逆合成分析
license: MIT
---

# Retrosynthesis

## Overview
This skill is used to perform retrosynthesis on some given molecules. It uses the RDKit library to perform the retrosynthesis. The environment is set up using Conda, the environment name is rxngraphormer (/home/codepublic/.conda/envs/rxngraphormer/bin/python). The input file contain one or more SMILES. Run the script as the following example and it will predict synthesis route for all moluecules.

### Arguments
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `input_file` | string | 是 | 存放分子SMILES的文本文件路径 |
| `output_path` | string | 是 | 存放逆合成分析结果的目录路径 |

## Quick start

```bash
source "$(conda info --base)/etc/profile.d/conda.sh" && conda activate rxngraphormer && python .opencode/skills/skills/retrosynthesis/scripts/retrosynthesis.py --input_file {{input_file}} --output_path {{output_path}}
```
