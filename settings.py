#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@desc  : 
@author: Sarah
@file  : settings.py
@time  : 2020/8/11 11:23
"""
import os

CURRENT_ENV = os.environ.get("ENV", "development")


class BaseConfig(object):
    """配置基类"""
    # mysql+pymysql://user:password@hostip:port/database
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True  # 调试设置为true


class DevelopmentConfig(BaseConfig):
    """开发环境"""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/flaskblog?charset=utf8'
    pass


class ProductionConfig(BaseConfig):
    """正式环境"""
    DEBUG = False

    pass


if CURRENT_ENV == "development":
    config = DevelopmentConfig  # 开发环境
elif CURRENT_ENV == "production":
    config = ProductionConfig  # 正式环境
