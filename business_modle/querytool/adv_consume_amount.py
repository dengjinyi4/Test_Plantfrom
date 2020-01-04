# -*- coding: utf-8 -*-
# @Time    : 2019/08/08 14:19
# @Author  : wanglanqing
from utils.db_info import *
from utils.ToBeJson import *
from business_modle.querytool import db

class AdvConsumeAmount(object):
    def __init__(self,qdate,env='0'):
        env_dict = {'1':True,'0':False}
        self.db = DbOperations(env_value=env_dict[env])
        self.qdate = qdate
        pass

    def query_consume_amount(self):
        #AND charge_status = 2 20190809删除该查询条件
        sql = """
                    SELECT
                consumer_date,
                advertiser_id,
                order_id,
                ROUND(SUM(amount) / 100, 2),
                ROUND(AVG(consume_amount) / 100, 2),
                ROUND(
                    (
                        SUM(amount) - AVG(consume_amount)
                    ) / 100,
                    2
                ) 差值
            FROM
                voyager.advertiser_balance_pre_deduction
            WHERE
                consumer_date = '{}'
            GROUP BY
                advertiser_id,
                order_id
            ORDER BY
                ROUND(
                    (
                        SUM(amount) - AVG(consume_amount)
                    ) / 100,
                    2
                );
        """.format(self.qdate)
        re = self.db.execute_sql(sql)
        re_list =['consume_date','advertiser_id','order_id','amount','consume_amount','chazhi']
        if re:
            return ToBeJson.trans(re_list,re)
        else:
            return '只能查询今天以前的数据，请检查查询日期'

if __name__ == '__main__':
    res=AdvConsumeAmount('test','voyager')
    print res