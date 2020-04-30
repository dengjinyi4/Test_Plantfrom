#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import urllib
import json,time,datetime,schedule
# from business_modle.querytool import db
from collections import Counter
from elasticsearch import Elasticsearch
def get_es(project):
    if project=='ddyz':
        es=Elasticsearch(["123.59.17.221:9200",],timeout=100300);
        body={
      "query": {
        "bool": {
          "must": [
            { "match": { "message": "ddyzreport.gouwubang.com" } },
            { "match": { "message": "responseStatus" } },
            # {"range": {"@timestamp": {"gt": "now-1h","lt": "now"}}}
          ]
        }
      },
       "size": 10000,
       "sort": {
            "@timestamp": "desc"
        }
    }
    elif project=='bidding' :
       es=Elasticsearch(["123.59.17.221:9200",],timeout=100300);
    #    body={
    #   "query": {
    #     "bool": {
    #       "must": [
    #         { "match": { "message": "bridge.do" } },
    #         {"range": {
    #             "@timestamp": {
    #              "gte":1586324400,
    #             "lte":1586325600,
    #             "format":"epoch_millis"}}}
    #       ]
    #     }
    #   },
    #    "size": 11,
    #    "sort": {
    #         "@timestamp": "desc"
    #     }
    # }
    body={
  "version": True,
  "size": 10000,
  "sort": [
    {
      "@timestamp": {
        "order": "desc",
        "unmapped_type": "boolean"
      }
    }
  ],
  "query": {
    "bool": {
      "must": [
        {
          "query_string": {
            "analyze_wildcard": True,
            "query": "bridge.do"
          }
        },
        {
          "range": {
            "@timestamp": {
              "gte": 1586324400000,
              "lte": 1586325616401,
              "format": "epoch_millis"
            }
          }
        }
      ],
      "must_not": []
    }
  },
  "aggs": {
    "2": {
      "date_histogram": {
        "field": "@timestamp",
        "interval": "30s",
        "time_zone": "Asia/Shanghai",
        "min_doc_count": 1
      }
    }
  }}
    try:
        res = es.search(index="logstash-nginxlog-*", body=body)
    except Exception as e:
        print e.message
    return res

def getbidinglog():
    res=get_es('bidding')
    tmp=[]
    for hit in res["hits"]["hits"]:
        if "&status=" in hit['_source']['request']  and "&adChoosenTag=" in  hit['_source']['request']:
            status=str(str(hit['_source']['request']).split('&status=')[1].split('&')[0])
            adChoosenTag=str(str(hit['_source']['request']).split('&adChoosenTag=')[1].split('&')[0])
            if status=="1" and adChoosenTag<>'':
                # tmp.append(str(hit['_source']['request']))
                tmp.append(str(adChoosenTag))
        print '处理到第{}条数据'.format(str(res["hits"]["hits"].index(hit)))
    f1=open('D:/nginxlogs/biddingbridge{0}.txt'.format(datetime.datetime.now().strftime('%Y-%m-%d%H%M%S')),'w+')
    for i in range(0,len(tmp)-1) :
        f1.write(tmp[i]+'\n')
    f1.close()

    return tmp

def get_esapishop(project):
    if project=='apishop':
        es=Elasticsearch(["221.122.127.68:9200",],timeout=100300);
        body={
      "query": {
        "bool": {
          "must": [
            { "match": { "message": "com.egou.api.shop.ShareService - shop.activity.wxcode.get>>>timecost>>>" } },
            { "match": { "message": "status" } },
            # {"range": {"@timestamp": {"gt": "now-1h","lt": "now"}}}
          ]
        }
      },
       "size": 10000,
       "sort": {
            "@timestamp": "desc"
        }
    }
    try:
        res = es.search(index="logstash-egoujavalog-*", body=body)
    except Exception as e:
        print e.message
    return res
def getmessageapishop(project):
    tmpmessage=[]
    if project=='apishop':
        res=get_esapishop(project)
        for hit in res["hits"]["hits"]:
            tmp={}
            message=hit['_source']['message']
            tmp['time']=str(message[0]).split(' [')[0]
            message=json.loads(str(hit['_source']['message'][0]).split('shop.activity.wxcode.get>>>timecost>>>')[1])
            if 'methodUpCost' in message:
                tmp['methodUpCost']=message['methodUpCost']
            else:
                tmp['methodUpCost']=''
            if 'methodWxCost' in message:
                tmp['methodWxCost']=message['methodWxCost']
            else:
                tmp['methodWxCost']=''
            if 'methodTokenCost' in message:
                tmp['methodTokenCost']=message['methodTokenCost']
            else:
                tmp['methodTokenCost']=''
            if 'uuid' in message:
                tmp['uuid']=message['uuid']
            else:
                tmp['uuid']=''
            if 'methodStartEndCost' in message:
                tmp['methodStartEndCost']=message['methodStartEndCost']
            else:
                tmp['methodStartEndCost']=''
            if 'sid' in message:
                tmp['sid']=message['sid']
            else:
                tmp['sid']=''
            if 'status' in message:
                tmp['status']=message['status']
            else:
                tmp['status']=''
            tmpmessage.append(tmp)
    return tmpmessage
# 根据点击id查询出所有的过滤原因的订单
def orderbylognew(project):
    # es=Elasticsearch([{"host":"221.122.127.41"}],port=9200);

    # time.sleep(1)
    # res = es.search(index="logstash-voyagerjavalog-*", body=body)
    try:
        res = get_es(project)
        # tmpmessage=[]
        print len(res["hits"]["hits"])
        if project=='ddyz':
            tmpmessage=[]
            for hit in res["hits"]["hits"]:
                tmpdict={}
                message=hit['_source']['message']
                # print message
                requesttime=message.split('[')[1].split(' +')[0]
                if 'responseStatus=' in str(message):
                    responseStatus=message.split('responseStatus=')[1].split('&')[0]
                else:
                    responseStatus=''
                if 'method=' in str(message):
                    method=message.split('method=')[1].split('&')[0]
                else:
                    method=''
                if 'openId' in message:
                    openId=message.split('openId=')[1].split(' ')[0]
                else:
                    openId=''
                # time=message.split('time=')[1].split('&')[0]
                if '&' in message.split('time=')[1]:
                    time=message.split('time=')[1].split('&')[0]
                else:
                    time=message.split('time=')[1].split(' HTTP')[0]
                tmpdict['requesttime']=requesttime
                tmpdict['responseStatus']=responseStatus
                tmpdict['method']=method
                tmpdict['time']=time
                tmpdict['openId']=openId
                tmpmessage.append(tmpdict)
        elif project=='baobei':
            tmpmessage=[]
            for hit in res["hits"]["hits"]:
                tmpdict={}
                message=hit['_source']['message']
                # print message
                # message=message.deco
                if 'accessTerminal=' in str(message):
                    accessTerminal=message.split('accessTerminal=')[1].split('&')[0]
                else:
                    accessTerminal=''
                if accessTerminal=='1':
                    requesttime=message.split('[')[1].split(' +')[0]
                    responseStatus=message.split('responseStatus=')[1].split('&')[0]
                    method=urllib.unquote(message.split('method=')[1].split('&')[0])
                    if '&' in message.split('time=')[1]:
                        time=message.split('time=')[1].split('&')[0]
                    elif ' HTTP' in message.split('time=')[1]:
                        time=message.split('time=')[1].split(' HTTP')[0]
                    if 'userId=' in message:
                        userId=message.split('userId=')[1].split(' HTTP')[0]
                    else:
                        userId=''
                    tmpdict['responseStatus']=responseStatus
                    tmpdict['method']=method
                    tmpdict['time']=time
                    tmpdict['userId']=userId
                    tmpdict['accessTerminal']=accessTerminal
                    tmpdict['requesttime']=requesttime

                    tmpmessage.append(tmpdict)
            # print tmpmessage
    except Exception as e:
        print 111111
        print hit
        print 111111
        print e.message
    return tmpmessage
def writelog(project):
    tmpdit=orderbylognew(project)
    print tmpdit
    # f=open('1.txt','w')
    if project=='ddyz':
        f1=open('D:/nginxlogs/ddyz{0}.txt'.format(datetime.datetime.now().strftime('%Y-%m-%d%H%M%S')),'w+')
        for i in tmpdit:
            f1.write(i['requesttime']+','+i['method']+','+i['responseStatus']+','+i['time']+','+i['openId']+'\n')
        f1.close()
        # print tmpdit
    elif project=='baobei':
        f=open('D:/nginxlogs/baobei{0}.txt'.format(datetime.datetime.now().strftime('%Y-%m-%d%H%M%S')),'w+')
        f.write('baobeirequesttime'+','+'method'+','+'responseStatus'+','+'time'+','+'userId'+','+'accessTerminal'+'\n')
        # f.write(('requesttime')
        for i in tmpdit:
            f.write(i['requesttime']+','+i['method']+','+i['responseStatus']+','+i['time']+','+i['userId']+','+i['accessTerminal']+'\n')
        f.close()

def writelogapishop(project):
    tmpdit=getmessageapishop(project)
    print tmpdit
    # f=open('1.txt','w')
    if project=='apishop':
        f1=open('D:/nginxlogs/apishop{0}.txt'.format(datetime.datetime.now().strftime('%Y-%m-%d%H%M%S')),'w+')
        f1.write('time'+','+'methodUpCost'+','+'methodWxCost'+','+'methodTokenCost'+','+'uuid'+','+'methodStartEndCost'+','+'sid'+','+'status'+'\n')
        for i in tmpdit:
            f1.write(str(i['time'])+','+str(i['methodUpCost'])+','+str(i['methodWxCost'])+','+str(i['methodTokenCost'])+','+str(i['uuid'])+','+str(i['methodStartEndCost'])+','+str(i['sid'])+','+str(i['status'])+'\n')
        f1.close()
        # print tmpdit
def dojob():
    schedule.every(30).seconds.do(writelog,'ddyz')
    # schedule.every(30).seconds.do(writelog,'baobei')
    print 'do schedule'
    while True:
        schedule.run_pending()
        # time.sleep(11)
def dojob1():
    # schedule.every(3600).seconds.do(writelog,'ddyz')
    schedule.every(1).hours.do(writelog,'ddyz')
    # schedule.every(3600).seconds.do(writelog,'baobei')
    schedule.every(1).hours.do(writelog,'baobei')
    print 'do schedule'
    while True:
        schedule.run_pending()
        # time.sleep(300)


if __name__ == '__main__':
    # writelog('ddyz')
    getbidinglog()
    # writelog('baobei')
    # getmessageapishop('apishop')
    # apishops数据
    # writelogapishop('apishop')
    # dojob()
    # dojob1()
    #
    # schedule.every(1).hours.do(writelog,'ddyz')
    # schedule.every(1).hours.do(writelog,'baobei')
    # print 'do schedule'
    # while True:
    #     schedule.run_pending()