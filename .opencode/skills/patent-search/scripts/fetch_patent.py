import requests
import sys
import time
from pathlib import Path
from urllib.parse import quote_plus
import json

def search_google_patents(query, max_results=20):
    """
    使用Google Patents搜索专利
    
    Args:
        query (str): 搜索查询词
        max_results (int): 最大返回结果数
    
    Returns:
        list: 专利信息列表
    """
    print(f"正在搜索专利，关键词: {query}...")
    
    # Google Patents搜索页面URL
    base_url = "https://patents.google.com"
    search_url = f"{base_url}/?q={quote_plus(query)}"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # 发送搜索请求
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        # 使用BeautifulSoup解析HTML
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            patents = []
            
            # 尝试查找专利链接
            patent_links = soup.find_all('a', href=True)
            href_links = [a for a in patent_links if '/patent/' in str(a.get('href', ''))]
            
            print(f"找到 {len(href_links)} 个可能的专利链接")
            
            for i, link in enumerate(href_links[:max_results], 1):
                try:
                    # 提取专利号
                    href = str(link.get('href', ''))
                    if '/patent/' in href:
                        # 从URL中提取专利号
                        parts = href.split('/patent/')
                        if len(parts) > 1:
                            patent_number = parts[1].split('/')[0]
                            # 清理专利号
                            patent_number = patent_number.replace('?oq', '').split('?')[0]
                            
                            if len(patent_number) > 3 and len(patent_number) < 30:  # 合理的专利号长度
                                title = link.get_text(strip=True)
                                if not title or len(title) > 200:
                                    title = f"Patent {patent_number}"
                                
                                patent_info = {
                                    'patent_number': patent_number,
                                    'title': title,
                                    'assignee': 'Unknown',
                                    'abstract': '',
                                    'url': base_url + '/patent/' + patent_number,
                                    'pdf_url': f"{base_url}/patent/{patent_number}?oq={patent_number}"
                                }
                                
                                patents.append(patent_info)
                                
                                print(f"\n{i}. 专利号: {patent_number}")
                                print(f"   标题: {title[:80]}...")
                except Exception as e:
                    continue
            
            # 去重
            seen = set()
            unique_patents = []
            for patent in patents:
                if patent['patent_number'] not in seen:
                    seen.add(patent['patent_number'])
                    unique_patents.append(patent)
            
            print(f"\n找到 {len(unique_patents)} 个唯一专利")
            return unique_patents
            
        except ImportError:
            print("未安装BeautifulSoup")
            return []
        
    except requests.exceptions.Timeout:
        print("搜索超时，网络连接可能有问题")
        return []
    except Exception as e:
        print(f"搜索出错: {e}")
        return []

def create_demo_patents(query, count=10):
    """
    创建演示用专利数据（当搜索失败时使用）
    
    Args:
        query (str): 搜索关键词
        count (int): 创建的专利数量
    
    Returns:
        list: 演示专利信息列表
    """
    print(f"创建演示专利数据...")
    
    demo_patents = []
    base_url = "https://patents.google.com"
    
    # 创建一些合理的演示数据
    demo_data = [
        {
            'patent_number': 'US20230123456',
            'title': f'Methods and compounds for treating {query}-related diseases',
            'assignee': 'Pharmaceutical Corp.',
            'abstract': f'This invention relates to novel compounds and methods for treating diseases associated with {query}. The compounds provided herein demonstrate improved efficacy and safety profiles.',
            'url': f"{base_url}/patent/US20230123456",
            'pdf_url': f"{base_url}/patent/US20230123456?oq=US20230123456"
        },
        {
            'patent_number': 'WO2023123456',
            'title': f'Kinase inhibitors and their therapeutic applications',
            'assignee': 'Biotech Innovations Ltd.',
            'abstract': f'Disclosed are kinase inhibitors effective against {query} and their use in treating various medical conditions. The invention provides pharmaceutical compositions and methods of use.',
            'url': f"{base_url}/patent/WO2023123456",
            'pdf_url': f"{base_url}/patent/WO2023123456?oq=WO2023123456"
        },
        {
            'patent_number': 'EP3123456',
            'title': f'Novel therapeutic agents targeting {query}',
            'assignee': 'European Pharma AG',
            'abstract': f'The present invention relates to novel therapeutic agents that target {query}. These agents show promise for the treatment of various disorders.',
            'url': f"{base_url}/patent/EP3123456",
            'pdf_url': f"{base_url}/patent/EP3123456?oq=EP3123456"
        },
        {
            'patent_number': 'CN115678901',
            'title': f'{query} inhibitor compositions and methods',
            'assignee': 'China Medical Research Institute',
            'abstract': f'This invention provides {query} inhibitor compositions and methods for their preparation. The compositions exhibit excellent therapeutic effects.',
            'url': f"{base_url}/patent/CN115678901",
            'pdf_url': f"{base_url}/patent/CN115678901?oq=CN115678901"
        },
        {
            'patent_number': 'JP2023012345',
            'title': f'Drug discovery methods for {query} modulators',
            'assignee': 'Tokyo Pharmaceuticals',
            'abstract': f'A method for discovering {query} modulators using high-throughput screening. The method enables rapid identification of potential drug candidates.',
            'url': f"{base_url}/patent/JP2023012345",
            'pdf_url': f"{base_url}/patent/JP2023012345?oq=JP2023012345"
        }
    ]
    
    # 如果需要更多数据，复制并修改
    while len(demo_data) < count:
        base_patent = demo_data[len(demo_data) % len(demo_data)]
        new_patent = base_patent.copy()
        patent_num = len(demo_data) + 1
        new_patent['patent_number'] = f"US{20240000000 + patent_num}"
        demo_data.append(new_patent)
    
    return demo_data[:count]

def save_patent_list(patents, query, output_dir="."):
    """
    保存专利列表到文件
    
    Args:
        patents (list): 专利信息列表
        query (str): 搜索关键词
        output_dir (str): 输出目录
    """
    if not patents:
        return
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 保存为文本文件
    txt_file = output_path / f"{query.replace(' ', '_')}_patent_list.txt"
    with open(txt_file, 'w', encoding='utf-8') as f:
        f.write(f"专利搜索结果\n")
        f.write(f"搜索关键词: {query}\n")
        f.write(f"搜索时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"专利数量: {len(patents)}\n")
        f.write("=" * 60 + "\n\n")
        
        for i, patent in enumerate(patents, 1):
            f.write(f"{i}. 专利号: {patent['patent_number']}\n")
            f.write(f"   标题: {patent['title']}\n")
            f.write(f"   申请人: {patent['assignee']}\n")
            f.write(f"   详情链接: {patent['url']}\n")
            f.write(f"   PDF下载: {patent['pdf_url']}\n")
            if patent.get('abstract'):
                f.write(f"   摘要: {patent['abstract']}\n")
            f.write("\n")
    
    print(f"专利列表已保存到: {txt_file}")
    
    # 保存为JSON文件
    json_file = output_path / f"{query.replace(' ', '_')}_patent_list.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(patents, f, ensure_ascii=False, indent=2)
    
    print(f"专利数据已保存到: {json_file}")
    
    # 保存单独的专利信息文件
    for i, patent in enumerate(patents, 1):
        safe_number = patent['patent_number'].replace('/', '_').replace(' ', '').replace(':', '')
        info_file = output_path / f"{safe_number}_info.txt"
        
        with open(info_file, 'w', encoding='utf-8') as f:
            f.write(f"专利号: {patent['patent_number']}\n")
            f.write(f"标题: {patent['title']}\n")
            f.write(f"申请人: {patent['assignee']}\n")
            f.write(f"搜索关键词: {query}\n")
            f.write(f"搜索时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            if patent.get('abstract'):
                f.write(f"摘要: {patent['abstract']}\n")
            f.write(f"\n详情链接: {patent['url']}\n")
            f.write(f"PDF下载: {patent['pdf_url']}\n")
    
    print(f"单独专利信息已保存到 {output_path}")

def download_patent_pdfs(patents, output_dir="."):
    """
    下载专利PDF文件
    
    Args:
        patents (list): 专利信息列表
        output_dir (str): 输出目录
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    downloaded_count = 0
    failed_count = 0
    
    for i, patent in enumerate(patents, 1):
        safe_number = patent['patent_number'].replace('/', '_').replace(' ', '').replace(':', '')
        pdf_path = output_path / f"{safe_number}.pdf"
        
        print(f"\n[{i}/{len(patents)}] 尝试下载: {patent['patent_number']}")
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(patent['pdf_url'], headers=headers, timeout=10)
            
            # 检查是否是PDF
            if response.status_code == 200 and 'application/pdf' in response.headers.get('content-type', ''):
                with open(pdf_path, 'wb') as f:
                    f.write(response.content)
                file_size = pdf_path.stat().st_size
                print(f"  ✓ 成功下载: {pdf_path} ({file_size} bytes)")
                downloaded_count += 1
            else:
                print(f"  ✗ 无法下载PDF，状态码: {response.status_code}")
                print(f"  内容类型: {response.headers.get('content-type', 'Unknown')}")
                failed_count += 1
        
        except Exception as e:
            print(f"  ✗ 下载出错: {e}")
            failed_count += 1
        
        # 避免请求过于频繁
        time.sleep(0.5)
    
    print(f"\n下载完成:")
    print(f"  成功: {downloaded_count} 个")
    print(f"  失败: {failed_count} 个")
    return downloaded_count

def create_search_summary(query, output_dir="."):
    """
    创建搜索摘要文件
    
    Args:
        query (str): 搜索关键词
        output_dir (str): 输出目录
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    summary_file = output_path / f"{query.replace(' ', '_')}_search_summary.txt"
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write(f"专利搜索摘要\n")
        f.write(f"搜索关键词: {query}\n")
        f.write(f"搜索时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("搜索链接:\n")
        f.write(f"1. Google Patents: https://patents.google.com/?q={quote_plus(query)}\n")
        f.write(f"2. WIPO PATENTSCOPE: https://patentscope.wipo.int/search/en/result.jsf?query={quote_plus(query)}\n")
        f.write(f"3. USPTO: https://ppubs.uspto.gov/?q={quote_plus(query)}\n")
        f.write(f"4. EPO Espacenet: https://worldwide.espacenet.com/patent/search?q={quote_plus(query)}\n\n")
        
        f.write("使用说明:\n")
        f.write("1. 查看专利列表文件获取专利号和基本信息\n")
        f.write("2. 使用详情链接查看专利完整信息\n")
        f.write("3. 如需下载PDF，可使用PDF下载链接或手动下载\n")
        f.write("4. 建议使用多个数据库交叉验证搜索结果\n\n")
        
        f.write("注意事项:\n")
        f.write("- 专利具有地域性和时间限制\n")
        f.write("- 注意检查专利的法律状态\n")
        f.write("- 引用专利时请注明专利号和来源\n")
        f.write("- 商业用途前请咨询法律专业人士\n")
    
    print(f"搜索摘要已保存到: {summary_file}")

def main():
    if len(sys.argv) < 2:
        print("使用方法: python fetch_patent.py <search_term> [max_results] [output_dir] [--download-pdf] [--demo]")
        print("")
        print("参数说明:")
        print("  search_term: 搜索关键词（蛋白名称、化合物名称等）")
        print("  max_results: 最大返回结果数（可选，默认为20）")
        print("  output_dir: 输出目录（可选，默认为当前目录）")
        print("  --download-pdf: 下载PDF文件（可选，默认不下载）")
        print("  --demo: 使用演示数据（可选，当网络问题时使用）")
        print("")
        print("示例:")
        print("  python fetch_patent.py \"tyk2 inhibitor\"")
        print("  python fetch_patent.py \"tyk2 inhibitor\" 10 ./patents")
        print("  python fetch_patent.py \"tyk2 inhibitor\" 10 ./patents --download-pdf")
        print("  python fetch_patent.py \"tyk2 inhibitor\" 10 ./patents --demo")
        print("")
        print("功能:")
        print("  - 从Google Patents搜索专利")
        print("  - 提取专利号、标题、申请人等信息")
        print("  - 生成专利列表和单独信息文件")
        print("  - 支持PDF文件下载")
        print("  - 提供演示模式用于测试")
        print("")
        print("注意: 需要安装BeautifulSoup: pip install beautifulsoup4")
        sys.exit(1)
    
    search_term = sys.argv[1]
    
    # 解析参数
    max_results = 20
    output_dir = "."
    download_pdf = False
    demo_mode = False
    
    for arg in sys.argv[2:]:
        if arg.isdigit():
            max_results = int(arg)
        elif not arg.startswith('--'):
            output_dir = arg
        elif arg == '--download-pdf':
            download_pdf = True
        elif arg == '--demo':
            demo_mode = True
    
    print(f"专利搜索工具")
    print(f"搜索关键词: {search_term}")
    print(f"最大结果数: {max_results}")
    print(f"输出目录: {output_dir}")
    print(f"下载PDF: {'是' if download_pdf else '否'}")
    print(f"演示模式: {'是' if demo_mode else '否'}")
    print("=" * 60)
    print()
    
    # 搜索专利或使用演示数据
    if demo_mode:
        patents = create_demo_patents(search_term, max_results)
        print(f"\n使用演示数据，共 {len(patents)} 个专利")
    else:
        patents = search_google_patents(search_term, max_results)
        
        # 如果搜索失败，提供选项
        if not patents:
            print("\n搜索未找到结果")
            print("建议:")
            print("1. 检查网络连接")
            print("2. 尝试使用 --demo 参数查看演示")
            print("3. 手动访问以下链接搜索:")
            
            print(f"\n  Google Patents: https://patents.google.com/?q={quote_plus(search_term)}")
            print(f"  WIPO PATENTSCOPE: https://patentscope.wipo.int/search/en/result.jsf?query={quote_plus(search_term)}")
            
            # 创建搜索摘要
            create_search_summary(search_term, output_dir)
            print(f"\n搜索摘要已保存，包含所有搜索链接")
            sys.exit(0)
    
    print(f"\n处理 {len(patents)} 个专利")
    
    # 保存专利列表
    save_patent_list(patents, search_term, output_dir)
    
    # 创建搜索摘要
    create_search_summary(search_term, output_dir)
    
    # 下载PDF
    if download_pdf:
        print(f"\n开始下载PDF文件...")
        download_patent_pdfs(patents, output_dir)
    
    print(f"\n完成!")
    print(f"所有文件已保存到: {output_dir}")
    print("\n输出文件说明:")
    print(f"  - {search_term.replace(' ', '_')}_patent_list.txt: 专利列表")
    print(f"  - {search_term.replace(' ', '_')}_patent_list.json: JSON格式数据")
    print(f"  - {search_term.replace(' ', '_')}_search_summary.txt: 搜索摘要")
    print(f"  - [专利号]_info.txt: 单独专利信息")
    if download_pdf:
        print(f"  - [专利号].pdf: 专利PDF文件")

if __name__ == "__main__":
    main()