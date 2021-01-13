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
        self.act_time=0
        self.region=' '
        self.order_id=0
        self.order_region_type=0
        self.region_exclude=0
        self.region_type=0
        self.term=0
        self.priority=1
        self.operator='test'
        self.popup_associate_type=0
        self.popup_collation='2'
        self.create_time=str(datetime.date.today().strftime('%Y-%m-%d')) + ' 00:00:00'


    def updateAdzoneAct(self):
        delete_sql = "delete from voyager.adzone_act where adzone_id in ({});".format(self.adzoneId).strip()
        update_base_zone="""UPDATE `base_adzone_info` SET `specify_act_type`='1', `specify_order_random`='1' WHERE (`id`='{}')""".format(self.adzoneId.strip())
        update_sql = """INSERT INTO voyager.adzone_act (adzone_id,act_id,act_time,act_begin_time,act_end_time,region,order_id,order_region_type,region_exclude,region_type,term,priority,operator,popup_associate_type,popup_collation,create_time)
              VALUES('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')"""


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
                self.db.execute_sql(update_sql.format(self.adzoneId,acts_list[priority],self.act_time,self.begin_time,self.end_time,self.region,self.order_id, self.order_region_type,self.region_exclude,self.region_type,
                                                      self.term,priority+1,self.operator,self.popup_associate_type,self.popup_collation,self.create_time))
        else:
            self.db.execute_sql(update_sql.format(self.adzoneId.strip(),self.acts.strip(),self.act_time,self.begin_time, self.end_time,self.region,self.order_id, self.order_region_type,self.region_exclude,self.region_type,
                                                  self.term,1,self.operator,self.popup_associate_type,self.popup_collation,self.create_time))





    def get_adzone_url(self):
        req_url = 'http://api.admin.adhudong.com/adzone/getLinkAct.htm?id={}'.format(self.adzoneId)
        re = login_admin().get(req_url).json()['data']['adzoneAct']
        acts_len = len(re)
        if acts_len>0:
            return re
        else:
            return '没有关联活动'

    def get_link(self):
        req_url ="http://api.admin.adhudong.com/adzone/getLink.htm?id={}".format(self.adzoneId)
        re = login_admin().get(req_url).json()['data']['url']
        return re


if __name__ == "__main__":
    RAA = relateAdzoneAct('8061','100')
    print RAA.updateAdzoneAct()
    print RAA.get_link()
