#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
__author__ = 'jinyi'
from business_modle.querytool import db
from business_modle.querytool import bidding_analysis
import threading,time
class Job(threading.Thread):
    def __init__(self,*args,**kwargs):
        super(Job,self).__init__(*args,**kwargs)
        self.__flag=threading.Event()
        self.__flag.set()
        self.__running=threading.Event()
        self.__running.set()
    def run(self):
        while self.__running.isSet():
            self.__flag.wait()
            print '任务开始运行'
            print time.time()
            time.sleep(1)
    def pause(self):
        print '任务暂停'
        print time.time()
        self.__flag.clear()
    def resume(self):
        print '任务重新启动'
        self.__flag.set()
    def stop(self):
        print '任务停止'
        self.__flag.set()
        self.__running.clear()

class jobreason(object):
    # 所有的任务信息
    # job=''
    # 任务id
    # jobid=''
    def __init__(self,id):
        self.jobid=id
        sql='''SELECT * from test.job_ad_reason where id={};'''.format(self.jobid)
        self.job=db.selectsql('testtest',sql)
    #元祖转成字符串(('B0H3CDC01J7UNK3CZL',), ('B0H0BDC11J7UNJ9CQR',), ('B0H0BDC01J7UNFE1B6',))->B0H3CDC01J7UNK3CZL,B0H0BDC11J7UNJ9CQR,B0H0BDC01J7UNFE1B6
    def tuptostr(self,tmptup):
        print len(tmptup)
        tmplist=[]
        for i in tmptup:
            tmplist.append(','.join(i))
        tmplist=','.join([str(x) for x in tmplist])
        return tmplist
    #  根据sql查出来对应的adzoneclickid集合，并更新到任务表
    def update_job_adzoneclickids(self):
        tmpsql=str(self.job[0][3])
        print tmpsql
        # 查出来所有的adzonclickids
        adzonclickids=db.selectsql('devvoyager',tmpsql)
        # print adzonclickids
        adzonclickids=self.tuptostr(adzonclickids)
        # 更新到job_ad_reason
        updatetmpsql='''UPDATE test.job_ad_reason SET adzone_click_ids='{}' where id={}'''.format(str(adzonclickids),self.jobid)
        try:
            r=db.execsql('testtest',updatetmpsql)
            return True,r
        except Exception as e:
            print e.message
            return False,e.message
    def update_job_result(self):
        if(len(self.job[0][4])<8):
            print '没有广告位点击id'
            return False
        else:
            # 将元祖转换成列表
            adzoneclickids=str(self.job[0][4]).split(',')
            result=bidding_analysis.allorderdit(ad_order_id=str(self.job[0][2]),adzone_click_id=adzoneclickids,myenv='dev')
            # 返回字典中‘广告位点击id为’的value为list，在后期统计报表中用不到，移除
            result.pop(str('广告位点击id为'))
            tmpkey=','.join(list(result.keys())).replace('//','')
            tmpvalues=str(list(result.values())).replace('//','')
            updatetmpsql='''UPDATE test.job_ad_reason SET result_key=\"{}\",result_value=\"{}\" where id={}'''.format(tmpkey,tmpvalues,self.jobid)
            # 把订单不出现原因更新到数据库
            r=db.execsql('testtest',updatetmpsql)
            print 11111111111111111
            print r
            return 111111111111111111111


if __name__ == '__main__':
    # print job(3)
    # j=jobreason(3)
    # print j.update_job_adzoneclickids()
    # print j.update_job_result()
    print 111

    person_dev_group ={'name': '菜鸟教程', 'alexa': 10000, '地址 ':'www.runoob.com'}
    # print type(person_dev_group.keys())
    tmp11=person_dev_group.pop(str("地址 "))
    print person_dev_group

    # print ','.join(person_dev_group)
    # job=Job()
    # job.start()
    # print 'job start'*5
    # time.sleep(3)
    # job.pause()
    # time.sleep(3)
    # # job.resume()
    # # time.sleep(4)
    # job.pause()
    # time.sleep(1)
    # job.resume()
    # time.sleep(3)
    # job.stop()
