#!/usr/bin/env python
#coding=utf-8

import sys
import json
import os
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.auth.credentials import EcsRamRoleCredential
from aliyunsdkcore.request import CommonRequest
from aliyunsdkcore.auth.credentials import AccessKeyCredential
from aliyunsdkcore.auth.credentials import StsTokenCredential

# Please ensure that the environment variables ALIBABA_CLOUD_ACCESS_KEY_ID and ALIBABA_CLOUD_ACCESS_KEY_SECRET are set.
# use STS Token
# credentials = StsTokenCredential(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'], os.environ['ALIBABA_CLOUD_SECURITY_TOKEN'])

cred = AccessKeyCredential(os.environ['ALIBABA_CLOUD_ACCESS_KEY_ID'], os.environ['ALIBABA_CLOUD_ACCESS_KEY_SECRET'])
client = AcsClient(region_id='cn-shanghai', credential=cred)

request = CommonRequest()
request.set_accept_format('json')
request.set_domain('ehpcinstant.cn-shanghai.aliyuncs.com')
request.set_method('POST')
request.set_protocol_type('https') # https | http
request.set_version('2023-07-01')
request.set_action_name('DeleteJobs')

jobSpec2 = [
  {
    "JobId": "job-xxxx\n",
    "TaskSpec": [
      {
        "TaskName": "task0",
        "ArrayIndex": [
          2
        ]
      }
    ]
  }
]

executorIds = [
  "job-xxxx-Task0-1"
]

job_id = sys.argv[1]
jobSpec = [
  {
    "JobId": job_id
  }
]

jobSpecStr = json.dumps(jobSpec)
#executorIdsStr = json.dumps(executorIds)
request.add_query_param('JobSpec', jobSpecStr)
#request.add_query_param('ExecutorIds', executorIdsStr)


response = client.do_action(request)
# python2:  print(response)
print(str(response, encoding = 'utf-8'))