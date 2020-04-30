# -*- coding: utf-8 -*-
__author__ = 'jinyi'
import time
from datetime import  datetime
from flask import Flask,request,render_template,Blueprint,flash,url_for
from business_modle.querytool import plantfromwtf as ft
from business_modle.querytool.report import myreport as mr


hdtreport = Blueprint('myreport', __name__,template_folder='templates')

#汇总  菜单名---- 毛利表-分媒体毛利
@hdtreport.route('/reportall/',methods=('POST','GET'))
def reportall():
    myform=ft.myreportall()
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        endtime=str(myform.data['enddate'])[0:10]
        # data=adzone.getadzoneinfo(mytype=type,begintime=begintime,endtime=endtime,adzoneid=adzone_id)
        # rp=mr.myreport(begintime='2020-04-17',endtime='2020-04-17')
        rp=mr.myreport(begintime=begintime,endtime=endtime)
        data,filed,tmpsql=rp.getallreport()
        return render_template('reportall.html',form=myform,data=data,filed=filed,tmpsql=tmpsql)
    data=[]
    return render_template('reportall.html',data=data,form=myform)
#广告主联动毛利    菜单名---- 毛利表-联动客户毛利
@hdtreport.route('/repotadvliandong/',methods=('POST','GET'))
def repotadvliandong():
    myform=ft.myreportall()
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        endtime=str(myform.data['enddate'])[0:10]
        rp=mr.myreport(begintime=begintime,endtime=endtime)
        data,filed,tmpsql=rp.getadvliandong()
        return render_template('reportliandong.html',form=myform,data=data,filed=filed,tmpsql=tmpsql)
    data=[]
    return render_template('reportliandong.html',data=data,form=myform)
#汇总     菜单名---- 毛利表-平台毛利细化
@hdtreport.route('/repotptmaoli/',methods=('POST','GET'))
def repotptmaoli():
    myform=ft.myreportall()
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        endtime=str(myform.data['enddate'])[0:10]
        rp=mr.myreport(begintime=begintime,endtime=endtime)
        data,filed,tmpsql=rp.getptmaoli()
        return render_template('repotptmaoli.html',form=myform,data=data,filed=filed,tmpsql=tmpsql)
    data=[]
    return render_template('repotptmaoli.html',data=data,form=myform)
#菜单名：媒体效果-评估-日表
@hdtreport.route('/reportmtpinggu/',methods=('POST','GET'))
def reportmtpinggu():
    myform=ft.myreporpingguday()
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        endtime=str(myform.data['enddate'])[0:10]
        adzoneid=str(myform.data['adzoneid'])
        rp=mr.myreport(begintime=begintime,endtime=endtime,adzoneids=adzoneid)
        data,filed,tmpsql=rp.getmtpinggu()
        return render_template('reportmtpingguday.html',form=myform,data=data,filed=filed,tmpsql=tmpsql)
    data=[]
    return render_template('reportmtpingguday.html',data=data,form=myform)
#菜单名：媒体效果-评估-小时表 4、媒体效果-去联动-评估-小时表
@hdtreport.route('/reportmtpingguhour/',methods=('POST','GET'))
def reportmtpingguhour():
    myform=ft.myreporpingguhour()
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        # endtime=str(myform.data['enddate'])[0:10]
        adzoneid=str(myform.data['adzoneid'])
        rp=mr.myreport(begintime=begintime,adzoneids=adzoneid)
        data,filed,tmpsql=rp.getmtpinguhour()
        return render_template('reportmtpingguhour.html',form=myform,data=data,filed=filed,tmpsql=tmpsql)
    return render_template('reportmtpingguhour.html',form=myform)
#菜单名：地域指标效果数据
# 查询维度:日期，广告位，广告主
@hdtreport.route('/reporregionbyday/',methods=('POST','GET'))
def reporregionbyday():
    myform=ft.myreporregionbyday()
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        endtime=str(myform.data['enddate'])[0:10]
        adzoneid=str(myform.data['adzoneid'])
        advertiser=str(myform.data['advertiser'])
        rp=mr.myreport(begintime=begintime,endtime=endtime,adzoneids=adzoneid,advertiser_id=advertiser)
        data,filed,tmpsql=rp.getregionbyday()
        return render_template('reporregionbyday.html',form=myform,data=data,filed=filed,tmpsql=tmpsql)
    return render_template('reporregionbyday.html',form=myform)
#菜单名：广告主地域效果
#查询项：广告位ID，日期        #省（查出来在页面上）
@hdtreport.route('/reporregionbyadv/',methods=('POST','GET'))
def reporregionbyadv():
    myform=ft.myreporregionbyadv()
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        endtime=str(myform.data['enddate'])[0:10]
        adzoneid=str(myform.data['adzoneid'])
        region=str(myform.data['region'])
        rp=mr.myreport(begintime=begintime,endtime=endtime,adzoneids=adzoneid,region=region)
        data,filed,tmpsql=rp.getregionbyadv()
        return render_template('reporregionbyadv.html',form=myform,data=data,filed=filed,tmpsql=tmpsql)
    return render_template('reporregionbyadv.html',form=myform)