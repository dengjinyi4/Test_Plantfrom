# encoding=utf-8
__author__ = 'aidinghua'

import sys
import datetime
import time
import json
from openpyxl import Workbook
from utils.db_info import *

class Crm_order(object):

    def __init__(self,begin_time,end_time,env_value=False):

        self.db=DbOperations(env_value=env_value)
        self.begin_time=begin_time
        self.end_time=end_time


    def show_result(self):

        showsql = r"""SELECT
        a.*,
        b.adclick_num,
        CONCAT(
        TRUNCATE(
        a.提交订单数/b.adclick_num * 1000,
        2
        ),
        '‰'
        )

        FROM
        (SELECT
        t.日期,
        t.提交订单数,
        t.商品数量,
        0 + CAST(t.销售额 AS CHAR),
        t.待出库订单数,
        t.出库订单数,
        0 + CAST(t.出库销售额 AS CHAR),
        CONCAT(
        TRUNCATE(
        t.出库订单数 / t.提交订单数 * 100,
        2
        ),'%'
        ),
        t.签收订单数,
        t.无效订单数,
        CONCAT(
        TRUNCATE(
        t.无效订单数 / t.提交订单数 * 100,
        2
        ),
        '%'
        )
        FROM
        (SELECT
        DATE_FORMAT(order_time, '%Y%m%d') 日期,
        COUNT(id) 提交订单数,
        SUM(product_num) `商品数量`,
        SUM(order_amount / 100) `销售额`,
        SUM(
        CASE
          WHEN state = 0
          THEN 1
          ELSE 0
        END) `待出库订单数`,
        SUM(
        CASE
          WHEN state IN (1, 2, 4)
          THEN 1
          ELSE 0
        END
        ) `出库订单数`,
        SUM(
        CASE
          WHEN state IN (1, 2, 4)
          THEN order_amount / 100
          ELSE 0
        END
        ) `出库销售额`,
        SUM(
        CASE
          WHEN state = 2
          THEN 1
          ELSE 0
        END) 签收订单数,
        SUM(
        CASE
          WHEN state IN (5, 6)
          THEN 1
          ELSE 0
        END
        ) 无效订单数
        FROM
        crm_order
        WHERE order_time >= {}
        AND order_time < {}
        GROUP BY DATE_FORMAT(order_time, '%Y%m%d')
        ORDER BY DATE_FORMAT(order_time, '%Y%m%d') DESC) t) a,
        (SELECT
        a.date,
        SUM(a.adclick_num) adclick_num
        FROM
        voyager.report_order a,
        (SELECT
        DATE_FORMAT(order_time, '%Y%m%d') order_time,
        m.ad_order_id
        FROM
        voyager.`crm_order` m
        WHERE m.order_time >= {}
        AND m.order_time < {}
        GROUP BY DATE_FORMAT(order_time, '%Y%m%d'),
        m.ad_order_id) b
        WHERE a.date = b.order_time
        AND a.adorder_id = b.ad_order_id
        GROUP BY a.date) b WHERE a.日期 = b.date  """.format(self.begin_time,self.end_time,self.begin_time,self.end_time)

        result = self.db.execute_sql(showsql)

        if len(result)>0:

            self.exportXls(result)

        return  result
        
    def exportXls(self,result):

        if len(str(result)) > 0 :
            result = list(result)

            result.insert(0,('日期','提交订单数','商品数量','销售额','待出库订单数','出库订单数','出库销售额','出库率','签收订单数','无效订单数','无效率','广告点击数','订单转化率'))

            row = len(result)

            wb = Workbook()

            sheet = wb.active

            for i in range(row):

                sheet.append(result[i])

            wb.save("../crm_order.xlsx")
     

    def manage_result(self):

        result=str(self.show_result())

        rowlen = len(result)
        print rowlen

        final_review=[]
        for row in range(rowlen):

            col_len=len(result[row])
            rowlist=[]
            for col in range(col_len):
                rowlist.append(result[row][col])

            final_review.append(rowlist)

        return final_review



if __name__=='__main__':

    re=Crm_order(20180801,20180820)

    print re.show_result()
    # print re.manage_result()












