# -*- coding: utf-8 -*-
__author__ = 'jinyi'
from business_modle.querytool import db
import datetime
from dateutil.relativedelta import relativedelta

class myreport(object):
    def __init__(self,begintime='',endtime='',adzoneids='',advertiser_id='',region=''):
        self.begintime=begintime
        self.endtime=endtime
        self.adzoneids=adzoneids
        self.advertiser_id=advertiser_id
        self.region=region
    # 根据输入的日期返回时间列表
    # ['2020-04-01', '2020-04-02', '2020-04-03', '2020-04-04', '2020-04-05', '2020-04-06']
    def gettimelist(self,):
        bgintime=datetime.datetime.strptime(self.begintime,'%Y-%m-%d')
        endtime=datetime.datetime.strptime(self.endtime,'%Y-%m-%d')
        dates=[]
        while bgintime<=endtime:
            dates.append(bgintime.strftime('%Y-%m-%d')[0:10])
            bgintime=bgintime+relativedelta(days=+1)
        return dates
    # 汇总 菜单名---- 毛利表-分媒体毛利
    def getallreport(self):
        daylist=self.gettimelist()
        tmpsql='''select adzone_id as 广告位ID, max(adzone_name) as 广告位名称, max(settle_type) as 结算方式
     ,(case when  instr(max(adzone_name),"亿起发")>0 then "--" when sum(jf97_consume)>0 then  "R5" else "R1" end) as R级别
     ,sum(jf97_consume)/sum(consume) as 总加粉比例,sum(consume) as 总消耗,sum(cash_consume)-sum(linkage_cash_consume) as 去除联动的现金消耗
    ,sum(platform_profit)-sum(linkage_cash_consume) as 去除联动的平台毛利
     ,(sum(platform_profit)-sum(linkage_cash_consume))/(sum(cash_consume)-sum(linkage_cash_consume)) as 去除联动的毛利率'''
        tmp1=''
        for i in daylist:
            tmp1=tmp1+''', (case date when "{0}" then consume else 0 end) as "消耗{1}" '''.format(i,i)
        # tmpsql=tmpsql+tmp1
        tmp2=''
        for i in daylist:
            tmp2=tmp2+''',(case date when "{0}" then platform_profit-linkage_cash_consume else 0 end) as "去除联动平台毛利{1}" '''.format(i,i)
        tmp3=''
        for i in daylist:
            tmp3=tmp3+''',(case date when "{0}" then adzone_ecpc else 0 end) as "入口点击成本{1}"'''.format(i,i)
            tmp4=''
        for i in daylist:
            tmp4=tmp4+''',(case when date="{0}" and (cash_consume-linkage_cash_consume)>0 then (platform_profit-linkage_cash_consume)/(cash_consume-linkage_cash_consume) else 0 end) as "去除联动毛利率{1}"'''.format(i,i)
        tmpend=''' from tt.tt_adzone_data
    where date between "{0}" and "{1}"
    group by adzone_id;'''.format(self.begintime,self.endtime)
        tmpsql=tmpsql+tmp1+tmp2+tmp3+tmp4+tmpend
        print tmpsql
        res,filed=db.selectsqlnew('devtidb',tmpsql)
        return res,filed,tmpsql
    #广告主联动毛利    菜单名---- 毛利表-联动客户毛利
    def getadvliandong(self):
        tmpsql='''
        select addata.date as 日期
     ,sum(addata.linkage_consume) as 联动总消耗
    ,sum(addata.linkage_cash_consume) as 联动现金消耗
    ,sum(adzonedata.adzone_cost) as 联动成本
    ,sum(addata.linkage_cash_consume)-sum(adzonedata.adzone_cost) as 联动毛利
    ,sum(addata.consume) as 联动广告主总消耗
    ,sum(addata.linkage_consume)/sum(addata.consume) as 联动消耗占比
    ,sum(case addata.advertiser_id when  5209 then addata.linkage_consume  else 0 end) as 5209anyihua联动消耗
    ,sum(case addata.advertiser_id when  5209 then addata.linkage_cash_consume  else 0 end) as 5209anyihua联动现金消耗
    ,sum(case addata.advertiser_id when  5209 then adzonedata.adzone_cost  else 0 end) as 5209anyihua联动成本
    ,sum(case addata.advertiser_id when  5209 then addata.consume  else 0 end) as 5209anyihua总消耗
    ,sum(case addata.advertiser_id when  5209 then addata.linkage_consume  else 0 end)/sum(case addata.advertiser_id when  5209 then addata.consume  else 0 end) as 5209anyihua联动消耗占比
    ,sum(case addata.advertiser_id when  5002 then addata.linkage_consume  else 0 end) as 5002马上消耗金融联动消耗
    ,sum(case addata.advertiser_id when  5002 then addata.linkage_cash_consume  else 0 end) as 5002马上消耗金融联动现金消耗
    ,sum(case addata.advertiser_id when  5002 then adzonedata.adzone_cost  else 0 end) as 5002马上消耗金融联动成本
    ,sum(case addata.advertiser_id when  5002 then addata.consume  else 0 end) as 5002马上消耗金融总消耗
    ,sum(case addata.advertiser_id when  5002 then addata.linkage_consume  else 0 end)/sum(case addata.advertiser_id when  5002 then addata.consume  else 0 end) as 5002马上消耗金融联动消耗占比
    from (    select date ,advertiser_id         ,linkage_consume        ,linkage_cash_consume        ,consume    from tt.tt_advertiser_data    where advertiser_id in (5209,5002)
    and date between "{begin1}" and "{end1}") addata left join (    select a.date,a.advertiser_id,sum(adzone_cost) as adzone_cost from(               select sum(adzone_cost) as adzone_cost
    , date  , (case
    when instr(max(adzone_name), "anyi") > 0 then 5209
    when instr(max(adzone_name), "马上") > 0 then 5002
    else 0
                   end)     as advertiser_id
               from tt.tt_adzone_data               where adzone_name like "%亿起发%"
               and date between "{begin2}" and "{end2}"
               group by date,adzone_name           ) a group by a.date,a.advertiser_id    ) adzonedata on addata.date=adzonedata.date and addata.advertiser_id=adzonedata.advertiser_id;
        '''.format(begin1=self.begintime,end1=self.endtime,begin2=self.begintime,end2=self.endtime)
        print tmpsql
        # re=db.selectsqlnew()
        res,filed=db.selectsqlnew('devtidb',tmpsql)
        return res,filed,tmpsql
    #汇总   菜单名---- 毛利表-平台毛利细化
    def getptmaoli(self):
        tmpsql='''select adzonedata.date as 日期
                ,adzonedata.现金消耗,adzonedata.媒体成本,adzonedata.平台毛利,adzonedata.平台毛利/adzonedata.现金消耗 as 毛利率
                ,adzonedata.R1去联动现金消耗,adzonedata.R1媒体成本,adzonedata.R1去联动毛利,adzonedata.R1去联动毛利/adzonedata.R1去联动现金消耗 as 毛利率
                ,adzonedata.R5去联动现金消耗,adzonedata.R5媒体成本,adzonedata.R5去联动毛利,adzonedata.R5去联动毛利/adzonedata.R5去联动现金消耗 as 毛利率
                ,addata.联动现金消耗,adzonedata.联动媒体成本,addata.联动现金消耗-adzonedata.联动媒体成本 as R5去联动毛利,(addata.联动现金消耗-adzonedata.联动媒体成本)/addata.联动现金消耗 as 毛利率
                ,addata.广点通现金消耗
                from (
                select date
                 ,sum(cash_consume-linkage_cash_consume) as 现金消耗
                 ,sum(adzone_cost) as 媒体成本
                 ,sum(platform_profit) as 平台毛利
                 ,sum(case  when instr(adzone_name,"亿起发")>0 then 0 when jf97_consume>0 then 0 else cash_consume-linkage_cash_consume end) as R1去联动现金消耗
                 ,sum(case  when instr(adzone_name,"亿起发")>0 then 0 when jf97_consume>0 then 0 else adzone_cost end) as R1媒体成本
                 ,sum(case  when instr(adzone_name,"亿起发")>0 then 0 when jf97_consume>0 then 0 else platform_profit-linkage_cash_consume end) as R1去联动毛利
                 ,sum(case  when instr(adzone_name,"亿起发")>0 then 0 when jf97_consume>0 then cash_consume-linkage_cash_consume else 0 end) as R5去联动现金消耗
                 ,sum(case  when instr(adzone_name,"亿起发")>0 then 0 when jf97_consume>0 then adzone_cost else 0 end) as R5媒体成本
                 ,sum(case  when instr(adzone_name,"亿起发")>0 then 0 when jf97_consume>0 then platform_profit-linkage_cash_consume else 0 end) as R5去联动毛利
                 ,sum(case  when instr(adzone_name,"亿起发")>0 then adzone_cost else 0 end) as 联动媒体成本
                from tt.tt_adzone_data
                where date between "{begin1}" and "{end1}"
                group by date
                ) adzonedata left join(    select date        ,sum(case  when instr(advertiser_name,"广点通")>0 then 0 else linkage_cash_consume end) as 联动现金消耗
                ,sum(case  when instr(advertiser_name,"广点通")>0 then cash_consume else 0 end) as 广点通现金消耗
                from tt.tt_advertiser_data    where (advertiser_id in (5209,5002) or advertiser_name like "%广点通%")
                and date between "{begin2}" and "{end2}"    group by date
    ) addata on adzonedata.date=addata.date;'''.format(begin1=self.begintime,end1=self.endtime,begin2=self.begintime,end2=self.endtime)
        print tmpsql
        res,filed=db.selectsqlnew('devtidb',tmpsql)
        return res,filed,tmpsql
#菜单名：媒体效果-评估-日表
# 查询日期，广告位（广告位为可选）
    def getmtpinggu(self):
        daylist=self.gettimelist()
        tmp='''select aa.advertiser_id as 广告主ID
    ,aa.advertiser_name as 广告主名称
    # ,aa.adzone_id as 广告位id
    # ,aa.adzone_name as 广告位名称
    ,tag as 类型
    ,concat(b.effect_typename,"-",b.standard) 考核标准
    ,sum(ad_show) as 曝光
    ,sum(ad_click) as 点击
    ,sum(consume) as 消耗
    ,sum(consume)/sum(ad_click) as CPC'''
        tmp1=''
        for i in daylist:
            tmp1=tmp1+''' ,sum(case date when "{begin1}" then consume else 0 end)/
     sum(case date when "{begin2}" then
        (case  b.standard
            when 1 then t1_num
            when 2 then t2_num
            when 3 then t3_num
            when 4 then t4_num
            when 5 then t5_num
            when 6 then t6_num
            when 7 then t7_num
            when 8 then t8_num
            when 9 then t9_num
            when 10 then t10_num
            when 11 then t11_num
            when 12 then t12_num
            when 13 then t13_num
            when 14 then t14_num
            when 15 then t15_num
            when 16 then t16_num
            else "--"
        end )
        else 0 end) as "效果成本2{begin3}"'''.format(begin1=i,begin2=i,begin3=i)
        tmp2=''
        for i in daylist:
            tmp2=tmp2+''' , sum(case date when "{begin1}" then consume else 0 end)/sum(case date when "{begin2}" then ad_click else 0 end) as "CPC{begin3}"'''.format(begin1=i,begin2=i,begin3=i)
        tmp3=''
        for i in daylist:
            tmp3=tmp3+''' , sum(case date when "{begin1}" then consume else 0 end) as "消耗{begin2}"'''.format(begin1=i,begin2=i)
        tmp4=''' from tt.tt_advertiser_adzone aa
            left join  tt.tt_advertiser_effect_standard b on aa.advertiser_id=b.advertiser_id
		    where date between "{begin}" and "{end}"'''.format(begin=self.begintime,end=self.endtime)
        if self.adzoneids<>'' and self.adzoneids<>'mytest':
            tmp5='''and adzone_id in ({0})'''.format(self.adzoneids)
        else:
            tmp5=''
        tmp6='''group by aa.advertiser_id'''
        tmpsql=tmp+tmp1+tmp2+tmp3+tmp4+tmp5+tmp6
        print tmpsql
        res,filed=db.selectsqlnew('devtidb',tmpsql)
        #
        return res,filed,tmpsql
        # return 1
#菜单名：媒体效果-评估-小时表     #查询维度，日期
    def getmtpinguhour(self):
        tmpsql='''select  azh.advertiser_id as 广告主ID
    ,azh.advertiser_name as 广告主名称
    ,tag as 类型
    ,concat(b.effect_typename,"-",b.standard) 考核标准
    ,sum(ad_show) as 曝光
    ,sum(ad_click) as 点击
    ,sum(consume) as 消耗
    ,sum(consume)/sum(ad_click) as CPC'''
        tmpsql1=''
        tmpsql2=''
        tmpsql3=''
        for i in range(0,24):
            tmpsql1=tmpsql1+''' ,sum(case hour when {0} then consume else 0 end)/
                                sum(case hour when {1} then
                                (case  b.standard
                                when 1 then t1_num
                                when 2 then t2_num
                                when 3 then t3_num
                                when 4 then t4_num
                                when 5 then t5_num
                                when 6 then t6_num
                                when 7 then t7_num
                                when 8 then t8_num
                                when 9 then t9_num
                                when 10 then t10_num
                                when 11 then t11_num
                                when 12 then t12_num
                                when 13 then t13_num
                                when 14 then t14_num
                                when 15 then t15_num
                                when 16 then t16_num
                                else "--"
                            end ) else 0 end) as "效果成本{2}"'''.format(i,i,i)
            tmpsql2=tmpsql2+''' ,sum(case hour when "{0}" then consume else 0 end)/sum(case hour when "{1}" then ad_click else 0 end) as "CPC{2}"'''.format(i,i,i)
            tmpsql3=tmpsql3+''' ,sum(case hour when "{0}" then consume else 0 end) as "消耗{1}"'''.format(i,i)
        tmpsql4='''from tt.tt_advertiser_adzone_hour azh
                left join  tt.tt_advertiser_effect_standard b on azh.advertiser_id=b.advertiser_id
                where date = "{0}" '''.format(self.begintime)
        if self.adzoneids<>'' and self.adzoneids<>'mytest' :
            tmpsql5=''' and adzone_id in ({0})
                    group by azh.advertiser_id'''.format(self.adzoneids)
        else:
            tmpsql5='''group by azh.advertiser_id'''
        tmpsqlall=tmpsql+tmpsql1+tmpsql2+tmpsql3+tmpsql4+tmpsql5
        print tmpsql
        res,filed=db.selectsqlnew('devtidb',tmpsqlall)
        return res,filed,tmpsqlall

#菜单名：地域指标效果数据
# 查询维度:日期，广告位，广告主
    def getregionbyday(self):
        daylist=self.gettimelist()
        tmpsql1='''select aar.advertiser_id as 广告主ID
                ,aar.advertiser_name as 广告主名称
                ,tag as 类型
                ,concat(b.effect_typename,"-",b.standard) 考核标准
                ,region as 省
                ,sum(ad_show) as 曝光
                ,sum(consume)/sum(ad_show)*1000 as CPM
                ,sum(ad_click) as 点击
                ,sum(consume) as 消耗
                ,sum(consume)/sum(ad_click) as CPC
                ,sum(ad_click)/sum(ad_show) as CTR'''
        tmpsql2=''
        for i in daylist:
            tmpsql2=tmpsql2+''' ,sum(case date when "{0}" then consume else 0 end)/
                         sum(case date when "{1}" then
                        (case  b.standard
                        when 1 then t1_num
                        when 2 then t2_num
                        when 3 then t3_num
                        when 4 then t4_num
                        when 5 then t5_num
                        when 6 then t6_num
                        when 7 then t7_num
                        when 8 then t8_num
                        when 9 then t9_num
                        when 10 then t10_num
                        when 11 then t11_num
                        when 12 then t12_num
                        when 13 then t13_num
                        when 14 then t14_num
                        when 15 then t15_num
                        when 16 then t16_num
                        else "--"
                    end )
                    else 0 end) as "效果成本{2}"'''.format(i,i,i)
        tmpsql3=''
        tmpsql4=''
        tmpsql5=''
        for i in daylist:
            tmpsql3=tmpsql3+''' ,sum(case date when "{0}" then consume else 0 end) as "消耗{1}"'''.format(i,i)
            tmpsql4=tmpsql4+''' ,sum(case date when "{0}" then consume else 0 end)/sum(case date when "{1}" then ad_click else 0 end) as "CPC{2}"'''.format(i,i,i)
            tmpsql5=tmpsql5+''' ,sum(case date when "{0}1" then adzone_click else 0 end) as "入口点击{1}"'''.format(i,i)
        tmpsql6=''' from tt_advertiser_adzone_region aar
                    left join  tt.tt_advertiser_effect_standard b on aar.advertiser_id=b.advertiser_id
                    where date between "{0}" and "{1}"'''.format(self.begintime,self.endtime)
        if self.adzoneids<>'' and self.adzoneids<>'mytest':
            tmpsql7=''' and adzone_id in ({0})'''.format(self.adzoneids)
        else:
            tmpsql7=' '
        #     必填
        tmpsql8=''' and aar.advertiser_id ={0} group by aar.advertiser_id,region;'''.format(self.advertiser_id)
        tmpall=tmpsql1+tmpsql2+tmpsql3+tmpsql4+tmpsql5+tmpsql6+tmpsql7+tmpsql8
        print tmpall
        res,filed=db.selectsqlnew('devtidb',tmpall)
        return res,filed,tmpall

#菜单名：广告主地域效果
#查询项：广告位ID，日期  #省（查出来在页面上）
    def getregionbyadv(self):
        daylist=self.gettimelist()
        tmp='''select aar.advertiser_id as 广告主ID
                ,aar.advertiser_name as 广告主名称
                ,tag as 类型
                ,concat(b.effect_typename,"-",b.standard) 考核标准'''
        tmp1=''
        tmp2=''
        tmp3=''
        tmp4=''
        tmp5=''
        for i in daylist:
            tmp1=tmp1+''' ,sum(case date when "{0}" then consume else 0 end)/
                 sum(case date when "{1}" then
                    (case  b.standard
                        when 1 then t1_num
                        when 2 then t2_num
                        when 3 then t3_num
                        when 4 then t4_num
                        when 5 then t5_num
                        when 6 then t6_num
                        when 7 then t7_num
                        when 8 then t8_num
                        when 9 then t9_num
                        when 10 then t10_num
                        when 11 then t11_num
                        when 12 then t12_num
                        when 13 then t13_num
                        when 14 then t14_num
                        when 15 then t15_num
                        when 16 then t16_num
                        else "--"
                    end )
                    else 0 end) as "效果成本{2}" '''.format(i,i,i)
            tmp2=tmp2+''' ,sum(case date when "{0}" then consume else 0 end) as "消耗{1}"'''.format(i,i)
            tmp3=tmp3+'''  ,sum(case date when "{0}" then ad_click else 0 end) as "点击{1}"'''.format(i,i)
            tmp4=tmp4+''' ,sum(case date when "{0}" then consume else 0 end)/sum(case date when "{1}" then ad_click else 0 end) as "CPC{2}"'''.format(i,i,i)
            tmp5=tmp5+''',sum(case date when "{0}" then
                        (case  b.standard
                            when 1 then t1_num
                            when 2 then t2_num
                            when 3 then t3_num
                            when 4 then t4_num
                            when 5 then t5_num
                            when 6 then t6_num
                            when 7 then t7_num
                            when 8 then t8_num
                            when 9 then t9_num
                            when 10 then t10_num
                            when 11 then t11_num
                            when 12 then t12_num
                            when 13 then t13_num
                            when 14 then t14_num
                            when 15 then t15_num
                            when 16 then t16_num
                            else "--"
                        end )
                        else 0 end)
                        /sum(case date when "{1}" then ad_click else 0 end) as "CVR{2}"'''.format(i,i,i)
        tmp6='''from tt_advertiser_adzone_region aar
                left join  tt.tt_advertiser_effect_standard b on aar.advertiser_id=b.advertiser_id
                where date between "{0}" and "{1}"'''.format(self.begintime,self.endtime)
        if self.adzoneids<>'' and self.adzoneids<>'mytest':
            tmp7=''' and adzone_id in ({0})'''.format(self.adzoneids)
        else:
            tmp7=''
        if self.region<>'' and self.region<>'mytest':
            tmp8=''' and region like "%{0}%" '''.format(self.region)
        else:
            tmp8=''
        tmp9=' group by aar.advertiser_id,region;'
        tmpall=tmp+tmp1+tmp2+tmp3+tmp4+tmp5+tmp6+tmp7+tmp8+tmp9
        print tmpall
        res,filed=db.selectsqlnew('devtidb',tmpall)
        return res,filed,tmpall
if __name__ == '__main__':
    # test=myreport(begintime='2020-04-1',endtime='2020-04-02',adzoneids='21')
    test=myreport(begintime='2020-04-1',endtime='2020-04-01',adzoneids='22222',advertiser_id=1,region='北京')
    tmp=test.getregionbyadv()
    print tmp
    # print get_date_list('2018-01-01','2018-02-28')
