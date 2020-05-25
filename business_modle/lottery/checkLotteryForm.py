# -*- coding: utf-8 -*-
# @Time    : 2019/1/8 11:06
# @Author  : wanglanqing
from flask_wtf import Form
from wtforms import RadioField,StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Required

class lotteryCheckForm(Form):
    env = RadioField(u'环境', validators=[DataRequired()], choices=[('1', '灰度环境'), ('0', '测试环境')], default='1')
    app_key = StringField(u'广告位app_key:',validators=[DataRequired()], render_kw={'placeholder': "广告位app_key", 'style': 'width:300px'})
    # domain_key = StringField(u'域名:',render_kw={'placeholder':'默认为adhudong.com','style':'width:300px'})
    submit = SubmitField(u'查询')
