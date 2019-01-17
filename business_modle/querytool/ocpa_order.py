# encoding=utf-8
__author__ = 'aidinghua'

import sys
import datetime
import time

from utils.db_info import * 

from openpyxl import  Workbook


class Ocpa_order(object):

    def __init__(self,begin_time,env_value=False):

        self.db = DbOperations(env_value=env_value)
        self.begin_time=begin_time

    def cur_date(self):


        return datetime.datetime.now().strftime("%Y-%m-%d")

    def show_result(self):

        show_sql ='''SELECT
        a.date 日期,
        a.adorder_id ocpa订单id,
        CONVERT(a.ad_withhold/ 100, DECIMAL(10, 0)) ocpa订单预扣,
        CASE WHEN b.state=4 THEN '投放中'
             WHEN b.state=5 THEN '暂停'
             ELSE  '其他状态'
        END  订单状态,
        a.show_num  ocpa展现次数,
        a.adclick_num ocpa点击次数,
        CONVERT(a.ocpa_consume / 100, DECIMAL(10, 2))
        ocpa消耗,
        CONCAT(TRUNCATE(((a.ocpa_consume / 100) / (a.ad_withhold/ 100)  ) * 100, 2), '%') ocpa消耗比例,
        a.ocpa_effect_num
        ocpa效果数,
        CONVERT(
            a.ocpa_consume / a.ocpa_effect_num / 100,
            DECIMAL(10, 2)
        )
        实际效果消耗,
        CONVERT(b.payment / 100, DECIMAL(10, 2))
        预期效果消耗,
        CONVERT(
            a.ocpa_consume / a.ocpa_effect_num / 100,
            DECIMAL(10, 2)
        ) - CONVERT(b.payment / 100, DECIMAL(10, 2))
        效果偏差,
        CONCAT(TRUNCATE(((a.ocpa_consume / a.ocpa_effect_num / 100 - b.payment / 100 ) / (b.payment / 100) ) * 100, 2), '%')
        消耗偏差百分比
        FROM voyager.report_order a, voyager.ad_order b
        WHERE a.adorder_id = b.id AND a.DATE = '{}' AND a.adorder_id IN (SELECT id FROM ad_order WHERE payment_mode = 4)'''.format(self.begin_time)


        result=self.db.execute_sql(show_sql)

        if result<>():

            self.exportXls(result)

        return result

    def exportXls(self,result):

        if len(str(result)) > 0 :

            result = list(result)

            result.insert(0,('日期','ocpa订单id','ocpa订单状态','ocpa展现次数','ocpa点击次数','ocpa消耗','ocpa效果数','实际效果消耗','预期效果消耗','效果偏差','消耗偏差百分比'))

            row = len(result)

            wb = Workbook()

            sheet = wb.active

            for i in range(row):

                sheet.append(result[i])

            wb.save("./ocpa_order.xlsx")

Oc=Ocpa_order('2018-11-01',True)

print Oc.cur_date()
print Oc.show_result()

