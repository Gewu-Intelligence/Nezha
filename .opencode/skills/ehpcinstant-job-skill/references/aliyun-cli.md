# 阿里云CLI配置指南

## 安装阿里云CLI
```bash
# Linux/macOS
curl -fsSL https://aliyuncli.alicdn.com/aliyun-cli-linux-latest-amd64.tgz | tar xz
sudo mv aliyun /usr/local/bin/

# Windows (PowerShell)
Invoke-WebRequest -Uri "https://aliyuncli.alicdn.com/aliyun-cli-windows-latest-amd64.zip" -OutFile "aliyun-cli.zip"
Expand-Archive -Path "aliyun-cli.zip" -DestinationPath "."
```

## 配置AccessKey
```bash
aliyun configure
# 按提示输入：
# Access Key ID: [您的AccessKey ID]
# Access Key Secret: [您的AccessKey Secret]
# Default Region Id: cn-shanghai
# Default Output Format: json
```

## 验证配置
```bash
aliyun configure list
aliyun ehpcinstant ListJobs --region cn-shanghai
```

## 常见问题
- **认证失败**：检查 `~/.aliyun/config.json` 文件中的 AccessKey 配置
- **区域错误**：确保使用正确的区域（如 cn-shanghai）
- **权限不足**：确保 AccessKey 具有 E-HPC Instant 相关权限