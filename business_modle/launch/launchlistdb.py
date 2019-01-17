#encoding:utf-8
import MySQLdb as mysql ,time,datetime,calendar
from openpyxl import Workbook

def myc():
    # db = mysql.connect(host='221.122.127.183',user='voyager',passwd='voyager',db='voyager',port=5701,charset='utf8')
    db = mysql.connect(host='221.122.127.183',user='voyager',passwd='voyager',db='test',port=5701,charset='utf8')
    db.autocommit(True)
    myc=db.cursor()
    return myc,db
def selectsql(sql):
    tmpmyc,tmpdb=myc()
    try:
        tmpmyc.execute(sql)
        result=tmpmyc.fetchall()
    except:
        raise SystemError
    tmpmyc.close()
    tmpdb.close()
    return result
def instertsql(sql):
    tmpmyc,tmpdb=myc()
    try:
        tmpmyc.execute(sql)
        tmpdb.commit()
    except:
        tmpdb.rollback()
        raise SystemExit
    tmpdb.close()
def lanuchlisttmpsql(group,project,src_version,Changes):
    tmpsql='''INSERT INTO `voyagerlog`.`launchlist` ( `group`, `status`, `project`, `src_version`, `Changes`, `createtime`, `updatetime`)
    VALUES ('%s', '1', '%s', '%s', '%s', '%s', '%s');'''%(group,project,src_version,Changes,str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))),str(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))))
    return tmpsql

def exportXls(result):
    #处理传入的sql查询结果，把表头insert到result[0][0]
    if len(result)>0:
        result = list(result)
        result.insert(0,(u'id',u' 业务组',u'项目',u'开发' ,u'测试',u'版本',u'描述', u'上线时间'))
        row = len(result)
        wb = Workbook()
        ws = wb.active
        for r in range(row):
            ws.append(result[r])
        wb.save('./static/result/result.xlsx')
        
def getlanuchlist(year,month,group_id, tester_name):
    day_begin = '%d-%02d-01' % (year, month)  # 月初肯定是1号
    wday, monthRange = calendar.monthrange(year, month)  # 得到本月的天数 第一返回为月第一日为星期几（0-6）, 第二返回为此月天数
    day_end = '%d-%02d-%02d' % (year, month, monthRange)
    # tmpsql='''SELECT `id`, case when `group`= 1 then '互动推' else '其他' end, case when `status`= 1 then '上线成功' else '未知' end , `project`, `src_version`, `Changes`, `createtime`, `updatetime`
    # from voyagerlog.launchlist where createtime>'%s' and createtime<'%s'''%(day_begin+' 00:00:00',day_end+' 23:59:59\'')+'order by createtime desc '
    tmpsql='''SELECT v.id,g.name 业务组,j.name 项目,u.ch_name 开发 ,
        v.tester 测试,v.version,v.v_desc,v.create_time from test.version_tracker v
        INNER JOIN  test.group  g on v.group_id=g.id
        INNER JOIN test.jenkins_job j on v.job_id=j.id
        INNER JOIN test.user u on v.applicant_id=u.id
        where g.status=1 and j.status=1 and u.status=1 and '''#g.id=%s and create_time>'%s' and create_time<'%s'''%(group_id,day_begin+' 00:00:00',day_end+' 23:59:59\'')+'order by create_time desc '
    if tester_name == 'ALL':
        tmpsql = tmpsql + '''g.id=%s and create_time>'%s' and create_time<'%s'''%(group_id,day_begin+' 00:00:00',day_end+' 23:59:59\'')+'order by create_time desc '
        print tmpsql
        result=selectsql(tmpsql)
    else:
        tmpsql = tmpsql + '''v.tester like '%{}%' and g.id={} and  create_time>'{} 00:00:00' and create_time<'{} 23:59:59'order by create_time desc'''.format(tester_name, group_id, day_begin, day_end)
        print tmpsql
        result = selectsql(tmpsql)
    print result
    return result
def getlanuch(id):
    tmpsql='''SELECT vt.id,g.name,jj.name,u.ch_name,tester,create_time,v_desc,vt.status
            from test.version_tracker vt
            join test.group g on vt.group_id=g.id
            join test.user u on vt.applicant_id=u.id
            join test.jenkins_job jj on vt.job_id=jj.id
            where vt.id=%s'''%id
    #根据sql查询的字段，定义表单元素
    name_list = ['id',u'业务组',u'job名',u'开发者',u'测试者',u'上线时间',u'上线描述',u'状态']
    print tmpsql
    result=dict(zip(name_list,list(selectsql(tmpsql)[0])))
    print result
    return result




if __name__ == '__main__':
    tmpsql=lanuchlisttmpsql('bidd','321321fdas','fdasfda')

    print getlanuch(1)
