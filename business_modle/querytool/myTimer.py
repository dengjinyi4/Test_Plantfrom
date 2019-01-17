import time
import schedule
import myjob as job
def hello():
    with open('log.txt','a') as f:
        tmptime=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        print 'time is {}'.format(tmptime)
        f.write(tmptime+'do ..........'+'\n')


if __name__ == "__main__":
    # schedule.every(2).seconds.do(hello)
    schedule.every(10).seconds.do(job.adzon2666)
    while True:
        schedule.run_pending()
        # time.sleep(1)