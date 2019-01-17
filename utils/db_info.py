# -*- coding: utf-8 -*-
# @Time    : 2018/2/25 15:38
# @Author  : wanglanqing


import MySQLdb

# -*- coding: utf-8 -*-
# @Time    : 2017/12/13 9:53
# @Author  : wanglanqing

import MySQLdb

class DbOperations(object):

    def __init__(self, env_value=True):
        if env_value == True:
            #测试环境
            self.db = MySQLdb.connect(host="221.122.127.183",
                                       port=5701,
                                       db="voyager",
                                       user="voyager",
                                       passwd="voyager",
                                       charset = 'utf8')
        else:
            #生产环境,            123.59.17.121,
            self.db = MySQLdb.connect(host="123.59.111.25",
                                      port=3306,
                                      db="voyager",
                                      user="voyager",
                                      passwd="SIkxiJI5r48JIvPh",
                                      charset='utf8')
        self.cursor = self.db.cursor()

    def execute_sql(self, sql):
        print '执行的sql是： '+ sql
        try:
            self.cursor.execute(sql)
            self.db.commit()
            results = self.cursor.fetchall()
            # print results
            return results
        except Exception as e:
            print e

    def len_value(self, sql):
        # print '执行的sql是： '+ sql
        results = self.execute_sql(sql)
        if results == None:
            results = 0
            return results
        else:
            return len(results)
        sum()


    def close_db(self):
        self.db.close()

    def close_cursor(self):
        self.cursor.close()

    def mycommit(self):
        self.db.commit()

    def myrollback(self):
        self.db.rollback()

if __name__=='__main__':
    db = DbOperations()
    sql= "select id from voyager.template_type where name='类型1'"
    re= db.execute_sql(sql)
    print int(re[0][0])
