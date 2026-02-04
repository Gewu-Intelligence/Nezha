# 化合物性质查询工具

基于 [PubChemPy](https://pubchempy.readthedocs.io/) 的化合物信息查询工具，支持通过 SMILES、CAS 号、IUPAC 名称等标识符查询化合物的各种物理化学性质。

## 功能特性

- **多种输入方式**：支持 SMILES、CAS 号、IUPAC 名称、PubChem CID
- **自动类型检测**：自动识别输入的标识符类型
- **全面的性质查询**：查询分子的各种物理化学性质
- **多种输出格式**：支持表格、JSON、CSV 格式输出
- **文件保存**：可将查询结果保存到文件
- **中文界面**：支持中文显示，便于理解

## 安装

### 1. 安装依赖

```bash
pip install -r requirements_compound.txt
```

或直接安装：

```bash
pip install pubchempy
```

### 2. 赋予执行权限（可选）

```bash
chmod +x compound_query.py
```

## 使用方法

### 基本用法

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

### 命令行参数

```
positional arguments:
  identifier            化合物标识符（SMILES、CAS 或 IUPAC 名称）

optional arguments:
  -h, --help            显示帮助信息
  -t, --type {smiles,smls,cas,name,iupac,cid}
                        标识符类型（可选）
  -f, --format {table,json,csv}
                        输出格式（默认: table）
  -o, --output OUTPUT   保存到文件
  -v, --verbose         显示详细信息
```

### 使用示例

#### 示例 1: 查询乙醇

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
  InChI                     : InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3
  InChI Key                : LFQSCWFLJHTTHZ-UHFFFAOYSA-N
  IUPAC 名称                : ethanol
  氢键供体数                : 1
  氢键受体数                : 1
  可旋转键数                : 0
  拓扑极性表面积            : 20.2

【热力学性质】
  沸点                      : 78.37 °C
  熔点                      : -114.14 °C
  密度                      : 0.789 g/mL
  闪点                      : 13 °C
  LogP                      : -0.31

============================================================
```

#### 示例 2: 使用 SMILES 查询

```bash
python compound_query.py "CC(=O)O" -o acetic_acid.json
```

#### 示例 3: 使用 CAS 号查询

```bash
python compound_query.py "50-78-2" -t cas
```

#### 示例 4: 保存为 CSV 格式

```bash
python compound_query.py "ethanol" -f csv -o data.csv
```

#### 示例 5: 查询并显示详细信息

```bash
python compound_query.py "CCO" -v
```

## 支持的化合物性质

### 基本信息
- 分子式 (Molecular Formula)
- 分子量 (Molecular Weight)
- 精确分子量 (Exact Mass)
- 单同位素质量 (Monoisotopic Mass)
- InChI
- InChI Key
- IUPAC 名称
- 同义词

### 物理化学性质
- 标准 SMILES (Canonical SMILES)
- 异构 SMILES (Isomeric SMILES)
- 氢键供体数 (Hydrogen Bond Donor Count)
- 氢键受体数 (Hydrogen Bond Acceptor Count)
- 可旋转键数 (Rotatable Bond Count)
- 拓扑极性表面积 (Topological Polar Surface Area)
- 脂溶性 (XLogP3, LogP)
- 复杂度 (Complexity)
- 重原子数 (Heavy Atom Count)

### 热力学性质
- 沸点 (Boiling Point)
- 熔点 (Melting Point)
- 闪点 (Flash Point)
- 密度 (Density)
- pKa 值
- 水溶性 (Solubility, LogS)
- 蒸气压 (Vapor Pressure)
- 表面张力 (Surface Tension)

## 编程使用示例

```python
from compound_query import CompoundQuery

# 创建查询对象
query = CompoundQuery("ethanol")

# 执行查询
if query.query():
    # 获取所有性质
    properties = query.get_all_properties()
    
    # 打印结果
    query.print_properties()
    
    # 保存到文件
    query.save_to_file("ethanol.json", "json")

# 使用指定类型查询
query = CompoundQuery("64-17-5", identifier_type="cas")
if query.query():
    properties = query.get_all_properties()
    print(properties)
```

## 常见问题

### 1. 查询失败或显示"服务器繁忙"怎么办？

- **PubChem 服务器繁忙**：PubChem 是公共资源，可能会出现服务器繁忙的情况（HTTP 503）
  - 等待几分钟后重试
  - 脚本内置了自动重试机制，默认重试 3 次，每次间隔 2 秒
  - 避免在短时间内发送大量请求

- **检查网络连接**：确保能够访问 PubChem API
- **检查输入**：确认输入的标识符是否正确
- **尝试不同标识符**：如果一种方式不行，可以尝试使用其他方式（如 SMILES、CAS、名称）

### 2. 某些性质显示为空？

- PubChem 数据库中可能没有该化合物的某些性质
- 某些实验数据可能不可用
- 不是所有化合物都有完整的性质数据

### 3. 如何获取 CAS 号？

- 可以使用化学数据库（如 SciFinder、Reaxys）
- 使用在线工具（如 ChemSpider）
- 从化学品供应商的产品信息中获取
- 查询 PubChem 后，结果中可能包含 CAS 号作为同义词

### 4. 支持的 SMILES 格式？

- 标准 SMILES（Canonical SMILES）
- 异构 SMILES（Isomeric SMILES）
- 自动检测 SMILES 格式

## 注意事项

- **需要网络连接**：必须能够访问 PubChem API
- **查询速度**：取决于网络状况和服务器负载
- **数据完整性**：PubChem 数据可能不是最新的或完整的
- **请求限制**：避免频繁请求，以免被限制访问
- **数据准确性**：实验数据可能存在误差，建议交叉验证

## 性能优化

- 使用 PubChem CID 查询速度最快
- SMILES 查询次之
- 名称查询最慢（因为需要模糊匹配）
- CAS 号查询实际上使用名称查询，速度较慢

## 批量查询示例

如需批量查询多个化合物，可以创建一个简单的循环：

```python
from compound_query import CompoundQuery

compounds = ["ethanol", "methanol", "propanol"]

for comp in compounds:
    print(f"\n查询: {comp}")
    query = CompoundQuery(comp)
    if query.query():
        properties = query.get_all_properties()
        print(f"  CID: {properties.get('PubChem CID')}")
        print(f"  分子式: {properties.get('分子式')}")
        print(f"  分子量: {properties.get('分子量')}")
    else:
        print("  查询失败")
```

## 相关资源

- [PubChem 官网](https://pubchem.ncbi.nlm.nih.gov/)
- [PubChemPy 文档](https://pubchempy.readthedocs.io/)
- [SMILES 格式说明](https://en.wikipedia.org/wiki/Simplified_molecular-input_line-entry_system)

## 许可证

MIT License
