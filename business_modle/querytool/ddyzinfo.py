#coding=utf-8
#！/usr/bin/pyhon

from business_modle.querytool.utils.db_egou import *


class YzInfo(object):
    def __init__(self,userid,env='1'):
        env_dict={'1':True,'0':False}
        # env_dict = {u'测试环境':True,u'生产环境':False}
        self.db = Dboperation(env_value=env_dict[env])
        self.userid = userid
        pass


    def show_result(self):
        # sql = "SELECT NAME, user_id, phone,create_time,update_time,LEVEL, parent_user_id   FROM fanxian.union_leader WHERE  user_id=" + str(self.userid)
        sql = "SELECT NAME, user_id, phone,create_time,update_time, CASE LEVEL  WHEN 0 THEN '总代' ELSE '代理' END AS LEVEL , parent_user_id FROM fanxian.union_leader WHERE  user_id=" + str(self.userid)
        print sql
        re=self.db.execute_sql(sql)
        print re
        return re

     # def resultLi(self,re):
     #     if len(str(re)) > 0:
     #         re = list(re)
     #         row = len(re)
     #         for col in range(row):
     #             re.append(re[row][col])
     #             return re


# if __name='__main__':
#     re=db.execute_sql(sql)
#     print int(re[0][0])

if __name__=="__main__" :
    ddy = YzInfo(10838218)
    print ddy.show_result()







