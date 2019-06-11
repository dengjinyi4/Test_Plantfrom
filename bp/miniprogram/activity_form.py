# encoding=utf-8
__author__ = 'aidinghua'

import time
from flask_wtf import Form

from wtforms import StringField,SelectField,SubmitField,SelectFieldBase
from wtforms.validators import DataRequired
from business_modle.querytool.utils.db_info import  *


class activity_form(Form):

    db=DbOperations()

    template_type_name = StringField(label='模板类型名称:',validators=[DataRequired()])
    path= StringField(label='模板路由地址:',validators=[DataRequired()])
    click_xpath = StringField(label='抽奖按钮xpath:',validators=[DataRequired()])
    obtain_xpath = StringField(label='点击广告xpath:',validators=[DataRequired()])
    status = StringField(label='状态:',validators=[DataRequired()])
    logid_start = StringField(label='logid起始值:',validators=[DataRequired()])
    logid_end = StringField(label='logid结束值:',validators=[DataRequired()])
    create_time = StringField(label='创建日期:',default=time.strftime('%Y-%m-%d'),validators=[DataRequired()],render_kw={'class':"form-control",'aria-describedby':'emailHelp'})
    update_time = StringField(label='更新日期:',default=time.strftime('%Y-%m-%d'),validators=[DataRequired()],render_kw={'class':"form-control",'aria-describedby':'emailHelp'})

if __name__=='__main__':

    activity_form()




