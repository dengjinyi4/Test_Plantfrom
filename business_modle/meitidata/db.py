#encoding:utf-8
import MySQLdb as mysql ,time,datetime,calendar
from openpyxl import Workbook

def myc(env):
    # db = mysql.connect(host='221.122.127.183',user='voyager',passwd='voyager',db='voyager',port=5701,charset='utf8')
    if env=='testvoyager':
        db = mysql.connect(host='172.16.105.12',user='voyager',passwd='voyager',db='voyager',port=5701,charset='utf8')
    if env=='testtest':
        db = mysql.connect(host='172.16.105.12',user='voyager',passwd='voyager',db='test',port=5701,charset='utf8')
    if env=='devvoyager':
        db = mysql.connect(host='123.59.17.42',user='voyager_reader',passwd='qtwAZz2ozHFOsPD6',db='voyagerlog',port=3306,charset='utf8')
    if env=='nomandytest':
        db = mysql.connect(host='172.16.105.12',user='voyager',passwd='voyager',db='normandy',port=5701,charset='utf8')
    if env=='nomandydev':
        db = mysql.connect(host='123.59.17.36',user='yiqifa_bs_read',passwd='yiqifabsreader',db='normandy',port=3306,charset='utf8')
    db.autocommit(True)
    myc=db.cursor()
    return myc,db
def selectsql(env,sql):
    tmpmyc,tmpdb=myc(env)
    try:
        tmpmyc.execute(sql)
        result=tmpmyc.fetchall()
    except:
        raise SystemError
    tmpmyc.close()
    tmpdb.close()
    return result
def execsql(env,sql):
    tmpmyc,tmpdb=myc(env)
    try:
        tmpmyc.execute(sql)
        tmpdb.commit()
    except Exception as e :
        print 'error is {}'.format(e.message)
    return tmpmyc.rowcount

if __name__ == '__main__':
    tmpsql='''SELECT ad_click_tag FROM voyagerlog.ad_click_log20180930 where ad_choosen_tag='D3W1CD6R1IIZXEMSKH' '''
    re=selectsql('testvoyager',tmpsql)
    print re
    print re[0][0]
    print type(re[0][0])