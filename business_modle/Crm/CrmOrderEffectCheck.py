# -*- coding: utf-8 -*-
# @Time    : 2018/11/6 15:46
# @Author  : wanglanqing

from utils.db_info import *
from utils.ToBeJson import *

class Crm(object):
    def __init__(self,date):
        self.db=DbOperations(env_value=False)
        self.date=date

    def check_info(self):
        sql_effect='''
            SELECT ad_click_tag,COUNT(1) from voyagerlog.ad_effect_log_{} where create_time>='{} 00:00:00' AND create_time<'{} 23:59:59'
            and url like '%ypg%'
            and ad_click_tag like 'E%'
            GROUP BY ad_click_tag
            HAVING COUNT(1)>=1
            ORDER BY COUNT(1) DESC;
        '''.format(self.date[5:7],self.date,self.date)
        dict_effect=dict(self.db.execute_sql(sql_effect))
        if dict_effect.has_key(None):
            dict_effect.pop(None)
        effect_tag_list = dict_effect.keys()
        dict_order={}
        for tag in effect_tag_list:
            if tag !='None':
                sql_crm_order='''
                  SELECT ad_click_tag,count(*) from voyager.crm_order where ad_click_tag='{}'
                '''.format(tag)
            re=self.db.execute_sql(sql_crm_order)
            dict_order[re[0][0]]=re[0][1]
        return dict_effect,dict_order,effect_tag_list
        pass

    def cmp_infos(self,check_re):
        lost=[] #effect中有，但order表中没有
        neq=[] #order表中比effect表的数量不一致
        dict_effect=check_re[0]
        dict_order=check_re[1]
        effect_tag_list=check_re[2]
        re_final={'msg':'','data':[]}
        #根据effect的ad_click_tag遍历effect和order的key，比较对应的value
        for tag in effect_tag_list:
            if dict_order.has_key(tag):
                if int(str(dict_effect[tag])) != int(str(dict_order[tag])):
                    effect_list=[]
                    order_list=[]
                    sql_effect = '''select ad_click_tag,url,advertiser_id,ad_order_id,ad_creative_id from voyagerlog.ad_effect_log_{} where ad_click_tag='{}'
                        '''.format(self.date[5:7], tag)
                    effect_list.append(ToBeJson.trans(['ad_click_tag','url','advertiser_id','ad_order_id','ad_creative_id'],self.db.execute_sql(sql_effect)))

                    sql_order = '''SELECT ad_click_tag,order_url,customer_id,ad_order_id,order_no,product_id  from voyager.crm_order where ad_click_tag='{}'
                        '''.format(tag)
                    # print type(ToBeJson.trans(['ad_click_tag','order_url','customer_id','ad_order_id','order_no','product_id'] ,self.db.execute_sql(sql_order)))
                    order_list.append(ToBeJson.trans(['ad_click_tag','order_url','customer_id','ad_order_id','order_no','product_id'] ,self.db.execute_sql(sql_order)))
                    re_final['msg']=self.date+'order表中比effect表的数量不一致,effect和order表的数据分别为'
                    re_final['data']=effect_list,order_list
                    # print 'effect_list'
                    # print effect_list


                    return re_final
            #
            # else:
            #     # lost.append(tag)
            #     lost.append(str(tag) + u',只在effect中有，crm_order表中没有')
            #
            #     lost.append(self.db.execute_sql(sql_effect))
        if len(lost)==0 & len(neq)==0:
            re_final['msg']=self.date+'的crm_order表数据和effect表数据一致，无差异'
            return re_final
        else:
            return lost,neq

if __name__=='__main__':
    ceo=Crm('2018-11-03')
    # print ceo.check_info('2018-11-05')
    print ceo.cmp_infos(ceo.check_info())


