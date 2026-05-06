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

sleep 180
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
          "Cores": 4,
          "Memory": 8,
          "InstanceTypes":[
          "ecs.c7.xlarge"
        ]
        }
      },
      "ExecutorPolicy": {
        "MaxCount": 1
      },
      "TaskSustainable": False
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

request.add_query_param('JobName', "create_vm_job")
request.add_query_param('JobDescription', "E-HPC Instant VM批处理作业提交")
request.add_query_param('Tasks', tasksStr)
request.add_query_param('DeploymentPolicy', deploymentPolicyStr)
request.add_query_param('SecurityPolicy', securityPolicyStr)

response = client.do_action(request)
# python2:  print(response) 
print(str(response, encoding = 'utf-8'))
