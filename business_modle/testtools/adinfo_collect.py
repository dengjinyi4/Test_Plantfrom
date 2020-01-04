# encoding=utf-8
__author__ = 'aidinghua'

import requests
import json
import datetime
import time
import random
import string
from utils import db_info

class Advertiser_collect(object):

    def __init__(self,ad_link,env_value=False):

        self.ad_link=ad_link
        self.db = db_info.DbOperations(env_value=env_value)


    def date(self):

        date=time.strftime("%Y%m%d", time.localtime())

        return date
    def get_month(self):

       mon = datetime.datetime.now().month

       if  mon<10:
        return "0"+str(mon)
       else:
        return str(mon)

    def click_tag(self):

        show_sql1=r"""
        SELECT
        ad_click_tag
        FROM
        voyagerlog.ad_click_log{}
        where adzone_id =4620 ORDER BY RAND() LIMIT 1 """.format(self.date())
        result1 = self.db.execute_sql(show_sql1)[0][0]
        return  result1

    def query_result(self,ad_click_tag):
        show_sql2=r"""
        SELECT
        ad_click_tag,
        type,
        uid,
        adzone_id,
        media_id,
        advertiser_id,
        ad_order_id,
        create_time
        FROM
        voyagerlog.ad_effect_log_{}
        WHERE ad_click_tag ='{}'""".format(self.get_month(),ad_click_tag)

        result2= self.db.execute_sql(show_sql2)

        return  result2

    #
    # def show_result(self):
    #
    #     show_sql2=r"""
    #     SELECT
    #     ad_click_tag,
    #     uid,
    #     adzone_id,
    #     media_id,
    #     advertiser_id,
    #     ad_order_id,
    #     create_time
    #     FROM
    #     voyagerlog.ad_effect_log_{}
    #     WHERE ad_click_tag ='{}'""".format(self.get_month(),self.click_tag())
    #
    #     result2= self.db.execute_sql(show_sql2)
    #
    #     return  result2



if  __name__=='__main__':

    advertiser_result=Advertiser_collect("https://rx.ad.haolints.com/101253/index.html",env_value=False)

    print advertiser_result.click_tag()
    # print advertiser_result.query_result('E0H2UD9T1JMWOPZPTT')




























