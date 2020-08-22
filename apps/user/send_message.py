#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@desc  : 
@author: Sarah
@file  : send_message.py
@time  : 2020/8/22 16:47
"""
import hashlib
import json
import random
from time import time

import requests

"""
网易云信发送请求，帮助后台发送短信息
https://dev.yunxin.163.com/docs/product/%E7%9F%AD%E4%BF%A1/%E7%9F%AD%E4%BF%A1%E6%8E%A5%E5%8F%A3%E6%8C%87%E5%8D
%97?#%E5%8F%91%E9%80%81%E7%9F%AD%E4%BF%A1/%E8%AF%AD%E9%9F%B3%E7%9F%AD%E4%BF%A1%E9%AA%8C%E8%AF%81%E7%A0%81
返回:{'code': 200, 'msg': '1', 'obj': '3584'}
"""


def util_sendmsg(mobile, app_secret, app_key):
    """网易云手机短信验证码"""
    url = 'https://api.netease.im/sms/sendcode.action'
    data = {
        'mobile': mobile,  # 你的手机号码
    }
    AppSecret = app_secret
    AppKey = app_key
    Nonce = str(random.random() * 100000000)  # 这个字符串时随机的长度不大于128，随便设
    CurTime = str(int((time() * 1000)))  # 采用时间戳
    content = AppSecret + Nonce + str(CurTime)
    CheckSum = hashlib.sha1(content.encode('utf-8')).hexdigest()  # 对上述进行按要求哈希
    # 设置请求头
    headers = {
        'AppKey': AppKey,
        'Nonce': Nonce,
        'CurTime': CurTime,
        'CheckSum': CheckSum
    }
    response = requests.post(url, data=data, headers=headers)  # 发送post请求
    str_result = response.text
    json_result = json.loads(str_result)
    return json_result
