# -*- coding: utf-8 -*-
import time
from datetime import  datetime
from flask import Flask,request,render_template,Blueprint,flash,url_for
from business_modle.querytool import myredis as mr
from business_modle.querytool import myredis_status as mrs
from business_modle.querytool import plantfromwtf as ft
from business_modle.querytool import bidding_analysis as ba
from business_modle.querytool import ad_orderinfor as ao
from buinfor import *
import buinfor

hdtgetother = Blueprint('infor', __name__,template_folder='templates')

#给媒体单独放一个页面
@hdtgetother.route('/get/',methods=('POST','GET'))
def getinfor():
    # myform=ft.myredis()
    # if myform.validate_on_submit():
    #     myenv=myform.data['myenv']
    #     print myenv
    #     mybudget,allcount,negativecount=mr.mygetredis(myenv,'voyager:budget')
    #     return render_template('myredis.html',mybudget=mybudget,allcount=allcount,negativecount=negativecount,form=myform,myenv=myenv)
    data=buinfor.getmediainfor()
    return render_template('getinfor.html',data=data)
