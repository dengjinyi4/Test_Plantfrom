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
    elif project=='baobei' :
       es=Elasticsearch(["123.59.17.221:9200",],timeout=100300);
       body={
      "query": {
        "bool": {
          "must": [
            { "match": { "message": "egoubbreport.gouwubang.com" } },
            # { "match": { "message": "responseStatus" } },
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
        res = es.search(index="logstash-nginxlog-*", body=body)
    except Exception as e:
        print e.message
    return res


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
                responseStatus=message.split('responseStatus=')[1].split('&')[0]
                method=message.split('method=')[1].split('&')[0]
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
                if 'accessTerminal=' in message:
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

                tmpdict['requesttime']=requesttime
                tmpdict['responseStatus']=responseStatus
                tmpdict['method']=method
                tmpdict['time']=time
                tmpdict['userId']=userId
                tmpdict['accessTerminal']=accessTerminal
                tmpmessage.append(tmpdict)
            # print tmpmessage
    except Exception as e:
        print e.message
    return tmpmessage
def writelog(project):
    tmpdit=orderbylognew(project)
    print tmpdit
    # f=open('1.txt','w')
    if project=='ddyz':
        f1=open('../../logs/ddyz{0}.txt'.format(datetime.datetime.now().strftime('%Y-%m-%d%H%M%S')),'w+')
        for i in tmpdit:
            f1.write(i['requesttime']+','+i['method']+','+i['responseStatus']+','+i['time']+','+i['openId']+'\n')
        f1.close()
        # print tmpdit
    elif project=='baobei':
        f=open('../../logs/baobei{0}.txt'.format(datetime.datetime.now().strftime('%Y-%m-%d%H%M%S')),'w+')
        f.write('baobeirequesttime'+','+'method'+','+'responseStatus'+','+'time'+','+'userId'+','+'accessTerminal'+'\n')
        # f.write(('requesttime')
        for i in tmpdit:
            f.write(i['requesttime']+','+i['method']+','+i['responseStatus']+','+i['time']+','+i['userId']+','+i['accessTerminal']+'\n')
        f.close()
def dojob():
    schedule.every(30).seconds.do(writelog,'ddyz')
    # schedule.every(30).seconds.do(writelog,'baobei')
    print 'do schedule'
    while True:
        schedule.run_pending()
        # time.sleep(11)
def dojob1():
    schedule.every(3600).seconds.do(writelog,'ddyz')
    schedule.every(3600).seconds.do(writelog,'baobei')
    print 'do schedule'
    while True:
        schedule.run_pending()
        time.sleep(300)


if __name__ == '__main__':
    # writelog('ddyz')
    # writelog('baobei')
    # dojob()
    dojob1()