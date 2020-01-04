# -*- coding: utf-8 -*-
# @Time    : 2020/01/04 13:43
# @Author  : dengjinyi
import schedule,datetime,time
def job(t):
    t=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print t
    f=open('{0}.txt'.format(datetime.datetime.now().strftime('%Y-%m-%d%H%M%S')),'w+')
    f.write(t+'\n')
    f.close()
    print t


if __name__ == '__main__':
    schedule.every(5).seconds.do(job,1111)
    schedule.every(5).seconds.do(job,22222)
    while True:
        schedule.run_pending()
        time.sleep(1)