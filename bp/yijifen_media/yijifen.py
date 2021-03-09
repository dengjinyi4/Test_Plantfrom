#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 作者:jinyi
# 创建:2021-01-25
from flask import Flask,request,render_template,Blueprint,flash,url_for
from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Length
# from flask_ckeditor import CKEditorField
# from wtforms import StringField, SubmitField
# from flask_ckeditor import CKEditor
yijifen = Blueprint('yijifen', __name__,template_folder='templates')
# ckeditor = CKEditor(yijifen)
# 易积分 描述文件
@yijifen.route('/desc/',methods=('POST','GET'))
def yijifendesc():
    # myform=RichTextForm()
    article_body='22222222222123212331'
    return render_template('yijifen/yijifen_desc.html',article_body=article_body)

# class RichTextForm(FlaskForm):
#     title = StringField('Title', validators=[DataRequired(),Length(1,50)])
#     body = CKEditorField('Body', validators=[DataRequired()])
#     submit = SubmitField('Publish')