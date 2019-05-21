# encoding=utf-8
__author__ = 'aidinghua'

from utils.dtdb_info import *

class Mini_add(object):

    def __init__(self,open_id,balance,env_value=True):

        self.open_id=open_id
        self.balance=balance
        self.db=DtdbOperations(env_value=env_value)


    def update_balance(self):

        sql='''UPDATE ditandaka.wx_user_info SET total_tjf={} ,balance_tjf={} WHERE
            open_id= '{}' '''.format(self.balance,self.balance,self.open_id)


        self.db.execute_sql(sql)

        self.db.mycommit()

        result= self.db.execute_sql(sql)

        if result==():

           return "数据更新成功!"

        else:
           return "数据更新失败"







if __name__=='__main__':

    minidd=Mini_add('o0hyf4lMU7CcdWQJLbF5NUcoDtco',3000,env_value=True)

    print minidd.update_balance()



