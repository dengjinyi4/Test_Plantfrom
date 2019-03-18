# -*- coding: utf-8 -*-
# @Time    : 2019/1/21 17:43
# @Author  : wanglanqing

from flask_wtf.form import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required,DataRequired

class adzoneActForm(Form):
    adzoneId = StringField(u'广告位ID',validators=[DataRequired()],render_kw={'placeholder':'请输入广告位'})
    acts = StringField(u'活动ids',validators=[DataRequired()],render_kw={'placeholder':'多个活动id，请用;分隔','style':'width:300px'})
    submit = SubmitField(u'提交')