#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:dengjinyi date:2020-0331
# 广告位高级屏蔽数据处理
# private Long adzoneId;
#  private Integer type;  //类型 1 屏蔽 2 指定
#  private Integer timeType;//屏蔽时间类型 0-不限 1-限制
#  private Integer timeBegin;//屏蔽时间开始时间 （小时-数字）
#  private Integer timeEnd;//屏蔽时间结束时间 （小时-数字）
#  private Date createTime;//
#  private Integer regionType;//屏蔽地域类型 0-不限 1-限制
#  private String shieldRegion;//地域汉字，逗号分隔
#  private String creativeValue;//屏蔽创意等级（多个逗号分隔） 1：A1，3：A3,5：A5
#  private Integer advertiserIndustryType;//屏蔽广告主行业类型 0-不限 1-限制
#  private String advertiserIndustry;//行业类型id，逗号分隔
#  private Date effectiveTimeBegin;//屏蔽生效开始时间 年月日 时分秒
#  private Date effectiveTimeEnd;//屏蔽生效结束时间 年月日 时分秒
#  private Integer effectiveTimeType;//屏蔽生效类型 0-长期 1-时间段
#  private Integer advertiserIndustryTagType;//屏蔽广告主行业标签类型 0-不限 1-限制
#  private String advertiserIndustryTag;//行业标签id，逗号分隔
#  private Integer advertiserTagType;//屏蔽广告主标签类型 0-不限 1-限制
#  private String advertiserTag;//广告主标签id，逗号分隔，格式：,1,2,3,
#  private Integer advertiserIdsType;//屏蔽广告主 0-不屏蔽,1-屏蔽
#  private String advertiserIds;//广告主id字符串(多个以','分割)
#  private Integer creativeBrandTagType;//屏蔽广告主创意品牌标签(0-不屏蔽,1-屏蔽)
#  private String creativeBrandTagIds;//创意品牌标签id(多个以','分割)
#  private String advertiserIdsShow;//广告主_等级(多个以','分割)
#  private Integer termType;//屏蔽终端设备(0-不屏蔽,1-屏蔽)
#  private String  termIds;//终端id(1-安卓,2-IOS)
import requests
from business_modle.querytool import db

class adzoneinfo(object):
    def __init__(self,env='',begintime='',endtime='',adzoneid='',mytype=''):
        self.env=env
        self.begintime=begintime
        self.endtime=endtime
        self.adzoneid=adzoneid
        self.mytype=mytype

    def getindb(self,tmpsql):
        # tmpsql='''SELECT operation_content,operator,create_time
        #         from voyager.um_operation_log where create_time>'{begintime}' and create_time<'{endtime}' and operation_content LIKE '%{adzoneid}%'
        #         AND operation_target='广告位修改' ORDER BY create_time ;'''.format(begintime=begintime,endtime=endtime,adzoneid=adzoneid)
        # print tmpsql
        if self.env=='test':
            res,filed=db.selectsqlnew('testvoyager',tmpsql)
        if self.env=='dev':
            res,filed=db.selectsqlnew('devvoyager',tmpsql)
        return res,filed
    def getadzoneinfo (self):
        tmp=[]
        # 高级屏蔽
        if self.mytype=='1':
            tmpsql='''SELECT operation_content,operator,create_time
            from voyager.um_operation_log where create_time>'{begintime}' and create_time<'{endtime} 23:59:59' and operation_content LIKE '%{adzoneid}%'
            AND operation_target='广告位修改' ORDER BY create_time ;'''.format(begintime=self.begintime,endtime=self.endtime,adzoneid=self.adzoneid)
            res,filed=self.getindb(tmpsql)
            filed=['类型','屏蔽时间类型','屏蔽时间开始时间','屏蔽时间结束时间','屏蔽地域类型','地域','屏蔽创意等级','屏蔽广告主行业类型','行业类型id','屏蔽生效开始时间','屏蔽生效结束时间','屏蔽生效类型','屏蔽广告主行业标签类型','行业标签id','屏蔽广告主标签类型','广告主标签id','屏蔽广告主','广告主id','屏蔽广告主创意品牌标签','创意品牌标签id','广告主_等级','屏蔽终端设备','终端id','操作者','时间']
            if len(res)>0:
                for inf in res:
                    tmpdict={}
                    # if mytype=='1':
                    if 'shieldTactics'in inf[0] :
                        tmpshieldTactics=eval(inf[0])['shieldTactics'][0]
                        if  'type' in (tmpshieldTactics):
                            # 有的value为null 进行eval转换的时候报错，把null替换成空
                            null=''
                            shieldTactics=[]
                            shieldTactics=eval(tmpshieldTactics)[0]
                            shieldTactics['operator']=str(inf[1])
                            shieldTactics['create_time1']=str(inf[2])
                            shieldTactics=self.filldict(shieldTactics)
                            tmp.append(shieldTactics)
            tmp=self.setcolor(tmp)
        if self.mytype=='2':
            tmpsql='''SELECT CASE data_type WHEN 1 THEN '广告主行业'  WHEN 2 THEN '广告主'  WHEN 3 THEN '广告订单' WHEN 4 THEN '广告主前台修改' WHEN 5 THEN '广告主前台新增'
            END 类别,item 变更项,data_id, `before` 变更前, `after` 变更后 , create_time,operator,ip from voyager.core_effect_change_log
        WHERE create_time>'{begintime}' and create_time<'{endtime} 23:59:59' ORDER   by id desc limit 3000;'''.format(begintime=self.begintime,endtime=self.endtime)
            tmp,filed=self.getindb(tmpsql)
        if self.mytype=='3':
            tmpsql='''SELECT  operation_content,operator,create_time from voyager.um_operation_log where create_time>'{begintime}' and create_time<'{endtime} 23:59:59'
             and operation_content LIKE '%{adzoneid}%' and operation_target ='订单基本设置修改' ORDER BY create_time desc;
             '''.format(begintime=self.begintime,endtime=self.endtime,adzoneid=self.adzoneid)
            res,filed=self.getindb(tmpsql)
            filed=['智能增量','初始广告位','操作人','操作时间']
            tmp=[]
            if len(res)>0:
                for inf in res:
                    tmpdict={}
                    if 'ocpaAdzone'  in inf[0]:
                        ocpaAdzone=eval(inf[0])
                        tmpdict['ocpa']='YES'
                        tmpdict['adzone']=ocpaAdzone['ocpaAdzone']
                    else:
                        tmpdict['ocpa']='NO'
                        tmpdict['adzone']=''
                    tmpdict['operator']=inf[1]
                    tmpdict['create_time']=inf[2]
                    tmp.append(tmpdict)
            tmp=self.setcolor(tmp)
        return tmp,filed,tmpsql
    # 如果有key值不存，添加key，value赋值为空
    # 替换value值为中文
    def filldict(self,tmp):
        allkey=['advertiserIdsShow','advertiserIndustryTag','timeEnd','create_time','adzoneId','operator','effectiveTimeType','advertiserIndustryTagType','advertiserIds','type','termIds','advertiserIndustry','advertiserIdsType','advertiserTag','timeType','advertiserTagType','shieldRegion','effectiveTimeBegin','createTime','termType','creativeBrandTagType','advertiserIndustryType','effectiveTimeEnd','regionType','timeBegin','creativeValue','creativeBrandTagIds']
        # 补全所有的key
        for i in allkey:
            if i not in tmp.keys():
                tmp[i]=''
        # 将value值替换成中文
        for k in tmp:
            if k in["timeType","regionType","advertiserIndustryType","advertiserIndustryTagType","advertiserTagType"
                ,"advertiserIdsType","creativeBrandTagType","termType","type","termIds"]:
                tmp[k]=self.checkdict(k,tmp[k])
        return tmp
    # 将value替换成中文
    def checkdict(self,type,vlue1):
        if type in ["timeType","regionType","advertiserIndustryType","advertiserIndustryTagType","advertiserTagType"]:
            if vlue1==0 :
                return '不限'
            if vlue1==1:
                return '限制'
        if type in ["type"]:
            if vlue1==1 :
                return '屏蔽'
            if vlue1==2:
                return '指定'
        if type in ["advertiserIdsType","creativeBrandTagType","termType"]:
            if vlue1==0 :
                return '不屏蔽'
            if vlue1==1:
                return '屏蔽'
        if type in ["termIds"]:
            if vlue1==1 :
                return '安卓'
            if vlue1==2:
                return 'IOS'
    def setcolor(self,tmp):
        diff=[]
        # 第一条数据不用比对
        for i in range(0,len(tmp)-1):
            if i==0:
                diff.append(tmp[0])
            # 当前数据与第二条数据对比如果不同就标红
            newdict={}
            for k in tmp[i]:
                if tmp[i][k] !=tmp[i+1][k]:
                    newdict[k]='<font size="3" color="red">'+str(tmp[i+1][k])+'</font>'
                else:
                    newdict[k]=tmp[i+1][k]
            diff.append(newdict)
                # if tmp[i][k] !=tmp[i+1][k]:

        return diff
if __name__ == '__main__':
    # re=getadzoneinfo('dev',mytype='1',begintime='2020-04-02',endtime='2020-05-01',adzoneid='6469')
    adzon=adzoneinfo(env='test',begintime='2020-11-21',endtime='2020-11-30',adzoneid='32646',mytype='3')
    tmp,filed,tmpsql=adzon.getadzoneinfo()

    # tmplist=[{"A":"123","B":"456"},{"A":"123444","B":"456"},{"A":"123444","B":"45611111"}]
    # re=setcolor(tmplist)
    print tmp

    # strdict='{"key1":null,"key2":"3"}'
    # null=''
    # tmpdict=eval(strdict)
    # print type(tmpdict)
    # print tmpdict

