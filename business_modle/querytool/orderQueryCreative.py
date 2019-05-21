# -*- coding: utf-8 -*-
# @Time    : 2019/4/8 10:17
# @Author  : zhaoyu
# @Function  : 根据订单查创意
import time
from utils.db_info import *
from utils.ToBeJson import *

class orderCreativeQuery(object):

    def __init__(self,orderId,env='1'):
        env_dict = {'1':True,'0':False}
        self.db = DbOperations(env_value=env_dict[env])
        self.orderId = orderId


    def queryCreative(self):
        sql = "select A.order_id,c.name,c.state,b.id,b.name,b.state,a.state from ad_order_creative a,ad_creative b,ad_order c where a.creative_id=b.id and a.order_id=c.id and a.order_id=" + str(self.orderId)
        re = self.db.execute_sql(sql)

        res = []
        if len(re)==0:
            return r"查不到数据"
        else:
            for data in re:
                datas ={}
                datas["order_id"] = data[0]
                datas["order_name"] = data[1]
                if data[2]==0:
                    datas["order_state"] = r"草稿"
                elif data[2]==1:
                    datas["order_state"] = r"待审核"
                elif data[2]==2:
                    datas["order_state"] = r"审核驳回"
                elif data[2]==3:
                    datas["order_state"] = r"待投放"
                elif data[2]==4:
                    datas["order_state"] = r"投放中"
                elif data[2]==5:
                    datas["order_state"] = r"暂停"
                elif data[2]==6:
                    datas["order_state"] = r"结束"
                elif data[2]==7:
                    datas["order_state"] = r"冻结"

                datas["creative_id"] = data[3]
                datas["creative_name"] = data[4]
                if data[5] == 0:
                    datas["creative_state"] = r"草稿"
                elif data[5] == 1:
                    datas["creative_state"] = r"待审核"
                elif data[5] == 2:
                    datas["creative_state"] = r"审核成功"
                elif data[5] == 3:
                    datas["creative_state"] = r"审核失败"

                if data[6] == 1:
                    datas['bind_state'] = u'有效'
                elif data[6] == 0:
                    datas['bind_state'] = u'无效'
                res.append(datas)
            print res
            return res

    def queryByCreative(self,creativeUrl=None,creativeId=None):
        if creativeUrl:
            #根据创意url查询order
            query_order_id_sql = """select DISTINCT(b.order_id),b.creative_id
                    from voyager.ad_creative_link a
                    left join voyager.ad_order_creative b on b.creative_id = a.creative_id
                    where
                    a.link_android like '%{}%'
                    or a.link_common like '%{}%'
                    or a.link_ios like '%{}%'
                    or a.link_other like '%{}%'
                    and a.is_valid=1
                    and b.state=1
                    order by a.creative_id desc;""".format(creativeUrl, creativeUrl, creativeUrl, creativeUrl)
            re_tmp = self.db.execute_sql(query_order_id_sql)
        if creativeId:
            # 根据创意id查询order
            query_order_id_sql = """select order_id, creative_id from voyager.ad_order_creative
                    where creative_id={}
                    and state=1
                    order by creative_id desc;""".format(creativeId)
            re_tmp = self.db.execute_sql(query_order_id_sql)
        key_list = ['order_id', 'creative_id']
        report_list = ['advertiser_id', 'payment_mode', 'adorder_state', 'ad_consume', 'ad_budget']
        if re_tmp:
            re = ToBeJson.trans(key_list, re_tmp)
            re_len = len(re)
            for i in range(re_len):
                query_report_sql ="""select advertiser_id,
                    case payment_mode when 1 then 'CPM' when 2 then 'CPC' when 3 then 'CPA' when 4 then 'OCPA' end  ,
                    case adorder_state when 1 then '待审核' when 3 then '待投放' when 4 then '投放中' when 5 then '暂停' when 6 then '结束' end,
                    ad_consume/100, ad_budget/100  from voyager.report_order
                    where adorder_id={} and `date`='{}'""".format(re[i]['order_id'],time.strftime('%Y-%m-%d'))
                report_re = self.db.execute_sql(query_report_sql)
                if report_re:
                    re[i]['report_info']=dict(zip(report_list,list(report_re[0])))
                else:
                    re[i]['report_info'] = dict(zip(report_list, list(len(report_list)*'-')))
            return re
        else:
            '没有符合条件的数据'

    def queryByCreativeId(self,creativeId):
        sql = ""
        self.db.execute_sql(sql)
        pass

if __name__=='__main__':
    ocq = orderCreativeQuery(2405)
    print ocq.queryByCreative('https://display.intdmp.com/new/da/-4118-.html')