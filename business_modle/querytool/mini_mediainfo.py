# encoding=utf-8
__author__ = 'aidinghua'


import time
import datetime
import sys
from utils.dtdb_info import  *

class Mini_mediainfo(object):


#初始函数 定义查询日期 查询环境为线上环境

    def __init__(self,source_id,begin_time,env_value=False):

        self.begin_time=begin_time
        self.db=DtdbOperations(env_value=env_value)
        self.source_id=source_id


#查询授权用户数

    def authorize_user(self):

        sql=''' SELECT count(1) FROM ditandaka.wx_user_info  WHERE  source_id = '{}' AND  create_time>'{} 00:00:00' AND  create_time<'{} 23:59:59'   AND nick_name IS NOT NULL  AND open_id IN(SELECT DISTINCT open_id FROM ditandaka.wx_user_authorize_log WHERE TYPE =1 AND operate=1 ) ORDER BY id DESC '''.format(self.source_id,self.begin_time,self.begin_time)
        result = self.db.execute_sql(sql)[0][0]
        return result



###查询领取微信步数的用户数

    def wxstep_user(self):

        sql=''' SELECT count(DISTINCT(open_id)) FROM ditandaka.wx_steplogs WHERE open_id IN (SELECT open_id FROM ditandaka.wx_user_info  WHERE   source_id = '{}' AND  create_time>'{} 00:00:00' AND   create_time<'{} 23:59:59'   AND nick_name IS NOT NULL  AND open_id IN(SELECT DISTINCT open_id FROM ditandaka.wx_user_authorize_log WHERE TYPE =1 AND operate=1 ))
            AND TYPE=5   AND  create_time>'{} 00:00:00' AND   create_time<'{} 23:59:59'  '''.format(self.source_id,self.begin_time,self.begin_time,self.begin_time,self.begin_time)
        result = self.db.execute_sql(sql)[0][0]

        return result


#查询多少授权用户邀请到了好友
    def invite_user(self):

        sql=''' SELECT count(DISTINCT inviter_openid) FROM ditandaka.wx_invite_relation WHERE inviter_openid IN (SELECT open_id FROM ditandaka.wx_user_info  WHERE   source_id = '{}' AND  create_time>'{} 00:00:00' AND   create_time<'{} 23:59:59' AND nick_name IS NOT NULL  AND open_id IN(SELECT DISTINCT open_id FROM ditandaka.wx_user_authorize_log WHERE TYPE =1 AND operate=1 ))
            AND  create_time>'{} 00:00:00' AND   create_time<'{} 23:59:59'  '''.format(self.source_id,self.begin_time,self.begin_time,self.begin_time,self.begin_time)
        result = self.db.execute_sql(sql)[0][0]
        return result





###查询授权用户邀请到了多少好友
    def invited_user(self):

          sql='''SELECT count(DISTINCT open_id) FROM ditandaka.wx_invite_relation WHERE inviter_openid IN (SELECT open_id FROM ditandaka.wx_user_info  WHERE   source_id = '{}'AND  create_time>'{} 00:00:00' AND   create_time<'{} 23:59:59'    AND nick_name IS NOT NULL  AND open_id IN(SELECT DISTINCT open_id FROM ditandaka.wx_user_authorize_log WHERE TYPE =1 AND operate=1 ))
                 AND  create_time>'{} 00:00:00' AND   create_time<'{} 23:59:59'  '''.format(self.source_id,self.begin_time,self.begin_time,self.begin_time,self.begin_time)

          result = self.db.execute_sql(sql)[0][0]

          return result



###获得了广告位任务奖励的用户数
    def task_user(self):

          sql='''SELECT count(DISTINCT(open_id)) FROM ditandaka.wx_steplogs WHERE open_id IN (SELECT open_id FROM ditandaka.wx_user_info  WHERE   source_id = '{}' AND  create_time>'{} 00:00:00' AND   create_time<'{} 23:59:59'   AND nick_name IS NOT NULL  AND open_id IN(SELECT DISTINCT open_id FROM ditandaka.wx_user_authorize_log WHERE TYPE =1 AND operate=1 ))
              AND TYPE=7  AND    create_time>'{} 00:00:00' AND   create_time<'{} 23:59:59'   '''.format(self.source_id,self.begin_time,self.begin_time,self.begin_time,self.begin_time)
          result = self.db.execute_sql(sql)[0][0]
          return result




if __name__=='__main__':

     mediainfo=Mini_mediainfo('wxe65c34b4ec242be','2019-01-02',env_value=False)

     print mediainfo.authorize_user()
     print mediainfo.wxstep_user()
     print mediainfo.invite_user()
     print mediainfo.invited_user()
     print mediainfo.task_user()

     # print datetime.datetime.now().strftime("%Y-%m-%d")

