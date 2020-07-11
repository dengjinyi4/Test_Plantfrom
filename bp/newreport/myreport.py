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
        data,filed,tmpsql,headtr=rp.getallreport()
        return render_template('reportall.html',form=myform,data=data,filed=filed,tmpsql=tmpsql,headtr=headtr)
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
        data,filed,tmpsql,headtr=rp.getadvliandong()
        return render_template('reportliandong.html',form=myform,data=data,filed=filed,tmpsql=tmpsql,headtr=headtr)
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
        data,filed,tmpsql,datasum=rp.getptmaoli()
        return render_template('repotptmaoli.html',form=myform,data=data,filed=filed,tmpsql=tmpsql,datasum=datasum)
    data=[]
    return render_template('repotptmaoli.html',data=data,form=myform)

#菜单名：毛利表-广告主维度
# 查询维度:日期，广告位，广告主
@hdtreport.route('/reportptmaoliadtag/',methods=('POST','GET'))
def reportptmaoliadtag():
    myform=ft.myreportptmaoliadtag()
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        endtime=str(myform.data['enddate'])[0:10]
        adzoneid=str(myform.data['adzoneid'])
        advertiser=str(myform.data['advertiser'])
        tagorad=str(myform.data['tagorad'])
        if myform.data['showadzone']:
            showadzone='1'
        else:
            showadzone='0'
        rp=mr.myreport(begintime=begintime,endtime=endtime,adzoneids=adzoneid,advertiser_id=advertiser,tagorad=tagorad,showadzone=showadzone)
        data,filed,tmpsql,colspanx,datasum=rp.getreportptmaoliadtag()
        return render_template('reportptmaoliadtag.html',form=myform,data=data,filed=filed,tmpsql=tmpsql,colspanx=colspanx,datasum=datasum)
    return render_template('reportptmaoliadtag.html',form=myform)



#菜单名：媒体效果-评估-日表
@hdtreport.route('/reportmtpinggu/',methods=('POST','GET'))
def reportmtpinggu():
    myform=ft.myreporpingguday()
    addfieldnum=0
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        endtime=str(myform.data['enddate'])[0:10]
        adzoneid=str(myform.data['adzoneid'])
        advertiser=str(myform.data['advertiser'])
        if advertiser :
            addfieldnum=2
        else:
            addfieldnum=0
        rp=mr.myreport(begintime=begintime,endtime=endtime,adzoneids=adzoneid,advertiser_id=advertiser)
        data,filed,tmpsql,colspanx,datasum=rp.getmtpinggu()
        return render_template('reportmtpingguday.html',form=myform,data=data,filed=filed,tmpsql=tmpsql,colspanx=colspanx,datasum=datasum,addfieldnum=addfieldnum)
    data=[]
    return render_template('reportmtpingguday.html',data=data,form=myform)


#菜单名：媒体效果-评估-小时表 4、媒体效果-去联动-评估-小时表
@hdtreport.route('/reportmtpingguhour/',methods=('POST','GET'))
def reportmtpingguhour():
    myform=ft.myreporpingguhour()
    addfieldnum=0
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        # endtime=str(myform.data['enddate'])[0:10]
        adzoneid=str(myform.data['adzoneid'])
        advertiser=str(myform.data['advertiser'])
        if advertiser :
            addfieldnum=2
        else:
            addfieldnum=0
        rp=mr.myreport(begintime=begintime,adzoneids=adzoneid,advertiser_id=advertiser)
        data,filed,tmpsql,datasum=rp.getmtpinguhour()
        return render_template('reportmtpingguhour.html',form=myform,data=data,filed=filed,tmpsql=tmpsql,datasum=datasum,advertiser=advertiser,addfieldnum=addfieldnum)
    return render_template('reportmtpingguhour.html',form=myform,addfieldnum=addfieldnum)

#菜单名：媒体效果-评估-广告主类型
@hdtreport.route('/reportByadvtag/',methods=('POST','GET'))
def reportByadvtag():
    myform=ft.myreportByadvtag()
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        endtime=str(myform.data['enddate'])[0:10]
        adzoneid=str(myform.data['adzoneid'])
        rp=mr.myreport(begintime=begintime,endtime=endtime,adzoneids=adzoneid)
        data,filed,tmpsql=rp.getreportByadvtag()
        return render_template('reportByadvtag.html',form=myform,data=data,filed=filed,tmpsql=tmpsql)
    data=[]
    return render_template('reportByadvtag.html',data=data,form=myform)


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
        data,filed,tmpsql,colspanx=rp.getregionbyday()
        return render_template('reporregionbyday.html',form=myform,data=data,filed=filed,tmpsql=tmpsql,colspanx=colspanx)
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
        data,filed,tmpsql,colspanx=rp.getregionbyadv()
        return render_template('reporregionbyadv.html',form=myform,data=data,filed=filed,tmpsql=tmpsql,colspanx=colspanx)
    return render_template('reporregionbyadv.html',form=myform)