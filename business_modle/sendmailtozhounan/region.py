#encoding:utf-8
__author__ = 'jinyi'

import sys
from business_modle.querytool import db
import requests as r
import MySQLdb as mysql ,time,datetime,calendar
import Emar_SendMail_Attachments as emarmail
from decimal import  Decimal
# from openpyxl import Workbook
reload(sys)
sys.setdefaultencoding('utf-8')
# 处理ipsevice中没有的ip段，收集这些ip段放到ipservice中
def getbeijing_region():
    sql='''SELECT 'beijing',ip FROM voyagerlog.ad_show_log20191014 where region='天津天津' '''
    re=db.selectsql('devvoyager',sql)
    # print re
    tmpbeijing=[]
    for i in re:
        tlist=str(i[1]).split('.')
        tip=tlist[0]+'.'+tlist[1]+'.'+tlist[2]
        if tip not in tmpbeijing:
            tmpbeijing.append(tip)
    print '111111111111111111111'
    print tmpbeijing
    return 1
def getregion():
    tmpsql='''
select start_ip1,cityid from voyager.ipservice where create_time is not null and (city not LIKE'%北京%' and city not LIKE'%上海%' and city not LIKE'%天津%') and city LIKE '%市%';'''
    result=db.selectsql('testvoyager',tmpsql)
    url='https://api01.aliyun.venuscn.com/ip?'
    theader={'Authorization':"APPCODE 870b5c272b134c6396bb1f66ad1b588b"}
    tmperr=[]
    for i in result:
        print i
        para={"ip":str(i[0])}
        r1=r.Session()
        time.sleep(2)
        res=r1.get(url,headers=theader,params=para)
        print res.text
        city_id=str(res.json()['data']['city_id'])
        if city_id<>str(i[1]):
            tmperr.append(i[0])
    print tmperr
    return 1

def getregionbeijing1():
    tmpsql='''select start_ip1,cityid from voyager.ipservice where create_time is not null and city  LIKE'%北京%' ;'''
    result=db.selectsql('testvoyager',tmpsql)
    url='https://api01.aliyun.venuscn.com/ip?'
    theader={'Authorization':"APPCODE 870b5c272b134c6396bb1f66ad1b588b"}
    tmperr=[]
    for i in result:
        print i
        para={"ip":str(i[0])}
        r1=r.Session()
        time.sleep(2)
        res=r1.get(url,headers=theader,params=para)
        print res.text
        city_id=str(res.json()['data']['city_id'])
        if city_id=='110100':
            print 'beijing'*10
            if str(i[1])<>'110000':
                print 'not bijin' *10
                tmperr.append(i[0])
    print tmperr
    return 1


def getregiontianjin1():
    tmpsql='''select start_ip1,cityid from voyager.ipservice where create_time is not null and city  LIKE'%天津%';'''
    result=db.selectsql('testvoyager',tmpsql)
    url='https://api01.aliyun.venuscn.com/ip?'
    theader={'Authorization':"APPCODE 870b5c272b134c6396bb1f66ad1b588b"}
    tmperr=[]
    for i in result:
        print i
        para={"ip":str(i[0])}
        r1=r.Session()
        time.sleep(2)
        res=r1.get(url,headers=theader,params=para)
        print res.text
        city_id=str(res.json()['data']['city_id'])
        if city_id=='120100':
            print '天津'*10
            if str(i[1])<>'120000':
                print 'not bijin' *10
                tmperr.append(i[0])
    print tmperr
    return 1

def getregionshanghai1():
    tmpsql='''select start_ip1,cityid from voyager.ipservice where create_time is not null and city  LIKE'%上海%' ;'''
    result=db.selectsql('testvoyager',tmpsql)
    url='https://api01.aliyun.venuscn.com/ip?'
    theader={'Authorization':"APPCODE 870b5c272b134c6396bb1f66ad1b588b"}
    tmperr=[]
    for i in result:
        print i
        para={"ip":str(i[0])}
        r1=r.Session()
        time.sleep(2)
        res=r1.get(url,headers=theader,params=para)
        print res.text
        city_id=str(res.json()['data']['city_id'])
        if city_id=='310100':
            print '上海'*10
            if str(i[1])<>'310000':
                print 'not bijin' *10
                tmperr.append(i[0])
    print tmperr
    return 1

if __name__ == '__main__':
    # getbeijing_region()
    # getregionshanghai1()
    # getregiontianjin1()
    # getregionbeijing1()
    # tmp='116.171.246.25'
    # tplist=tmp.split('.')
    # print tplist[0]+'.'+tplist[1]+'.'+tplist[2]
    address=['北京市朝阳区双桥东路7号院']
    # address=['beijing']
    mykey=['北京','上海','北京市']
    # mykey=['beijing']
    re=[i for  i in mykey if i in str(address).decode('string_escape')]
    print str(re).decode('string_escape')

