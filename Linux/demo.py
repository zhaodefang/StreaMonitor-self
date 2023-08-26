#!/usr/bin/env python 3.10
# -*- coding: UTF-8 -*-
# @date: 2023/8/27 2:56
# @name: demo.py
# @author：Ryen
# @webside：www.prlrr.com
# @software: PyCharm
import requests
import json
import time
import hmac
import hashlib
import base64
import urllib.parse

def send_dingtalk_message(webhook_url, secret, title, text):
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    # 调用示例
    webhook_url = webhook_url + '&timestamp={timestamp}&sign={sign}'.format(
        timestamp=timestamp, sign=sign)
    headers = {'Content-Type': 'application/json'}
    data = {
        "msgtype": "markdown",
        "markdown": {
            "title":title,
            "text": text
        },
    }

    try:
        response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        print("钉钉消息发送成功")
    except requests.exceptions.RequestException as e:
        print("钉钉消息发送失败:", str(e))
if __name__ == '__main__':
    ss = '553123'
    secret = 'SEC6bbb58d2e08ca3cdb9ce79883cc9baa6cbcb01f5cf6bebfb1a38fca7090e903c'
    webhook_url = 'https://oapi.dingtalk.com/robot/send?access_token=f3d9971f909edf26843ae6cd0a16aa7892360dcc5c7c146073ff4898f0607db5'
    title = "视频略缩图已经生成完成！"
    text = f"# 视频略缩图已经生成完成！\n#### 文件夹：{ss} \n#### 共计耗时：{ss}\n"
    send_dingtalk_message(webhook_url, secret, title, text)
