import sys
import time
from pathlib import Path
from urllib.parse import quote_plus

def search_patent_links(search_term, output_dir="."):
    """
    生成专利搜索链接列表
    
    Args:
        search_term (str): 搜索关键词
        output_dir (str): 输出目录
    
    Returns:
        list: 搜索链接列表
    """
    # 各种专利搜索网站的URL模板
    patent_search_urls = {
        'WIPO PATENTSCOPE': f"https://patentscope.wipo.int/search/en/result.jsf?query={quote_plus(search_term)}",
        'Google Patents': f"https://patents.google.com/?q={quote_plus(search_term)}",
        'USPTO': f"https://ppubs.uspto.gov/pubwebapp/static/pages/landing.html?query={quote_plus(search_term)}",
        'EPO Espacenet': f"https://worldwide.espacenet.com/patent/search/family/{quote_plus(search_term)}?q={quote_plus(search_term)}",
        'CNIPA': f"http://pss-system.cponline.cnipa.gov.cn/pss/search/search!searchIndex.action?q={quote_plus(search_term)}"
    }
    
    # 保存搜索链接到文件
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    safe_filename = search_term.replace(' ', '_').replace('/', '_').replace(':', '_')
    search_file = output_path / f"{safe_filename}_search_links.txt"
    
    with open(search_file, 'w', encoding='utf-8') as f:
        f.write(f"专利搜索链接 - 搜索关键词: {search_term}\n")
        f.write("=" * 60 + "\n\n")
        
        for site_name, url in patent_search_urls.items():
            f.write(f"{site_name}:\n")
            f.write(f"{url}\n\n")
    
    print(f"搜索链接已保存到: {search_file}")
    
    # 同时在控制台显示链接
    print(f"\n{search_term} 专利搜索链接:")
    print("=" * 60)
    for site_name, url in patent_search_urls.items():
        print(f"\n{site_name}:")
        print(f"  {url}")
    
    return patent_search_urls

def create_search_report(search_term, output_dir="."):
    """
    创建详细的搜索报告
    
    Args:
        search_term (str): 搜索关键词
        output_dir (str): 输出目录
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    safe_filename = search_term.replace(' ', '_').replace('/', '_').replace(':', '_')
    report_file = output_path / f"{safe_filename}_patent_search_report.txt"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(f"专利搜索报告\n")
        f.write(f"搜索关键词: {search_term}\n")
        f.write(f"生成时间: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("搜索建议:\n")
        f.write("1. 使用多个关键词进行搜索 (如: 'tyk2', 'tyk2 inhibitor', 'kinase')\n")
        f.write("2. 尝试使用英文和中文关键词\n")
        f.write("3. 关注专利的公开日期和申请日期\n")
        f.write("4. 注意专利的法律状态\n")
        f.write("5. 检查专利的权利要求范围\n\n")
        
        f.write("常用专利数据库:\n")
        f.write("- WIPO PATENTSCOPE: 国际专利数据库\n")
        f.write("- Google Patents: 简单易用的专利搜索工具\n")
        f.write("- USPTO: 美国专利商标局数据库\n")
        f.write("- EPO Espacenet: 欧洲专利局数据库\n")
        f.write("- CNIPA: 中国国家知识产权局专利数据库\n\n")
        
        f.write("专利下载:\n")
        f.write("- 大部分专利提供PDF格式全文\n")
        f.write("- WIPO和Google Patents通常提供免费下载\n")
        f.write("- 某些专利可能需要注册或付费\n\n")
        
        f.write("注意事项:\n")
        f.write("- 专利具有地域性和时间限制\n")
        f.write("- 引用专利时请注明专利号和来源\n")
        f.write("- 商业用途前请咨询法律专业人士\n")
    
    print(f"搜索报告已保存到: {report_file}")

def main():
    import time  # 导入time模块
    
    if len(sys.argv) < 2:
        print("使用方法: python fetch_patent.py <search_term> [output_dir]")
        print("")
        print("参数说明:")
        print("  search_term: 搜索关键词（蛋白名称、化合物名称等）")
        print("  output_dir: 输出目录（可选，默认为当前目录）")
        print("")
        print("示例:")
        print("  python fetch_patent.py \"tyk2 inhibitor\"")
        print("  python fetch_patent.py \"kinase\" ./patents")
        print("  python fetch_patent.py \"蛋白激酶\" ./patents")
        print("")
        print("功能说明:")
        print("  - 生成多个专利数据库的搜索链接")
        print("  - 创建详细的专利搜索报告")
        print("  - 提供搜索和下载指导")
        print("  - 保存所有链接到文件，方便后续查询")
        sys.exit(1)
    
    search_term = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    print(f"专利搜索工具")
    print(f"搜索关键词: {search_term}")
    print(f"输出目录: {output_dir}")
    print("=" * 60)
    print()
    
    # 生成搜索链接
    search_patent_links(search_term, output_dir)
    
    print()
    print("=" * 60)
    print()
    
    # 创建搜索报告
    create_search_report(search_term, output_dir)
    
    print()
    print("完成!")
    print(f"所有文件已保存到: {output_dir}")
    print()
    print("提示:")
    print("1. 点击上面的链接进行专利搜索")
    print("2. 查看详细的搜索报告获取更多指导")
    print("3. 根据搜索结果手动下载相关专利文件")

if __name__ == "__main__":
    main()