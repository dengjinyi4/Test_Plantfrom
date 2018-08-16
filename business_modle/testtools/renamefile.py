#encoding:utf8
import time,datetime,os
def filename():
    t = time.strftime('%Y-%m-%d-%H',time.localtime(time.time()))
    filename = 'log/log%s.txt' %(t)
    fp = file(filename, 'wb')
    f=open(filename,'a')
    f.write('test')
#每天一个日志，日志名字为日期 
def logrename():
    # 读取文件获取时间
    f=open('filename.txt')
    filename=f.readline()
    f.closed
    # print filename
    filename=datetime.datetime.strptime(filename,'%Y-%m-%d')
    now = datetime.datetime.now()
    # print now
    # print type(now)
    days=now-filename
    print days.days
    if days.days>=1:
        newfilename=str(now)[0:10]
        print 'rename'
        try:
            os.rename('f1.txt',str(filename)+'.txt')
            f1=open('filename.txt','w')
            f1.write(newfilename)
            f1.close()
        except Exception as e:
            print e
    else:
        print 'no'
if __name__ == '__main__':
    while True:
        logrename()
        print time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        time.sleep(300)

