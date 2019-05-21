# -*- coding: utf-8 -*-
__author__ = 'jinyi'
from flask import Flask,request,render_template,Blueprint,flash,url_for
from business_modle.querytool import plantfromwtf as ft

egoubaobei = Blueprint('egoubaobei', __name__,template_folder='templates')

@egoubaobei.route('/payouder/',methods=('POST','GET'))
def payorder():
    myform=ft.egoubaobei_orderpay()
    if myform.validate_on_submit():
        orderid=myform.data['orderid']
        order_status=myform.data['order_status']
        return render_template('egoubaobei/orderstatus.html',data=str(orderid)+str(order_status),form=myform)
        # return str(orderid)+str(order_status)
    return render_template('egoubaobei/orderstatus.html',form=myform)