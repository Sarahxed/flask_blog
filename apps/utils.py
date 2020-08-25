#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@desc  : 
@author: Sarah
@file  : utils.py
@time  : 2020/8/24 15:04
"""

import hashlib
import json
import random
from time import time

import requests


def util_sendmsg(mobile, app_secret, app_key):
    """
    网易云手机短信验证码
    返回:{'code': 200, 'msg': '1', 'obj': '3584'}
    """

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

