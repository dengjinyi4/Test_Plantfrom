# encoding=utf-8
__author__ = 'aidinghua'

import sys
import datetime
import time

from utils.db_info import  *

from openpyxl import Workbook


class Ocpa_try(object):

    def __init__(self,begin_time,ad_order_id,env_value=False):

        self.begin_time = begin_time

        self.ad_order_id = ad_order_id

        self.db= DbOperations(env_value=env_value)


###查询ocpa订单试投明细

    def ocpa_try(self):

        sql = '''
              SELECT
              try_day 日期,
              adzone_id 广告位id,
              ad_order_id 广告订单id,
              show_num 广告展现量,
              click_num 广告点击量,
              round(consume/100,2) 消耗,
              eff_num 效果数,
              case
              when state = '1' then '试投中'
              when state = '2' Then '未知'
              WHEN state = '3' Then '被过滤结束'
              When state = '4' Then '成功'
              WHen state = '5' Then '失败'
              END  状态
              FROM
              voyager.ocpa_try_log
              WHERE try_day = '{}'
              AND ad_order_id = {}

              '''.format(self.begin_time,self.ad_order_id)

        result = self.db.execute_sql(sql)

        return result


##查询订单试投总消耗
    def try_consum(self):

        sql='''
             select
             round(SUM(consume) / 100, 2)
             From
             voyager.ocpa_try_log
             where try_day = '{}'
             AND ad_order_id = {}
            '''.format(self.begin_time,self.ad_order_id)


        result = self.db.execute_sql(sql)[0][0]

        return result

######查询订单试投总消耗占所有数据上报广告主订单的百分比

     # def try_percent(self):














Oc=Ocpa_try('2019-03-13',27010,False)

print Oc.ocpa_try()
print Oc.try_consum()
