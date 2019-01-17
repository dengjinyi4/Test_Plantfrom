import requests
from threading import Thread
from contextlib import closing

import json
import time


class TestT(Thread):

    def __init__(self):
        super(TestT, self).__init__()

        self.s = requests.session()
        self.IsStop = False

    def stop(self):
        self.p.connection.close()
        self.s.close()
        self.IsStop = True

    def run(self):
        t = time.time()

        # self.p = self.s.get('https://display.adhudong.com/site_login_ijf.htm?app_key=adhu450c59063e0341b8', stream=True, timeout=10)
        self.p = self.s.get('https://display.adhudong.com/site_login_ijf.htm?app_key=adhu450c59063e0341b8', stream=True, timeout=10)
        print time.time()-t

        with closing(self.p) as r:
            print time.time()-t

            data = ''

            for chunk in r.iter_content(4096):
                if self.IsStop : return None
                data += chunk

            print json.loads(data)

        print time.time()-t


t = TestT()
t.start()
t.join(30)
t.stop()
t.join()