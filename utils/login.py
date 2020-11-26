#!/usr/bin/env python
#coding=utf-8
__author__ = 'jinyi'
import sys,pyotp,qrcode
reload(sys)
sys.setdefaultencoding('utf8')
from business_modle.querytool import db
from flask import g,request
import socket,os,base64
class login(object):

    def __init__(self,username='',password='',REMOTE_ADDR='',HTTP_HOST='',method='',otppass='',imgurl='',ip=''):
        self.username=username
        self.password=password
        self.REMOTE_ADDR=REMOTE_ADDR
        self.HTTP_HOST=HTTP_HOST
        self.method=method
        self.otppass=otppass
        self.imgurl=imgurl
        self.ip=ip
    #     用户登录
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
    # 互动推平台跳转到测试平台登陆验证
    def loginvoyager(self):
        tmpsql='''SELECT * from voyager.um_user where USERNAME='{username}' and `PASSWORD`='{password}'
        '''.format(username=self.username,password=self.password)
        # 先写到测试环境
        r=db.selectsql('testvoyager',tmpsql)
        return len(r)
    def user_log(self):
        insertsql='''INSERT INTO `test`.`user_login_log` (`username`, `ip`, `method`) VALUES ('{username}', '{REMOTE_ADDR}', '{method}');'''.format(username=self.username,REMOTE_ADDR=self.REMOTE_ADDR,method=self.method)
        db.execsql('testtest',insertsql)
        return 1
    # otp登录
    def loginuserotp(self):
        HTTP_HOST= socket.getfqdn(socket.gethostname())
        tmpsql="SELECT id,username,isotp,isfirstotp from test.testuser where username='{0}' and pass='{1}' and status=1".format(str(self.username),str(self.password))
        r=db.selectsql('testtest',tmpsql)
        # 更新下登录时间
        if len(r)>0:
            insertsql='''INSERT INTO `test`.`user_login_log` (`username`, `ip`, `method`) VALUES ('{username}', '{ip}', '{method}');'''.format(username=self.username,ip=self.REMOTE_ADDR,method='test')
            if r[0][2]=='1':
                updatesql="UPDATE test.testuser set isfirstotp=0,login_time=current_timestamp,hostname='{}',ip='{}' where username='{}' ".format(HTTP_HOST,self.REMOTE_ADDR,str(self.username))
            else:
                updatesql="UPDATE test.testuser set login_time=current_timestamp,hostname='{}',ip='{}' where username='{}' ".format(HTTP_HOST,self.REMOTE_ADDR,str(self.username))
            # db.execsql('testtest',updatesql)
            db.execsql('testtest',insertsql)
        return r
    sec='base32secret32321'
    # 存放登录二维码图片
    def otppic(self):
        # sec='base32secret3232'
        # sec= base64.b32encode(os.urandom(10)).decode('utf-8')
        # topt=pyotp.TOTP(sec)
        sec_name=base64.b32encode(self.sec+self.username)
        qr_uri = pyotp.totp.TOTP(sec_name).provisioning_uri('TestPlatform({0})'.format(self.username))
        print qr_uri
        img = qrcode.make(qr_uri)
        imgurl='/static/qrcodepic/{0}.png'.format(self.username)
        # imgurl='../static/qrcodepic/{0}.png'.format(self.username)
        try:
            img.save(imgurl)
            # img.save('{0}.png'.format(self.username))
        except  Exception  as e:
            print e.message
        # imgurl='../../'+imgurl
        return imgurl

    def otppic1(self):
        # sec='base32secret3232'
        # sec= base64.b32encode(os.urandom(10)).decode('utf-8')
        # topt=pyotp.TOTP(sec)
        sec_name=base64.b32encode(self.sec+self.username)
        qr_uri = pyotp.totp.TOTP(sec_name).provisioning_uri('TestPlatform({0})'.format(self.username))
        print qr_uri
        img = qrcode.make(qr_uri)
        # img.get_image().show()
        path=os.getcwd()
        path=path+'/static/qrcodepic/{0}.BMP'.format(self.username)
        # imgurl='/static/qrcodepic/{0}.png'.format(self.username)
        # imgurl='../static/qrcodepic/{0}.png'.format(self.username)
        try:
            img.save(path)
            # img.save('{0}.png'.format(self.username))
        except  Exception  as e:
            print e.message
        # imgurl='../../'+imgurl
        return 1
    def otpverify(self):
        # sec='base32secret3232'
        # sec= base64.b32encode(os.urandom(10)).decode('utf-8')
        sec_name=base64.b32encode(self.sec+self.username)
        topt=pyotp.TOTP(sec_name)
        try:
            x=topt.verify(self.otppass)
        except Exception as e:
            print e.message
        if x:
            return True
        else:
            return False
    def ip_into_int(self):
        # 先把 192.168.1.13 变成16进制的 c0.a8.01.0d ，再去了“.”后转成10进制的 3232235789 即可。
        # (((((192 * 256) + 168) * 256) + 1) * 256) + 13
        return reduce(lambda x,y:(x<<8)+y,map(int,self.ip.split('.')))
    def is_internal_ip(self):
        ip = self.ip_into_int(self.ip)
        net_a = self.ip_into_int('10.255.255.255') >> 24
        net_b = self.ip_into_int('172.31.255.255') >> 20
        net_c = self.ip_into_int('192.168.255.255') >> 16
        return ip >> 24 == net_a or ip >>20 == net_b or ip >> 16 == net_c

if __name__ == '__main__':
    print 1
    x=login(username='dengjinyi',otppass=116846)
    # path=x.otppic()
    # x.otppic1()
    # print x.otpverify()
    tmp='test_760cae49c5e27063cfde241d0f0f35bf'
    tmp=base64.b64encode(tmp)
    print tmp
    tmp=base64.b64decode(tmp)
    print tmp
    # REMOTE_ADDR = request.META['REMOTE_ADDR'].split(':')[0]

    # s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # s.connect(('8.8.8.8', 80))
    # ip = s.getsockname()[0]
    # print 'ipis %s'%ip
    # print s.getsockname()

    # print REMOTE_ADDR