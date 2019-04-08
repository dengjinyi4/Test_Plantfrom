# -*- coding: utf-8 -*-
# @Time    : 2019/3/28 14:08
# @Author  : wanglanqing

import datetime
from rediscluster import RedisCluster
from business_modle.querytool.utils.db_info import DbOperations

def connect_redis():
        redis_nodes=[{"host":'123.59.17.118',"port":'13601'},{"host":'123.59.17.85',"port":'13601'},{"host":'123.59.17.11',"port":'13601'}]
        redis_nodesh=[{"host":'101.227.103.243',"port":'13601'},{"host":'101.227.103.244',"port":'101.227.103.245'}]
        redis_nodeht=[{"host":'221.122.127.148',"port":'13601'}]
        r = RedisCluster(startup_nodes=redis_nodes,max_connections=30,decode_responses=True,skip_full_coverage_check=True)
        rsh = RedisCluster(startup_nodes=redis_nodesh,max_connections=30,decode_responses=True,skip_full_coverage_check=True)
        rht = RedisCluster(startup_nodes=redis_nodeht,max_connections=30,decode_responses=True,skip_full_coverage_check=True)
        return ((r, rsh, rht),('bj_', 'sh_', 'ht_'))

class AdzoneOrders(object):
    def __init__(self,env='0'):
        self.redis_key = 'voyager:adzone_limit:'
        env_dict = {'1':True,'0':False}
        self.db = DbOperations(env_value=env_dict[env])
        self.sql = "SELECT adzone_id from voyager.report_zone where date='{}' ORDER BY adzone_consume DESC LIMIT 20;".format(datetime.datetime.now().strftime('%Y-%m-%d'))

    #从当日的report_zone表里获取前10的广告位信息
    def get_adzones(self):
        return self.db.execute_sql(self.sql)

    #分别查询同一广告主，在3地redis缓存的数据
    def get_orders(self):
        '''
        返回：返回以集群_adzoneID为key，返回订单字典，返回集群_adzoneID的二维list
        '''
        redis_connection = connect_redis()
        adzones = self.get_adzones()
        orders = {}
        #按照bj_adzoneID的方式，返回各个redis查询的数据
        #按照每个广告位，在redis中进行查询
        adzones_group = []
        for adzone in adzones:
            redis_key = self.redis_key + str(adzone[0])
            redis_groups_len = len(redis_connection[0])
            adzone_group = []
            for group in range(redis_groups_len):
                order_key = redis_connection[1][group] + str(adzone[0])
                adzone_group.append(order_key)
                #获得redis中该广告位，订单的消耗数据
                orders[order_key] = redis_connection[0][group].hgetall(redis_key)
            adzones_group.append(adzone_group)
        return orders, adzones_group

    #进行数据比对
    def find_diff(self):
        orders_tmp = self.get_orders()
        orders = orders_tmp[0]
        adzones_group = orders_tmp[1]
        re = []
        adzoneIds = []
        for adzone_group in adzones_group:
            adzoneId = adzone_group[0].split('_')[1]
            adzoneIds.append(adzoneId)
            bj_keys = orders[adzone_group[0]].keys()
            for order in bj_keys:
                re_row = {}
                #bj_redis中的消耗数据，作为基准值
                bj_consum = float(orders[adzone_group[0]][order])/100

                #获得订单在sh redis中的消耗
                if order in orders[adzone_group[1]]:
                    sh_consum = float(orders[adzone_group[1]][order])/100
                else:
                    sh_consum  = 0

                # 获得订单在sh redis中的消耗
                if order in orders[adzone_group[2]]:
                    ht_consum = float(orders[adzone_group[2]][order])/100
                else:
                    ht_consum  = 0

                #将查询结果存入字典中
                re_row['adzoneId'] = adzoneId
                re_row['orderId'] = order
                re_row['bj_consum'] = bj_consum
                re_row['sh_consum'] = sh_consum
                re_row['ht_consum'] = ht_consum
                re_row['bj_sh_diff'] = bj_consum - sh_consum
                re_row['bj_ht_diff'] = bj_consum - ht_consum
                if abs(re_row['bj_ht_diff']) > 0.0 or abs(re_row['bj_sh_diff']) > 0.0:
                    re.insert(0, re_row)
                else:
                    re.append(re_row)
        return re, adzoneIds


if __name__ == '__main__':
    aod = AdzoneOrders()
    # print aod.get_orders()
    print aod.find_diff()
    # with open('we.txt',"w") as f:
    #     f.write(aod.find_diff())