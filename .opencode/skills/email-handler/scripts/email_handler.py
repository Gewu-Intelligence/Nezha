import smtplib
import imaplib
import poplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import decode_header
import os
import yaml
import argparse
from typing import List, Optional, Dict


def load_config(config_file: str = 'email_config.yaml') -> Dict:
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    return {}


class EmailHandler:
    def __init__(self, smtp_server: Optional[str] = None, smtp_port: Optional[int] = None, 
                 imap_server: Optional[str] = None, imap_port: Optional[int] = None,
                 pop3_server: Optional[str] = None, pop3_port: Optional[int] = None,
                 username: Optional[str] = None, password: Optional[str] = None,
                 config_file: str = 'email_config.yaml'):
        config = load_config(config_file)
        
        self.smtp_server = smtp_server or config.get('smtp', {}).get('server')
        self.smtp_port = smtp_port or config.get('smtp', {}).get('port')
        self.imap_server = imap_server or config.get('imap', {}).get('server')
        self.imap_port = imap_port or config.get('imap', {}).get('port')
        self.pop3_server = pop3_server or config.get('pop3', {}).get('server')
        self.pop3_port = pop3_port or config.get('pop3', {}).get('port')
        self.username = username or config.get('account', {}).get('username')
        self.password = password or config.get('account', {}).get('password')

    def send_email(self, to_address: str, subject: str, body: str,
                   attachments: Optional[List[str]] = None, is_html: bool = False) -> None:
        msg = MIMEMultipart()
        msg['From'] = self.username
        msg['To'] = to_address
        msg['Subject'] = subject

        content_type = 'html' if is_html else 'plain'
        msg.attach(MIMEText(body, content_type, 'utf-8'))

        if attachments:
            for file_path in attachments:
                if os.path.isfile(file_path):
                    with open(file_path, 'rb') as f:
                        part = MIMEApplication(f.read(), Name=os.path.basename(file_path))
                    part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
                    msg.attach(part)

        if self.smtp_port == 465:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.username, self.password)
                server.send_message(msg)
        else:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

    def receive_emails(self, folder: str = 'INBOX', limit: int = 10, 
                      download_path: Optional[str] = None) -> List[dict]:
        emails = []
        
        with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as mail:
            mail.login(self.username, self.password)
            mail.select(folder)
            
            status, messages = mail.search(None, 'ALL')
            if status != 'OK':
                return emails
            
            email_ids = messages[0].split()
            for email_id in email_ids[-limit:]:
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                if status == 'OK' and msg_data and msg_data[0]:
                    raw_email = msg_data[0][1]
                    if isinstance(raw_email, bytes):
                        email_message = email.message_from_bytes(raw_email)
                        
                        email_info = {
                            'id': email_id.decode(),
                            'from': self._decode_header(email_message['From']),
                            'to': self._decode_header(email_message['To']),
                            'subject': self._decode_header(email_message['Subject']),
                            'date': email_message['Date'],
                            'body': self._get_email_body(email_message),
                            'attachments': self._get_attachment_info(email_message),
                            'downloaded_files': []
                        }
                        
                        if download_path:
                            downloaded = self._download_attachments_from_message(
                                email_message, download_path)
                            email_info['downloaded_files'] = downloaded
                        
                        emails.append(email_info)
        
        return emails

    def receive_emails_pop3(self, limit: int = 10, 
                           download_path: Optional[str] = None,
                           delete_after_download: bool = False) -> List[dict]:
        emails = []
        
        try:
            if self.pop3_port == 995:
                mail = poplib.POP3_SSL(self.pop3_server, self.pop3_port)
            else:
                mail = poplib.POP3(self.pop3_server, self.pop3_port)
        except Exception as e:
            raise Exception(f"连接 POP3 服务器失败: {e}")
        
        try:
            mail.user(self.username)
            mail.pass_(self.password)
            
            mail_list = mail.list()
            status = mail_list[0]
            
            if not status.startswith(b'+OK'):
                raise Exception(f"获取邮件列表失败: {status}")
            
            if not mail_list[1]:
                print("没有邮件")
                return emails
            
            num_messages = len(mail_list[1])
            print(f"服务器上有 {num_messages} 封邮件")
            
            if num_messages == 0:
                print("没有邮件")
                return emails
            
            emails_to_fetch = min(limit, num_messages)
            
            for i in range(emails_to_fetch, 0, -1):
                try:
                    response, lines, octets = mail.retr(i)
                    raw_email = b'\r\n'.join(lines)
                    email_message = email.message_from_bytes(raw_email)
                    
                    email_info = {
                        'id': str(i),
                        'from': self._decode_header(email_message['From']),
                        'to': self._decode_header(email_message['To']),
                        'subject': self._decode_header(email_message['Subject']),
                        'date': email_message['Date'],
                        'body': self._get_email_body(email_message),
                        'attachments': self._get_attachment_info(email_message),
                        'downloaded_files': []
                    }
                    
                    if download_path:
                        downloaded = self._download_attachments_from_message(
                            email_message, download_path)
                        email_info['downloaded_files'] = downloaded
                    
                    emails.append(email_info)
                    
                    if delete_after_download:
                        mail.dele(i)
                
                except Exception as e:
                    print(f"获取邮件 {i} 时出错: {e}")
                    continue
        
        except poplib.error_proto as e:
            raise Exception(f"POP3 协议错误: {e}\n提示: 请检查用户名和密码是否正确")
        finally:
            mail.quit()
        
        return emails

    def _download_attachments_from_message(self, email_message, save_path: str) -> List[str]:
        downloaded_files = []
        os.makedirs(save_path, exist_ok=True)
        
        for part in email_message.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                if filename:
                    filename = self._decode_header(filename)
                    file_path = os.path.join(save_path, filename)
                    payload = part.get_payload(decode=True)
                    if payload and isinstance(payload, bytes):
                        with open(file_path, 'wb') as f:
                            f.write(payload)
                        downloaded_files.append(file_path)
        
        return downloaded_files

    def download_attachments(self, email_id: str, save_path: str = './attachments',
                           folder: str = 'INBOX') -> List[str]:
        downloaded_files = []
        os.makedirs(save_path, exist_ok=True)
        
        with imaplib.IMAP4_SSL(self.imap_server, self.imap_port) as mail:
            mail.login(self.username, self.password)
            mail.select(folder)
            
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            if status != 'OK' or not msg_data or not msg_data[0]:
                return downloaded_files
            
            raw_email = msg_data[0][1]
            if isinstance(raw_email, bytes):
                email_message = email.message_from_bytes(raw_email)
                
                for part in email_message.walk():
                    if part.get_content_disposition() == 'attachment':
                        filename = part.get_filename()
                        if filename:
                            filename = self._decode_header(filename)
                            file_path = os.path.join(save_path, filename)
                            payload = part.get_payload(decode=True)
                            if payload and isinstance(payload, bytes):
                                with open(file_path, 'wb') as f:
                                    f.write(payload)
                                downloaded_files.append(file_path)
        
        return downloaded_files

    def _decode_header(self, header: str) -> str:
        if not header:
            return ''
        decoded_parts = decode_header(header)
        result = []
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                if encoding:
                    result.append(part.decode(encoding))
                else:
                    result.append(part.decode('utf-8', errors='ignore'))
            else:
                result.append(str(part))
        return ''.join(result)

    def _get_email_body(self, email_message) -> str:
        body = ''
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                if content_type == 'text/plain' or content_type == 'text/html':
                    payload = part.get_payload(decode=True)
                    charset = part.get_content_charset() or 'utf-8'
                    body = payload.decode(charset, errors='ignore')
                    break
        else:
            payload = email_message.get_payload(decode=True)
            charset = email_message.get_content_charset() or 'utf-8'
            body = payload.decode(charset, errors='ignore')
        return body

    def _get_attachment_info(self, email_message) -> List[dict]:
        attachments = []
        for part in email_message.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()
                if filename:
                    payload = part.get_payload(decode=True)
                    size = len(payload) if payload else 0
                    attachments.append({
                        'filename': self._decode_header(filename),
                        'content_type': part.get_content_type(),
                        'size': size
                    })
        return attachments


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='邮件处理工具')
    parser.add_argument('--config', '-c', default='email_config.yaml', 
                       help='配置文件路径 (默认: email_config.yaml)')
    
    subparsers = parser.add_subparsers(dest='command', help='操作命令')
    
    send_parser = subparsers.add_parser('send', help='发送邮件')
    send_parser.add_argument('--to', '-t', required=True, help='收件人邮箱地址')
    send_parser.add_argument('--subject', '-s', required=True, help='邮件主题')
    send_parser.add_argument('--body', '-b', help='邮件内容 (纯文本)')
    send_parser.add_argument('--html', help='邮件内容 (HTML格式)')
    send_parser.add_argument('--attach', '-a', nargs='+', help='附件路径 (多个文件)')
    
    receive_parser = subparsers.add_parser('receive', help='接收邮件')
    receive_parser.add_argument('--limit', '-l', type=int, default=10, 
                               help='获取邮件数量 (默认: 10)')
    receive_parser.add_argument('--folder', '-f', default='INBOX',
                               help='邮件文件夹 (默认: INBOX)')
    receive_parser.add_argument('--detail', '-d', action='store_true',
                               help='显示邮件详情')
    receive_parser.add_argument('--download', '-dl', dest='download_path',
                               help='下载附件到指定目录 (不指定则不下载)')
    
    download_parser = subparsers.add_parser('download', help='下载附件')
    download_parser.add_argument('--email-id', '-e', required=True, help='邮件ID')
    download_parser.add_argument('--path', '-p', default='./attachments',
                               help='保存路径 (默认: ./attachments)')
    download_parser.add_argument('--folder', '-f', default='INBOX',
                               help='邮件文件夹 (默认: INBOX)')
    
    receive_pop_parser = subparsers.add_parser('receive-pop', help='使用 POP3 接收邮件')
    receive_pop_parser.add_argument('--limit', '-l', type=int, default=10, 
                                   help='获取邮件数量 (默认: 10)')
    receive_pop_parser.add_argument('--detail', '-d', action='store_true',
                                   help='显示邮件详情')
    receive_pop_parser.add_argument('--download', '-dl', dest='download_path',
                                   help='下载附件到指定目录 (不指定则不下载)')
    receive_pop_parser.add_argument('--delete', action='store_true',
                                   help='下载后删除服务器上的邮件')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        exit(1)
    
    if not os.path.exists(args.config):
        print(f"错误: 配置文件不存在: {args.config}")
        print(f"请复制 email_config.yaml.example 到 {args.config} 并填写配置")
        exit(1)
    
    try:
        handler = EmailHandler(config_file=args.config)
    except Exception as e:
        print(f"错误: 加载配置失败: {e}")
        exit(1)
    
    if args.command == 'send':
        body = args.html or args.body or ''
        is_html = args.html is not None
        attachments = args.attach or None
        
        try:
            handler.send_email(args.to, args.subject, body, attachments, is_html)
            print("邮件发送成功!")
        except Exception as e:
            print(f"发送失败: {e}")
            exit(1)
    
    elif args.command == 'receive':
        try:
            emails = handler.receive_emails(
                folder=args.folder, 
                limit=args.limit,
                download_path=getattr(args, 'download_path', None)
            )
            
            if not emails:
                print(f"在文件夹 {args.folder} 中没有找到邮件")
                exit(0)
            
            total_downloaded = 0
            for email_info in emails:
                total_downloaded += len(email_info.get('downloaded_files', []))
            
            print(f"\n共找到 {len(emails)} 封邮件")
            if total_downloaded > 0:
                print(f"共下载 {total_downloaded} 个附件\n")
            else:
                print()
            
            for i, email_info in enumerate(emails, 1):
                print(f"[{i}] ID: {email_info['id']}")
                print(f"    发件人: {email_info['from']}")
                print(f"    主题: {email_info['subject']}")
                print(f"    日期: {email_info['date']}")
                
                if email_info['attachments']:
                    print(f"    附件: {', '.join([a['filename'] for a in email_info['attachments']])}")
                
                if email_info.get('downloaded_files'):
                    print(f"    已下载: {len(email_info['downloaded_files'])} 个文件")
                
                if args.detail:
                    print(f"    内容预览: {email_info['body'][:200]}...")
                print()
        
        except Exception as e:
            print(f"接收邮件失败: {e}")
            exit(1)
    
    elif args.command == 'download':
        try:
            files = handler.download_attachments(
                email_id=args.email_id,
                save_path=args.path,
                folder=args.folder
            )
            
            if files:
                print(f"附件下载成功:")
                for f in files:
                    print(f"  - {f}")
            else:
                print("该邮件没有附件或下载失败")
        
        except Exception as e:
            print(f"下载附件失败: {e}")
            exit(1)
    
    elif args.command == 'receive-pop':
        try:
            if not handler.pop3_server or not handler.pop3_port:
                print("错误: 配置文件中缺少 POP3 服务器配置")
                print("请在配置文件中添加 pop3 配置:")
                print("pop3:")
                print("  server: pop.163.com")
                print("  port: 995")
                exit(1)
            
            emails = handler.receive_emails_pop3(
                limit=args.limit,
                download_path=getattr(args, 'download_path', None),
                delete_after_download=getattr(args, 'delete', False)
            )
            
            if not emails:
                print("没有找到邮件")
                exit(0)
            
            total_downloaded = 0
            for email_info in emails:
                total_downloaded += len(email_info.get('downloaded_files', []))
            
            print(f"\n共找到 {len(emails)} 封邮件")
            if total_downloaded > 0:
                print(f"共下载 {total_downloaded} 个附件\n")
            else:
                print()
            
            for i, email_info in enumerate(emails, 1):
                print(f"[{i}] ID: {email_info['id']}")
                print(f"    发件人: {email_info['from']}")
                print(f"    主题: {email_info['subject']}")
                print(f"    日期: {email_info['date']}")
                
                if email_info['attachments']:
                    print(f"    附件: {', '.join([a['filename'] for a in email_info['attachments']])}")
                
                if email_info.get('downloaded_files'):
                    print(f"    已下载: {len(email_info['downloaded_files'])} 个文件")
                
                if args.detail:
                    print(f"    内容预览: {email_info['body'][:200]}...")
                print()
            
            if hasattr(args, 'delete') and args.delete:
                print(f"已删除服务器上的 {len(emails)} 封邮件")
        
        except Exception as e:
            print(f"接收邮件失败: {e}")
            exit(1)
