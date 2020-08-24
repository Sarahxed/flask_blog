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
from apps.article.views import article_bp
from apps.user.views import user_bp
from exts import db, bootstrap
from apps.user.models import User
from apps.article.models import Comment, Article, Article_type


def create_app():
    app = Flask(__name__, template_folder='../templates', static_folder='../static')
    app.config.from_object(settings.config)
    db.init_app(app=app)
    # 初始化bootstrap
    bootstrap.init_app(app=app)
    # 注册蓝图
    app.register_blueprint(user_bp)
    app.register_blueprint(article_bp)
    return app
