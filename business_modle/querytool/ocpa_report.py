# encoding=utf-8
__author__ = 'aidinghua'
import datetime
import sys

from utils.db_info import *
from openpyxl import  Workbook

class Ocpa_report(object):

    def __init__(self,begin_date,end_date,env_value=False):

        self.db=DbOperations(env_value=env_value)
        self.begin_date=begin_date
        self.end_date=end_date



    def show_result(self):

        sql= '''SELECT
              a.date AS '日期',
              #      a.industry_id AS '行业类型id',
              #      a.name  AS '行业',
              SUM(a.num) AS '总效果数',
              COUNT(DISTINCT (a.advertiser_id)) AS '总广告主个数',
              SUM(b.consume) AS '总广告消耗',
              SUM(b.ocpa_effect_num) AS 'OCPA效果数',
              SUM(b.ocpa_consume) AS 'OCPA订单消耗',
              SUM(b.consume) - SUM(b.ocpa_consume) AS 'CPC订单消耗',
              CONCAT(
                TRUNCATE(
                  (SUM(b.ocpa_consume) / SUM(b.consume)) * 100,
                  2
                ),
                '%'
              ) 'OCPA消耗占比',
              c.ocpa_adv_num AS 'OCPA广告主个数' #c.effect_consume as '数据上报的消耗'
            FROM
              (SELECT
                c.date,
                c.`advertiser_id`,
                c.adv_industry_id industry_id,
                d.name,
                SUM(c.effect_num) num
              FROM
                voyager.report_effect c,
                voyager.industry d
              WHERE c.date >= '{}'
                AND d.id <> 43
                AND c.date <= '{}'
                AND c.adv_industry_id IS NOT NULL
                AND c.adv_industry_id = d.id
              GROUP BY industry_id,
                advertiser_id,
                c.date) a
              LEFT JOIN
                (SELECT
                  e.date,
                  e.advertiser_id,
                  ROUND(SUM(e.ad_consume) / 100, 2) consume,
                  SUM(e.ocpa_effect_num) ocpa_effect_num,
                  ROUND(SUM(e.ocpa_consume) / 100, 2) ocpa_consume
                FROM
                  voyager.report_order e
                  LEFT JOIN voyager.ad_order p  ON e.adorder_id=p.id
                WHERE e.date >= '{}'
                  AND p.ocpa_ext_order<>1
                  AND e.advertiser_id <> 4014
                  AND e.date <= '{}'
                GROUP BY e.advertiser_id,
                  e.date) b
                ON a.advertiser_id = b.advertiser_id
                AND a.date = b.date
              LEFT JOIN
                (SELECT
                  c.date,
                  c.adv_industry_id industry_id,
                  COUNT(DISTINCT c.`advertiser_id`) ocpa_adv_num,
                  ROUND(SUM(c.consume) / 100, 2) effect_consume
                FROM
                  voyager.report_effect c
                WHERE c.date >= '{}'
                  AND c.date <= '{}'
                  AND c.adv_industry_id IS NOT NULL
                  AND c.payment_mode = 4
                GROUP BY adv_industry_id,
                  c.date) c
                ON a.industry_id = c.industry_id
                AND a.date = c.date
            GROUP BY a.date
            ORDER BY a.date DESC #,a.industry_id'''.format(self.begin_date,self.end_date,self.begin_date,self.end_date,self.begin_date,self.end_date)

        result = self.db.execute_sql(sql)

        if result<>():

            self.exportXls(result)

        return result


    def exportXls(self,result):

        if len(str(result)) > 0 :

            result = list(result)

            result.insert(0,('日期','总效果数','总广告主个数','总广告消耗','OCPA效果数','OCPA订单消耗','CPC订单消耗','OCPA消耗占比','OCPA广告主个数'))

            row = len(result)

            wb = Workbook()
            sheet = wb.active

            for i in range(row):

                sheet.append(result[i])

            # wb.save("../../templates/ocpa_order.xlsx")

            wb.save("./static/result/ocpa_report.xlsx")



if __name__=='__main__':


    OR=Ocpa_report('2019-05-01','2019-05-05',env_value=False)

    print OR.show_result()












