import requests
import sys
import csv
from pathlib import Path
import argparse

def download_pdb_file(pdb_id, output_dir=".", format_type="pdb"):
    """
    从RCSB PDB数据库下载PDB文件
    
    Args:
        pdb_id (str): PDB ID (例如: 4E1Z)
        output_dir (str): 输出目录
        format_type (str): 文件类型，可选: 'pdb', 'cif', 'mmCIF'
    
    Returns:
        str: 下载的文件路径
    """
    # RCSB PDB文件下载URL
    base_url = "https://files.rcsb.org/download"
    
    # 根据格式类型选择文件扩展名
    if format_type.lower() in ['mmcif', 'cif']:
        file_extension = ".cif"
        format_name = "mmCIF"
    else:
        file_extension = ".pdb"
        format_name = "PDB"
    
    pdb_id = pdb_id.upper().strip()
    url = f"{base_url}/{pdb_id}{file_extension}"
    
    try:
        print(f"正在从 {url} 下载...")
        
        download_response = requests.get(url, stream=True)
        download_response.raise_for_status()
        
        # 创建输出目录
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # 保存文件
        file_path = output_path / f"{pdb_id}{file_extension}"
        
        with open(file_path, 'wb') as f:
            for chunk in download_response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"成功下载: {file_path}")
        print(f"文件大小: {file_path.stat().st_size} bytes")
        
        return str(file_path)
        
    except requests.exceptions.HTTPError as e:
        if hasattr(e, 'response') and e.response.status_code == 404:
            raise ValueError(f"PDB ID '{pdb_id}' 未找到")
        else:
            raise ValueError(f"HTTP错误: {e}")
    except Exception as e:
        raise ValueError(f"下载失败: {e}")

def get_pdb_info(pdb_id):
    """
    获取PDB文件的基本信息
    
    Args:
        pdb_id (str): PDB ID
    
    Returns:
        dict: 包含PDB信息的字典
    """
    base_url = "https://data.rcsb.org/rest/v1/core/entry"
    pdb_id = pdb_id.upper().strip()
    
    try:
        response = requests.get(f"{base_url}/{pdb_id}")
        response.raise_for_status()
        data = response.json()
        
        info = {
            'pdb_id': pdb_id,
            'title': data.get('struct', {}).get('title', 'Unknown'),
            'deposition_date': data.get('rcsb_accession_info', {}).get('deposit_date', 'Unknown'),
            'resolution': 'Unknown',
            'experimental_method': 'Unknown'
        }
        
        # 获取实验方法
        if 'exptl' in data and data['exptl']:
            info['experimental_method'] = data['exptl'][0].get('method', 'Unknown')
        
        # 获取分辨率信息
        if 'rcsb_entry_info' in data:
            info['resolution'] = data['rcsb_entry_info'].get('resolution_combined', [None])[0]
            if info['resolution']:
                info['resolution'] = f"{info['resolution']:.2f} Å"
        
        return info
        
    except Exception as e:
        raise ValueError(f"获取PDB信息失败: {e}")

def main():
    parser = argparse.ArgumentParser(description='下载PDB文件')
    parser.add_argument('--info_file', default=None, 
                       help='PDB ID文件 (默认: None)')
    parser.add_argument('--pdb_id', default=None, 
                       help='PDB ID号 (默认: None)')
    parser.add_argument('--output_dir', default='PDB_file', 
                       help='输出文件夹 (默认: PDB_file)')
    parser.add_argument('--output_format', default='pdb', 
                       help='文件格式 (默认: pdb)')

    args = parser.parse_args()
    pdb_ids = []
    if (args.info_file is None) and (args.pdb_id is None):
        print("使用方法: python fetch_pdb.py --info-file <info_file> --pdb-id <pdb_id> --output-dir [output_dir]")
        print("")
        print("参数说明:")
        print("  pdb-id: PDB ID (例如: 4E1Z)")
        print("  info_file: info file (例如: P29597_info.txt)")
        print("  output-dir: 输出目录 (可选，默认为当前目录)")
        print("  output-format: 文件格式 (可选，默认为 pdb)")
        print("         - pdb: PDB格式")
        print("         - cif: mmCIF格式")
        print("")
        sys.exit(1)

    if args.info_file is not None:
        with open(args.info_file) as inf:
            lines = inf.readlines()
        for line in lines:
            ss = line.split(":")
            if ss[0].strip() == "PDB IDs":
                pdb_ids = [s.strip() for s in ss[1].split(",")]
    if args.pdb_id is not None:
        pdb_ids.append(args.pdb_id)

    output_dir = args.output_dir
    format_type = args.output_format
    
    print(f"PDB ID: {', '.join([pdb_id.upper() for pdb_id in pdb_ids])}")
    print(f"输出目录: {output_dir}")
    print(f"文件格式: {format_type}")
    print()
    pdb_file_infos = []
    for pdb_id in pdb_ids:
        try:
            # 获取PDB信息
            file_path = download_pdb_file(pdb_id, output_dir, format_type)
            print("正在获取PDB信息...")
            pdb_info = get_pdb_info(pdb_id)
            pdb_file_infos.append({"pdb-id":pdb_id.upper(),
                                   "title":pdb_info['title'],
                                   "expt-method":pdb_info['experimental_method'],
                                   "resolution":pdb_info['resolution'],
                                   "date":pdb_info['deposition_date'],
                                   "file-path":file_path
                                   })
        
        
            # 下载PDB文件
            
        
            # 保存PDB信息
            #info_file = Path(output_dir) / f"{pdb_id.upper()}_info.txt"
            #with open(info_file, 'w', encoding='utf-8') as f:
            #    f.write(f"PDB ID: {pdb_info['pdb_id']}\n")
            #    f.write(f"标题: {pdb_info['title']}\n")
            #    f.write(f"实验方法: {pdb_info['experimental_method']}\n")
            #    f.write(f"分辨率: {pdb_info['resolution']}\n")
            #    f.write(f"提交日期: {pdb_info['deposition_date']}\n")
            #    f.write(f"文件路径: {file_path}\n")
        
            #print(f"PDB信息已保存到: {info_file}")
            #print("\n下载完成!")
        
        except Exception as e:
            print(f"错误: {e}")
            #sys.exit(1)
    if len(pdb_file_infos) > 0:
        pdb_file_infos = sorted(pdb_file_infos,key=lambda x:x["resolution"])
        pdb_file_infos = sorted(pdb_file_infos,key=lambda x:x["pdb-id"][0],reverse=True)
        fields = ["pdb-id","title","expt-method","resolution","date","file-path"]
        with open(f"{output_dir}/pdb_infos.csv",'w') as outf:
            writer = csv.DictWriter(outf,fieldnames=fields)
            writer.writeheader()
            writer.writerows(pdb_file_infos)
        if len(pdb_file_infos) > 1:
            print(f"建议使用分辨率最高的PDB文件: {pdb_file_infos[0]['pdb-id']}")
    else:
        print("没有找到任何PDB文件")

if __name__ == "__main__":
    main()