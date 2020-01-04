# _*_ coding:utf-8 _*_

__author__ = 'aidinghua'

from utils.db_info import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class Hour_report_adzone(object):




    def __init__(self,begin_date,begin_hour,end_hour,adzone_id,env_value=False):

        self.db=DbOperations(env_value=env_value)
        self.dbstat=DbOperations(env_value='ss')
        self.begin_date=begin_date
        self.begin_date1=str(self.begin_date).replace('-','')
        self.begin_hour=begin_hour
        self.end_hour=end_hour
        self.adzone_id=adzone_id
        # print type(self.begin_date)
        # print type(self.end_hour)
        if self.begin_hour<self.end_hour:
            self.begin_time=self.begin_date+" "+str(self.begin_hour)+":00:00"
            self.end_time=self.begin_date+" "+str(self.end_hour)+":00:00"
        else:
            self.begin_time=self.begin_date+" "+str(self.begin_hour)+":00:00"
            self.end_time=self.begin_date+" "+str(self.end_hour+1)+":00:00"
            self.end_hour=self.begin_hour+1


#校验广告位有效点击量

    def cmp_zone_clicknum(self):




        sql1 = '''SELECT  sum(zone_effect_click_num)  FROM voyagerstat.summary_zone_hour{}  WHERE adzone_id = {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.adzone_id,self.begin_hour,self.end_hour)

        sql2= '''SELECT  COUNT(1) FROM voyagerlog.adzone_click_log{} WHERE adzone_id = {} AND STATUS =1  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.adzone_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:
                return "校验广告位有效点击量字段成功！ "
            else:
                return ("summary_zone_hour表zone_effect_click_num:{},adzone_click_log表:{}\nsummary_zone_hour表sql:{},adzone_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_zone_hour表查询zone_effect_click_num数据为空"

#校验广告位有效点击人数
    # def cmp_zone_clickperson(self):
    #
    #
    #     sql1='''SELECT  SUM(zone_effect_click_person)  FROM voyagerstat.summary_zone_hour{}  WHERE HOUR >={} and HOUR<{} AND adzone_id = {}'''.format(self.begin_date1,self.begin_hour,self.end_hour,self.adzone_id)
    #
    #     sql2='''SELECT  COUNT(DISTINCT(user_cookie)) FROM voyagerlog.adzone_click_log{} WHERE adzone_id = {} AND STATUS =1 and  create_time >='{}' AND create_time<'{}' '''.format(self.begin_date1,self.adzone_id,self.begin_time,self.end_time)
    #
    #     re1=self.dbstat.execute_sql(sql1)[0][0]
    #     print re1
    #     re2=self.db.execute_sql(sql2)[0][0]
    #     print re2
    #     if re1>=0:
    #
    #         if re1==re2:
    #             return "校验广告位有效点击人数字段成功！ "
    #         else:
    #             return ("summary_zone_hour表zone_effect_click_person:{},adzone_click_log表:{}\nsummary_zone_hourr表sql:{},adzone_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))
    #     else:
    #         return "summary_zone_hour表查询zone_effect_click_person数据为空"


##校验广告位无效点击量

    def cmp_zone_invalidnum(self):


        sql1 = '''SELECT  SUM(zone_invalid_click_num)  FROM voyagerstat.summary_zone_hour{}  WHERE adzone_id = {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.adzone_id,self.begin_hour,self.end_hour)

        sql2= '''SELECT  COUNT(1) FROM voyagerlog.adzone_click_log{} WHERE adzone_id = {} AND STATUS =2  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.adzone_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:
                return "校验广告位无效点击量字段成功！ "
            else:
                return ("summary_zone_hour表zone_invalid_click_num:{},adzone_click_log表:{}\nsummary_zone_hour表sql:{},adzone_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_zone_hour表查询zone_invalid_click_num数据为空"






##校验广告(媒体)现金收入
    def cmp_mediacash(self):


        sql1 = '''SELECT sum(media_income_cash) FROM voyagerstat.summary_zone_hour{}  WHERE adzone_id = {}  AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.adzone_id,self.begin_hour,self.end_hour)

        sql2= '''SELECT sum(media_income_cash) FROM voyagerlog.ad_click_log{}  WHERE adzone_id = {} AND STATUS =1  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.adzone_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:
                return "校验广告(媒体)现金收入字段成功！ "
            else:
                return ("summary_zone_hour表media_income_cash:{},ad_click_log表:{}\nsummary_zone_hour表sql:{},ad_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_zone_hour表查询media_income_cash数据为空"



##校验广告(媒体)奖励收入
    def cmp_mediaaward(self):


        sql1 = '''SELECT sum(media_income_award) FROM voyagerstat.summary_zone_hour{}  WHERE adzone_id = {}  AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.adzone_id,self.begin_hour,self.end_hour)

        sql2= '''SELECT sum(media_income_award) FROM voyagerlog.ad_click_log{}  WHERE adzone_id = {} AND STATUS =1  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.adzone_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:
                return "校验广告(媒体)奖励收入字段成功！ "
            else:
                return ("summary_zone_hour表media_income_award:{},ad_click_log表:{}\nsummary_zone_hour表sql:{},ad_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_zone_hour表查询media_income_award数据为空"

##校验广告有效曝光量
    def cmp_adshownum(self):


        sql1 = '''SELECT  SUM(adshow_effect_num)  FROM voyagerstat.summary_zone_hour{}   WHERE adzone_id = {}  AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.adzone_id,self.begin_hour,self.end_hour)

        sql2= '''SELECT  COUNT(1) FROM voyagerlog.ad_show_log{}   WHERE adzone_id = {} AND STATUS =1  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.adzone_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:
                return "校验广告有效曝光量字段成功！ "
            else:
                return ("summary_zone_hour表adshow_effect_num:{},ad_show_log表:{}\nsummary_zone_hour表sql:{},ad_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_zone_hour表查询adshow_effect_num数据为空"


##校验广告有效曝光人数 人数统计暂不做校验

    # def cmp_adshowperson(self):
    #
    #
    #     sql1 = '''SELECT  SUM(adshow_effect_person)  FROM voyagerstat.summary_zone_hour{}   WHERE adzone_id = {}  AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.adzone_id,self.begin_hour,self.end_hour)
    #
    #     sql2= '''SELECT  COUNT(DISTINCT(user_cookie)) FROM voyagerlog.ad_show_log{}   WHERE adzone_id = {} AND STATUS =1  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.adzone_id,self.begin_time,self.end_time)
    #
    #     re1=self.dbstat.execute_sql(sql1)[0][0]
    #     print re1
    #     re2=self.db.execute_sql(sql2)[0][0]
    #     print re2
    #     if re1>=0:
    #
    #         if re1==re2:
    #             return "校验广告有效曝光人数字段成功！ "
    #         else:
    #             return ("summary_zone_hour表adshow_effect_person:{},ad_show_log表:{}\nsummary_zone_hour表sql:{},ad_show_log表sql:{}".format(str(re1),str(re2),sql1,sql2))
    #
    #     else:
    #         return "summary_zone_hour表查询adshow_effect_person数据为空"

##校验广告有效点击量
    def cmp_adclicknum(self):


        sql1 = '''SELECT  SUM(adclick_effect_num)  FROM voyagerstat.summary_zone_hour{}  WHERE adzone_id = {}  AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.adzone_id,self.begin_hour,self.end_hour)

        sql2= '''SELECT COUNT(1) FROM voyagerlog.ad_click_log{}    WHERE adzone_id = {} AND STATUS =1  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.adzone_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:
                return "校验广告有效点击量字段成功！ "
            else:
                return ("summary_zone_hour表adclick_effect_num:{},ad_click_log表:{}\nsummary_zone_hour表sql:{},ad_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_zone_hour表查询adclick_effect_num数据为空"

##校验谢谢参与次数
    def cmp_xiexienum(self):


        sql1 = '''SELECT  SUM(xiexie_num)  FROM voyagerstat.summary_zone_hour{}  WHERE adzone_id = {}  AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.adzone_id,self.begin_hour,self.end_hour)

        sql2= '''select count(1) From voyagerlog.lottery_click_log{}   WHERE adzone_id = {} AND act_award_type =6   AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.adzone_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:
                return "校验谢谢参与次数字段成功！ "
            else:
                return ("summary_zone_hour表xiexie_num:{},lottery_click_log表:{}\nsummary_zone_hour表sql:{},lottery_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_zone_hour表查询xiexie_num数据为空"




if __name__=='__main__':

    Hra=Hour_report_adzone('2019-08-13',8,9,4833,False)
    print Hra.cmp_zone_clicknum()
    # print Hra.cmp_zone_clickperson()
    print Hra.cmp_zone_invalidnum()
    print Hra.cmp_mediacash()
    print Hra.cmp_mediaaward()
    print Hra.cmp_adshownum()
    # print Hra.cmp_adshowperson()
    print Hra.cmp_adclicknum()
    print Hra.cmp_xiexienum()