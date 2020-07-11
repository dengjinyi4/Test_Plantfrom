# -*- coding: utf-8 -*-
# @Time    : 2020/5/27 17:42
# @Author  : zhaoyu
# @Function  : 修改易购宝贝用户状态
from utils.db_info import *

class alter_user(object):

    def __init__(self,phone,status):
        self.phone = phone
        self.status = status

    def alterStaus(self):
        sql = "select * from normandy.normandy_user where `status`=1 AND phone='"+str(self.phone)+"'"
        sql1 ="update normandy.normandy_user set status=3 where `status`=1 AND phone='"+str(self.phone)+"'"
        sql2 = "update normandy.normandy_user set member_status=0 where `status`=1 AND phone='" + str(self.phone) + "'"
        sql3 = "update normandy.normandy_user set member_status=1 where `status`=1 AND phone='" + str(self.phone) + "'"
        sql4 = "update normandy.normandy_user set member_status=2 where `status`=1 AND phone='" + str(self.phone) + "'"
        print sql
        try:
            counts = DbOperations().len_value(sql)
            print counts
            if counts>0 and self.status=='1':
                DbOperations(env_value=True).execute_sql(sql1)
                return '修改成功'
            elif counts>0 and self.status=='2':
                DbOperations(env_value=True).execute_sql(sql2)
                return '修改成功'
            elif counts>0 and self.status=='3':
                DbOperations(env_value=True).execute_sql(sql3)
                return '修改成功'
            elif counts>0 and self.status=='4':
                DbOperations(env_value=True).execute_sql(sql4)
                return '修改成功'
            else:
                return "请确认用户状态是否正常"
        except Exception as e:
            print(e)


if __name__ == '__main__':
    a = alter_user('13693511025').alterStaus()

