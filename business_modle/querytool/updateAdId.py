# encoding=utf-8
__author__ = 'aidinghua'

import sys
import datetime
from utils.db_info import *

class updateAdId(object):
    reload(sys)
    sys.setdefaultencoding('utf-8')
    def __init__(self,BeforeAdID,AfterAdID):
        self.db= DbOperations()
        self.beforeAd=BeforeAdID
        self.afterAd=AfterAdID
#更新advertiser表,advertiser_account表,advertiser_credentials表
    def udpate(self):
        up_sql="UPDATE `advertiser` SET id ="+str(self.afterAd)+ ",password='d0dcbf0d12a6b1e7fbfa2ce5848f3eff'WHERE id ="+str(self.beforeAd)
        up_result=self.db.execute_sql(up_sql)
        upAccount_sql="UPDATE advertiser_account SET advertiser_id ="+str(self.afterAd) +",cash_total_amount=1000000,cash_balance=1000000 WHERE advertiser_id= "+str(self.beforeAd)
        upAccount_result=self.db.execute_sql(upAccount_sql)
        upCre_sql= "UPDATE advertiser_credentials SET advertiser_id="+str(self.afterAd) +" WHERE advertiser_id= "+str(self.beforeAd)
        upCre_result=self.db.execute_sql(upCre_sql)
        print up_sql
        print upAccount_sql
        print upCre_sql
        return up_result
        return upAccount_result
        return upCre_result
#查询更新结果
    def select(self):
        seA_sql="select count(1) from advertiser where id="+str(self.afterAd)
        seB_sql="select count(1) from advertiser where id="+str(self.beforeAd)
        seAccount_sql="select count(1) from advertiser_account where advertiser_id="+str(self.afterAd)
        seCre_sql="select count(1) from advertiser_credentials where advertiser_id="+str(self.afterAd)
        seA_result=self.db.execute_sql(seA_sql)
        seB_result=self.db.execute_sql(seB_sql)
        seAccount_result=self.db.execute_sql(seAccount_sql)
        seCre_result=self.db.execute_sql(seCre_sql)
        print seA_result[0][0]
        print seB_result[0][0]
        print seAccount_result[0][0]
        print seCre_result[0][0]
        if int(seA_result[0][0])==1 and int(seB_result[0][0])==0 and int(seAccount_result[0][0])==1 and int(seCre_result[0][0])>=1:
            return "全部更新成功"
        elif int(seA_result[0][0])==0:
            return "advertiser表更新失败"
        elif int(seAccount_result[0][0])==0:
            return "advertiser_account表更新失败"
        elif int (seCre_result[0][0])==0:
            return "advertiser_credentials表更新失败"
        else:
            return "其他情况更新失败"
    def __del__(self):
        self.db.close_cursor()
        self.db.close_db()

if "__main__"==__name__:
    ua=updateAdId(888,5)
    ua.udpate()
    print ua.select()




