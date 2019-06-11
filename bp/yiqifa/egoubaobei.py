# -*- coding: utf-8 -*-
__author__ = 'jinyi'
from flask import Flask,request,render_template,Blueprint,flash,url_for
from business_modle.querytool import plantfromwtf as ft
from business_modle.querytool import egoubaobei as baobei
from business_modle.querytool import egoubaobei_jd as baobei_jd
egoubaobei = Blueprint('egoubaobei', __name__,template_folder='templates')

@egoubaobei.route('/payorder/',methods=('POST','GET'))
def payorder():
    myform=ft.egoubaobei_orderpay()
    if myform.validate_on_submit():
        orderid=myform.data['orderid']
        order_status=myform.data['order_status']
        re=baobei.orderpay(str(orderid))
        return render_template('egoubaobei/orderstatus.html',data=str(re.text),form=myform)
        # return str(orderid)+str(order_status)
    return render_template('egoubaobei/orderstatus.html',form=myform)

@egoubaobei.route('/getproduct/',methods=('POST','GET'))
def getproduct():
    myform=ft.egoubaobei_product()
    if myform.validate_on_submit():
        skuid=myform.data['skuid']
        jd=baobei_jd.product_jd(skuid)
        re=jd.get_jd_goods()
        return render_template('egoubaobei/baobeiproduct.html',data=re,form=myform)
        # return str(orderid)+str(order_status)
    return render_template('egoubaobei/baobeiproduct.html',form=myform,data='')