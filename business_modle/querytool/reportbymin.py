# encoding=utf-8
__author__ = 'aidinghua'

import  time
from utils.db_info import *
from openpyxl import  Workbook

class Reportbymin(object):

    def __init__(self,begin_date,begin_hour,end_hour,begin_min,end_min,env_value=False):

        self.db=DbOperations(env_value=env_value)
        self.begin_date=begin_date
        self.begin_date_new=self.begin_date.replace('-','')
        self.begin_hour=begin_hour
        self.end_hour=end_hour
        self.begin_min=begin_min
        self.end_min=end_min



    def adzoneclick(self):

        sql='''select DATE_FORMAT(create_time,'%Y-%m-%d %H:%i') 时间,count(1) 广告位点击 from voyagerlog.`adzone_click_log{}` where status=1 and create_time>='{} {}:{}:00' and create_time<'{} {}:{}:59' GROUP BY DATE_FORMAT(create_time,'%Y-%m-%d %H:%i')'''.format(self.begin_date_new,self.begin_date,self.begin_hour,self.begin_min,self.begin_date,self.end_hour,self.end_min );

        result=self.db.execute_sql(sql)

        return result



    def adshow(self):

        sql=''' SELECT DATE_FORMAT(create_time,'%Y-%m-%d %H:%i') 时间,COUNT(1) 广告展现,SUM(charge_amount)/100 CPM订单消耗 FROM voyagerlog.`ad_show_log{}` WHERE STATUS=1 AND create_time>='{} {}:{}:00' AND create_time<='{} {}:{}:59' GROUP BY DATE_FORMAT(create_time,'%Y-%m-%d %H:%i') '''.format(self.begin_date_new,self.begin_date,self.begin_hour,self.begin_min,self.begin_date,self.end_hour,self.end_min );

        result=self.db.execute_sql(sql)

        return result

    def adclick(self):

        sql=''' select DATE_FORMAT(create_time,'%Y-%m-%d %H:%i') 时间,count(1) 广告点击 ,sum(charge_amount)/100 CPC订单消耗 from voyagerlog.`ad_click_log{}` WHERE STATUS=1 AND create_time>'{} {}:{}:00' AND create_time<'{} {}:{}:59' GROUP BY DATE_FORMAT(create_time,'%Y-%m-%d %H:%i')'''.format(self.begin_date_new,self.begin_date,self.begin_hour,self.begin_min,self.begin_date,self.end_hour,self.end_min );

        result=self.db.execute_sql(sql)

        return result



if __name__=='__main__':

    reportmin=Reportbymin('2019-06-01','9','9','10','20')

    print reportmin.adzoneclick()