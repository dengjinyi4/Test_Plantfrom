# encoding=utf-8
__author__ = 'aidinghua'

import sys
import datetime
import json
from utils.db_info import  *

class QueryAppKey(object):
    def __init__(self,Adzone_id,env_value=True):
        self.db=DbOperations(env_value=env_value)
        self.Adzone_id=Adzone_id

    def queryAppKey(self):
        sql="SELECT app_key FROM base_adzone_info WHERE id = "+ str(self.Adzone_id)
        result=self.db.execute_sql(sql)
        appkey=result[0][0]
        print sql
        print appkey
        return appkey
    def __del__(self):
        self.db.close_cursor()
        self.db.close_db()


if "__main__"==__name__:
    qa=QueryAppKey(125,True)
    qa.queryAppKey()
    print qa


