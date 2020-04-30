# -*- coding: utf-8 -*-
# @Time    : 2018/11/27 14:19
# @Author  : wanglanqing
from utils.db_info import *
from business_modle.querytool import db

class phoneVaild(object):
    def __init__(self,env='1'):
        env_dict = {'1':True,'0':False}
        self.db = DbOperations(env_value=env_dict[env])
        pass

    def get_valid_code(self):
        sql = "select PHONE,MSG,create_time from voyager.phone_send_record order by id desc limit 50"
        re = self.db.execute_sql(sql)
        # re='sss'
        return re

def getsql(db):
    if db=='voyager':
        tmpsql='select PHONE,MSG,create_time from voyager.phone_send_record order by id desc limit 50;'
        return tmpsql
    if db=='normandy':
        tmpsql='select PHONE,MSG,create_time from normandy.phone_send_record order by id desc limit 50;'
        return tmpsql
    if db=='egoufanli':
        tmpsql='SELECT PHONE,MSG,CREATE_TIME from fanxian.phone_send_record ORDER BY id DESC LIMIT 100;'
        return tmpsql

def get_phonevaild(env,mydb):
    tmpsql=getsql(mydb)
    if env=='test':
        if mydb=='voyager' or mydb=='normandy':
            result=db.selectsql('testvoyager',tmpsql)
        if mydb=='egoufanli':
            result=db.selectsql('egoufanlitest',tmpsql)
    if env=='dev':
        result=''
        if mydb=='voyager':
            result=db.selectsql('devvoyager',tmpsql)
        if mydb=='normandy':
            result=db.selectsql('nomandydev',tmpsql)
        if mydb=='egoufanlitest':
           result=''
    return result
if __name__ == '__main__':
    res=get_phonevaild('test','voyager')
    print res