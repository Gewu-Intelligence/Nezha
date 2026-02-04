import requests
import sys
from pathlib import Path

def search_uniprot_by_name(protein_name):
    """
    根据蛋白名称搜索UniProt ID
    
    Args:
        protein_name (str): 蛋白名称
    
    Returns:
        dict: 搜索结果列表
    """
    base_url = "https://rest.uniprot.org/uniprotkb/search"
    
    try:
        # 构建搜索查询
        query = f"{protein_name} AND reviewed:true AND organism_id:9606"
        
        response = requests.get(base_url, params={
            'query': query,
            'format': 'json',
            'fields': 'accession,protein_name,organism_name,xref_pdb',
            'size': 5  # 限制返回前5个结果
        })
        response.raise_for_status()
        
        data = response.json()
        
        # 提取搜索结果
        results = []
        for item in data.get('results', []):
            # 提取PDB ID数量
            cross_refs = item.get('uniProtKBCrossReferences', [])
            pdb_count = sum(1 for ref in cross_refs if ref.get('database') == 'PDB')
            
            results.append({
                'uniprot_id': item.get('primaryAccession'),
                'protein_name': item.get('protein', {}).get('recommendedName', {}).get('fullName', {}).get('value', 'Unknown'),
                'organism': item.get('organism', {}).get('scientificName'),
                'pdb_count': pdb_count
            })
        
        return results
        
    except Exception as e:
        raise ValueError(f"搜索时出错: {e}")

def get_uniprot_data(uniprot_id):
    """
    从UniProt获取蛋白数据
    
    Args:
        uniprot_id (str): UniProt蛋白ID (例如: P12345)
    
    Returns:
        dict: 包含蛋白信息的字典
    """
    base_url = "https://rest.uniprot.org/uniprotkb"
    
    try:
        # 获取蛋白基本信息
        info_response = requests.get(f"{base_url}/{uniprot_id}")
        info_response.raise_for_status()
        protein_data = info_response.json()
        
        # 获取FASTA序列
        fasta_response = requests.get(f"{base_url}/{uniprot_id}.fasta")
        fasta_response.raise_for_status()
        fasta_sequence = fasta_response.text
        
        # 提取标准名称
        protein_name = protein_data.get('proteinDescription', {}).get('recommendedName', {}).get('fullName', {}).get('value', 'Unknown')
        if protein_name == 'Unknown':
            # 如果没有推荐名称，尝试获取其他名称
            alternative_names = protein_data.get('proteinDescription', {}).get('alternativeNames', [])
            if alternative_names:
                protein_name = alternative_names[0].get('fullName', {}).get('value', 'Unknown')
        
        # 提取PDB ID
        pdb_ids = []
        cross_refs = protein_data.get('uniProtKBCrossReferences', [])
        for ref in cross_refs:
            if ref.get('database') == 'PDB':
                pdb_id = ref.get('id', '')
                if pdb_id:
                    pdb_ids.append(pdb_id)
        
        return {
            'uniprot_id': uniprot_id,
            'protein_name': protein_name,
            'pdb_ids': pdb_ids,
            'fasta_sequence': fasta_sequence
        }
        
    except requests.exceptions.HTTPError as e:
        if hasattr(e, 'response') and e.response.status_code == 404:
            raise ValueError(f"UniProt ID '{uniprot_id}' 未找到")
        else:
            raise ValueError(f"HTTP错误: {e}")
    except Exception as e:
        raise ValueError(f"获取数据时出错: {e}")

def save_data(data, output_dir="."):
    """
    保存蛋白数据到文件
    
    Args:
        data (dict): 蛋白数据
        output_dir (str): 输出目录
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 保存FASTA文件
    fasta_file = output_path / f"{data['uniprot_id']}.fasta"
    with open(fasta_file, 'w') as f:
        f.write(data['fasta_sequence'])
    print(f"FASTA文件已保存到: {fasta_file}")
    
    # 保存蛋白信息
    info_file = output_path / f"{data['uniprot_id']}_info.txt"
    with open(info_file, 'w') as f:
        f.write(f"UniProt ID: {data['uniprot_id']}\n")
        f.write(f"Protein Name: {data['protein_name']}\n")
        f.write(f"PDB IDs: {', '.join(data['pdb_ids']) if data['pdb_ids'] else 'None'}\n")
    print(f"蛋白信息已保存到: {info_file}")

def interactive_search(protein_name):
    """
    交互式搜索并选择结果
    
    Args:
        protein_name (str): 蛋白名称
    
    Returns:
        str: 选择的UniProt ID
    """
    try:
        results = search_uniprot_by_name(protein_name)
        
        if not results:
            raise ValueError(f"未找到名称包含 '{protein_name}' 的蛋白")
        
        print(f"\n找到 {len(results)} 个匹配结果:")
        for i, result in enumerate(results, 1):
            pdb_info = f" [{result['pdb_count']} PDB structures]" if result['pdb_count'] > 0 else ""
            print(f"{i}. {result['uniprot_id']} - {result['protein_name']} ({result['organism']}){pdb_info}")
        
        while True:
            try:
                choice = input("\n请选择编号 (输入数字1-{}) 或输入 'q' 取消: ".format(len(results)))
                if choice.lower() == 'q':
                    return None
                
                index = int(choice) - 1
                if 0 <= index < len(results):
                    return results[index]['uniprot_id']
                else:
                    print("请输入有效的编号!")
                    
            except ValueError:
                print("请输入数字!")
                
    except Exception as e:
        print(f"搜索失败: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("使用方法:")
        print("  1. 根据UniProt ID查询: python fetch_uniprot.py <uniprot_id> [output_dir]")
        print("  2. 根据蛋白名称搜索: python fetch_uniprot.py name:<protein_name> [output_dir]")
        print("示例:")
        print("  python fetch_uniprot.py P12345")
        print("  python fetch_uniprot.py name:hemoglobin")
        print("  python fetch_uniprot.py name:insulin ./output")
        sys.exit(1)
    
    input_str = sys.argv[1].strip()
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    # 判断是UniProt ID还是名称搜索
    if input_str.startswith('name:'):
        protein_name = input_str[5:]  # 去掉 'name:' 前缀
        print(f"正在搜索蛋白名称: {protein_name}...")
        
        uniprot_id = interactive_search(protein_name)
        if not uniprot_id:
            print("搜索已取消")
            return
    else:
        uniprot_id = input_str
    
    print(f"\n正在获取UniProt ID: {uniprot_id} 的数据...")
    
    try:
        data = get_uniprot_data(uniprot_id)
        
        print(f"\n成功获取数据:")
        print(f"UniProt ID: {data['uniprot_id']}")
        print(f"Protein Name: {data['protein_name']}")
        print(f"PDB IDs: {', '.join(data['pdb_ids']) if data['pdb_ids'] else 'None'}")
        print(f"FASTA序列长度: {len(data['fasta_sequence'].split(chr(10))[1:])} 氨基酸")
        
        save_data(data, output_dir)
        print("\n完成!")
        
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()