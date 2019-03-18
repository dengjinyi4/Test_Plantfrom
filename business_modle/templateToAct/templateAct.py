# -*- coding: utf-8 -*-
# @Time    : 2019/1/8 9:27
# @Author  : wanglanqing
from business_modle.querytool.utils.db_info import *
from business_modle.querytool.utils.ToBeJson import *
from openpyxl import Workbook

class templateAct():

    def __init__(self,env='1'):
        env_dict = {'1':True,'0':False}
        self.db = DbOperations(env_value=env_dict[env])
        pass

    def get_infos(self,template_kws=None,act_ids=None):
        result_final = []
        if template_kws:
            if ';' in template_kws:
                template_kws_list = template_kws.split(';')
                # print template_kws_list
                for item in template_kws_list:
                    # 通过模板查询活动
                    template_sql = """SELECT a.id as '活动id',a.act_name  as '活动名称', t.id as '模板id',t.template_name AS '模板名称',
                    v.location_adress,t.remark FROM base_act_info a
                    INNER JOIN base_template_info t ON a.template_id = t.id
                    LEFT JOIN template_type v ON t.template_type_id = v.id
                    WHERE v.location_adress like '%{}%'
                    ORDER BY v.location_adress DESC;""".format(item)
                    result_tmp = self.db.execute_sql(template_sql)
                    if result_tmp:
                        for item_tmp in result_tmp:
                            result_final.append(item_tmp)
            else:
                # 通过模板查询活动
                template_sql = """SELECT a.id as '活动id',a.act_name  as '活动名称', t.id as '模板id',t.template_name AS '模板名称',
                v.location_adress,t.remark FROM base_act_info a
                INNER JOIN base_template_info t ON a.template_id = t.id
                LEFT JOIN template_type v ON t.template_type_id = v.id
                WHERE v.location_adress like '%{}%'
                ORDER BY v.location_adress DESC;""".format(template_kws.strip())
                result_tmp = self.db.execute_sql(template_sql)
                if result_tmp:
                    for item in result_tmp:
                        result_final.append(item)

        if act_ids:
            # 通过活动id查询模板
            if ';' in act_ids:
                act_ids_list = act_ids.split(';')
                for id_item in act_ids_list:
                    act_sql = """select bai.id as '活动id',bai.act_name  as '活动名称', bti.id as '模板id',bti.template_name AS '模板名称',
                    tt.location_adress,bti.remark from voyager.template_type tt
                    join voyager.base_template_info bti
                    on tt.id = bti.template_type_id
                    join voyager.base_act_info bai
                    on bai.template_id=bti.id
                    where bai.id='{}'""".format(id_item.strip())

                    result_tmp2 = self.db.execute_sql(act_sql)
                    if result_tmp2:
                        result_final.append(result_tmp2[0])
            else:
                act_sql = """select bai.id as '活动id',bai.act_name  as '活动名称', bti.id as '模板id',bti.template_name AS '模板名称',
                tt.location_adress,bti.remark from voyager.template_type tt
                join voyager.base_template_info bti
                on tt.id = bti.template_type_id
                join voyager.base_act_info bai
                on bai.template_id=bti.id
                where bai.id='{}'""".format(act_ids)
                result_tmp2 = self.db.execute_sql(act_sql)
                if result_tmp2:
                    result_final.append(result_tmp2[0])
        if result_final:
            return result_final
        else:
            return '没有查询到'

    def exportTemplateXls(self,result):
        # 处理传入的sql查询结果，把表头insert到result[0][0]
        if len(result) > 0:
            result = list(result)
            result.insert(0, (u'活动id', u' 活动名称', u'模板id', u'模板名称', u'模板url地址',u'模板配置信息'))
            row = len(result)
            wb = Workbook()
            ws = wb.active
            for r in range(row):
                print result[r]
                ws.append(result[r])
            try:
                wb.save('./static/result/templateResult.xlsx')
            except IOError as e:
                print e

    #查询坑位信息
    def get_position(self,template_id):
        position_sql = """
        select bpi.position_name,tp.position_id from voyager.template_position tp
        join voyager.base_position_info bpi
        on tp.position_id = bpi.id
        where tp.template_id={}""".format(template_id)
        position_re = self.db.execute_sql(position_sql)
        return position_re