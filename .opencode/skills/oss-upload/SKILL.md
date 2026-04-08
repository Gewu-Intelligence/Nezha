---
name: oss-upload
description: "When the service is deployed on a cloud server, use this skill when the user provide a file path and ask to download to their personal computer. This skill upload a file to Alibaba Cloud OSS and generate a shareable preview link for users to download easily. Trigger especially when user mentions: download file, upload to OSS, cloud storage upload, view image, preview image, generate share link, preview file via URL, or provides a local file path that needs to be shared online. "
---

# Overview

Trigger when user need to download a file. Upload a local file to Alibaba Cloud OSS and generate a shareable presigned URL for preview and download.

The workflow involves: 
1. checking the local file exist
2. uploading to OSS using the V2 SDK
3. generating a presigned URL with expiration time, 
4. returning the clickable link for preview. 

The clickable link must be in the formula like:

```html
<a href="{{RESULT_URL}}" target="_blank">Download Link: {{FILE_NAME}}</a>
```
where RESULT_URL is the url link generated after file-uploading，FILE_NAME is the filename

Requires OSS_ACCESS_KEY_ID and OSS_ACCESS_KEY_SECRET environment variables to be set.

# Requirements

## Prerequisites

- **Install Python Packages**:
  ```bash
  pip install alibabacloud-oss-v2 python-dotenv
  ```
- **Create .env File**: Copy `.env.example` to `.env` and fill in your credentials:
  ```bash
  cp .env.example .env
  # Then edit .env with your actual OSS credentials
  ```

## Configuration Required

### From .env File (Recommended)

The following can be configured in `.env`:

- **OSS_ACCESS_KEY_ID**: Your Alibaba Cloud AccessKey ID
- **OSS_ACCESS_KEY_SECRET**: Your Alibaba Cloud AccessKey Secret
- **OSS_BUCKET_NAME**: Your OSS bucket name (default for uploads)
- **OSS_REGION**: OSS bucket region (e.g., "cn-hangzhou")
- **OSS_EXPIRES_HOURS**: Default link expiration time (default: 1 hour)

### Runtime Parameters

- **key**: The filename/key to save in OSS (e.g., "file.txt"), will be prefixed with OSS_UPLOAD_PREFIX
- **local_file_path**: Full path to local file (required)
- **--prefix**: Optional override for upload prefix (defaults to OSS_UPLOAD_PREFIX from .env)

# OSS Upload Workflow


## Step-by-Step Process

### 1. Setup Credentials Provider

Load OSS credentials from .env file (via python-dotenv):

```python
import os
from dotenv import load_dotenv
import alibabacloud_oss_v2 as oss

load_dotenv()

credentials_provider = oss.credentials.EnvironmentVariableCredentialsProvider()
```

### 2. Configure Client

```python
cfg = oss.config.load_default()
cfg.credentials_provider = credentials_provider
cfg.region = region
client = oss.Client(cfg)
```

### 3. Upload File

Use the uploader for automatic chunking and concurrent uploads:

```python
put_request = oss.PutObjectRequest(
    bucket=bucket_name,
    key=object_name,
)

uploader = client.uploader()
upload_result = uploader.upload_file(put_request, filepath=local_file_path)
print(f"ETag: {upload_result.etag}")
```

### 4. Generate Presigned URL

Create a time-limited shareable link:

```python
from datetime import timedelta

get_request = oss.GetObjectRequest(
    bucket=bucket_name,
    key=object_name
)

expires_in = timedelta(seconds=3600)  # 1 hour
presign_result = client.presign(get_request, expires=expires_in)

print(f"Share link: {presign_result.url}")
```

# Script Usage

## Command Line

```bash
python scripts/upload.py \
  --bucket your-bucket-name \
  --key uploads/file.txt \
  --file /path/to/local/file.txt \
  --region cn-hangzhou \
  --expires 1
```

Or with defaults from .env:

```bash
python scripts/upload.py \
  --key file.txt \
  --file /path/to/local/file.txt
# This will upload to "uploads/file.txt" if OSS_UPLOAD_PREFIX=uploads/
```

## Python Function

```python
from scripts.upload import upload_and_share

result = upload_and_share(
    bucket_name="your-bucket",
    object_name="uploads/file.txt",
    local_file_path="/path/to/file.txt",
    region="cn-hangzhou",
    expires_hours=1
)

print(f"[Preview]({result['url']})")
```

# Best Practices

- Always use `client.uploader()` instead of basic `put_object` for large files
- Set appropriate expiration time for presigned URLs (typically 1-24 hours)
- Verify credentials are set before proceeding with upload
- Handle exceptions and provide clear error messages
- Use descriptive object names for better organization
