#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@desc  : 
@author: Sarah
@file  : views.py
@time  : 2020/8/14 16:40
"""
from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash

from apps.user.models import User
from apps.user.send_message import util_sendmsg
from exts import db

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/index', endpoint='index')
def index():
    """首页"""
    # cookie获取
    # uid = request.cookies.get('uid', None)
    # session获取
    uid = session.get('uid', None)
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
            return redirect(url_for('user.login'))
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
        f = request.args.get('f')
        print(f)
        if f == str(1):  # 用用户名和密码登录
            username = request.form.get("username")
            password = request.form.get('password')
            print(username, password)
            users = User.query.filter(User.username == username).all()
            print(users)
            for user in users:
                flag = check_password_hash(user.password, password)
                print("flag:", flag)
                if flag:
                    # cookie实现机制
                    # response = redirect(url_for('user.index'))
                    # response.set_cookie('uid', str(user.id), max_age=3600)
                    # return response
                    # session机制
                    session['uid'] = user.id
                    return redirect(url_for('user.index'))
            else:
                return render_template('user/login.html', msg="用户名或密码错误")
        elif f == str(2):  # 短信验证码登录
            phone = request.form.get('phone')
            code = request.form.get('code')
            # 先检验验证码
            vaild_code = session.get(phone)
            if vaild_code == code:
                # 查询用户
                user = User.query.filter(User.phone == phone).first()
                if user:
                    # 登录成功，设置session
                    session['uid'] = user.id
                    return redirect(url_for('user.index'))
                else:
                    return render_template('user/login.html', msg="此号码未注册！")
            else:
                return render_template('user/login.html', msg="验证码有误！")

    return render_template('user/login.html')


@user_bp.route('/send_message', endpoint='send_message')
def send_message():
    phone = request.args.get("phone")
    app_secret = "596880f468b1"
    app_key = "a2a65f514a49d9cd11700eb79d6d8406"
    api_response = util_sendmsg(phone, app_secret, app_key)
    if api_response.get('code') == 200:
        session[phone] = api_response.get('obj')
        return jsonify(code=200, msg='短信发送成功！')
    else:
        return jsonify(code=400, msg='短信发送失败！')


@user_bp.route('/logout', endpoint='logout')
def logout():
    """退出登录"""
    response = redirect(url_for('user.index'))
    # 删除cookie
    # response.delete_cookie('uid')
    # 删除session
    # del session['uid']  # 只删除值 不删除空间
    session.clear()  # 值和空间都删除python
    return response
