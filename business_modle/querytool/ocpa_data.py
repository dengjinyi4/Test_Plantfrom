# encoding=utf-8
__author__ = 'aidinghua'

import time

import requests
from datetime import datetime,timedelta
from utils.db_info import *



class Ocpa_data(object):

    def __init__(self,begin_time,url,url2,env_value=True):

        self.db=DbOperations(env_value=env_value)

        self.begin_time=begin_time

        self.url=url

        self.url2=url2



##############获取月份##############

    def mon(self):

        mon =datetime.now().strftime("%m")

        return mon


        # if time<10:
        #
        #    return "0" +time
        #

#######获取页面选择时间yyyymmdd############

    def selected_time(self):

        time=datetime.now().strftime("%Y%m%d")

        return  time



#######获取页面选择时间年月yyyymm#############

    def yearmon(self):

        time=datetime.now().strftime("%Y%m")

        return  time



#######获取页面选择时间yyyy-mm-dd############

    def selected_time1(self):

        time=datetime.now().strftime("%Y-%m-%d")

        return  time

#######获取页面时间前一天yyyymmdd###########


    def selected1_time(self):

        now=datetime.now()

        time1 = now - timedelta(days=1)


        return time1.strftime("%Y%m%d")

#######获取页面时间前一天yyyy-mm-dd###########


    def selected1_time1(self):

        now=datetime.now()

        time1 = now - timedelta(days=1)

        return time1.strftime("%Y-%m-%d")



##########获取页面选择时间前两天yyyymmdd#############
    def selected2_time(self):

        now=datetime.now()

        time2 = now - timedelta(days=2)

        return time2.strftime("%Y%m%d")


##########获取页面选择时间前两天yyyy-mm-dd#############
    def selected2_time1(self):

        now=datetime.now()

        time2 = now - timedelta(days=2)

        return time2.strftime("%Y-%m-%d")




##########获取页面选择时间前三天yyyymmdd#############
    def selected3_time(self):

        now=datetime.now()

        time2 = now - timedelta(days=3)

        return time2.strftime("%Y%m%d")


##########获取页面选择时间前两天yyyy-mm-dd#############
    def selected3_time1(self):

        now=datetime.now()

        time2 = now - timedelta(days=3)

        return time2.strftime("%Y-%m-%d")





#################获取配置表中配置延迟时间天数(目前写死7)的前三天############

#############延迟时间前一天###################
    def delay1(self):

        now=datetime.now()

        time1 = now - timedelta(days=8)

        return time1.strftime("%Y-%m-%d")



###########################延迟时间前两天########################
    def delay2(self):

        now=datetime.now()

        time2 = now - timedelta(days=9)

        return time2.strftime("%Y-%m-%d")



    ##############################延迟时间前三天###############
    def delay3(self):

        now=datetime.now()

        time3 = now - timedelta(days=10)

        return time3.strftime("%Y-%m-%d")










############导入当天ocpa_ad_show_log_stat,ocpa_ad_click_log_stat表数据##########

    def show_stat1(self):

        url='https://ypg.adhudong.com/private/crm/info.html?channel=adhudong&utm_click=${click_tag}&id=171'

        sql11='''
             DELETE
             FROM
             voyagerlog.ocpa_ad_show_log_stat{}
             WHERE adzone_id = 102
             AND advertiser_id = 2222559

            '''.format(self.selected_time())
        sql12='''
              insert into voyagerlog.ocpa_ad_show_log_stat{} (
              `day`,
              `adzone_id`,
              `advertiser_id`,
              `url`,
              `num`)
              values
              (
                '{}',
                '102',
                '2222559',
                '{}',
                '120'
              )'''.format(self.selected_time(),self.selected_time1(),self.url)

        sql13='''
             DELETE
             FROM
             voyagerlog.ocpa_ad_click_log_stat{}
             WHERE adzone_id = 102
             AND advertiser_id = 2222559
              '''.format(self.selected_time())

        sql14='''
           INSERT INTO   voyagerlog.ocpa_ad_click_log_stat{} (
          `day`,
          `adzone_id`,
          `advertiser_id`,
          `ourl`,
          `num`,
          `click_num`
        )
        VALUES
          (
            '{}',
            '102',
            '2222559',
             '{}',
            '180.00',
            '300'
          ) '''.format(self.selected_time(),self.selected_time1(),self.url)
        sql15='''
          insert into voyagerlog.ad_effect_log_{} ( `ad_click_tag`, `type`, `uid`, `adzone_id`, `media_id`, `advertiser_id`, `ad_order_id`, `ad_creative_id`, `act_id`, `position_id`, `dev_id`, `price`, `create_time`, `update_time`, `adzone_click_id`, `method_type`, `mobile`, `age`, `name`, `meet_demand`, `int1`, `int2`, `int3`, `str1`, `str2`, `str3`, `chn`, `tag`, url, `charge_amount`, `media_income_cash`, `media_income_award`, `ua`, `region`, `ip`, `ad_plan_id`) values('E3W1CD6R1IUW88N08Y','1','999','102','1','2222559','1713','10','529','1',NULL,NULL,'{} 00:38:38','{} 11:42:37','111','2',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{}','0','0','0','0',NULL,NULL,'3')'''.format(self.mon(),self.selected_time1(),self.selected_time1(),self.url)

        self.db.execute_sql(sql11)
        self.db.execute_sql(sql12)
        self.db.execute_sql(sql13)
        self.db.execute_sql(sql14)
        self.db.execute_sql(sql15)

        return "今日ocpa_ad_show_log_stat,ocpa_ad_click_log_stat,ad_effect_log数据导入完成"

############导入昨天ocpa_ad_show_log_stat表,ocpa_ad_click_log_stat表数据##########

    def show_stat2(self):
        url='https://ypg.adhudong.com/private/crm/info.html?channel=adhudong&utm_click=${click_tag}&id=171'

        sql11='''
             DELETE
             FROM
             voyagerlog.ocpa_ad_show_log_stat{}
             WHERE adzone_id = 102
             AND advertiser_id = 2222559

            '''.format(self.selected1_time())
        sql12='''
              insert into voyagerlog.ocpa_ad_show_log_stat{} (
              `day`,
              `adzone_id`,
              `advertiser_id`,
              `url`,
              `num`)
              values
              (
                '{}',
                '102',
                '2222559',
                '{}',
                '120'
              )
              '''.format(self.selected1_time(),self.selected1_time1(),self.url)

        sql13='''
             DELETE
             FROM
             voyagerlog.ocpa_ad_click_log_stat{}
             WHERE adzone_id = 102
             AND advertiser_id = 2222559
              '''.format(self.selected1_time())

        sql14='''
           INSERT INTO  voyagerlog.ocpa_ad_click_log_stat{} (
          `day`,
          `adzone_id`,
          `advertiser_id`,
          `ourl`,
          `num`,
          `click_num`
        )
        VALUES
          (
            '{}',
            '102',
            '2222559',
            '{}',
            '180.00',
            '300'
          ) '''.format(self.selected1_time(),self.selected1_time1(),self.url)
        sql15='''
          insert into voyagerlog.ad_effect_log_{} ( `ad_click_tag`, `type`, `uid`, `adzone_id`, `media_id`, `advertiser_id`, `ad_order_id`, `ad_creative_id`, `act_id`, `position_id`, `dev_id`, `price`, `create_time`, `update_time`, `adzone_click_id`, `method_type`, `mobile`, `age`, `name`, `meet_demand`, `int1`, `int2`, `int3`, `str1`, `str2`, `str3`, `chn`, `tag`, `url`, `charge_amount`, `media_income_cash`, `media_income_award`, `ua`, `region`, `ip`, `ad_plan_id`) values('E3W1CD6R1IUW88N08Y','1','999','102','1','2222559','1713','10','529','1',NULL,NULL,'{} 00:38:38','{} 11:42:37','111','2',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{}','0','0','0','0',NULL,NULL,'3')'''.format(self.mon(),self.selected1_time1(),self.selected1_time1(),self.url)

        self.db.execute_sql(sql11)
        self.db.execute_sql(sql12)
        self.db.execute_sql(sql13)
        self.db.execute_sql(sql14)
        self.db.execute_sql(sql15)
        return "昨日ocpa_ad_show_log_stat,ocpa_ad_click_log_stat,ad_effect_log数据导入完成"



    ############导入前天ocpa_ad_show_log_stat表数据##########

    def show_stat3(self):
        url='https://ypg.adhudong.com/private/crm/info.html?channel=adhudong&utm_click=${click_tag}&id=171'

        sql11='''
             DELETE
             FROM
             voyagerlog.ocpa_ad_show_log_stat{}
             WHERE adzone_id = 102
             AND advertiser_id = 2222559

            '''.format(self.selected2_time())
        sql12='''
              insert into voyagerlog.ocpa_ad_show_log_stat{} (
              `day`,
              `adzone_id`,
              `advertiser_id`,
              `url`,
              `num`)
              values
              (
                '{}',
                '102',
                '2222559',
                '{}',
                '120'
              )
              '''.format(self.selected2_time(),self.selected2_time1(),self.url)

        sql13='''
             DELETE
             FROM
             voyagerlog.ocpa_ad_click_log_stat{}
             WHERE adzone_id = 102
             AND advertiser_id = 2222559
              '''.format(self.selected2_time())

        sql14='''
           INSERT INTO   voyagerlog.ocpa_ad_click_log_stat{} (
          `day`,
          `adzone_id`,
          `advertiser_id`,
          `ourl`,
          `num`,
          `click_num`
        )
        VALUES
          (
            '{}',
            '102',
            '2222559',
            '{}',
            '180.00',
            '300'
          ) '''.format(self.selected2_time(),self.selected2_time1(),self.url)
        sql15='''
          insert into voyagerlog.ad_effect_log_{} ( `ad_click_tag`, `type`, `uid`, `adzone_id`, `media_id`, `advertiser_id`, `ad_order_id`, `ad_creative_id`, `act_id`, `position_id`, `dev_id`, `price`, `create_time`, `update_time`, `adzone_click_id`, `method_type`, `mobile`, `age`, `name`, `meet_demand`, `int1`, `int2`, `int3`, `str1`, `str2`, `str3`, `chn`, `tag`, `url`, `charge_amount`, `media_income_cash`, `media_income_award`, `ua`, `region`, `ip`, `ad_plan_id`) values('E3W1CD6R1IUW88N08Y','6','999','102','1','2222559','1713','10','529','1',NULL,NULL,'{} 00:38:38','{} 11:42:37','111','2',NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,'{}','0','0','0','0',NULL,NULL,'3')'''.format(self.mon(),self.selected2_time1(),self.selected2_time1(),self.url)

        self.db.execute_sql(sql11)
        self.db.execute_sql(sql12)
        self.db.execute_sql(sql13)
        self.db.execute_sql(sql14)
        self.db.execute_sql(sql15)
        return "前天ocpa_ad_show_log_stat,ocpa_ad_click_log_stat,ad_effect_log数据导入完成"







    ###############更新最近三天cvr_log表################

    def cvr_data(self):
        url2='adz102_https://ypg.adhudong.com/private/crm/info.html?channel=adhudong&utm_click=${click_tag}&id=171_6_2'
        sqldel1='''DELETE FROM  voyager.cvr_log WHERE cvr_key = '{}' AND cvr_time='{}'  '''.format(self.url2,self.selected_time1())
        sqldel2='''DELETE FROM  voyager.cvr_log WHERE cvr_key = '{}' AND cvr_time='{}' '''.format(self.url2,self.selected1_time1())
        sqldel3='''DELETE FROM  voyager.cvr_log WHERE cvr_key = '{}' AND cvr_time='{}'  '''.format(self.url2,self.selected2_time1())
        sql1='''INSERT INTO voyager.cvr_log ( `cvr_time`, `day_diff`, `cvr_key`, `cvr`, `create_time`,`effect_num`,`click_num`) VALUES('{}','7011','{}','0.1733','{} 10:36:35','50','1600')'''.format(self.selected_time1(),self.url2,self.selected_time1())
        sql2='''INSERT INTO voyager.cvr_log ( `cvr_time`, `day_diff`, `cvr_key`, `cvr`, `create_time`,`effect_num`,`click_num`) VALUES('{}','7011','{}','0.1733','{} 10:36:35','50','1600')'''.format(self.selected1_time1(),self.url2,self.selected1_time1())
        sql3='''INSERT INTO voyager.cvr_log ( `cvr_time`, `day_diff`, `cvr_key`, `cvr`, `create_time`,`effect_num`,`click_num`) VALUES('{}','7011','{}','0.1733','{} 10:36:35','50','1600')'''.format(self.selected2_time1(),self.url2,self.selected2_time1())
        self.db.execute_sql(sqldel1)
        self.db.execute_sql(sqldel2)
        self.db.execute_sql(sqldel3)
        self.db.execute_sql(sql1)
        self.db.execute_sql(sql2)
        self.db.execute_sql(sql3)

        return "cvr_log表数据导入完成"



#######更新今天之前的效果数
    def before_effect(self):
        url='https://ypg.adhudong.com/private/crm/info.html?channel=adhudong&utm_click=${click_tag}&id=171'

        sql1='''insert into voyagerlog.`stat_ocpa_ad_effect_log{}` (`create_time`, `advertiser_id`, `adzone_id`, `url`, `num`) values('{}','2222559','102','{}','2') '''.format(self.yearmon(),self.selected1_time1(),self.url)

        sql2='''insert into voyagerlog.`stat_ocpa_ad_effect_log{}` (`create_time`, `advertiser_id`, `adzone_id`, `url`, `num`) values('{}','2222559','102','{}','2') '''.format(self.yearmon(),self.selected2_time1(),self.url)

        sql3='''insert into voyagerlog.`stat_ocpa_ad_effect_log{}` (`create_time`, `advertiser_id`, `adzone_id`, `url`, `num`) values('{}','2222559','102','{}','2') '''.format(self.yearmon(),self.selected3_time1(),self.url)
        self.db.execute_sql(sql1)
        self.db.execute_sql(sql2)
        self.db.execute_sql(sql3)
        return "今天之前的效果中间表数据导入完成"



###############更新延迟时间之前三天的cvr_log表################

    def cvr_data2(self):
        url2='adz102_https://ypg.adhudong.com/private/crm/info.html?channel=adhudong&utm_click=${click_tag}&id=171_6_2'
        sqldel1='''DELETE FROM  voyager.cvr_log WHERE cvr_key = '{}' AND cvr_time='{}'  '''.format(self.url2,self.delay1())
        sqldel2='''DELETE FROM  voyager.cvr_log WHERE cvr_key = '{}' AND cvr_time='{}' '''.format(self.url2,self.delay2())
        sqldel3='''DELETE FROM  voyager.cvr_log WHERE cvr_key = '{}' AND cvr_time='{}'  '''.format(self.url2,self.delay3())
        sql1='''INSERT INTO voyager.cvr_log ( `cvr_time`, `day_diff`, `cvr_key`, `cvr`, `create_time`,`effect_num`,`click_num`) VALUES('{}','7011','{}','0.1733','{} 10:36:35','50','1600')'''.format(self.delay1(),self.url2,self.delay1())
        sql2='''INSERT INTO voyager.cvr_log ( `cvr_time`, `day_diff`, `cvr_key`, `cvr`, `create_time`,`effect_num`,`click_num`) VALUES('{}','7011','{}','0.1733','{} 10:36:35','50','1600')'''.format(self.delay2(),self.url2,self.delay2())
        sql3='''INSERT INTO voyager.cvr_log ( `cvr_time`, `day_diff`, `cvr_key`, `cvr`, `create_time`,`effect_num`,`click_num`) VALUES('{}','7011','{}','0.1733','{} 10:36:35','50','1600')'''.format(self.delay3(),self.url2,self.delay3())
        self.db.execute_sql(sqldel1)
        self.db.execute_sql(sqldel2)
        self.db.execute_sql(sqldel3)
        self.db.execute_sql(sql1)
        self.db.execute_sql(sql2)
        self.db.execute_sql(sql3)

        return "cvr_log表数据导入完成"



########清除问题数据##############


    def del_error(self):

        sql1='''DELETE  FROM voyagerlog.ocpa_ad_show_log_stat{}  WHERE advertiser_id  NOT IN (SELECT id FROM voyager.advertiser ) '''.format(self.selected_time())
        sql2='''DELETE  FROM voyagerlog.ocpa_ad_show_log_stat{}  WHERE advertiser_id  NOT IN (SELECT id FROM voyager.advertiser ) '''.format(self.selected1_time())
        sql3='''DELETE  FROM voyagerlog.ocpa_ad_show_log_stat{}  WHERE advertiser_id  NOT IN (SELECT id FROM voyager.advertiser ) '''.format(self.selected2_time())
        sql4='''DELETE  FROM voyagerlog.ocpa_ad_click_log_stat{}  WHERE advertiser_id  NOT IN (SELECT id FROM voyager.advertiser ) '''.format(self.selected_time())
        sql5='''DELETE  FROM voyagerlog.ocpa_ad_click_log_stat{}  WHERE advertiser_id  NOT IN (SELECT id FROM voyager.advertiser ) '''.format(self.selected1_time())
        sql6='''DELETE  FROM voyagerlog.ocpa_ad_click_log_stat{}  WHERE advertiser_id  NOT IN (SELECT id FROM voyager.advertiser ) '''.format(self.selected2_time())

        self.db.execute_sql(sql1)
        self.db.execute_sql(sql2)
        self.db.execute_sql(sql3)
        self.db.execute_sql(sql4)
        self.db.execute_sql(sql5)
        self.db.execute_sql(sql6)

        return "问题数据清理完毕"
###########执行广告位定时任务###########

    def adzonedo(self):

        url = 'http://172.16.105.11:17091/ocpa_adzone.do'

        result=requests.get(url).text

        if  result == '1':

            return "广告位定时任务执行完成"

        else:
            return  "广告位定时任务执行失败",result

###############导入report_order表数据防止创意暂停#############


    def creative_active(self):



        sql = '''INSERT ignore INTO voyager.report_order (`date`, `adorder_id`, `agent_id`, `advertiser_id`, `plan_id`, `creative_id`, `adv_industry_id`, `creative_level`, `sales_manager_id`, `service_manager_id`, `payment_mode`, `brand_tag_id`, `adorder_state`, `show_num`, `show_invalid_num`, `show_uv`, `adclick_num`, `adclick_invalid_num`, `adclick_uv`, `ad_consume`, `ad_media_income`, `ad_budget`, `ad_withhold`, `ad_effect_num`, `cash_consume`, `reward_consume`, `cpa_ad_consume`, `cpa_cash_consume`, `ocpa_effect_num`, `ocpa_click_num`, `ocpa_consume`, `ocpa_media_income`, `ocpa_expect_consume`, `update_time`) VALUES('{}','2009','2222557','2222559','308','1884','65','1',NULL,NULL,'4','0','4','2','0','1','2','0','1','20000','145','200000','200000','1','0','0','0','0','1','2','220','145','2000','{} 05:10:09')'''.format(self.selected_time1(),self.selected_time1())

        self.db.execute_sql(sql)


        return  "report_order表数据导入成功"







if __name__ == '__main__':

    url='https://ypg.adhudong.com/private/crm/info.html?channel=adhudong&utm_click=${click_tag}&id=171'
    url2='adz102_https://ypg.adhudong.com/private/crm/info.html?channel=adhudong&utm_click=${click_tag}&id=171_6_2'
    Ocpadata= Ocpa_data('20190328',url,url2,env_value=True)

    print Ocpadata.selected_time1()

    print Ocpadata.selected1_time1()

    print Ocpadata.selected2_time1()

    print Ocpadata.mon()

    print Ocpadata.adzonedo()

    print Ocpadata.before_effect

















