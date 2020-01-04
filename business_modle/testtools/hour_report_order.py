# _*_ coding:utf-8 _*_

__author__ = 'aidinghua'

from utils.db_info import *
import sys
from datetime import datetime,timedelta

reload(sys)
sys.setdefaultencoding('utf-8')



class Hour_report_order(object):




    def __init__(self,begin_date,begin_hour,end_hour,order_id,env_value=False):

        self.db=DbOperations(env_value=env_value)
        self.dbstat=DbOperations(env_value='ss')
        self.begin_date=begin_date
        self.begin_date1=str(self.begin_date).replace('-','')
        self.begin_hour=begin_hour
        self.end_hour=end_hour
        self.order_id=order_id
        self.mon=datetime.now().strftime("%m")

        print self.mon
        print type(self.mon)
        # print type(self.begin_date)
        # print type(self.end_hour)
        if self.begin_hour<self.end_hour:
            self.begin_time=self.begin_date+" "+str(self.begin_hour)+":00:00"
            self.end_time=self.begin_date+" "+str(self.end_hour)+":00:00"
        else:
            self.begin_time=self.begin_date+" "+str(self.begin_hour)+":00:00"
            self.end_time=self.begin_date+" "+str(self.end_hour+1)+":00:00"
            self.end_hour=self.begin_hour+1



##############获取月份##############

    def mon(self):

        mon =datetime.now().strftime("%m")

        return mon


        if time<10:

           return "0" +time
        else:
            return time


#广告消耗

    def cmp_order_consume(self):


        sql1 = '''SELECT SUM(ad_consume) FROM voyagerstat.summary_order_hour{}  WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)

        sql2= ''' SELECT SUM(charge_amount) FROM voyagerlog.ad_click_log{} WHERE ad_order_id = {} AND STATUS =1  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.order_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:
                return "校验广告消耗字段成功！ "
            else:
                return ("summary_order_hour表ad_consume:{},ad_click_log表:{}\nsummary_order_hour表sql:{},ad_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_order_hour表查询ad_consume数据为空"


 #校验广告(媒体)现金收入

    def cmp_order_cashincome(self):

        sql1 = ''' SELECT SUM(media_income_cash) FROM voyagerstat.summary_order_hour{}  WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)
        sql2= ''' SELECT  SUM(media_income_cash) FROM voyagerlog.ad_click_log{} WHERE ad_order_id = {} AND STATUS =1  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.order_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:
                return "校验广告(媒体)现金收入字段成功！ "
            else:
                return ("summary_order_hour表media_income_cash:{},ad_click_log表:{}\nsummary_order_hour表sql:{},ad_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_order_hour表查询media_income_cash数据为空"


#校验广告(媒体)奖励收入

    def cmp_order_awardincome(self):

        sql1 = ''' SELECT SUM(media_income_award) FROM voyagerstat.summary_order_hour{}  WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)
        sql2= ''' SELECT  SUM(media_income_award) FROM voyagerlog.ad_click_log{} WHERE ad_order_id = {} AND STATUS =1  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.order_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:
                return "校验广告(媒体)奖励收入字段成功！ "
            else:
                return ("summary_order_hour表media_income_award:{},ad_click_log表:{}\nsummary_order_hour表sql:{},ad_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_order_hour表查询media_income_award数据为空"


##广告有效点击次数

    def cmp_order_ad_clicknum(self):


        sql1 = ''' SELECT SUM(ad_click_effect_num) FROM voyagerstat.summary_order_hour{}   WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)
        sql2= ''' SELECT  COUNT(1) FROM voyagerlog.ad_click_log{} WHERE ad_order_id = {} AND STATUS =1  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.order_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:
                return "校验广告有效点击次数字段成功！ "
            else:
                return ("summary_order_hour表ad_click_effect_num:{},ad_click_log表:{}\nsummary_order_hour表sql:{},ad_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_order_hour表查询ad_click_effect_num数据为空"

 ##广告无效点击次数

    def cmp_order_ad_invlidnum(self):


        sql1 = ''' SELECT SUM(ad_click_invalid_num) FROM voyagerstat.summary_order_hour{}   WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)
        sql2= ''' SELECT  COUNT(1) FROM voyagerlog.ad_click_log{} WHERE ad_order_id = {} AND STATUS =2  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.order_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:
                return "校验广告无效点击次数字段成功！ "
            else:
                return ("summary_order_hour表ad_click_invalid_num:{},ad_click_log表:{}\nsummary_order_hour表sql:{},ad_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_order_hour表查询ad_click_invalid_num数据为空"

##广告废弃点击次数

    def cmp_order_ad_disusenum(self):


        sql1 = ''' SELECT SUM(ad_click_disuse_num) FROM voyagerstat.summary_order_hour{}   WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)
        sql2= ''' SELECT  COUNT(1) FROM voyagerlog.ad_click_log{} WHERE ad_order_id = {} AND STATUS =3  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.order_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:
                return "校验广告废弃点击次数字段成功！ "
            else:
                return ("summary_order_hour表ad_click_disuse_num:{},ad_click_log表:{}\nsummary_order_hour表sql:{},ad_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_order_hour表查询ad_click_disuse_num数据为空"





##校验广告点击人数暂不校验
    #
    # def cmp_order_adclickr_person(self):
    #
    #
    #     sql1 = ''' SELECT SUM(ad_click_person) FROM voyagerstat.summary_order_hour{}   WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)
    #
    #     sql2= ''' SELECT  COUNT(DISTINCT(user_cookie)) FROM voyagerlog.ad_click_log{} WHERE ad_order_id = {} AND STATUS =1  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.order_id,self.begin_time,self.end_time)
    #
    #     re1=self.dbstat.execute_sql(sql1)[0][0]
    #     print re1
    #     re2=self.db.execute_sql(sql2)[0][0]
    #     print re2
    #     if re1>=0:
    #
    #         if re1==re2:
    #
    #             return "校验广告点击人数字段成功！ "
    #         else:
    #             return ("summary_order_hour表ad_click_person:{},ad_click_log表:{}\nsummary_order_hour表sql:{},ad_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))
    #
    #     else:
    #         return "summary_order_hour表查询ad_click_person数据为空"




##校验广告有效曝光量

    def cmp_ad_effectshownum(self):



        sql1 = ''' SELECT SUM(ad_show_effect_num) FROM voyagerstat.summary_order_hour{}   WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)

        sql2= ''' SELECT COUNT(1) FROM voyagerlog.ad_show_log{} WHERE ad_order_id ={} AND STATUS =1 AND position_id <>0  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.order_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:

                return "校验广告有效曝光量字段成功！ "
            else:
                return ("summary_order_hour表ad_show_effect_num:{},ad_show_log表:{}\nsummary_order_hour表sql:{},ad_show_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_order_hour表查询ad_show_log数据为空"

##校验广告无效曝光次数

    def cmp_ad_invlidshownum(self):

        sql1 = ''' SELECT SUM(ad_show_invalid_num) FROM voyagerstat.summary_order_hour{}   WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)

        sql2= ''' SELECT COUNT(1) FROM voyagerlog.ad_show_log{} WHERE ad_order_id ={} AND STATUS =2  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.order_id,self.begin_time,self.end_time)
        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:

                return "校验广告无效曝光次数成功!"
            else:
                return ("summary_order_hour表ad_show_invalid_num:{},ad_show_log表:{}\nsummary_order_hour表sql:{},ad_show_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_order_hour表查询ad_show_log数据为空"


##校验广告无效曝光次数

    def cmp_ad_dissueshownum(self):

        sql1 = ''' SELECT SUM(ad_show_disuse_num) FROM voyagerstat.summary_order_hour{}   WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)

        sql2= ''' SELECT COUNT(1) FROM voyagerlog.ad_show_log{} WHERE ad_order_id ={} AND STATUS=3  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.order_id,self.begin_time,self.end_time)
        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:

                return "校验广告废弃曝光次数成功!"
            else:
                return ("summary_order_hour表ad_show_disuse_num:{},ad_show_log表:{}\nsummary_order_hour表sql:{},ad_show_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_order_hour表查询ad_show_log数据为空"

# ##校验广告曝光人数 暂不校验
#
#     def cmp_adshow_person(self):
#
#         sql1 = ''' SELECT SUM(ad_show_person) FROM voyagerstat.summary_order_hour{}   WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)
#
#         sql2= ''' SELECT COUNT(DISTINCT(user_cookie)) FROM voyagerlog.ad_show_log{} WHERE ad_order_id ={}  AND STATUS=1  AND create_time >='{}' AND create_time <'{}' '''.format(self.begin_date1,self.order_id,self.begin_time,self.end_time)
#
#         re1=self.dbstat.execute_sql(sql1)[0][0]
#         print re1
#         re2=self.db.execute_sql(sql2)[0][0]
#         print re2
#         if re1>=0:
#
#             if re1==re2:
#
#                 return "校验广告废弃曝光次数成功!"
#             else:
#                 return ("summary_order_hour表ad_show_disuse_num:{},ad_show_log表:{}\nsummary_order_hour表sql:{},ad_show_log表sql:{}".format(str(re1),str(re2),sql1,sql2))
#
#         else:
#             return "summary_order_hour表查询ad_show_log数据为空"

##校验表单预约效果数

    def cmp_effect_1(self):



        sql1 = ''' SELECT  SUM(type1_num)  FROM voyagerstat.summary_order_hour{}     WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)

        sql2= ''' SELECT COUNT(1) FROM voyagerlog.ad_effect_log_{} WHERE ad_order_id = {}  AND TYPE=1    AND create_time >='{}' AND create_time <'{}' '''.format(self.mon,self.order_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:

                return "校校验表单预约效果数成功!"
            else:
                return ("summary_order_hour表type1_num:{},ad_show_log表:{}\nsummary_order_hour表sql:{},ad_effect_log_表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_order_hour表查询type1_num数据为空"


##校验下载效果数

    def cmp_effect_2(self):


        sql1 = ''' SELECT  SUM(type2_num)  FROM voyagerstat.summary_order_hour{}     WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)

        sql2= ''' SELECT COUNT(1) FROM voyagerlog.ad_effect_log_{} WHERE ad_order_id = {}  AND TYPE=2  AND create_time >='{}' AND create_time <'{}' '''.format(self.mon,self.order_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:

                return "校校验表单预约效果数成功!"
            else:
                return ("summary_order_hour表type2_num:{},ad_show_log表:{}\nsummary_order_hour表sql:{},ad_effect_log_表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_order_hour表查询type2_num数据为空"


 ##校验激活效果数

    def cmp_effect_3(self):


        sql1 = ''' SELECT  SUM(type3_num)  FROM voyagerstat.summary_order_hour{}     WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)

        sql2= ''' SELECT COUNT(1) FROM voyagerlog.ad_effect_log_{} WHERE ad_order_id = {}  AND TYPE=3    AND create_time >='{}' AND create_time <'{}' '''.format(self.mon,self.order_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:

                return "校验激活效果数成功!"
            else:
                return ("summary_order_hour表type3_num:{},ad_show_log表:{}\nsummary_order_hour表sql:{},ad_effect_log_表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_order_hour表查询type3_num数据为空"


##校验注册效果数

    def cmp_effect_4(self):


        sql1 = ''' SELECT  SUM(type4_num)  FROM voyagerstat.summary_order_hour{}     WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)

        sql2= ''' SELECT COUNT(1) FROM voyagerlog.ad_effect_log_{} WHERE ad_order_id = {}  AND TYPE=4    AND create_time >='{}' AND create_time <'{}' '''.format(self.mon,self.order_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:

                return "校验注册效果数成功!"
            else:
                return ("summary_order_hour表type4_num:{},ad_show_log表:{}\nsummary_order_hour表sql:{},ad_effect_log_表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_order_hour表查询type4_num数据为空"

##校验付费行为效果数

    def cmp_effect_5(self):


        sql1 = ''' SELECT  SUM(type5_num)  FROM voyagerstat.summary_order_hour{}     WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)

        sql2= ''' SELECT COUNT(1) FROM voyagerlog.ad_effect_log_{} WHERE ad_order_id = {}  AND TYPE=5   AND create_time >='{}' AND create_time <'{}' '''.format(self.mon,self.order_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:

                return "校验付费效果数成功!"
            else:
                return ("summary_order_hour表type5_num:{},ad_show_log表:{}\nsummary_order_hour表sql:{},ad_effect_log_表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_order_hour表查询type5_num数据为空"


##校验下单行为效果数

    def cmp_effect_6(self):


        sql1 = ''' SELECT  SUM(type6_num)  FROM voyagerstat.summary_order_hour{}     WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)

        sql2= ''' SELECT COUNT(1) FROM voyagerlog.ad_effect_log_{} WHERE ad_order_id = {}  AND TYPE=6   AND create_time >='{}' AND create_time <'{}' '''.format(self.mon,self.order_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:

                return "校验下单效果数成功!"
            else:
                return ("summary_order_hour表type6_num:{},ad_show_log表:{}\nsummary_order_hour表sql:{},ad_effect_log_表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_order_hour表查询type6_num数据为空"

##校验加粉效果数

    def cmp_effect_17(self):


        sql1 = ''' SELECT  SUM(type17_num)  FROM voyagerstat.summary_order_hour{}     WHERE adorder_id= {} AND HOUR >={} and HOUR<{} '''.format(self.begin_date1,self.order_id,self.begin_hour,self.end_hour)

        sql2= ''' SELECT COUNT(1) FROM voyagerlog.ad_effect_log_{} WHERE ad_order_id = {}  AND TYPE=17   AND create_time >='{}' AND create_time <'{}' '''.format(self.mon,self.order_id,self.begin_time,self.end_time)

        re1=self.dbstat.execute_sql(sql1)[0][0]
        print re1
        re2=self.db.execute_sql(sql2)[0][0]
        print re2
        if re1>=0:

            if re1==re2:

                return "校验加粉效果数成功!"
            else:
                return ("summary_order_hour表type17_num:{},ad_show_log表:{}\nsummary_order_hour表sql:{},ad_effect_log_表sql:{}".format(str(re1),str(re2),sql1,sql2))

        else:
            return "summary_order_hour表查询type17_num数据为空"




if __name__=='__main__':

    Hro=Hour_report_order('2019-08-18',8,9,29980,False)
    print Hro.cmp_order_consume()
    print Hro.cmp_order_cashincome()
    print Hro.cmp_order_awardincome()
    print Hro.cmp_order_ad_clicknum()
    print Hro.cmp_order_ad_invlidnum()
    print Hro.cmp_order_ad_disusenum()
    print Hro.cmp_ad_effectshownum()
    print Hro.cmp_ad_invlidshownum()
    print Hro.cmp_ad_dissueshownum()
    print Hro.cmp_effect_1()
    print Hro.cmp_effect_2()
    print Hro.cmp_effect_3()
    print Hro.cmp_effect_4()
    print Hro.cmp_effect_5()
    print Hro.cmp_effect_6()
    print Hro.cmp_effect_17()



    # # print Hra.cmp_zone_clickperson()
    # print Hra.cmp_zone_invalidnum()
    # print Hra.cmp_mediacash()
    # print Hra.cmp_mediaaward()
    # print Hra.cmp_adshownum()
    # # print Hra.cmp_adshowperson()
    # print Hra.cmp_adclicknum()
    # print Hra.cmp_xiexienum()
