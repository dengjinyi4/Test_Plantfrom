#coding=utf-8
#!/usr/bin/python

import MySQLdb

class Dboperation(object):
    def __init__(self,env_value=True):
        if env_value == True:
            #测试环境
            self.db=MySQLdb.connect(host="172.16.9.9",
                                port=3306,
                                user="egou",
                                passwd="egou",
                                db="fanxian",
                                charset="utf8")
        else:
            #生成环境
            self.db=MySQLdb.connect(host="221.122.127.202",
                                    port=3306,
                                    user="xiaxiaomei",
                                    passwd="butKRQ5Zxi",
                                    db="fanxian",
                                    charset="utf8")
        self.cursor = self.db.cursor()

    def execute_sql(self,sql):
        print '执行的sql是:' + sql
        # try:
        self.cursor.execute(sql)
        self.db.commit()
        results = self.cursor.fetchall()
        return results
        # except Exception as e:
        #     print e


   # def close_db(self):
   #     self.db.close()
   #
   # def close_cursor(self):
   #      self.cursor.close()
   # def mycommit(self):
   #     self.db.commit()

if __name__ == '__main__':
    db=Dboperation()
    sql="SELECT NAME, user_id, phone,create_time,update_time,LEVEL, parent_user_id   FROM fanxian.union_leader WHERE  user_id='类型1' "
    re=db.execute_sql(sql)
    print str(re)










