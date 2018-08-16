#encoding:utf-8
import MySQLdb as mysql,time,datetime

def tmpdaylist(days):
    daylist=''
    d = datetime.datetime.now()
    tmpdate_from=d+datetime.timedelta(days=-int(days))
    tmpdate_from=str(tmpdate_from)[0:10].replace('-','')
    # daylist.append(tmpdate_from)
    # daylist.sort()
    daylist=tmpdate_from
    return daylist
# 返回包含日期的sql 查找托底订单
def tmpsqllist(days):
    day=tmpdaylist(days)
    tmpsqllist=[]
    # for d in daylist:
    tmpsql='SELECT ad_order_id,COUNT(*) FROM ad_show_log'+day+' where advertiser_id=153 and position_id <>0 GROUP BY ad_order_id order by COUNT(*) '
    tmpsqllist.append(tmpsql)
    return tmpsqllist,day
def mydb(days,adorder):
    db = mysql.connect(host='123.59.17.121',user='voyager',passwd='SIkxiJI5r48JIvPh',db='voyagerlog',port=3306,charset='utf8')
    db.autocommit(True)
    c = db.cursor()
    # 返回的数据-前端显示执行的sql
    sqllist=[]
    # 返回横坐标的数据 个数
    xcount=[]
    # 返回纵坐标 单个执行订单时返回的数据
    yclist=[]
    # 返回的数据 小时
    # 153广告主下面的所有订单
    adtuodi_order=[]
    # 153广告主下面各个订单的数量
    adtuodi_order_count=[]
    ordersql,day=tmpsqllist(days)
    c.execute(ordersql[0])
    # 返回这个托底广告订单
    orderresult=c.fetchall()
    for i in orderresult:
        adtuodi_order.append(i[0])
        adtuodi_order_count.append(int(i[1]))
    # for adorder in adtuodi_order:
    tmpsql='SELECT LEFT( create_time, 13 ),ad_order_id,COUNT(*) FROM ad_show_log'+day+' WHERE ad_order_id='+str(adorder)+' and  position_id <>0  GROUP BY LEFT( create_time, 13 ) order by LEFT( create_time, 13 );'
    sqllist.append(tmpsql)
    c.execute(tmpsql)
    print tmpsql
    # 获得单个订单按照小时汇总数据
    re=c.fetchall()
    for i in re:
        xcount.append(str(i[0]))
        yclist.append(int(i[2]))
    print xcount,yclist
    db.close()
    return xcount,yclist,sqllist,adtuodi_order,adtuodi_order_count
    # return '111'
if __name__ == '__main__':
    mydb(0,414)
    # print tmpsqllist(2)

    # print mydb()


