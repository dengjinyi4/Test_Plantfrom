# encoding=utf-8
__author__ = 'aidinghua'

import sys
import time
import  datetime
from utils.dtdb_info import *
class Del_minipragram(object):

    def __init__(self,openid,env_value=True):

        self.openid=openid
        self.db= DtdbOperations(env_value=env_value)

    def cur_date(self):


        return datetime.datetime.now().strftime("%Y%m")



    def del_sql(self):

    
        sql1="DELETE FROM ditandaka.wx_user_info WHERE open_id ='{}'".format(self.openid)
        sql2="DELETE FROM ditandaka.wx_user_order WHERE open_id ='{}'".format(self.openid)
        sql3="DELETE FROM ditandaka.wx_user_program WHERE open_id='{}'".format(self.openid)
        sql4="DELETE FROM ditandaka.wx_tjflogs{}  WHERE open_id ='{}'".format(self.cur_date(),self.openid)
        sql5="DELETE FROM ditandaka.wx_steplogs{} WHERE open_id ='{}'".format(self.cur_date(),self.openid)
        sql6="DELETE FROM ditandaka.wx_invite_relation WHERE inviter_openid ='{}'".format(self.openid)
        sql7="DELETE FROM ditandaka.wx_user_punchedcard WHERE open_id ='{}'".format(self.openid)
        sql8="DELETE FROM ditandaka.wx_user_authorize_log WHERE open_id ='{}'".format(self.openid)
        sql9="DELETE FROM ditandaka.wx_user_clock_remind{} WHERE open_id='{}'".format(self.cur_date(),self.openid)
        sql10="DELETE FROM ditandaka.wx_user_award WHERE open_id='{}'".format(self.openid)

        sqllist=[sql1,sql2,sql3,sql4,sql5,sql6,sql7,sql8,sql9,sql10]
        #print sqllist[0]
        for i in range(0,10):
            self.db.execute_sql(sqllist[i])
    

        return "数据删除完成!!!"



if __name__=='__main__':

   Del = Del_minipragram('o0hyf4lMU7CcdWQJLbF5NUcoDtco',env_value=True)
   Del.del_sql()
