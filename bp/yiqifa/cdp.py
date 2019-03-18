# -*- coding: utf-8 -*-
__author__ = 'Administrator'
from flask import Blueprint, request, render_template
from business_modle.yiqifa.FinancLayer import *
from business_modle.yiqifa import cdbEsForm as cf
from business_modle.yiqifa import esImplement as ei
#创建活动蓝图
cdpRoute = Blueprint('CDP', __name__,template_folder='templates')
@cdpRoute.route('yiqifaCdpES/',methods=['GET','POST'])
def yiqifaCdpES():
     form = cf.MyForm()
     # print form.is_submitted()
     # print form.validate()
     cdplist=[]
     if form.validate_on_submit():
       esKeyValue = form.data['esKeyValue'] #搜索键值
       myenv = form.data['myenv']  #环境
       cdpValue = form.data['cdpValue']  #搜索值
       dataSource = form.data['dataSource']  #来源
       Indexes=request.args.get('Indexes') #索引
       actionType = form.data['actionType'] #行为类型
       cdplist = ei.getEsByKey(esKeyValue,myenv,cdpValue,dataSource,actionType,Indexes)
       return render_template('cdpBusiness.html',form=form,cdplist=cdplist)
     return render_template('cdpBusiness.html',form=form,cdplist=cdplist)

#对比mySql和Es数据
@cdpRoute.route('yiqifaCdpMysql/',methods=['GET','POST'])
def yiqifaCdpMysql():
    myenv=request.args.get('myenv')
    actionNo=request.args.get('actionNo')
    dataSource=request.args.get('dataSource')
    Indexes=request.args.get('Indexes')
    dictList = ei.getMysqlByActionNo(myenv,actionNo,dataSource) #返回查询mysql数据List
    esResults = ei.getEsByActionNo(myenv,actionNo,dataSource,Indexes)  #返回查询Es数据List
    return render_template('/cdpDataFile.html',dictList=dictList,esResults=esResults)
