# -*- coding: utf-8 -*-
# @Time    : 2018/6/24 16:22
# @Author  : wanglanqing


from hdt_tools.utils.db_info import *
from config import sub_systems,db_config
from utils.ToBeJson import ToBeJson

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
        try:
            rowcount = self.db.exe_insert_sql(sql)
        except Exception as e:
            print(e)
        return rowcount

    def update_case(self,set_value,cid):
        sql = r"""UPDATE test.testcase_adv SET {} WHERE id='{}'""".format(set_value,cid)
        try:
            rowcount = self.db.execute_sql(sql)
            print sql
        except Exception as e:
            print(e)
        return rowcount
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

    #查询每个子系统的用例明细数据
    def query_case_list(self,sub_system,pageNumber=None,pagesize=None,id=None):
        # print pageNumber,pagesize
        # tmp=(int(pageNumber) - 1)*int(pagesize)
        if id:
            sql = r'''
                select id,apiname,
                case
                when param_type='A' then '错误信息'
                when param_type='B' then '数据结构'
                when param_type='C' then '状态码'
                end param_type,
                testcasename,methodurl,param,expect_value
                from test.testcase_adv where `group`='{}'  and id={} ;'''.format(sub_system,id)
        else:
            sql = r'''
                select id,apiname,
                case
                when param_type='A' then '错误信息'
                when param_type='B' then '数据结构'
                when param_type='C' then '状态码'
                end param_type,
                testcasename,methodurl,param,expect_value
                from test.testcase_adv where `group`='{}'  group by id desc;'''.format(sub_system)
                # format(sub_system,tmp,pagesize)
        re = self.db.execute_sql(sql)
        total = int(self.db.execute_sql("select count(*) from test.testcase_adv where `group`='{}' ".format(sub_system))[0][0])
        # re.insert(0,('id','apiname','param_type','testcasename','methodurl','param','expect_value','edit'))
        keys_list=['id','apiname','param_type','testcasename','methodurl','param','expect_value']
        # ToBeJson(keys_list,re)
        # return re
        if re:
            return ToBeJson.trans(keys_list,re),total
        else:
            return '还没编写测试用例'
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
            re_tmp=[sub_system, id_re, ss_re,cs_re, format(float(ss_re)/float(id_re), '.2%'),'查看']
            re.append(re_tmp)
        re.append([u'总计', tid_re, tss_re, tcs_re, format(float(tss_re)/float(tid_re),'.2%'),'查看'])
        return re

    def query_case_detail(self,id):
        keys_list=['id','apiname','apiState','testcasename','group','status','level','param_type','methodurl','param','actresult','expect_value','remarks']
        c_sql=r"select * from test.testcase_adv a where id={};".format(id)
        case_detail=self.db.execute_sql(c_sql)
        # print len(keys_list)
        # print c_sql
        # print 'case_detail',len(case_detail)
        return ToBeJson.trans(keys_list,case_detail)

    def split_url(self,url):
        if url.__contains__('?'):
            url_list = url.split('?')
            url_f = url_list[0]
            #将params转换为{'aid':'2222455'}的格式
            params = "{'" + url_list[1].replace('=',"':'").replace('&',"','") + "'}"
            return url_f, params
        else:
            url_f = url
            params={}
            return url_f, params

    def __del__(self):
        pass

    def  merge_url_param(self,url,param):
        param_str='?'
        if isinstance(url,str) and isinstance(param,str) and len(param)>2:
            param=param.replace("':'",'=').replace("','",'&')
            return url+param_str+param[2:-2]
        elif isinstance(url,str) and isinstance(param,dict):
            for k,v in param.items():
                print k,v
                param_str=param_str+str(k)+'='+str(v)+'&'
            return url+param_str[0:-1]
        else:
            return url


if __name__=='__main__':
    ai = Api()
    # print ai.query_case_detail(182)
    print ai.merge_url_param('https://apidemand.adhudong.com/api/voyager/plan/add.htm','{}')
    # print ai.split_url('https://apidemand.adhudong.com/api/voyager/plan/add.htm')