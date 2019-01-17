# -*- coding: utf-8 -*-
# @Time    : 2018/12/18 9:33
# @Author  : wanglanqing

from flask_wtf import Form
from wtforms import RadioField,StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Required


class checkRouteForm(Form):
    env = RadioField(u'环境',validators=[DataRequired()],choices=[('1','测试环境'),('0','生成环境')],default='1')
    adzoneLink = StringField(u'广告位链接',validators=[DataRequired()],render_kw={'placeholder':'请输入广告位链接',
    'style':'width:600px'},default="https://display.adhudong.com/site_login_ijf.htm?app_key=adhuc5f5526ee4664923")
    submit = SubmitField(u'执行')