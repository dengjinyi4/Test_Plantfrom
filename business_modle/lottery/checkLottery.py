# -*- coding: utf-8 -*-
# @Time    : 2020/5/12 17:18
# @Author  : wanglanqing
#测试抽奖接口
import requests,json, time


class checkLotteryApi(object):
    def __init__(self, app_key, env):
        env_dict = {'1':'123.59.17.106:17280',
                    '0':'172.16.105.11:17081'}
        self.domain = env_dict[str(env)]
        self.result_list =[]
        self.result = {'data':self.result_list}
        #通过点击广告位接口，获取基本参数
        # self.adzone_url = 'https://apidisplay.{}/node/site_login_ijf.htm?app_key={}&thirdPartJson={}&ip=172.16.146.79' \
        self.adzone_url = 'http://{}/node/site_login_ijf.htm?app_key={}&thirdPartJson={}&ip=172.16.146.79' \
                     '&node_server_name=display.eqigou.com'.format(self.domain, app_key, '')
        print self.adzone_url
        self.s = requests.session()
        self.s.keep_alive = False
        self.adzone_url_re = self.s.get(self.adzone_url)
        self.isOk = False
        if  self.adzone_url_re.status_code == 200:
            self.adzone_url_re = self.adzone_url_re.json()
            self.isOk = True

    def analyze(self):
        position_api = {
            '1': self.lottery,
            '2': self.fallEnvelopes,
            '5': self.innerPromotion,
            '6': self.innerPromotion,
            '7': self.innerPromotion,
            '8': self.innerPromotion,
            '9': self.innerPromotion,
            '10': self.innerPromotion,
            '11': self.innerPromotion,
            '12': self.innerPromotion,
            '14': self.actGameLottery,
            '15': self.actGameLottery,
            '16': self.actGameLottery,
            '17': self.actGameLottery,
            '18': self.actGameLottery,
            '19': self.actGameLottery,
            '20': self.actGameLottery,
            '21': self.actGameLottery,
            '22': self.feePromotion,
            '23': self.feePromotion,
            '24': self.feePromotion,
            '25': self.feePromotion,
            '26': self.feePromotion,
            '27': self.picVedio,
            '28': self.picVedio,
            '29': self.picVedio,
            '30': self.picVedio
        }
        if self.isOk:
            #返回的为普通活动后，再根据/activity/接口，获取配置的坑位信息，养成坑位14~21无法根据该接口判断
            if self.adzone_url_re['code'] == 200 and self.adzone_url_re['data']['actId'] != 100:
                self.result['message'] = 'ok'
                self.adzone_id = self.adzone_url_re['data']['adzoneId']  # 广告位id
                self.act_id = self.adzone_url_re['data']['actId']   #活动id
                self.adzone_click_id = self.adzone_url_re['data']['logId']  #广告位点击id
                self.token = self.adzone_url_re['data']['token']   #token值
                self.ctm_code = self.adzone_url_re['data']['ctm_code']  #cookie
                self.device = 'android'  #活动id
                self.showPostionFee = str(self.adzone_url_re['data']['mediaInfo']['showPostionFee']).split(',')  #媒体支持的坑位
                self.temp_name = self.adzone_url_re['data']['locationAdress'].split('/new/')[1]  #还没解析完呢
                #调用activity接口，通过innerPosiList，posiList，pointss_wall_order_img，ads来判断坑位
                # activity_url = 'https://apidisplay.{}/node/activity/{}.htm?adzoneId={}&logId={}&ctm_code=' \
                activity_url = 'http://{}/node/activity/{}.htm?adzoneId={}&logId={}&ctm_code=' \
                               '{}&ip=172.16.146.79&node_server_name=display.eqigou.com'.\
                    format(self.domain, self.act_id, self.adzone_id,self.adzone_click_id ,self.ctm_code)
                activity_url_re = self.s.get(activity_url).json()
                #获取活动上的坑位信息
                activity_pos_list = []
                #获取活动免费坑位
                if 'innerPosiList' in  activity_url_re['data']:
                    innerPosiList_tmp = activity_url_re['data']['innerPosiList']
                    for i in innerPosiList_tmp:
                        activity_pos_list.append(str(i['id']))
                #获取活动其他坑位
                if 'posiList' in activity_url_re['data']:
                    posiList_tmp = activity_url_re['data']['posiList']
                    for i in posiList_tmp:
                        activity_pos_list.append(str(i['id']))

                #媒体控制2,4,22~26坑位，以上坑位用活动坑位在媒体坑位中遍历，匹配则调用，不匹配不调
                activity_pos_list.sort()
                for pos in activity_pos_list:
                    if pos == 2 or pos == 4 or (pos >21 and pos <27):
                        if pos in self.showPostionFee:
                            position_api[pos](pos)
                    else:
                        position_api[pos](pos)

                # #调用养成坑位
                # self.actGameLottery()

            #返回的为直跳100活动的处理
            elif self.adzone_url_re['code'] == 200 and self.adzone_url_re['data']['actId'] == 100:
                self.result['message'] = 'ok'
                if 'redirect_url' in self.adzone_url_re['data']:
                    self.result_list.append({'positionId':'1','url':self.adzone_url, 'result':'直跳100幸运奖'})
                else:
                    self.result_list.append({'positionId':'1','url':self.adzone_url, 'result': '直跳100谢谢参与'})
                self.result['data'] = self.result_list
                return self.result

        #返回的异常情况处理
            elif self.adzone_url_re['code'] == 303:
                    self.result['message'] = '303'
                    self.result_list.append({'positionId':'-1', 'url':self.adzone_url, 'result': '303,广告位无效！请检查环境，app_key是否正确'})
                    self.result['data'] = self.result_list
                    return self.result

        elif self.adzone_url_re.status_code == 502:
                self.result['message'] = '502'
                self.result_list.append({'positionId' : '-1' , 'url':self.adzone_url, 'result': '502,Bad Gateway,请重启apidisplay'})
                self.result['data'] = self.result_list
                return self.result
        else:
            self.result['message'] = self.adzone_url_re
            self.result['message'] = 'service not ok'
            self.result_list.append({'url':self.adzone_url})
            self.result['data'] = self.result_list
            return self.result
            pass
        return self.result

    def lottery(self, pos):
        #坑位1的抽奖
        re_temp = {}
        result_tmp = {}
        re_temp['positionId'] = int(pos)
        re_temp['result'] = result_tmp
        # lottery_url = 'https://display.{}/new/api/lottery.htm?act_id={}&adzone_click_id={}&token={}&ctm_code={}&device={}'.\
        lottery_url = 'http://{}/lottery.htm?act_id={}&adzone_click_id={}&token={}&ctm_code={}&device={}'.\
            format(self.domain, self.act_id, self.adzone_click_id, self.token, self.ctm_code, self.device)
        print lottery_url
        lottery_url_re = self.s.get(lottery_url).json()
        re_temp['url'] = lottery_url
        print lottery_url, lottery_url_re
        if lottery_url_re['code'] == 200 and lottery_url_re['data']:
            result_tmp['award_type'] = lottery_url_re['data']['award_type']
            if lottery_url_re['data']['award_type'] == 7:
                result_tmp['order_id'] = lottery_url_re['data']['ad']['order_id']
        else:
            result_tmp['re'] = lottery_url_re
        self.result_list.append(re_temp)


    def fallEnvelopes(self, pos):
        #坑位2的抽奖
        re_temp = {}
        result_tmp = {}
        re_temp['positionId'] = int(pos)
        re_temp['result'] = result_tmp
        # fallEnvelopes_url = 'https://display.{}/new/api/fallEnvelopes.htm?act_id={}&adzone_click_id={}&ctm_code={}&device={}'.\
        fallEnvelopes_url = 'http://{}/node/fallEnvelopes.htm?act_id={}&adzone_click_id={}&ctm_code={}&device={}&' \
                            'ip=172.16.146.79&node_server_name=display.eqigou.com'.\
            format(self.domain, self.act_id, self.adzone_click_id, self.ctm_code, self.device)
        print fallEnvelopes_url
        re_temp['url'] = fallEnvelopes_url
        fallEnvelopes_url_re = self.s.get(fallEnvelopes_url).json()
        print fallEnvelopes_url, fallEnvelopes_url_re
        if fallEnvelopes_url_re['code'] == 200 and fallEnvelopes_url_re['data']:
            result_tmp['award_type'] = fallEnvelopes_url_re['data']['award_type']
            if fallEnvelopes_url_re['data']['award_type'] == 7:
                result_tmp['order_id'] = fallEnvelopes_url_re['data']['ad']['ad_id']
        else:
            re_temp['result'] = fallEnvelopes_url_re['message']
        self.result_list.append(re_temp)

    def innerPromotion(self, pos):
        #坑位5~12的抽奖
        re_temp = {}
        result_tmp = {}
        re_temp['positionId'] = int(pos)
        re_temp['result'] = result_tmp
        # innerPromotion_url = 'https://display.{}/new/api/innerPromotion.htm?position_id={}&act_id={}&adzone_click_id={}&ctm_code={}'.\
        innerPromotion_url = 'http://{}/node/innerPromotion.htm?position_id={}&act_id={}&adzone_click_id={}&ctm_code={}&' \
                             'node_server_name=display.eqigou.com&ip=127.0.0.1'.\
            format(self.domain, int(pos), self.act_id, self.adzone_click_id, self.ctm_code)
        re_temp['url'] = innerPromotion_url
        print innerPromotion_url
        innerPromotion_url_re = self.s.get(innerPromotion_url).json()
        # print innerPromotion_url_re
        if innerPromotion_url_re['code'] == 200 and innerPromotion_url_re['data']:
            result_tmp['award_type'] = innerPromotion_url_re['data']['award_type']
            if innerPromotion_url_re['data']['award_type'] == 7:
                result_tmp['order_id'] = innerPromotion_url_re['data']['ad']['ad_id']
        else:
            re_temp['result'] = innerPromotion_url_re
        self.result_list.append(re_temp)

    def feePromotion(self, pos):
        #坑位22~26的抽奖
        re_temp = {}
        result_tmp = {}
        re_temp['positionId'] = int(pos)
        re_temp['result'] = result_tmp
        # feePromotion_url = 'https://display.{}/new/api/feePromotion.htm?position_id={}&act_id={}&adzone_click_id={}&ctm_code={}&device={}'.\
        feePromotion_url = 'http://{}/node/feePromotion.htm?position_id={}&act_id={}&adzone_click_id={}&ctm_code={}&' \
                           'device={}&node_server_name=display.eqigou.com&ip=127.0.0.1'.\
            format(self.domain, int(pos), self.act_id, self.adzone_click_id, self.ctm_code, self.device)
        re_temp['url'] = feePromotion_url
        feePromotion_url_re = self.s.get(feePromotion_url).json()
        print feePromotion_url, feePromotion_url_re
        if feePromotion_url_re['code'] == 200 and 'ad' in feePromotion_url_re['data']:
            result_tmp['award_type'] = feePromotion_url_re['data']['award_type']
            result_tmp['order_id'] = feePromotion_url_re['data']['ad']['ad_id']
        else:
            re_temp['result'] = '免费坑位，没有广告，谢谢参与'
        self.result_list.append(re_temp)

    def picVedio(self, pos):
        #坑位27~30的抽奖
        re_temp = {}
        result_tmp = {}
        re_temp['positionId'] = int(pos)
        re_temp['result'] = result_tmp
        # picVedio_url = 'https://display.{}/new/api/picVedio.htm?position_id={}&act_id={}&adzone_click_id={}&ctm_code={}&device={}'.\
        picVedio_url = 'http://{}/node/picVedio.htm?position_id={}&act_id={}&adzone_click_id={}&ctm_code={}&device={}&' \
                       'node_server_name=display.eqigou.com&ip=127.0.0.1'.\
            format(self.domain, int(pos), self.act_id, self.adzone_click_id, self.ctm_code, self.device)
        re_temp['url'] = picVedio_url
        picVedio_url_re = self.s.get(picVedio_url).json()
        print picVedio_url, picVedio_url_re
        if picVedio_url_re['code'] == 200 and 'ad' in picVedio_url_re['data']:
            result_tmp['award_type'] = picVedio_url_re['data']['award_type']
            result_tmp['order_id'] = picVedio_url_re['data']['ad']['order_id']
        else:
            #{code: 200,data: {record_id: "C3W1CD6H1KCA7LQW75"}}
            re_temp['result'] = '视频坑位，没有广告，谢谢参与'
        self.result_list.append(re_temp)

    def actGameLottery(self):
        # 坑位14~21的抽奖
        pos = 14
        re_temp = {}
        result_tmp = {}
        re_temp['positionId'] = int(pos)
        re_temp['result'] = result_tmp
        re_temp = {'positionId': int(pos)}
        # actGameLottery = 'https://display.{}/new/api/actGame/lottery.htm?positionId={}&act_id={}&adzone_click_id={}&' \
        actGameLottery = 'http://{}/node/actGame/lottery.htm?positionId={}&act_id={}&adzone_click_id={}&' \
                         'ctm_code={}&device={}&timeSign={}&apply_type=1&temp_name=developAct&' \
                         'node_server_name=display.eqigou.com&ip=127.0.0.1'. \
            format(self.domain, int(pos), self.act_id, self.adzone_click_id, self.ctm_code, self.device, str(int(round(time.time())*1000)))
        re_temp['url'] = actGameLottery
        actGameLottery_re = self.s.get(actGameLottery).json()
        # print actGameLottery, actGameLottery_re
        if actGameLottery_re['code'] == 200 and actGameLottery_re['data']:
            result_tmp['award_type'] = actGameLottery_re['data']['award_type']
            if actGameLottery_re['data']['award_type'] == 7:
                result_tmp['order_id'] = actGameLottery_re['data']['ad']['order_id']
        else:
            re_temp['result'] = actGameLottery_re
        self.result_list.append(re_temp)


if __name__ == '__main__':
    # lottery = checkLotteryApi('adhuec770c98d9cf423e', 'adhudong.com') #支持所有坑位
    lottery = checkLotteryApi('adhuec770c98d9cf423e', '172.16.105.11:17081') #测试环境广告位
    # lottery = checkLotteryApi('adhu5a2c9d417ef14b6e', '123.59.17.106:17280') #灰度广告位,6443
    # lottery = Lottery('adhu4041e55bb2a04fb0', 'adhudong.com') #直跳100谢谢参与
    # lottery = Lottery('adhu2dbd800e221549d4', 'adhudong.com') #直跳100幸运奖
    # lottery = Lottery('adhu2dbd800esss221549d4', 'adhudong.com') #303
    print lottery.analyze()
    # print lottery.result
    # print lottery.lottery('1')