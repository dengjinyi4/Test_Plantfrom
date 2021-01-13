# encoding=utf-8
__author__ = 'aidinghua'

import time
import json
from utils.db_info import  *

class Adzone_cp(object):

    def __init__(self,target_adzone_id,resource_adzone_id,env_value):

        self.db=DbOperations(env_value=env_value)
        self.target_adzone_id=target_adzone_id
        self.resource_adzone_id=resource_adzone_id

####比对广告过滤####


    def ad_filter(self):

        sql_target='''SELECT ad_filter_type,ad_filter_content FROM voyager.`base_adzone_info` WHERE id  = {} '''.format(self.target_adzone_id)
        result_target = self.db.execute_sql(sql_target)
        sql_resource='''SELECT ad_filter_type,ad_filter_content FROM voyager.`base_adzone_info` WHERE id  = {} '''.format(self.resource_adzone_id)
        result_resource=self.db.execute_sql(sql_resource)
        print "****************"
        print result_target[0][0]
        if result_target<>() and result_resource<>() :
            if  result_target[0][0]==1 and result_resource[0][0]==1:
                return u"广告过滤比对一致"
            else:

                if result_target==result_resource:
                    return u"广告过滤比对一致"

                else:
                    return str(self.target_adzone_id)+u"目标广告位配置:" + \
                           json.dumps(result_target[0],ensure_ascii=False,encoding='utf-8')+ \
                           "<hr>"+ str(self.resource_adzone_id)+u"来源广告位配置:" + \
                           json.dumps(result_resource[0],ensure_ascii=False,encoding='utf-8')
        elif result_target==() and result_resource==() :
            return u"广告过滤比对一致"
        else:
            return u"广告过滤比对不一致"

#####是否走高级屏蔽策略

    def is_super_static(self):
        sql_super='''SELECT ad_filter_type FROM voyager.`base_adzone_info` WHERE id  = {}'''.format(self.resource_adzone_id)
        result_sql_super=self.db.execute_sql(sql_super)
        print "++++++++"
        print result_sql_super[0][0]
        if result_sql_super[0][0]==6:
            return u"是"
        else:
            return u"否"



####高级屏蔽策略####
    def super_static(self):

        sql_target='''select type,time_type,time_begin,time_end,region_type,shield_region,creative_value,advertiser_industry_type,advertiser_industry,effective_time_begin,effective_time_end,effective_time_type,advertiser_industry_tag_type,advertiser_industry_tag,advertiser_tag_type,advertiser_tag,advertiser_ids_type,advertiser_ids,advertiser_ids_show,creative_brand_tag_type,creative_brand_tag_ids,term_type,term_ids from voyager.`adzone_shield_tactics` where adzone_id ={} '''.format(self.target_adzone_id)
        result_target = self.db.execute_sql(sql_target)
        sql_resource='''select type,time_type,time_begin,time_end,region_type,shield_region,creative_value,advertiser_industry_type,advertiser_industry,effective_time_begin,effective_time_end,effective_time_type,advertiser_industry_tag_type,advertiser_industry_tag,advertiser_tag_type,advertiser_tag,advertiser_ids_type,advertiser_ids,advertiser_ids_show,creative_brand_tag_type,creative_brand_tag_ids,term_type,term_ids from voyager.`adzone_shield_tactics` where adzone_id ={} '''.format(self.resource_adzone_id)
        result_resource= self.db.execute_sql(sql_resource)
        if result_target<>() and result_resource<>() :
            if  result_target==result_resource:
                return u"高级屏蔽比对一致"
            else:
                return str(self.target_adzone_id)+u"目标广告位配置:" + \
                       json.dumps(result_target[0],ensure_ascii=False,encoding='utf-8')+\
                       "<br>" + str(self.resource_adzone_id)+u"来源广告位配置:" + \
                       json.dumps(result_resource[0],ensure_ascii=False,encoding='utf-8')

        elif result_target==() and result_resource==() :
            return u"高级屏蔽比对一致"
        else:
            return u"高级屏蔽比对不一致"

####普通广告CPC出价范围####

    def  cpc_limit(self):
        sql_target='''select a.cpc_limit,b.price_min,b.price_max   FROM voyager.base_adzone_info a
                    left join voyager.adzone_cpc_price_setting b  on a.id = b.adzone_id
                    where a.id= {} and b.status =1  '''.format(self.target_adzone_id)
        result_target = self.db.execute_sql(sql_target)
        sql_resource='''select a.cpc_limit,b.price_min,b.price_max   FROM voyager.base_adzone_info a
                    left join voyager.adzone_cpc_price_setting b  on a.id = b.adzone_id
                    where a.id= {} and b.status =1  '''.format(self.resource_adzone_id)

        result_resource= self.db.execute_sql(sql_resource)

        if result_target<>() and result_resource<>() :
            if result_target==result_resource:
                return u"普通广告CPC出价范围比对一致"

            else:
                return str(self.target_adzone_id)+u"目标广告位配置:" + \
                       json.dumps(result_target[0],ensure_ascii=False,encoding='utf-8')+\
                       "<hr>"+ str(self.resource_adzone_id)+u"来源广告位配置:" + \
                       json.dumps(result_resource[0],ensure_ascii=False,encoding='utf-8')
        elif result_target==() and result_resource==() :
            return u"普通广告CPC出价范围比对一致"
        else:
            return u"普通广告CPC出价范围比对不一致"
####托底广告主过滤类型####
    def  td_filter(self):
        sql_target='''select td_filter_type,td_filter_ids  FROM voyager.base_adzone_info  WHERE id ={} '''.format(self.target_adzone_id)
        result_target = self.db.execute_sql(sql_target)
        sql_resource='''SELECT td_filter_type,td_filter_ids FROM voyager.base_adzone_info WHERE id ={} '''.format(self.resource_adzone_id)
        result_resource= self.db.execute_sql(sql_resource)
        if result_target<>() and result_resource<>() :
            if result_target==result_resource:
                return u"托底广告主过滤比对一致"

            else:
                return str(self.target_adzone_id)+u"目标广告位配置:" + \
                       json.dumps(result_target[0],ensure_ascii=False,encoding='utf-8')+ \
                       "<hr>"+ str(self.resource_adzone_id)+u"来源广告位配置:" + \
                       json.dumps(result_resource[0],ensure_ascii=False,encoding='utf-8')
        elif result_target==() and result_resource==() :
            return u"托底广告主过滤比对一致"
        else:
            return u"托底广告主过滤比对不一致"

####弹出位次限定####
    def  occurrence(self):
        sql_target='''SELECT occurrence,advertiser_ids,advertiser_type,industry_ids,industry_type,status,specific_award,award_ids,position_id,advertiser_tag_type,advertiser_tag_ids,creative_tag_type,creative_tag_ids FROM voyager.advertiser_occurrence_config  WHERE adzone_id ={} and status=1 '''.format(self.target_adzone_id)
        result_target = self.db.execute_sql(sql_target)
        sql_resource='''SELECT occurrence,advertiser_ids,advertiser_type,industry_ids,industry_type,status,specific_award,award_ids,position_id,advertiser_tag_type,advertiser_tag_ids,creative_tag_type,creative_tag_ids FROM voyager.advertiser_occurrence_config  WHERE adzone_id ={} and status=1 '''.format(self.resource_adzone_id)
        result_resource= self.db.execute_sql(sql_resource)
        if result_target<>() and result_resource<>() :
          if result_target[0][0]==1 and result_resource[0][0]==1:

              return u"弹出位次限定比对一致"
          else:
            if result_target==result_resource:
                return u"弹出位次限定比对一致"

            else:
                return str(self.target_adzone_id)+u"目标广告位配置:" + \
                       json.dumps(result_target[0],ensure_ascii=False,encoding='utf-8')+ \
                       "<hr>"+ str(self.resource_adzone_id)+u"来源广告位配置:" + \
                       json.dumps(result_resource[0],ensure_ascii=False,encoding='utf-8')
        elif result_target==() and result_resource==() :
            return u"弹出位次限定比对一致"
        else:
            return u"弹出位次限定比对不一致"


####url过滤####
    def url_filter(self):
        sql_target='''select url_filter,url_filter_content,url_assign_content FROM voyager.`base_adzone_info` WHERE id  = {}  '''.format(self.target_adzone_id)
        result_target = self.db.execute_sql(sql_target)
        sql_resource='''select url_filter,url_filter_content,url_assign_content FROM voyager.`base_adzone_info` WHERE id  = {}  '''.format(self.resource_adzone_id)
        result_resource= self.db.execute_sql(sql_resource)
        if result_target<>() and result_resource<>() :
            if result_target==result_resource:
                return u"url过滤比对一致"

            else:
                return str(self.target_adzone_id)+u"目标广告位配置:" + \
                       json.dumps(result_target[0],ensure_ascii=False,encoding='utf-8')+ \
                       "<hr>"+ str(self.resource_adzone_id)+u"来源广告位配置:" + \
                       json.dumps(result_resource[0],ensure_ascii=False,encoding='utf-8')
        elif result_target==() and result_resource==() :
            return u"url过滤比对一致"
        else:
            return u"url过滤比对不一致"



if __name__=='__main__':
    ac=Adzone_cp(8060,1610,True)

    print ac.ad_filter()
    print ac.is_super_static()
    print ac.super_static()
    print ac.cpc_limit()
    print ac.td_filter()
    print ac.occurrence()
    print ac.url_filter()
