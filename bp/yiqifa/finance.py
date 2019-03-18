# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from flask import Blueprint, request, render_template
from business_modle.yiqifa.FinancLayer import *
#创建活动蓝图
Finace = Blueprint('Finace', __name__,template_folder='templates')

@Finace.route('yiqiFinace/',methods=['GET','POST'])
def yiqiFinace():
    if request.method=='GET':
        return render_template('financSettlement.html')
    else:
        userId = request.form.get('userId')
        financId = request.form.get('financId')
        results = getFinaceValue(userId,financId)
        return render_template('/financSettlement.html',results=results,userId=userId,financId=financId)
