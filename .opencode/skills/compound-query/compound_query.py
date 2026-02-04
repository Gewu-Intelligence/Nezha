#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
化合物性质查询工具
基于 PubChemPy 查询化合物信息
支持 SMILES、CAS 号、IUPAC 名称输入
"""

import argparse
import json
import sys
import time
from typing import Dict, Any, Optional
from datetime import datetime


try:
    import pubchempy as pcp
except ImportError:
    print("错误: 未安装 pubchempy 包")
    print("请运行: pip install pubchempy")
    sys.exit(1)


class CompoundQuery:
    """化合物查询类"""
    
    # PubChem 属性代码映射
    PROPERTY_MAPPING = {
        'Molecular Formula': '分子式',
        'Molecular Weight': '分子量',
        'Isomeric SMILES': '异构 SMILES',
        'Canonical SMILES': '标准 SMILES',
        'InChI': 'InChI',
        'InChI Key': 'InChI Key',
        'IUPAC Name': 'IUPAC 名称',
        'XLogP3-AA': '脂溶性 (XLogP3)',
        'Hydrogen Bond Donor Count': '氢键供体数',
        'Hydrogen Bond Acceptor Count': '氢键受体数',
        'Rotatable Bond Count': '可旋转键数',
        'Exact Mass': '精确分子量',
        'Monoisotopic Mass': '单同位素质量',
        'Topological Polar Surface Area': '拓扑极性表面积',
        'Complexity': '复杂度',
        'Charge': '电荷',
        'Heavy Atom Count': '重原子数',
        'Isotope Atom Count': '同位素原子数',
        'Defined Atom Stereocenter Count': '定义的立体中心数',
        'Undefined Atom Stereocenter Count': '未定义的立体中心数',
        'Defined Bond Stereocenter Count': '定义的键立体中心数',
        'Undefined Bond Stereocenter Count': '未定义的键立体中心数',
        'Covalently-Bonded Unit Count': '共价键单元数',
        'Compound Is Canonicalized': '是否规范化',
        'Melting Point': '熔点',
        'Boiling Point': '沸点',
        'Flash Point': '闪点',
        'Density': '密度',
        'Solubility': '溶解度',
        'Vapor Pressure': '蒸气压',
        'Surface Tension': '表面张力',
        'Viscosity': '粘度',
        'Refractive Index': '折射率',
        'pKa': '酸解离常数 (pKa)',
        'LogP': '脂溶性 (LogP)',
        'LogS': '水溶性 (LogS)',
        'pKa (strongest acidic)': '最强酸性 pKa',
        'pKa (strongest basic)': '最强碱性 pKa',
    }
    
    def __init__(self, identifier: str, identifier_type: Optional[str] = None):
        """
        初始化查询
        
        Args:
            identifier: 化合物标识符（SMILES、CAS 或 IUPAC 名称）
            identifier_type: 标识符类型（可选）
        """
        self.identifier = identifier
        self.identifier_type = identifier_type
        self.compound = None
        self.cid = None
        self.properties = {}
    
    def query(self, max_retries: int = 3, retry_delay: int = 2) -> bool:
        """
        查询化合物
        
        Args:
            max_retries: 最大重试次数
            retry_delay: 重试延迟（秒）
        
        Returns:
            bool: 是否查询成功
        """
        for attempt in range(max_retries):
            try:
                # 尝试使用不同方式查询
                if self.identifier_type:
                    self.compound = self._query_by_type()
                else:
                    self.compound = self._auto_detect_and_query()
                
                if self.compound:
                    self.cid = self.compound.cid
                    return True
                return False
            
            except pcp.ServerBusyError:
                if attempt < max_retries - 1:
                    print(f"服务器繁忙，等待 {retry_delay} 秒后重试...")
                    time.sleep(retry_delay)
                else:
                    print("错误: PubChem 服务器繁忙，请稍后重试")
                    return False
            
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"查询错误: {e}，重试中...")
                    time.sleep(retry_delay)
                else:
                    print(f"查询错误: {e}")
                    return False
        
        return False
    
    def _auto_detect_and_query(self):
        """自动检测标识符类型并查询"""
        # 尝试按 SMILES 查询
        if self._is_smiles(self.identifier):
            try:
                return pcp.get_compounds(self.identifier, 'smiles')[0]
            except:
                pass
        
        # 尝试按 IUPAC 名称查询
        try:
            return pcp.get_compounds(self.identifier, 'name')[0]
        except:
            pass
        
        # 尝试按 CID 查询
        if self.identifier.isdigit():
            try:
                return pcp.Compound.from_cid(int(self.identifier))
            except:
                pass
        
        return None
    
    def _query_by_type(self):
        """按指定类型查询"""
        type_mapping = {
            'smiles': 'smiles',
            'smls': 'smiles',
            'cas': 'name',
            'name': 'name',
            'iupac': 'name',
            'cid': 'cid',
        }
        
        query_type = type_mapping.get(self.identifier_type.lower(), 'name')
        
        if query_type == 'cid':
            return pcp.Compound.from_cid(int(self.identifier))
        else:
            return pcp.get_compounds(self.identifier, query_type)[0]
    
    def _is_smiles(self, s: str) -> bool:
        """判断是否为 SMILES 格式"""
        smiles_chars = set('CNOFClBrSI()=#[]@+-\\/')
        return len(s) > 1 and all(c in smiles_chars or c.isalnum() for c in s)
    
    def get_all_properties(self) -> Dict[str, Any]:
        """
        获取所有性质
        
        Returns:
            dict: 化合物性质字典
        """
        if not self.compound:
            return {}
        
        # 获取所有可用属性
        all_properties = pcp.get_properties(
            list(self.PROPERTY_MAPPING.keys()), 
            self.cid
        )
        
        if all_properties:
            properties = all_properties[0]
            
            # 映射到中文名称
            self.properties = {}
            for key, chinese_name in self.PROPERTY_MAPPING.items():
                if key in properties and properties[key] is not None:
                    self.properties[chinese_name] = properties[key]
        
        # 添加基本信息
        self.properties['PubChem CID'] = self.cid
        if self.compound.synonyms:
            self.properties['同义词'] = self.compound.synonyms[:5]  # 只显示前5个
        
        return self.properties
    
    def print_properties(self, output_format: str = 'table'):
        """
        打印化合物性质
        
        Args:
            output_format: 输出格式 ('table', 'json')
        """
        if not self.compound:
            print("未找到化合物信息")
            return
        
        print(f"\n{'='*60}")
        print(f"化合物查询结果")
        print(f"{'='*60}")
        print(f"查询内容: {self.identifier}")
        print(f"PubChem CID: {self.cid}")
        print(f"{'='*60}\n")
        
        if output_format == 'json':
            print(json.dumps(self.properties, ensure_ascii=False, indent=2))
        else:
            self._print_table()
    
    def _print_table(self):
        """以表格形式打印性质"""
        if not self.properties:
            print("未找到性质信息")
            return
        
        # 分类显示
        basic_info = {}
        physicochemical = {}
        thermodynamic = {}
        
        for key, value in self.properties.items():
            if key in ['分子式', '分子量', '精确分子量', '单同位素质量', 'InChI', 'InChI Key']:
                basic_info[key] = value
            elif key in ['熔点', '沸点', '闪点', '密度', 'pKa', 'LogP', 'LogS']:
                thermodynamic[key] = value
            else:
                physicochemical[key] = value
        
        # 基本信息
        if basic_info:
            print("【基本信息】")
            for key, value in basic_info.items():
                print(f"  {key:25s}: {value}")
            print()
        
        # 物理化学性质
        if physicochemical:
            print("【物理化学性质】")
            for key, value in physicochemical.items():
                if key == '同义词':
                    print(f"  {key:25s}: {', '.join(value[:3])}...")
                elif key == 'PubChem CID':
                    pass
                else:
                    print(f"  {key:25s}: {value}")
            print()
        
        # 热力学性质
        if thermodynamic:
            print("【热力学性质】")
            for key, value in thermodynamic.items():
                print(f"  {key:25s}: {value}")
            print()
        
        print(f"{'='*60}\n")
    
    def save_to_file(self, filename: str, output_format: str = 'json'):
        """
        保存到文件
        
        Args:
            filename: 文件名
            output_format: 输出格式 ('json', 'csv')
        """
        if not self.properties:
            print("没有可保存的数据")
            return False
        
        try:
            if output_format == 'json':
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.properties, f, ensure_ascii=False, indent=2)
            
            elif output_format == 'csv':
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['性质', '值'])
                    for key, value in self.properties.items():
                        if key != '同义词':
                            writer.writerow([key, value])
            
            print(f"数据已保存到: {filename}")
            return True
        
        except Exception as e:
            print(f"保存失败: {e}")
            return False


def main():
    parser = argparse.ArgumentParser(
        description='查询化合物性质',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
示例用法:
  %(prog)s "CCO"                          # 使用 SMILES
  %(prog)s "ethanol"                      # 使用名称
  %(prog)s "64-17-5" -t cas               # 指定类型为 CAS
  %(prog)s "CCO" -o result.json          # 保存为 JSON
  %(prog)s "ethanol" -f csv -o data.csv  # 保存为 CSV
        '''
    )
    
    parser.add_argument('identifier', help='化合物标识符（SMILES、CAS 或 IUPAC 名称）')
    parser.add_argument('-t', '--type', 
                       choices=['smiles', 'smls', 'cas', 'name', 'iupac', 'cid'],
                       help='标识符类型（可选）')
    parser.add_argument('-f', '--format', 
                       choices=['table', 'json', 'csv'],
                       default='table',
                       help='输出格式（默认: table）')
    parser.add_argument('-o', '--output', help='保存到文件')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='显示详细信息')
    
    args = parser.parse_args()
    
    # 查询化合物
    query = CompoundQuery(args.identifier, args.type)
    
    if args.verbose:
        print(f"正在查询: {args.identifier}")
        if args.type:
            print(f"类型: {args.type}")
    
    success = query.query()
    
    if not success:
        print(f"错误: 未找到化合物 '{args.identifier}'")
        print("提示: 请检查输入是否正确")
        sys.exit(1)
    
    # 获取所有性质
    query.get_all_properties()
    
    # 输出结果
    output_format = args.format
    
    if args.output:
        if args.format == 'table':
            # 如果指定了输出文件但格式是 table，默认用 json
            output_format = 'json'
        query.save_to_file(args.output, output_format)
    else:
        query.print_properties(output_format)


if __name__ == '__main__':
    main()
