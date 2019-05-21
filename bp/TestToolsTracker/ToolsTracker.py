# -*- coding: utf-8 -*-
# @Time    : 2019/4/7 12:28
# @Author  : wanglanqing


import json
from hdt_tools.utils.db_info import *
from utils.ToBeJson import ToBeJson


class ToolsTracker(object):
    def __init__(self):
        self.db = DbOperations()

    def get_tracker_list(self):
        keys='id,group_id,func_type,submit_date,func_path,func_name,func_desc,tester'
        tracker_list_sql = '''SELECT tt.id,
	                    CASE WHEN tt.group_id = 0 THEN "其他"
                        ELSE g. NAME
                        END NAME,
                         CASE tt.func_type
                        WHEN 1 THEN "新增"
                        WHEN 2 THEN "修改"
                        ELSE "其他"
                        END func_type,
                         tt.submit_date,
                         tt.func_path,
                         tt.func_name,
                         tt.func_desc,
                         u.ch_name
                        FROM
                            `test`.`test_tools_tracker` tt
                        LEFT JOIN `test`.`group` g ON tt.group_id = g.id
                        JOIN `test`.`user` u ON tt.tester = u.id
                        ORDER BY tt.id DESC;'''
        re = self.db.execute_sql(tracker_list_sql)
        return ToBeJson.trans(keys.split(','),re)

    def add_tools_tracker(self,form_datas):
        keys = str(form_datas.keys())[1:-1].replace("'","`")
        values = json.dumps(form_datas.values(), encoding='utf-8', ensure_ascii=False)[1:-1]
        sql = 'insert into test.test_tools_tracker ({})  values ({})'.format(keys,values)
        print '=========='
        print self.db.execute_sql(sql)
        self.db.mycommit()


if __name__=='__main__':
    tt = ToolsTracker()
    print tt.get_tracker_list()