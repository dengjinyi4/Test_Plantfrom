# encoding=utf-8
__author__ = 'aidinghua'
from openpyxl import  Workbook
import time
import datetime
import  sys
import re
from utils.db_info import *

# 有练换换	wx0a051787252f83fa
# 步数大联盟	wxe65c34b4ec242be
# 优质福利所	wx3c48ef7a45e89118
# 易购赚	wx0a051787252f83fa
# 遇见球球 	wxbb67c77aea9d76a8
# 开心游戏大乱斗	wx2fa65dcf3dbe5926
# 十一光年	wx42d12a5790960727
# 福礼惠公众号	wx4ef839c292cb41ad
# 我蹦我再蹦	wx85d4b50441231b98
# 弹球大乱斗	wx4aab7ee381936b54
# 手机弹幕小程序 wx3fe2d608967de425


class Media_reportnew(object):

    def __init__(self,source_id,begin_date,end_date,env_value=False):

        self.dbinfo=DbOperations(env_value=env_value)
        self.begin_date=begin_date
        self.end_date=end_date
        self.source_id =source_id

    def begin_ym(self):

        begin_ym=self.begin_date[0:7]

        begin_ym1= begin_ym.replace('-','')
        return begin_ym1

    def end_ym(self):

        end_ym=self.end_date[0:7]
        end_ym1 = end_ym.replace('-','')
        return end_ym1



####勾选了新增留存

###媒体选择全部,日期选择单天

    def add_result(self):

        sql = '''
                  SELECT
                  a.date 日期,

                  '全部' 媒体 ,
                  SUM(a.new_user_num) 新用户数,
                  SUM(a.active_user_num) 活跃用户数,
                  SUM(a.authorize_nuser_num) 授权用户数,
                  CONCAT(TRUNCATE((SUM(a.day2_new_retain)/SUM(a.new_user_num) ) * 100, 2), '%')   新增次日留存率 ,
                  CONCAT(TRUNCATE((SUM(a.day3_new_retain)/SUM(a.new_user_num) ) * 100, 2), '%')   新增三日留存率 ,
                  CONCAT(TRUNCATE((SUM(a.day4_new_retain)/SUM(a.new_user_num)  ) * 100, 2), '%')   新增四日留存率 ,
                  CONCAT(TRUNCATE((SUM(a.day5_new_retain)/SUM(a.new_user_num)  ) * 100, 2), '%')   新增五日留存率 ,
                  CONCAT(TRUNCATE((SUM(a.day6_new_retain)/SUM(a.new_user_num)  ) * 100, 2), '%')   新增六日留存率 ,
                  CONCAT(TRUNCATE((SUM(a.day7_new_retain)/SUM(a.new_user_num)  ) * 100, 2), '%')   新增七日留存率
                  FROM
                  voyager.wx_user_report a WHERE

                  a.date>='{}' AND a.date <='{}'
                  GROUP BY a.date,媒体  ORDER BY  a.date DESC '''.format(self.begin_date,self.end_date)

        result =self.dbinfo.execute_sql(sql)

        if result<>():

           self.exportXlsadd(result)

        return result

    def add_result_one(self):

        sql = '''
                 SELECT
                  a.date 日期,

                  CASE
                  WHEN a.source_id='wx239bfcba6aeb0084' THEN '有练换换'
                  WHEN a.source_id='wxe65c34b4ec242be' THEN '步数大联盟'
                  WHEN a.source_id='wx3c48ef7a45e89118' THEN '优质福利所'
                  WHEN a.source_id='wx0a051787252f83fa' THEN '易购赚'
                  WHEN a.source_id='wxbb67c77aea9d76a8' THEN '遇见球球'
                  WHEN a.source_id='wx2fa65dcf3dbe5926' THEN '开心游戏大乱斗'
                  WHEN a.source_id='wx42d12a5790960727' THEN '十一光年'
                  WHEN a.source_id='wx4ef839c292cb41ad' THEN '福礼惠公众号'
                  WHEN a.source_id='wx85d4b50441231b98' THEN '我蹦我再蹦'
                  WHEN a.source_id='wx4aab7ee381936b54' THEN '弹球大乱斗'
                  WHEN a.source_id='1017757' THEN 'APP-DSP光速动力'
                  WHEN a.source_id='wx3fe2d608967de425'  THEN '手机弹幕小程序'
                  WHEN a.source_id='wx76dcd806f382ec8e' THEN '智行火车票小程序'
                  WHEN a.source_id='wxd8de2f6276406b2a' THEN '步数换换乐'
                  WHEN a.source_id='wx18a2d299d1482fc0' THEN '打卡小日历'
                  WHEN a.source_id='wxefda0ea3619d87eb'  THEN '玩赚签到'
                  WHEN a.source_id='880090' THEN '光微科技公众号'
                  WHEN a.source_id='582068' THEN '番茄小程序矩阵'
                  WHEN a.source_id='wxd949b04824167683' THEN '小麦圈打卡'
                  WHEN a.source_id='sanyan1017628' THEN '三言app'
                  WHEN a.source_id='wx9bda6799b29d7868' THEN '小集盒'
                  WHEN a.source_id='wx5325ee83f4181dab' THEN '超级打投'
                  WHEN a.source_id='tqoxinwen001' THEN '淘新闻'
                  WHEN a.source_id='1018004' THEN '付呗'
                  WHEN a.source_id='wx5c9a5ce20be8207b'  THEN '哆啦宝'
                  WHEN a.source_id='wxc79d91f3a01dcd31'  THEN '今天点餐吃什么'
                  WHEN a.source_id='wxb09486b4d08778c7'  THEN '八斗优选'
                  WHEN a.source_id='appID'  THEN '薪头条'
                  WHEN a.source_id='wxdc39e4684804a8a5' THEN'你包我猜'
                  WHEN a.source_id='yuetoutiao'  THEN'悦头条'

                  ELSE '自然流量'
                  END  媒体 ,
                  a.new_user_num 新用户数,
                  a.active_user_num 活跃用户数,
                  a.authorize_nuser_num 授权用户数,
                  CONCAT(TRUNCATE(( a.day2_new_retain/a.new_user_num  ) * 100, 2), '%')   新增次日留存率 ,
                  CONCAT(TRUNCATE(( a.day3_new_retain/a.new_user_num  ) * 100, 2), '%')   新增三日留存率 ,
                  CONCAT(TRUNCATE(( a.day4_new_retain/a.new_user_num  ) * 100, 2), '%')   新增四日留存率 ,
                  CONCAT(TRUNCATE(( a.day5_new_retain/a.new_user_num  ) * 100, 2), '%')   新增五日留存率 ,
                  CONCAT(TRUNCATE(( a.day6_new_retain/a.new_user_num  ) * 100, 2), '%')   新增六日留存率 ,
                  CONCAT(TRUNCATE(( a.day7_new_retain/a.new_user_num  ) * 100, 2), '%')   新增七日留存率
                FROM
                   voyager.wx_user_report a

                WHERE

                a.date>='{}' AND a.date <='{}'
                GROUP BY a.date,媒体  ORDER BY  a.date DESC '''.format(self.begin_date,self.end_date)


        result =self.dbinfo.execute_sql(sql)

        if result<>():

          self.exportXlsadd(result)

        return result








###媒体选择了非全部

    def add_result2(self):

        sql = '''
                SELECT
                a.date 日期,

                  CASE
                  WHEN a.source_id='wx239bfcba6aeb0084' THEN '有练换换'
                  WHEN a.source_id='wxe65c34b4ec242be' THEN '步数大联盟'
                  WHEN a.source_id='wx3c48ef7a45e89118' THEN '优质福利所'
                  WHEN a.source_id='wx0a051787252f83fa' THEN '易购赚'
                  WHEN a.source_id='wxbb67c77aea9d76a8' THEN '遇见球球'
                  WHEN a.source_id='wx2fa65dcf3dbe5926' THEN '开心游戏大乱斗'
                  WHEN a.source_id='wx42d12a5790960727' THEN '十一光年'
                  WHEN a.source_id='wx4ef839c292cb41ad' THEN '福礼惠公众号'
                  WHEN a.source_id='wx85d4b50441231b98' THEN '我蹦我再蹦'
                  WHEN a.source_id='wx4aab7ee381936b54' THEN '弹球大乱斗'
                  WHEN a.source_id='1017757' THEN 'APP-DSP光速动力'
                  WHEN a.source_id='wx3fe2d608967de425'  THEN '手机弹幕小程序'
                  WHEN a.source_id='wx76dcd806f382ec8e' THEN '智行火车票小程序'
                  WHEN a.source_id='wxd8de2f6276406b2a' THEN '步数换换乐'
                  WHEN a.source_id='wx18a2d299d1482fc0' THEN '打卡小日历'
                  WHEN a.source_id='wxefda0ea3619d87eb'  THEN '玩赚签到'
                  WHEN a.source_id='880090' THEN '光微科技公众号'
                  WHEN a.source_id='582068' THEN '番茄小程序矩阵'
                  WHEN a.source_id='wxd949b04824167683' THEN '小麦圈打卡'
                  WHEN a.source_id='sanyan1017628' THEN '三言app'
                  WHEN a.source_id='wx9bda6799b29d7868' THEN '小集盒'
                  WHEN a.source_id='wx5325ee83f4181dab' THEN '超级打投'
                  WHEN a.source_id='tqoxinwen001' THEN '淘新闻'
                  WHEN a.source_id='1018004' THEN '付呗'
                  WHEN a.source_id='wx5c9a5ce20be8207b'  THEN '哆啦宝'
                  WHEN a.source_id='wxc79d91f3a01dcd31'  THEN '今天点餐吃什么'
                  WHEN a.source_id='wxb09486b4d08778c7'  THEN '八斗优选'
                  WHEN a.source_id='appID'  THEN '薪头条'
                  WHEN a.source_id='wxdc39e4684804a8a5' THEN'你包我猜'
                  WHEN a.source_id='yuetoutiao'  THEN'悦头条'
                ELSE '自然流量'
                END  媒体 ,
                a.new_user_num 新用户数,
                a.active_user_num 活跃用户数,
                a.authorize_nuser_num 授权用户数,
                CONCAT(TRUNCATE(( a.day2_new_retain/a.new_user_num  ) * 100, 2), '%')   新增次日留存率 ,
                CONCAT(TRUNCATE(( a.day3_new_retain/a.new_user_num  ) * 100, 2), '%')   新增三日留存率 ,
                CONCAT(TRUNCATE(( a.day4_new_retain/a.new_user_num  ) * 100, 2), '%')   新增四日留存率 ,
                CONCAT(TRUNCATE(( a.day5_new_retain/a.new_user_num  ) * 100, 2), '%')   新增五日留存率 ,
                CONCAT(TRUNCATE(( a.day6_new_retain/a.new_user_num  ) * 100, 2), '%')   新增六日留存率 ,
                CONCAT(TRUNCATE(( a.day7_new_retain/a.new_user_num  ) * 100, 2), '%')   新增七日留存率
                FROM
                voyager.wx_user_report a

                WHERE
                a.source_id ='{}' and
                a.date>='{}' AND a.date <='{}'
                GROUP BY a.date,媒体  ORDER BY  a.date DESC '''.format(self.source_id,self.begin_date,self.end_date)


        result =self.dbinfo.execute_sql(sql)





        if result<>():

            self.exportXlsadd(result)







        return  result



    def exportXlsadd(self,result):

        if result:

            result = list(result)

            result.insert(0,('日期','媒体/活动','新用户数','活跃用户数','授权用户数','次日留存','三日留存','四日留存','五日留存','六日留存','七日留存'))

            row = len(result)

            wb=Workbook()
            sheet=wb.active
            for i in range(row):

                sheet.append(result[i])


            wb.save('./static/result/mediareport.xlsx')



##勾选了活跃留存

##媒体选择全部，多天
    def live_result(self):

        sql='''
               SELECT
                  a.date 日期,

                  '全部' 媒体 ,
                  SUM(a.new_user_num) 新用户数,
                  SUM(a.active_user_num) 活跃用户数,
                  SUM(a.authorize_nuser_num) 授权用户数,
                  CONCAT(TRUNCATE((SUM(a.day2_active_retain)/SUM(a.active_user_num) ) * 100, 2), '%')   活跃次日留存率 ,
                  CONCAT(TRUNCATE((SUM(a.day3_active_retain)/SUM(a.active_user_num) ) * 100, 2), '%')   活跃三日留存率 ,
                  CONCAT(TRUNCATE((SUM(a.day4_active_retain)/SUM(a.active_user_num) ) * 100, 2), '%')   活跃四日留存率 ,
                  CONCAT(TRUNCATE((SUM(a.day5_active_retain)/SUM(a.active_user_num) ) * 100, 2), '%')   活跃五日留存率 ,
                  CONCAT(TRUNCATE((SUM(a.day6_active_retain)/SUM(a.active_user_num) ) * 100, 2), '%')   活跃六日留存率 ,
                  CONCAT(TRUNCATE((SUM(a.day7_active_retain)/SUM(a.active_user_num) ) * 100, 2), '%')   活跃七日留存率
                FROM
                   voyager.wx_user_report a

                WHERE

                   a.date>='{}' AND a.date <='{}'
                GROUP BY a.date,媒体  ORDER BY  a.date DESC  '''.format(self.begin_date,self.end_date)

        result=self.dbinfo.execute_sql(sql)


        if result<>():

         self.exportXlslive(result)

        return result

###媒体选择全部，单天

    def live_result_one(self):

        sql='''
              SELECT
                  a.date 日期,

                  CASE
                  WHEN a.source_id='wx239bfcba6aeb0084' THEN '有练换换'
                  WHEN a.source_id='wxe65c34b4ec242be' THEN '步数大联盟'
                  WHEN a.source_id='wx3c48ef7a45e89118' THEN '优质福利所'
                  WHEN a.source_id='wx0a051787252f83fa' THEN '易购赚'
                  WHEN a.source_id='wxbb67c77aea9d76a8' THEN '遇见球球'
                  WHEN a.source_id='wx2fa65dcf3dbe5926' THEN '开心游戏大乱斗'
                  WHEN a.source_id='wx42d12a5790960727' THEN '十一光年'
                  WHEN a.source_id='wx4ef839c292cb41ad' THEN '福礼惠公众号'
                  WHEN a.source_id='wx85d4b50441231b98' THEN '我蹦我再蹦'
                  WHEN a.source_id='wx4aab7ee381936b54' THEN '弹球大乱斗'
                  WHEN a.source_id='1017757' THEN 'APP-DSP光速动力'
                  WHEN a.source_id='wx3fe2d608967de425'  THEN '手机弹幕小程序'
                  WHEN a.source_id='wx76dcd806f382ec8e' THEN '智行火车票小程序'
                  WHEN a.source_id='wxd8de2f6276406b2a' THEN '步数换换乐'
                  WHEN a.source_id='wx18a2d299d1482fc0' THEN '打卡小日历'
                  WHEN a.source_id='wxefda0ea3619d87eb'  THEN '玩赚签到'
                  WHEN a.source_id='880090' THEN '光微科技公众号'
                  WHEN a.source_id='582068' THEN '番茄小程序矩阵'
                  WHEN a.source_id='wxd949b04824167683' THEN '小麦圈打卡'
                  WHEN a.source_id='sanyan1017628' THEN '三言app'
                  WHEN a.source_id='wx9bda6799b29d7868' THEN '小集盒'
                  WHEN a.source_id='wx5325ee83f4181dab' THEN '超级打投'
                  WHEN a.source_id='tqoxinwen001' THEN '淘新闻'
                  WHEN a.source_id='1018004' THEN '付呗'
                  WHEN a.source_id='wx5c9a5ce20be8207b'  THEN '哆啦宝'
                  WHEN a.source_id='wxc79d91f3a01dcd31'  THEN '今天点餐吃什么'
                  WHEN a.source_id='wxb09486b4d08778c7'  THEN '八斗优选'
                  WHEN a.source_id='appID'  THEN '薪头条'
                  WHEN a.source_id='wxdc39e4684804a8a5' THEN'你包我猜'
                  WHEN a.source_id='yuetoutiao'  THEN'悦头条'

                  ELSE '自然流量'
                  END  媒体 ,
                  a.new_user_num 新用户数,
                  a.active_user_num 活跃用户数,
                  a.authorize_nuser_num 授权用户数,
                  CONCAT(TRUNCATE(( a.day2_active_retain/a.active_user_num ) * 100, 2), '%') 活跃次日留存率 ,
                  CONCAT(TRUNCATE(( a.day3_active_retain/a.active_user_num ) * 100, 2), '%') 活跃三日留存率,
                  CONCAT(TRUNCATE(( a.day4_active_retain/a.active_user_num ) * 100, 2), '%') 活跃四日留存率,
                  CONCAT(TRUNCATE(( a.day5_active_retain/a.active_user_num ) * 100, 2), '%') 活跃五日留存率,
                  CONCAT(TRUNCATE(( a.day6_active_retain/a.active_user_num ) * 100, 2), '%') 活跃六日留存率,
                  CONCAT(TRUNCATE(( a.day7_active_retain/a.active_user_num ) * 100, 2), '%') 活跃七日留存率
                FROM
                   voyager.wx_user_report a

                WHERE

                   a.date>='{}' AND a.date <='{}'
                GROUP BY a.date,媒体  ORDER BY  a.date DESC  '''.format(self.begin_date,self.end_date)

        result=self.dbinfo.execute_sql(sql)


        if result<>():

          self.exportXlslive(result)

        return result












###媒体选择非全部
    def live_result2(self):

        sql='''
              SELECT
                  a.date 日期,

                  CASE
                  WHEN a.source_id='wx239bfcba6aeb0084' THEN '有练换换'
                  WHEN a.source_id='wxe65c34b4ec242be' THEN '步数大联盟'
                  WHEN a.source_id='wx3c48ef7a45e89118' THEN '优质福利所'
                  WHEN a.source_id='wx0a051787252f83fa' THEN '易购赚'
                  WHEN a.source_id='wxbb67c77aea9d76a8' THEN '遇见球球'
                  WHEN a.source_id='wx2fa65dcf3dbe5926' THEN '开心游戏大乱斗'
                  WHEN a.source_id='wx42d12a5790960727' THEN '十一光年'
                  WHEN a.source_id='wx4ef839c292cb41ad' THEN '福礼惠公众号'
                  WHEN a.source_id='wx85d4b50441231b98' THEN '我蹦我再蹦'
                  WHEN a.source_id='wx4aab7ee381936b54' THEN '弹球大乱斗'
                  WHEN a.source_id='1017757' THEN 'APP-DSP光速动力'
                  WHEN a.source_id='wx3fe2d608967de425'  THEN '手机弹幕小程序'
                  WHEN a.source_id='wx76dcd806f382ec8e' THEN '智行火车票小程序'
                  WHEN a.source_id='wxd8de2f6276406b2a' THEN '步数换换乐'
                  WHEN a.source_id='wx18a2d299d1482fc0' THEN '打卡小日历'
                  WHEN a.source_id='wxefda0ea3619d87eb'  THEN '玩赚签到'
                  WHEN a.source_id='880090' THEN '光微科技公众号'
                  WHEN a.source_id='582068' THEN '番茄小程序矩阵'
                  WHEN a.source_id='wxd949b04824167683' THEN '小麦圈打卡'
                  WHEN a.source_id='sanyan1017628' THEN '三言app'
                  WHEN a.source_id='wx9bda6799b29d7868' THEN '小集盒'
                  WHEN a.source_id='wx5325ee83f4181dab' THEN '超级打投'
                  WHEN a.source_id='tqoxinwen001' THEN '淘新闻'
                  WHEN a.source_id='1018004' THEN '付呗'
                  WHEN a.source_id='wx5c9a5ce20be8207b'  THEN '哆啦宝'
                  WHEN a.source_id='wxc79d91f3a01dcd31'  THEN '今天点餐吃什么'
                  WHEN a.source_id='wxb09486b4d08778c7'  THEN '八斗优选'
                  WHEN a.source_id='appID'  THEN '薪头条'
                  WHEN a.source_id='wxdc39e4684804a8a5' THEN'你包我猜'
                  WHEN a.source_id='yuetoutiao'  THEN'悦头条'
                  ELSE '自然流量'
                  END  媒体 ,
                  a.new_user_num 新用户数,
                  a.active_user_num 活跃用户数,
                  a.authorize_nuser_num 授权用户数,
                  CONCAT(TRUNCATE(( a.day2_active_retain/a.active_user_num ) * 100, 2), '%') 活跃次日留存率 ,
                  CONCAT(TRUNCATE(( a.day3_active_retain/a.active_user_num ) * 100, 2), '%') 活跃三日留存率,
                  CONCAT(TRUNCATE(( a.day4_active_retain/a.active_user_num ) * 100, 2), '%') 活跃四日留存率,
                  CONCAT(TRUNCATE(( a.day5_active_retain/a.active_user_num ) * 100, 2), '%') 活跃五日留存率,
                  CONCAT(TRUNCATE(( a.day6_active_retain/a.active_user_num ) * 100, 2), '%') 活跃六日留存率,
                  CONCAT(TRUNCATE(( a.day7_active_retain/a.active_user_num ) * 100, 2), '%') 活跃七日留存率
                FROM
                   voyager.wx_user_report a

                WHERE
                   a.source_id = '{}' and
                   a.date>='{}' AND a.date <='{}'
                GROUP BY a.date,媒体  ORDER BY  a.date DESC  '''.format(self.source_id,self.begin_date,self.end_date)

        result=self.dbinfo.execute_sql(sql)





        if result<>():

            self.exportXlslive(result)

        else:
            pass





        return result


    def exportXlslive(self,result):

        if result:

            result=list(result)

            result.insert(0,('日期','媒体/活动','新用户数','活跃用户数','授权用户数','次日留存','三日留存','四日留存','五日留存','六日留存','七日留存'))

            row=len(result)

            wb = Workbook()

            sheet = wb.active

            for i in range(row):

                sheet.append(result[i])

            wb.save('./static/result/mediareport.xlsx')

        else:
            pass




if __name__=='__main__':

    Me= Media_reportnew('1017757','2019-02-01','2019-02-13')
    # print Me.show_result()
    # print Me.begin_ym()
    # print Me.end_ym()
    # print Me.liveuser()
    print Me.add_result()
    print Me.add_result2()
    print Me.live_result()
    print Me.live_result2()