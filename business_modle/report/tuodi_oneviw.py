#encoding:utf-8
import MySQLdb as mysql,time,datetime

def tmpdaylist(days):
    daylist=[]
    d = datetime.datetime.now()
    for i in range(0,int(days)):
        tmpdate_from=d+datetime.timedelta(days=-i)
        tmpdate_from=str(tmpdate_from)[0:10].replace('-','')
        daylist.append(tmpdate_from)
        daylist.sort()
    return daylist
# 返回包含日期的sql 查找托底订单
def tmpsqllist(days,advertiser_id):
    daylist=tmpdaylist(days)
    tmpsqllist=[]
    for d in daylist:
        tmpsql='SELECT ad_order_id,COUNT(*) FROM ad_show_log'+d+' where advertiser_id='+str(advertiser_id)+' GROUP BY ad_order_id order by COUNT(*) '
        tmpsqllist.append(tmpsql)
    return tmpsqllist,daylist
def mydbnew1(days,advertiser_id):
    db = mysql.connect(host='123.59.17.121',user='voyager',passwd='SIkxiJI5r48JIvPh',db='voyagerlog',port=3306,charset='utf8')
    db.autocommit(True)
    myc = db.cursor()
    # 前端显示执行的sql
    sqllist=[]
    # 返回纵坐标数据 [{name:订单id，data:[1,2,3,4,5,6,7,8,]},{}]
    yclist=[]
    # 定义广告订单对应展示数(字典)
    # adorder_cout={}
    # 153广告主下面各个订单的数量
    adordercount=[]
    # 广告订单点击数量
    # adordershowcount=[]
    # 横坐标赋值
    xcount=tmpdaylist(days)
    # for day in xcount:
    t1sql='SELECT DISTINCT ad_order_id FROM ad_show_log'+xcount[0]+' where advertiser_id='+str(advertiser_id)+';'
    myc.execute(t1sql)
    result=myc.fetchall()
    if len(result)<=0:
        adordercount.append('0')
    else:
        for i in result:
            adordercount.append(str(i[0]))
        # print 'adordercount%s'%adordercount
    for order in adordercount:
        adordershowcount=[]
        adorder_cout={}
        for day in xcount:
            tsql='SELECT ad_order_id,COUNT(*) FROM ad_show_log'+str(day)+' where ad_order_id='+str(order)+' and advertiser_id='+str(advertiser_id)+' GROUP BY ad_order_id order by COUNT(*) '
            # print tsql
            sqllist.append(tsql)
            myc.execute(tsql)
            result1=myc.fetchall()
            if len(result1)<=0:
                adordershowcount.append(0)
            else:
                for i in result1:
                    adordershowcount.append(int(i[1]))
            # print adordershowcount
        adorder_cout['name']=order
        adorder_cout['data']=adordershowcount
        yclist.append(adorder_cout)
    print yclist
    myc.close()
    db.close()
    # return 1
    return xcount,yclist,sqllist
def mydbnew(days,advertiser_id):
    db = mysql.connect(host='123.59.17.121',user='voyager',passwd='SIkxiJI5r48JIvPh',db='voyagerlog',port=3306,charset='utf8')
    db.autocommit(True)
    myc = db.cursor()
    # 前端显示执行的sql
    sqllist=[]
    # 返回纵坐标数据 [{name:订单id，data:[1,2,3,4,5,6,7,8,]},{}]
    yclist=[]
    # 定义广告订单对应展示数(字典)
    # adorder_cout={}
    # 某个广告主下面所有的而广告订单
    tmproderlist=[]
    # 广告订单点击数量
    # adordershowcount=[]
    # 横坐标赋值
    xcount=tmpdaylist(days)
    for day in xcount:
        t1sql='SELECT DISTINCT ad_order_id FROM ad_show_log'+day+' where advertiser_id='+str(advertiser_id)+';'
        myc.execute(t1sql)
        res=myc.fetchall()
        if len(res)>0:
            for i in res:
                tmproderlist.append(str(i[0]))
    # 广告主的所有订单
    tmproderlist=list(set(tmproderlist))
    for order in tmproderlist:
        adordershowcount=[]
        adorder_cout={}
        for day in xcount:
            tsql='SELECT ad_order_id,COUNT(*) FROM ad_show_log'+str(day)+' where ad_order_id='+str(order)+' and advertiser_id='+str(advertiser_id)+' GROUP BY ad_order_id order by COUNT(*) '
            # print tsql
            sqllist.append(tsql)
            myc.execute(tsql)
            result1=myc.fetchall()
            if len(result1)<=0:
                adordershowcount.append(0)
            else:
                for i in result1:
                    adordershowcount.append(int(i[1]))
            # print adordershowcount
        adorder_cout['name']=order
        adorder_cout['data']=adordershowcount
        yclist.append(adorder_cout)
    print yclist
    myc.close()
    db.close()
    # return 1
    return xcount,yclist,sqllist
if __name__ == '__main__':
    # print tmpsqllist(3,153)
    (x,y,s)= mydbnew(6,210)
    print y





