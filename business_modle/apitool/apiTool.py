# -*- coding: utf-8 -*-
# @Time    : 2018/6/24 16:22
# @Author  : wanglanqing


from hdt_tools.utils.db_info import *
from config import sub_systems,db_config


class Api(object):
    def __init__(self):
        self.db = DbOperations()
        self.doc_db = DbOperations(env_value=db_config['doc_online'])
        self.sub_systems = sub_systems
        pass

    #增加用例
    def insert_case(self,values_list,keys):
        sql = r"INSERT INTO test.testcase_adv {} VALUES ".format(keys).replace("'","`")
        sql = sql + "("  + values_list[1:-1] +")"
        rowcount = self.db.exe_insert_sql(sql)
        return rowcount

    def update_case(self):
        pass

    def delete_case(self):
        pass

    def query_case(self):
        pass

    #查询子系统的用例编写数据
    def query_api_stat_detail(self,sub_system):
        sql = r'''select `group`,`actresult`,apiname,count(*) from test.testcase_adv a where a.`group`='{}'  group by  a.apiname,a.actresult;'''.format(sub_system)
        re = self.db.execute_sql(sql)
        return re
        pass

    #分别查询两个数据库，获取total和finished的数据
    def query_api_stat_summary(self):
        ss = sub_systems.keys()
        ids = sub_systems.values()
        re = []
        tid_re =0
        tss_re = 0
        tcs_re = 0
        for id, sub_system in sub_systems.items():
            id_sql = r"select count(*) from doc.doc_api_method a where a.MENU_ID ={} and a.STATUS=1;".format(id)
            ss_sql =r"select count(DISTINCT(apiname)) from test.testcase_adv a where `group`='{}' and apiState=1;".format(sub_system)
            cs_sql = r"select count(*) from test.testcase_adv a where `group`='{}' and apiState=1;".format(sub_system)
            id_re = self.doc_db.execute_sql(id_sql)[0][0]
            ss_re = self.db.execute_sql(ss_sql)[0][0]
            cs_re = self.db.execute_sql(cs_sql)[0][0]
            tid_re = id_re + tid_re
            tss_re = ss_re + tss_re
            tcs_re = cs_re + tcs_re
            re_tmp=[sub_system, id_re, ss_re,cs_re, format(float(ss_re)/float(id_re), '.2%')]
            re.append(re_tmp)
        re.append([u'总计', tid_re, tss_re, tcs_re, format(float(tss_re)/float(tid_re),'.2%')])
        return re

    def __del__(self):
        pass