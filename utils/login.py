#!/usr/bin/env python
#coding=utf-8
__author__ = 'jinyi'
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from business_modle.querytool import db
from flask import g,request
import socket
class login(object):
    def __init__(self,username='',password='',REMOTE_ADDR='',HTTP_HOST='',method=''):
        self.username=username
        self.password=password
        self.REMOTE_ADDR=REMOTE_ADDR
        self.HTTP_HOST=HTTP_HOST
        self.method=method
    def loginuser(self):
        # hostname = socket.getfqdn(socket.gethostname(  ))
        HTTP_HOST= socket.getfqdn(socket.gethostname(  ))
        # # ip=socket.gethostbyname(hostname)
        # ip= request.META['REMOTE_ADDR']
        # tmpsql="SELECT count(1) from test.testuser where username=\'%s\' and pass=\'%s\'"%(str(username),str(password))
        tmpsql="SELECT id,username from test.testuser where username='{0}' and pass='{1}' and status=1".format(str(self.username),str(self.password))
        r=db.selectsql('testtest',tmpsql)
        # 更新下登录时间
        updatesql="UPDATE test.testuser set login_time=current_timestamp,hostname='{}',ip='{}' where username='{}' ".format(HTTP_HOST,self.REMOTE_ADDR,str(self.username))
        insertsql='''INSERT INTO `test`.`user_login_log` (`username`, `ip`, `method`) VALUES ('{username}', '{ip}', '{method}');'''.format(username=self.username,ip=self.REMOTE_ADDR,method='test')
        db.execsql('testtest',updatesql)
        db.execsql('testtest',insertsql)
        return r
    def user_log(self):
        insertsql='''INSERT INTO `test`.`user_login_log` (`username`, `ip`, `method`) VALUES ('{username}', '{REMOTE_ADDR}', '{method}');'''.format(username=self.username,REMOTE_ADDR=self.REMOTE_ADDR,method=self.method)
        db.execsql('testtest',insertsql)
        return 1
if __name__ == '__main__':
    print 1
    # x=loginuser('dengjinyi','123')
    # print x
    # REMOTE_ADDR = request.META['REMOTE_ADDR'].split(':')[0]

    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(('8.8.8.8', 80))
    # ip = s.getsockname()[0]
    # print 'ipis %s'%ip
    # print s.getsockname()

    # print REMOTE_ADDR