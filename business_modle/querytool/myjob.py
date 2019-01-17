#encoding:utf-8
import db,time
import business_modle.report.hdtmonitor as h
from collections import Counter
# 装饰器 写日志
def deco(funcq):
    def a():
        with open('log.txt','a') as f:
            startime=time.time()
            tmpcountsql,r,tmpinsertsql,rexec=funcq()
            endtime=time.time()
            msecs=(endtime-startime)*1000
            print 'time is {} ms'.format(str(msecs))
            print r
            f.write('{} 查找sql{},查找出来的数量是:{},插入sql:{},插入影响数据:{}\n'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),tmpcountsql,r,tmpinsertsql,rexec))
    return a
@deco
def adzon2666():
    tmpday=h.tmpdaylist(0).replace('-','')
    tmpcountsql='''SELECT COUNT(1) from voyagerlog.adzone_click_log{} where adzone_id=2666'''.format(tmpday)
    r=db.selectsql('devvoyager',tmpcountsql)
    tmpinsertsql='''INSERT INTO `test`.`job_log` ( `data`, `type`, `createtime`) VALUES ({}, '1','{}')'''.format(r[0][0],time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    print r[0][0]
    print tmpinsertsql
    rexec=db.execsql('testtest',tmpinsertsql)
    print rexec
    return tmpcountsql,r[0][0],tmpinsertsql,rexec


if __name__ == '__main__':
    adzon2666()
    # print 1111


