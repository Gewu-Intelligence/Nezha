#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试 POP3 连接，帮助诊断 163 邮箱问题"""

import poplib
import sys

def test_pop3(server: str, port: int, username: str, password: str):
    """测试 POP3 连接"""
    print(f"测试 POP3 连接: {server}:{port}")
    print("-" * 50)
    
    try:
        if port == 995:
            print("使用 SSL 连接...")
            mail = poplib.POP3_SSL(server, port, timeout=10)
        else:
            print("使用普通连接...")
            mail = poplib.POP3(server, port, timeout=10)
        
        print(f"✓ 连接成功: {mail.getwelcome().decode('utf-8', errors='ignore')}")
        
        print(f"正在登录: {username}")
        mail.user(username)
        mail.pass_(password)
        print("✓ 登录成功")
        
        mail_list = mail.list()
        num_messages = len(mail_list[1])
        print(f"✓ 服务器上有 {num_messages} 封邮件")
        
        if num_messages > 0:
            print("\n最新邮件列表:")
            for i, msg_id in enumerate(mail_list[1][-5:]):  # 显示最新5封
                print(f"  {msg_id.decode('utf-8', errors='ignore')}")
        
        mail.quit()
        return True
    
    except poplib.error_proto as e:
        error_msg = str(e)
        print(f"✗ POP3 协议错误")
        
        if 'ERR' in error_msg.upper():
            if 'LOGIN' in error_msg.upper() or 'AUTH' in error_msg.upper():
                print("  认证失败: 用户名或密码错误")
                print("  提示:")
                print("  1. 检查用户名是否正确（需要完整的邮箱地址）")
                print("  2. 检查密码是否为 163 邮箱授权码（不是登录密码）")
                print("  3. 前往 163 邮箱设置 -> POP3/SMTP/IMAP 开启服务并获取授权码")
            else:
                print(f"  服务器错误: {error_msg}")
        else:
            print(f"  错误: {error_msg}")
        
        return False
    
    except ConnectionRefusedError:
        print(f"✗ 连接被拒绝: {server}:{port}")
        print("  提示:")
        print("  1. 检查服务器地址是否正确")
        print("  2. 检查端口是否正确（995 为 SSL，110 为普通）")
        print("  3. 检查网络连接")
        print("  4. 163 邮箱 POP3 服务器应为: pop.163.com:995")
        return False
    
    except TimeoutError:
        print("✗ 连接超时")
        print("  提示:")
        print("  1. 检查网络连接")
        print("  2. 检查服务器地址是否正确")
        print("  3. 尝试使用其他网络")
        return False
    
    except Exception as e:
        print(f"✗ 未知错误: {e}")
        return False

def main():
    import argparse
    import yaml
    
    parser = argparse.ArgumentParser(description='测试 POP3 连接')
    parser.add_argument('--config', '-c', default='email_config.yaml', 
                       help='配置文件路径')
    
    args = parser.parse_args()
    
    try:
        with open(args.config, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"错误: 配置文件不存在: {args.config}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"错误: 配置文件格式错误: {e}")
        sys.exit(1)
    
    pop3_server = config.get('pop3', {}).get('server')
    pop3_port = config.get('pop3', {}).get('port')
    username = config.get('account', {}).get('username')
    password = config.get('account', {}).get('password')
    
    if not all([pop3_server, pop3_port, username, password]):
        print("错误: 配置文件缺少必要字段")
        print(f"pop3_server: {pop3_server}")
        print(f"pop3_port: {pop3_port}")
        print(f"username: {username}")
        print(f"password: {'已设置' if password else '未设置'}")
        sys.exit(1)
    
    print("=" * 50)
    print("POP3 连接测试")
    print("=" * 50)
    print(f"服务器: {pop3_server}:{pop3_port}")
    print(f"邮箱: {username}")
    print("=" * 50)
    print()
    
    result = test_pop3(pop3_server, pop3_port, username, password)
    
    print("\n" + "=" * 50)
    if result:
        print("✓ 测试成功！配置正确。")
        print("\n您现在可以使用以下命令接收邮件:")
        print(f"python email_handler.py receive-pop -l 10")
        sys.exit(0)
    else:
        print("✗ 测试失败，请根据上述提示检查配置。")
        sys.exit(1)

if __name__ == '__main__':
    main()
