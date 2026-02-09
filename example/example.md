# EXAMPLE: TYK2 药物设计工作流

> 这是一个 **示例**，展示一些提示词如何把一个从靶点调研 → 结构准备 → MD → 口袋预测 → 分子生成 → 配体准备 → 对接 → FEP → 合成路线 → 邮件沟通 → 入库 的流程组织成可复现的项目结构与任务清单。  


###  靶点调研
```txt
调研 TYK2 的 UniProt ID 和 PDB 信息，并推荐一个 PDB（输出到 ./uniprot）
```
```txt
调研 TYK2 的专利（输出到 ./patents）
```
```
下载 8S99 的 PDB（存为 .pdb，输出到 ./pdb）
```

### 结构准备

```
准备蛋白（输入 ./pdb/8S99.pdb，输出到 ./pdb）
```
### MD
```
运行MD模拟（10000 步；输入 ./pdb/protein_A_apo.pdb.pdb；输出到 ./md）
```

### 预测结合口袋
```
预测结合口袋（输入 ./pdb/protein_A_apo.pdb.pdb；输出到 ./pocket/）
```

### 分子生成
```
分子生成（蛋白 + 口袋；输出到 ./generation）
输入：
./pdb/protein_A_apo.pdb.pdb
./pocket/pockets_summary.csv
```
### 配体准备
```
小分子准备（输入 ./example/generation/SMILES.csv；输出到 ./lig_prep）
```
### 分子对接
```
分子对接（蛋白 + 口袋 + 小分子；“生成个新分子”；输出到 ./docking）
输入：
./pdb/protein_A_apo.pdb.pdb
./pocket/pockets_summary.csv
./lig_prep/lig_prepped.sdf
```

### FEP
```
做 FEP（输入蛋白 + ligands_docking.sdf；输出到 ./fep）
输入：
./pdb/_A_apo.pdb.pdb
./docking/output/ligands_docking.sdf
```

### ADMET
```
预测example/generation/SMILES.csv的admet
```

### 预测合成路线
```
预测合成路线（输入 ./example/generation/SMILES.csv；输出到 ./synthesis）
```

### 邮件与入库

```
写邮件：通知内部药化团队审核附件分子并选择需要合成的分子

模板示例：

主题：请审核分子（TYK2项目）

各位同事好，

附件包含本轮 TYK2 口袋驱动生成 + 对接筛选得到的候选分子（含SMILES、对接分数、简单可合成性标注）。
请大家协助：
1）优先挑选 5–20 个建议合成的分子（可在表格“Selected”列标记 Y，并备注理由）
2）如发现明显不可合成/结构风险，请在“Notes”列说明

我们将根据大家反馈汇总进入下一轮采购/合成评估。

谢谢！
（署名）

发送上面的邮件到 cABC@ABC，主题“请审核分子”，附件 @.txt
```

```
写邮件：查询附件化合物是否可购买、价格与可购数量
模板示例：

主题：化合物查询（可购性/价格/交期）

您好，

附件包含一组化合物信息（SMILES/ID）。想请贵方协助确认：
1）每个化合物是否可直接购买（现货/定制）
2）可供数量（mg/g）与对应价格
3）预计交期与纯度规格（如可提供 COA 更佳）

烦请按附件表格补全报价信息后回复，非常感谢！

（署名）
发送上面的邮件到 ABC@ABC，主题“化合物查询”，附件 @.txt地址
```
```
化合物录入到数据库
```