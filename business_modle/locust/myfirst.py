__author__ = 'emar0901'
# from locust import HttpLocust, TaskSet, task
from locust import HttpLocust, TaskSet,task
import subprocess,time

class MyTasks(TaskSet):
    @task
    def one_task(self):
        print ('12132123123123')
        self.client.get('/media/query/')


class RunTasks(HttpLocust):
    task_set = MyTasks
    host = "http://test.ebg.com"
    min_wait = 2000
    max_wait = 5000
if __name__ == '__main__':
    # subprocess.Popen("locust -f myfirst.py",shell=True)
    starttime=time.time()
    tmplist=[]
    for i in range(20011101):
        if i%2==0:
            tmplist.append(i)
    print  time.time()-starttime

    newtime=time.time()
    tmp=[x  for x in range(20011101) if x%2==0]
    print time.time()-newtime
