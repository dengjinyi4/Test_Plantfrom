# -*- coding: utf-8 -*-
# @Time    : 2019/4/8 11:40
# @Author  : wanglanqing

import time
from flask_wtf import Form
from wtforms import RadioField,StringField,SubmitField,TextAreaField,SelectField,DateField
from wtforms.validators import DataRequired
from utils.db_info import DbOperations


class ToolsTrackerForm(Form):
    db = DbOperations()
    tester_sql = 'select id, ch_name from test.user where status=1 and role=2; '
    group_sql = "select id, name from test.group where status=1;"
    testers = db.execute_sql(tester_sql)
    groups = list(db.execute_sql(group_sql))
    groups.append((0L,'其他'))

    #构造页面元素
    group_id = SelectField(label=u'业务组:', choices=groups,default=1, render_kw={'class':"form-control",'aria-describedby':'emailHelp'})
    func_type = SelectField(label=u'类型:', choices=[(1,'新增'),(2,'修改')], validators=[DataRequired()], render_kw={'class':"form-control"})
    func_name = StringField(label=u'功能名称：', validators=[DataRequired()], render_kw={'class':"form-control",'aria-describedby':'emailHelp'})
    func_desc = TextAreaField(label=u'功能描述：', validators=[DataRequired()], render_kw={'class':"form-control",'aria-describedby':'emailHelp'})
    func_path = StringField(label=u'访问路由：', validators=[DataRequired()], render_kw={'class':"form-control",'aria-describedby':'emailHelp','placeholder':'/hdt_cssc/'})
    submit_date = StringField(label=u'提交日期：',default=time.strftime('%Y-%m-%d'), validators=[DataRequired()], render_kw={'class':"form-control",'aria-describedby':'emailHelp'})
    tester = SelectField(label=u'提交者：',  choices=testers, validators=[DataRequired()], render_kw={'class':"form-control",'aria-describedby':'emailHelp'})
    # submit = SubmitField('submit', render_kw={'class':"form-control",'aria-describedby':'emailHelp'})