# encoding=utf-8
__author__ = 'aidinghua'

import sys
import datetime
import time
from utils import db_info

class Recharge(object):
    reload(sys)
    sys.setdefaultencoding('utf-8')

    def __init__(self,advertiser_id,amount):

        self.db=db_info.DbOperations()
        self.advertiser_id=advertiser_id
        self.amount=int(amount)*100

    def localtime(self):
        self.tick=time.time()
        self.systime= time.strftime("%Y-%m-%d %H:%M:%S",time.localtime())
        self.systime_hour=(datetime.datetime.now()+datetime.timedelta(hours=-1)).strftime("%Y-%m-%d %H:%M:%S")
        self.sysdate= time.strftime("%Y-%m-%d",time.localtime())
        return self.tick,self.systime,self.sysdate,self.systime_hour

    def balance(self):

        select_sql="SELECT cash_balance,cash_total_amount FROM advertiser_account where advertiser_id= "+str(self.advertiser_id)
        self.result=self.db.execute_sql(select_sql)
        self.balance_result=self.result[0][0]
        self.total_balance_result=self.result[0][1]
        return  int(self.balance_result) ,int(self.total_balance_result)
    def showreview(self):
        showsql="SELECT advertiser_id,recharge_amount/100,rebate_ratio,rebate_begin_time,rebate_end_time FROM `rebate_review_ratio` WHERE rebate_review_id IN( SELECT id FROM `rebate_review` WHERE STATUS=2 AND advertiser_id = 1789)"
        review_result=self.db.execute_sql(showsql)
        return review_result
        # self.advertiser_result=self.show[0][0]
        # self.recharge_amount=self.show[0][1]
        # self.rebate_ratio=self.show[0][2]
        # self.rebate_begin=self.show[0][3]
        # self.rebate_end=self.show[0][4]
#        return str(self.advertiser_result),str(self.recharge_amount),str(self.rebate_ratio),str(self.rebate_begin),str(self.rebate_end)
    def manage_review(self):


         review_result=self.showreview()

         rowlen = len(review_result)

         final_review=[]
         for row in range(rowlen):

             col_len=len(review_result[row])
             rowlist=[]
             for col in range(col_len):
                 rowlist.append(review_result[row][col])

             final_review.append(rowlist)

         return final_review



         # review_result=self.showreview()
         # raw_len=len(review_result)
         # final_review=[]
         # for row in range(raw_len):
         #
         #     col_len = len(review_result[row])
         #     row1ist=[]
         #     for col in range(col_len):
         #         row1ist.append(review_result[row][col])
         #     final_review.append(row1ist)
         #
         # return final_review


    def insert(self):

        del_sql="DELETE FROM advertiser_recharge_log WHERE advertiser_id = '{}'".format(self.advertiser_id)
        self.db.execute_sql(del_sql)
#        insert_sql1=r'''INSERT  INTO voyager.advertiser_balance_log ( `advertiser_id`, `ad_order_id`, `biz_no`, `descn`, `change_time`, `charge_back_status`, `amount`, `balance`, `total_balance`, `type`, `account_type`, `create_time`, `update_time`, `advertiser_type`, `recharge_method`, `available_balance`, `available_total_balance`) VALUES
#            ('{}',NULL,'201808021512075972222506','联动支付','{}','1','{}','{}','{}','1','1', '{}','{}','1','4','1','1');'''.format(self.advertiser_id,self.systime, self.amount,self.amount+self.balance_result,self.amount+self.total_balance_result,self.systime,self.systime)
#        print insert_sql1
#        self.db.execute_sql(insert_sql1)
#        insert_sql2=r"UPDATE voyager.advertiser_account SET cash_total_amount ='{}',cash_balance='{}'  WHERE advertiser_id = '{}'".format(self.total_balance_result +self.amount,self.balance_result+self.amount,self.advertiser_id)
#        print insert_sql2
#        self.db.execute_sql(insert_sql2)
#        insert_sql3=r"INSERT INTO voyager.um_advertiser_deal_log ( `advertiser_id`, `account_type`, `company_name`, `refunds_method`, `recharge_method`, `confirm_receipt_time`, `amount`, `remark`, `account_name`, `account_bank`, `account`, `create_time`, `operator`, `status`, `crm_no`, `account_status`, `refunds_type`, `refund_account`) VALUES('{}','1','亿玛在线',NULL,'4', '{}','{}',NULL,NULL,'CMB',NULL,'{}',NULL,'1','{}','1','1','0');".format(self.advertiser_id,self.systime,self.amount,self.systime,self.tick)
#        print insert_sql3
#        self.db.execute_sql(insert_sql3)
        insert_sql4=r"INSERT INTO voyager.advertiser_recharge_log ( `advertiser_id`, `buyer_id`, `total_amount`, `platform`, `egou_trade_no`, `platform_trade_no`, `passback_params`, `status`, `platform_trade_status`, `timeout_express`, `gmt_create`, `gmt_payment`, `create_time`, `update_time`, `pay_type`, `settle_date`, `pay_seq`, `error_code`, `gate_id`, `last_four_cardid`, `target`) VALUES('{}',NULL,'{}','umpay','20180721214045887001789','3807212140123536','{}','0','TRADE_SUCCESS','120h','2018-07-21 11:14:25','{}','{}','{}','B2CBANK','{}','9064999284',NULL,'CMB',NULL,'0');".format(self.advertiser_id,self.amount,self.amount,self.systime,self.systime_hour,self.systime,self.sysdate)
        print insert_sql4
        self.db.execute_sql(insert_sql4)
        return "联动模拟充值成功，请重启api.demand进程后查看返点奖励是否正确(也可以等待15分钟后定时任务自动执行)"



if __name__=="__main__":

    re=Recharge(2222509,1)
    # print re.localtime()
    # print re.balance()
    # print re.insert()
    print re.showreview()
    print re.manage_review()


