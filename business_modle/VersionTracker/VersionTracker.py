# -*- coding: utf-8 -*-
# @Time    : 2018/7/10 21:33
# @Author  : wanglanqing
import datetime
from hdt_tools.utils.db_info import *
from config import *


class VersionTracker(object):
    def __init__(self):
        self.db = DbOperations()
        pass

    def get_user_info(self, sql):
        re = self.db.execute_sql(sql)
        return re
        pass
    def get_user_ch_name(self,sql):
        re = self.db.execute_sql(sql)[0]
        return re

    def get_group_info(self, sql):
        re = self.db.execute_sql(sql)
        return re

    def get_jenkins_job(self, sql):
        re = self.db.execute_sql(sql)
        return re

    def get_date(self):
        return datetime.date.today()

    # 增加用例
    def insert_version(self, values_list, keys):
        sql = r"INSERT INTO test.version_tracker {} VALUES ".format(keys).replace("'", "`")
        # sql = r"INSERT INTO test.test_version_tracker {} VALUES ".format(keys).replace("'", "`")
        sql = sql + "(" + values_list[1:-1] + ")"
        rowcount = self.db.exe_insert_sql(sql)
        return rowcount

    # 查询子系统的用例编写数据
    def query_version_stat_detail(self, sub_system):
        sql = r'''select `group`,`actresult`,apiname,count(*) from test.testcase_adv a where a.`group`='{}'  group by  a.apiname,a.actresult;'''.format(
            sub_system)
        re = self.db.execute_sql(sql)
        return re
        pass

    # 分别查询两个数据库，获取total和finished的数据
    def query_version_stat_summary(self):
        ss = sub_systems.keys()
        ids = sub_systems.values()
        re = []
        tid_re = 0
        tss_re = 0
        tcs_re = 0
        for id, sub_system in sub_systems.items():
            id_sql = r"select count(*) from doc.doc_api_method a where a.MENU_ID ={} and a.STATUS=1;".format(id)
            ss_sql = r"select count(DISTINCT(apiname)) from test.testcase_adv a where `group`='{}' and apiState=1;".format(
                sub_system)
            cs_sql = r"select count(*) from test.testcase_adv a where `group`='{}' and apiState=1;".format(sub_system)
            id_re = self.doc_db.execute_sql(id_sql)[0][0]
            ss_re = self.db.execute_sql(ss_sql)[0][0]
            cs_re = self.db.execute_sql(cs_sql)[0][0]
            tid_re = id_re + tid_re
            tss_re = ss_re + tss_re
            tcs_re = cs_re + tcs_re
            re_tmp = [sub_system, id_re, ss_re, cs_re, format(float(ss_re) / float(id_re), '.2%')]
            re.append(re_tmp)
        re.append([u'总计', tid_re, tss_re, tcs_re, format(float(tss_re) / float(tid_re), '.2%')])
        return re

    def update_version_desc_state(self,id,status,v_desc,tester):
        sql = '''update test.version_tracker
            set v_desc='{}',status={},update_time=now(),tester='{}'
            where id= {}'''.format(v_desc,status,tester,id)
        # print sql
        rowcount = self.db.exe_insert_sql(sql)
        return rowcount

    #获得统计数据
    def get_version_stat(self,year=None):
        '''
        :param year: int类型
        :return:返回字典，month返回月份，1返回互动推数据，2返回亿起发数据，3返回易购数据
        '''
        if year:
            re = {}
            month_tmp = self.db.execute_sql('''select DISTINCT date_format(a.create_time,'%Y-%m') from test.version_tracker a
                                where YEAR(a.create_time)={} group by MONTH(a.create_time);'''.format(year))
            re['month'] = self.to_list(month_tmp,type=2)
            for group_id in range(1,4):
                sql = '''select count(1) from test.version_tracker a
                            join test.`group` b on b.id =a.group_id
                            where a.group_id={} and YEAR(a.create_time)={}
                            group by MONTH(a.create_time);'''.format(group_id, year)
                tmp_re = self.db.execute_sql(sql)
                re[group_id]=self.to_list(tmp_re,type=1)
                #因2018-07月，亿起发和易购没有线上记录，特殊处理，7月的亿起发和易购数据为0
                if year == 2018 and group_id in (2,3):
                    re[group_id].insert(0,0)
            return re
        else:
            re = {}
            month_tmp = self.db.execute_sql('''select  DISTINCT date_format(a.create_time,'%Y-%m') from test.version_tracker a
                            where a.group_id=1 order by YEAR(a.create_time) ,MONTH(a.create_time);''')
            re['month'] = self.to_list(month_tmp,type=2)
            for group_id in range(1,4):
                sql = '''select count(1) from test.version_tracker a
                            join test.`group` b on b.id =a.group_id
                            where a.group_id={} group by YEAR(a.create_time) ,MONTH(a.create_time);'''.format(group_id)
                tmp_re = self.db.execute_sql(sql)
                re[group_id]=self.to_list(tmp_re,type=1)
                # 因2018-07月，亿起发和易购没有线上记录，特殊处理，7月的亿起发和易购数据为0
                if group_id in (2,3):
                    re[group_id].insert(0,0)
            return re


    def to_list(self,list,type=1):
        list_len = len(list)
        if list_len>0:
            re = []
            if type == 1:
                for item in list:
                    re.append(int(item[0]))
                return re
            else:
                for item in list:
                    re.append(item[0].encode("utf-8"))
                return re
        else:
            return []

    def __del__(self):
        pass

    # def send_mail(self):
    #     mail = Mail()
    #     msg = Message(subject='test send mail',sender='wanglanqing@emar.com',recipients=['wanglanqing@emar.com'])
    #     msg.body = 'send by testr'
    #     msg.html = '<p>中文对么？</p>'


if __name__=='__main__':
    vt = VersionTracker()
    print vt.get_date()