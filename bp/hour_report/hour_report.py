# encoding=utf-8
__author__ = 'aidinghua'

from flask import Blueprint,render_template,request

from business_modle.testtools.hour_report_act import *
from business_modle.testtools.hour_report_adzone import *
from business_modle.testtools.hour_report_order import *

hour_report = Blueprint('hour_report',__name__)

@hour_report.route('/hour_report_act',methods=['get','post'])

def hour_report_act():
    if request.method == 'GET':
        return render_template('hour_report_act.html')

    else:
        begin_date=request.form.get('begin_date')
        begin_hour=request.form.get('begin_hour')
        end_hour=request.form.get('end_hour')
        act_id = request.form.get('act_id')

        print begin_date
        hra=Hour_report_act(begin_date,begin_hour,end_hour,act_id,False)

        re1= hra.cmp_act_shownum()
        re2= hra.cmp_act_adclicknum()
        return render_template('hour_report_act.html',begin_date=begin_date,begin_hour=begin_hour,end_hour=end_hour,act_id=act_id,re1=re1,re2=re2)


@hour_report.route('/hour_report_adzone',methods=['get','post'])

def hour_report_adzone():
    if request.method == 'GET':
        return render_template('hour_report_adzone.html')

    else:
        begin_date=request.form.get('begin_date')
        begin_hour=request.form.get('begin_hour')
        end_hour=request.form.get('end_hour')
        adzone_id = request.form.get('adzone_id')

        print begin_date
        Hra=Hour_report_adzone(begin_date,begin_hour,end_hour,adzone_id,False)

        re1= Hra.cmp_zone_clicknum()
        re2= Hra.cmp_zone_invalidnum()
        re3= Hra.cmp_mediacash()
        re4= Hra.cmp_mediaaward()
        re5= Hra.cmp_adshownum()
        re6= Hra.cmp_adclicknum()
        re7= Hra.cmp_xiexienum()





        return render_template('hour_report_adzone.html',begin_date=begin_date,begin_hour=begin_hour,end_hour=end_hour,adzone_id=adzone_id,re1=re1,re2=re2,re3=re3,re4=re4,re5=re5,re6=re6,re7=re7)


@hour_report.route('/hour_report_order',methods=['get','post'])

def hour_report_order():
    if request.method == 'GET':
        return render_template('hour_report_order.html')

    else:
        begin_date=request.form.get('begin_date')
        begin_hour=request.form.get('begin_hour')
        end_hour=request.form.get('end_hour')
        order_id = request.form.get('order_id')

        print begin_date
        Hro=Hour_report_order(begin_date,begin_hour,end_hour,order_id,False)

        re1=Hro.cmp_order_consume()
        re2=Hro.cmp_order_cashincome()
        re3=Hro.cmp_order_awardincome()
        re4=Hro.cmp_order_ad_clicknum()
        re5= Hro.cmp_order_ad_invlidnum()
        re6= Hro.cmp_order_ad_disusenum()
        re7= Hro.cmp_ad_effectshownum()
        re8= Hro.cmp_ad_invlidshownum()
        re9= Hro.cmp_ad_dissueshownum()
        re10=Hro.cmp_effect_1()
        re11=Hro.cmp_effect_2()
        re12=Hro.cmp_effect_3()
        re13= Hro.cmp_effect_4()
        re14=Hro.cmp_effect_5()
        re15=Hro.cmp_effect_6()
        re16=Hro.cmp_effect_17()
        return render_template('hour_report_order.html',begin_date=begin_date,begin_hour=begin_hour,end_hour=end_hour,order_id=order_id,re1=re1,re2=re2,re3=re3,re4=re4,re5=re5,re6=re6,re7=re7,re8=re8,re9=re9,re10=re10,re11=re11,re12=re12,re13=re13,re14=re14,re15=re15,re16=re16)
