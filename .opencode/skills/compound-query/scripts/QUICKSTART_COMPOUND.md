# 化合物查询工具 - 快速入门

## 安装

```bash
pip install -r requirements_compound.txt
```

或直接安装：

```bash
pip install pubchempy
```

## 基本使用

### 1. 查询化合物

```bash
# 使用名称查询
python compound_query.py "ethanol"

# 使用 SMILES 查询
python compound_query.py "CCO"

# 使用 CAS 号查询
python compound_query.py "64-17-5" -t cas

# 使用 PubChem CID 查询
python compound_query.py "702" -t cid
```

### 2. 保存结果

```bash
# 保存为 JSON
python compound_query.py "ethanol" -o ethanol.json

# 保存为 CSV
python compound_query.py "ethanol" -f csv -o ethanol.csv

# 查看结果（JSON 格式）
python compound_query.py "ethanol" -f json
```

### 3. 查看详细信息

```bash
python compound_query.py "ethanol" -v
```

## 支持的标识符

| 标识符类型 | 说明 | 示例 |
|----------|------|------|
| 名称 | IUPAC 名称或常用名 | ethanol, 乙醇 |
| SMILES | 分子结构表示 | CCO (乙醇) |
| CAS 号 | 化学文摘服务登记号 | 64-17-5 (乙醇) |
| CID | PubChem 化合物 ID | 702 (乙醇) |

## 查询到的性质

### 基本信息
- 分子式、分子量、InChI、InChI Key 等

### 物理化学性质
- SMILES、氢键供受体数、可旋转键数、脂溶性等

### 热力学性质
- 沸点、熔点、密度、闪点、pKa 等

## 示例输出

运行：
```bash
python compound_query.py "ethanol"
```

输出：
```
============================================================
化合物查询结果
============================================================
查询内容: ethanol
PubChem CID: 702
============================================================

【基本信息】
  分子式                    : C2H6O
  分子量                    : 46.06844
  精确分子量                : 46.041864828

【物理化学性质】
  标准SMILES                 : CCO
  异构SMILES                 : CCO
  InChI Key                : LFQSCWFLJHTTHZ-UHFFFAOYSA-N
  IUPAC 名称                 : ethanol
  氢键供体数                : 1
  氢键受体数                : 1
  可旋转键数                : 0
  拓扑极性表面积            : 20.2
  脂溶性 (XLogP3)             : -0.31

【热力学性质】
  沸点                       : 78.37 °C
  熔点                       : -114.14 °C
  密度                       : 0.789 g/mL
  闪点                       : 13 °C

============================================================
```

## 常见问题

**Q: 显示"服务器繁忙"怎么办？**
A: PubChem 服务器可能负载过高，等待几分钟后重试即可。

**Q: 查询不到某个化合物？**
A: 确认 PubChem 数据库中是否有该化合物，或者尝试使用其他标识符查询。

**Q: 某些性质为空？**
A: 并非所有化合物都有完整的性质数据。

## 查看更多

- 完整文档：[README_COMPOUND.md](README_COMPOUND.md)
- 查看示例输出：`python test_compound_query.py`
- 查看帮助：`python compound_query.py -h`
