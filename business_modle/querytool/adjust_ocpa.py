# encoding=utf-8
__author__ = 'aidinghua'


from utils.db_info import *
# from EBG_Test_Plantfrom.utils import  db_info

import datetime

import time

class adjust_price(object):

    def __init__(self,day,ad_order_id,env_value=False,adzone_id=0):
        self.day=day
        self.ad_order_id=ad_order_id
        self.adzone_id=adzone_id
        self.db=DbOperations(env_value=env_value)


##返回这一天中这个广告订单的调价时间段

    def inittime(self):


         sql_time=''' SELECT create_time FROM voyager.ocpa_adjust_log  WHERE ad_order_id = {} and adzone_id={} AND adjust_day= '{}' ORDER BY create_time limit 1 '''.format(self.ad_order_id,self.adzone_id,self.day)

         result = self.db.execute_sql(sql_time)

         return str(result[0][0])


    def timelist(self):


         sql_len='''SELECT count(1) FROM voyager.ocpa_adjust_log  WHERE ad_order_id = {} and adzone_id={} AND adjust_day= '{}' '''.format(self.ad_order_id,self.adzone_id,self.day)
         time_len=self.db.execute_sql(sql_len)
         lenlen=int(time_len[0][0])
         sql_time=''' SELECT create_time FROM voyager.ocpa_adjust_log  WHERE ad_order_id = {} and adzone_id = {} AND adjust_day= '{}' ORDER BY create_time '''.format(self.ad_order_id,self.adzone_id,self.day)
         result = self.db.execute_sql(sql_time)
         timelist_data=[]
         if lenlen>0:
          for i in range(0,lenlen):
            timelist_data.append(str(result[i][0]))
          timelist_data.insert(0,self.inittime())
         else:
            timelist_data.append('0')
         return  timelist_data




    ##返回这一天中这个广告订单的初始OCPA价格

    def init_price(self):

        sql_init='''SELECT payment FROM voyager.ocpa_adjust_log  WHERE ad_order_id = {} and adzone_id = {} AND adjust_day= '{}'ORDER BY create_time limit 1 '''.format(self.ad_order_id,self.adzone_id,self.day)

        result = self.db.execute_sql(sql_init)

        if result <>():
            result_fal=(result[0][0]/100.00)
        else:
            result_fal=0
        return result_fal

        #
        #    result_fal=(result[0][0]/100.00)
        # else:
        #     result_fal=0
        # return result_fal

##返回这一天中这个广告订单的实际OCPA消耗初始值

    def init_actpaymet(self):
        sql_init='''SELECT actual_payment FROM voyager.ocpa_adjust_log  WHERE ad_order_id = {} and adzone_id ={} AND adjust_day= '{}'ORDER BY create_time limit 1 '''.format(self.ad_order_id,self.adzone_id,self.day)
        result = self.db.execute_sql(sql_init)
        if result<>():

            result_fal=(result[0][0]/100.00)
        else:
            result_fal=0
        return result_fal




##返回这一天中这个广告订单的OCPA调价
    def adjust_ocpa(self):

        sql_len='''SELECT count(1) FROM voyager.ocpa_adjust_log  WHERE ad_order_id = {} and adzone_id={} AND adjust_day= '{}' ORDER BY create_time '''.format(self.ad_order_id,self.adzone_id , self.day)
        time_len=self.db.execute_sql(sql_len)
        lenlen=int(time_len[0][0])
        sql_price='''SELECT adjust_payment FROM voyager.ocpa_adjust_log  WHERE ad_order_id = {} and adzone_id = {} AND adjust_day= '{}' ORDER BY create_time '''.format(self.ad_order_id,self.adzone_id,self.day)
        result=self.db.execute_sql(sql_price)
        pricelist=[]
        if lenlen>0:
          for i in range(0,lenlen):

            pricelist.append(result[i][0]/100.00)
          pricelist.insert(0,self.init_price())

        else:
            pricelist.append(0)
        return pricelist

##返回这一天中这个广告订单的OCPA实际消耗

    def actual_payment(self):

         sql_len='''SELECT count(1) FROM voyager.ocpa_adjust_log  WHERE ad_order_id = {} and adzone_id = {} AND adjust_day= '{}'  ORDER BY create_time '''.format(self.ad_order_id,self.adzone_id,self.day)
         actual_len=self.db.execute_sql(sql_len)
         lenlen = int(actual_len[0][0])
         sql_payment='''SELECT actual_payment FROM voyager.ocpa_adjust_log  WHERE ad_order_id = {} and adzone_id = {} AND adjust_day= '{}' ORDER BY create_time '''.format(self.ad_order_id,self.adzone_id,self.day)
         result = self.db.execute_sql(sql_payment)
         paymentlist=[]
         if lenlen>0:
           for i in range(0,lenlen):

             paymentlist.append(result[i][0]/100.00)
           paymentlist.insert(0,self.init_actpaymet())
         else:
             paymentlist.append(0)


         return paymentlist


    def adzone(self):

        sql_len='''SELECT COUNT(DISTINCT adzone_id) FROM voyager.ocpa_adjust_log  WHERE ad_order_id = {} AND adjust_day= '{}'  ORDER BY create_time '''.format(self.ad_order_id,self.day)
        actual_len=self.db.execute_sql(sql_len)
        lenlen = int(actual_len[0][0])
        sql_adzone='''SELECT DISTINCT adzone_id  FROM `ocpa_adjust_log` WHERE  ad_order_id = {} AND adjust_day= '{}'  ORDER BY create_time '''.format(self.ad_order_id,self.day)

        result=self.db.execute_sql(sql_adzone)
        adzonelist=[]

        if lenlen>0:
           for i in range(1,lenlen):


              adzonelist.append(int(result[i][0]))



        else:

              adzonelist.append(0)

        return adzonelist
    def shownum(self):

        sql_show='''SELECT count(1) FROM voyager.ocpa_adjust_log  WHERE ad_order_id = {} and adzone_id = {} AND adjust_day= '{}'  ORDER BY create_time '''.format(self.ad_order_id,self.adzone_id,self.day)
        actual_len=self.db.execute_sql(sql_show)
        lenlen = int(actual_len[0][0])
        sql_num='''SELECT show_num FROM voyager.ocpa_adjust_log  WHERE ad_order_id = {} and adzone_id = {} AND adjust_day= '{}' ORDER BY create_time '''.format(self.ad_order_id,self.adzone_id,self.day)
        result = self.db.execute_sql(sql_num)
        showlist=[]
        if lenlen>0:
            for i in range(0,lenlen):

                showlist.append(int(result[i][0]))
            showlist.insert(0,int(result[0][0]))
        else:
            showlist.append(0)


        return showlist






if  __name__=='__main__':

    adjust=adjust_price('2018-12-04',19795,False)
    print adjust.timelist()
#    print adjust.inittime()
    print adjust.actual_payment()
    print adjust.adjust_ocpa()
    print adjust.adzone()
    print adjust.shownum()





