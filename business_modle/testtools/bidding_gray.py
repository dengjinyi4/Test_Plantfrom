# encoding=utf-8
__author__ = 'aidinghua'

import requests
import json
from utils.db_info import *
import time,datetime
import random
import string
# import schedule



#获取日期
requests.packages.urllib3.disable_warnings()

class Bidding_gray(object):

    def __init__(self,env):
        if env=='test':
            self.db=DbOperations(True)
            self.appkey='adhu225e7fc828c248b2'
            self.adzone_id=98
            self.ip_display='101.254.242.11:17081'
            self.ip_bidding='101.254.242.11:17091'
            param={"app_key":self.appkey,"thirdPartJson":"{}","ip":"172.16.144.19","node_server_name":"display.adhudong.com"}
            url = "http://{}/node/site_login_ijf.htm".format(self.ip_display)
            self.re=requests.get(url,params=param)
            self.adzone_click_id=self.re.json()['data']['logId']
            print self.adzone_click_id
            self.act_id=self.re.json()['data']['actId']
            time.sleep(3)
            self.act_click()
            time.sleep(3)
            url=self.lottery()
            url1=url.split('.com',1)[1]
            urlnew='http://'+self.ip_bidding+url1
            # param={"positionId":"1","logType":"2"}
            click=requests.get(urlnew,params=param)



        else :
            self.db=DbOperations(False)
            self.appkey='adhu1abc6dd46a8a4dbb'
            self.adzone_id=4620
            self.ip_display='123.59.17.106:17280'
            self.ip_bidding='123.59.17.106:17200'
            param={"app_key":self.appkey,"thirdPartJson":"{}","ip":"172.16.144.19","node_server_name":"display.adhudong.com"}
            url = "http://{}/node/site_login_ijf.htm".format(self.ip_display)
            self.re=requests.get(url,params=param)
            self.adzone_click_id=self.re.json()['data']['logId']
            print self.adzone_click_id
            self.act_id=self.re.json()['data']['actId']
            time.sleep(3)
            self.act_click()
            time.sleep(3)
            url=self.lottery()
            url1=url.split('.com',1)[1]
            urlnew='http://'+self.ip_bidding+url1
            # param={"positionId":"1","logType":"2"}
            click=requests.get(urlnew,params=param)



    def tmpdaylist(self,days):

        d = datetime.datetime.now()

        timedate_from = d+ datetime.timedelta(days=-int(days))

        timedate_from = str(timedate_from)[0:10]

        daylist = timedate_from.replace('-','')

        return daylist

    def timestamp(self):
        # stamp = int(time.time())
        stamp = int(round(time.time()*1000))
        return stamp


    def get_date(self):

        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


    def get_datetime(self):

        return datetime.datetime.now().strftime("%Y%m%d")

    def get_month(self):

        mon = datetime.datetime.now().month

        if  mon<10:
            return "0"+mon
        else:
            return mon

##校验广告位点击日志

    def check_adzone_click(self):

        sql='''SELECT
              act_id 活动ID,
              adzone_id 广告位ID,
              ip IP,
              create_time 创建时间,
              media_id 媒体ID,
              master_id 站长ID,
              (
                CASE
                  STATUS
                  WHEN '1'
                  THEN '有效'
                  WHEN '2'
                  THEN '无效'
                  ELSE '废弃'
                END
              ) AS 状态,
              adzone_click_id 广告位点击ID
            FROM voyagerlog.adzone_click_log{} WHERE adzone_click_id='{}' '''.format(self.tmpdaylist(0),self.adzone_click_id)

        re=self.db.execute_sql(sql)

        return re

##检验广告展现日志

    def check_adshow(self):

        sql='''   SELECT
            ad_choosen_tag 广告展现唯一标识,
            media_id 媒体ID,
            adzone_id 广告位ID,
            act_id 活动ID,
            position_id 坑位ID,
            ad_order_id 广告订单ID,
            ad_creative_id 广告创意ID,
            ip IP,
            url 创意url,
            (CASE charge_type
            WHEN '2' THEN 'CPC'
            WHEN '4' THEN 'OCPA'
            ELSE 'CPM' END)  AS 出价方式,
            charge_amount 扣费金额,
            create_time 创建时间,
              (
            CASE
              STATUS
              WHEN '1'
              THEN '有效'
              WHEN '2'
              THEN '无效'
              ELSE '废弃'
            END
          ) AS 状态,
            adzone_click_id 广告位点击ID

            FROM voyagerlog.ad_show_log{} WHERE adzone_click_id='{}' '''.format(self.tmpdaylist(0),self.adzone_click_id)

        re = self.db.execute_sql(sql)
        print sql
        return re




##校验广告点击日志
    def check_adclick(self):

        sql=''' SELECT
              adzone_id 广告位ID,
              act_id  活动ID,
              position_id 坑位ID,
              ad_order_id 订单ID,
              ad_creative_id 创意ID,
              ip IP地址,
              (CASE charge_type
              WHEN '2' THEN 'CPC'
              WHEN '4' THEN 'OCPA'
              ELSE 'CPM' END)  AS 出价方式,
              charge_amount 扣费,
              create_time 创建时间,
              occurrence 位次,
              (CASE STATUS
              WHEN '1' THEN '有效'
              WHEN '2' THEN '无效'
              ELSE '废弃' END) AS 状态,
              adzone_click_id 广告位点击ID,
              system_income 平台收益,
              media_income_cash 媒体现金收益,
              media_income_award 媒体奖励收益
              FROM voyagerlog.ad_click_log{} WHERE adzone_click_id='{}' '''.format(self.tmpdaylist(0),self.adzone_click_id)
        time.sleep(3)
        re=self.db.execute_sql(sql)
        return re
##校验抽奖日志
    def check_lottery(self):

        sql=''' SELECT
              adzone_id 广告位ID,
              act_id  活动ID,
              position_id 坑位ID,
              order_id 订单ID,
              ip IP地址,
              create_time 创建时间,
              occurrence 位次,
              (CASE STATUS
              WHEN '1' THEN '有效'
              WHEN '2' THEN '无效'
              ELSE '废弃' END) AS 状态,
              (CASE act_award_type
              WHEN '6' THEN '谢谢参与'
              WHEN '7' THEN '幸运奖'
              ELSE '其他' END) AS 奖品类型,
              adzone_click_id 广告位点击ID from  voyagerlog.lottery_click_log{} WHERE adzone_click_id='{}' '''.format(self.tmpdaylist(0),self.adzone_click_id)
        time.sleep(3)
        re=self.db.execute_sql(sql)
        return re




##校验活动点击日志

    def check_act_click(self):

        sql=''' SELECT
          act_id 活动ID,
          adzone_id 广告位ID,
          ip IP,
          create_time 创建时间,
          media_id 媒体ID,
            (
            CASE
              STATUS
              WHEN '1' THEN '有效'
              WHEN '2' THEN '无效'
              ELSE '废弃'
            END
          ) AS 状态,
          adzone_click_id 广告位点击ID
          FROM voyagerlog.act_click_log{} WHERE adzone_click_id='{}' '''.format(self.tmpdaylist(0),self.adzone_click_id)

        re=self.db.execute_sql(sql)
        return re









    def adzone_click(self):
        param={"app_key":self.appkey,"thirdPartJson":"{}","ip":"172.16.144.19","node_server_name":"display.adhudong.com"}

        # url = "https://apidisplay.adhudong.com/node/site_login_ijf.htm"
        url = "http://{}/node/site_login_ijf.htm".format(self.ip_display)
        re = requests.get(url,params=param)
        print "==========adzone_click==============="
        print re.json()
        # adzone_click_id=re.json()['data']['logId']
        return  re

    def act_click(self):

        param={"ip":"172.16.144.19","node_server_name":"display.adhuodong.com"}
        param['ctm_code']=self.re.json()['data']['ctm_code']
        param['logId']=self.re.json()['data']['logId']
        param['adzoneId']=self.re.json()['data']['adzoneId']


        url="http://{}/node/activity/{}.htm".format(self.ip_display,self.act_id)

        re=requests.get(url,params=param)
        print re.url
        return re


    def lottery(self):
        # re_adzone = self.adzone_click()
        #url=http://display.eqigou.com/new/api/lottery.htm?act_id=577&adzone_click_id=B3W1CD6H1KCPK75VHD&device=IOS&token=&temp_name=rotate_drivingTest&ctm_code=Mi8vMTYxMC8vMi8vMi8vNzk4NjMvLzE1ODk3ODE2NTczNzgvL2Y0NWRkNzBiNGI0NGYwNjc3ZmQ4YzAzNGRiOTExNjIzLy9lNjMwZjNjYmI1NzM%3D
        param={"ip":"172.16.144.19","device":"IOS","token":"","temp_name":"rotate_drivingTest","node_server_name":"display.adhuodong.com","isIntercept":"1"}
        param['act_id']=self.re.json()['data']['actId']
        param['adzone_click_id']=self.re.json()['data']['logId']
        param['ctm_code']=self.re.json()['data']['ctm_code']
        url="http://{}/node/lottery.htm".format(self.ip_display)
        # url="http://{}/new/api/lottery.htm".format(self.ip_display)
        re= requests.get(url,params=param)
        print re.json()
        print "==========lottery==============="
        return re.json()['data']['ad']['ad_url']
#
# act_id=577&adzone_click_id=B3W1CD6H1KCPSF05Z5&device=IOS
# &token=&temp_name=rotate_drivingTest&
# ctm_code=Mi8vOTgvLzIvLzIvLzcwMDE4Ly8xNTg5Nzg2NjI2OTE2Ly83OTczMmE0MDg5OTNiZGNmOTRiYjkyZjk2MzgxMzZlYS8vZTg1OTNhZmNkZDQ=
# &ip=172.16.144.19&node_server_name=display.eqigou.com&
# referer=https://display.eqigou.com/new/rotate_drivingTest.html?logId=B3W1CD6H1KCPSF05Z5
# &adzoneId=98&actId=577&ref=&mediaId=40&ctm_code=Mi8vOTgvLzIvLzIvLzcwMDE4Ly8xNTg5Nzg2NjI2OTE2Ly83OTczMmE0MDg5OTNiZGNmOTRiYjkyZjk2MzgxMzZlYS8vZTg1OTNhZmNkZDQ=&isIntercept=1


    #调用广告展现接口


    # http://172.16.105.11:17091/ad_bidding.do?pids=1&uniq_tag=11&ip=172.16.144.19&cookie=daf1222111ads&device=IOS&adzone_id=1610&pos_num=1_0&act_id=243
    def ad_show(self):
        ###试投订单时，'pos_num':'1_2'
        # re_adzone =  self.adzone_click()
        # re_lottery = self.lottery()
        print self.adzone_click_id
        param={'pids':1,'uniq_tag':23232112231,'ip':'172.16.144.19','cookie':'1sadsd222111','device':'IOS',
               'adzone_id':self.adzone_id,'pos_num':'1_0',
               'ua':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1'}
        # param['act_id']=self.re.json()['data']['actId']
        param['cookie']=self.re.json()['data']['ctm_code']
        param['adzone_id']=self.re.json()['data']['adzoneId']
        param['act_id']=self.re.json()['data']['actId']
        param['uniq_tag']=self.re.json()['data']['logId']
        # param['cookie']=''.join(random.sample(string.ascii_letters+string.hexdigits,20))
        # param['uniq_tag']=''.join(random.sample(string.acii_letters+string.hexdigits,10))
        url = "http://{}/ad_bidding.do".format(self.ip_bidding)
        #s=requests.session()
        re=requests.get(url,params=param)
        print "==========ad_show==============="
        print re.json()
        return re,param['cookie']

    #调用广告点击接口

    # def ad_click(self):

    #     re_adshow,usercookie=self.ad_show()
    #     print 'sssssssssssss'
    #     print re_adshow.json()
        # param={'ip':'172.16.144.19','agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1',
        #        'refer':'https://display.adhudong.com/new/rotary_table_iphonex.html?logId=B3W1CD6H1IJW9MY8RL','adZoneId':self.adzone_id,'actId':577,'ref':'','mediaId':86,
        #        'ctm_code':'Mi8vMTgxNy8vMi8vMi8vODA4NTEvLzE1Mzg5OTA4OTI3ODkvLzZjYWYwZjg4MDliMTQ0OTk2NGQwZDk1NDNhNmY5ZmIyLy9jNTc5NjFhYzZlZjg=','isIntercept':'1','adzone_show_tag':'null','adPlanId':237,'adOrderId':29121,
        #        'adCreativeId':35256,'userCookie':'','adLinkUrl':'http://m.baidu.com/','chargeType':2,'advertiserId':4761,'adChoosenTag':'D3W1CD6R1IJW9NHJ7L','adzoneClickId':'B3W1CD6H1IJW9MY8RL','invalid_message':'',
        #        'isCharge':1,'logType':2,'status':1,'positionId':1,'occurrence':0,'reach_time':self.timestamp(),'award_type':7,
        #        'award_type_id':0,'open_id':'null','appid':'','path':'','create_time':self.timestamp()}
        # param['adOrderId']=re_adshow.json()['data']['{"id":1,"positionSize":"640x300","positionType":1,"occurrenceTime":0}'][0]['adOrder']['id']
        # param['chargeType']=re_adshow.json()['data']['{"id":1,"positionSize":"640x300","positionType":1,"occurrenceTime":0}'][0]['adOrder']['paymentMode']
        # param['adCreativeId']=re_adshow.json()['data']['{"id":1,"positionSize":"640x300","positionType":1,"occurrenceTime":0}'][0]['adCreative']['id']
        # param['advertiserId']=re_adshow.json()['data']['{"id":1,"positionSize":"640x300","positionType":1,"occurrenceTime":0}'][0]['adOrder']['advertiserId']
        # param['adChoosenTag']=re_adshow.json()['data']['{"id":1,"positionSize":"640x300","positionType":1,"occurrenceTime":0}'][0]['tag']
        # param['adLinkUrl'] =re_adshow.json()['data']['{"id":1,"positionSize":"640x300","positionType":1,"occurrenceTime":0}'][0]['linkUrl']
        # param['adPlanId'] = re_adshow.json()['data']['{"id":1,"positionSize":"640x300","positionType":1,"occurrenceTime":0}'][0]['adOrder']['planId']
        # param['userCookie']=usercookie
        # param['mediaId']=1
        # url="http://{}/bridge.do".format(self.ip_bidding)
        # # re=requests.get(url,params=param,verify=False)
        # url=self.lottery()
        # print url[8:20]
        # re=requests.get(url)
        # return re.json()
        #
        # print "==========ad_click==============="
        # return url




if  __name__=='__main__':

    #调用广告位点击接口

        bidding_gray = Bidding_gray('test')
        # bidding_gray.ad_show()

        # ad_choosen_tag = bidding_gray.ad_click(4620,'adhu1abc6dd46a8a4dbb')

##线上环境
        # re1=bidding_gray.adzone_click()
        # bidding_gray.adzone_click()
        # bidding_gray.lottery()
        # bidding_gray.ad_click()
        # bidding_gray.ad_show()
        time.sleep(5)

        re1=bidding_gray.check_adzone_click()
        re2=bidding_gray.check_adshow()
        re3=bidding_gray.check_adclick()
        re4=bidding_gray.check_act_click()
        re5=bidding_gray.check_lottery()
##测试环境
        # re=bidding_gray.adzone_click('adhu225e7fc828c248b2')

        # re=bidding_gray.ad_show(4620,'adhu1abc6dd46a8a4dbb')


        print re1
        print re2
        print re3
        print re4
        print re5
        # print bidding_gray.check_click(ad_choosen_tag)
        # print bidding_gray.check_lottery(ad_choosen_tag)


