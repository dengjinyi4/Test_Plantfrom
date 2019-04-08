#!flask/bin/env python
#coding:utf-8
import sys
reload(sys)
import json
from collections import Counter
import requests
from elasticsearch import Elasticsearch
from business_modle.yiqifa import esBody
from hdt_tools.utils import DbConnection as fb

#根据键值查询CDP_ES数据
def getEsByKey(esKeyValue,myenv,cdpValue,dataSource,actionType,Indexes):
    if myenv == 'dev': #查询es线上环境
        es=Elasticsearch(["http://221.122.127.41:9200"])
        body=esBody.Body(actionType,dataSource,esKeyValue,cdpValue,myenv)
    elif myenv == 'test': #查询es测试环境
        es = Elasticsearch(["http://172.16.105.37:9200"])
        body = esBody.Body(actionType,dataSource,esKeyValue,cdpValue,myenv)
    elif myenv == 'development':  #查询es开发环境
        es=Elasticsearch(["http://172.16.18.118:9200"])
        body=esBody.Body(actionType,dataSource,esKeyValue,cdpValue,myenv)
    #查询es，循环es数据
    res = es.search(index=Indexes,size=1000,body=body)
    return analysisEs(res)

#根据订单号，查询Mysql数据
def getMysqlByActionNo(myenv,actionNo,dataSource):
    tmplist = []
    if myenv == "development" or myenv == 'test':
        strSql = "SELECT UNION_CAMPAIGN_ID, COMMODITY_NO,FEEDBACK_TAG ORDER_NO FROM fanxian.finance_unabridged_order WHERE ORDER_NO ="+actionNo
        results = fb.ExecuteSelectList(strSql,"mysql_fanxian")
    elif myenv == 'dev':
        strSql = "SELECT UNION_CAMPAIGN_ID, COMMODITY_NO,FEEDBACK_TAG ORDER_NO FROM fanxian.finance_unabridged_order WHERE ORDER_NO ="+actionNo
        results = fb.ExecuteSelectList(strSql,"mysql_fanxian")
    for rs in results:
        res = requests.get("http://cdpapi.adhudong.com/cdp/egouclick?clickId='"+ rs[2]+"'") #获取反馈标签
        res.encoding = 'utf-8'
        print(res.text)
        if rs[0]=="2060": #淘宝订单，查询淘宝商品
            tmpSql ="SELECT  f.ORDER_NO AS actionNo,f.COMMODITY_NO,f.EXPECTED_MONEY AS cost,f.ORDER_TIME AS actionTime,f.EXPECTED_COMMISSION AS commission,f.FEEDBACK_TAG,  CASE f.STATUS 	WHEN 0 THEN 'original'	WHEN 1 THEN 'invalid'	WHEN 2 THEN 'valid'	WHEN 3 THEN 'invalid'	WHEN 4 THEN 'valid'	WHEN 5 THEN 'invalid'	WHEN 6 THEN 'invalid'	ELSE 'invalid'END AS 'STATUS',f.CREATE_TIME,f.user_id,u.register_time,p.ICON,p.PHONE AS phone,m.BIND_UID AS wechatUnionid,t.title,k.id,k.page,k.ip,k.ua,k.to_time,CASE k.pos 	WHEN 'btnzms' THEN '分享'	WHEN 'btnfxz' THEN '自买'	ELSE ''END AS 'exportType',t.category_lv1,c.text,t.category_lv2,s.text,t.discount_price AS productPresentPrice,t.reserve_price AS 原价,CASE t.is_post	WHEN 0 THEN 'false'	WHEN 1 THEN 'true'	ELSE 'false'END AS 'isPostageFree',CASE t.label1_money	WHEN '' THEN 'false'	ELSE 'true'END AS 'isCoupon',o.WEBSITE_ALIAS FROM `fanxian`.finance_unabridged_order f  LEFT JOIN `fanxian`.`reg_user` u ON f.user_id = u.id  LEFT JOIN `fanxian`.`personal_user` p  ON f.user_id =  p.USER_ID  LEFT JOIN `fanxian`.`mcs_bind_info` m ON  f.user_id =  m.USER_ID AND m.BIND_TYPE='weixin' LEFT JOIN `taobao`.`taobao_egou_item` t ON f.COMMODITY_NO = t.num_iid LEFT JOIN `taobao`.`taobao_item_cats` c ON t.category_lv1 = c.id   LEFT JOIN `taobao`.`taobao_item_cats` s ON t.category_lv2 = s.id  LEFT JOIN `user_order`.`click20190101` k ON f.FEEDBACK_TAG = k.id  LEFT JOIN fanxian.shop_order_mapping o ON  f.UNION_CAMPAIGN_ID=o.UNION_CAMPAIGN_ID  AND f.UNION_CAMPAIGN_ID IS NOT NULL WHERE f.UNION_CAMPAIGN_ID=2060 AND f.ORDER_NO  ="+actionNo
            tmpResults = fb.ExecuteSelectList(tmpSql,"mysql_fanxian")
            # if tmpResults: #返回了数据，渲染页面
            #     tmplist=renderingSource("1",rs[0],tmpResults)
            # else: #返回了数据，渲染页面
            #     tSql = "SELECT  f.ORDER_NO AS actionNo,f.COMMODITY_NO,f.EXPECTED_MONEY AS cost,f.ORDER_TIME AS actionTime,f.EXPECTED_COMMISSION AS commission,f.FEEDBACK_TAG,  CASE f.STATUS 	WHEN 0 THEN 'original'	WHEN 1 THEN 'invalid'	WHEN 2 THEN 'valid'	WHEN 3 THEN 'invalid'	WHEN 4 THEN 'valid'	WHEN 5 THEN 'invalid'	WHEN 6 THEN 'invalid'	ELSE 'invalid'END AS 'STATUS',f.CREATE_TIME,f.user_id,u.register_time,p.ICON,p.PHONE AS phone,m.BIND_UID AS wechatUnionid,t.title,k.id,k.page,k.ip,k.ua,k.to_time,CASE k.pos 	WHEN 'btnzms' THEN '分享'	WHEN 'btnfxz' THEN '自买'	ELSE ''END AS 'exportType',t.category_lv1,c.text,t.category_lv2,s.text,t.discount_price AS productPresentPrice,t.reserve_price AS 原价,CASE t.is_post	WHEN 0 THEN 'false'	WHEN 1 THEN 'true'	ELSE 'false'END AS 'isPostageFree',CASE t.label1_money	WHEN '' THEN 'false'	ELSE 'true'END AS 'isCoupon',o.WEBSITE_ALIAS FROM `fanxian`.finance_unabridged_order f  LEFT JOIN `fanxian`.`reg_user` u ON f.user_id = u.id  LEFT JOIN `fanxian`.`personal_user` p  ON f.user_id =  p.USER_ID  LEFT JOIN `fanxian`.`mcs_bind_info` m ON  f.user_id =  m.USER_ID AND m.BIND_TYPE='weixin' LEFT JOIN `taobao`.`taobao_egou_item` t ON f.COMMODITY_NO = t.num_iid LEFT JOIN `taobao`.`taobao_item_cats` c ON t.category_lv1 = c.id   LEFT JOIN `taobao`.`taobao_item_cats` s ON t.category_lv2 = s.id  LEFT JOIN `user_order`.`click20190101` k ON f.FEEDBACK_TAG = k.id  LEFT JOIN fanxian.shop_order_mapping o ON  f.UNION_CAMPAIGN_ID=o.UNION_CAMPAIGN_ID  AND f.UNION_CAMPAIGN_ID IS NOT NULL WHERE f.UNION_CAMPAIGN_ID=2060 AND f.ORDER_NO  ="+actionNo
            #     tResults = fb.ExecuteSelectList(tSql,"mysql_fanxian")
            tmplist = renderingSource("2",rs[0],tmpResults)
        else:  #商城订单
           return
    return tmplist

#渲染MySql页面数据，返回list
def renderingSource(tmp,campaign_id,results):
    tmplist = []
    for rs in results:
        tmpdict = {}
        tmpdict["actionNo"] = rs[0]
        tmpdict["COMMODITY_NO"] = rs[1]
        tmpdict["cost"] = rs[2]
        tmpdict["UNION_CAMPAIGN_ID"] = campaign_id
        tmpdict["advertiserName"] = rs[28]
        tmpdict["actionTime"] = rs[3]
        tmpdict["commission"] = rs[4]
        tmpdict["FEEDBACK_TAG"] =rs[5]
        tmpdict["STATUS"] = rs[6]
        tmpdict["CREATE_TIME"] = rs[7]
        tmpdict["channel"] = "egou"
        tmpdict["user_id"] = rs[8]
        tmpdict["register_time"] = rs[9]
        tmpdict["ICON"] = rs[10]
        tmpdict["phone"] = rs[11]
        tmpdict["wechatUnionid"] = rs[12]
        tmpdict["title"] = rs[13]
        tmpdict["exportId"] = rs[14]
        tmpdict["page"] = rs[15]
        tmpdict["ip"] = rs[16]
        tmpdict["ua"] = rs[17]
        tmpdict["to_time"] = rs[18]
        tmpdict["exportType"] = rs[19]
        if tmp == "2":  # 2060 商品信息
            tmpdict["category_lv1"] = rs[21]
            tmpdict["category_lv2"] = rs[23]
            tmpdict["productPresentPrice"] = rs[24]
            tmpdict["reserve_price"] = rs[25]
            tmpdict["isPostageFree"] = rs[26]
            tmpdict["isCoupon"] = rs[27]
        else:
            tlist = getEsByProductId(rs[1]) #查询亿起发商品库ES信息
            for hit in tlist["hits"]["hits"]:
              tmpdict["actionTime"]=hit["_source"]["actionTime"]
        tmplist.append(tmpdict)
    return tmplist

#读取亿起发ES商品数据
def getEsByProductId(productId):
    es=Elasticsearch(["http://172.16.18.118:9200"])
    body={
  "query": {
   "bool":{
          "must": [
            {"term": {
              "product_id": {
                "value": ""
              }
            }}
          ]

        }
    }
}
    body['query']["bool"]['must'][0]['term']['dataSource']="{0}".format(productId)
    res = es.search(index="yiqifa_product/complete_product/_search",size=1000,body=body)
    return res

#根据dataSource和actionNo查询【CDP-ES】数据
def getEsByActionNo(myenv,actionNo,dataSource,Indexes):
    if myenv=="development":
        es=Elasticsearch(["http://172.16.18.118:9200"])
        body=esBody.BodyByActionNo(dataSource,actionNo)
        res = es.search(index=Indexes,size=1000,body=body)
    elif myenv=='test': #查询es测试环境
        es=Elasticsearch(["http://172.16.105.37:9200"])
        body=esBody.BodyByActionNo(dataSource,actionNo)
        res = es.search(index=Indexes,size=1000,body=body)
    elif myenv=='dev': #查询es生产环境
        es=Elasticsearch(["http://221.122.127.41:9200"])
        body=esBody.BodyByActionNo(dataSource,actionNo)
        res = es.search(index=Indexes,size=1000,body=body)
    return analysisEs(res)

#解析CDP_ES数据返回list
def analysisEs(res):
    tmplist=[]
    for hit in res["hits"]["hits"]:
        tmpdict={}
        tmpdict["actionTime"]=hit["_source"]["actionTime"]
        tmpdict["advertiserName"]=hit["_source"]["advertiserName"]
        tmpdict["campaignName"]=hit["_source"]["campaignName"]
        tmpdict["actionStatus"]=hit["_source"]["actionStatus"]
        tmpdict["actionType"]=hit["_source"]["actionType"]
        tmpdict["dataSource"]=hit["_source"]["dataSource"]
        tmpdict["advertiserName"]=hit["_source"]["advertiserName"]
        tmpdict["actionNo"]=hit["_source"]["actionNo"]
        if 'phoneCity' in hit["_source"]:
            tmpdict["phoneCity"]=hit["_source"]["phoneCity"]
        else:
            tmpdict["phoneCity"]=""
        if 'exportCity' in hit["_source"]:
            tmpdict["exportCity"]=hit["_source"]["exportCity"]
        else:
            tmpdict["exportCity"]=""
        if 'exportOs' in hit["_source"]:
            tmpdict["exportOs"]=hit["_source"]["exportOs"]
        else:
            tmpdict["exportOs"]=""
        if 'exportPhoneBrand' in hit["_source"]:
            tmpdict["exportPhoneBrand"]=hit["_source"]["exportPhoneBrand"]
        else:
            tmpdict["exportPhoneBrand"]=""
        if 'exportTerminal' in hit["_source"]:
            tmpdict["exportTerminal"]=hit["_source"]["exportTerminal"]
        else:
            tmpdict["exportTerminal"]=""
        if 'exportTime' in hit["_source"]:
            tmpdict["exportTime"]=hit["_source"]["exportTime"]
        else:
            tmpdict["exportTime"]=""
        if 'exportProvince' in hit["_source"]:
            tmpdict["exportProvince"]=hit["_source"]["exportProvince"]
        else:
            tmpdict["exportProvince"]=""
        if 'phoneProvince' in hit["_source"]:
            tmpdict["phoneProvince"]=hit["_source"]["phoneProvince"]
        else:
            tmpdict["phoneProvince"]=""
        if 'exportBrowser' in hit["_source"]:
            tmpdict["exportBrowser"]=hit["_source"]["exportBrowser"]
        else:
            tmpdict["exportBrowser"]=""
        if 'exportId' in hit["_source"]:
            tmpdict["exportId"]=hit["_source"]["exportId"]
        else:
            tmpdict["exportId"]=""
        if 'isCoupon' in hit["_source"]:
            tmpdict["isCoupon"]=hit["_source"]["isCoupon"]
        else:
            tmpdict["isCoupon"]=""
        if 'isPostageFree' in hit["_source"]:
            tmpdict["isPostageFree"]=hit["_source"]["isPostageFree"]
        else:
            tmpdict["isPostageFree"]=""
        if 'productPriceRebate' in hit["_source"]:
            tmpdict["productPriceRebate"]=hit["_source"]["productPriceRebate"]
        else:
            tmpdict["productPriceRebate"]=""
        if 'productReducePrice' in hit["_source"]:
            tmpdict["productReducePrice"]=hit["_source"]["productReducePrice"]
        else:
            tmpdict["productReducePrice"]=""
        if 'productPresentPrice' in hit["_source"]:
            tmpdict["productPresentPrice"]=hit["_source"]["productPresentPrice"]
        else:
            tmpdict["productPresentPrice"]=""
        if 'productCategory1' in hit["_source"]:
            tmpdict["productCategory1"]=hit["_source"]["productCategory1"]
        else:
            tmpdict["productCategory2"]=""
        if 'productCategory1' in hit["_source"]:
            tmpdict["productCategory2"]=hit["_source"]["productCategory2"]
        else:
            tmpdict["productCategory2"]=""
        if 'campaignName' in hit["_source"]:
            tmpdict["campaignName"]=hit["_source"]["campaignName"]
        else:
            tmpdict["campaignName"]=""
        if 'phone' in hit["_source"]:
            tmpdict["phone"]=hit["_source"]["phone"]
        else:
            tmpdict["phone"]=""
        if 'egouId' in hit["_source"]:
            tmpdict["egouId"]=hit["_source"]["egouId"]
        else:
            tmpdict["egouId"]=""
        if 'commission' in hit["_source"]:
            tmpdict["commission"]=hit["_source"]["commission"]
        else:
            tmpdict["commission"]=""
        if 'productName' in hit["_source"]:
            tmpdict["productName"]=hit["_source"]["productName"]
        else:
            tmpdict["productName"]=""
        if 'productPresentPrice' in hit["_source"]:
            tmpdict["productPresentPrice"]=hit["_source"]["productPresentPrice"]
        else:
            tmpdict["productPresentPrice"]=""
        if 'channel' in hit["_source"]:
            tmpdict["channel"]=hit["_source"]["channel"]
        else:
            tmpdict["channel"]=""
        if 'cost' in hit["_source"]:
            tmpdict["cost"]=hit["_source"]["cost"]
        else:
            tmpdict["cost"]=""
        tmplist.append(tmpdict)
    return tmplist

