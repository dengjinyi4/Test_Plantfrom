# encoding=utf-8
__author__ = 'aidinghua'

import sys
import datetime
import time

from utils.dtdb_info import *

class Punchcard(object):

    def __init__(self,begin_date,end_date,env_value=False):

        self.dbinfo=DtdbOperations(env_value=env_value)
        self.begin_date=begin_date
        self.end_date=end_date


#查询低碳打卡用户总数
    def total_amount(self):

        sql="select  count(1)  FROM  ditandaka.wx_user_info"
        result=self.dbinfo.execute_sql(sql)[0][0]
        return result

#查询低碳打卡今日新增用户数
    def today_addamount(self):

        sql="select  count(1)   FROM  ditandaka.wx_user_info  where create_time >= curdate()"
        result = self.dbinfo.execute_sql(sql)[0][0]
        return result

#查询今日完成打卡用户数
    def today_sign(self):

        sql="SELECT count(1) FROM ditandaka.wx_user_punchedcard WHERE create_time >= CURRENT_DATE()"
        result = self.dbinfo.execute_sql(sql)[0][0]
        return result


#查询日期输出

    def dateRange(self,beginDate, endDate):

      beginDate=self.begin_date
      endDate=self.end_date
      dates = []
      dt = datetime.datetime.strptime(beginDate,"%Y-%m-%d")

      date = beginDate[:]
      while date <= endDate:
        dates.append(str(date))
        dt += datetime.timedelta(days=1)
        date = dt.strftime("%Y-%m-%d")
      print type(dates)
      return dates

#按日期查询每日新增用户输出

    def add_user(self,beginDate,endDate):

        beginDate=self.begin_date
        endDate=self.end_date
        # endDate = datetime.datetime.strptime(endDate,"%Y-%m%d")
        # endDate+=datetime.timedelta(days=1)
        timelist=Punchcard(beginDate,endDate,env_value=False).dateRange(beginDate,endDate)

        len_time = len(timelist)
        usernum=[]
        for i in range(0,len_time):
               sql='''SELECT count(1) FROM  ditandaka.wx_user_info WHERE DATE_FORMAT(create_time,'%Y-%m-%d')='{}' '''.format(timelist[i])
               result=self.dbinfo.execute_sql(sql)[0][0]
               usernum.append(int(result))


        return usernum

#今日通过邀请新增的用户

    def invite_add(self):

         sql ='''SELECT count(1) FROM ditandaka.wx_user_info WHERE open_id   IN (SELECT open_id FROM ditandaka.wx_invite_relation )
              AND  create_time >=CURRENT_DATE()'''
         result = self.dbinfo.execute_sql(sql)[0][0]
         return result

#今日通过非邀请新增的用户

    def non_inviteadd(self):

         sql = ''' SELECT count(1)  FROM ditandaka.wx_user_info  WHERE open_id NOT IN (SELECT a.open_id FROM ditandaka.wx_user_info a ,ditandaka.wx_invite_relation b
               WHERE a.open_id = b.open_id ) AND  create_time >=CURRENT_DATE() '''
         result = self.dbinfo.execute_sql(sql)[0][0]
         return result


##输出今日日期
    def today_date(self):

        return datetime.datetime.now().strftime("%Y-%m-%d")

##输出昨日日期

    def yesterday_date(self):

        return (datetime.datetime.now()+datetime.timedelta(days=-1)).strftime("%Y-%m-%d")

##输出当前年月份

    def mon(self):

        return time.strftime("%Y%m")


##查询每日用户日活数

    def user_live(self,beginDate,endDate):

        beginDate=self.begin_date
        endDate=self.end_date
        timelist=Punchcard(beginDate,endDate,env_value=False).dateRange(beginDate,endDate)
        print timelist
        len_time = len(timelist)
        usernum=[]
        for i in range(0,len_time):
            sql='''SELECT COUNT(DISTINCT(open_id)) FROM ditandaka.`wx_user_log{}` WHERE DATE_FORMAT( create_time, '%Y-%m-%d') = '{}' '''.format(self.mon(),timelist[i])
            result=self.dbinfo.execute_sql(sql)[0][0]
            usernum.append(int(result))

        return usernum



##输出昨日日期




#查询低碳打卡用户明细数据
    #
    # def user_info(self):
    #
    #     sql='''select
    #         open_id openid,
    #         nick_name 昵称,
    #         total_tjf 用户累计碳积分,
    #         balance_tjf 用户碳积分余额,
    #         total_step 用户累计步数,
    #         tree_level 树的等级
    #         from
    #         voyager.wx_user_info order by total_tjf desc'''
    #
    #     result = self.dbinfo.execute_sql(sql)
    #
    #     return result





if  __name__=='__main__':

    re = Punchcard("2019-02-01","2019-02-12")

    # print re.total_amount()
    # print re.today_addamount()
    # print re.user_info()
    # print re.dateRange("2018-12-01","2018-12-23")
    # print re.add_user("2018-12-01","2018-12-23")
    print re.user_live('2019-02-01','2019-02-12')
    # print re.invite_add()
    # print re.non_inviteadd()
    #
    # print re.today_date()
    # print re.yesterday_date()
    # print re.mon()





