#encoding: utf-8
__author__ = 'Administrator'
#数据库连接
import MySQLdb
from hdt_tools.utils.DbInfo import ReadDBConfig

def ConnectDB(mysqlname):
    cp = ReadDBConfig();  #读取数据库配置文件
    db =cp.get(mysqlname, "db")
    host = cp.get(mysqlname, "host")
    user = cp.get(mysqlname, "user")
    passwd = cp.get(mysqlname, "passwd")
    port = int(cp.get(mysqlname, "port"))
    # 打开数据库连接
    db = MySQLdb.connect(host ,user,passwd,db,port,charset='utf8')
    return db

#查询数据返回list
def ExecuteSelectList(sqlStr,mysqlname):
    db = ConnectDB(mysqlname);
    cursor = db.cursor()
    # 执行sql
    cursor.execute(sqlStr)
    # 获取列表集合
    results = cursor.fetchall()
    db.close()
    return results
