#!/usr/bin/python3
# -*- encoding: utf-8 -*-
"""
@desc  : 
@author: Sarah
@file  : models.py
@time  : 2020/8/14 17:00
"""
from datetime import datetime

from exts import db


class ArticleType(db.Model):
    """文章类别表"""
    __tablename__ = "article_type"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="文章ID")
    type_name = db.Column(db.String(30), nullable=False)
    articles = db.relationship('Article', backref="article_type")


class Article(db.Model):
    """文章表"""
    __tablename__ = "article"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="文章ID")
    title = db.Column(db.String(50), nullable=False, comment="文章标题")
    content = db.Column(db.String(300), nullable=False, comment="文章内容")
    pdatetime = db.Column(db.DateTime, default=datetime.now, comment="发布时间")
    click_num = db.Column(db.Integer, default=0, comment="浏览数")
    save_num = db.Column(db.Integer, default=0, comment="收藏数")
    love_num = db.Column(db.Integer, default=0, comment="点赞数")
    # 外键 同步到数据库的外键关系
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('article_type.id'), nullable=False)
    comments = db.relationship('Comment', backref="articles")


class Comment(db.Model):
    """评论表"""
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="评论ID")
    comment = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'))
    cdatetime = db.Column(db.DateTime, default=datetime.now)

    def __str__(self):
        return self.comment
