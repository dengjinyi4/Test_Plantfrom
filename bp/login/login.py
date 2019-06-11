#!/usr/bin/env python
#coding=utf-8
__author__ = 'jinyi'
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from utils import login as l
from business_modle.querytool import plantfromwtf as ft
from flask import session,request
from flask import render_template,Blueprint,redirect,url_for,flash
mylogin = Blueprint('plantfrom_login', __name__,template_folder='templates')

@mylogin.route('/login111/',methods=('POST','GET'))
def login111():
    myform=ft.Mylogin()
    if myform.validate_on_submit():
        username=myform.data['username']
        password=myform.data['password']
        # REMOTE_ADDR = request.META['REMOTE_ADDR'].split(':')[0]
        REMOTE_ADDR = request.remote_addr
        HTTP_HOST = request.remote_addr
        r=l.loginuser(username,password,REMOTE_ADDR,HTTP_HOST)
        if (len(r)>0):
            session['username']=str(r[0][1])
            return redirect(url_for('index'))

            # return render_template('logintest.html',flag=u'登录成功',form=myform)
        else:
            flash(u'登录失败')
            return render_template('logintest.html',form=myform)
    else:
        return render_template('logintest.html',form=myform)
@mylogin.route('/a1/',methods=('POST','GET'))
def a1():
    myform=ft.myredis()
    if myform.validate_on_submit():
        return 'ddddddd'
    else:
        if 'username' in session:
            return 'okkkk'
        else:
            return  'no session'