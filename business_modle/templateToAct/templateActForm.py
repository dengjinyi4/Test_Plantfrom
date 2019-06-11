# -*- coding: utf-8 -*-
# @Time    : 2019/1/8 11:06
# @Author  : wanglanqing
from flask_wtf import Form
from wtforms import RadioField,StringField,SubmitField,TextAreaField
from wtforms.validators import DataRequired,Required

class templateActForm(Form):
    env = RadioField(u'环境',validators=[DataRequired()],choices=[('1','测试环境'),('0','生成环境')],default='1')
    template_ids = StringField(u'模板ID:', render_kw={'placeholder': "多个模板id请用;分割,如598;597;596", 'style': 'width:600px'})
    template_kws = StringField(u'模板kw:',render_kw={'placeholder':'多个关键字请用;分割，如smash_egg;money_tree_turntable.html',
    'style':'width:600px'})
    ad_ids = StringField(u'活动ID:',render_kw={'placeholder':"多个活动id请用;分割,如598;597;596",'style':'width:600px'})
    submit = SubmitField(u'查询')
