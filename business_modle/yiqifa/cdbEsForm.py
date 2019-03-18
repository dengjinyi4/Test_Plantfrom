#!flask/bin/env python
#coding:utf-8
from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField, TextAreaField, SubmitField,BooleanField,RadioField,SelectMultipleField
from wtforms.validators import DataRequired, Length

class MyForm(Form):
    # kwargs = {"phone": u'手机号', "phoneDeviceCode": u'手机设备号', "wechatUnionid": u'微信unionid'}
    # esKeyValue = BooleanField('I accept the Terms of Use', default='checked', validators=[DataRequired()],**kwargs)
    esKeyValue = SelectField('esKeyValue',choices=[('actionNo',u'订单号（点击id）'),('cdpid',u'cdpid')],default='actionNo')
    # esKeyValue = SelectField('esKeyValue',choices=[('actionNo',u'订单号（点击id）'),('phone',u'手机号'),('phoneDeviceCode',u'手机设备号'),('wechatUnionid',u'微信unionid'),('egouId',u'egouid'),('cdpid',u'cdpid')],default='actionNo')
    myenv=RadioField('myenv',choices=[('development',u'开发环境'),('test',u'测试环境')],default='test')
    actionType=RadioField('actionType',choices=[('order',u'order'),('export',u'export'),('all',u'all')],default='order')
    dataSource = SelectField('dataSource',choices=[('egou',u'易购')],default='egou')
    cdpValue = StringField('cdpValue')
    Indexes=SelectField('Indexes',choices=[('cdp_data_2019',u'cdp_data_2019'),('cdp_data_2018',u'cdp_data_2018'),('cdp_data_*',u'cdp_data_*')],default='cdp_data_2019')
    submit =SubmitField(u'搜 索')
    # cdpValue = StringField('cdpValue', validators=[Length(min=4, max=25)])
