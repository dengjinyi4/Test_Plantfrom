# -*- coding: utf-8 -*-
# @Time    : 2019/2/21 14:30
# @Author  : wanglanqing

import json
from flask import Blueprint,request,flash,render_template
# from flask_paginate import Pagination,get_page_parameter
from business_modle.apitool.apiTool import *
from business_modle.querytool.plantfromwtf import *

testCase = Blueprint('testCase',__name__,template_folder='TestCase')

@testCase.route('/Api_index/')
def Api_index():
    at = Api()
    re = at.query_api_stat_summary()
    return render_template('TestCase/apiStatic.html',re =re, col_len = len(re[0]))

#通过jquery控件实现的分页，统计和查询case
@testCase.route('/Api_index/<sub_system>/<any(stat,detail):page_name>/', methods=['POST','GET'])
def sub_system(sub_system,page_name): #,id=None):
    title = sub_system
    at = Api()
    if page_name=='stat':
        static_data = at.query_api_stat_detail(sub_system)
        return render_template('TestCase/sub_system_static.html',title = title, static_data = static_data, static_count = len(static_data),sub_system=sub_system )
    elif page_name=='detail':
        detail_data = at.query_case_list(sub_system)
        return render_template('TestCase/caseList.html', title=title, detail_data=detail_data[0], sub_system=sub_system)

#新建，修改测试用例
@testCase.route('/Api_index/TestCase/<sub_system>/<any(new,update):page_name>/', methods=('POST','GET'))
def TestCase(sub_system,page_name):
    form = TestCaseForm()
    at = Api()
    if page_name=='new' and form.is_submitted():
        sql_data = form.data
        sql_data.pop('csrf_token')
        sql_data.pop('submit')
        url_params = at.split_url(sql_data['methodurl'])
        # print url_params[1]
        sql_data['methodurl'] = url_params[0].strip()
        sql_data['param'] = str(url_params[1]).strip()
        sql_data['group'] = sub_system
        print sql_data
        keys = tuple(sql_data.keys())
        values_list = json.dumps(sql_data.values(), encoding='utf-8', ensure_ascii=False)
        re = at.insert_case(values_list, keys)
        if re != 0:
            flash('添加成功')
        else:
            flash('添加失败')
        return render_template('TestCase/testCase.html', form=form, case_detail=None, sub_system=sub_system)
    elif page_name=='update':
        if len(request.args) > 0:
            cid = request.args['id']
            case_detail = at.query_case_detail(cid)[0]
            methodurl = at.merge_url_param(str(case_detail['methodurl']), str(case_detail['param']))
            if form.is_submitted():
                sql_data = form.data
                sql_data.pop('csrf_token')
                sql_data.pop('submit')
                url_params = at.split_url(sql_data['methodurl'])
                sql_data['methodurl'] = url_params[0].strip()
                sql_data['param'] = url_params[1]
                sql_data['group'] = sub_system.strip()
                set_value='''apiState= "{}",apiName= "{}",testCaseName= "{}",`status`= "{}",`level` = "{}",param_type = "{}",
                             methodurl = "{}",param="{}", actresult = "{}", expect_value = "{}", remarks = "{}"
                             '''.format(sql_data['apiState'],sql_data['apiName'],sql_data['testCaseName'],sql_data['status'],
                                        sql_data['level'],sql_data['param_type'],sql_data['methodurl'],sql_data['param'],
                                        sql_data['actresult'],sql_data['expect_value'],sql_data['remarks'])
                print set_value
                at.update_case(set_value,cid)
                case_detail = at.query_case_detail(cid)[0]
                return render_template('TestCase/testCase.html', form=form, case_detail=case_detail,methodurl=methodurl, sub_system=sub_system)
            else:
                return render_template('TestCase/testCase.html', form=form, case_detail=case_detail, methodurl=methodurl,sub_system=sub_system)
        return render_template('TestCase/testCase.html', form=form, case_detail=None, sub_system=sub_system)
    return render_template('TestCase/testCase.html', form = form,case_detail=None,sub_system=sub_system)


#通过pageniation实现的分页，查询每个子系统的用例明细数据
    # def query_case_list(self,sub_system,pageNumber,pagesize,id=None):
    #     # print pageNumber,pagesize
    #     tmp=(int(pageNumber) - 1)*int(pagesize)
    #     if id:
    #         sql = r'''
    #             select id,apiname,
    #             case
    #             when param_type='A' then '错误信息'
    #             when param_type='B' then '数据结构'
    #             when param_type='C' then '状态码'
    #             end param_type,
    #             testcasename,methodurl,param,expect_value
    #             from test.testcase_adv where `group`='{}'  and id={};'''.format(sub_system,id)
    #     else:
    #         sql = r'''
    #             select id,apiname,
    #             case
    #             when param_type='A' then '错误信息'
    #             when param_type='B' then '数据结构'
    #             when param_type='C' then '状态码'
    #             end param_type,
    #             testcasename,methodurl,param,expect_value
    #             from test.testcase_adv where `group`='{}'  group by id desc
    #             limit {},{};'''.format(sub_system,tmp,pagesize)
    #     re = self.db.execute_sql(sql)
    #     total = int(self.db.execute_sql("select count(*) from test.testcase_adv where `group`='{}' ".format(sub_system))[0][0])
    #     # re.insert(0,('id','apiname','param_type','testcasename','methodurl','param','expect_value','edit'))
    #     keys_list=['id','apiname','param_type','testcasename','methodurl','param','expect_value']
    #     # ToBeJson(keys_list,re)
    #     # return re
    #     if re:
    #         return ToBeJson.trans(keys_list,re),total
    #     else:
    #         return '还没编写测试用例'
    #     pass