# -*- coding: utf-8 -*-
__author__ = 'jinyi'
from business_modle.querytool import db
import datetime
from dateutil.relativedelta import relativedelta
from openpyxl import  Workbook,load_workbook
import os

class myreport(object):
    def __init__(self,begintime='',endtime='',adzoneids='',advertiser_id='',region='',showadzone='',tagorad=''):
        self.begintime=begintime
        self.endtime=endtime
        self.adzoneids=adzoneids
        self.advertiser_id=advertiser_id
        self.region=region
        self.showadzone=showadzone
        self.tagorad=tagorad
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
    # 处理fload展示小数据点.0的问题
    def getresfloadtoint(self,res):
        tmpres=[]
        for i in res:
            # print i
            tmplist=list(i)
            for k in range(len(tmplist)):
                if type(tmplist[k])==float:
                    if int(tmplist[k])==tmplist[k]:
                        tmplist[k]=int(tmplist[k])
            tmpres.append(tmplist)
        return tmpres
    # 导出excel
    def exportexcel(self,filed,res,excelname):
        if len(res)<>0:
            res=list(res)
            # res.insert(0,headtr)
            res.insert(0,filed)
            wb=Workbook()
            sheet=wb.active
            for i in range(len(res)):
                sheet.append(res[i])
            try:
                # wb.save("../../../static/result/reportall.xlsx")
                wb.save("./static/result/{0}.xlsx".format(excelname))
            except Exception as e:
                print e.message
        return ''



    # 汇总 菜单名---- 毛利表-分媒体毛利
    def getallreport(self):
        daylist=self.gettimelist()
        tmpsql='''select adzone_id as ID, max(adzone_name) as 广告位, ifnull(max(settle_type),"") as 结算
                    ,ifnull((case when  instr(max(adzone_name),"亿起发")>0 and instr(max(adzone_name),"jinlika")<=0 and instr(max(adzone_name),"省点")<=0 then "--" when sum(jf97_consume)>0 then  "R5" else "R1" end),"") as R级别
                    ,concat(round(ifnull(sum(jf97_consume)/sum(consume),0)*100,0),"%") as 加粉比例
                    ,round(ifnull(sum(consume),0),0) as 总消耗
                    ,round(ifnull(sum(cash_consume)-sum(linkage_cash_consume),0),0) as 去联现金
                    ,round(ifnull(sum(platform_profit)-sum(linkage_cash_consume),0),0) as 去联毛利
                    ,concat(round(ifnull((sum(platform_profit)-sum(linkage_cash_consume))/(sum(cash_consume)-sum(linkage_cash_consume)),0)*100,0),"%") as 去联毛利率'''
        tmp1=''
        colspanx=0
        for i in daylist:  #消耗
            tmp1=tmp1+''', round(ifnull(sum(case date when "{0}" then consume else 0 end),0),0) as "{1}" '''.format(i,i.replace("2020-",""))
            colspanx=colspanx+1
            # tmpsql=tmpsql+tmp1
        tmp2=''
        for i in daylist: #去除联动平台毛利
            tmp2=tmp2+''',round(ifnull(sum(case date when "{0}" then platform_profit-linkage_cash_consume else 0 end),0),0) as "{1}" '''.format(i,i.replace("2020-",""))
        tmp3=''
        for i in daylist: #入口点击成本
            tmp3=tmp3+''',round(ifnull(sum(case date when "{0}" then adzone_ecpc else 0 end),0),2) as "{1}"'''.format(i,i.replace("2020-",""))
        tmp4=''
        for i in daylist: #去除联动毛利率
            tmp4=tmp4+''',concat(round(ifnull(sum(case when date="{0}" and (cash_consume-linkage_cash_consume)>0 then (platform_profit-linkage_cash_consume) / (cash_consume-linkage_cash_consume) else 0 end),0)*100,0),"%") as "{1}"'''.format(i,i.replace("2020-",""))
        tmpend=''' from tt.tt_adzone_data
                where date between "{0}" and "{1}"
                group by adzone_id order by 总消耗 desc;'''.format(self.begintime,self.endtime)
        tmpsql=tmpsql+tmp1+tmp2+tmp3+tmp4+tmpend
        headtr='''<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td>
            <td align="center" colspan={0}>消耗</td><td align="center" colspan={1}>去除联动平台毛利</td><td align="center" colspan={2}>入口点击成本</td><td align="center" colspan={3}>去除联动毛利率</td></tr>'''.format(colspanx,colspanx,colspanx,colspanx)
        # print tmpsql
        res,filed=db.selectsqlnew('devtidb',tmpsql)
        res=self.getresfloadtoint(res)
        self.exportexcel(filed,res,"reportall")

        return res,filed,tmpsql ,headtr



    #广告主联动毛利    菜单名---- 毛利表-联动客户毛利
    def getadvliandong(self):
        tmpsql='''
        select addata.date as 日期
            ,round(ifnull(sum(addata.linkage_consume),0),0) as 联动总消耗
            ,round(ifnull(sum(addata.linkage_cash_consume),0),0) as 联动现金消耗
            ,concat(round(ifnull(sum(addata.linkage_cash_consume),0)/ifnull(sum(addata.linkage_consume),0)*100,0),"%") as 联动现金占比
            ,round(ifnull(sum(adzonedata.adzone_cost),0),0) as 联动成本
            ,round(ifnull(sum(addata.linkage_cash_consume)-sum(adzonedata.adzone_cost),0),0) as 联动毛利
            ,round(ifnull(sum(addata.consume),0),0) as 联动广告主总消耗
            ,concat(round(ifnull(sum(addata.linkage_consume)/sum(addata.consume),0)*100,0),"%") as 联动消耗占比
            ,round(ifnull(sum(case addata.advertiser_id when  5209 then addata.linkage_consume  else 0 end),0),0) as 联动消耗
            ,round(ifnull(sum(case addata.advertiser_id when  5209 then addata.linkage_cash_consume  else 0 end),0),0) as 联动现金消耗
            ,concat(round(ifnull(sum(case addata.advertiser_id when  5209 then addata.linkage_cash_consume  else 0 end),0)/ifnull(sum(case addata.advertiser_id when  5209 then addata.linkage_consume  else 0 end),0)*100,0),"%") as 联动现金比例
            ,round(ifnull(sum(case addata.advertiser_id when  5209 then adzonedata.adzone_cost  else 0 end),0),0) as 联动成本
            ,round(ifnull(sum(case addata.advertiser_id when  5209 then addata.consume  else 0 end),0),0) as 总消耗
            ,concat(round(ifnull(sum(case addata.advertiser_id when  5209 then addata.linkage_consume  else 0 end)/sum(case addata.advertiser_id when  5209 then addata.consume  else 0 end),0)*100,0),"%") as 联动消耗占比
            ,round(ifnull(sum(case addata.advertiser_id when  5209 then e.e  else 0 end),0),0) as 联动效果数
            ,round(ifnull(sum(case addata.advertiser_id when  5209 then addata.linkage_consume  else 0 end),0)/ifnull(sum(case addata.advertiser_id when  5209 then e.e  else 0 end),0),0) as 总消耗_转化成本
            ,round(ifnull(sum(case addata.advertiser_id when  5209 then adzonedata.adzone_cost  else 0 end),0)/ifnull(sum(case addata.advertiser_id when  5209 then e.e  else 0 end),0),0) as 成本_转化成本
            ,round(ifnull(sum(case addata.advertiser_id when  5002 then addata.linkage_consume  else 0 end),0),0) as 联动消耗
            ,round(ifnull(sum(case addata.advertiser_id when  5002 then addata.linkage_cash_consume  else 0 end),0),0) as 联动现金消耗
            ,concat(round(ifnull(sum(case addata.advertiser_id when  5002 then addata.linkage_cash_consume  else 0 end),0)/ifnull(sum(case addata.advertiser_id when  5002 then addata.linkage_consume  else 0 end),0)*100,0),"%") as 联动现金占比
            ,round(ifnull(sum(case addata.advertiser_id when  5002 then adzonedata.adzone_cost  else 0 end),0),0) as 联动成本
            ,round(ifnull(sum(case addata.advertiser_id when  5002 then addata.consume  else 0 end),0),0) as 总消耗
            ,concat(round(ifnull(sum(case addata.advertiser_id when  5002 then addata.linkage_consume  else 0 end)/sum(case addata.advertiser_id when  5002 then addata.consume  else 0 end),0)*100,0),"%") as 联动消耗占比
            ,round(ifnull(sum(case addata.advertiser_id when  5002 then e.e  else 0 end),0),0) as 联动效果数
            ,round(ifnull(sum(case addata.advertiser_id when  5002 then addata.linkage_consume  else 0 end),0)/ifnull(sum(case addata.advertiser_id when  5002 then e.e  else 0 end),0),0) as 总消耗_转化成本
            ,round(ifnull(sum(case addata.advertiser_id when  5002 then adzonedata.adzone_cost  else 0 end),0)/ifnull(sum(case addata.advertiser_id when  5002 then e.e  else 0 end),0),0) as 成本_转化成本
        from (    
            select date ,advertiser_id ,linkage_consume ,linkage_cash_consume,consume from tt.tt_advertiser_data    
            where advertiser_id in (5209,5002) and date between "{begin1}" and "{end1}"
        ) addata left join ( 
            select a.date,a.advertiser_id,sum(adzone_cost) as adzone_cost 
            from( 
                select sum(adzone_cost) as adzone_cost, date  , (case when instr(max(adzone_name), "anyi") > 0 then 5209 when instr(max(adzone_name), "马上") > 0 then 5002  else 0 end)     as advertiser_id
                from tt.tt_adzone_data 
                where adzone_name like "%亿起发%" and date between "{begin2}" and "{end2}"
                group by date,adzone_name 
            ) a group by a.date,a.advertiser_id
        ) adzonedata on addata.date=adzonedata.date and addata.advertiser_id=adzonedata.advertiser_id
         left join (select e.advertiser_id, e.date,
                          sum(ELT(a.effect_type, t1_num, t2_num,t3_num,t4_num,t5_num,t6_num,t7_num,t8_num,t9_num,t10_num,t11_num,t12_num,t13_num,t14_num,t15_num,t16_num)) as e
                   from tt.tt_advertiser_linkage_data e left join tt.tt_advertiser_effect_standard a on e.advertiser_id=a.advertiser_id
                   where e.date  between "{begin3}" and "{end3}"
                group by e.advertiser_id,e.date
            ) e  on e.advertiser_id=addata.advertiser_id and e.date=addata.date
        group by addata.date;
        '''.format(begin1=self.begintime,end1=self.endtime,begin2=self.begintime,end2=self.endtime,begin3=self.begintime,end3=self.endtime)
        print tmpsql
        headtr = '''<tr><td colspan=8>&nbsp;</td>
                    <td align="center" colspan=9>5209anyihua</td>
                    <td align="center" colspan=9>5002马上消费金融</td>
                    </tr>'''
        res,filed=db.selectsqlnew('devtidb',tmpsql)
        res=self.getresfloadtoint(res)
        self.exportexcel(filed,res,"reportadvliandong")

        return res,filed,tmpsql,headtr

    # 汇总   菜单名---- 毛利表-平台毛利细化
    def getptmaoli(self):
        tmpsql = '''select adzonedata.date as 日期
                ,round(ifnull(adzonedata.现金消耗,0),0) as 现金消耗
                ,round(ifnull(adzonedata.媒体成本,0),0) as 媒体成本
                ,round(ifnull(adzonedata.平台毛利,0),0) as 平台毛利
                ,concat(round(ifnull(adzonedata.平台毛利/adzonedata.现金消耗,0)*100,0),"%") as 毛利率
                ,round(ifnull(adzonedata.R1去联动现金消耗,0),0) as R1去联动现金消耗
                ,round(ifnull(adzonedata.R1媒体成本,0),0) as R1媒体成本
                ,round(ifnull(adzonedata.R1去联动毛利,0),0) as R1去联动毛利
                ,concat(round(ifnull(adzonedata.R1去联动毛利/adzonedata.R1去联动现金消耗,0)*100,0),"%") as 毛利率
                ,round(ifnull(adzonedata.R5去联动现金消耗,0),0) as R5去联动现金消耗
                ,round(ifnull(adzonedata.R5媒体成本,0),0) as R5媒体成本
                ,round(ifnull(adzonedata.R5去联动毛利,0),0) as R5去联动毛利
                ,concat(round(ifnull(adzonedata.R5去联动毛利/adzonedata.R5去联动现金消耗,0)*100,0),"%") as 毛利率
                ,round(ifnull(addata.联动现金消耗,0),0) as 联动现金消耗
                ,round(ifnull(adzonedata.联动媒体成本,0),0) as 联动媒体成本
                ,round(ifnull(addata.联动现金消耗-adzonedata.联动媒体成本,0),0) as 联动毛利
                ,concat(round(ifnull((addata.联动现金消耗-adzonedata.联动媒体成本)/addata.联动现金消耗,0)*100,0),"%") as 毛利率
                ,round(ifnull(addata.广点通现金消耗,0),0) as 广点通现金消耗
                from (
                    select date
                     ,sum(cash_consume) as 现金消耗
                     ,sum(adzone_cost) as 媒体成本
                     ,sum(platform_profit) as 平台毛利
                     ,sum(case  when instr(adzone_name,"亿起发")>0 and instr(adzone_name,"jinlika")<=0 and instr(adzone_name,"省点")<=0 and instr(adzone_name,"优惠现报")<=0 then 0 when jf97_consume>0 then 0 else ifnull(cash_consume,0)-ifnull(linkage_cash_consume,0) end) as R1去联动现金消耗
                     ,sum(case  when instr(adzone_name,"亿起发")>0 and instr(adzone_name,"jinlika")<=0 and instr(adzone_name,"省点")<=0 and instr(adzone_name,"优惠现报")<=0 then 0 when jf97_consume>0 then 0 else ifnull(adzone_cost,0) end) as R1媒体成本
                     ,sum(case  when instr(adzone_name,"亿起发")>0 and instr(adzone_name,"jinlika")<=0 and instr(adzone_name,"省点")<=0 and instr(adzone_name,"优惠现报")<=0 then 0 when jf97_consume>0 then 0 else ifnull(platform_profit,0)-ifnull(linkage_cash_consume,0) end) as R1去联动毛利
                     ,sum(case  when instr(adzone_name,"亿起发")>0 and instr(adzone_name,"jinlika")<=0 and instr(adzone_name,"省点")<=0 and instr(adzone_name,"优惠现报")<=0 then 0 when jf97_consume>0 then ifnull(cash_consume,0)-ifnull(linkage_cash_consume,0) else 0 end) as R5去联动现金消耗
                     ,sum(case  when instr(adzone_name,"亿起发")>0 and instr(adzone_name,"jinlika")<=0 and instr(adzone_name,"省点")<=0 and instr(adzone_name,"优惠现报")<=0 then 0 when jf97_consume>0 then ifnull(adzone_cost,0) else 0 end) as R5媒体成本
                     ,sum(case  when instr(adzone_name,"亿起发")>0 and instr(adzone_name,"jinlika")<=0 and instr(adzone_name,"省点")<=0 and instr(adzone_name,"优惠现报")<=0 then 0 when jf97_consume>0 then ifnull(platform_profit,0)-ifnull(linkage_cash_consume,0) else 0 end) as R5去联动毛利
                     ,sum(case  when instr(adzone_name,"亿起发")>0 and instr(adzone_name,"jinlika")<=0 and instr(adzone_name,"省点")<=0 and instr(adzone_name,"优惠现报")<=0 then ifnull(adzone_cost,0) else 0 end) as 联动媒体成本
                    from tt.tt_adzone_data a
                    where date between "{begin1}" and "{end1}"
                    group by date
                ) adzonedata left join(    
                    select date        
                    ,sum(case  when instr(advertiser_name,"广点通")>0 then 0 else linkage_cash_consume end) as 联动现金消耗
                    ,sum(case  when instr(advertiser_name,"广点通")>0 then cash_consume else 0 end) as 广点通现金消耗
                    from tt.tt_advertiser_data    where 1=1 
                    and date between "{begin2}" and "{end2}"    group by date
                ) addata on adzonedata.date=addata.date;'''.format(begin1=self.begintime, end1=self.endtime, begin2=self.begintime,
                                                       end2=self.endtime)
        print tmpsql
        res, filed = db.selectsqlnew('devtidb', tmpsql)
        res = self.getresfloadtoint(res)
        self.exportexcel(filed,res,"reportptmaoli")

        tmpsqlsum = tmpsql.replace("group by date","").replace("select date","select 1 as date ").replace("select adzonedata.date","select '汇总' ")
        ressum, filedsum = db.selectsqlnew('devtidb', tmpsqlsum)
        ressum = self.getresfloadtoint(ressum)


        return res, filed, tmpsql ,ressum

        # 菜单名：毛利细化-广告主维度
        # 查询日期，广告位（广告位为可选）
    def getreportptmaoliadtag(self):
        daylist = self.gettimelist()

        tmpad = ''
        tmpadz = ''
        if self.advertiser_id <> '' and self.advertiser_id <> 'mytest':
            tmpad = ''' and aa.advertiser_id in ({0}) '''.format(self.advertiser_id)
        else:
            tmpad = ' '

        if self.adzoneids <> '' and self.adzoneids <> 'mytest':
            tmpadz = ''' and aa.adzone_id in ({0}) '''.format(self.adzoneids)
        else:
            tmpadz = ''

        tmpshowadzone =''
        tmpshowadzone1 =''
        tmpshowadzonesum =''
        if self.showadzone == '1':
            tmpshowadzone = ''' ,aa.adzone_id as  广告位ID,aa.adzone_name as 广告位名称 '''
            tmpshowadzone1 = ''' ,aa.adzone_id '''
            tmpshowadzonesum = ''' ,"--" as  广告位ID,"--" as 广告位名称 '''
        else:
            tmpshowadzone = ''
            tmpshowadzone1 = ''
            tmpshowadzonesum =''

        tmptagorad=''
        tmptagorad1=''
        tmptagoradsum = ''
        if self.tagorad == 'tag':
            tmptagorad = ''' ifnull(tag, "")    as 类型 '''
            tmptagorad1 = ''' aa.tag '''
            tmptagoradsum = ''' "--" '''
        elif self.tagorad =='ad':
            tmptagorad = '''  ifnull(tag, "")    as 类型 ,aa.advertiser_id  as 广告主ID, aa.advertiser_name  as 广告主名称 '''
            tmptagorad1 = ''' aa.advertiser_id '''
            tmptagoradsum = ''' "--","--","--" '''
        else:
            tmptagorad = ''
            tmptagorad1 = ''



        colspanx = 0
        tmp1 = ''
        for i in daylist:  # 转化成本
            colspanx = colspanx + 1
            tmp1 = tmp1 + ''' , round(ifnull(sum(case aa.date when "{begin1}" then aa.cash_consume-aa.linkage_cash_consume-ifnull(b.singleshowvalue,0)*ifnull(aa.ad_show,0) else 0 end), 0), 0) as "{begin2}" '''.format(begin1=i, begin2=i.replace("2020-", ""))

        tmp = '''select  {tmptagorad}  {tmpshowadzone} 
                 , round(ifnull(sum(aa.ad_show), 0), 0)                                                               as 曝光
                 , round(ifnull(sum(aa.ad_click), 0), 0)                                                              as 点击
                 , round(ifnull(sum(aa.consume) - sum(aa.linkage_consume), 0), 0)                                        as 消耗
                 , round(ifnull(sum(aa.cash_consume-aa.linkage_cash_consume),0)-sum(ifnull(b.singleshowvalue,0)*ifnull(aa.ad_show,0)),0) as 总盈亏
                 , round(ifnull((sum(aa.consume) - sum(aa.linkage_consume)) / sum(aa.ad_click), 0), 2)       as CPC
                 ''' + tmp1 + '''
            from tt.tt_advertiser_adzone aa
                     left join (select adzone_id,date,adzone_cost/ad_show as singleshowvalue,ad_show from tt.tt_adzone_data where adzone_name not like "%亿起发%" or (adzone_name  like "%亿起发%" and adzone_name not like "%anyi%" and adzone_name not like "%马上%")) b on aa.adzone_id = b.adzone_id and aa.date=b.date
            where aa.date between "{begin}" and "{end}" '''.format(begin=self.begintime, end=self.endtime) + tmpad + tmpadz + '''
            group by   {tmptagorad1}  {tmpshowadzone1} '''

        tmpsql = tmp.format( tmptagorad=tmptagorad, tmpshowadzone=tmpshowadzone, tmptagorad1=tmptagorad1, tmpshowadzone1=tmpshowadzone1)

        res, filed = db.selectsqlnew('devtidb', tmpsql)
        res = self.getresfloadtoint(res)
        self.exportexcel(filed,res,"reportptmaoliadtag")

        tmpsqlsum = tmp.format(tmptagorad=tmptagoradsum, tmpshowadzone=tmpshowadzonesum, tmptagorad1='', tmpshowadzone1='').replace("group by","")
        ressum, filedsum = db.selectsqlnew('devtidb', tmpsqlsum)
        ressum = self.getresfloadtoint(ressum)

        return res, filed, tmpsql, colspanx,ressum


    #菜单名：媒体效果-评估-日表   曝光点击无联动值；消耗包含联动
    # 查询日期，广告位（广告位为可选）
    def getmtpinggu(self):
        daylist=self.gettimelist()

        tmpt01=''
        tmpt02=''
        tmpt03=''
        tmpt01sum=''
        if self.advertiser_id<>'' and self.advertiser_id<>'mytest':
            tmpt01=''' aa.advertiser_id as 广告主ID ,aa.advertiser_name as 广告主名称,aa.adzone_id as 广告位ID ,concat(aa.adzone_name,"&nbsp;-&nbsp;",tad.settle_type)  as 广告位名称 '''
            tmpt01sum = ''' "","","","汇总" '''
            tmpt02=''' and aa.advertiser_id in ({0}) '''.format(self.advertiser_id)
            tmpt03=''' ,aa.adzone_id '''
        else:
            tmpt01=''' aa.advertiser_id as 广告主ID ,aa.advertiser_name as 广告主名称 '''
            tmpt01sum=''' "","汇总" '''

        tmpsql000=''' ,ifnull(b.effect_typename,"") as 考核 ,ifnull(b.standard,"") as 要求 ,ifnull(tag,"") as 类型 '''
        tmp='''select '''+tmpt01+tmpsql000+'''
            ,round(ifnull(sum(ad_show),0),0) as 曝光
            ,round(ifnull(sum(ad_click),0),0) as 点击
            ,round(ifnull(sum(consume)-sum(linkage_consume),0),0) as 消耗
            ,round(ifnull((sum(consume)-sum(linkage_consume))/sum(ad_show)*1000,0),0) as CPM
            ,round(ifnull((sum(consume)-sum(linkage_consume))/sum(ad_click),0),2) as CPC
            ,ifnull(sum(ELT(b.effect_type, t1_num, t2_num,t3_num,t4_num,t5_num,t6_num,t7_num,t8_num,t9_num,t10_num,t11_num,t12_num,t13_num,t14_num,t15_num,t16_num)),0) as 效果数
            ,concat(round(ifnull(sum(ELT(b.effect_type, t1_num, t2_num,t3_num,t4_num,t5_num,t6_num,t7_num,t8_num,t9_num,t10_num,t11_num,t12_num,t13_num,t14_num,t15_num,t16_num))/sum(ad_click),0)*100,0),"%") as 转化率
            ,round(ifnull((sum(consume)-sum(linkage_consume))/sum(ELT(b.effect_type, t1_num, t2_num,t3_num,t4_num,t5_num,t6_num,t7_num,t8_num,t9_num,t10_num,t11_num,t12_num,t13_num,t14_num,t15_num,t16_num)),0),2) as 转化成本
            '''
        tmp1=''
        colspanx = 0
        for i in daylist: #转化成本
            colspanx=colspanx+1
            tmp1=tmp1+''' ,round(ifnull(sum(case date when "{begin1}" then consume-linkage_consume else 0 end)/
     sum(case date
            when "{begin2}" then ELT(b.effect_type, t1_num, t2_num,t3_num,t4_num,t5_num,t6_num,t7_num,t8_num,t9_num,t10_num,t11_num,t12_num,t13_num,t14_num,t15_num,t16_num)
        else 0 end),0),2) as "{begin3}"'''.format(begin1=i,begin2=i,begin3=i.replace("2020-",""))
        tmp2=''
        for i in daylist:   #CPC
            tmp2=tmp2+''' , round(ifnull(sum(case date when "{begin1}" then consume-linkage_consume else 0 end)/sum(case date when "{begin2}" then ad_click else 0 end),0),2) as "{begin3}"'''.format(begin1=i,begin2=i,begin3=i.replace("2020-",""))
        tmp3=''
        for i in daylist:  #消耗
            tmp3=tmp3+''' , round(ifnull(sum(case date when "{begin1}" then consume-linkage_consume else 0 end),0),0) as "{begin2}"'''.format(begin1=i,begin2=i.replace("2020-",""))
        tmpcvr = ''
        for i in daylist:  #转化率
            tmpcvr=tmpcvr+''' , concat(round(ifnull(sum(case date when "{begin1}" then ELT(b.effect_type, t1_num, t2_num,t3_num,t4_num,t5_num,t6_num,t7_num,t8_num,t9_num,t10_num,t11_num,t12_num,t13_num,t14_num,t15_num,t16_num) else 0 end)/sum(case date when "{begin2}" then ad_click else 0 end),0)*100,0),"%") as "{begin3}"'''.format(begin1=i,begin2=i,begin3=i.replace("2020-",""))
        tmp4=''' from tt.tt_advertiser_adzone aa
            left join  tt.tt_advertiser_effect_standard b on aa.advertiser_id=b.advertiser_id  left join (select (case lower(settle_type) when "cps" then "cps" else "媒购" end) as settle_type ,adzone_id from tt.tt_adzone_data group by adzone_id) tad on aa.adzone_id=tad.adzone_id 
            where date between "{begin}" and "{end}"'''.format(begin=self.begintime,end=self.endtime)
        if self.adzoneids<>'' and self.adzoneids<>'mytest':
            tmp5=''' and aa.adzone_id in ({0}) '''.format(self.adzoneids)
        else:
            tmp5=''
        tmp6='''group by aa.advertiser_id'''+tmpt03
        tmpsql=tmp+tmp1+tmp2+tmp3+tmpcvr+tmp4+tmp5+tmpt02+tmp6
        print tmpsql
        res,filed=db.selectsqlnew('devtidb',tmpsql)
        res = self.getresfloadtoint(res)
        self.exportexcel(filed,res,"reportmtpinggu")


        ressum=""
        tmpsqlsum = tmpsql.replace(tmpt01,tmpt01sum).replace(tmpsql000,' ,"","","" ').replace(tmp6,"")
        ressum, filedsum = db.selectsqlnew('devtidb', tmpsqlsum)
        ressum = self.getresfloadtoint(ressum)

        return res,filed,tmpsql,colspanx,ressum
        # return 1


    #菜单名：媒体效果-评估-小时表     #查询维度，日期
    def getmtpinguhour(self):

        tmpt01=''
        tmpt01sum=''
        tmpt02=''
        tmpt03=''
        tmpt04=''
        tmpt05=''
        if self.advertiser_id<>'' and self.advertiser_id<>'mytest':
            tmpt01=''' azh.advertiser_id as 广告主ID ,azh.advertiser_name as 广告主名称,azh.adzone_id as 广告位ID ,concat(azh.adzone_name,"&nbsp;-&nbsp;",adz.settle_type) as 广告位名称 '''
            tmpt01sum = ''' "","","","汇总" '''
            tmpt02=''' and azh.advertiser_id in ({0}) '''.format(self.advertiser_id)
            tmpt03=''' ,azh.adzone_id '''
            tmpt04=''' left join (select adzone_id,sum(ifnull(platform_profit,0)) as platform_profit, (case lower(settle_type) when "cps" then "cps" else "媒购" end) as settle_type  from tt.tt_adzone_data where date between date_format(date_add(now() ,interval -7 day),'%Y-%m-%d') and  date_format(now(),'%Y-%m-%d') and adzone_cost>0 group by adzone_id) adz on adz.adzone_id=azh.adzone_id '''
            tmpt05=''' ,sum(ifnull(adz.platform_profit,0)) as platform_profit '''
        else:
            tmpt01=''' azh.advertiser_id as 广告主ID ,azh.advertiser_name as 广告主名称 '''
            tmpt01sum = ''' "","汇总" '''
            tmpt05 = ''' ,999 as platform_profit '''

        tmpsql000='''  ,ifnull(b.effect_typename,"") as 考核 ,ifnull(b.standard,"") as 要求 ,round(ifnull((sum(consume)-sum(linkage_consume))/sum(ELT(b.effect_type, t1_num, t2_num,t3_num,t4_num,t5_num,t6_num,t7_num,t8_num,t9_num,t10_num,t11_num,t12_num,t13_num,t14_num,t15_num,t16_num)),0),2) as 总成本,ifnull(tag,"") as 类型 '''
        tmpsql000sum='''  ,"","" ,round(ifnull((sum(consume)-sum(linkage_consume))/sum(ELT(b.effect_type, t1_num, t2_num,t3_num,t4_num,t5_num,t6_num,t7_num,t8_num,t9_num,t10_num,t11_num,t12_num,t13_num,t14_num,t15_num,t16_num)),0),2) as 总成本,"" '''

        tmpsql='''select  '''+ tmpt01 + tmpsql000 +'''
                ,round(ifnull(sum(ad_show),0),0) as 曝光
                ,round(ifnull(sum(ad_click),0),0) as 点击
                ,round(ifnull(sum(consume)-sum(linkage_consume),0),0) as 消耗
                ,round(ifnull((sum(consume)-sum(linkage_consume))/sum(ad_click),0),2) as CPC
                ,ifnull(sum(ELT(b.effect_type, t1_num, t2_num,t3_num,t4_num,t5_num,t6_num,t7_num,t8_num,t9_num,t10_num,t11_num,t12_num,t13_num,t14_num,t15_num,t16_num)),0) as 效果数
            ,concat(round(ifnull(sum(ELT(b.effect_type, t1_num, t2_num,t3_num,t4_num,t5_num,t6_num,t7_num,t8_num,t9_num,t10_num,t11_num,t12_num,t13_num,t14_num,t15_num,t16_num))/sum(ad_click),0)*100,0),"%") as 转化率
            '''
        tmpsql1=''
        tmpsql2=''
        tmpsql3=''
        tmpsql6=''
        tmpcvr=''
        for i in range(0,24):
            tmpsql1=tmpsql1+''' ,round(ifnull(sum(case hour when {0} then consume-linkage_consume else 0 end)/
                                sum(case hour when {1} then
                                ELT(b.effect_type, t1_num, t2_num,t3_num,t4_num,t5_num,t6_num,t7_num,t8_num,t9_num,t10_num,t11_num,t12_num,t13_num,t14_num,t15_num,t16_num) 
                                else 0 end),0),2) as "{2}"'''.format(i,i,i)  #效果成本
            tmpsql2=tmpsql2+''' ,round(ifnull(sum(case hour when "{0}" then consume-linkage_consume else 0 end)/sum(case hour when "{1}" then ad_click else 0 end),0),2) as "{2}" '''.format(i,i,i)  #CPC
            tmpsql3=tmpsql3+''' ,round(ifnull(sum(case hour when "{0}" then consume-linkage_consume else 0 end),0),0) as "{1}" '''.format(i,i)  #消耗
            #转化率
            tmpcvr=tmpcvr+''' , concat(round(ifnull(sum(case date when "{0}" then ELT(b.effect_type, t1_num, t2_num,t3_num,t4_num,t5_num,t6_num,t7_num,t8_num,t9_num,t10_num,t11_num,t12_num,t13_num,t14_num,t15_num,t16_num) else 0 end)/sum(case date when "{1}" then ad_click else 0 end),0)*100,0),"%") as "{2}"'''.format(i,i,i)
        tmpsql4=''' from tt.tt_advertiser_adzone_hour azh
                left join  tt.tt_advertiser_effect_standard b on azh.advertiser_id=b.advertiser_id {0}  
                where ifnull(azh.consume,0)-ifnull(azh.linkage_consume,0) >0 and azh.date = "{1}" '''.format(tmpt04,self.begintime)
        if self.adzoneids<>'' and self.adzoneids<>'mytest' :
            tmpsql5=''' and azh.adzone_id in ({0}) '''.format(self.adzoneids)
        else:
            tmpsql5=' '
        tmpsql6 = ''' group by azh.advertiser_id '''+tmpt03
        tmpsqlall=tmpsql+tmpsql1+tmpsql2+tmpsql3+tmpcvr+tmpt05+tmpsql4+tmpsql5+tmpt02+tmpsql6

        res,filed=db.selectsqlnew('devtidb',tmpsqlall)
        res = self.getresfloadtoint(res)
        self.exportexcel(filed,res,"reportmtpingguhour")

        ressum=""
        tmpsqlsum = tmpsqlall.replace(tmpt01,tmpt01sum).replace(tmpsql000,tmpsql000sum).replace(tmpsql6,"").replace(tmpt04,"").replace(tmpt05,",999")
        ressum, filedsum = db.selectsqlnew('devtidb', tmpsqlsum)
        ressum = self.getresfloadtoint(ressum)

        return res,filed,tmpsqlall,ressum

    # 菜单名：媒体效果-评估-广告主类型
    def getreportByadvtag(self):
        daylist = self.gettimelist()

        if self.adzoneids <> '' and self.adzoneids <> 'mytest':
            tmpadzone = ''' and adzone_id in ({0}) '''.format(self.adzoneids)
        else:
            tmpadzone = ''


        tmpsql = '''select
                          aa.adzone_name as 广告位名称,aa.date as 日期,ifnull(tag, "")           as 类型
                         , round(ifnull(sum(ad_show), 0), 0)       as 曝光
                         , round(ifnull(sum(ad_click), 0), 0)      as 点击
                         , concat(round(ifnull(sum(ad_click)/sum(ad_show), 0)*100, 0),"%")      as CTR
                         , round(ifnull(sum(consume) - sum(linkage_consume), 0), 0)    as 消耗
                         , round(ifnull((sum(consume) - sum(linkage_consume)) / sum(ad_click), 0), 2)      as CPC
                         , ifnull(sum(ELT(b.effect_type, t1_num, t2_num, t3_num, t4_num, t5_num, t6_num, t7_num, t8_num, t9_num, t10_num,
                                          t11_num, t12_num, t13_num, t14_num, t15_num, t16_num)), 0)     as 效果数
                         , concat(round(ifnull(sum(ELT(b.effect_type, t1_num, t2_num, t3_num, t4_num, t5_num, t6_num, t7_num, t8_num,
                                                       t9_num, t10_num, t11_num, t12_num, t13_num, t14_num, t15_num, t16_num)) /
                                               sum(ad_click), 0) * 100, 0), "%")       as 转化率
                         , round(ifnull((sum(consume) - sum(linkage_consume)) / sum(
                            ELT(b.effect_type, t1_num, t2_num, t3_num, t4_num, t5_num, t6_num, t7_num, t8_num, t9_num, t10_num, t11_num,
                                t12_num, t13_num, t14_num, t15_num, t16_num)), 0), 2)      as 转化成本
                    from tt.tt_advertiser_adzone aa
                             left join tt.tt_advertiser_effect_standard b on aa.advertiser_id = b.advertiser_id
                    where date between "{begin}" and "{end}"
                         {adzone}
                    group by aa.tag,aa.date,aa.adzone_name
            '''.format(begin=self.begintime, end=self.endtime,adzone=tmpadzone)


        res, filed = db.selectsqlnew('devtidb', tmpsql)
        res = self.getresfloadtoint(res)
        self.exportexcel(filed, res, "reportByadvtag")

        return res, filed, tmpsql


    #菜单名：地域指标效果数据
    # 查询维度:日期，广告位，广告主
    def getregionbyday(self):
        daylist=self.gettimelist()
        tmpsql1='''select aar.advertiser_id as 广告主ID
                ,ifnull(aar.advertiser_name,"") as 广告主名称
                ,ifnull(b.effect_typename,"") as 考核
                ,ifnull(b.standard,"") as 要求
                ,ifnull(tag,"") as 类型
                ,ifnull(region,"") as 省
                ,round(ifnull(sum(ad_show),0),0) as 曝光
                ,round(ifnull((sum(consume)-sum(linkage_consume))/sum(ad_show)*1000,0),0) as CPM
                ,round(ifnull(sum(ad_click),0),0) as 点击
                ,round(ifnull(sum(consume)-sum(linkage_consume),0),0) as 消耗
                ,round(ifnull((sum(consume)-sum(linkage_consume))/sum(ad_click),0),2) as CPC
                ,concat(round(ifnull(sum(ad_click)/sum(ad_show),0)*100,0),"%") as CTR'''
        tmpsql2=''
        tmpsql3=''
        tmpsql4=''
        tmpsql5=''
        colspanx=0
        for i in daylist:
            colspanx=colspanx+1
            tmpsql2=tmpsql2+''' ,round(ifnull(sum(case date when "{0}" then consume-linkage_consume else 0 end)/
                         sum(case date when "{1}" then
                        ELT(b.effect_type, t1_num, t2_num,t3_num,t4_num,t5_num,t6_num,t7_num,t8_num,t9_num,t10_num,t11_num,t12_num,t13_num,t14_num,t15_num,t16_num)
                    else 0 end),0),2) as "{2}"'''.format(i,i,i.replace("2020-","")) #效果成本
            tmpsql3=tmpsql3+''' ,round(ifnull(sum(case date when "{0}" then consume-linkage_consume else 0 end),0),0) as "{1}"'''.format(i,i.replace("2020-","")) #消耗
            tmpsql4=tmpsql4+''' ,round(ifnull(sum(case date when "{0}" then consume-linkage_consume else 0 end)/sum(case date when "{1}" then ad_click else 0 end),0),2) as "{2}"'''.format(i,i,i.replace("2020-","")) #CPC
            tmpsql5=tmpsql5+''' ,round(ifnull(sum(case date when "{0}1" then adzone_click else 0 end),0),0) as "{1}"'''.format(i,i.replace("2020-","")) #入口点击
        tmpsql6=''' from tt_advertiser_adzone_region aar
                    left join  tt.tt_advertiser_effect_standard b on aar.advertiser_id=b.advertiser_id
                    where date between "{0}" and "{1}"'''.format(self.begintime,self.endtime)
        if self.adzoneids<>'' and self.adzoneids<>'mytest':
            tmpsql7=''' and adzone_id in ({0})'''.format(self.adzoneids)
        else:
            tmpsql7=' '
        #     必填
        tmpsql8=''' and aar.advertiser_id in ({0}) group by aar.advertiser_id,region;'''.format(self.advertiser_id)
        tmpall=tmpsql1+tmpsql2+tmpsql3+tmpsql4+tmpsql5+tmpsql6+tmpsql7+tmpsql8
        print tmpall
        res,filed=db.selectsqlnew('devtidb',tmpall)
        res = self.getresfloadtoint(res)
        self.exportexcel(filed,res,"reportregionbyday")
        return res,filed,tmpall,colspanx

#菜单名：广告主地域效果
#查询项：广告位ID，日期  #省（查出来在页面上）
    def getregionbyadv(self):
        daylist=self.gettimelist()
        tmp='''select aar.advertiser_id as 广告主ID
                ,ifnull(aar.advertiser_name,"") as 广告主名称
                ,ifnull(b.effect_typename,"") as 考核
                ,ifnull(b.standard,"") as 要求
                ,ifnull(tag,"") as 类型
                ,round(ifnull(sum(consume)-sum(linkage_consume),0),0) as 消耗
                ,round(ifnull((sum(consume)-sum(linkage_consume))/sum(ad_show)*1000,0),0) as CPM
                ,round(ifnull(sum(ad_click),0),0) as 点击
                ,round(ifnull((sum(consume)-sum(linkage_consume))/sum(ad_click),0),2) as CPC
                ,concat(round(ifnull(sum(
                        ELT(b.effect_type, t1_num, t2_num,t3_num,t4_num,t5_num,t6_num,t7_num,t8_num,t9_num,t10_num,t11_num,t12_num,t13_num,t14_num,t15_num,t16_num))
                        /sum( ad_click ),0)*100,0),"%") as CVR
                ,ifnull(region,"") as 省'''
        tmp1=''
        tmp2=''
        tmp3=''
        tmp4=''
        tmp5=''
        colspanx=0
        for i in daylist:
            colspanx=colspanx+1
            tmp1=tmp1+''' ,round(ifnull(sum(case date when "{0}" then consume-linkage_consume else 0 end)/
                 sum(case date when "{1}" then
                    ELT(b.effect_type, t1_num, t2_num,t3_num,t4_num,t5_num,t6_num,t7_num,t8_num,t9_num,t10_num,t11_num,t12_num,t13_num,t14_num,t15_num,t16_num)
                    else 0 end),0),2) as "{2}" '''.format(i,i,i.replace("2020-","")) #效果成本
            tmp2=tmp2+''' ,round(ifnull(sum(case date when "{0}" then consume-linkage_consume else 0 end),0),0) as "{1}"'''.format(i,i.replace("2020-","")) #消耗
            tmp3=tmp3+'''  ,round(ifnull(sum(case date when "{0}" then ad_click else 0 end),0),0) as "{1}"'''.format(i,i.replace("2020-","")) #点击
            tmp4=tmp4+''' ,round(ifnull(sum(case date when "{0}" then consume-linkage_consume else 0 end)/sum(case date when "{1}" then ad_click else 0 end),0),2) as "{2}"'''.format(i,i,i.replace("2020-","")) #CPC
            tmp5=tmp5+''',concat(round(ifnull(sum(case date when "{0}" then
                        ELT(b.effect_type, t1_num, t2_num,t3_num,t4_num,t5_num,t6_num,t7_num,t8_num,t9_num,t10_num,t11_num,t12_num,t13_num,t14_num,t15_num,t16_num)
                        else 0 end)
                        /sum(case date when "{1}" then ad_click else 0 end),0)*100,0),"%") as "{2}"'''.format(i,i,i.replace("2020-","")) #CVR
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
        res = self.getresfloadtoint(res)
        self.exportexcel(filed,res,"reportregionbyadv")
        return res,filed,tmpall,colspanx


if __name__ == '__main__':
    # test=myreport(begintime='2020-04-1',endtime='2020-04-02',adzoneids='21')
    test=myreport(begintime='2020-04-01',endtime='2020-04-11',adzoneids='22222',advertiser_id=1,region='北京')
    tmp=test.getallreport()
    # print tmp
    # print get_date_list('2018-01-01','2018-02-28')
    # cwd = os.getcwd()
    # print(cwd)
    # wb=Workbook()
    # sheet=wb.active
    # wb1=load_workbook('reportall.xlsx')
    # w=wb1["Sheet"]
    # sheet.merge_cells('J1:L1')
    # sheet['J1']='消费消费'



