#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@desc  : 
@author: Sarah
@file  : __init__.py.py
@time  : 2020/8/14 15:31
"""
from flask import Flask

import settings
from exts import db, bootstrap


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(settings.config)
    db.init_app(app=app)
    # 初始化bootstrap
    bootstrap.init_app(app=app)
    return app
