# 化合物查询工具 - 文件列表

## 文件说明

| 文件 | 说明 |
|------|------|
| `compound_query.py` | 主程序：化合物性质查询工具 |
| `README_COMPOUND.md` | 完整文档：详细的使用说明和API文档 |
| `QUICKSTART_COMPOUND.md` | 快速入门：快速上手指南 |
| `requirements_compound.txt` | 依赖列表：Python 包依赖 |
| `test_compound_query.py` | 示例脚本：展示查询结果示例 |

## 快速开始

1. **安装依赖**
   ```bash
   pip install -r requirements_compound.txt
   ```

2. **查询化合物**
   ```bash
   python compound_query.py "ethanol"
   ```

3. **查看示例输出**
   ```bash
   python test_compound_query.py
   ```

4. **查看帮助**
   ```bash
   python compound_query.py -h
   ```

## 功能特性

- ✅ 支持多种输入方式（SMILES、CAS 号、IUPAC 名称、CID）
- ✅ 自动类型检测
- ✅ 查询全面的化合物性质
- ✅ 多种输出格式（表格、JSON、CSV）
- ✅ 支持保存到文件
- ✅ 中文界面显示
- ✅ 自动重试机制
- ✅ 详细的错误提示

## 使用示例

```bash
# 基本查询
python compound_query.py "ethanol"

# 保存为 JSON
python compound_query.py "ethanol" -o ethanol.json

# 保存为 CSV
python compound_query.py "ethanol" -f csv -o data.csv

# 使用 SMILES
python compound_query.py "CCO"

# 使用 CAS 号
python compound_query.py "64-17-5" -t cas

# 查看详细信息
python compound_query.py "ethanol" -v
```

## 查询到的性质

### 基本信息
- 分子式、分子量、精确分子量
- InChI、InChI Key
- IUPAC 名称、同义词

### 物理化学性质
- SMILES（标准和异构）
- 氢键供体/受体数
- 可旋转键数
- 拓扑极性表面积
- 脂溶性（XLogP3、LogP）
- 复杂度、重原子数

### 热力学性质
- 沸点、熔点
- 密度、闪点
- pKa 值
- 水溶性

## 文档

- **快速入门**: 阅读 [QUICKSTART_COMPOUND.md](QUICKSTART_COMPOUND.md)
- **完整文档**: 阅读 [README_COMPOUND.md](README_COMPOUND.md)
- **示例输出**: 运行 `python test_compound_query.py`
- **命令行帮助**: 运行 `python compound_query.py -h`

## 依赖

- Python 3.6+
- pubchempy >= 1.0.4

## 注意事项

- 需要网络连接访问 PubChem API
- PubChem 服务器可能繁忙，脚本会自动重试
- 避免频繁请求，以免被限制访问
- 某些化合物的部分性质可能缺失

## 许可证

MIT License
