#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@desc  : 
@author: Sarah
@file  : views.py
@time  : 2020/8/14 16:40
"""
from flask import Blueprint, render_template, request
from werkzeug.security import generate_password_hash

from apps.user.models import User
from exts import db

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/index', endpoint='index')
def index():
    return render_template('base.html')


@user_bp.route('/register', methods=['POST', 'GET'], endpoint='register')
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get('confirmpwd')
        email = request.form.get('email')
        phone = request.form.get('phone')
        if password == confirm_password:
            user = User()
            user.username = username
            user.password = generate_password_hash(password)
            user.phone = phone
            user.email = email
            db.session.add(user)
            db.session.commit()
            return "注册成功！"
    return render_template("user/register.html")
