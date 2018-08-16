#encoding:utf-8
import MySQLdb as mysql,time,datetime

def getweeknew(days,j):
    d = datetime.datetime.now()
    dayscount = datetime.timedelta(days=d.isoweekday())
    print
    dayto = d - dayscount
    sixdays = datetime.timedelta(days=days)
    dayfrom = dayto - sixdays
    print '1111111'+str(type(dayfrom))+str(dayfrom)
    date_from = datetime.datetime(dayfrom.year, dayfrom.month, dayfrom.day, 0, 0, 0)
    tmplist=[]
    for i in range(0,j,1):
        tmpdate_from=date_from+datetime.timedelta(days=i)
        tmplist.append(str(tmpdate_from)[0:10].replace('-',''))
        print tmplist[i]
    return tmplist
def tmpdaylist(days):
    daylist=[]
    d = datetime.datetime.now()
    for i in range(0,int(days)):
        tmpdate_from=d+datetime.timedelta(days=-i)
        tmpdate_from=str(tmpdate_from)[0:10].replace('-','')
        daylist.append(tmpdate_from)
        daylist.sort()
    return daylist
# 返回日期和包含日期的sql
def tmpsqllist(days):
    daylist=tmpdaylist(days)
    tmpsqllist=[]
    for d in daylist:
        tmpsql='select count(*) from ad_show_log'+d+' where advertiser_id=153 and position_id <>0 GROUP BY advertiser_id'
        tmpsqllist.append(tmpsql)
    return daylist,tmpsqllist
def mydb(days):
    db = mysql.connect(host='123.59.17.121',user='voyager',passwd='SIkxiJI5r48JIvPh',db='voyagerlog',port=3306,charset='utf8')
    db.autocommit(True)
    c = db.cursor()
    count=[]
    (daylist,sqllist)=tmpsqllist(days)
    for tsql in sqllist:
        # c.execute('SELECT COUNT(*) from ad_show_log20170827 where advertiser_id=153')
        c.execute(tsql)
        result=c.fetchall()
        # print result
        # count = [i[0] for i in c.fetchall()]
        for i in result:
            count.append(int(i[0]))
    # print count
    db.close()
    return daylist,count,sqllist
if __name__ == '__main__':

    print mydb()

