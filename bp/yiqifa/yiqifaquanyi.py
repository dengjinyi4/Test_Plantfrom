# -*- coding: utf-8 -*-
__author__ = 'jinyi'
from flask import Flask,request,render_template,Blueprint,flash,url_for
from business_modle.querytool import plantfromwtf as ft
from business_modle.querytool.yqfqy import quanyi as qy

yiqifaquanyi = Blueprint('yiqifaquanyi', __name__,template_folder='templates')

@yiqifaquanyi.route('/quanyiproduct/',methods=('POST','GET'))
def quanyiproduct():
    myform=ft.yiqifaquanyi()
    if myform.validate_on_submit():
        # orderid=myform.data['orderid']
        env=myform.data['myenv']
        quanyi=qy.quanyi(env=env)
        res,filed,tmpsql=quanyi.geproduct()
        return render_template('yiqifaquanyi/quanyiproduct.html',res=res,filed=filed,tmpsql=tmpsql,form=myform)
        # return str(orderid)+str(order_status)
    return render_template('yiqifaquanyi/quanyiproduct.html',form=myform)

@yiqifaquanyi.route('/quanyiorder/',methods=('POST','GET'))
def quanyiorder():
    myform=ft.yiqifaquanyi()
    if myform.validate_on_submit():
        # orderid=myform.data['orderid']
        env=myform.data['myenv']
        quanyi=qy.quanyi(env=env)
        res,filed,tmpsql=quanyi.georder()
        return render_template('yiqifaquanyi/quanyiorder.html',res=res,filed=filed,tmpsql=tmpsql,form=myform)
        # return str(orderid)+str(order_status)
    return render_template('yiqifaquanyi/quanyiorder.html',form=myform)

@yiqifaquanyi.route('/thirdprodcutstock/',methods=('POST','GET'))
def thirdprodcutstock():
    myform=ft.yiqifaquanyi()
    if myform.validate_on_submit():
        # orderid=myform.data['orderid']
        env=myform.data['myenv']
        quanyi=qy.quanyi(env=env)
        res,filed,tmpsql=quanyi.getthirdproduct()
        return render_template('yiqifaquanyi/getthirdproduct.html',res=res,filed=filed,tmpsql=tmpsql,form=myform)
        # return str(orderid)+str(order_status)
    return render_template('yiqifaquanyi/getthirdproduct.html',form=myform)
