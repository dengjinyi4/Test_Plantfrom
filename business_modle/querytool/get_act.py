# -*- coding: utf-8 -*-
# @Time    : 2018/1/4 10:10
# @Author  : wanglanqing

import requests,datetime
import sys,json
from utils.db_info import *
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)

mycookies = {'adhd_wdata1':"Mi8vMzk4Ly8yLy8yLy81MDUyOC8vMTUxNTM4MzY1MDQzMi8vOGQzZGQwMWI5NGU1ZThjZjhmMWU2ZjMwZmIwM2VkMGQvLzQ2YTZlMDEzYzA0OQ%3D%3D"}

#模拟投放接口
def get_ad_simulation_info(adzoneId, adOrderId,checkedList,env_value='T'):
    '''
    传入广告位的list，如['372','412']
    输出的为每个广告位上要展示的创意、订单及对应的广告主的信息，返回类型为字典
    字典结构为：
    num：
    '''
    env_dict = {'T':'101.254.242.11:17091','P':'123.59.17.106:17200'}
    bidTime = datetime.datetime.now().strftime('%Y-%m-%d')
    adzoneId = str(adzoneId)
    adOrderId = str(adOrderId)

    re_dict={}
    if len(adzoneId)== 0 :
        return ('请输入广告位id')
    elif len(checkedList)== 0:
        return ('请勾选关键字')
    else:
        result_dict = {}
        url = "http://{0}/ad_simulation.do?positionId=1&adZoneId={1}&bidTime={2}&adOrderId={3}&occ=0".format(env_dict[env_value], adzoneId, bidTime, adOrderId)
        # print(url)
        # try:
        # print( 'result' in  (requests.get(url, cookies=mycookies).json()))
        response = requests.get(url, cookies=mycookies).json()['data']
        try:
            if isinstance(response,dict):
                response = response[adzoneId]
                # print(response)
                res_len = len(response)
                if res_len != 0:
                    for i in range(res_len):
                        re = response[i]
                        chk_dict = {'adOrderID': re['adOrder']['id'], 'adOrderName': re['adOrder']['name'],
                                    'adCreativeID': re['adCreative']['id'], 'adCreativeName': re['adCreative']['name'],
                                    'advertiserId': re['adCreative']['advertiserId'], 'tag':re['adOrder']['tag'] ,'ctr': re['ctr']}
                        tmp_list = []
                        # 筛选勾选项的内容
                        for chk in checkedList:
                            tmp_value = chk_dict[chk]
                            tmp_list.append(tmp_value)
                        result_dict[i] = tmp_list
                        # print(result_dict)
                    return result_dict
                else:
                    return '没有订单啊'
                # print response['data']
            else:
                return response
        except Exception as e:
            return e

def knowlegde():
    know = [
        [u"英文描述", u'代号', u'原因描述', u'编号', u'解决方式'],
        ["AD__REPEAT", "A", u"同一用户cookie24小时内重复展现", "0", u""],
        ["AD__UNAVAILABLE", "B", u"订单无效或当前时间不可投放", "1", u""],
        ["AD__NO_BUDGET", "C", u"今日没有预算", "2", u"在广告主前台，给广告主增加预算"],
        ["AD__LACK_BUDGET", "D", u"预算已不足", "3", u"在广告主前台，广告订单列表，修改订单的每日预算信息"],
        ["AD__WRONG_STATUS", "E", u"投放状态错误（冻结或暂停或结束）", "4", u"开启暂停状态的订单"],
        ["AD__LOW_PRICE", "F", u"出价过低", "5", u"在广告主前台，调高订单的出价"],
        ["AD__ADV_INVALID", "G", u"订单对应广告主无效或状态错误", "6", u"广告主被冻结"],
        ["AD__ADP_INVALID", "H", u"订单对应广告计划无效或错误", "7", u""],
        ["AD__ADZ_FILTER", "I", u"被此广告位定向过滤过滤", "8", u"在运营后台，查看该广告位的屏蔽信息"],
        ["AD__URL_FILTER", "J", u"被此广告位URL定向过滤", "9", u"在运营后台，查看该广告位的屏蔽信息"],
        ["AD__UNSUIT", "K", u"该订单过滤该广告位媒体", "10", u""],
        ["AD__REGION_FILTER", "L", u"被订单的地域限制过滤", "11", u""],
        ["AD__DEVICE_FILTER", "M", u"被订单的设备限制过滤", "12", u""],
        ["AD__USER_FREQ", "N", u"被用户频次限制过滤", "13", u""],
        ["AD__POS_UNSUIT", "O", u"坑位类型不匹配", "14", u""],
        ["AD__LACK_LINK", "P", u"没有广告着陆页地址", "15", u""],
        ["AD__REPEAT_LINK", "Q", u"广告链接重复", "16", u""],
        ["AD__BLOCKED_LINK", "R", u"广告着陆页域名被封", "17", u""],
        ["AD__SIMILAR_PIC", "S", u"广告图片相似", "18", u""],
        ["AD__CRE_INVALID", "T", u"创意无效或状态错误", "19", u""],
        ["AD__OCC_CONFIG", "U", u"被广告位次配置过滤", "20", u""],
        ["AD__NO_HOUR_BUDGET", "V", u"没有小时预算", "21", u""],
        ["AD__LACK_HOUR_BUDGET","W", u"小时预算不足", "22",u""],
        ["AD_Z_CRE_LV_UNSUIT", "X", u"广告位和广告创意等级不匹配", "23", u""],
        ["AD__SEC_TIME_FILTER", "Y", u"隐藏过滤时间", "24", u""],
        ["AD__SEC_REG_FILTER", "Z", u"隐藏过滤地域", "25", u""],
        ["AD__QUALITY_FILTER", "a", u"广告订单媒体资质定向不符", "27", u""],
        ["AD__MEDADZ_FILTER", "b", u"广告订单媒体广告位定向不符", "28",u""]
    ]
    # know='同一用户cookie24小时内重复展现'
    return know

def get_tuodi_ads():
    # sql = "select `value` from voyager.config_parameters where id=13"
    sql = "select * from voyager.config_parameters where id=13"
    ads = DbOperations().execute_sql(sql)[0][3]
    ads_list=[]
    # print(ads)
    print()
    ads_tmp = (ads).split(',')
    print(ads_tmp)
    for i in range(len(ads_tmp)):
        ads_list.append(ads_tmp[i].split('/')[0])
    return ads_list

def get_info():
    url="http://123.59.17.106:17200/ad_simulation.do?positionId=1&adZoneId=1370&bidTime=2018-05-03&adOrderId="
    aos=['16495',
'14549',
'16241',
'13428',
'13429',
'14386',
'16479',
'17377',
'17378',
'17528',
'17952',
'17953',
'14033',
'14862',
'16398',
'17523',
'17731',
'17910',
'18017',
'11632',
'13957',
'17150',
'17979',
'16162',
'17622',
'13376',
'14831',
'14833',
'16379',
'14634',
'14670',
'14863',
'15033',
'15488',
'16207',
'14807',
'14846',
'14847',
'15053',
'15073',
'15218',
'15659',
'16404',
'16405',
'14942',
'14946',
'15500',
'17047',
'17083',
'15264',
'15647',
'17665',
'17680',
'17913',
'17983']
    for item in aos:
        print(item +' results:')
        url_new = url+str(item)
        re= requests.get(url_new).text
        print(re)


if __name__=='__main__':
    #模拟投放接口
    # get_ad_simulation_info(['371', '372'])
    # print(get_ad_simulation_info(372,'',['adOrderID','adOrderName','adCreativeID'],'T'))
    # get_tuodi_ads()
    get_info()


