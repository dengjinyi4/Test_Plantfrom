# encoding=utf-8
__author__ = 'aidinghua'


import sys
import datetime
import time
from utils.db_info import  *


class Mini_userinfo(object):

    def __init__(self,nick_name,open_id,env_value=False):

        self.nick_name=nick_name
        self.open_id=open_id
        self.db = DbOperations(env_value=env_value)


    ###查询低碳打卡小程序用户个人信息

    def userinfo(self):

        sql = """SELECT
            CASE
            WHEN source_id = 'wx0a051787252f83fa' THEN '有练换换'
            WHEN source_id = 'wxe65c34b4ec242be' THEN '步数大联盟'
            WHEN source_id = 'wx3c48ef7a45e89118' THEN '优质福利所'
            ELSE source_id
            END 来源ID,
            CASE
            WHEN source_type = '1' THEN '公众号'
            WHEN source_type = '2' THEN '小程序'
            WHEN source_type = '3' THEN '微信群'
            WHEN source_type = '4' Then  '自然流量'
            WHEN source_type = '5' Then '好友邀请'
            WHEN source_type = '6' THEN '好友邀请免费兑换活动'
            ELSE '其他'
            END 来源类型,
            open_id OPEN_ID,
            nick_name 微信昵称,
            CASE
            WHEN gender='1' THEN '男'
            WHEN gender='2' THEN '女'
            ELSE '其他'
            END 用户性别,
            total_tjf 总碳积分,
            balance_tjf 碳积分余额,
            tree_level 数的级别,
            total_step 总的步数,
            today_step 今日微信步数,
            today_step_time 今日微信步数领取时间,
            today_giftstep_num 今日赠送步数,
            todaygift_time 今日赠送步数领取时间,
            CASE
            WHEN receive_continu_card ='1' THEN '是'
            WHEN receive_continu_card = '0' THEN '否'
            ELSE '其他'
            END 是否领取连续打卡奖励,
            continu_days 连续打卡天数,
            receive_continu_card_time 领取连续打卡奖励时间
            FROM
            wx_user_info
            WHERE nick_name = '{}' """.format(self.nick_name)

        result = self.db.execute_sql(sql)

        return result

    #####查看小程序用户步数明细

    def step_detail(self):

        sql='''  SELECT
                  open_id OPEN_ID,
                  CASE
                    WHEN TYPE = '1'
                    THEN '邀请拉新赠送'
                    WHEN TYPE = '2'
                    THEN '新人礼包'
                    WHEN TYPE = '3'
                    THEN '每日签到'
                    WHEN TYPE = '4'
                    THEN '连续打卡加成'
                    WHEN TYPE = '5'
                    THEN '当日步数'
                    WHEN TYPE = '6'
                    THEN '赠送步数'
                    WHEN TYPE = '7'
                    THEN '广告任务'
                    WHEN TYPE = '9'
                    THEN '关注公众号'
                    WHEN TYPE = '10'
                    THEN '解锁红包'
                    ELSE '其他'
                  END 获取步数类型,
                  step 步数,
                  create_time 获取步数时间
                FROM
                  voyager.`wx_steplogs`
                WHERE open_id = '{}' order by id desc '''.format(self.open_id)
        result=self.db.execute_sql(sql)

        return result


















if __name__=='__main__':

    miniinfo = Mini_userinfo('Beyond','o0hyf4lMU7CcdWQJLbF5NUcoDtco',env_value=False)

    miniinfo.userinfo()
    miniinfo.step_detail()