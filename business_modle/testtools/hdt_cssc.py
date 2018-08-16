#encoding:utf-8
#version: 2018/07/11,ad_show,ad_click,lottery_click表增加award_type_id，award_type的展示

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
# 返回包含日期的sql
def tmpsqllist(days,type,adzone_click_id):
    day=tmpdaylist(days)
    tmpsqllist=[]
    if type=='adzon':
        tmpsql="SELECT act_id,adzone_id,ip,region,media_id,master_id,status,adzone_click_id from voyagerlog.adzone_click_log"+day+" where adzone_click_id='"+adzone_click_id+"'"
    elif type=='lottery':
        tmpsql="SELECT award_id,advertiser_id,order_id,act_id,adzone_id,media_id,ip,region,act_award_type,ad_creative_id,plan_id,award_name,choosen_tag,award_id from voyagerlog.lottery_click_log"+day+" where adzone_click_id='"+adzone_click_id+"'"
    elif type=='show':
        tmpsql="SELECT ad_choosen_tag,media_id,adzone_id,act_id,position_id,ad_plan_id,ad_order_id,ad_creative_id,advertiser_id,status,mark,award_type_id,award_type from voyagerlog.ad_show_log"+day+" where adzone_click_id='"+adzone_click_id+"'"
    elif type=='click':
        tmpsql="SELECT media_id,adzone_id,act_id,position_id,ad_plan_id,ad_order_id,ad_creative_id,charge_amount,advertiser_id,occurrence,status,click_source,invalid_message,media_income,system_income,award_type_id,award_type from voyagerlog.ad_click_log"+day+" where adzone_click_id='"+adzone_click_id+"'"
    elif type=='award_show':
        tmpsql="SELECT award_id,act_id,adzone_id,media_id,ip,region,create_time,adzone_click_id,act_award_type,log_type,status,invalid_message,position_id from  award_show_click_log   where adzone_click_id='"+adzone_click_id+"'"
    # tmpsqllist.append(tmpsql)
    print tmpsql
    return tmpsql
def mycursor(type):
    if type=='test':
        db = mysql.connect(host='221.122.127.183',user='voyager',passwd='voyager',db='voyagerlog',port=5701,charset='utf8')
    else:
        db = mysql.connect(host='123.59.17.121',user='voyager',passwd='SIkxiJI5r48JIvPh',db='voyagerlog',port=3306,charset='utf8')
    db.autocommit(True)
    c = db.cursor()
    return c

def mydata(days,dbtype,tabletype,adzone_click_id):
    c=mycursor(dbtype)
    ordersql=tmpsqllist(days,tabletype,adzone_click_id)
    c.execute(ordersql)
    result=c.fetchall()
    c.close()
    return result
    # return '111'
def diffcreatetime():
    myc=mycursor('test')
    sql=r"SELECT create_time  from voyagerlog.lottery_click_log20180103 where adzone_click_id='B3W1CD6H1HP85Z4UM9'"
    myc.execute(sql)
    re=myc.fetchall()
    print re
    count=[]
    for i in range(1,len(re)):
        a=re[i][0]-re[i-1][0]
        count.append(a.seconds)
    print count
    return 1
if __name__ == '__main__':
    allshow=mydata(0,'test','show','B3W1CD6H1HP85Z4UM9')
    print type(allshow)
    print allshow
    # print count[0].seconds
    # print len(re)
    # print type(re[1][0])
    # print re[1][0]-re[0][0]




