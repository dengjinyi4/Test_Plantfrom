#encoding:utf-8
# import sys
import MySQLdb as mysql ,time,datetime,calendar
import Emar_SendMail_Attachments as emarmail
from decimal import  Decimal
# from openpyxl import Workbook
# reload(sys)
# sys.setdefaultencoding('utf-8')

def myc():
    # db = mysql.connect(host='221.122.127.183',user='voyager',passwd='voyager',db='voyager',port=5701,charset='utf8')
    db = mysql.connect(host='123.59.111.125',user='voyager',passwd='SIkxiJI5r48JIvPh',db='voyager',port=3306,charset='utf8')
    db.autocommit(True)
    myc=db.cursor()
    return myc,db
def selectsql(sql):
    tmpmyc,tmpdb=myc()
    # print sql
    try:
        tmpmyc.execute(sql)
        result=tmpmyc.fetchall()
    except:
        raise SystemError
    tmpmyc.close()
    tmpdb.close()
    return result

def writefile(msg):
    f=open('log.txt','a')
    t=datetime.datetime.now()
    f.write(str(t)+','+msg+','+'\n')
    # f.write('----------------')
    f.closed

def getlanuchlist(year,month,group_id, test_id):
    day_begin = '%d-%02d-01' % (year, month)  # 月初肯定是1号
    wday, monthRange = calendar.monthrange(year, month)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
    day_end = '%d-%02d-%02d' % (year, month, monthRange)
    # tmpsql='''SELECT `id`, case when `group`= 1 then '互动推' else '其他' end, case when `status`= 1 then '上线成功' else '未知' end , `project`, `src_version`, `Changes`, `createtime`, `updatetime`
    # from voyagerlog.launchlist where createtime>'%s' and createtime<'%s'''%(day_begin+' 00:00:00',day_end+' 23:59:59\'')+'order by createtime desc '
    tmpsql='''SELECT g.name 业务组,j.name 项目,u.ch_name 开发 ,ut.ch_name 测试,v.version,v.v_desc,v.create_time from test.version_tracker v
        INNER JOIN  test.group  g on v.group_id=g.id
        INNER JOIN test.jenkins_job j on v.job_id=j.id
        INNER JOIN test.user u on v.applicant_id=u.id
        INNER JOIN test.user ut on v.tester=ut.id
        where g.status=1 and j.status=1 and u.status=1 and '''#g.id=%s and create_time>'%s' and create_time<'%s'''%(group_id,day_begin+' 00:00:00',day_end+' 23:59:59\'')+'order by create_time desc '
    if test_id == 0:
        tmpsql = tmpsql + '''g.id=%s and create_time>'%s' and create_time<'%s'''%(group_id,day_begin+' 00:00:00',day_end+' 23:59:59\'')+'order by create_time desc '
        result=selectsql(tmpsql)
    else:
        tmpsql = tmpsql + '''g.id=%s and ut.id=%s and create_time>'%s' and create_time<'%s'''%(group_id,test_id,day_begin+' 00:00:00',day_end+' 23:59:59\'')+'order by create_time desc '
        result = selectsql(tmpsql)
    return result

def getlanuch(id):
    tmpsql='''SELECT `id`, case when `group`= 1 then '互动推' else '其他' end, case when `status`= 1 then '上线成功' else '未知' end , `project`, `src_version`, `Changes`, `createtime`, `updatetime`
    from voyagerlog.launchlist where id=%s'''%id
    print tmpsql
    result=selectsql(tmpsql)
    return result
def tmpdaylist(days):
    d = datetime.datetime.now()
    # tmpdate_from=d+datetime.timedelta(days=-int(days))
    tmpdate_from=d+datetime.timedelta(days=-int(days))
    tmpdate_from=str(tmpdate_from)[0:10]
    daylist=tmpdate_from
    return str(daylist)
def industrysql(day):
    today=tmpdaylist(day-1)
    yesterday=tmpdaylist(day)
    d=yesterday.replace('-','')
    month=time.strftime("%m", time.localtime())
    sql='''SELECT a.industry_id,i.name,a.num,b.consume FROM ( SELECT c.adv_industry_id industry_id,sum(c.effect_num ) num
    FROM voyager.report_effect c WHERE c.date>='{}' AND c.date<'{}'
    AND c.adv_industry_id IS NOT NULL GROUP BY c.adv_industry_id ) a,
    ( SELECT b.industry_id, ROUND(SUM(a.charge_amount)/100,2) consume FROM voyagerlog.ad_click_log{} a, voyager.advertiser b
    WHERE a.advertiser_id=b.id AND (a.ad_order_id IN ( SELECT DISTINCT b.order_id FROM voyager.ad_creative_link a,
    voyager.ad_order_creative b WHERE a.creative_id=b.creative_id '''.format(yesterday,today,d)
    sql=sql+'''AND a.link_common LIKE '%utm_click=${click_tag}%' AND a.is_valid=1)'''
    sql=sql+''' OR a.ad_order_id IN ( SELECT DISTINCT b.ad_order_id FROM voyagerlog.ad_effect_log_{} b '''.format(month)
    sql=sql+'''WHERE b.create_time >= '{}' AND b.create_time < '{}' ) )
    GROUP BY b.industry_id ) b,voyager.industry i WHERE a.industry_id = b.industry_id AND a.industry_id = i.id'''.format(yesterday,today)
    return sql,yesterday

def sendmai(res,yesterday):
    tmplist=[]
    for k in res:
        tmplist.append(k)
    print tmplist
    mail='''<p></p><p>&emsp;&emsp;&emsp;消耗和成本</p><br>
    <table border=1 cellspacing=0>
    <tr><td>行业id</td><td>行业类型</td><td>效果</td><td>消耗</td><td>成本</td></tr>'''
    for i in tmplist:
        # mail=mail+'''<tr><td>{}</td><td>{}</td><td>{}</td><td>{}</td><td>{}</td></tr>'''.format(i[0],i[1],i[2],i[5],i[5]/i[2])
        mail=mail+'''<tr><td>{}</td><td>'''.format(i[0])
        mail=mail+i[1].encode('utf-8')
        mail=mail+'''</td><td>{}</td><td>{}</td><td>{}</td></tr>'''.format(i[2],'%.2f'%Decimal(i[3]),'%.2f'%Decimal(i[3]/i[2]))
    mail=mail+'''</table>'''
    print mail
    title='''生产行业类型消耗—{}'''.format(yesterday)
    emarmail.sendTestreport(['dengjinyi@emar.com','zhaojing@emar.com'],title,mail)
if __name__ == '__main__':
    tsql,yesterday=industrysql(2)
    res1=selectsql(tsql)
    sendmai(res1,yesterday)
    # print time.strftime("%m", time.localtime())


