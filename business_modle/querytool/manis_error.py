# encoding=utf-8
__author__ = 'aidinghua'

import time
from utils.db_info import *
from openpyxl import  Workbook
class Manis_error(object):

    def __init__(self,begin_date,env_value=False):

        self.db=DbOperations(env_value=env_value)
        self.begin_date=begin_date



    def show_result(self):

        sql=''' SELECT date(a.create_time) 日期,
              a.adzone_id 广告位ID,
              c.adzone_name 广告位名称,
              a.media_id 媒体ID,
              b.name 媒体名称,
              a.video_play_error 穿山甲视频错误,
              COUNT(1) 数量
            FROM
              voyagerlog.sdk_detail_log{} a
              left join voyager.base_media_info b on a.media_id = b.id
              left join voyager.base_adzone_info c on a.adzone_id = c.id
            WHERE a.video_play_error IS NOT NULL
              AND a.ad_order_id IN
              (SELECT
                id
              FROM
                voyager.`ad_order`
              WHERE state = 4
                AND advertiser_id = 6015)
            GROUP BY date(a.create_time),a.adzone_id,c.adzone_name,a.media_id,b.name,a.video_play_error '''.format(self.begin_date)
        result = self.db.execute_sql(sql)
        if result<>():
            self.export_xls(result)

        return result

    def export_xls(self,result):

        if len(str(result))>0:
            result = list(result)
            result.insert(0,('日期','广告位ID','广告位名称','媒体ID','媒体名称','穿山甲视频错误','数量'))
            row=len(result)
            wb=Workbook()
            sheet=wb.active

            for i in range(row):

                sheet.append(result[i])

            wb.save("./static/result/manis_error.xlsx")


if __name__=='__main__':

    Me=Manis_error('2020-10-28',False)
    re=Me.show_result()
    print re
