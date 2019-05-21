# encoding=utf-8
__author__ = 'aidinghua'

import time
from flask_wtf import Form

from wtforms import StringField,SubmitField,SelectField,RadioField
from wtforms.validators import DataRequired
from business_modle.querytool.utils.db_info import  *


class mini_form(Form):

    db = DbOperations()

    ###构造页面元素

    name = StringField(label='媒体名称:',validators=[DataRequired()])
    create_time = StringField(label='提交日期:',default=time.strftime('%Y-%m-%d'),validators=[DataRequired()],render_kw={'class':"form-control",'aria-describedby':'emailHelp'})
    update_time = StringField(label='更新日期:',default=time.strftime('%Y-%m-%d'),validators=[DataRequired()],render_kw={'class':"form-control",'aria-describedby':'emailHelp'})



if __name__=='__main__':

    mini_form()