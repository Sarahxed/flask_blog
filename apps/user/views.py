#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@desc  : 
@author: Sarah
@file  : views.py
@time  : 2020/8/14 16:40
"""
import os

from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

from apps.article.models import Article_type, Article
from apps.user.models import User, AboutMe, MessageBoard
from apps.utils import util_sendmsg
from exts import db
from settings import config

user_bp = Blueprint('user', __name__, url_prefix='/user')

required_login_list = ['/user/center',
                       '/user/update_info',
                       '/article/article_publish',
                       '/article/article_detail',
                       '/article/add_comment',
                       '/user/about_me',
                       '/user/show_about'
                       ]


@user_bp.before_app_request
def before_request():
    if request.path in required_login_list:
        id = session.get('uid')
        if not id:
            return render_template('user/login.html')
        else:
            user = User.query.get(id)
            g.user = user


@user_bp.app_template_filter('cdecode')
def content_decode(content):
    content = content.decode('utf-8')
    return content[:200] + "......"


@user_bp.app_template_filter('ddecode')
def content_decode(content):
    content = content.decode('utf-8')
    return content


@user_bp.route('/index', endpoint='index')
def index():
    """首页"""
    # cookie获取
    # uid = request.cookies.get('uid', None)
    # session获取
    uid = session.get('uid', None)
    # 获取文章列表
    page = int(request.args.get('page', default=1))
    pagination = Article.query.order_by(Article.pdatetime).paginate(page=page, per_page=3)
    # 获取分类列表
    types = Article_type.query.all()
    # 判断用户是否登录
    if uid:
        user = User.query.get(uid)
        return render_template('user/index.html', user=user, pagination=pagination, types=types)
    else:
        return render_template('user/index.html', pagination=pagination, types=types)


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
        if f == str(1):  # 用用户名和密码登录
            username = request.form.get("username")
            password = request.form.get('password')
            users = User.query.filter(User.username == username).all()
            for user in users:
                flag = check_password_hash(user.password, password)
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


@user_bp.route('/center', endpoint='center')
def center():
    types = Article_type.query.all()
    return render_template('user/center.html', user=g.user, types=types)


@user_bp.route('/update_info', methods=['POST', 'GET'], endpoint='update_info')
def update_info():
    """用户信息修改"""
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        email = request.form.get('email')
        icon = request.files.get('icon')
        icon_name = icon.filename
        print(icon_name)
        icon_type = icon_name.rsplit('.')[-1]
        if icon_type in config.ALLOWED_EXTENSIONS:
            icon_name = secure_filename(icon_name)
            print(icon_name)
            file_path = os.path.join(config.UPLOAD_ICON_DIR, icon_name)
            icon.save(file_path)
            # 数据库更新
            user = g.user
            user.username = username
            user.phone = phone
            user.email = email
            user.icon = "upload/icon/{}".format(icon_name)
            db.session.commit()
            return redirect(url_for('user.center'))
        else:
            return render_template('user/center.html', user=g.user, msg="扩展名必须是jpg, png, git, jpeg, bmp")
    else:
        return render_template('user/center.html', user=g.user)


@user_bp.route('/about_me', methods=['POST', 'GET'], endpoint='about_me')
def about_me():
    """添加我的信息"""
    try:
        content = request.form.get('about')
        aboutme = AboutMe()
        aboutme.content = content.encode('utf-8')
        aboutme.user_id = g.user.id
        db.session.add(aboutme)
        db.session.commit()
        return render_template('user/about_me.html', user=g.user)
    except Exception as e:
        return render_template('user/center.html')


@user_bp.route('/show_about', methods=['POST', 'GET'], endpoint='show_about')
def show_about():
    """展示我的信息，权限验证"""
    return render_template('user/about_me.html', user=g.user)


@user_bp.route('/board', methods=['POST', 'GET'], endpoint='board')
def show_board():
    page = int(request.args.get('page', 1))
    boards = MessageBoard.query.order_by(-MessageBoard.mdatetime).paginate(page=page, per_page=5)
    # 获取登录信息
    uid = session.get('uid', None)
    user = None
    if uid:
        user = User.query.get(uid)
    if request.method == "POST":
        content = request.form.get('board')
        msg_board = MessageBoard()
        msg_board.content = content
        if uid:
            msg_board.user_id = uid
        db.session.add(msg_board)
        db.session.commit()
        return redirect(url_for('user.board'))
    else:

        return render_template('user/board.html', user=user, boards=boards)


@user_bp.route('/del_board', methods=['POST', 'GET'], endpoint='del_board')
def del_board():
    bid = request.args.get('bid')
    if bid:
        msg_board = MessageBoard.query.get(bid)
        db.session.delete(msg_board)
        db.session.commit()
        return redirect(url_for('user.center'))


