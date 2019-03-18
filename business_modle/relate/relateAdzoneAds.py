# -*- coding: utf-8 -*-
# @Time    : 2018/11/27 14:19
# @Author  : wanglanqing

import datetime
from business_modle.querytool.utils.db_info import *
from business_modle.querytool.utils.admin import login_admin


class relateAdzoneAct(object):
    def __init__(self,adzoneId,acts):
        self.db = DbOperations()
        self.adzoneId = adzoneId
        self.acts = acts
        self.begin_time = str(datetime.date.today().strftime('%Y-%m-%d')) + ' 00:00:00'
        self.end_time = str((datetime.date.today() + datetime.timedelta(days=120)).strftime('%Y-%m-%d')) + ' 00:00:00'

    def updateAdzoneAct(self):
        delete_sql = "delete from voyager.adzone_act where adzone_id in ({});".format(self.adzoneId).strip()
        update_base_zone="""UPDATE `base_adzone_info` SET `specify_act_type`='1', `specify_order_random`='1' WHERE (`id`='{}')""".format(self.adzoneId.strip())
        update_sql = """INSERT INTO voyager.adzone_act (adzone_id,act_id,act_begin_time,act_end_time,priority)
              VALUES('{}','{}','{}','{}','{}')"""

        #删除广告位上旧数据
        try:
            self.db.execute_sql(delete_sql)
        except Exception as e:
            return e

        #更新广告位的关联活动、指定活动顺序排序属性
        try:
            self.db.execute_sql(update_base_zone)
        except Exception as e:
            return e

        #插入广告位和活动的数据
        if self.acts.__contains__(';'):
            acts_list = self.acts.split(';')
            acts_len = len(acts_list)
            for priority in range(acts_len):
                self.db.execute_sql(update_sql.format(self.adzoneId,acts_list[priority],self.begin_time,self.end_time,priority+1))
        else:
            self.db.execute_sql(update_sql.format(self.adzoneId.strip(),self.acts.strip(), self.begin_time, self.end_time, 1))

    def get_adzone_url(self):
        req_url = 'http://api.admin.adhudong.com/adzone/getLinkAct.htm?id={}'.format(self.adzoneId)
        re = login_admin().get(req_url).json()['data']['adzoneAct']
        acts_len = len(re)
        print req_url
        if acts_len>0:
            return re
        else:
            return '没有关联活动'

    def get_link(self):
        req_url ="http://api.admin.adhudong.com/adzone/getLink.htm?id={}".format(self.adzoneId)
        re = login_admin().get(req_url).json()['data']['url']
        return re


if __name__ == "__main__":
    RAA = relateAdzoneAct('467','580;590')
    print RAA.updateAdzoneAct()
    print RAA.get_link()
