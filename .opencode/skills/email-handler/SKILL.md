---
name: email-handler
description: 发送和接收邮件。发送邮件时，需要提供对方的邮箱，如果带有文件，则发送附件；接收邮件时，如果有路径名，则把邮件的附件下载到邮件中
---

## Overview
Send and receive emails. To send an email, the user must provide the recipient’s email address; if files are included, attach them to the message. To receive email, if a destination path is specified, download any attachments to that location.

### Arguments
| 参数名 | 类型 | 必填 | 描述 |
| :--- | :--- | :--- | :--- |
| `send_email` | string | 是 | 接受方的邮箱 |
| `mail_subject` | string | 是 | 邮件的主题 |
| `mail_text` | string | 是 | 邮件的内容 |
| `attach` | string | 否 | 发送邮件时带的附件 |
| `attach_path` | string | 是 | 接受邮件时，附件下载到的文件夹 |

## Quick Start

## 发送邮件
### 如果没有附件
```bash
python email_handler.py send --to {{send_email}} --subject {{mail_subject}} --body {{mail_text}}

```

### 带附件的邮件
```bash
python email_handler.py send --to {{send_email}} --subject {{mail_subject}} --body {{mail_text}} --attach {{attach}}

```

### 接受邮件
```bash
python email_handler.py receive-pop -l 10 -dl {{attach_path}} --detail

```