#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@desc  : 
@author: Sarah
@file  : views.py
@time  : 2020/8/14 17:04
"""
from flask import Blueprint, request, render_template, redirect, url_for, session, jsonify

from apps.article.models import Article, Article_type
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
    return render_template('article/detail.html', article=article, types=types)


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
