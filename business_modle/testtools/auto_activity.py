# encoding=utf-8
__author__ = 'aidinghua'

from utils.db_info import  *
from business_modle.querytool.utils.adh_bejson import *

class manage_activity(object):


    def __init__(self):

        self.db=DbOperations()



    def activity_list(self):

        keys='id,template_type_name,path,click_xpath,obtain_xpath,status,logid_start,logid_end,create_time,update_time'
        sql=''' SELECT
            id ID,
            template_type_name 模板类型名称,
            path 模板路由地址,
            click_xpath 抽奖按钮xpath,
            obtain_xpath 点击广告xpath,
            case status
            when '1' then '有效'
            else '无效'
            end
            状态,
            logid_start logid起始值,
            logid_end logid结束值,
            create_time 创建时间,
            update_time 更新时间
            FROM
            test.test_activity  '''
        result = self.db.execute_sql(sql)

        return adh_bejson.trans(keys.split(','),result)

    def add_activity(self,formdata):

        keys = str(formdata.keys())[1:-1].replace("'","")

        values=json.dumps(formdata.values(),ensure_ascii=False,encoding='utf-8')[1:-1]

        sql = '''insert into test.test_activity ({}) values({}); '''.format(keys,values)

        self.db.execute_sql(sql)
        self.db.mycommit()

if  __name__=='__main__':

    ma = manage_activity()

    print ma.activity_list()









