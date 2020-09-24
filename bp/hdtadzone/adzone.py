# -*- coding: utf-8 -*-
import time
from datetime import  datetime
from flask import Flask,request,render_template,Blueprint,flash,url_for
from business_modle.querytool import myredis as mr
from business_modle.querytool import myredis_status as mrs
from business_modle.querytool import plantfromwtf as ft
from business_modle.querytool.adzone import adzone as adzone

hdtadzone = Blueprint('adzone11', __name__,template_folder='templates')

#给媒体单独放一个页面
@hdtadzone.route('/getadzone/',methods=('POST','GET'))
def getadzone():
    myform=ft.myadzone()
    if myform.validate_on_submit():
        myenv=str(myform.data['myenv'])
        type=str(myform.data['type'])
        begintime=str(myform.data['begindate'])
        endtime=str(myform.data['enddate'])
        adzone_id=str(myform.data['adzone_id'])
        adzoninfor=adzone.adzoneinfo(env=myenv,mytype=type,begintime=begintime,endtime=endtime,adzoneid=adzone_id)
        data,filed,tmpsql=adzoninfor.getadzoneinfo()
        return render_template('adzon.html',form=myform,data=data,filed=filed,tmpsql=tmpsql,type=type)
    data=[]
    return render_template('adzon.html',data=data,form=myform)
