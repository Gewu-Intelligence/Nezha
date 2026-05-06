#!/usr/bin/env python
#coding=utf-8

import os
import json
import base64
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import EcsRamRoleCredential
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials import StsTokenCredential

# Please ensure that the environment variables ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET are set.
#credentials = AccessKeyCredential(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'])
# use STS Token
# credentials = StsTokenCredential(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'], os.environ['ALIBABA_CLOUD_SECURITY_TOKEN'])
#cred = EcsRamRoleCredential(role_name='AliyunECSInstanceForEHPCRole')
cred = AccessKeyCredential(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'])
client = AcsClient(region_id='cn-shanghai', credential=cred)

request = CommonRequest()
request.set_accept_format('json')
request.set_domain('ehpcinstant.cn-shanghai.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https') # https | http
request.set_version('2023-07-01')
request.set_action_name('CreateJob')

# Step 1: 定义 Shell 脚本字符串
shell_script = """#!/bin/bash

source  /etc/profile.d/mount-data.sh
INPUT_DIR=/mnt/af3data/af_input
OUTPUT_DIR=/mnt/af3data/af_output
DATA_DIR=/data/af3_databases
MODEL_PARAMS_DIR=/mnt/af3data/af3_models
LOG_DIR=/mnt/af3data/logs
INPUT_FILE_NAME='fold_input.json'
mkdir -p ${LOG_DIR} ${OUTPUT_DIR}
TIME_SUFFIX=\`date "+%Y%m%d-%H-%M"\`

echo "--------AF3 run start!--------"
start_time_mod=$(date +%s)
docker run --rm \\
    --env XLA_FLAGS='--xla_disable_hlo_passes=custom-kernel-fusion-rewriter' \\
    --volume ${INPUT_DIR}:/root/af_input \\
    --volume ${OUTPUT_DIR}:/root/af_output \\
    --volume ${MODEL_PARAMS_DIR}:/root/models \\
    --volume ${DATA_DIR}:/root/public_databases \\
    --privileged=true --net=host  --gpus all \\
    alphafold3:latest \\
    python run_alphafold.py \\
    --json_path=/root/af_input/${INPUT_FILE_NAME} \\
    --flash_attention_implementation=xla \\
    --model_dir=/root/models \\
    --output_dir=/root/af_output \\
    2>&1 | tee ${LOG_DIR}/af3_run_${TIME_SUFFIX}.log
echo "--------AF3 run success--------"
#wait
end_time_mod=$(date +%s)

start_date=$(date -d @$start_time_mod)
end_date=$(date -d @$end_time_mod)
echo "Started: "$start_date"; Ended: "$end_date"; Elapsed time: "$(($end_time_mod - $start_time_mod))" sec"
"""

# Step 2: 将字符串转换为 Base64 编码
# 注意：Base64 编码需要将字符串转换为字节格式
encoded_script = base64.b64encode(shell_script.encode('utf-8')).decode('utf-8')

tasks = [
    {
      "TaskSpec": {
        "TaskExecutor": [
          {
            "VM": {
              "Image": "m-xxx",
              "Script": encoded_script,
              "Password": "test@123"
            }
          }
        ],
        "VolumeMount": [
          {
            "MountPath": "/mnt",
            "VolumeDriver": "alicloud/nas",
            "MountOptions": "{\"server\":\"xxx.cn-hangzhou.nas.aliyuncs.com\",\"vers\":\"3\",\"path\":\"/\",\"options\":\"nolock,tcp,noresvport\"}"
          }
        ],
        "Resource": {
          "Disks": [
            {
              "Type": "System",
              "Size": 40
            }
          ],
          "InstanceTypes": [
            "ecs.gn6i-c8g1.2xlarge"
          ],
          "Cores": 8,
          "Memory": 31
        }
      },
      "ExecutorPolicy": {
        "MaxCount": 1
      }
    }
  ],

deploymentPolicy = {
  "Network": {
    "Vswitch": [
      "vsw-xxx"
    ],
    "EnableExternalIpAddress": False,
  },
  "AllocationSpec": "Standard",
  "Level":"General"
}

securityPolicy = {
  "SecurityGroup": {
    "SecurityGroupIds": [
      "sg-xxx"
    ]
  }
}

tasksStr = json.dumps(tasks)
deploymentPolicyStr = json.dumps(deploymentPolicy)
securityPolicyStr = json.dumps(securityPolicy)

request.add_query_param('JobName', "create_vm_af3_job")
request.add_query_param('JobDescription', "E-HPC Instant Alphafold3 VM作业提交")
request.add_query_param('Tasks', tasksStr)
request.add_query_param('DeploymentPolicy', deploymentPolicyStr)
request.add_query_param('SecurityPolicy', securityPolicyStr)

response = client.do_action(request)
# python2:  print(response) 
print(str(response, encoding = 'utf-8'))
