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
        redis_nodes=[{"host":'123.59.17.118',"port":'13601'},{"host":'123.59.17.85',"port":'13601'},{"host":'123.59.17.11',"port":'13601'}]
        # redis_nodesh=[{"host":'101.227.103.243',"port":'13601'},{"host":'101.227.103.244',"port":'13601'}]
        redis_nodesh=[{"host":'123.59.17.11',"port":'13601'},{"host":'123.59.17.118',"port":'13601'},{"host":'123.59.17.120',"port":'13601'}]
        redis_nodeht=[{"host":'123.59.17.11',"port":'13601'},{"host":'123.59.17.118',"port":'13601'},{"host":'123.59.17.120',"port":'13601'}]
        r = RedisCluster(startup_nodes=redis_nodes,max_connections=30,decode_responses=True,skip_full_coverage_check=True)
        rsh = RedisCluster(startup_nodes=redis_nodesh,max_connections=30,decode_responses=True,skip_full_coverage_check=True)
        rht = RedisCluster(startup_nodes=redis_nodeht,max_connections=30,decode_responses=True,skip_full_coverage_check=True)
    # print r.hgetall('voyager:budget')
    # 剩余预算
    # 负数订单的个数
    negativecount=0
    if key=='voyager:budget':
        if myenv=='test':
            # mybudget=r.hgetall('voyager:budget')
            mybudget=r.hgetall('voyager:budget')
            # print type(mybudget)
            # 负数的订单个数
            tmp_budget=[]
            for i in  mybudget:
                tmpdict=()
                tmpdict=(i,float(mybudget[i])/100000,0,0,float(mybudget[i])/100000,float(mybudget[i])/100000)
                # print i
                tmp_budget.append(tmpdict)
                if str(mybudget[i])[:1]=='-' or int(mybudget[i])==0:
                    negativecount=negativecount+1
                print '订单为:'+str(i)+' 金额为: '+str(mybudget[i])
        else:
            mybudget=r.hgetall('voyager:budget')
            mybudgetsh=rsh.hgetall('voyager:budget')
            # time.sleep(5)
            mybudgetht=rht.hgetall('voyager:budget')
            for i in  mybudget:
                if str(mybudget[i])[:1]=='-':
                    negativecount=negativecount+1
                print '订单为:'+str(i)+' 金额为: '+str(mybudget[i])
            # print mybudget
            # print mybudgetsh
            if len(mybudget)>len(mybudgetsh):
                print '订单没有完全同步'
            tmp_budget=[]
            tmp_budgetdis=[]
            for i,j in mybudget.items():
                tmpdict=()
                # print i
                # print j
                if (i in(mybudgetsh)) and (i in (mybudgetht)):
                    # 如果有差异放到单独一个列表中
                    tmpdict=(i,float(r.get('voyager:budget_all:'+str(i)))/100,float(j)/100000,float(mybudgetsh[i])/100000,float(mybudgetht[i])/100000,(float(j)-float(mybudgetsh[i]))/100000,(float(j)-float(mybudgetht[i]))/100000)
                    if float(j)-float(mybudgetsh[i])>0:
                        tmp_budgetdis.append(tmpdict)
                    else:
                        tmp_budget.append(tmpdict)
                else:
                    tmpdict=(i,float(r.get('voyager:budget_all:'+str(i)))/100,float(j)/100000,0,0,float(j)/100000,float(j)/100000)
                    tmp_budget.append(tmpdict)
            # 有差异的在前面显示
            tmp_budget=tmp_budgetdis+tmp_budget
        print tmp_budget
        return tmp_budget,len(tmp_budget),negativecount
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
    # 查看ocpa订单实际成本

    elif key=='voyager:ocpa_actual_cost':
        mycost=r.hgetall('voyager:ocpa_actual_cost')
        tmplist = []
        for k,v in mycost.items():
            tmplist.append({k:v})
        return tmplist

    #查看加粉订单新媒体消耗

    elif key=='voyager:new:media:budget':


        myconsume=r.hgetall(key)
        tmp_total=[]

        for k,v in myconsume.items():
            v=float(v)/100000
            tmp_total.append({k:v})

        return tmp_total

    ##查看加粉订单新媒体小时消耗
    elif 'voyager:new:media:budget:hour' in key:

        # key='voyager:new:media:budget:hour_15 23390'
        key1=key.split(' ')
        # print key1[0]


        hourconsume=r.hget(key1[0],key1[1])

        if hourconsume:

           finalhourconsume=float(hourconsume)/100000

        else:
            finalhourconsume=0

        return finalhourconsume










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
        tmp_all=[]
        tmp_list=()
        for i in range(0,24):
            tmp_list=(i,str(tmp_total[i]['total_'+str(i)]),str(tmp_rest[i]['rest_'+str(i)]))
            tmp_all.append(tmp_list)
        return tmp_all

if __name__ == '__main__':
    # 测试
    redis_nodes=[{"host":'101.254.242.12',"port":'17001'},]
    # 生产
    # redis_nodes=[{"host":'123.59.17.118',"port":'13601'},{"host":'123.59.17.85',"port":'13601'},{"host":'123.59.17.11',"port":'13601'}]
    tmp_list=mygetredis('dev','voyager:budget')
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

