# -*- coding: utf-8 -*-
# @Time    : 2019/5/14 11:40
# @Author  : wanglanqing

import time
from flask_wtf import Form
from wtforms import RadioField,StringField,SubmitField,TextAreaField,SelectField,DateField
from wtforms.validators import DataRequired
from utils.db_info import DbOperations


class JobAdReasonForm(Form):
    #构造页面元素
    jobname = TextAreaField(label=u'任务名称:', render_kw={'class':"form-control",'aria-describedby':'emailHelp'})
    ad_order = StringField(label=u'订单ID:',  validators=[DataRequired()], render_kw={'class':"form-control",'placeholder':'只输入一个订单id'})
    jobsql = TextAreaField(label=u'sql查询条件：', validators=[DataRequired()], render_kw={'class':"form-control",'aria-describedby':'emailHelp'})