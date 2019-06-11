# encoding=utf-8
__author__ = 'aidinghua'
import time
from utils.db_info import  *

from openpyxl import  Workbook

class Report_byadzone(object):

    def __init__(self,adzone_id,begin_date,env_value=False):

        self.db=DbOperations(env_value=env_value)

        self.adzone_id = adzone_id

        self.begin_date= begin_date






    def show_result(self):

        sql = '''SELECT
        DATE 日期,
        HOUR 小时,
        adzone_id 广告位ID,
        adzone_effect_num 广告位点击数,
        show_num 广告展现数,
        adclick_num 广告点击数,
        CONCAT(TRUNCATE(( (adclick_num)/(adzone_effect_num) ) * 100, 2), '%') 广告导出率,
        ROUND(adzone_consume / 100, 2) 小时消耗,
        ROUND(
            (adzone_consume / 100) / adclick_num,
            2
        ) 均价
        FROM
        voyager.`report_zone_hour`
        WHERE adzone_id = {}
        AND DATE = '{}' '''.format(self.adzone_id,self.begin_date)

        result = self.db.execute_sql(sql)

        if result<>():

            self.export_xls(result)

        return result

    def show_result2(self):


        sql='''
         SELECT
        DATE 日期,
        HOUR 小时,
        0 广告位ID,
        SUM(adzone_effect_num) 广告位点击数,
        SUM(show_num) 广告展现数,
        SUM(adclick_num) 广告点击数,
        CONCAT(TRUNCATE(( SUM(adclick_num)/SUM(adzone_effect_num) ) * 100, 2), '%') 广告导出率,

        SUM(ROUND(adzone_consume / 100, 2)) 小时消耗,
        ROUND((SUM(adzone_consume) / 100) / SUM(adclick_num),2) 均价

        FROM
        voyager.report_zone_hour
        WHERE
          DATE = '{}' GROUP BY DATE,HOUR '''.format(self.begin_date)
        result = self.db.execute_sql(sql)

        if result<>():

            self.export_xls(result)

        return result



    def export_xls(self,result):

        if len(str(result))>0:
            result = list(result)
            result.insert(0,('日期','小时','广告位ID','广告位点击数','广告展现数','广告点击数','广告导出率','小时消耗','均价'))
            row=len(result)
            wb=Workbook()
            sheet=wb.active

            for i in range(row):

                sheet.append(result[i])

            wb.save("./static/result/report_byadzone.xlsx")








if __name__=='__main__':

 Rb=Report_byadzone('3105','2019-05-24',False)

 # print Rb.show_result()
 print Rb.show_result2()

