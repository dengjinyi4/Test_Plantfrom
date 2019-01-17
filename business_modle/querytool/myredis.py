#!/usr/bin/env python
#encoding: utf-8
# from rediscluster import StrictRedisCluster
from rediscluster import  RedisCluster
def mygetredis(jobid1,key):
    # 测试
    if jobid1=='110':
        redis_nodes=[{"host":'101.254.242.12',"port":'17001'},]
    else:
        redis_nodes=[{"host":'123.59.17.118',"port":'13601'},{"host":'123.59.17.85',"port":'13601'},{"host":'123.59.17.11',"port":'13601'}]
    r = RedisCluster(startup_nodes=redis_nodes,max_connections=30,decode_responses=True,skip_full_coverage_check=True)

    # print r.hgetall('voyager:budget')
    # 剩余预算
    if key=='voyager:budget':
        # mybudget=r.hgetall('voyager:budget')
        mybudget=r.hgetall('voyager:budget')
        # print type(mybudget)
        # 负数的订单个数
        j=0
        for i in  mybudget:
            if str(mybudget[i])[:1]=='-':
                j=j+1
            print '订单为:'+str(i)+' 金额为: '+str(mybudget[i])
        return mybudget,len(mybudget),j
    # ocpa广告位可投放的订单
    elif key=='voyager:ocpa_adzones':
        mybudget=r.hgetall('voyager:ocpa_adzones')
        tmplist=[]
        for k,v in mybudget.items():
            if "normal" in k:
                tmplist.append({k:v})
            elif "adv" in k:
                tmplist.append({k:v})
            elif "indu" in k:
                tmplist.append({k:v})
        return tmplist
    # 小时预算
    else:
        mybudget=r.hgetall(key)
        tmp_rest=[]
        tmp_total=[]
        for i in range (0,24):
            rest_key='rest_'+str(i)
            total_key='total_'+str(i)
            if mybudget.get(rest_key)  is  None or mybudget.get(total_key)  is  None:
                tmp_rest.append({rest_key:0})
                tmp_total.append({total_key:0})
            else:
                rest_value=float(mybudget.get(rest_key))/100000
                total_value=float(mybudget.get(total_key))/100000
                tmp_rest.append({rest_key:rest_value})
                tmp_total.append({total_key:total_value})
        print tmp_rest
        print tmp_total
        return tmp_total,tmp_rest
if __name__ == '__main__':
    # 测试
    redis_nodes=[{"host":'101.254.242.12',"port":'17001'},]
    # 生产
    # redis_nodes=[{"host":'123.59.17.118',"port":'13601'},{"host":'123.59.17.85',"port":'13601'},{"host":'123.59.17.11',"port":'13601'}]
    # tmp=mygetredis('111','voyager:ocpa_adzones')
    tmp_total,tmp_rest=mygetredis('110','voyager:budget_control:1713')
    print tmp_total,tmp_rest
    # for i in range(0,24):
    #     print i
    # tmpdict=[{'rest_0': u'38888888'}, {'total_1': 0}, {'total_2': 0}, {'total_3': 0}, {'total_4': 0}, {'rest_5': u'38883222'}, {'rest_6': u'43743625'}, {'rest_7': u'43743625'}, {'rest_8': u'49992714'}, {'rest_9': u'49992714'}, {'rest_10': u'58324833'}, {'rest_11': u'58316333'}, {'rest_12': u'69979600'}, {'rest_13': u'69969400'}, {'rest_14': u'87436250'}, {'rest_15': u'87385250'}, {'total_16': 0}, {'total_17': 0}, {'total_18': 0}, {'rest_19': u'116462666'}, {'rest_20': u'116411666'}, {'rest_21': u'116411666'}, {'rest_22': u'116411666'}, {'total_23': 0}]
    # # print tmpdict[0]['rest_0']
    # for i in tmpdict:
    #     print i.keys()


    # tmplist=[]
    # tmplist.append('{"x_23":"23"}')
    # tmplist.append('{"x_22":"21"}')
    # tmplist.append('{"x_25":"21"}')
    # print tmplist
    # tmpdict={"x_1":"1","X_2":"321312321","X_3":"3","X_4":"4",}
    # print tmpdict.get('x_2')
    # if tmpdict.get('x_1') is None:
    #     print '3333333333333333333'
    # for i in range(0,24):
    #     print i

