# -*- coding: utf-8 -*-
# @Time    : 2019/1/8 9:27
# @Author  : wanglanqing
from business_modle.querytool.utils.db_info import *
from business_modle.querytool.utils.ToBeJson import *
from openpyxl import Workbook

class templateAct():

    def __init__(self,env='1'):
        env_dict = {'1':True,'0':False}
        #用户选择的db
        self.db = DbOperations(env_value=env_dict[env])
        #实例化用户未选择的db
        if env=='1':
            self.db_unchoosed = DbOperations(env_value=env_dict['0'])
        else:
            self.db_unchoosed = DbOperations(env_value=env_dict['1'])
        pass

    def get_infos(self,template_kws=None,act_ids=None,template_ids=None):
        result_final = []
        if template_kws:
            if ';' in template_kws:
                template_kws_list = template_kws.split(';')
                # print template_kws_list
                for item in template_kws_list:
                    # 通过模板查询活动
                    template_sql = """SELECT a.id as '活动id',a.act_name  as '活动名称',
                    a.popup_template_id as '活动使用的天降红包弹窗模板',case a.is_popup_ad when 0 then '否' when 1 then '是' end as '活动是否直接调用天降红包',
                    t.id as '模板id',t.template_name AS '模板名称',
                    GROUP_CONCAT(p.position_id) as '坑位',case t.support_pop when 0 then '不支持' when 1 then '支持' end as '模板是否支持可配置活动弹窗',
                    v.location_adress,t.remark FROM base_act_info a
                    INNER JOIN base_template_info t ON a.template_id = t.id
                    LEFT JOIN template_type v ON t.template_type_id = v.id
                    join template_position p on p.template_id=a.template_id
                    WHERE v.location_adress like '%{}%' group by a.id
                    ORDER BY a.id DESC;""".format(item)
                    result_tmp = self.db.execute_sql(template_sql)
                    if result_tmp:
                        for item_tmp in result_tmp:
                            result_final.append(item_tmp)
            else:
                # 通过模板查询活动
                template_sql = """SELECT a.id as '活动id',a.act_name  as '活动名称',
                a.popup_template_id as '活动使用的天降红包弹窗模板',case a.is_popup_ad when 0 then '否' when 1 then '是' end as '活动是否直接调用天降红包',
                t.id as '模板id',t.template_name AS '模板名称',
                GROUP_CONCAT(p.position_id) as '坑位',case t.support_pop when 0 then '不支持' when 1 then '支持' end as '模板是否支持可配置活动弹窗',
                v.location_adress,t.remark FROM base_act_info a
                INNER JOIN base_template_info t ON a.template_id = t.id
                LEFT JOIN template_type v ON t.template_type_id = v.id
                join template_position p on p.template_id=a.template_id
                WHERE v.location_adress like '%{}%' group by a.id
                ORDER BY a.id DESC;""".format(template_kws.strip())
                result_tmp = self.db.execute_sql(template_sql)
                if result_tmp:
                    for item in result_tmp:
                        result_final.append(item)

        if act_ids:
            # 通过活动id查询模板
            if ';' in act_ids:
                act_ids_list = act_ids.split(';')
                for id_item in act_ids_list:
                    act_sql = """select bai.id as '活动id',bai.act_name  as '活动名称',
                    bai.popup_template_id as '活动使用的天降红包弹窗模板',case bai.is_popup_ad when 0 then '否' when 1 then '是' end as '活动是否直接调用天降红包',
                    bti.id as '模板id',bti.template_name AS '模板名称',
                    GROUP_CONCAT(p.position_id) as '坑位',case bti.support_pop when 0 then '不支持' when 1 then '支持' end as '模板是否支持可配置活动弹窗',
                    tt.location_adress,bti.remark from voyager.template_type tt
                    join voyager.base_template_info bti on tt.id = bti.template_type_id
                    join voyager.base_act_info bai on bai.template_id=bti.id
                    join template_position p on p.template_id=bai.template_id
                    where bai.id='{}'
                    group by bai.id order by bai.id desc""".format(id_item.strip())

                    result_tmp2 = self.db.execute_sql(act_sql)
                    if result_tmp2:
                        result_final.append(result_tmp2[0])
            else:
                act_sql = """select bai.id as '活动id',bai.act_name  as '活动名称',
                bai.popup_template_id as '活动使用的天降红包弹窗模板',case bai.is_popup_ad when 0 then '否' when 1 then '是' end as '活动是否直接调用天降红包',
                bti.id as '模板id',bti.template_name AS '模板名称',
                GROUP_CONCAT(p.position_id) as '坑位',case bti.support_pop when 0 then '不支持' when 1 then '支持' end as '模板是否支持可配置活动弹窗',
                tt.location_adress,bti.remark from voyager.template_type tt
                join voyager.base_template_info bti on tt.id = bti.template_type_id
                join voyager.base_act_info bai on bai.template_id=bti.id
                join template_position p on p.template_id=bai.template_id
                where bai.id='{}'
                group by bai.id order by bai.id desc""".format(act_ids)
                result_tmp2 = self.db.execute_sql(act_sql)
                if result_tmp2:
                    result_final.append(result_tmp2[0])

        if template_ids:
            # 通过模板id查询
            if ';' in template_ids:
                template_ids_list = template_ids.split(';')
                for template_id_item in template_ids_list:
                    act_sql = """SELECT a.id as '活动id',a.act_name  as '活动名称',
                    a.popup_template_id as '活动使用的天降红包弹窗模板',case a.is_popup_ad when 0 then '否' when 1 then '是' end as '活动是否直接调用天降红包',
                    t.id as '模板id',t.template_name AS '模板名称',
                    GROUP_CONCAT(p.position_id) as '坑位',case t.support_pop when 0 then '不支持' when 1 then '支持' end as '模板是否支持可配置活动弹窗',
                    v.location_adress,t.remark FROM base_act_info a
                    INNER JOIN base_template_info t ON a.template_id = t.id
                    LEFT JOIN template_type v ON t.template_type_id = v.id
                    join template_position p on p.template_id=a.template_id
                    WHERE t.id='{}'
                    group by a.id order by a.id desc; ;""".format(template_id_item)
                    result_tmp2 = self.db.execute_sql(act_sql)
                    if result_tmp2:
                        for result_tmp3 in result_tmp2:
                            result_final.append(result_tmp3)
            else:
                act_sql = """SELECT a.id as '活动id',a.act_name  as '活动名称',
                a.popup_template_id as '活动使用的天降红包弹窗模板',case a.is_popup_ad when 0 then '否' when 1 then '是' end as '活动是否直接调用天降红包',
                t.id as '模板id',t.template_name AS '模板名称',
                GROUP_CONCAT(p.position_id) as '坑位',case t.support_pop when 0 then '不支持' when 1 then '支持' end as '模板是否支持可配置活动弹窗',
                v.location_adress,t.remark FROM base_act_info a
                INNER JOIN base_template_info t ON a.template_id = t.id
                LEFT JOIN template_type v ON t.template_type_id = v.id
                join template_position p on p.template_id=a.template_id
                WHERE t.id='{}'
                group by a.id order by a.id desc; """.format(template_ids)
                result_tmp2 = self.db.execute_sql(act_sql)
                if result_tmp2:
                    for result_tmp3 in result_tmp2:
                        result_final.append(result_tmp3)

        if result_final:
            return result_final
        else:
            return '没有查询到'

    def exportTemplateXls(self,result):
        # 处理传入的sql查询结果，把表头insert到result[0][0]
        if len(result) > 0:
            result = list(result)
            result.insert(0, (u'活动id', u' 活动名称',u'活动使用的天降红包弹窗模板',u'活动是否直接调用天降红包', u'模板id', u'模板名称',u'模板坑位',u'模板是否支持可配置活动弹窗', u'模板url地址',u'模板配置信息'))
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

    #根据模板查询生产/测试活动id
    def get_act_id(self,template_key_words):
        result_final = []
        #避免线上测试域名不一致，以new为关键字，去掉域名，获取new/xxx.html模板关键字
        template_key=template_key_words.split('.com/')[1]
        template_key_words_sql ="""SELECT a.id as '活动id',a.act_name  as '活动名称',
                a.popup_template_id as '活动使用的天降红包弹窗模板',case a.is_popup_ad when 0 then '否' when 1 then '是' end as '活动是否直接调用天降红包',
                t.id as '模板id',t.template_name AS '模板名称',
                GROUP_CONCAT(p.position_id) as '坑位',case t.support_pop when 0 then '不支持' when 1 then '支持' end as '模板是否支持可配置活动弹窗',
                v.location_adress,t.remark FROM voyager.base_act_info a
                INNER JOIN voyager.base_template_info t ON a.template_id = t.id
                LEFT JOIN voyager.template_type v ON t.template_type_id = v.id
                join voyager.template_position p on p.template_id=a.template_id
                WHERE v.location_adress like '%{}%' group by a.id
                ORDER BY a.id DESC;""".format(template_key)
        self.db_unchoosed.execute_sql(template_key_words_sql)
        result_tmp2 = self.db_unchoosed.execute_sql(template_key_words_sql)
        if result_tmp2:
            for result_tmp3 in result_tmp2:
                result_final.append(result_tmp3)
        if result_final:
            return result_final
        else:
            return '没有查询到'
