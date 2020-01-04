# -*- coding: utf-8 -*-
# @Time    : 2019/12/18 18:05
# @Author  : dengjinyi
import datetime
from business_modle.querytool import db
class ad_order(object):
    def __init__(self,order_id,env):
        self.order_id=order_id
        self.env=env
    # 广告主广告订单预扣款
    def get_order_balance_pre_deduction(self):
        tmpsql='''SELECT
                advertiser_id,order_id,ROUND(amount/100,2) 预付金额 ,ROUND(consume_amount/100,2) 消耗金额,
                create_time 创建时间,update_time 更新时间, ratio 比例 ,case charge_status when 1 then '未结算' when 2 then '已结算' END
                from voyager.advertiser_balance_pre_deduction where create_time>'{time}' and order_id={order_id}'''.format(time=datetime.datetime.now().strftime("%Y-%m-%d"),order_id=self.order_id)
        print tmpsql
        re=self.get_re(tmpsql)
        return re
    # 广告主账户流水
    def get_order_balance_log(self):
        tmpsql='''SELECT advertiser_id,ad_order_id,descn,case charge_back_status when 1 then '需要回款' when 2 then '不需要回款' end 回款,
                ROUND(amount/100,2) 金额, ROUND(balance/100,2) 余额,ROUND(total_balance/100,2) 现金加奖励,
                case type when 1 then '充值' when 2 then '退款' when 3 then '划拨' when 4 then '回收' when 5 then '预扣款划拨' when 6 then '预扣款回款' when 7 then '投放消费' end 类型,
                create_time,update_time
                from voyager.advertiser_balance_log where create_time>'{time}' and ad_order_id={order_id} ORDER BY create_time;
                '''.format(time=datetime.datetime.now().strftime("%Y-%m-%d"),order_id=self.order_id)
        re=self.get_re(tmpsql)
        return re
    # 前台操作日志
    def get_manager_log(self):
        tmpsql='''SELECT advertiser_id,advertiser_name,target_id '订单id',
                CASE operate_type when 1 then '添加' when 2 then '修改' WHEN 3 then '暂停' when 4 then '删除' end  '操作',
                item,`before`,`after`,ip,create_time
                FROM voyager.manager_log WHERE create_time>'{time}' and type=1 and target_id={order_id};
                '''.format(time=datetime.datetime.now().strftime("%Y-%m-%d"),order_id=self.order_id)
        re=self.get_re(tmpsql)
        return re
    def get_re(self,tmpsql):
        if self.env=='test':
            re=db.selectsql('testvoyager',tmpsql)
        else:
            re=db.selectsql('devvoyager',tmpsql)
        return re
if __name__ == '__main__':
    order=ad_order(2527,'test')
    print order.get_order_balance_pre_deduction()
    print order.get_order_balance_log()
    print 1
