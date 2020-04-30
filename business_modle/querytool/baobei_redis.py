#!/usr/bin/env python
#encoding: utf-8
# from rediscluster import StrictRedisCluster
import time
from rediscluster import  RedisCluster
def mygetredis(myenv,key):
    # 测试
    if myenv=='test':
        redis_nodes=[{"host":'101.254.242.12',"port":'17001'},]
        r = RedisCluster(startup_nodes=redis_nodes,max_connections=30,decode_responses=True,skip_full_coverage_check=True)
    else:
        redis_nodes=[{"host":'123.59.17.215',"port":'13400'},{"host":'123.59.17.217',"port":'13400'},{"host":'123.59.17.218',"port":'13400'}]
        r = RedisCluster(startup_nodes=redis_nodes,max_connections=30,decode_responses=True,skip_full_coverage_check=True)
    # print r.hgetall('voyager:budget')
    # 剩余预算
    # 负数订单的个数
    negativecount=0

    # ocpa广告位可投放的订单
    if key=='normandy_cate_goods_hset_task_key':
        mybudget=r.hgetall('normandy_cate_goods_hset_task_key')
        tmplist=[]
        tmpv=''
        for k,v in mybudget.items():
            tmpdic={}
            # u'1:1:1578647040056#@#164#@#1578646920088'
            tmpv=r.lrange(v.split('#@#')[0],0,200)
            print tmpv
            tmpdic[k]=r.lrange(v.split('#@#')[0],0,200)
            tmplist.append(tmpdic)

        return tmplist



if __name__ == '__main__':
    # 测试
    redis_nodes=[{"host":'101.254.242.12',"port":'17001'},]
    # 生产
    # redis_nodes=[{"host":'123.59.17.118',"port":'13601'},{"host":'123.59.17.85',"port":'13601'},{"host":'123.59.17.11',"port":'13601'}]
    tmp_list=mygetredis('dev','normandy_cate_goods_hset_task_key')
    # tmp_list=mygetredis('dev','voyager:new:media:budget:hour_16 29702')
    print tmp_list
    # print tmp_list

    # tmplist=['a','b','c','d','e','f','g','h','j','k']
    # print tmplist[8:12]
    # for i in range(5,10):
    #     print i
    # tmpdict=[{'rest_0': u'38888888'}, {'total_1': 0}, {'total_2': 0}, {'total_3': 0}, {'total_4': 0}, {'rest_5': u'38883222'}, {'rest_6': u'43743625'}, {'rest_7': u'43743625'}, {'rest_8': u'49992714'}, {'rest_9': u'49992714'}, {'rest_10': u'58324833'}, {'rest_11': u'58316333'}, {'rest_12': u'69979600'}, {'rest_13': u'69969400'}, {'rest_14': u'87436250'}, {'rest_15': u'87385250'}, {'total_16': 0}, {'total_17': 0}, {'total_18': 0}, {'rest_19': u'116462666'}, {'rest_20': u'116411666'}, {'rest_21': u'116411666'}, {'rest_22': u'116411666'}, {'total_23': 0}]
    # # print tmpdict[0]['rest_0']
    # for i in tmpdict:
    #     print i.keys()

