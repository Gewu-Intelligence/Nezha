#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""连接测试工具，帮助诊断邮件配置问题"""

import smtplib
import imaplib
import poplib
import sys

def test_smtp(server: str, port: int, username: str, password: str):
    """测试 SMTP 连接"""
    print(f"\n测试 SMTP 连接: {server}:{port}")
    print("-" * 50)
    
    try:
        if port == 465:
            print("使用 SSL 连接...")
            with smtplib.SMTP_SSL(server, port, timeout=10) as smtp:
                smtp.set_debuglevel(1)
                print("正在登录...")
                smtp.login(username, password)
                print("✓ SMTP 连接成功！")
        else:
            print("使用 STARTTLS 连接...")
            with smtplib.SMTP(server, port, timeout=10) as smtp:
                smtp.set_debuglevel(1)
                print("启动 TLS 加密...")
                smtp.starttls()
                print("正在登录...")
                smtp.login(username, password)
                print("✓ SMTP 连接成功！")
        return True
    except smtplib.SMTPAuthenticationError:
        print("✗ 认证失败：用户名或密码错误")
        print("  提示：Gmail 需要使用应用专用密码，QQ/163 需要使用授权码")
        return False
    except smtplib.SMTPException as e:
        print(f"✗ SMTP 错误: {e}")
        return False
    except ConnectionRefusedError:
        print(f"✗ 连接被拒绝：{server}:{port}")
        print("  提示：检查端口是否正确")
        return False
    except TimeoutError:
        print("✗ 连接超时")
        print("  提示：检查网络连接或服务器地址")
        return False
    except Exception as e:
        print(f"✗ 未知错误: {e}")
        return False

def test_imap(server: str, port: int, username: str, password: str):
    """测试 IMAP 连接"""
    print(f"\n测试 IMAP 连接: {server}:{port}")
    print("-" * 50)
    
    if not server:
        print("✗ IMAP 服务器未配置")
        return False
    
    try:
        print("正在连接...")
        with imaplib.IMAP4_SSL(server, port, timeout=10) as imap:
            print("正在登录...")
            imap.login(username, password)
            print("✓ IMAP 连接成功！")
            return True
    except imaplib.IMAP4.error as e:
        print(f"✗ IMAP 错误: {e}")
        print("  提示：检查用户名和密码")
        return False
    except ConnectionRefusedError:
        print(f"✗ 连接被拒绝：{server}:{port}")
        print("  提示：检查端口是否正确")
        return False
    except TimeoutError:
        print("✗ 连接超时")
        print("  提示：检查网络连接或服务器地址")
        return False
    except Exception as e:
        print(f"✗ 未知错误: {e}")
        return False

def test_pop3(server: str, port: int, username: str, password: str):
    """测试 POP3 连接"""
    print(f"\n测试 POP3 连接: {server}:{port}")
    print("-" * 50)
    
    if not server:
        print("✗ POP3 服务器未配置")
        return False
    
    try:
        if port == 995:
            print("使用 SSL 连接...")
            mail = poplib.POP3_SSL(server, port, timeout=10)
        else:
            print("使用普通连接...")
            mail = poplib.POP3(server, port, timeout=10)
        
        print("正在登录...")
        mail.user(username)
        mail.pass_(password)
        
        mail_list = mail.list()
        num_messages = len(mail_list[1])
        print(f"✓ POP3 连接成功！服务器上有 {num_messages} 封邮件")
        
        mail.quit()
        return True
    
    except poplib.error_proto as e:
        print(f"✗ POP3 错误: {e}")
        if 'ERR' in str(e).upper():
            print("  提示: 可能是用户名或密码错误")
            print("  163 邮箱请使用授权码而非登录密码")
        return False
    except ConnectionRefusedError:
        print(f"✗ 连接被拒绝：{server}:{port}")
        print("  提示：检查端口是否正确")
        return False
    except TimeoutError:
        print("✗ 连接超时")
        print("  提示：检查网络连接或服务器地址")
        return False
    except Exception as e:
        print(f"✗ 未知错误: {e}")
        return False

def main():
    import argparse
    import yaml
    
    parser = argparse.ArgumentParser(description='测试邮件服务器连接')
    parser.add_argument('--config', '-c', default='email_config.yaml', 
                       help='配置文件路径')
    parser.add_argument('--smtp-only', action='store_true', help='只测试 SMTP')
    parser.add_argument('--imap-only', action='store_true', help='只测试 IMAP')
    
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
    
    smtp_server = config.get('smtp', {}).get('server')
    smtp_port = config.get('smtp', {}).get('port')
    imap_server = config.get('imap', {}).get('server')
    imap_port = config.get('imap', {}).get('port')
    pop3_server = config.get('pop3', {}).get('server')
    pop3_port = config.get('pop3', {}).get('port')
    username = config.get('account', {}).get('username')
    password = config.get('account', {}).get('password')
    
    if not all([smtp_server, smtp_port, username, password]):
        print("错误: 配置文件缺少必要字段")
        sys.exit(1)
    
    print("=" * 50)
    print("邮件服务器连接测试")
    print("=" * 50)
    print(f"邮箱: {username}")
    print(f"SMTP: {smtp_server}:{smtp_port}")
    if imap_server:
        print(f"IMAP: {imap_server}:{imap_port}")
    if pop3_server:
        print(f"POP3: {pop3_server}:{pop3_port}")
    print("=" * 50)
    
    results = []
    
    if not args.imap_only:
        results.append(test_smtp(smtp_server, smtp_port, username, password))
    
    if not args.smtp_only and imap_server:
        results.append(test_imap(imap_server, imap_port, username, password))
    
    if not args.smtp_only and pop3_server:
        results.append(test_pop3(pop3_server, pop3_port, username, password))
    
    print("\n" + "=" * 50)
    print("测试总结")
    print("=" * 50)
    
    if all(results):
        print("✓ 所有测试通过！配置正确。")
        sys.exit(0)
    else:
        print("✗ 部分测试失败，请检查配置。")
        sys.exit(1)

if __name__ == '__main__':
    main()
