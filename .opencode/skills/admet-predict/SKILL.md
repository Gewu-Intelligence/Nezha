---
name: admet-predict
description: 预测化合物的admet性质
license: Proprietary. LICENSE.txt has complete terms
---

## Overview
When given a compound, predict its ADMET properties (absorption, distribution, metabolism, excretion, and toxicity).

### Arguments
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `smiles_file` | string | 是 | 包含smiles的文件 文件格式可能是.csv或者.txt |
| `output_dir` | string | 是 | 文件输出的目录 |

## 执行

**非常重要** 每次使用该skills时请重新载入环境：
```bash
source "$(conda info --base)/etc/profile.d/conda.sh" && conda activate admet_ai && CUDA_VISIBLE_DEVICES=-1 python admet-predict.py --smiles_file {{smiles_file}} --output_dir {{output_dir}}
```
