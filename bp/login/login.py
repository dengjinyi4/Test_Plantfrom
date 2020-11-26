#!/usr/bin/env python
#coding=utf-8
__author__ = 'jinyi'
import sys,os,pyotp,qrcode
reload(sys)
sys.setdefaultencoding('utf8')
from utils import login as l
from business_modle.querytool import plantfromwtf as ft
from flask import session,request,g
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
        user=l.login(username,password,REMOTE_ADDR,HTTP_HOST)
        r=user.loginuser()
        if (len(r)>0):
            session['username']=str(r[0][1])
            return redirect(url_for('index'))

            # return render_template('logintest.html',flag=u'登录成功',form=myform)
        else:
            flash(u'登录失败')
            return render_template('logintest.html',form=myform)
    else:
        return render_template('logintest.html',form=myform)
@mylogin.route('/loginnew/',methods=('POST','GET'))
def loginnew():
    myform=ft.Myloginotp()
    if myform.validate_on_submit():
        username=myform.data['username']
        password=myform.data['password']
        # REMOTE_ADDR = request.META['REMOTE_ADDR'].split(':')[0]
        REMOTE_ADDR = request.remote_addr
        HTTP_HOST = request.remote_addr
        user=l.login(username,password,REMOTE_ADDR,HTTP_HOST)
        r=user.loginuserotp()
        if (len(r)>0):
            # 如果是内网
            if HTTP_HOST.split('.')[0]=='127':
                session['username']=str(r[0][1])
                return redirect(url_for('index'))
            else:
                # g.user1==str(r[0][1])
                # 需要验证otp
                if r[0][2]=='1':
                    # 需要扫描二维码
                    ispic=r[0][3]
                    # 设置ispic 是否显示二维码图片
                    if r[0][3]=='1':
                        session['ispic']=r[0][3]
                    else:
                        session['ispic']=''
                    # session['username']=str(r[0][1])
                    session['otp']=str(r[0][1])
                    return redirect(url_for('plantfrom_login.otpindex'))
                else:
                    session['username']=str(r[0][1])
                    return redirect(url_for('index'))
            # return render_template('logintest.html',flag=u'登录成功',form=myform)
        else:
            flash(u'登录失败')
            return render_template('logintestotp.html',form=myform)
    else:
        return render_template('logintestotp.html',form=myform)
@mylogin.route('/otpindex/',methods=('POST','GET'))
def otpindex():
    myform=ft.myotp()
    if session.get('ispic')=='1':
        picurl='/static/qrcodepic/{0}.BMP'.format(session['otp'])
        user=l.login(username=session['otp'])
        user.otppic1()
        session['picurl']=picurl
    else:
        picurl=''
    if myform.validate_on_submit():
        otppass=myform.data['otppass']
        user=l.login(username=session['otp'],otppass=int(otppass))
        if user.otpverify():
            session['username']=session['otp']
            print 'okkkkkkkkkkkkk'
            return redirect(url_for('index'))
        else:
             session['username']=''
             flash(u'otp登录失败')
        print otppass
    return render_template('otplogin.html',picurl=picurl,form=myform)
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
# if __name__ == '__main__':
#     user=l.login()
#     picpath='../../static/qrcodepic/sssssssss.png'
#     img=user.otppic1()
#     try:
#         img.save(picpath)
#     except Exception as e:
#         print e.message