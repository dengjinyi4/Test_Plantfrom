# -*- coding: utf-8 -*-
# @Time    : 2019/7/25 17:22
# @Author  : wanglanqing

from flask_wtf.form import Form
from wtforms import StringField,SubmitField,RadioField,IntegerField
from wtforms.validators import Required,DataRequired

class simulateAdDatasForm(Form):
    adzoneId = StringField(u'广告位ID',validators=[DataRequired()],render_kw={'placeholder':'请输入广告位'})
    loop_count = IntegerField(u'循环次数',validators=[DataRequired()],render_kw={'placeholder':'请输入正整数'})
    submit = SubmitField(u'提交')