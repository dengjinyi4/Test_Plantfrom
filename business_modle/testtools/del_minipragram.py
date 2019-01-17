# encoding=utf-8
__author__ = 'aidinghua'

import sys
import time
import  datetime
from utils.db_info import  *
class Del_minipragram(object):

    def __init__(self,openid,env_value=True):

        self.openid=openid
        self.db= DbOperations(env_value=env_value)

    def del_sql(self):

        sql1="DELETE FROM voyager.wx_user_info WHERE open_id ='{}'".format(self.openid)
        sql2="DELETE FROM voyager.wx_user_order WHERE open_id ='{}'".format(self.openid)
        sql3="DELETE FROM voyager.wx_user_program WHERE open_id='{}'".format(self.openid)
        sql4="DELETE FROM voyager.wx_tjflogs  WHERE open_id ='{}'".format(self.openid)
        sql5="DELETE FROM voyager.wx_steplogs WHERE open_id ='{}'".format(self.openid)
        sql6="DELETE FROM voyager.wx_invite_relation WHERE inviter_openid ='{}'".format(self.openid)
        sql7="DELETE FROM voyager.wx_user_punchedcard WHERE open_id ='{}'".format(self.openid)
        sql8="DELETE FROM voyager.wx_user_order WHERE open_id ='{}'".format(self.openid)
        sql9="DELETE FROM voyager.wx_user_authorize_log WHERE open_id ='{}'".format(self.openid)
        sql10="DELETE FROM voyager.wx_user_clock_remind WHERE open_id='{}'".format(self.openid)


        self.db.execute_sql(sql1)
        self.db.execute_sql(sql2)
        self.db.execute_sql(sql3)
        self.db.execute_sql(sql4)
        self.db.execute_sql(sql5)
        self.db.execute_sql(sql6)
        self.db.execute_sql(sql7)
        self.db.execute_sql(sql8)
        self.db.execute_sql(sql9)
        self.db.execute_sql(sql10)
        return "数据删除完成!!!"



Del = Del_minipragram('o0hyf4jfdPYcE-Zvacj4NRMZa111',env_value=True)
Del.del_sql()