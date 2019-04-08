# -*- coding: utf-8 -*-
__author__ = 'Hui Ma'


# from hdt_tools.utils import DbConnection as fb
def getFinaceValue(earnerID,financId):
    # c查询网站主佣金结算数据，并且渲染页面
    # sqlDb = 'SELECT * FROM effect_balance WHERE earner_id = '+str(earnerID)+' ORDER BY id DESC '
    if financId != 'all':
        sqlDb = 'SELECT * FROM effect_balance WHERE earner_id = '+str(earnerID)+' AND balance_status =  "'+str(financId)+'" ORDER BY id DESC'
    else:
        sqlDb = 'SELECT * FROM effect_balance WHERE earner_id = '+str(earnerID)+' ORDER BY id DESC'
    results = fb.ExecuteSelectList(sqlDb)
    #for row in results:
    #  fname = row[0]
    #   lname = row[1]
    #   age = row[2]
    #   sex = row[3]
    #   income = row[4]
    #   # 打印结果
    #   print "fname=%s,lname=%s,age=%d,sex=%s,income=%d" % \
    #          (fname, lname, age, sex, income )
    return results


