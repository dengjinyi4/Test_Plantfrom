# -*- coding: utf-8 -*-
# @Time    : 2019/7/16 10:17
# @Author  : wanglanqing

from business_modle.querytool.utils.db_info import *
import requests
import time
import random
import threading


class LoopAdDatas(threading.Thread):
    def __init__(self,adzone_id, loop_count):
        super(LoopAdDatas, self).__init__()
        self.__flag = threading.Event()
        self.__flag.set()
        self.__running = threading.Event()
        self.__running.set()
        self.adzone_id = adzone_id
        self.loop_count = loop_count


    def run(self):
        if self.loop_count>0:
            for i in range(self.loop_count):
                t1 = time.time()
                SAD = SimulateAdDatas(self.adzone_id)
                SAD.lottery()
                t2 = time.time()
                print '******单次执行时长**********'
                print t2-t1
            self.stop()

    def stop(self):
        self.__flag.set()
        self.__running.clear()

class SimulateAdDatas(object):
    def __init__(self,adzone_id):
        self.db = DbOperations()
        self.s = requests.session()
        self.adzoneId = adzone_id
        self.adzoneUrl = "https://apidisplay.adhudong.com/node/site_login_ijf.htm"
        self.user_agent=[
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 6.0.1; vivo Y66 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/66.0.3359.126 MQQBrowser/6.2 TBS/044807 Mobile Safari/537.36 webviewversion/3030",
            "Mozilla/5.0 (Linux; Android 8.1.0; vivo Y85A Build/OPM1.171019.011; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 11_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15F79 yuedong AppVersion/4.6.7 OSVersion/11.4 DeviceType/iPhone X",
            "Mozilla/5.0 (iPad; CPU OS 12_3_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 JYWebInfo channelid/1 clientid/11 isJailbreak/0 lang/zh-Hans-CN ver/8.1",
            "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:38.0) Gecko/20100101 Firefox/38.0"
        ]

        headers = {'User-Agent': random.choice(self.user_agent)}
        self.s.headers.update(headers)
        app_key = self.get_app_key()
        self.post_json = {
            "app_key": app_key,
            "thirdPartJson": "{}",
            "ip": "172.16.146.61",
            "node_server_name": "display.adhudong.com"
        }
        re = (self.s.get(self.adzoneUrl,params=self.post_json)).json()
        print '=====广告位点击url is ====='
        print re
        self.act_id = re['data']['actId']
        self.adzone_click_id = re['data']['logId']
        self.token = re['data']['token']
        self.ctm_code = re['data']['ctm_code']
        self.act_click()

    def act_click(self):
        '''
        活动点击，等同于循环次数
        :return:
        '''
        act_click_url = "https://apidisplay.adhudong.com/node/activity/{}.htm".format(self.act_id)
        post_json = {
            "adzoneId": self.adzoneId,
            "logId":self.adzone_click_id,
            "ip":"172.16.145.66",
            "node_server_name":"display.adhudong.com"
        }
        re = self.s.get(act_click_url, params=post_json)
        # print '====== act_click url is: ======='
        # print re.url

    def user_lottery_info(self):
        '''
        剩余抽奖次数接口
        :return:
        '''
        user_lottery_url = "https://display.adhudong.com/new/api/user_lottery_info.htm"
        post_json = {
            "act_id" :self.act_id,
            "adzoneId" : self.adzoneId,
            "timeSign" : int(time.time()*1000),
            "ctm_code" : self.ctm_code,
        }
        try:
            re = (self.s.get(user_lottery_url,params=post_json)).json()
        except Exception as e:
            raise e
        print '===== 剩余抽奖次数url is ====='
        print re
        return re['data']['lottery_left_times']


    def lottery(self):
        '''
        调用抽奖接口，抽中幸运将，则进行广告点击
        :return:
        '''
        flag =1
        # x =0
        while flag != 0 :
            time.sleep(random.randint(1, 3))
            lottery_left_times = self.user_lottery_info()
            if lottery_left_times >= 1:
                # x = x+1
                lottery_url = "https://display.adhudong.com/new/api/lottery.htm"
                post_json = {"act_id": self.act_id,
                     "adzone_click_id":self.adzone_click_id,
                     "device":"android",
                     "token":self.token,
                     "ctm_code":self.ctm_code,
                     "ip":"172.16.146.61",
                     "node_server_name":"display.adhudong.com",
                     "referer":"通过调用抽奖接口，造抽奖数据"}
                #调用抽奖接口
                re = (self.s.get(lottery_url,params=post_json)).json()
                # print re['data']
                # print '==== 广告抽奖url is ====='
                # print re.url
                #如果抽奖接口返回幸运奖(award_type=7),则进行广告点击
                try:
                    if re['data']['award_type'] == 7:
                        ad_click_url = re['data']['ad']['ad_url']
                        self.s.get(ad_click_url)
                except Exception as e:
                    raise e
            else:
                flag =0
        # print x


    def get_app_key(self):
        app_key_sql = '''select app_key from voyager.base_adzone_info where id={}'''.format(self.adzoneId)
        app_key = self.db.execute_sql(app_key_sql)[0][0]
        self.db.close_cursor()
        self.db.close_db()
        return app_key

if __name__=='__main__':
    LAD = LoopAdDatas(1869,5)
    LAD.run()