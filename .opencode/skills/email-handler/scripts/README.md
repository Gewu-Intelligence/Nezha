# 邮件处理工具

一个完整的 Python 邮件发送和接收工具，支持附件功能。

## 功能特性

- 发送邮件（支持纯文本和 HTML 格式）
- 发送附件（支持多个文件）
- 接收邮件（IMAP 协议）
- 接收邮件（POP3 协议）
- 下载邮件附件
- 通过配置文件管理邮箱信息

## IMAP vs POP3

**IMAP（推荐）：**
- 支持多文件夹（收件箱、发件箱、草稿等）
- 邮件保留在服务器，多设备同步
- 支持服务器端管理

**POP3：**
- 只能访问收件箱
- 邮件可以下载后从服务器删除
- 适合简单的邮件接收场景

## 使用方法

### 1. 安装依赖

```bash
pip install pyyaml
```

### 2. 配置邮箱

复制示例配置文件并修改：

```bash
cp email_config.yaml.example email_config.yaml
```

编辑 `email_config.yaml`：

```yaml
smtp:
  server: smtp.gmail.com
  port: 587

imap:
  server: imap.gmail.com
  port: 993

account:
  username: your_email@gmail.com
  password: your_password_or_app_password
```

### 3. 运行脚本

```bash
python email_handler.py -h
```

首次运行如果没有配置文件，会提示您创建。

## 常用邮箱配置

### Gmail
- SMTP: smtp.gmail.com:587 (TLS) 或 smtp.gmail.com:465 (SSL)
- IMAP: imap.gmail.com:993
- POP3: pop.gmail.com:995 (SSL)
- 注意: 需要使用应用专用密码（不是登录密码）

### Outlook/Hotmail
- SMTP: smtp-mail.outlook.com:587 (TLS)
- IMAP: outlook.office365.com:993
- POP3: outlook.office365.com:995 (SSL)

### QQ 邮箱
- SMTP: smtp.qq.com:587 (TLS) 或 smtp.qq.com:465 (SSL)
- IMAP: imap.qq.com:993
- POP3: pop.qq.com:995 (SSL)
- 注意: 需要在设置中开启 POP3/SMTP 服务并获取授权码

### 163 邮箱
- SMTP: smtp.163.com:465 (SSL) 或 smtp.163.com:25 (普通)
- IMAP: imap.163.com:993
- POP3: pop.163.com:995 (SSL)
- **重要**: 需要使用授权码（不是登录密码）
- 获取授权码步骤:
  1. 登录 163 邮箱网页版
  2. 设置 -> POP3/SMTP/IMAP
  3. 开启"POP3/SMTP服务"
  4. 按提示发送短信获取授权码
  5. 将授权码填入配置文件的 password 字段

## SMTP 端口说明

- **465**: SSL 加密，直接使用 SMTP_SSL 连接
- **587**: STARTTLS，先建立连接再加密（推荐）
- **25**: 普通端口（不加密，不推荐）

脚本会根据端口自动选择正确的连接方式。

## 命令行使用

### 发送邮件

```bash
# 发送纯文本邮件
python email_handler.py send --to recipient@example.com --subject "测试邮件" --body "这是一封测试邮件"

# 发送 HTML 邮件
python email_handler.py send --to recipient@example.com --subject "HTML邮件" --html "<h1>标题</h1><p>内容</p>"

# 发送带附件的邮件
python email_handler.py send --to recipient@example.com --subject "带附件" --body "请查看附件" --attach file1.pdf file2.jpg

# 简写形式
python email_handler.py send -t recipient@example.com -s "测试" -b "内容"
```

### 接收邮件（IMAP）

```bash
# 接收最新 10 封邮件
python email_handler.py receive

# 接收最新 20 封邮件
python email_handler.py receive --limit 20

# 从其他文件夹接收
python email_handler.py receive --folder "Sent"

# 显示邮件详情
python email_handler.py receive --limit 5 --detail

# 接收邮件并自动下载附件
python email_handler.py receive --download ./attachments

# 接收 20 封邮件并下载附件到指定目录
python email_handler.py receive -l 20 -dl ./my_downloads

# 简写形式
python email_handler.py receive -l 20
```

### 接收邮件（POP3）

```bash
# 使用 POP3 接收最新 10 封邮件
python email_handler.py receive-pop

# 接收最新 20 封邮件
python email_handler.py receive-pop --limit 20

# 显示邮件详情
python email_handler.py receive-pop -l 5 --detail

# 接收邮件并自动下载附件
python email_handler.py receive-pop --download ./attachments

# 接收邮件、下载附件后删除服务器上的邮件
python email_handler.py receive-pop -l 10 -dl ./attachments --delete

# 简写形式
python email_handler.py receive-pop -l 20
```

### 下载指定邮件的附件

```bash
# 下载指定邮件的附件到默认目录
python email_handler.py download --email-id 12345

# 下载到指定目录
python email_handler.py download --email-id 12345 --path ./my_downloads

# 从指定文件夹下载
python email_handler.py download --email-id 12345 --folder "Sent"

# 简写形式
python email_handler.py download -e 12345 -p ./downloads
```

### 自定义配置文件

```bash
# 使用指定的配置文件
python email_handler.py -c /path/to/custom_config.yaml send --to user@example.com --subject "测试"
```

## 编程使用示例

### 使用配置文件（推荐）

```python
from email_handler import EmailHandler

# 自动读取 email_config.yaml 配置文件
handler = EmailHandler()
```

### 手动指定配置

```python
from email_handler import EmailHandler

handler = EmailHandler(
    smtp_server='smtp.gmail.com',
    smtp_port=587,
    imap_server='imap.gmail.com',
    imap_port=993,
    username='your_email@gmail.com',
    password='your_password_or_app_password'
)

# 发送简单邮件
handler.send_email(
    to_address='recipient@example.com',
    subject='测试邮件',
    body='这是一封测试邮件'
)

# 发送带附件的邮件
handler.send_email(
    to_address='recipient@example.com',
    subject='带附件的邮件',
    body='请查看附件',
    attachments=['/path/to/file1.pdf', '/path/to/file2.jpg']
)

# 发送 HTML 邮件
html_body = '''
<html>
<body>
    <h1>欢迎</h1>
    <p>这是一封 <strong>HTML</strong> 邮件</p>
</body>
</html>
'''
handler.send_email(
    to_address='recipient@example.com',
    subject='HTML 邮件',
    body=html_body,
    is_html=True
)
```

### 接收邮件（IMAP）

```python
# 获取最新 10 封邮件
emails = handler.receive_emails(limit=10)

for email_info in emails:
    print(f"发件人: {email_info['from']}")
    print(f"主题: {email_info['subject']}")
    print(f"内容: {email_info['body']}")
    if email_info['attachments']:
        print(f"附件: {[a['filename'] for a in email_info['attachments']]}")
```

### 接收邮件（POP3）

```python
# 获取最新 10 封邮件
emails = handler.receive_emails_pop3(limit=10)

for email_info in emails:
    print(f"发件人: {email_info['from']}")
    print(f"主题: {email_info['subject']}")
    print(f"内容: {email_info['body']}")
    if email_info['attachments']:
        print(f"附件: {[a['filename'] for a in email_info['attachments']]}")

# 接收邮件并下载附件
emails = handler.receive_emails_pop3(limit=10, download_path='./attachments')

for email_info in emails:
    print(f"已下载: {email_info['downloaded_files']}")

# 接收邮件、下载附件后从服务器删除
emails = handler.receive_emails_pop3(
    limit=10, 
    download_path='./attachments',
    delete_after_download=True
)
```

### 接收邮件并自动下载附件

```python
# 获取最新 10 封邮件，并自动下载附件
emails = handler.receive_emails(limit=10, download_path='./attachments')

for email_info in emails:
    print(f"主题: {email_info['subject']}")
    print(f"附件: {[a['filename'] for a in email_info['attachments']]}")
    print(f"已下载: {email_info['downloaded_files']}")
```

### 下载指定邮件的附件

```python
# 下载指定邮件的所有附件
email_id = '123'  # 从 receive_emails 获取的邮件 ID
downloaded_files = handler.download_attachments(
    email_id=email_id,
    save_path='./downloads'
)

print(f"已下载: {downloaded_files}")
```

## 完整使用流程示例

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 复制配置模板
cp email_config.yaml.example email_config.yaml

# 3. 编辑配置文件（填入真实的邮箱信息）
# 163 邮箱用户注意：
# - password 字段必须填入授权码（不是登录密码）
# - 前往 163 邮箱设置 -> POP3/SMTP/IMAP 开启服务并获取授权码
vim email_config.yaml

# 4. 测试连接（推荐先测试）
python test_connection.py    # 测试所有连接
python test_pop3.py           # 专门测试 POP3

# 5. 查看帮助
python email_handler.py -h

# 6. 发送测试邮件
python email_handler.py send --to myfriend@example.com --subject "测试" --body "Hello World"

# 7. 使用 IMAP 接收邮件
python email_handler.py receive --limit 5 --detail

# 8. 使用 IMAP 接收邮件并自动下载附件
python email_handler.py receive -l 10 -dl ./attachments

# 9. 使用 POP3 接收邮件
python email_handler.py receive-pop --limit 5 --detail

# 10. 使用 POP3 接收邮件并下载附件后删除
python email_handler.py receive-pop -l 10 -dl ./attachments --delete

# 11. 下载指定邮件的附件（假设邮件 ID 是 123）
python email_handler.py download --email-id 123 --path ./attachments
```

## 故障排除

### 快速诊断

1. **测试配置是否正确**：
   ```bash
   python test_connection.py    # 测试所有连接
   python test_pop3.py           # 专门测试 POP3
   ```

2. **常见问题**：
   - 163 邮箱必须使用**授权码**（不是登录密码）
   - 用户名必须是**完整邮箱地址**
   - POP3 端口应为 **995**（SSL）

### POP3 连接测试

如果遇到 POP3 连接问题，使用测试工具诊断：

```bash
python test_pop3.py
```

### 163 邮箱 POP3 连接失败

**问题**: "接收邮件失败: None" 或认证错误

**解决方案**:

1. **检查 POP3 配置** - 确保配置正确：
   ```yaml
   pop3:
     server: pop.163.com
     port: 995
   ```

2. **使用授权码而非登录密码** - 163 邮箱必须使用授权码：
   - 登录 163 邮箱
   - 进入 设置 -> POP3/SMTP/IMAP
   - 开启"POP3/SMTP服务"
   - 按提示发送短信获取授权码
   - 将授权码填入配置文件的 password 字段

3. **检查用户名格式** - 必须使用完整邮箱地址：
   ```yaml
   account:
     username: yourname@163.com  # 正确
     username: yourname         # 错误
   ```

4. **运行测试工具** - 详细诊断连接问题：
   ```bash
   python test_pop3.py
   ```

### "Connection unexpectedly closed" 错误

这个错误通常由以下原因导致：

1. **端口配置错误**
   - 检查 SMTP 端口是否正确
   - Gmail: 465 (SSL) 或 587 (TLS)
   - QQ/163: 465 (SSL) 或 587 (TLS)

2. **密码或认证错误**
   - Gmail 必须使用应用专用密码，不能使用登录密码
   - QQ/163 邮箱需要使用授权码

3. **安全设置**
   - 确保邮箱已开启 SMTP 服务
   - 检查是否有安全策略限制（如"不太安全的应用访问"）

4. **网络问题**
   - 检查网络连接
   - 某些网络环境可能阻止 SMTP 端口

### Gmail 获取应用专用密码

1. 访问 https://myaccount.google.com/security
2. 开启"两步验证"
3. 选择"应用专用密码"
4. 生成新密码，并在配置文件中使用

### QQ 邮箱获取授权码

1. 登录 QQ 邮箱网页版
2. 设置 -> 账户 -> POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务
3. 开启"POP3/SMTP服务"
4. 按提示发送短信获取授权码

### 测试连接

使用提供的测试工具检查配置：

```bash
# 测试 SMTP 和 IMAP 连接
python test_connection.py

# 只测试 SMTP
python test_connection.py --smtp-only

# 只测试 IMAP
python test_connection.py --imap-only

# 使用自定义配置文件
python test_connection.py -c /path/to/config.yaml
```

或使用 Python 代码手动测试：

```python
import smtplib

server = smtplib.SMTP('smtp.gmail.com', 587)
server.set_debuglevel(1)  # 显示调试信息
server.starttls()
server.login('your_email@gmail.com', 'your_password')
server.quit()
```

## 注意事项

1. **Gmail 用户**：需要开启两步验证并生成应用专用密码
2. **QQ/163 邮箱**：需要在邮箱设置中开启 POP3/SMTP 服务
3. **安全**：建议使用配置文件，不要在代码中硬编码密码
4. **附件大小**：注意邮件服务器对附件大小的限制
5. **编码**：脚本自动处理中文和特殊字符的编码问题
6. **配置文件**：将 `email_config.yaml` 添加到 `.gitignore` 避免密码泄露
