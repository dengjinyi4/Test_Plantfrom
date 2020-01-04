# encoding=utf-8
__author__ = 'aidinghua'

import requests
from utils.db_info import  *
import time

import json
class checkurl(object):

    def __init__(self,env_value=False):

        self.db=DbOperations(env_value=env_value)


######返回当前日期

    def cur_date(self):

        cur = time.strftime("%Y-%m-%d",time.localtime())

        return cur


    ######获取创意的条数

    def len_creative(self):

        sql =''' SELECT COUNT(DISTINCT link_common) FROM voyager.ad_creative_link WHERE is_valid = 1 AND creative_id IN (SELECT creative_id FROM voyager.report_order WHERE DATE = '{}')'''.format(checkurl().cur_date())

        len= self.db.execute_sql(sql)[0][0]

        return int(len)

    #####获取创意链接
    def creativelist(self):

        crlist = []

        sql =''' SELECT DISTINCT link_common FROM voyager.ad_creative_link WHERE is_valid = 1 AND creative_id IN (SELECT creative_id FROM voyager.report_order WHERE DATE = '{}')'''.format(checkurl().cur_date())
        len = checkurl().len_creative()
        for i in range(len):
            result  = self.db.execute_sql(sql)[i][0]

            print result

            crlist.append(str(result))


        return crlist






    ##调用链接查看创意是否被封
    def check(self):


        url='http://vip.weixin139.com/weixin/1810472189.php?'
        list = checkurl().creativelist()
        len  =checkurl().len_creative()
        checklist=[]
        for i in range(len):
            paragram={'domain':list[i]}
            result = requests.get(url,params=paragram)
            re= json.loads(result.content)
            # print re
            #
            # print re['status']
            # print type(re['status'])
            #
            # print re['domain']

            if int(re['status'])==2:
                # checklist.append(str(result.content))
                checklist.append(str(re['domain']))


        return checklist



    def len_check(self):


        url='http://vip.weixin139.com/weixin/1810472189.php?'
        list = checkurl().creativelist()
        len  =checkurl().len_creative()
        checklist=[]
        for i in range(len):
            paragram={'domain':list[i]}
            result = requests.get(url,params=paragram)
            re= json.loads(result.content)
            # print re

            # print re['status']
            #
            # print re['domain']

            if int(re['status'])==2:
                # checklist.append(str(result.content))
                checklist.append(str(re['domain']))


        return len(checklist)


if __name__=='__main__':

    ck = checkurl(False)

    print ck.check()

    # print ck.len_check()

    # print ck.len_creative()

