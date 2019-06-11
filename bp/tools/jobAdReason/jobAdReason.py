# -*- coding: utf-8 -*-
# @Time    : 2019/5/14 11:40
# @Author  : wanglanqing


import json
from hdt_tools.utils.db_info import *
from utils.ToBeJson import ToBeJson


class JobAdReason(object):
    def __init__(self):
        self.db = DbOperations()
        self.pdb = DbOperations(env_value=True)
        self.jid = 0
        self.jobsql = ""

    def get_job_ad_reason_list(self):
        keys=['id','jobname','ad_order','jobsql','job_status','run_status','have_adzone_click_ids','ES_result']
        # ,if(LENGTH(result)>0,'是','否 ,'have_result'
        list_sql = '''SELECT id,jobname,ad_order,jobsql,
             case job_status when 1 then '有效' when 2 then '无效' END,
             case run_status when 1 then '停止' when 2 then '正在运行' when 3 then '获取广告位点击id完成' when 4 then '读取es进行中' when 5 then '读取es完成'end,
             IF ((LENGTH(adzone_click_ids) > 0)OR (LENGTH(adzone_click_ids_remark)),'有','无') AS have_adzone_click_ids,
             IF ((LENGTH(result_key)>0) and (LENGTH(result_value)>0),'有','无') as ES_result
            FROM test.job_ad_reason ORDER BY id DESC; '''
        re = self.db.execute_sql(list_sql)
        return ToBeJson.trans(keys,re)

   #提交sql的表单数据入库
    def add_job_ad_reason(self,form_datas):
        keys = str(form_datas.keys())[1:-1].replace("'", "`")
        values = json.dumps(form_datas.values(), encoding='utf-8', ensure_ascii=False)[1:-1]
        sql = 'insert into test.job_ad_reason ({})  values ({})'.format(keys,values)
        self.db.execute_sql(sql)
        self.db.mycommit()
        self.jid = int(self.db.execute_sql('SELECT @@IDENTITY;')[0][0])
        self.jobsql = form_datas['jobsql']
        # self.add_adzone_click_ids()


    #通过传入的sql，查询该广告位的adzone_click_id
    def add_adzone_click_ids(self,id):
        jobsql = self.db.execute_sql("select jobsql from test.job_ad_reason where id ={} ".format(id))
        re = self.db.execute_sql(str(jobsql[0][0]))
        print re
        if re:
            adzone_click_ids = JobAdReason.merge_adzone_click_ids(re)
            update_sql = """UPDATE test.`job_ad_reason` SET `adzone_click_ids`="{}" ,update_time=now() WHERE `id`='{}' """.format(
                adzone_click_ids, id)
        else:
            adzone_click_ids_remark='没有该广告位点击'
            update_sql = "UPDATE test.`job_ad_reason` SET `adzone_click_ids_remark`='{}' ,update_time=now()  WHERE `id`='{}' ".format(adzone_click_ids_remark, id)
        self.db.execute_sql(update_sql)

    @staticmethod
    def merge_adzone_click_ids(re):
        '''
        :param re: 序列类型
        :return:返回用;拼接的字符串
        '''
        ids = ''
        for item in re:
            ids = ids + item[0] + ';'
        return ids[:-1]

    def query_chart(self,jid):
        sql = '''select result_key,result_value from test.job_ad_reason where id={} '''.format(jid)
        re = self.db.execute_sql(sql)[0]
        return re

if __name__=='__main__':
    j = JobAdReason()
    print j.query_chart(3)[0]