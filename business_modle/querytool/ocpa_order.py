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

    def today(self):

        return datetime.datetime.now().strftime("%Y%m%d")


    def show_result(self):

        show_sql ='''SELECT
        a.date 日期,
        a.adorder_id ocpa订单id,
        CONVERT(a.ad_withhold/ 100, DECIMAL(10, 0)) ocpa订单预扣,
        c.name 订单所属广告主名称, 
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
        FROM voyager.report_order a, voyager.ad_order b,voyager.advertiser c
        WHERE  a.adorder_id = b.id AND b.advertiser_id = c.id AND a.DATE = '{}' AND a.adorder_id IN (SELECT id FROM ad_order WHERE payment_mode = 4)'''.format(self.begin_time)


        result=self.db.execute_sql(show_sql)

        if result<>():

            self.exportXls(result)

        return result

    ###查询ocpa订单今日试投总消耗

    def ocpa_alltry(self):

        sql='''
              SELECT
              ROUND(SUM(consume) / 100, 2)
              FROM
              voyager.ocpa_try_log
              WHERE try_day = '{}'
            '''.format(self.begin_time)

        result = self.db.execute_sql(sql)[0][0]

        return result


    def ocpa_consumer(self):

        sql='''
             SELECT
            SUM(f.OCPA订单消耗) OCPA订单总消耗
            FROM
            (SELECT
            a.industry_id AS '行业类型id',
            a.name AS '行业',
            SUM(a.num) AS '总效果数',
            COUNT(DISTINCT (a.advertiser_id)) AS '总广告主个数',
            SUM(b.consume) AS '总广告消耗',
            SUM(b.ocpa_effect_num) AS 'OCPA效果数',
            SUM(b.ocpa_consume) AS 'OCPA订单消耗',
            c.ocpa_adv_num AS 'OCPA广告主个数'
           FROM
            (SELECT
              c.`advertiser_id`,
              c.adv_industry_id industry_id,
              d.name,
              SUM(c.effect_num) num
            FROM
              voyager.report_effect c,
              voyager.industry d
            WHERE c.date >= '{}'
              AND d.id <> 43
              AND c.date < ADDDATE('{}', INTERVAL 1 DAY)
              AND c.adv_industry_id IS NOT NULL
              AND c.adv_industry_id = d.id
            GROUP BY industry_id,
              advertiser_id) a
            LEFT JOIN
              (SELECT
                e.advertiser_id,
                ROUND(SUM(e.ad_consume) / 100, 2) consume,
                SUM(e.ocpa_effect_num) ocpa_effect_num,
                ROUND(SUM(e.ocpa_consume) / 100, 2) ocpa_consume
              FROM
                voyager.report_order e
              WHERE e.date >= '{}'
                AND e.date < ADDDATE('{}', INTERVAL 1 DAY)
              GROUP BY e.advertiser_id) b
              ON a.advertiser_id = b.advertiser_id
            LEFT JOIN
              (SELECT
                c.adv_industry_id industry_id,
                COUNT(DISTINCT c.`advertiser_id`) ocpa_adv_num
              FROM
                voyager.report_effect c
              WHERE c.date >= '{}'
                AND c.date < ADDDATE('{}', INTERVAL 1 DAY)
                AND c.adv_industry_id IS NOT NULL
                AND c.payment_mode = 4
              GROUP BY adv_industry_id) c
              ON a.industry_id = c.industry_id
          GROUP BY a.industry_id) f '''.format(self.begin_time,self.begin_time,self.begin_time,self.begin_time,self.begin_time,self.begin_time)

        result = self.db.execute_sql(sql)[0][0]

        return result

    ###查询ocpa订单消耗占 数据上报广告主总订单消耗的百分比


    def ocpa_percent(self):

        sql= '''
                SELECT
                  CONCAT(
                    TRUNCATE(
                      (
                        SUM(f.OCPA订单消耗) / SUM(f.总广告消耗)
                      ) * 100,
                      2
                    ),
                    '%'
                  ) OCPA订单消耗占比
                FROM
                  (SELECT
                    a.industry_id AS '行业类型id',
                    a.name AS '行业',
                    SUM(a.num) AS '总效果数',
                    COUNT(DISTINCT (a.advertiser_id)) AS '总广告主个数',
                    SUM(b.consume) AS '总广告消耗',
                    SUM(b.ocpa_effect_num) AS 'OCPA效果数',
                    SUM(b.ocpa_consume) AS 'OCPA订单消耗',
                    c.ocpa_adv_num AS 'OCPA广告主个数'
                  FROM
                    (SELECT
                      c.`advertiser_id`,
                      c.adv_industry_id industry_id,
                      d.name,
                      SUM(c.effect_num) num
                    FROM
                      voyager.report_effect c,
                      voyager.industry d
                    WHERE c.date >= '{}'
                      AND d.id <> 43
                      AND c.date < ADDDATE('{}', INTERVAL 1 DAY)
                      AND c.adv_industry_id IS NOT NULL
                      AND c.adv_industry_id = d.id
                    GROUP BY industry_id,
                      advertiser_id) a
                    LEFT JOIN
                      (SELECT
                        e.advertiser_id,
                        ROUND(SUM(e.ad_consume) / 100, 2) consume,
                        SUM(e.ocpa_effect_num) ocpa_effect_num,
                        ROUND(SUM(e.ocpa_consume) / 100, 2) ocpa_consume
                      FROM
                        voyager.report_order e
                      WHERE e.date >= '{}'
                        AND e.advertiser_id<>4014
                        AND e.date < ADDDATE('{}', INTERVAL 1 DAY)
                      GROUP BY e.advertiser_id) b
                      ON a.advertiser_id = b.advertiser_id
                    LEFT JOIN
                      (SELECT
                        c.adv_industry_id industry_id,
                        COUNT(DISTINCT c.`advertiser_id`) ocpa_adv_num
                      FROM
                        voyager.report_effect c
                      WHERE c.date >= '{}'
                        AND c.date < ADDDATE('{}', INTERVAL 1 DAY)
                        AND c.adv_industry_id IS NOT NULL
                        AND c.payment_mode = 4
                      GROUP BY adv_industry_id) c
                      ON a.industry_id = c.industry_id
                  GROUP BY a.industry_id) f '''.format(self.begin_time,self.begin_time,self.begin_time,self.begin_time,self.begin_time,self.begin_time)
        result=self.db.execute_sql(sql)[0][0]

        return result

    def exportXls(self,result):

        if len(str(result)) > 0 :

            result = list(result)

            result.insert(0,('日期','ocpa订单id','ocpa订单预扣','订单所属广告主','ocpa订单状态','ocpa展现次数','ocpa点击次数','ocpa消耗','ocpa消耗比例','ocpa效果数','实际效果消耗','预期效果消耗','效果偏差','消耗偏差百分比'))

            row = len(result)

            wb = Workbook()
            sheet = wb.active

            for i in range(row):

                sheet.append(result[i])

            # wb.save("../../templates/ocpa_order.xlsx")

            wb.save("./static/result/ocpa_order.xlsx")



            # wb.save(os.path.join("../../","templates/ocpa_order.xlsx"))
            # wb.save("./ocpa_order.xlsx")

Oc=Ocpa_order('2019-03-02',True)

print Oc.cur_date()
