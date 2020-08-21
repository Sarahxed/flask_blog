#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@desc  : 
@author: Sarah
@file  : views.py
@time  : 2020/8/14 16:40
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

from apps.user.models import User
from exts import db

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/index', endpoint='index')
def index():
    """首页"""
    uid = request.cookies.get('uid', None)
    if uid:
        user = User.query.get(uid)
        return render_template('user/index.html', user=user)
    else:
        return render_template('user/index.html')


@user_bp.route('/register', methods=['POST', 'GET'], endpoint='register')
def register():
    """用户注册"""
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
            return redirect(url_for('user.index'))
    return render_template('user/register.html')


@user_bp.route('/isvalid_phone', methods=['POST', 'GET'], endpoint="isvalid_phone")
def is_valid_phone():
    """注册时手机号码校验"""
    phone = request.args.get('phone')
    user = User.query.filter(User.phone == phone).all()
    if len(user) > 0:
        return jsonify(code=400, msg="此号码已被注册")
    else:
        return jsonify(code=200, msg="此号码可用")


@user_bp.route('/isvalid_username', methods=['POST', 'GET'], endpoint="isvalid_username")
def is_valid_username():
    """注册时用户名校验"""
    username = request.args.get('username')
    user = User.query.filter(User.username == username).all()
    if len(user) > 0:
        return jsonify(code=400, msg="用户名已被注册")
    else:
        return jsonify(code=200, msg="此用户名可用")


@user_bp.route('/login', methods=['POST', 'GET'], endpoint="login")
def login():
    """用户登录"""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get('password')
        users = User.query.filter(User.username == username).all()
        for user in users:
            flag = check_password_hash(user.password, password)
            if flag:
                response = redirect(url_for('user.index'))
                response.set_cookie('uid', str(user.id), max_age=3600)
                return response
        else:
            return render_template('user/login.html', msg="用户名或密码错误")

    return render_template('user/login.html')


@user_bp.route('/logout', endpoint='logout')
def logout():
    """退出登录"""
    response = redirect(url_for('user.index'))
    # 删除cookie
    response.delete_cookie('uid')
    return response