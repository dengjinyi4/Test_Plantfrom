# -*- coding: utf-8 -*-
__author__ = 'jinyi'
import time
from datetime import  datetime
from flask import Flask,request,render_template,Blueprint,flash,url_for,jsonify
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
        searchword=str(myform.data['searchword'])
        # data=adzone.getadzoneinfo(mytype=type,begintime=begintime,endtime=endtime,adzoneid=adzone_id)
        # rp=mr.myreport(begintime='2020-04-17',endtime='2020-04-17')
        rp=mr.myreport(begintime=begintime,endtime=endtime,searchword=searchword)
        data,filed,tmpsql,headtr,datasum=rp.getallreport()
        return render_template('reportall.html',form=myform,data=data,filed=filed,tmpsql=tmpsql,headtr=headtr,datasum=datasum)
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
# http://mytest.adhudong.com/hdtreport/reportmtpinggu/?adzoneid=7915&begindate=2020-11-18&enddate=2020-11-25&key=dGVzdF83NjBjYWU0OWM1ZTI3MDYzY2ZkZTI0MWQwZjBmMzViZg==
# key=用户名_密码 base64加密
@hdtreport.route('/reportmtpinggu/',methods=('POST','GET'))
def reportmtpinggu():
    myform=ft.myreporpingguday()
    addfieldnum=0
    if request.args.get('enddate')  and  request.args.get('begindate'):
        adzoneid=request.args.get('adzoneid')
        begindate=request.args.get('begindate')
        enddate=request.args.get('enddate')
        myform.adzoneid.data=adzoneid
        myform.begindate.data=begindate
        myform.enddate.data=enddate
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
# http://mytest.adhudong.com/hdtreport/reportmtpingguhour/?adzoneid=7915&begindate=2020-11-18&enddate=2020-11-25&key=dGVzdF83NjBjYWU0OWM1ZTI3MDYzY2ZkZTI0MWQwZjBmMzViZg==
# key=用户名_密码 base64加密
@hdtreport.route('/reportmtpingguhour/',methods=('POST','GET'))
def reportmtpingguhour():
    myform=ft.myreporpingguhour()
    addfieldnum=0
    if  request.args.get('begindate') and request.args.get('enddate'):
        adzoneid=request.args.get('adzoneid')
        begindate=request.args.get('begindate')
        enddate=request.args.get('enddate')
        myform.adzoneid.data=adzoneid
        myform.begindate.data=begindate
        myform.enddate.data=enddate
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
        data,filed,tmpsql,datasum=rp.getmtpinguhour()
        return render_template('reportmtpingguhour.html',form=myform,data=data,filed=filed,tmpsql=tmpsql,datasum=datasum,advertiser=advertiser,addfieldnum=addfieldnum)
    return render_template('reportmtpingguhour.html',form=myform)

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




#菜单名：订单状态
@hdtreport.route('/reportOrderState/',methods=('POST','GET'))
def reportOrderState():
    myform=ft.myreportOrderState()
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        adzoneid=str(myform.data['adzoneid'])
        isstatus=str(myform.data['isstatus'])
        rp=mr.myreport(begintime=begintime,adzoneids=adzoneid,isstatus=isstatus)
        data,filed,tmpsql=rp.getreportOrderState()
        return render_template('reportOrderState.html',form=myform,data=data,filed=filed,tmpsql=tmpsql)
    return render_template('reportOrderState.html',form=myform)


#菜单名：广告位趋势
@hdtreport.route('/reportZoneTrend/',methods=('POST','GET'))
def reportZoneTrend():
    myform=ft.myreportZoneTrend()
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        endtime=str(myform.data['enddate'])[0:10]
        rp=mr.myreport(begintime=begintime,endtime=endtime)
        data,filed,tmpsql,colspanx,dataSum=rp.getreportZoneTrend()
        return render_template('reportZoneTrend.html',form=myform,data=data,filed=filed,tmpsql=tmpsql,colspanx=colspanx,dataSum=dataSum)
    return render_template('reportZoneTrend.html',form=myform)

#菜单名：预估毛利（日表）
@hdtreport.route('/reportPreProfitbyDay/',methods=('POST','GET'))
def reportPreProfitbyDay():
    myform=ft.myreportPreProfitbyDay()
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        endtime=str(myform.data['enddate'])[0:10]
        if myform.data['showbaidu']:
            showbaidu='1'
        else:
            showbaidu='0'
        rp=mr.myreport(begintime=begintime,endtime=endtime,showbaidu=showbaidu)
        data,filed,tmpsql=rp.getreportPreProfitbyDay()
        return render_template('reportPreProfitbyDay.html',form=myform,data=data,filed=filed,tmpsql=tmpsql)
    return render_template('reportPreProfitbyDay.html',form=myform)



#菜单名：活动维度广告主效果
@hdtreport.route('/reportAdzoneActEffect/',methods=('POST','GET'))
def reportAdzoneActEffect():
    myform=ft.myreportAdzoneActEffect()
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        endtime=str(myform.data['enddate'])[0:10]
        adzoneid=str(myform.data['adzoneid'])
        advertiser=str(myform.data['advertiser'])
        act=str(myform.data['act'])
        rp=mr.myreport(begintime=begintime,endtime=endtime,adzoneids=adzoneid,advertiser_id=advertiser,actid=act)
        data,filed,tmpsql,colspanx,datasum=rp.getreportAdzoneActEffect()
        return render_template('reportAdzoneActEffect.html',form=myform,data=data,filed=filed,tmpsql=tmpsql,colspanx=colspanx,datasum=datasum)
    return render_template('reportAdzoneActEffect.html',form=myform)


#易积分后台报表    菜单名---- 易积分后台报表
@hdtreport.route('/repotyijifen/',methods=('POST','GET'))
def repotyijifen():
    myform=ft.myreportyijifen()
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        endtime=str(myform.data['enddate'])[0:10]
        type=str(myform.data['type'])[0:10]
        rp=mr.myreport(begintime=begintime,endtime=endtime,type=type)
        data,filed,tmpsql,headtr=rp.getyijifen()
        return render_template('reportyijifenall.html',form=myform,data=data,filed=filed,tmpsql=tmpsql,headtr=headtr)
    data=[]
    return render_template('reportyijifenall.html',data=data,form=myform)

#易积分后台报表    菜单名---- 易积分后台报表没有消耗端
@hdtreport.route('/repotyijifenall/',methods=('POST','GET'))
def repotyijifenall():
    myform=ft.myreportyijifen()
    if myform.validate_on_submit():
        begintime=str(myform.data['begindate'])[0:10]
        endtime=str(myform.data['enddate'])[0:10]
        type=str(myform.data['type'])[0:10]
        rp=mr.myreport(begintime=begintime,endtime=endtime,type=type)
        data,filed,tmpsql,headtr=rp.getyijifenall()
        return render_template('reportyjfall.html',form=myform,data=data,filed=filed,tmpsql=tmpsql,headtr=headtr)
    data=[]
    return render_template('reportyjfall.html',data=data,form=myform)


#易积分后台报表    菜单名---- 易积分后台报表没有消耗端更新数据接口
@hdtreport.route('/yjf_update/',methods=('POST','GET'))
def yjf_update():
    yjf_data_report_id=request.args.get('yjf_data_report_id')
    value=request.args.get('value')
    type=request.args.get('type')
    rp=mr.myreport(yjf_data_report_id=yjf_data_report_id,value=value,update_type=type)
    rp.yjf_update()
    return jsonify({"code":"200"})


