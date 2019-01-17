# -*- coding: utf-8 -*-
# @Time    : 2018/11/27 14:19
# @Author  : wanglanqing
from utils.db_info import *


class phoneVaild(object):
    def __init__(self,env='1'):
        env_dict = {'1':True,'0':False}
        self.db = DbOperations(env_value=env_dict[env])
        pass

    def get_valid_code(self):
        sql = "select PHONE,MSG,create_time from voyager.phone_send_record order by id desc limit 50"
        re = self.db.execute_sql(sql)
        # re='sss'
        return re