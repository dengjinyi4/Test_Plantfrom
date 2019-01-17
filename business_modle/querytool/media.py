#!/usr/bin/env python
# encoding: utf-8
import requests,time,json,hashlib,random,string
import  db as db
import time,datetime
# 随机用户cookie参数
def tmpdaylist(days):
    d = datetime.datetime.now()
    # tmpdate_from=d+datetime.timedelta(days=-int(days))
    tmpdate_from=d+datetime.timedelta(days=-int(days))
    tmpdate_from=str(tmpdate_from)[0:10]
    daylist=tmpdate_from
    return str(daylist)
def ad_biddingpara():
    param={'pids':1,'uniq_tag':'fdfafd','ip':'172.16.148.119','cookie':'fdsafdfdaaad',
           'device':'172.16.148.119','adzone_id':101,'pos_num':'1_0','act_id':100}
    param['cookie']=''.join(random.sample(string.ascii_letters + string.digits, 8))
    return param
def get_ad_click_tag(ad_choosen_tag):
    tmpsql='''SELECT ad_click_tag FROM voyagerlog.ad_click_log{} where ad_choosen_tag='{}' '''.format(tmpdaylist(0).replace('-',''),ad_choosen_tag)
    # print tmpsql
    time.sleep(5)
    re=db.selectsql('testvoyager',tmpsql)
    return re[0][0]
# 模拟投放 展现
def ad_bidding():
    param=ad_biddingpara()
    url='http://172.16.105.11:17091/ad_bidding.do'
    s=requests.session()
    r=s.get(url,params=param)
    # print r.json()
    # print r.json()['data']['{"id":1,"positionSize":"640x300","positionType":1,"occurrenceTime":0}'][0]['adCreative']['image']
    return r,param['cookie']
# 模拟投放展现后点击点击
def ad_bidding_brige():
    r,usercookie=ad_bidding()
    url='http://172.16.105.11:17091/bridge.do'
    brigeparam={'ip':'172.16.148.119','agent':'Mozilla%2F5.0+%28Windows+NT+10.0%3B+WOW64%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F52.0.2729.4+Safari%2F537.36'
                ,'refer':'http%3A%2F%2Ft.ijifen.egou.com%3A8080%2Factivity%2F1.htm%3FlogId%3D24&','mediaId':1
                ,'adZoneId':'101','adPlanId':'3','adCreativeId':'10','userCookie':'','chargeType':'2','adzoneClickId':'111'
                ,'isCharge':'1','logType':'2','positionId':'1','adLinkUrl':'http://www.baidu.com','actId':'529'
                ,'adOrderId':'','advertiserId':'','adChoosenTag':''}
    brigeparam['adOrderId']=r.json()['data']['{"id":1,"positionSize":"640x300","positionType":1,"occurrenceTime":0}'][0]['adOrder']['id']
    brigeparam['advertiserId']=r.json()['data']['{"id":1,"positionSize":"640x300","positionType":1,"occurrenceTime":0}'][0]['adOrder']['advertiserId']
    brigeparam['adChoosenTag']=r.json()['data']['{"id":1,"positionSize":"640x300","positionType":1,"occurrenceTime":0}'][0]['tag']
    brigeparam['userCookie']=usercookie
    s=requests.session()
    result_bridge=s.get(url,params=brigeparam)
    print result_bridge.text
    return brigeparam['adChoosenTag']
# 模拟投放 点击后有效果
def ad_bidding_brige_effect():
    adChoosenTag=ad_bidding_brige()
    ad_clicktag=get_ad_click_tag(adChoosenTag)
    print ad_clicktag
    url='http://open.adhudong.com/jsonp/saveEffect.htm'
    param={'ad_click':'','type':'1','uid':999,'timestamp':''}
    param['ad_click']=ad_clicktag
    param['timestamp']=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    r=requests.session()
    re=r.get(url,params=param)
    print re.text
    return 1


if __name__ == '__main__':
    # print ad_bidding_brige()
    count=0
    while count<1:
        time.sleep(2)
        # 展现
        # ad_bidding()
        # 点击
        ad_bidding_brige()
        # ad_bidding_brige_effect()
        count=count+1
    # print tmpdaylist(0)
    # print get_ad_click_tag('D3W1CD6R1IIZXEMSKH')
