#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@desc  : 
@author: Sarah
@file  : views.py
@time  : 2020/8/14 17:04
"""
from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify, g

from apps.user.models import User
from apps.article.models import Article, Article_type, Comment
from exts import db

article_bp = Blueprint('article', __name__, url_prefix='/article')


@article_bp.route('/publish_article', methods=['POST', 'GET'], endpoint='publish_article')
def publish_article():
    """用户心中文章发表"""
    if request.method == 'POST':
        title = request.form.get('title')
        type_id = request.form.get('type')
        content = request.form.get('content')
        article = Article()
        article.title = title
        article.type_id = type_id
        article.content = content
        article.user_id = session.get('uid')
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('user.index'))


@article_bp.route('/article_detail', endpoint='article_detail')
def article_detail():
    """文章详情"""
    aid = request.args.get('aid')
    article = Article.query.get(aid)
    types = Article_type.query.all()
    # 登录用户
    user = None
    user_id = session.get('uid', None)
    if user_id:
        user = User.query.get(user_id)
    # 单独查询评论

    page = int(request.args.get('page', 1))
    comments = Comment.query.filter(Comment.article_id == aid) \
        .order_by(-Comment.cdatetime) \
        .paginate(page=page, per_page=3)
    return render_template('article/detail.html', article=article, types=types, comments=comments, user=user)


@article_bp.route('/love', endpoint='love')
def love():
    """点赞"""
    article_id = request.args.get('aid')
    tag = request.args.get('tag')
    article = Article.query.get(article_id)
    if tag == "1":
        article.love_num -= 1
    else:
        article.love_num += 1
    db.session.commit()
    return jsonify(num=article.love_num)


@article_bp.route('/save_num', endpoint='save_num')
def save_num():
    """收藏"""
    article_id = request.args.get('aid')
    tag = request.args.get('tag')
    article = Article.query.get(article_id)
    if tag == "1":
        article.save_num -= 1
    else:
        article.save_num += 1
    db.session.commit()
    return jsonify(num=article.save_num)


@article_bp.route('/add_comment',  methods=['POST', 'GET'], endpoint="add_comment")
def add_comment():
    if request.method == "POST":
        content = request.form.get('comment')
        user_id = session.get('uid')
        article_id = request.form.get('aid')
        comment = Comment()
        comment.comment = content
        comment.user_id = user_id
        comment.article_id = article_id
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('article.article_detail')+"?aid="+article_id)
    return render_template('user/index.html')


@article_bp.route('/type_search', endpoint='type_search')
def article_type_search():
    # 用户对象判断
    uid = session.get('uid', None)
    user = None
    if uid:
        user = User.query.get(uid)

    # 文章分类获取
    types = Article_type.query.all()

    # tid的获取
    tid = request.args.get('tid', 1)
    page = int(request.args.get('page', 1))
    articles = Article.query.filter(Article.type_id == tid).paginate(page=page, per_page=3)
    params = {
        'user': user,
        'types': types,
        'articles': articles,
        'tid': tid,
    }


    return render_template('article/article_type.html', **params)
