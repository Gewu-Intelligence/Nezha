---
name: patent-search
description: 根据输入的蛋白名称，搜索、下载相关的专利，反回专利号等
license: Proprietary. LICENSE.txt has complete terms
---

## Overview
Given a protein name, search for and download relevant patents, then return key details such as the patent publication number(s).

### Arguments
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `protein_name` | string | 是 | 蛋白的名称 ｜
| `path_dir` | string | 是 | 信息保存的文件夹 |

## Quick Start


```bash
python patent_search.py {{protein_name}} {{path_dir}}

```
