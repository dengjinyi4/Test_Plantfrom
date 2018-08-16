#encoding:utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import MySQLdb as mysql,time,datetime
def tmpdaylist(days):
    d = datetime.datetime.now()
    # tmpdate_from=d+datetime.timedelta(days=-int(days))
    tmpdate_from=d+datetime.timedelta(days=-int(days))
    tmpdate_from=str(tmpdate_from)[0:10]
    daylist=tmpdate_from
    return daylist
# 返回包含日期的sql 查找托底订单
def tmpsqllist(days,job_id):
    tmpsqllist=[]
    day=tmpdaylist(days)
    # if type==1:
    tmpsql=r'SELECT data,create_time from job_log where create_time>'+'\''+day+'\''+' and create_time<\''+day+r''' 23:59:59' and job_id='''+'\''+job_id+'\''
    # print tmpsql
    tmpsqllist.append(tmpsql)
    (leftthreshold,rightthreshold)=mythreshold(job_id)
    return tmpsqllist,leftthreshold,rightthreshold
def mediasql(days,mytype,mediaid):
    day=tmpdaylist(days)
    day=day.replace('-','')
    if mytype=='media_id':
        tmpsql='''SELECT l.media_id, l.media_id, COUNT(*)
        FROM voyagerlog.lottery_click_log'''+day+''' l
        WHERE l.act_award_type = 6
        GROUP BY l.media_id
        HAVING COUNT(*) > 1000
        ORDER BY COUNT(*) DESC'''
        return tmpsql
    elif mytype=='adzone_id':
        tmpsql='''SELECT adzone_id,adzone_id,COUNT(*) from voyagerlog.lottery_click_log'''+day+''' as l
        where l.media_id='''+mediaid+''' and act_award_type=6
        GROUP BY adzone_id
        HAVING COUNT(*) > 500
        ORDER BY COUNT(*) DESC
        LIMIT 10;
        '''
        # print tmpsql
        return tmpsql

# 根据jobid返回job报警阈值
def mythreshold(jobid):
    if jobid=='44':
        return 90,100
    elif jobid=='45':
        return 0,1000
    elif jobid=='46':
        return 0,1000
    elif jobid=='47':
        return 10,100
    elif jobid=='48':
        return 0,10
def mycursor():
    db = mysql.connect(host='123.59.17.121',user='voyager',passwd='SIkxiJI5r48JIvPh',db='voyagerlog',port=3306,charset='utf8')
    db.autocommit(True)
    c = db.cursor()
    # db.close()
    return c
def mymedia(days,mytype,mediaid):
    mycur=mycursor()
    sql=mediasql(days,mytype,mediaid)
    # 返回横坐标的数据 时间
    xcount=[]
    # 返回纵坐标 监控数据
    yclist=[]
    mycur.execute(sql)
    re=mycur.fetchall()
    for i in re:
        xcount.append(int(i[0]))
        yclist.append(int(i[2]))
    print xcount
    print yclist
    mycur.close()
    return xcount,yclist
# 数据钻取图
def media_ydata(media_id):
    mycur=mycursor()
    ydata=[]
    for i in  media_id:
        tmpysql='''SELECT adzone_id,COUNT(*) from voyagerlog.lottery_click_log20171111 as l where l.media_id='''+str(i)+''' and act_award_type=6 GROUP BY adzone_id ORDER BY COUNT(*) DESC'''
        mycur.execute(tmpysql)
        re=mycur.fetchall()
        series={}
        series['id']=i
        series_data=[]
        print '000000000000000000000'
        for j in re:
            series_data_item=[]
            series_data_item.append(str(j[0]))
            series_data_item.append(int(j[1]))
            series_data.append(series_data_item)
    # print series_data
        series['data']=series_data
        ydata.append(series)
    print ydata
    return ydata
# 数据钻取图 这个先不用了，速度太慢，通过单一图来处理
def mymediadrilldowns(days):
    mycur=mycursor()
    sql=mediasql(days)
    # 返回横坐标的数据 时间
    xcount=[]
    # 取出来媒体id为了给纵坐标使用
    media_id=[]
    # 返回纵坐标 监控数据
    yclist=[]
    mycur.execute(sql)
    re=mycur.fetchall()
    for i in re:
        # 单个的横坐标数据
        xitem={}
        media_id.append(i[0])
        xitem['name']='media'+str(i[0])
        xitem['y']=int(i[2])
        xitem['drilldown']=str(i[0])
        xcount.append(xitem)
    yclist=media_ydata(media_id)
    # print xcount,media_id
    # print yclist
    mycur.close()
    return xcount,yclist
def mydb(days,job_id):
    db = mysql.connect(host='123.59.17.246',user='egou_read',passwd='urm8cq9fey7gapnn',db='monitor',port=3306,charset='utf8')
    db.autocommit(True)
    c = db.cursor()
    sqllist=[]
    # 返回横坐标的数据 时间
    xcount=[]
    # 返回纵坐标 监控数据
    yclist=[]
    # 返回的数据 小时
    job_log,leftthreshold,rightthreshold=tmpsqllist(days,job_id)
    c.execute(job_log[0])
    # 返回监控数据
    orderresult=c.fetchall()
    for i in orderresult:
        xcount.append(str(i[1]))
        yclist.append(int(i[0]))
    tmpyclist=[]
    tmpdata={}
    for y in yclist:
        if int(y)>float(rightthreshold) or int(y)<float(leftthreshold):
            tmpdata={'y':int(y),
                     'marker':{'symbol':'url(http://www.highcharts.com/demo/gfx/snow.png)'}}
            tmpyclist.append(tmpdata)
        else:
            tmpyclist.append(int(y))
    db.close()
    print xcount,tmpyclist
    return xcount,tmpyclist,job_log
    # return '111'
if __name__ == '__main__':
    # mymediadrilldowns(0)
    print  mediasql(0,'adzone_id','20')



