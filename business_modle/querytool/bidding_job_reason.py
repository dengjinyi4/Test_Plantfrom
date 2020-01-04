#!/usr/bin/env python
#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
__author__ = 'jinyi'
from business_modle.querytool import db
from business_modle.querytool import bidding_analysis
import threading,time

# 装饰器-计算方法的耗时
def decorator(func):
    def wrapper(me_instance):
        start_time = time.time()
        print '开始时间：{}'.format(str(start_time))
        func(me_instance)
        end_time = time.time()
        print '任务--{}--耗时{}秒'.format(func.func_code.co_names[6],str(end_time - start_time))
    return wrapper
# 更新广告位点击id
class Job_updateAdzoneclickids(threading.Thread):
    # def __init__(self,*args,**kwargs):
    def __init__(self,jobid):
        super(Job_updateAdzoneclickids,self).__init__()
        self.__flag=threading.Event()
        self.__flag.set()
        self.__running=threading.Event()
        self.__running.set()
        self.jobid=jobid
    @decorator
    def run(self):
        j=jobreason(self.jobid)
        while self.__running.isSet():
            self.__flag.wait()
            j.update_job_adzoneclickids()
            time.sleep(1)
            self.stop()
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
# 根据广告位点击id更新过滤原因
class Jobresult(threading.Thread):
    # def __init__(self,*args,**kwargs):
    def __init__(self,jobid):
        super(Jobresult,self).__init__()
        self.__flag=threading.Event()
        self.__flag.set()
        self.__running=threading.Event()
        self.__running.set()
        self.jobid=jobid
    @decorator
    def run(self):
        j=jobreason(self.jobid)
        while self.__running.isSet():
            self.__flag.wait()
            # print '任务开始运行'
            # print '获取原因'
            # starttime=time.time()
            j.update_job_result()
            # endtime=time.time()
            # print '任务update_job_result耗时{}秒'.format(str(endtime-starttime))
            # time.sleep(1)
            self.stop()
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
        # 将任务更新为 获取广告位点击id正在运行
        self.update_jobrunstatus(2)
        # 查出来所有的adzonclickids
        adzonclickids=db.selectsql('devvoyager',tmpsql)
        # print adzonclickids
        adzonclickids=self.tuptostr(adzonclickids)
        # 更新到job_ad_reason
        updatetmpsql='''UPDATE test.job_ad_reason SET adzone_click_ids='{}' where id={}'''.format(str(adzonclickids),self.jobid)
        try:
            r=db.execsql('testtest',updatetmpsql)
        except Exception as e:
            print e.message
            return False,e.message
        # 将任务更新为 获取广告位点击id完成
        self.update_jobrunstatus(3)
        return True,r
    #     根据广告位点击ids更新广告过滤原因，result_key,result_value
    def update_job_result(self):
        if(len(self.job[0][4])<8):
            print '没有广告位点击id'
            return False
        else:
            # 将任务更新为 获取广告位点击id正在运行
            self.update_jobrunstatus(4)
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
            self.update_jobrunstatus(5)
            print 11111111111111111
            print r
            return 111111111111111111111
    #     根据jobid返回任务信息
    def get_jobadreason(self):
        return self.job
    #     根据jobid返回结果值
    def get_result(self):
        tmpresult={}
        result_key=str(self.job[0][5]).split(',')
        result_value=str(self.job[0][6])
        tmpresult['result_key']=result_key
        tmpresult['result_value']=result_value
        return tmpresult
    def update_jobrunstatus(self,status):
        tmpsql='''UPDATE job_ad_reason SET run_status={} where id={}'''.format(status,self.jobid)
        result=db.execsql('testtest',tmpsql)
        return result


if __name__ == '__main__':

    # j=Job_updateAdzoneclickids(52)
    # j.start()



    r=Jobresult(52)
    r.start()

    # start = time.time()
    # print 12*'fff'
    # time.sleep(1)
    # elapsed = (time.time() - start)
    # print elapsed


    # print ','.join(person_dev_group)
    # job=Job_updateAdzoneclickids(3)
    # job=Jobresult(3)
    # x=job.start()
    # print 'zouzzzzzzzzzzzzzzzzzzzzzz'
    # # print x
    # print 'zouzzzzzzzzzzzzzzzzzzzzzz'
    # str1='fdaf1111111111111\'{}\''.format('ddd')
    # print str1
    # print 'job start'*5
    # time.sleep(3)
    # job.pause()
    time.sleep(3)
    # job.resume()
    # time.sleep(4)
    # job.pause()
    # time.sleep(1)
    # job.resume()
    # time.sleep(3)
    # job.stop()
