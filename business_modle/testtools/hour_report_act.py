# _*_ coding:utf-8 _*_

__author__ = 'aidinghua'

from utils.db_info import *
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class Hour_report_act(object):




    def __init__(self,begin_date,begin_hour,end_hour,act_id,env_value=False):

        self.db=DbOperations(env_value=env_value)
        self.dbstat=DbOperations(env_value='ss')
        self.begin_date=begin_date
        self.begin_date1=str(self.begin_date).replace('-','')
        self.begin_hour=begin_hour
        self.end_hour=end_hour
        self.act_id=act_id
        # print type(self.begin_date)
        # print type(self.end_hour)
        if self.begin_hour<self.end_hour:
           self.begin_time=self.begin_date+" "+str(self.begin_hour)+":00:00"
           self.end_time=self.begin_date+" "+str(self.end_hour)+":00:00"
        else:
           self.begin_time=self.begin_date+" "+str(self.begin_hour)+":00:00"
           self.end_time=self.begin_date+" "+str(self.end_hour+1)+":00:00"
           self.end_hour=self.begin_hour+1



##校验act_show_num

    def cmp_act_shownum(self):




       sql1 = '''SELECT  SUM(act_show_num) FROM voyagerstat.summary_act_hour{}  WHERE HOUR >={} and HOUR<{} AND act_id = {}'''.format(self.begin_date1,self.begin_hour,self.end_hour,self.act_id)

       sql2= '''SELECT  COUNT(1) FROM voyagerlog.act_click_log{} WHERE status =1 and create_time >='{}' AND create_time<'{}' AND act_id = {}'''.format(self.begin_date1,self.begin_time,self.end_time,self.act_id)

       re1=self.dbstat.execute_sql(sql1)[0][0]
       print re1
       re2=self.db.execute_sql(sql2)[0][0]
       print re2
       if re1:

         if re1==re2:
           return "校验act_show_num字段成功！ "
         else:
           return ("summary_act_hour表act_show_num:{},act_click_log表:{}\nsummary_act_hour表sql:{},ad_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))

       else:
           return "summary_act_hour表查询act_show_num数据为空"

##校验act_adclick_num
    def cmp_act_adclicknum(self):


       sql1='''SELECT  SUM(act_adclick_num) FROM voyagerstat.summary_act_hour{}  WHERE HOUR >={} and HOUR<{} AND act_id = {}'''.format(self.begin_date1,self.begin_hour,self.end_hour,self.act_id)

       sql2='''SELECT COUNT(1) FROM voyagerlog.ad_click_log{}  WHERE STATUS =1 AND act_id = {} AND create_time >='{}' AND create_time<'{}' '''.format(self.begin_date1,self.act_id,self.begin_time,self.end_time)

       re1=self.dbstat.execute_sql(sql1)[0][0]
       print re1
       re2=self.db.execute_sql(sql2)[0][0]
       print re2
       if re1:

          if re1==re2:
             return "校验act_adclick_num字段成功！ "
          else:
             return ("summary_act_hour表act_adclick_num:{},ad_click_log表:{}\nsummary_act_hour表sql:{},ad_click_log表sql:{}".format(str(re1),str(re2),sql1,sql2))
       else:
           return "summary_act_hour表查询act_adclick_num数据为空"



##校验act_show_person,由于目前人数统计不准，暂不校验
#
# sql='''SELECT  SUM(act_show_person) FROM voyagerstat.summary_act_hour20190717  WHERE HOUR =10 AND act_id = 5074'''
#
# sql='''SELECT  COUNT(DISTINCT(user_cookie)) FROM voyagerlog.`act_click_log20190717` WHERE status =1 and create_time >='2019-07-17 10:00:00' AND create_time<'2019-07-17 11:00:00' AND act_id = 5074'''
#

##校验act_adshow_person,由于目前人数统计不准，暂不校验
#
# sql='''SELECT SUM(act_adshow_person) FROM voyagerstat.summary_act_hour20190717  WHERE HOUR =10 AND act_id = 5074'''
#
# sql='''SELECT COUNT(DISTINCT(user_cookie)) FROM voyagerlog.`ad_show_log20190717`  WHERE STATUS =1  AND  create_time >='2019-07-17 10:00:00' AND create_time<'2019-07-17 11:00:00' '''


if __name__=='__main__':

    Hra=Hour_report_act('2019-08-13',8,9,597,False)
    print Hra.cmp_act_shownum()
    print Hra.cmp_act_adclicknum()