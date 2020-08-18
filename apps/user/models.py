#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@desc  : 
@author: Sarah
@file  : models.py
@time  : 2020/8/14 16:40
"""
from datetime import datetime

from exts import db


class User(db.Model):
    """用户信息表"""
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="用户ID")
    username = db.Column(db.String(30), nullable=False, comment="用户名")
    password = db.Column(db.String(30), nullable=False, comment="密码")
    phone = db.Column(db.String(11), nullable=False, unique=True, comment="手机号码")
    email = db.Column(db.String(30), comment="邮箱")
    icon = db.Column(db.String(300), comment="用户头像")
    isdelete = db.Column(db.Boolean, default=False, comment="是否删除")
    rdatetime = db.Column(db.DateTime, default=datetime.now, comment="创建时间")
    article = db.relationship('Article', backref="user")
