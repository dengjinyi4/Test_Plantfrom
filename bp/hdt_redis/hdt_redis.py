# -*- coding: utf-8 -*-
import time
from flask import Flask,request,render_template,Blueprint,flash,url_for
from business_modle.querytool import myredis as mr
from business_modle.querytool import myredis_status as mrs
from business_modle.querytool import plantfromwtf as ft
from business_modle.querytool import bidding_analysis as ba
from adzone_limit import AdzoneOrders

hdtredis = Blueprint('hdt_redis', __name__,template_folder='templates')
# 查看缓存中订单的预算
@hdtredis.route('/myredis/',methods=('POST','GET'))
def myredis():
    myform=ft.myredis()
    if myform.validate_on_submit():
        myenv=myform.data['myenv']
        print myenv
        mybudget,allcount,negativecount=mr.mygetredis(myenv,'voyager:budget')
        return render_template('myredis.html',mybudget=mybudget,allcount=allcount,negativecount=negativecount,form=myform,myenv=myenv)
    return render_template('myredis.html',form=myform)
# 订单小时预算
@hdtredis.route('/budget_control/')
def budget_control():
    adorder=request.args.get('orderno')
    # page=request.args.get('page')
    key='voyager:budget_control:'+str(adorder)
    myenv=request.args.get('myenv')
    print key
    tmp_all=mr.mygetredis(myenv,key)
    # 当前小时
    myhour=int(time.strftime("%H", time.localtime()))
    return render_template('buggetcontrol.html',tmp_all=tmp_all,myhour=myhour)
@hdtredis.route('/myredis_status/',methods=('POST','GET'))
def myredis_status():
    if request.method=='GET':
        return render_template('myredis_status.html')
    else:
        jobid1=request.form.get('jobid')
        # mybudget=''
        if jobid1=='120':
            data='<option selected="selected">缓存中的订单状态：生产</option>'
            redis_nodes=[{"host":'123.59.17.118',"port":'13601'},{"host":'123.59.17.85',"port":'13601'},{"host":'123.59.17.11',"port":'13601'}]
            # mybudget,allcount,negativecount=mr.mygetredis(redis_nodes)
            # return render_template('myredis.html',mybudget=mybudget,allcount=allcount,negativecount=negativecount)
        elif jobid1=='110':
            data='<option selected="selected">缓存中的订单状态：测试</option>'
            redis_nodes=[{"host":'101.254.242.11',"port":'17001'},{"host":'101.254.242.12',"port":'17001'},{"host":'101.254.242.17',"port":'17001'}]
        order_status,allcount,negativecount=mrs.mygetredis(redis_nodes)
        return render_template('myredis_status.html',order_status=order_status,allcount=allcount,negativecount=negativecount,data=data)
@hdtredis.route('/orderresion/',methods=('POST','GET'))
def orderresion():
    myform1=ft.orderresion1()
    if myform1.validate_on_submit():
        begindate=myform1.data['begindate']
        enddate=myform1.data['enddate']
        adzoneClickid=myform1.data['adzone_id']
        ad_order_id=myform1.data['ad_order_id']
        myenv=myform1.data['myenv']
        mydata=ba.allorderdit(str(begindate),str(enddate),adzoneClickid,ad_order_id,myenv)
        print 111111111111
        print mydata
        return render_template('orderresion.html',form1=myform1,mydata1=mydata)
    return render_template('orderresion.html',form1=myform1)

@hdtredis.route('/adzone_limit/',methods=['GET'])
def adzone_limit_diff():
    aod = AdzoneOrders()
    re = aod.find_diff()
    return render_template('adzone_limit_diff.html',adzoneID=re[1],consum=re[0])