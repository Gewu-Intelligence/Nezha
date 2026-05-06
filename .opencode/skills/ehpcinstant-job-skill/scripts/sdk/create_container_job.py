#!/usr/bin/env python
#coding=utf-8

import os
import json
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

tasks = [
  {
    "TaskSpec": {
      "TaskExecutor": [
        {
          "Container": {
            "Image":"registry-vpc.cn-shanghai.aliyuncs.com/demo/xxx:v1.2",
            "AppId":"ci-ctn-xxx",
            "Command": [
              "sleep","180000",
            ],
            "EnvironmentVars": [
              {
                "Name": "RUN_PY_PATH",
                "Value": "/mnt/test.py"
              },
              {
                "Name": "OUTPUT_PATH",
                "Value": "/mnt/output/"
              },
              {
                "Name": "INPUT_PDB_PATH",
                "Value": "/mnt/input/test.pdb"
              },
              {
                "Name": "LOG_PATH",
                "Value": "/mnt/logs"
              }
            ]
          }
        }
      ],
      "VolumeMount": [
        {
          "MountPath": "/mnt",
          "VolumeDriver": "alicloud/nas",
          "MountOptions": "{\"server\":\"xxx.cn-shanghai.nas.aliyuncs.com\",\"vers\":\"3\",\"path\":\"/\",\"options\":\"nolock,tcp,noresvport\"}"
        }
      ],
      "Resource": {
        "Disks": [
          {
            "Type": "System",
            "Size": 40
          }
        ],
        "Cores": 8,
        "Memory": 32,
        "InstanceTypes":[
          "ecs.gn6v-c8g1.2xlarge"
        ]
      }
    },
    "ExecutorPolicy": {
      "MaxCount": 1
    },
    "TaskSustainable": False
  }
]

#request.set_InstanceType(["ecs.gn6v-c8g1.2xlarge"])  #V100, 16GB
#request.set_InstanceType(["ecs.gn7i-c8g1.2xlarge"])   #A10, 24GB
#request.set_InstanceType(["ecs.gn6e-c12g1.3xlarge"]) #V100, 32GB

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

request.add_query_param('JobName', "testX")
request.add_query_param('JobDescription', "container job test")
request.add_query_param('Tasks', tasksStr)
request.add_query_param('DeploymentPolicy', deploymentPolicyStr)
request.add_query_param('SecurityPolicy', securityPolicyStr)

response = client.do_action(request)
# python2:  print(response) 
print(str(response, encoding = 'utf-8'))
