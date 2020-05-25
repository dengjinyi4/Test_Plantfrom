import requests
from threading import Thread
from contextlib import closing

import json
import time

#
# class TestT(Thread):
#
#     def __init__(self):
#         super(TestT, self).__init__()
#
#         self.s = requests.session()
#         self.IsStop = False
#
#     def stop(self):
#         self.p.connection.close()
#         self.s.close()
#         self.IsStop = True
#
#     def run(self):
#         t = time.time()
#
#         # self.p = self.s.get('https://display.adhudong.com/site_login_ijf.htm?app_key=adhu450c59063e0341b8', stream=True, timeout=10)
#         self.p = self.s.get('https://display.adhudong.com/site_login_ijf.htm?app_key=adhu450c59063e0341b8', stream=True, timeout=10)
#         print time.time()-t
#
#         with closing(self.p) as r:
#             print time.time()-t
#
#             data = ''
#
#             for chunk in r.iter_content(4096):
#                 if self.IsStop : return None
#                 data += chunk
#
#             print json.loads(data)
#
#         print time.time()-t
#
#
# t = TestT()
# t.start()
# t.join(30)
# t.stop()
# t.join()

if __name__ == '__main__':

    # print "*"*80
    # add=lambda x,y:x+y
    # result=add(1,3)
    # print result
    # tmplist=[2,4,6,8,9]
    # result=filter(lambda x:x>4,tmplist)
    # print result
    # array = [{"age":40,"name":"e"},{"age":25,"name":"b"},{"age":40,"name":"c"}]
    # result = sorted(array,key=lambda x:(x["name"]))
    # print result
    # result=reduce(lambda a,b:a+b, [1, 2, 3, 4, 5, 6, 7, 8, 9])
    # print result
    #

    tmplist=[1,2,3,4,5]
    x=[i*2 for i in tmplist if i<4]
    print x
    newtmplist=[]
    for i in tmplist:
        if i<4:
            newtmplist.append(i*2)
    print newtmplist

