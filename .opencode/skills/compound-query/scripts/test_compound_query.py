#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本 - 展示化合物查询工具的示例输出
由于 PubChem 服务器可能繁忙，这里提供一个示例
"""

import json

# 模拟乙醇的查询结果
example_result = {
    "PubChem CID": 702,
    "分子式": "C2H6O",
    "分子量": 46.06844,
    "精确分子量": 46.041864828,
    "标准SMILES": "CCO",
    "异构SMILES": "CCO",
    "InChI": "InChI=1S/C2H6O/c1-2-3/h3H,2H2,1H3",
    "InChI Key": "LFQSCWFLJHTTHZ-UHFFFAOYSA-N",
    "IUPAC 名称": "ethanol",
    "氢键供体数": 1,
    "氢键受体数": 1,
    "可旋转键数": 0,
    "拓扑极性表面积": 20.2,
    "脂溶性 (XLogP3)": -0.31,
    "沸点": "78.37 °C",
    "熔点": "-114.14 °C",
    "密度": "0.789 g/mL",
    "闪点": "13 °C",
}

def print_example_output():
    """打印示例输出"""
    print("="*60)
    print("化合物查询工具 - 示例输出（乙醇）")
    print("="*60)
    print("\n命令: python compound_query.py 'ethanol'")
    print("\n输出:")
    print("="*60)
    
    # 基本信息
    print("\n【基本信息】")
    basic_info = ['分子式', '分子量', '精确分子量']
    for key in basic_info:
        print(f"  {key:25s}: {example_result[key]}")
    
    # 物理化学性质
    print("\n【物理化学性质】")
    phys_chem = ['标准SMILES', '异构SMILES', 'InChI Key', 'IUPAC 名称', 
                 '氢键供体数', '氢键受体数', '可旋转键数', '拓扑极性表面积', '脂溶性 (XLogP3)']
    for key in phys_chem:
        if key in example_result:
            print(f"  {key:25s}: {example_result[key]}")
    
    # 热力学性质
    print("\n【热力学性质】")
    thermo = ['沸点', '熔点', '密度', '闪点']
    for key in thermo:
        print(f"  {key:25s}: {example_result[key]}")
    
    print("\n" + "="*60)
    
    # JSON 输出示例
    print("\nJSON 输出示例:")
    print("="*60)
    print(json.dumps(example_result, ensure_ascii=False, indent=2))
    print("="*60)

if __name__ == '__main__':
    print_example_output()
