# encoding=utf-8
__author__ = 'aidinghua'

import time
from utils.db_info import *

from openpyxl import  Workbook
class Ttpt_errorlog(object):

    def __init__(self,begin_date,env_value):

        self.db=DbOperations(env_value=env_value)

        self.begin_date=begin_date


    def show_result(self):

        sql='''
          SELECT
          user_id 用户ID,
          adzone_id 广告位ID,
          platform_id 平台ID,
          message 错误信息,
          create_time 产生时间
          FROM
          voyager.thpt_error_log
          WHERE DATE(create_time) = '{}' order by create_time desc '''.format(self.begin_date)

        result=self.db.execute_sql(sql)

        print result

        if result<>():

            self.export_xls(result)

        return result

    def show2_result(self):
        sql='''
          SELECT
          user_id 用户ID,
          adzone_id 广告位ID,
          platform_id 平台ID,
          message 错误信息,
          create_time 产生时间
          FROM
          voyager.sbs_error_log
          WHERE DATE(create_time) = '{}' ORDER BY create_time DESC'''.format(self.begin_date)

        result = self.db.execute_sql(sql)

        print result
        if result<>():
            self.export_xls(result)
        return result



    def export_xls(self,result):

        if len(str(result))>0:
            result = list(result)

            result.insert(0,('用户ID','广告位ID','平台ID','错误信息','产生时间'))

            row =len(result)
            wb = Workbook()
            sheet = wb.active
            for i in range(row):

                sheet.append(result[i])
            wb.save("./static/result/ttpt_errorlog.xlsx")


if __name__=='__main__':

    Te=Ttpt_errorlog('2020-11-10',False)
    re=Te.show_result()
    re1=Te.show2_result()
    print re,re1


